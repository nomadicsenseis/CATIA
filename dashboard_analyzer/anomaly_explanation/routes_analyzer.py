"""
Routes Analyzer - Análisis de rutas específicas para anomalías NPS
Identifica rutas problemáticas y su contribución a las anomalías detectadas
"""

import pandas as pd
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class RoutesAnalyzer:
    """
    Analizador de rutas para identificar contribuciones específicas a anomalías NPS
    """
    
    def __init__(self, pbi_collector):
        """
        Initialize the Routes Analyzer
        
        Args:
            pbi_collector: Power BI data collector instance
        """
        self.pbi_collector = pbi_collector
        self.min_surveys = 2  # Mínimo número de encuestas para considerar una ruta
    
    def analyze_routes_for_anomaly(self, date_range: Tuple[str, str], node_path: str, 
                                 anomaly_type: str, causal_filter: Optional[str] = None) -> Dict:
        """
        Analiza rutas específicas durante una anomalía
        
        Args:
            date_range: Tupla con (start_date, end_date)
            node_path: Ruta del nodo en el árbol jerárquico
            anomaly_type: 'positive' o 'negative'
            causal_filter: Filtro de comparación (ej: 'vs_L7d')
        
        Returns:
            Dict con análisis de rutas
        """
        try:
            # Obtener datos de rutas
            routes_data = self._get_routes_data(date_range, node_path, causal_filter)
            
            if routes_data.empty:
                return {"routes": [], "summary": "No routes data available"}
            
            # Filtrar por número mínimo de encuestas
            routes_filtered = routes_data[routes_data['surveys_count'] >= self.min_surveys]
            
            # Ordenar según tipo de anomalía
            routes_sorted = self._sort_routes_by_anomaly_type(routes_filtered, anomaly_type)
            
            # Integrar datos NCS
            routes_with_ncs = self._integrate_ncs_data(routes_sorted, date_range, node_path)
            
            # Formatear resultados
            results = self._format_routes_results(routes_with_ncs, anomaly_type, causal_filter)
            
            return results
            
        except Exception as e:
            logger.error(f"Error analyzing routes for anomaly: {e}")
            return {"routes": [], "summary": f"Error: {str(e)}"}
    
    def get_routes_by_driver(self, driver_name: str, shap_value: float, date_range: Tuple[str, str],
                           node_path: str, causal_filter: Optional[str] = None) -> List[Dict]:
        """
        Obtiene rutas ordenadas por CSAT para un driver específico
        
        Args:
            driver_name: Nombre del driver explicativo
            shap_value: Valor SHAP del driver (determina orden)
            date_range: Tupla con fechas
            node_path: Ruta del nodo
            causal_filter: Filtro de comparación
        
        Returns:
            Lista de rutas con CSAT del driver
        """
        try:
            # Obtener datos de rutas con CSAT por driver
            routes_data = self.pbi_collector.collect_routes_for_date_range(
                start_date=date_range[0],
                end_date=date_range[1],
                node_path=node_path,
                comparison_filter=causal_filter
            )
            
            if routes_data.empty:
                return []
            
            # Filtrar por número mínimo de encuestas
            routes_filtered = routes_data[routes_data['surveys_count'] >= self.min_surveys]
            
            # Filtrar por driver específico si existe en los datos
            driver_column = f"csat_{driver_name.lower()}"
            driver_diff_column = f"csat_{driver_name.lower()}_diff"
            
            if driver_column in routes_filtered.columns:
                # Filtrar rutas con datos válidos del driver
                valid_routes = routes_filtered[
                    pd.notna(routes_filtered[driver_column]) & 
                    (routes_filtered[driver_column] != 0)
                ]
                
                # Ordenar según signo de SHAP value
                if shap_value < 0:
                    # SHAP negativo: ordenar por menor CSAT (peores)
                    if driver_diff_column in valid_routes.columns:
                        sorted_routes = valid_routes.sort_values(driver_diff_column, ascending=True)
                    else:
                        sorted_routes = valid_routes.sort_values(driver_column, ascending=True)
                else:
                    # SHAP positivo: ordenar por mayor CSAT (mejores)
                    if driver_diff_column in valid_routes.columns:
                        sorted_routes = valid_routes.sort_values(driver_diff_column, ascending=False)
                    else:
                        sorted_routes = valid_routes.sort_values(driver_column, ascending=False)
                
                # Tomar las top 5
                top_routes = sorted_routes.head(5)
                
                results = []
                for _, route in top_routes.iterrows():
                    route_info = {
                        'route': route.get('route', 'Unknown'),
                        'nps': round(route.get('nps', 0), 1),
                        'surveys_count': int(route.get('surveys_count', 0)),
                        f'csat_{driver_name.lower()}': round(route.get(driver_column, 0), 1)
                    }
                    
                    # Agregar NPS diff si existe
                    if 'nps_diff' in route:
                        route_info['nps_diff'] = round(route['nps_diff'], 1)
                    
                    # Agregar CSAT diff si existe
                    if driver_diff_column in route:
                        route_info[f'csat_{driver_name.lower()}_diff'] = round(route[driver_diff_column], 1)
                    
                    results.append(route_info)
                
                return results
            
            return []
            
        except Exception as e:
            logger.error(f"Error getting routes by driver {driver_name}: {e}")
            return []
    
    def _get_routes_data(self, date_range: Tuple[str, str], node_path: str, 
                        causal_filter: Optional[str] = None) -> pd.DataFrame:
        """Obtiene datos base de rutas"""
        try:
            if causal_filter:
                # Modo comparativo
                routes_data = self.pbi_collector.collect_routes_for_date_range(
                    start_date=date_range[0],
                    end_date=date_range[1],
                    node_path=node_path,
                    comparison_filter=causal_filter
                )
            else:
                # Modo single
                routes_data = self.pbi_collector.collect_routes_data(
                    start_date=date_range[0],
                    end_date=date_range[1],
                    node_path=node_path
                )
            
            return routes_data
            
        except Exception as e:
            logger.error(f"Error getting routes data: {e}")
            return pd.DataFrame()
    
    def _sort_routes_by_anomaly_type(self, routes_data: pd.DataFrame, anomaly_type: str) -> pd.DataFrame:
        """Ordena rutas según tipo de anomalía"""
        if anomaly_type == "negative":
            # Para anomalías negativas, ordenar de menor a mayor NPS (peores primero)
            return routes_data.sort_values('nps', ascending=True)
        else:
            # Para anomalías positivas, ordenar de mayor a menor NPS (mejores primero)
            return routes_data.sort_values('nps', ascending=False)
    
    def _integrate_ncs_data(self, routes_data: pd.DataFrame, date_range: Tuple[str, str], 
                           node_path: str) -> pd.DataFrame:
        """Integra datos de NCS (Network Control System)"""
        try:
            # Obtener rutas con incidentes NCS
            ncs_routes = self.pbi_collector.collect_ncs_routes(
                start_date=date_range[0],
                end_date=date_range[1],
                node_path=node_path
            )
            
            if not ncs_routes.empty:
                # Marcar rutas con incidentes NCS
                routes_data['has_ncs_incident'] = routes_data['route'].isin(ncs_routes['route'])
                
                # Agregar información de incidentes
                ncs_info = ncs_routes.groupby('route').agg({
                    'incident_count': 'sum',
                    'incident_types': lambda x: ', '.join(x.unique())
                }).reset_index()
                
                routes_data = routes_data.merge(ncs_info, on='route', how='left')
            else:
                routes_data['has_ncs_incident'] = False
                routes_data['incident_count'] = 0
                routes_data['incident_types'] = None
            
            return routes_data
            
        except Exception as e:
            logger.error(f"Error integrating NCS data: {e}")
            routes_data['has_ncs_incident'] = False
            return routes_data
    
    def _format_routes_results(self, routes_data: pd.DataFrame, anomaly_type: str, 
                              causal_filter: Optional[str] = None) -> Dict:
        """Formatea los resultados para presentación"""
        try:
            routes_list = []
            
            # Tomar las top 10 rutas
            top_routes = routes_data.head(10)
            
            for _, route in top_routes.iterrows():
                route_info = {
                    'route': route.get('route', 'Unknown'),
                    'nps': round(route.get('nps', 0), 1),
                    'surveys_count': int(route.get('surveys_count', 0)),
                    'has_ncs_incident': bool(route.get('has_ncs_incident', False))
                }
                
                # Agregar NPS diff en modo comparativo
                if causal_filter and 'nps_diff' in route:
                    route_info['nps_diff'] = round(route['nps_diff'], 1)
                
                # Agregar información de incidentes NCS si existen
                if route.get('incident_count', 0) > 0:
                    route_info['incident_count'] = int(route['incident_count'])
                    route_info['incident_types'] = route.get('incident_types', '')
                
                routes_list.append(route_info)
            
            # Crear resumen
            total_routes = len(routes_data)
            routes_with_incidents = len(routes_data[routes_data.get('has_ncs_incident', False)])
            
            summary = f"Analizadas {total_routes} rutas con al menos {self.min_surveys} encuestas."
            if routes_with_incidents > 0:
                summary += f" {routes_with_incidents} rutas con incidentes NCS."
            
            if causal_filter:
                summary += f" Comparación {causal_filter}."
            
            return {
                'routes': routes_list,
                'summary': summary,
                'total_routes_analyzed': total_routes,
                'routes_with_ncs_incidents': routes_with_incidents
            }
            
        except Exception as e:
            logger.error(f"Error formatting routes results: {e}")
            return {'routes': [], 'summary': f'Error formatting results: {str(e)}'}
    
    def get_verbatims_routes(self, date_range: Tuple[str, str], node_path: str,
                           causal_filter: Optional[str] = None) -> List[Dict]:
        """
        Obtiene rutas mencionadas en verbatims
        
        Args:
            date_range: Tupla con fechas
            node_path: Ruta del nodo
            causal_filter: Filtro de comparación
        
        Returns:
            Lista de rutas con verbatims
        """
        try:
            verbatims_routes = self.pbi_collector.collect_verbatims_routes(
                start_date=date_range[0],
                end_date=date_range[1],
                node_path=node_path,
                comparison_filter=causal_filter
            )
            
            if verbatims_routes.empty:
                return []
            
            results = []
            for _, route in verbatims_routes.iterrows():
                route_info = {
                    'route': route.get('route', 'Unknown'),
                    'nps': round(route.get('nps', 0), 1),
                    'verbatim_count': int(route.get('verbatim_count', 0)),
                    'sentiment_score': round(route.get('sentiment_score', 0), 2)
                }
                
                if causal_filter and 'nps_diff' in route:
                    route_info['nps_diff'] = round(route['nps_diff'], 1)
                
                results.append(route_info)
            
            return results
            
        except Exception as e:
            logger.error(f"Error getting verbatims routes: {e}")
            return [] 