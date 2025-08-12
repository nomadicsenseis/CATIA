"""
Chatbot Verbatims Collector - Recopilación y análisis de verbatims de clientes
Procesa comentarios de texto libre para extraer insights cualitativos sobre NPS
"""

import pandas as pd
import re
from typing import Dict, List, Tuple, Optional, Any
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class ChatbotVerbatimsCollector:
    """
    Recopilador y analizador de verbatims de chatbot y otras fuentes de feedback
    """
    
    def __init__(self, pbi_collector):
        """
        Initialize the Chatbot Verbatims Collector
        
        Args:
            pbi_collector: Power BI data collector instance
        """
        self.pbi_collector = pbi_collector
        
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
            # Obtener verbatims base del Power BI
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
            # For now, we'll test by checking if PBI collector is available
            if hasattr(self, 'pbi_collector') and self.pbi_collector:
                return True, "✅ Verbatims collector ready (using PBI fallback)"
            else:
                return False, "❌ PBI collector not available"
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
        Uses keyword matching and semantic analysis to filter relevant verbatims.
        
        Args:
            df: DataFrame with verbatims data
            intelligent_query: Query string to filter by
            
        Returns:
            Filtered DataFrame
        """
        try:
            if df.empty or not intelligent_query:
                return df
            
            # Normalize query for better matching
            query_lower = intelligent_query.lower()
            
            # Define keyword mappings for common queries
            keyword_mappings = {
                'retraso': ['retraso', 'delay', 'tarde', 'puntualidad', 'cancelado'],
                'equipaje': ['maleta', 'equipaje', 'baggage', 'perdido', 'dañado'],
                'servicio': ['servicio', 'atención', 'tripulación', 'azafata', 'personal'],
                'comida': ['comida', 'bebida', 'catering', 'menú', 'desayuno', 'almuerzo'],
                'asiento': ['asiento', 'seat', 'espacio', 'cómodo', 'incómodo'],
                'entretenimiento': ['wifi', 'entretenimiento', 'pantalla', 'película', 'música'],
                'conexión': ['conexión', 'transbordo', 'escala', 'connecting'],
                'limpieza': ['limpio', 'sucio', 'limpieza', 'higiene', 'clean'],
                'precio': ['precio', 'caro', 'barato', 'tarifa', 'coste', 'precio'],
                'reserva': ['reserva', 'booking', 'cambio', 'modificar', 'cancelar']
            }
            
            # Extract keywords from query
            relevant_keywords = []
            for category, keywords in keyword_mappings.items():
                if any(keyword in query_lower for keyword in keywords):
                    relevant_keywords.extend(keywords)
            
            # If no specific keywords found, use query terms directly
            if not relevant_keywords:
                relevant_keywords = [word.strip() for word in query_lower.split() if len(word.strip()) > 2]
            
            # Filter verbatims that contain relevant keywords
            if relevant_keywords and 'verbatim_text' in df.columns:
                mask = df['verbatim_text'].str.lower().str.contains('|'.join(relevant_keywords), na=False, regex=True)
                filtered_df = df[mask]
                
                logger.info(f"🔍 Intelligent query '{intelligent_query}' filtered {len(df)} -> {len(filtered_df)} verbatims")
                return filtered_df
            
            # If no text column or keywords, return original data
            return df
            
        except Exception as e:
            logger.error(f"Error applying intelligent query filter: {e}")
            return df  # Return original data on error 