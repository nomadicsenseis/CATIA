"""
NCS Route Filter - Utilidades para filtrar y procesar datos de rutas NCS
Proporciona funciones especializadas para manejar datos del Network Control System
"""

import pandas as pd
from typing import Dict, List, Tuple, Optional, Any, Set
import logging
from datetime import datetime, timedelta
import re

logger = logging.getLogger(__name__)


class NCSRouteFilter:
    """
    Filtro especializado para datos de rutas del Network Control System (NCS)
    Maneja incidentes operativos y su impacto en rutas específicas
    """
    
    def __init__(self, pbi_collector):
        """
        Inicializa el filtro de rutas NCS
        
        Args:
            pbi_collector: Colector de datos de Power BI
        """
        self.pbi_collector = pbi_collector
        
        # Tipos de incidentes NCS y su severidad
        self.incident_types = {
            'weather': {'severity': 'high', 'impact_factor': 0.8},
            'technical': {'severity': 'medium', 'impact_factor': 0.6},
            'atc': {'severity': 'medium', 'impact_factor': 0.5},  # Air Traffic Control
            'ground_stop': {'severity': 'critical', 'impact_factor': 0.9},
            'crew': {'severity': 'medium', 'impact_factor': 0.4},
            'maintenance': {'severity': 'low', 'impact_factor': 0.3},
            'slot': {'severity': 'medium', 'impact_factor': 0.5},
            'security': {'severity': 'high', 'impact_factor': 0.7}
        }
        
        # Patrones para extraer códigos de aeropuerto
        self.airport_patterns = [
            r'\b[A-Z]{3}\b',  # Códigos IATA de 3 letras
            r'\b[A-Z]{4}\b'   # Códigos ICAO de 4 letras
        ]
        
        # Aeropuertos principales y su impacto
        self.major_airports = {
            'MAD': {'impact_multiplier': 1.0, 'region': 'domestic'},
            'BCN': {'impact_multiplier': 0.9, 'region': 'domestic'},
            'LHR': {'impact_multiplier': 1.2, 'region': 'europe'},
            'CDG': {'impact_multiplier': 1.1, 'region': 'europe'},
            'FRA': {'impact_multiplier': 1.1, 'region': 'europe'},
            'JFK': {'impact_multiplier': 1.3, 'region': 'america'},
            'LAX': {'impact_multiplier': 1.2, 'region': 'america'},
            'MEX': {'impact_multiplier': 1.0, 'region': 'america'}
        }
        
        logger.info("NCSRouteFilter initialized")
    
    def filter_routes_by_incidents(self, date_range: Tuple[str, str], 
                                 node_path: str = None,
                                 incident_types: Optional[List[str]] = None,
                                 min_impact_score: float = 0.3) -> pd.DataFrame:
        """
        Filtra rutas que tuvieron incidentes NCS en el período
        
        Args:
            date_range: Tupla con (start_date, end_date)
            node_path: Filtro opcional por nodo específico
            incident_types: Tipos específicos de incidentes a incluir
            min_impact_score: Score mínimo de impacto para incluir la ruta
            
        Returns:
            DataFrame con rutas filtradas por incidentes
        """
        try:
            logger.info(f"Filtering routes by NCS incidents for {date_range}")
            
            # Obtener datos base de incidentes NCS
            ncs_data = self.pbi_collector.collect_ncs_data(
                start_date=date_range[0],
                end_date=date_range[1],
                node_path=node_path
            )
            
            if ncs_data.empty:
                logger.warning(f"No NCS data found for period {date_range}")
                return pd.DataFrame()
            
            # Procesar y enriquecer datos de incidentes
            processed_ncs = self._process_ncs_incidents(ncs_data)
            
            # Filtrar por tipos de incidentes si se especifica
            if incident_types:
                processed_ncs = processed_ncs[
                    processed_ncs['incident_type'].isin(incident_types)
                ]
            
            # Calcular score de impacto por ruta
            route_impacts = self._calculate_route_impact_scores(processed_ncs)
            
            # Filtrar por score mínimo de impacto
            filtered_routes = route_impacts[
                route_impacts['impact_score'] >= min_impact_score
            ]
            
            # Agregar información de NPS para las rutas afectadas
            if not filtered_routes.empty:
                filtered_routes = self._enrich_with_nps_data(
                    filtered_routes, date_range, node_path
                )
            
            logger.info(f"Found {len(filtered_routes)} routes with significant NCS impact")
            
            return filtered_routes
            
        except Exception as e:
            logger.error(f"Error filtering routes by incidents: {e}")
            return pd.DataFrame()
    
    def get_incident_summary(self, date_range: Tuple[str, str], 
                           node_path: str = None) -> Dict[str, Any]:
        """
        Obtiene resumen de incidentes NCS para el período
        
        Args:
            date_range: Período a analizar
            node_path: Filtro opcional por nodo
            
        Returns:
            Dict con resumen de incidentes
        """
        try:
            ncs_data = self.pbi_collector.collect_ncs_data(
                start_date=date_range[0],
                end_date=date_range[1],
                node_path=node_path
            )
            
            if ncs_data.empty:
                return {
                    'total_incidents': 0,
                    'affected_routes': 0,
                    'summary': 'No NCS incidents found'
                }
            
            # Procesar incidentes
            processed_ncs = self._process_ncs_incidents(ncs_data)
            
            # Estadísticas básicas
            total_incidents = len(processed_ncs)
            unique_routes = processed_ncs['route'].nunique()
            
            # Contar por tipo de incidente
            incident_type_counts = processed_ncs['incident_type'].value_counts().to_dict()
            
            # Contar por severidad
            severity_counts = processed_ncs['severity'].value_counts().to_dict()
            
            # Top rutas más afectadas
            route_incident_counts = processed_ncs['route'].value_counts().head(5).to_dict()
            
            # Aeropuertos más afectados
            affected_airports = self._extract_affected_airports(processed_ncs)
            
            summary_text = f"NCS Analysis: {total_incidents} incidents affecting {unique_routes} routes. "
            
            if incident_type_counts:
                top_incident_type = max(incident_type_counts, key=incident_type_counts.get)
                summary_text += f"Most common: {top_incident_type} ({incident_type_counts[top_incident_type]} incidents). "
            
            if route_incident_counts:
                most_affected_route = list(route_incident_counts.keys())[0]
                summary_text += f"Most affected route: {most_affected_route} ({route_incident_counts[most_affected_route]} incidents)."
            
            return {
                'total_incidents': total_incidents,
                'affected_routes': unique_routes,
                'incident_types': incident_type_counts,
                'severity_distribution': severity_counts,
                'top_affected_routes': route_incident_counts,
                'affected_airports': affected_airports,
                'summary': summary_text
            }
            
        except Exception as e:
            logger.error(f"Error getting incident summary: {e}")
            return {
                'total_incidents': 0,
                'affected_routes': 0,
                'summary': f'Error: {str(e)}'
            }
    
    def correlate_incidents_with_nps(self, date_range: Tuple[str, str],
                                   node_path: str = None) -> Dict[str, Any]:
        """
        Correlaciona incidentes NCS con impacto en NPS
        
        Args:
            date_range: Período a analizar
            node_path: Filtro opcional por nodo
            
        Returns:
            Dict con correlaciones encontradas
        """
        try:
            # Obtener rutas con incidentes
            routes_with_incidents = self.filter_routes_by_incidents(
                date_range, node_path, min_impact_score=0.1
            )
            
            if routes_with_incidents.empty:
                return {
                    'correlations': [],
                    'summary': 'No routes with incidents to correlate'
                }
            
            # Obtener datos NPS para comparación
            nps_data = self.pbi_collector.collect_routes_for_date_range(
                start_date=date_range[0],
                end_date=date_range[1],
                node_path=node_path
            )
            
            if nps_data.empty:
                return {
                    'correlations': [],
                    'summary': 'No NPS data available for correlation'
                }
            
            # Correlacionar datos
            correlations = self._perform_ncs_nps_correlation(
                routes_with_incidents, nps_data
            )
            
            # Crear resumen de correlaciones
            summary = self._create_correlation_summary(correlations)
            
            return {
                'correlations': correlations,
                'summary': summary,
                'total_routes_analyzed': len(routes_with_incidents)
            }
            
        except Exception as e:
            logger.error(f"Error correlating incidents with NPS: {e}")
            return {
                'correlations': [],
                'summary': f'Error: {str(e)}'
            }
    
    def _process_ncs_incidents(self, ncs_data: pd.DataFrame) -> pd.DataFrame:
        """Procesa y enriquece datos de incidentes NCS"""
        try:
            processed_data = ncs_data.copy()
            
            # Normalizar tipos de incidentes
            processed_data['incident_type'] = processed_data['incident_type'].apply(
                self._normalize_incident_type
            )
            
            # Agregar información de severidad
            processed_data['severity'] = processed_data['incident_type'].apply(
                lambda x: self.incident_types.get(x, {}).get('severity', 'low')
            )
            
            # Agregar factor de impacto
            processed_data['impact_factor'] = processed_data['incident_type'].apply(
                lambda x: self.incident_types.get(x, {}).get('impact_factor', 0.3)
            )
            
            # Extraer aeropuertos afectados
            processed_data['affected_airports'] = processed_data.apply(
                lambda row: self._extract_airports_from_incident(row), axis=1
            )
            
            # Calcular duración del incidente si hay timestamps
            if 'start_time' in processed_data.columns and 'end_time' in processed_data.columns:
                processed_data['duration_hours'] = self._calculate_incident_duration(
                    processed_data['start_time'], processed_data['end_time']
                )
            else:
                processed_data['duration_hours'] = 1.0  # Default 1 hour
            
            return processed_data
            
        except Exception as e:
            logger.error(f"Error processing NCS incidents: {e}")
            return ncs_data
    
    def _normalize_incident_type(self, incident_type: str) -> str:
        """Normaliza tipos de incidentes a categorías estándar"""
        if not incident_type or pd.isna(incident_type):
            return 'technical'
        
        incident_lower = str(incident_type).lower()
        
        # Mapeo de términos comunes a tipos estándar
        if any(term in incident_lower for term in ['weather', 'storm', 'wind', 'fog']):
            return 'weather'
        elif any(term in incident_lower for term in ['technical', 'mech', 'aircraft', 'engine']):
            return 'technical'
        elif any(term in incident_lower for term in ['atc', 'traffic', 'control']):
            return 'atc'
        elif any(term in incident_lower for term in ['ground', 'stop', 'closure']):
            return 'ground_stop'
        elif any(term in incident_lower for term in ['crew', 'staff', 'pilot']):
            return 'crew'
        elif any(term in incident_lower for term in ['maintenance', 'repair', 'inspection']):
            return 'maintenance'
        elif any(term in incident_lower for term in ['slot', 'delay', 'schedule']):
            return 'slot'
        elif any(term in incident_lower for term in ['security', 'baggage', 'screening']):
            return 'security'
        else:
            return 'technical'  # Default
    
    def _extract_airports_from_incident(self, incident_row: pd.Series) -> List[str]:
        """Extrae códigos de aeropuertos de los datos del incidente"""
        airports = set()
        
        # Campos donde buscar códigos de aeropuerto
        search_fields = ['description', 'route', 'affected_stations', 'details']
        
        for field in search_fields:
            if field in incident_row and pd.notna(incident_row[field]):
                text = str(incident_row[field]).upper()
                
                # Buscar patrones de aeropuertos
                for pattern in self.airport_patterns:
                    matches = re.findall(pattern, text)
                    airports.update(matches)
        
        # Filtrar aeropuertos válidos (conocidos)
        valid_airports = [apt for apt in airports if self._is_valid_airport(apt)]
        
        return list(valid_airports)
    
    def _is_valid_airport(self, airport_code: str) -> bool:
        """Verifica si un código de aeropuerto es válido"""
        # Lista básica de códigos válidos (se podría expandir)
        valid_codes = set(self.major_airports.keys()) | {
            'VLC', 'SVQ', 'BIO', 'LPA', 'TFS', 'AGP', 'ALC', 'PMI',  # España
            'LGW', 'MAN', 'EDI', 'DUB', 'AMS', 'BRU', 'ZUR', 'VIE',  # Europa
            'MIA', 'DFW', 'ORD', 'ATL', 'BOS', 'SFO', 'SEA', 'YYZ',  # América
            'NRT', 'ICN', 'SIN', 'HKG', 'BKK', 'DEL', 'DXB', 'DOH'   # Asia/Otros
        }
        
        return len(airport_code) >= 3 and airport_code in valid_codes
    
    def _calculate_route_impact_scores(self, processed_ncs: pd.DataFrame) -> pd.DataFrame:
        """Calcula scores de impacto por ruta"""
        try:
            if processed_ncs.empty:
                return pd.DataFrame()
            
            # Agrupar por ruta
            route_groups = processed_ncs.groupby('route')
            
            route_impacts = []
            
            for route, group in route_groups:
                # Score base: suma de factores de impacto
                base_score = group['impact_factor'].sum()
                
                # Multiplicador por duración total
                total_duration = group['duration_hours'].sum()
                duration_multiplier = min(total_duration / 24, 2.0)  # Max 2x por duración
                
                # Multiplicador por aeropuertos afectados
                all_airports = []
                for airports_list in group['affected_airports']:
                    all_airports.extend(airports_list)
                
                airport_multiplier = 1.0
                for airport in set(all_airports):
                    if airport in self.major_airports:
                        airport_multiplier *= self.major_airports[airport]['impact_multiplier']
                
                # Score final
                final_score = base_score * duration_multiplier * airport_multiplier
                
                route_impacts.append({
                    'route': route,
                    'incident_count': len(group),
                    'impact_score': round(final_score, 3),
                    'total_duration_hours': round(total_duration, 1),
                    'affected_airports': list(set(all_airports)),
                    'incident_types': group['incident_type'].unique().tolist(),
                    'max_severity': self._get_max_severity(group['severity'].tolist())
                })
            
            return pd.DataFrame(route_impacts)
            
        except Exception as e:
            logger.error(f"Error calculating route impact scores: {e}")
            return pd.DataFrame()
    
    def _get_max_severity(self, severities: List[str]) -> str:
        """Obtiene la severidad máxima de una lista"""
        severity_order = ['low', 'medium', 'high', 'critical']
        
        max_severity = 'low'
        for severity in severities:
            if severity in severity_order:
                if severity_order.index(severity) > severity_order.index(max_severity):
                    max_severity = severity
        
        return max_severity
    
    def _enrich_with_nps_data(self, routes_df: pd.DataFrame, 
                            date_range: Tuple[str, str],
                            node_path: str = None) -> pd.DataFrame:
        """Enriquece datos de rutas con información NPS"""
        try:
            # Obtener datos NPS para las rutas
            nps_data = self.pbi_collector.collect_routes_for_date_range(
                start_date=date_range[0],
                end_date=date_range[1],
                node_path=node_path
            )
            
            if nps_data.empty:
                logger.warning("No NPS data available for enrichment")
                return routes_df
            
            # Merge con datos NPS
            enriched_df = routes_df.merge(
                nps_data[['route', 'nps', 'surveys_count', 'nps_diff']], 
                on='route', 
                how='left'
            )
            
            return enriched_df
            
        except Exception as e:
            logger.error(f"Error enriching with NPS data: {e}")
            return routes_df
    
    def _extract_affected_airports(self, processed_ncs: pd.DataFrame) -> Dict[str, int]:
        """Extrae estadísticas de aeropuertos afectados"""
        airport_counts = {}
        
        for airports_list in processed_ncs['affected_airports']:
            for airport in airports_list:
                airport_counts[airport] = airport_counts.get(airport, 0) + 1
        
        # Ordenar por frecuencia
        sorted_airports = dict(sorted(airport_counts.items(), 
                                    key=lambda x: x[1], reverse=True))
        
        return dict(list(sorted_airports.items())[:10])  # Top 10
    
    def _calculate_incident_duration(self, start_times: pd.Series, 
                                   end_times: pd.Series) -> pd.Series:
        """Calcula duración de incidentes en horas"""
        try:
            durations = []
            
            for start, end in zip(start_times, end_times):
                if pd.isna(start) or pd.isna(end):
                    durations.append(1.0)  # Default 1 hour
                    continue
                
                try:
                    start_dt = pd.to_datetime(start)
                    end_dt = pd.to_datetime(end)
                    duration = (end_dt - start_dt).total_seconds() / 3600
                    durations.append(max(duration, 0.1))  # Minimum 6 minutes
                except:
                    durations.append(1.0)  # Default if parsing fails
            
            return pd.Series(durations)
            
        except Exception as e:
            logger.error(f"Error calculating incident duration: {e}")
            return pd.Series([1.0] * len(start_times))
    
    def _perform_ncs_nps_correlation(self, routes_with_incidents: pd.DataFrame,
                                   nps_data: pd.DataFrame) -> List[Dict]:
        """Realiza correlación entre incidentes NCS y NPS"""
        correlations = []
        
        try:
            # Merge datos
            merged_data = routes_with_incidents.merge(
                nps_data[['route', 'nps', 'nps_diff', 'surveys_count']], 
                on='route', 
                how='inner'
            )
            
            if merged_data.empty:
                return correlations
            
            for _, row in merged_data.iterrows():
                correlation = {
                    'route': row['route'],
                    'incident_count': row['incident_count'],
                    'impact_score': row['impact_score'],
                    'max_severity': row['max_severity'],
                    'nps': round(row['nps'], 1),
                    'surveys_count': int(row['surveys_count'])
                }
                
                # Agregar NPS diff si está disponible
                if 'nps_diff' in row and pd.notna(row['nps_diff']):
                    correlation['nps_diff'] = round(row['nps_diff'], 1)
                    
                    # Evaluar correlación
                    if row['impact_score'] > 0.5 and row['nps_diff'] < -2:
                        correlation['correlation_strength'] = 'strong'
                        correlation['interpretation'] = 'High incident impact correlates with NPS drop'
                    elif row['impact_score'] > 0.3 and row['nps_diff'] < -1:
                        correlation['correlation_strength'] = 'moderate'
                        correlation['interpretation'] = 'Moderate incident impact with NPS decline'
                    else:
                        correlation['correlation_strength'] = 'weak'
                        correlation['interpretation'] = 'Limited apparent correlation'
                else:
                    correlation['correlation_strength'] = 'unknown'
                    correlation['interpretation'] = 'No comparative NPS data available'
                
                correlations.append(correlation)
            
            return correlations
            
        except Exception as e:
            logger.error(f"Error performing NCS-NPS correlation: {e}")
            return correlations
    
    def _create_correlation_summary(self, correlations: List[Dict]) -> str:
        """Crea resumen de las correlaciones encontradas"""
        if not correlations:
            return "No correlations found between NCS incidents and NPS"
        
        total_routes = len(correlations)
        strong_correlations = len([c for c in correlations if c.get('correlation_strength') == 'strong'])
        moderate_correlations = len([c for c in correlations if c.get('correlation_strength') == 'moderate'])
        
        # Ruta con mayor impacto
        max_impact_route = max(correlations, key=lambda x: x['impact_score'])
        
        summary = f"NCS-NPS Correlation Analysis: {total_routes} routes analyzed. "
        summary += f"{strong_correlations} strong correlations, {moderate_correlations} moderate correlations. "
        summary += f"Highest impact route: {max_impact_route['route']} "
        summary += f"(impact score: {max_impact_route['impact_score']}, "
        
        if 'nps_diff' in max_impact_route:
            summary += f"NPS change: {max_impact_route['nps_diff']})."
        else:
            summary += f"NPS: {max_impact_route['nps']})."
        
        return summary 