"""
Chatbot Verbatims Collector - Recopilación y análisis de verbatims de clientes
Procesa comentarios de texto libre para extraer insights cualitativos sobre NPS
"""

import pandas as pd
import re
import os
import jwt
from typing import Dict, List, Tuple, Optional, Any, Union
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# Simple token management without Selenium automation


class ChatbotVerbatimsCollector:
    """
    Recopilador y analizador de verbatims de chatbot y otras fuentes de feedback
    """
    
    def __init__(self, pbi_collector=None, token: str = None):
        """
        Initialize the Chatbot Verbatims Collector
        
        Args:
            pbi_collector: Power BI data collector instance (fallback mode)
            token: JWT token for user authentication (from frontend)
        """
        self.pbi_collector = pbi_collector
        self.token = token
        
        # Simple token management
        self.token_file = "dashboard_analyzer/temp_aws_credentials.env"
        self.token_expired = False
        
        # Load token from file if not provided
        if not self.token:
            self.token = self._load_token_from_file()
        
        # Validate token on initialization
        if self.token:
            self._validate_token()

    def _load_token_from_file(self) -> str:
        """Load token from temp_aws_credentials.env file"""
        try:
            if os.path.exists(self.token_file):
                with open(self.token_file, 'r') as f:
                    for line in f:
                        if 'chatbot_jwt_token' in line and '=' in line:
                            token = line.split('=', 1)[1].strip()
                            logger.info("✅ Token loaded from file")
                            return token
            logger.warning("⚠️ No token found in file")
            return None
        except Exception as e:
            logger.error(f"❌ Error loading token from file: {e}")
            return None
        
        # Diccionarios para análisis temático
        self.route_patterns = [
            r'\b[A-Z]{3}[- ]?[A-Z]{3}\b',  # MAD-BCN, MADBCN
            r'\b[A-Z]{3}\s?-\s?[A-Z]{3}\b',  # MAD - BCN
            r'\bvuelo\s+[A-Z0-9]+\b',  # vuelo IB1234
            r'\bruta\s+[A-Z]{3}[- ]?[A-Z]{3}\b'  # ruta MAD-BCN
        ]
        
        self.theme_keywords = {
            'equipaje': [
                'maleta', 'equipaje', 'baggage', 'perdido', 'dañado', 
                'retraso equipaje', 'facturación', 'peso equipaje'
            ],
            'puntualidad': [
                'retraso', 'delay', 'tarde', 'puntual', 'cancelado', 
                'cambio horario', 'salida', 'llegada', 'conexión'
            ],
            'servicio_abordo': [
                'azafata', 'tripulación', 'comida', 'bebida', 'asiento',
                'entretenimiento', 'wifi', 'servicio', 'atención', 'cortesía'
            ],
            'reservas': [
                'reserva', 'booking', 'web', 'app', 'cambio vuelo',
                'cancelación', 'precio', 'tarifa', 'clase'
            ],
            'check_in': [
                'check-in', 'facturación', 'embarque', 'puerta',
                'boarding', 'mostrador', 'online check-in'
            ],
            'aeropuerto': [
                'terminal', 'puerta', 'mostrador', 'sala', 'espera',
                'seguridad', 'migración', 'aduana'
            ]
        }
        
        # Palabras indicadoras de sentimiento
        self.sentiment_positive = [
            'excelente', 'perfecto', 'fantástico', 'genial', 'bueno',
            'satisfecho', 'contento', 'recomiendo', 'gracias', 'amable'
        ]
        
        self.sentiment_negative = [
            'horrible', 'terrible', 'malo', 'pésimo', 'desastroso',
            'molesto', 'furioso', 'decepcionado', 'nunca más', 'awful'
        ]
    
    def _validate_token(self) -> bool:
        """
        Validates the current JWT token and checks if it's expired
        Returns True if token is valid, False if expired
        """
        try:
            if not self.token:
                return False
            
            # Decode JWT to check expiry (without signature verification)
            decoded = jwt.decode(self.token, options={"verify_signature": False})
            exp_timestamp = decoded.get('exp')
            
            if not exp_timestamp:
                logger.warning("Token has no expiration time")
                return False
            
            # Check if token is expired
            current_time = datetime.utcnow().timestamp()
            time_until_expiry = exp_timestamp - current_time
            
            if time_until_expiry <= 0:
                logger.warning("Token has expired")
                self.token_expired = True
                self._handle_token_expiration()
                return False
            
            # Check if token expires soon
            if time_until_expiry <= self.token_refresh_threshold:
                logger.warning(f"Token expires in {time_until_expiry:.0f} seconds")
                self._handle_token_expiration()
                return False
            
            self.token_expired = False
            return True
            
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired (signature error)")
            self.token_expired = True
            self._handle_token_expiration()
            return False
        except Exception as e:
            logger.error(f"Error validating token: {e}")
            return False
    
    def _handle_token_expiration(self):
        """
        Handles token expiration by trying to reload from file, then falling back to PBI
        """
        try:
            # Try to reload token from file (user may have updated it manually)
            if self._reload_token_from_file():
                logger.info("✅ Token reloaded from file successfully")
                return
            
            # If token reload fails, mark as expired and fall back to PBI
            logger.warning("⚠️ Token expired and could not be reloaded - will use PBI fallback")
            self.token_expired = True
                
        except Exception as e:
            logger.error(f"Error handling token expiration: {e}")
            self.token_expired = True
    
    def _reload_token_from_file(self) -> bool:
        """
        Attempts to reload the token from the credentials file
        Returns True if successful, False otherwise
        """
        try:
            if not os.path.exists(self.token_file):
                logger.warning(f"Token file {self.token_file} not found")
                return False
            
            # Read fresh token from file
            with open(self.token_file, 'r') as f:
                for line in f:
                    if line.startswith('chatbot_jwt_token ='):
                        new_token = line.split('=', 1)[1].strip().strip('"\'')
                        
                        # Validate new token
                        if self._is_valid_token(new_token):
                            self.token = new_token
                            self.token_expired = False
                            logger.info("✅ Token reloaded from file")
                            return True
                        else:
                            logger.warning("New token from file is also expired")
                            return False
            
            logger.warning("No valid token found in credentials file")
            return False
            
        except Exception as e:
            logger.error(f"Error reloading token from file: {e}")
            return False
    
    def _is_valid_token(self, token: str) -> bool:
        """
        Checks if a token is valid without setting it as the current token
        """
        try:
            if not token:
                return False
            
            decoded = jwt.decode(token, options={"verify_signature": False})
            exp_timestamp = decoded.get('exp')
            
            if not exp_timestamp:
                return False
            
            current_time = datetime.utcnow().timestamp()
            return exp_timestamp > current_time
            
        except Exception:
            return False
    
    def ensure_valid_token(self) -> bool:
        """
        Public method to ensure token is valid before operations
        Returns True if token is valid, False if expired
        """
        return self._validate_token()
    
    def get_token_status(self) -> Dict[str, Any]:
        """
        Returns current token status information
        """
        try:
            if not self.token:
                return {
                    'status': 'no_token',
                    'message': 'No token available',
                    'expires_in': None,
                    'expired': True
                }
            
            decoded = jwt.decode(self.token, options={"verify_signature": False})
            exp_timestamp = decoded.get('exp')
            
            if not exp_timestamp:
                return {
                    'status': 'invalid_token',
                    'message': 'Token has no expiration time',
                    'expires_in': None,
                    'expired': True
                }
            
            current_time = datetime.utcnow().timestamp()
            time_until_expiry = exp_timestamp - current_time
            
            if time_until_expiry <= 0:
                return {
                    'status': 'expired',
                    'message': 'Token has expired',
                    'expires_in': 0,
                    'expired': True
                }
            
            return {
                'status': 'valid',
                'message': 'Token is valid',
                'expires_in': int(time_until_expiry),
                'expired': False,
                'expires_at': datetime.fromtimestamp(exp_timestamp).isoformat()
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error checking token: {str(e)}',
                'expires_in': None,
                'expired': True
            }
    
    def _make_api_request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """
        Placeholder method for API requests - not used in current implementation
        This method exists for future API integration if needed
        """
        logger.warning("API requests not implemented - using PBI collector fallback")
        return None
    
    def _collect_from_chatbot_api(self, date_range: Tuple[str, str], node_path: str, 
                                 filters: Optional[Dict] = None) -> pd.DataFrame:
        """
        Placeholder method for chatbot API collection - not used in current implementation
        This method exists for future API integration if needed
        """
        logger.warning("Chatbot API collection not implemented - using PBI collector fallback")
        return pd.DataFrame()
    
    def collect_verbatims_for_period(self, date_range: Tuple[str, str], node_path: str,
                                   filters: Optional[Dict] = None) -> pd.DataFrame:
        """
        Recopila verbatims para el período especificado
        
        Args:
            date_range: Tupla con (start_date, end_date)
            node_path: Ruta del nodo en el árbol jerárquico
            filters: Filtros adicionales (sentiment, themes, etc.)
        
        Returns:
            DataFrame con verbatims procesados
        """
        try:
            # Intentar obtener verbatims de la API del chatbot primero
            if self.ensure_valid_token(): # Use ensure_valid_token here
                verbatims_data = self._collect_from_chatbot_api(date_range, node_path, filters)
                if not verbatims_data.empty:
                    logger.info(f"✅ Collected {len(verbatims_data)} verbatims from chatbot API")
                    return verbatims_data
                else:
                    logger.warning("Chatbot API returned no data, falling back to PBI collector")
            
            # Fallback al Power BI collector
            if self.pbi_collector:
                from datetime import datetime
                start_dt = datetime.strptime(date_range[0], '%Y-%m-%d')
                end_dt = datetime.strptime(date_range[1], '%Y-%m-%d')
                
                verbatims_data = self.pbi_collector.collect_verbatims_for_date_range(
                    node_path=node_path,
                    start_date=start_dt,
                    end_date=end_dt
                )
                
                if verbatims_data.empty:
                    logger.warning(f"No verbatims data found for period {date_range}")
                    return pd.DataFrame()
                
                # Procesar verbatims
                processed_verbatims = self._process_verbatims(verbatims_data)
                
                # Aplicar filtros si se especifican
                if filters:
                    processed_verbatims = self._apply_filters(processed_verbatims, filters)
                
                return processed_verbatims
            else:
                logger.error("No data source available (neither chatbot API nor PBI collector)")
                return pd.DataFrame()
            
        except Exception as e:
            logger.error(f"Error collecting verbatims for period {date_range}: {e}")
            return pd.DataFrame()
    
    def analyze_sentiment(self, verbatim_text: str) -> Dict[str, Any]:
        """
        Analiza el sentimiento de un verbatim individual
        
        Args:
            verbatim_text: Texto del verbatim
        
        Returns:
            Dict con análisis de sentimiento
        """
        try:
            if not verbatim_text or pd.isna(verbatim_text):
                return {'score': 0.0, 'category': 'neutral', 'confidence': 0.0}
            
            text_lower = verbatim_text.lower()
            
            # Contar palabras positivas y negativas
            positive_count = sum(1 for word in self.sentiment_positive if word in text_lower)
            negative_count = sum(1 for word in self.sentiment_negative if word in text_lower)
            
            # Calcular score simple (-1 a 1)
            total_sentiment_words = positive_count + negative_count
            if total_sentiment_words == 0:
                sentiment_score = 0.0
                category = 'neutral'
                confidence = 0.0
            else:
                sentiment_score = (positive_count - negative_count) / len(text_lower.split())
                confidence = min(total_sentiment_words / len(text_lower.split()) * 2, 1.0)
                
                if sentiment_score > 0.01:
                    category = 'positive'
                elif sentiment_score < -0.01:
                    category = 'negative'
                else:
                    category = 'neutral'
            
            return {
                'score': round(sentiment_score, 3),
                'category': category,
                'confidence': round(confidence, 3),
                'positive_words': positive_count,
                'negative_words': negative_count
            }
            
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return {'score': 0.0, 'category': 'neutral', 'confidence': 0.0}
    
    def extract_routes_mentions(self, verbatims_df: pd.DataFrame) -> pd.DataFrame:
        """
        Extrae menciones de rutas en los verbatims
        
        Args:
            verbatims_df: DataFrame con verbatims
        
        Returns:
            DataFrame con rutas mencionadas
        """
        try:
            routes_mentioned = []
            
            for _, verbatim in verbatims_df.iterrows():
                text = str(verbatim.get('verbatim_text', ''))
                verbatim_id = verbatim.get('verbatim_id', '')
                
                # Buscar patrones de rutas
                found_routes = []
                for pattern in self.route_patterns:
                    matches = re.findall(pattern, text.upper())
                    found_routes.extend(matches)
                
                # Limpiar y normalizar rutas encontradas
                for route in found_routes:
                    clean_route = self._normalize_route(route)
                    if clean_route:
                        routes_mentioned.append({
                            'verbatim_id': verbatim_id,
                            'route_mentioned': clean_route,
                            'original_text': route,
                            'verbatim_text': text[:200],  # Primeros 200 caracteres
                            'sentiment_score': verbatim.get('sentiment_score', 0),
                            'date': verbatim.get('date', None),
                            'nps_score': verbatim.get('nps_score', None)
                        })
            
            if routes_mentioned:
                return pd.DataFrame(routes_mentioned)
            else:
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"Error extracting route mentions: {e}")
            return pd.DataFrame()
    
    def categorize_themes(self, verbatims_df: pd.DataFrame) -> pd.DataFrame:
        """
        Categoriza verbatims por temas
        
        Args:
            verbatims_df: DataFrame con verbatims
        
        Returns:
            DataFrame con categorías temáticas
        """
        try:
            verbatims_with_themes = verbatims_df.copy()
            
            # Inicializar columnas de temas
            for theme in self.theme_keywords.keys():
                verbatims_with_themes[f'theme_{theme}'] = False
                verbatims_with_themes[f'theme_{theme}_count'] = 0
            
            verbatims_with_themes['primary_theme'] = 'otros'
            verbatims_with_themes['theme_confidence'] = 0.0
            
            for idx, verbatim in verbatims_with_themes.iterrows():
                text = str(verbatim.get('verbatim_text', '')).lower()
                
                theme_scores = {}
                
                # Contar menciones por tema
                for theme, keywords in self.theme_keywords.items():
                    count = sum(1 for keyword in keywords if keyword in text)
                    verbatims_with_themes.loc[idx, f'theme_{theme}'] = count > 0
                    verbatims_with_themes.loc[idx, f'theme_{theme}_count'] = count
                    
                    if count > 0:
                        theme_scores[theme] = count
                
                # Determinar tema principal
                if theme_scores:
                    primary_theme = max(theme_scores, key=theme_scores.get)
                    verbatims_with_themes.loc[idx, 'primary_theme'] = primary_theme
                    
                    # Calcular confianza (normalizada por longitud del texto)
                    max_score = theme_scores[primary_theme]
                    text_length = len(text.split())
                    confidence = min(max_score / max(text_length, 1) * 10, 1.0)
                    verbatims_with_themes.loc[idx, 'theme_confidence'] = round(confidence, 3)
            
            return verbatims_with_themes
            
        except Exception as e:
            logger.error(f"Error categorizing themes: {e}")
            return verbatims_df
    
    def filter_by_sentiment(self, verbatims_df: pd.DataFrame, 
                          sentiment_threshold: float = 0.0,
                          sentiment_type: str = 'all') -> pd.DataFrame:
        """
        Filtra verbatims por sentimiento
        
        Args:
            verbatims_df: DataFrame con verbatims
            sentiment_threshold: Umbral de sentimiento (-1 a 1)
            sentiment_type: 'positive', 'negative', 'neutral', 'all'
        
        Returns:
            DataFrame filtrado
        """
        try:
            if verbatims_df.empty:
                return verbatims_df
            
            filtered_df = verbatims_df.copy()
            
            if sentiment_type == 'positive':
                filtered_df = filtered_df[filtered_df['sentiment_score'] > sentiment_threshold]
            elif sentiment_type == 'negative':
                filtered_df = filtered_df[filtered_df['sentiment_score'] < -abs(sentiment_threshold)]
            elif sentiment_type == 'neutral':
                filtered_df = filtered_df[
                    (filtered_df['sentiment_score'] >= -abs(sentiment_threshold)) &
                    (filtered_df['sentiment_score'] <= abs(sentiment_threshold))
                ]
            # 'all' no aplica filtro
            
            return filtered_df
            
        except Exception as e:
            logger.error(f"Error filtering by sentiment: {e}")
            return verbatims_df
    
    def get_verbatims_summary(self, verbatims_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Genera resumen estadístico de verbatims
        
        Args:
            verbatims_df: DataFrame con verbatims procesados
        
        Returns:
            Dict con resumen estadístico
        """
        try:
            if verbatims_df.empty:
                return {
                    'total_verbatims': 0,
                    'summary': 'No hay verbatims disponibles'
                }
            
            total_verbatims = len(verbatims_df)
            
            # Análisis de sentimiento
            sentiment_counts = verbatims_df['sentiment_category'].value_counts().to_dict()
            avg_sentiment = verbatims_df['sentiment_score'].mean()
            
            # Análisis temático
            theme_columns = [col for col in verbatims_df.columns if col.startswith('theme_') and col.endswith('_count')]
            theme_summary = {}
            
            for col in theme_columns:
                theme_name = col.replace('theme_', '').replace('_count', '')
                mentions = verbatims_df[verbatims_df[col] > 0]
                if len(mentions) > 0:
                    theme_summary[theme_name] = {
                        'verbatims_count': len(mentions),
                        'avg_sentiment': mentions['sentiment_score'].mean()
                    }
            
            # Rutas más mencionadas
            routes_mentioned = []
            if 'routes_mentioned' in verbatims_df.columns:
                route_mentions = verbatims_df['routes_mentioned'].value_counts().head(5)
                routes_mentioned = route_mentions.to_dict()
            
            summary_text = f"Total: {total_verbatims} verbatims. "
            summary_text += f"Sentimiento promedio: {round(avg_sentiment, 2)}. "
            
            if sentiment_counts:
                sentiment_desc = []
                for category, count in sentiment_counts.items():
                    pct = round(count / total_verbatims * 100, 1)
                    sentiment_desc.append(f"{category}: {count} ({pct}%)")
                summary_text += "Distribución: " + ", ".join(sentiment_desc) + ". "
            
            if theme_summary:
                top_theme = max(theme_summary.items(), key=lambda x: x[1]['verbatims_count'])
                summary_text += f"Tema principal: {top_theme[0]} ({top_theme[1]['verbatims_count']} menciones)."
            
            return {
                'total_verbatims': total_verbatims,
                'sentiment_distribution': sentiment_counts,
                'average_sentiment': round(avg_sentiment, 3),
                'themes_summary': theme_summary,
                'top_routes_mentioned': routes_mentioned,
                'summary': summary_text
            }
            
        except Exception as e:
            logger.error(f"Error generating verbatims summary: {e}")
            return {
                'total_verbatims': 0,
                'summary': f'Error generando resumen: {str(e)}'
            }
    
    def _process_verbatims(self, verbatims_df: pd.DataFrame) -> pd.DataFrame:
        """Procesa verbatims aplicando análisis de sentimiento y limpieza"""
        try:
            processed_df = verbatims_df.copy()
            
            # Limpiar texto
            processed_df['verbatim_text_clean'] = processed_df['verbatim_text'].apply(self._clean_text)
            
            # Análisis de sentimiento
            sentiment_results = processed_df['verbatim_text_clean'].apply(self.analyze_sentiment)
            
            # Expandir resultados de sentimiento
            processed_df['sentiment_score'] = [result['score'] for result in sentiment_results]
            processed_df['sentiment_category'] = [result['category'] for result in sentiment_results]
            processed_df['sentiment_confidence'] = [result['confidence'] for result in sentiment_results]
            
            # Categorizar por temas
            processed_df = self.categorize_themes(processed_df)
            
            # Extraer menciones de rutas
            route_mentions = self.extract_routes_mentions(processed_df)
            if not route_mentions.empty:
                # Agregar información de rutas mencionadas
                route_counts = route_mentions.groupby('verbatim_id')['route_mentioned'].apply(list).to_dict()
                processed_df['routes_mentioned'] = processed_df.get('verbatim_id', processed_df.index).map(route_counts)
                processed_df['routes_mentioned'] = processed_df['routes_mentioned'].fillna('').apply(
                    lambda x: x if isinstance(x, list) else []
                )
            else:
                processed_df['routes_mentioned'] = [[] for _ in range(len(processed_df))]
            
            return processed_df
            
        except Exception as e:
            logger.error(f"Error processing verbatims: {e}")
            return verbatims_df
    
    def _clean_text(self, text: str) -> str:
        """Limpia y normaliza texto de verbatims"""
        try:
            if not text or pd.isna(text):
                return ""
            
            # Convertir a string y minúsculas
            clean_text = str(text).lower()
            
            # Remover caracteres especiales pero mantener espacios y puntuación básica
            clean_text = re.sub(r'[^\w\s\.\,\!\?\-]', ' ', clean_text)
            
            # Normalizar espacios
            clean_text = re.sub(r'\s+', ' ', clean_text).strip()
            
            return clean_text
            
        except Exception as e:
            logger.error(f"Error cleaning text: {e}")
            return str(text) if text else ""
    
    def _normalize_route(self, route_text: str) -> str:
        """Normaliza formato de rutas extraídas"""
        try:
            if not route_text:
                return ""
            
            # Remover espacios y guiones extra
            clean_route = re.sub(r'[^\w]', '', route_text.upper())
            
            # Verificar que tenga formato de ruta (6 caracteres)
            if len(clean_route) == 6 and clean_route.isalpha():
                return f"{clean_route[:3]}-{clean_route[3:]}"
            
            return ""
            
        except Exception as e:
            logger.error(f"Error normalizing route: {e}")
            return ""
    
    def _apply_filters(self, verbatims_df: pd.DataFrame, filters: Dict) -> pd.DataFrame:
        """Aplica filtros específicos a los verbatims"""
        try:
            filtered_df = verbatims_df.copy()
            
            # Filtro por sentimiento
            if 'sentiment_type' in filters:
                sentiment_threshold = filters.get('sentiment_threshold', 0.0)
                filtered_df = self.filter_by_sentiment(
                    filtered_df, 
                    sentiment_threshold, 
                    filters['sentiment_type']
                )
            
            # Filtro por tema
            if 'theme' in filters:
                theme = filters['theme']
                if f'theme_{theme}' in filtered_df.columns:
                    filtered_df = filtered_df[filtered_df[f'theme_{theme}'] == True]
            
            # Filtro por ruta mencionada
            if 'route_mentioned' in filters:
                route = filters['route_mentioned']
                filtered_df = filtered_df[
                    filtered_df['routes_mentioned'].apply(lambda x: route in x if isinstance(x, list) else False)
                ]
            
            # Filtro por NPS score mínimo
            if 'min_nps' in filters and 'nps_score' in filtered_df.columns:
                filtered_df = filtered_df[filtered_df['nps_score'] >= filters['min_nps']]
            
            return filtered_df
            
        except Exception as e:
            logger.error(f"Error applying filters: {e}")
            return verbatims_df

    def test_connection(self) -> tuple[bool, str]:
        """
        Test connection to the verbatims data source.
        Returns (success: bool, message: str)
        """
        try:
            # Test token validity first
            if self.ensure_valid_token():
                status = self.get_token_status()
                expires_in = status.get('expires_in', 'Unknown')
                return True, f"✅ Token is valid - expires in {expires_in}s"
            else:
                # Check if PBI fallback is available
                if hasattr(self, 'pbi_collector') and self.pbi_collector:
                    return True, "✅ Verbatims collector ready (using PBI fallback)"
                else:
                    return False, "❌ No data source available (neither valid token nor PBI collector)"
                
        except Exception as e:
            return False, f"❌ Connection test failed: {str(e)}"

    def get_verbatims_data(self, start_date: str, end_date: str, node_path: str, verbatim_type: str = None, intelligent_query: str = None) -> pd.DataFrame:
        """
        Get verbatims data for the specified period and node path.
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format  
            node_path: Node path for filtering
            verbatim_type: Type of verbatim (optional)
            intelligent_query: Intelligent query for filtering verbatims (optional)
            
        Returns:
            DataFrame with verbatims data
        """
        try:
            # Convert string dates to datetime
            from datetime import datetime
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
            
            # Use existing collect_verbatims_for_period method
            date_range = (start_date, end_date)
            
            # Prepare filters
            filters = {}
            if verbatim_type:
                filters["verbatim_type"] = verbatim_type
            
            # Call the existing method with appropriate parameters
            df = self.collect_verbatims_for_period(
                date_range=date_range,
                node_path=node_path,
                filters=filters
            )
            
            # Apply intelligent query filtering if provided
            if intelligent_query and not df.empty:
                df = self._apply_intelligent_query_filter(df, intelligent_query)
            
            return df
            
        except Exception as e:
            logger.error(f"Error getting verbatims data: {e}")
            return pd.DataFrame()  # Return empty DataFrame on error

    def _apply_intelligent_query_filter(self, df: pd.DataFrame, intelligent_query: str) -> pd.DataFrame:
        """
        Apply intelligent query filtering to verbatims data.
        Enhanced with specific handling for route-based queries and representative comments.
        
        Args:
            df: DataFrame with verbatims data
            intelligent_query: Query string to filter by
            
        Returns:
            Filtered DataFrame with enhanced route and sentiment analysis
        """
        try:
            if df.empty or not intelligent_query:
                return df
            
            # Normalize query for better matching
            query_lower = intelligent_query.lower()
            
            # Check for specific query types based on new verbatims questions
            if 'rutas' in query_lower and 'negativ' in query_lower:
                # Question 1: Routes with most negative comments
                return self._filter_routes_negative_comments(df)
            elif 'comentarios' in query_lower and 'representativ' in query_lower:
                # Question 2: Representative comments for each route
                return self._filter_representative_comments(df)
            else:
                # Use enhanced general filtering
                return self._filter_general_intelligent_query(df, intelligent_query)
            
        except Exception as e:
            logger.error(f"Error applying intelligent query filter: {e}")
            return df

    def _filter_routes_negative_comments(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Filter and analyze routes with most negative comments.
        Returns DataFrame with route analysis and negative sentiment focus.
        """
        try:
            if df.empty:
                return df
                
            # Focus on negative sentiment
            text_col = self._get_text_column(df)
            if not text_col:
                return df
                
            # Filter for negative sentiment using keywords and sentiment score
            negative_keywords = [
                'horrible', 'terrible', 'malo', 'pésimo', 'desastroso', 'awful',
                'molesto', 'furioso', 'decepcionado', 'nunca más', 'worst',
                'retraso', 'delay', 'cancelado', 'perdido', 'dañado', 'sucio',
                'mal servicio', 'bad service', 'poor', 'disappointing'
            ]
            
            # Create negative sentiment mask
            negative_pattern = '|'.join(negative_keywords)
            mask = df[text_col].str.lower().str.contains(negative_pattern, na=False, regex=True)
            
            # Also consider sentiment score if available
            if 'sentiment_score' in df.columns:
                # Sentiment scores typically range from -1 to 1, negatives are < 0
                mask = mask | (df['sentiment_score'] < -0.2)
            elif 'sentiment_category' in df.columns:
                # If categorical sentiment available
                mask = mask | (df['sentiment_category'].str.lower().isin(['negative', 'very negative', 'negativo']))
            
            negative_df = df[mask]
            
            # Extract and analyze routes
            negative_df = self._enhance_route_extraction(negative_df)
            
            logger.info(f"🔍 Found {len(negative_df)} negative verbatims from {len(df)} total")
            return negative_df
            
        except Exception as e:
            logger.error(f"Error filtering negative routes: {e}")
            return df

    def _filter_representative_comments(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Filter for most representative comments per route.
        Returns diverse, informative comments that best represent issues.
        """
        try:
            if df.empty:
                return df
                
            text_col = self._get_text_column(df)
            if not text_col:
                return df
                
            # Enhance route extraction first
            df = self._enhance_route_extraction(df)
            
            # Select representative comments based on criteria:
            # 1. Word count (not too short, not too long)
            # 2. Clear sentiment
            # 3. Specific issues mentioned
            # 4. Route diversity
            
            # Filter by word count (meaningful comments)
            if 'word_count' not in df.columns:
                df['word_count'] = df[text_col].str.split().str.len()
            
            # Keep comments with reasonable length (10-100 words for readability)
            mask = (df['word_count'] >= 10) & (df['word_count'] <= 100)
            filtered_df = df[mask]
            
            # If we have route information, try to get diverse examples
            if 'extracted_route' in filtered_df.columns:
                route_samples = []
                for route in filtered_df['extracted_route'].dropna().unique():
                    route_comments = filtered_df[filtered_df['extracted_route'] == route]
                    # Take top 3 most descriptive comments per route
                    if len(route_comments) > 0:
                        # Sort by word count (prefer moderately detailed comments)
                        top_comments = route_comments.nlargest(3, 'word_count')
                        route_samples.append(top_comments)
                
                if route_samples:
                    filtered_df = pd.concat(route_samples, ignore_index=True)
            else:
                # If no routes, select most informative comments overall
                filtered_df = filtered_df.nlargest(min(20, len(filtered_df)), 'word_count')
            
            logger.info(f"🔍 Selected {len(filtered_df)} representative comments from {len(df)} total")
            return filtered_df
            
        except Exception as e:
            logger.error(f"Error filtering representative comments: {e}")
            return df

    def _filter_general_intelligent_query(self, df: pd.DataFrame, intelligent_query: str) -> pd.DataFrame:
        """
        Enhanced general filtering for other intelligent queries.
        """
        try:
            query_lower = intelligent_query.lower()
            
            # Enhanced keyword mappings
            keyword_mappings = {
                'retraso': ['retraso', 'delay', 'tarde', 'puntualidad', 'cancelado', 'atrasado'],
                'equipaje': ['maleta', 'equipaje', 'baggage', 'perdido', 'dañado', 'facturación'],
                'servicio': ['servicio', 'atención', 'tripulación', 'azafata', 'personal', 'crew'],
                'comida': ['comida', 'bebida', 'catering', 'menú', 'desayuno', 'almuerzo', 'food'],
                'asiento': ['asiento', 'seat', 'espacio', 'cómodo', 'incómodo', 'comfort'],
                'entretenimiento': ['wifi', 'entretenimiento', 'pantalla', 'película', 'música', 'entertainment'],
                'conexión': ['conexión', 'transbordo', 'escala', 'connecting', 'connection'],
                'limpieza': ['limpio', 'sucio', 'limpieza', 'higiene', 'clean', 'dirty'],
                'precio': ['precio', 'caro', 'barato', 'tarifa', 'coste', 'price', 'expensive'],
                'reserva': ['reserva', 'booking', 'cambio', 'modificar', 'cancelar', 'reservation'],
                'aeropuerto': ['aeropuerto', 'airport', 'terminal', 'puerta', 'gate', 'security'],
                'boarding': ['embarque', 'boarding', 'puerta', 'gate', 'priority', 'zones']
            }
            
            # Extract keywords from query
            relevant_keywords = []
            for category, keywords in keyword_mappings.items():
                if any(keyword in query_lower for keyword in keywords):
                    relevant_keywords.extend(keywords)
            
            # If no specific keywords found, use query terms directly
            if not relevant_keywords:
                relevant_keywords = [word.strip() for word in query_lower.split() if len(word.strip()) > 2]
            
            # Filter verbatims
            text_col = self._get_text_column(df)
            if relevant_keywords and text_col:
                pattern = '|'.join([re.escape(keyword) for keyword in relevant_keywords])
                mask = df[text_col].str.lower().str.contains(pattern, na=False, regex=True)
                filtered_df = df[mask]
                
                logger.info(f"🔍 General query '{intelligent_query}' filtered {len(df)} -> {len(filtered_df)} verbatims")
                return filtered_df
            
            return df
            
        except Exception as e:
            logger.error(f"Error in general intelligent query filter: {e}")
            return df

    def _get_text_column(self, df: pd.DataFrame) -> str:
        """Get the name of the text column in the DataFrame"""
        possible_names = ['verbatim_text', 'Verbatim_Text', 'text', 'comment', 'feedback']
        for col in possible_names:
            if col in df.columns:
                return col
        return None

    def _enhance_route_extraction(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Enhanced route extraction from verbatim text.
        Adds 'extracted_route' column with identified routes.
        """
        try:
            text_col = self._get_text_column(df)
            if not text_col:
                return df
                
            # Improved route patterns
            route_patterns = [
                r'\b([A-Z]{3})\s*[-–—]\s*([A-Z]{3})\b',  # MAD-BCN, MAD – BCN
                r'\b([A-Z]{3})\s+to\s+([A-Z]{3})\b',      # MAD to BCN
                r'\b([A-Z]{3})\s*>\s*([A-Z]{3})\b',       # MAD > BCN
                r'\bfrom\s+([A-Z]{3})\s+to\s+([A-Z]{3})\b', # from MAD to BCN
                r'\b([A-Z]{3})[/\\]([A-Z]{3})\b',         # MAD/BCN, MAD\BCN
            ]
            
            extracted_routes = []
            for text in df[text_col].fillna(''):
                route_found = None
                for pattern in route_patterns:
                    matches = re.finditer(pattern, str(text).upper())
                    for match in matches:
                        origin, dest = match.groups()
                        route_found = f"{origin}-{dest}"
                        break
                    if route_found:
                        break
                extracted_routes.append(route_found)
            
            df = df.copy()  # Create a copy to avoid SettingWithCopyWarning
            df['extracted_route'] = extracted_routes
            
            # Log route extraction stats
            routes_found = sum(1 for route in extracted_routes if route)
            logger.info(f"🛫 Extracted routes from {routes_found}/{len(df)} verbatims")
            
            return df
            
        except Exception as e:
            logger.error(f"Error enhancing route extraction: {e}")
            return df  # Return original data on error 