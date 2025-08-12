"""
Target-Based Anomaly Detector - Detector de anomalías basado en targets
Detecta anomalías comparando NPS actual contra targets predefinidos
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class TargetBasedDetector:
    """
    Detector de anomalías basado en comparación con targets predefinidos
    Útil para detectar desviaciones significativas de objetivos empresariales
    """
    
    def __init__(self, pbi_collector, targets_config: Optional[Dict] = None):
        """
        Inicializa el detector basado en targets
        
        Args:
            pbi_collector: Colector de datos de Power BI
            targets_config: Configuración de targets por segmento
        """
        self.pbi_collector = pbi_collector
        
        # Configuración por defecto de targets
        self.default_targets = {
            'Global': {'target': 70.0, 'tolerance': 5.0},
            'LH': {'target': 72.0, 'tolerance': 5.0},
            'SH': {'target': 68.0, 'tolerance': 5.0},
            'Economy': {'target': 68.0, 'tolerance': 5.0},
            'Business': {'target': 75.0, 'tolerance': 4.0},
            'Premium': {'target': 78.0, 'tolerance': 4.0},
            'IB': {'target': 71.0, 'tolerance': 5.0},
            'YW': {'target': 69.0, 'tolerance': 5.0}
        }
        
        # Usar configuración personalizada o por defecto
        self.targets_config = targets_config or self.default_targets
        
        # Configuración de detección
        self.min_surveys_threshold = 30  # Mínimo de encuestas para considerar válido
        self.significance_levels = {
            'low': 1.0,     # 1 punto de diferencia
            'medium': 3.0,  # 3 puntos de diferencia  
            'high': 5.0,    # 5 puntos de diferencia
            'critical': 8.0 # 8 puntos de diferencia
        }
        
        logger.info("TargetBasedDetector initialized")
    
    def detect_anomalies(self, date_range: Tuple[str, str], 
                        nodes_to_analyze: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Detecta anomalías comparando NPS actual vs targets
        
        Args:
            date_range: Tupla con (start_date, end_date)
            nodes_to_analyze: Lista de nodos a analizar (None = todos)
            
        Returns:
            Dict con anomalías detectadas
        """
        try:
            logger.info(f"Starting target-based anomaly detection for {date_range}")
            
            # Obtener datos NPS del período
            nps_data = self._get_nps_data(date_range, nodes_to_analyze)
            
            if nps_data.empty:
                return {
                    'anomalies': [],
                    'summary': 'No data available for analysis',
                    'metadata': {'date_range': date_range, 'nodes_analyzed': 0}
                }
            
            # Detectar anomalías por nodo
            anomalies = []
            for _, row in nps_data.iterrows():
                node_path = row['node_path']
                anomaly = self._analyze_node_against_target(row, date_range)
                
                if anomaly:
                    anomalies.append(anomaly)
            
            # Crear resumen
            summary = self._create_summary(anomalies, date_range)
            
            return {
                'anomalies': anomalies,
                'summary': summary,
                'metadata': {
                    'date_range': date_range,
                    'nodes_analyzed': len(nps_data),
                    'anomalies_found': len(anomalies),
                    'detection_method': 'target_based'
                }
            }
            
        except Exception as e:
            logger.error(f"Error in target-based anomaly detection: {e}")
            return {
                'anomalies': [],
                'summary': f'Error during detection: {str(e)}',
                'metadata': {'error': str(e)}
            }
    
    def set_target(self, node_path: str, target_nps: float, tolerance: float = 5.0):
        """
        Establece un target personalizado para un nodo específico
        
        Args:
            node_path: Ruta del nodo (ej: 'Global/LH/Economy')
            target_nps: NPS objetivo
            tolerance: Tolerancia antes de considerar anomalía
        """
        # Extraer el nivel del nodo (último elemento del path)
        node_level = node_path.split('/')[-1] if '/' in node_path else node_path
        
        self.targets_config[node_level] = {
            'target': target_nps,
            'tolerance': tolerance
        }
        
        logger.info(f"Set custom target for {node_level}: {target_nps} ±{tolerance}")
    
    def get_target_performance(self, date_range: Tuple[str, str]) -> Dict[str, Any]:
        """
        Obtiene el rendimiento actual vs targets para todos los nodos
        
        Args:
            date_range: Período a analizar
            
        Returns:
            Dict con rendimiento vs targets
        """
        try:
            nps_data = self._get_nps_data(date_range)
            
            if nps_data.empty:
                return {'performance': [], 'summary': 'No data available'}
            
            performance = []
            
            for _, row in nps_data.iterrows():
                node_level = self._extract_node_level(row['node_path'])
                target_config = self.targets_config.get(node_level, {'target': 70.0, 'tolerance': 5.0})
                
                current_nps = row['nps']
                target_nps = target_config['target']
                difference = current_nps - target_nps
                
                # Calcular estado
                tolerance = target_config['tolerance']
                if abs(difference) <= tolerance:
                    status = 'on_target'
                elif difference > tolerance:
                    status = 'above_target'
                else:
                    status = 'below_target'
                
                performance.append({
                    'node_path': row['node_path'],
                    'node_level': node_level,
                    'current_nps': round(current_nps, 1),
                    'target_nps': target_nps,
                    'difference': round(difference, 1),
                    'tolerance': tolerance,
                    'status': status,
                    'surveys_count': int(row.get('surveys_count', 0))
                })
            
            # Crear resumen de rendimiento
            total_nodes = len(performance)
            on_target = len([p for p in performance if p['status'] == 'on_target'])
            above_target = len([p for p in performance if p['status'] == 'above_target'])
            below_target = len([p for p in performance if p['status'] == 'below_target'])
            
            summary = f"Target Performance: {on_target}/{total_nodes} on target, "
            summary += f"{above_target} above, {below_target} below target"
            
            return {
                'performance': performance,
                'summary': summary,
                'totals': {
                    'total_nodes': total_nodes,
                    'on_target': on_target,
                    'above_target': above_target,
                    'below_target': below_target
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting target performance: {e}")
            return {'performance': [], 'summary': f'Error: {str(e)}'}
    
    def _get_nps_data(self, date_range: Tuple[str, str], 
                     nodes_to_analyze: Optional[List[str]] = None) -> pd.DataFrame:
        """Obtiene datos NPS del período especificado"""
        try:
            # Obtener datos base de NPS
            nps_data = self.pbi_collector.collect_nps_data(
                start_date=date_range[0],
                end_date=date_range[1]
            )
            
            if nps_data.empty:
                logger.warning(f"No NPS data found for period {date_range}")
                return pd.DataFrame()
            
            # Filtrar por nodos específicos si se especifica
            if nodes_to_analyze:
                nps_data = nps_data[nps_data['node_path'].isin(nodes_to_analyze)]
            
            # Filtrar por número mínimo de encuestas
            nps_data = nps_data[nps_data['surveys_count'] >= self.min_surveys_threshold]
            
            return nps_data
            
        except Exception as e:
            logger.error(f"Error getting NPS data: {e}")
            return pd.DataFrame()
    
    def _analyze_node_against_target(self, node_data: pd.Series, 
                                   date_range: Tuple[str, str]) -> Optional[Dict]:
        """Analiza un nodo específico contra su target"""
        try:
            node_path = node_data['node_path']
            node_level = self._extract_node_level(node_path)
            
            # Obtener configuración del target
            target_config = self.targets_config.get(node_level)
            if not target_config:
                logger.warning(f"No target configuration found for {node_level}")
                return None
            
            current_nps = node_data['nps']
            target_nps = target_config['target']
            tolerance = target_config['tolerance']
            difference = current_nps - target_nps
            
            # Verificar si es una anomalía (fuera de tolerancia)
            if abs(difference) <= tolerance:
                return None  # No es anomalía
            
            # Determinar tipo y severidad de anomalía
            anomaly_type = 'positive' if difference > 0 else 'negative'
            severity = self._calculate_severity(abs(difference))
            
            # Obtener datos adicionales del nodo
            surveys_count = int(node_data.get('surveys_count', 0))
            
            anomaly = {
                'node_path': node_path,
                'node_level': node_level,
                'anomaly_type': anomaly_type,
                'severity': severity,
                'current_nps': round(current_nps, 1),
                'target_nps': target_nps,
                'difference_from_target': round(difference, 1),
                'tolerance': tolerance,
                'surveys_count': surveys_count,
                'date_range': date_range,
                'detection_method': 'target_based'
            }
            
            # Agregar descripción
            if anomaly_type == 'positive':
                anomaly['description'] = f"NPS superó target en {abs(difference):.1f} puntos"
            else:
                anomaly['description'] = f"NPS por debajo del target en {abs(difference):.1f} puntos"
            
            logger.info(f"Target-based anomaly detected: {node_path} - {anomaly['description']}")
            
            return anomaly
            
        except Exception as e:
            logger.error(f"Error analyzing node against target: {e}")
            return None
    
    def _extract_node_level(self, node_path: str) -> str:
        """Extrae el nivel del nodo del path completo"""
        if not node_path:
            return 'Global'
        
        # El nivel es el último elemento del path
        return node_path.split('/')[-1] if '/' in node_path else node_path
    
    def _calculate_severity(self, difference: float) -> str:
        """Calcula la severidad basada en la magnitud de la diferencia"""
        for level, threshold in reversed(list(self.significance_levels.items())):
            if difference >= threshold:
                return level
        return 'low'
    
    def _create_summary(self, anomalies: List[Dict], date_range: Tuple[str, str]) -> str:
        """Crea resumen de las anomalías detectadas"""
        try:
            if not anomalies:
                return f"No target-based anomalies detected for period {date_range[0]} to {date_range[1]}"
            
            total_anomalies = len(anomalies)
            positive_anomalies = len([a for a in anomalies if a['anomaly_type'] == 'positive'])
            negative_anomalies = len([a for a in anomalies if a['anomaly_type'] == 'negative'])
            
            # Contar por severidad
            severity_counts = {}
            for anomaly in anomalies:
                severity = anomaly['severity']
                severity_counts[severity] = severity_counts.get(severity, 0) + 1
            
            # Encontrar los casos más significativos
            critical_cases = [a for a in anomalies if a['severity'] == 'critical']
            
            summary = f"Target-based analysis detected {total_anomalies} anomalies: "
            summary += f"{positive_anomalies} above target, {negative_anomalies} below target. "
            
            if severity_counts:
                severity_desc = []
                for severity, count in severity_counts.items():
                    severity_desc.append(f"{count} {severity}")
                summary += f"Severity: {', '.join(severity_desc)}. "
            
            if critical_cases:
                critical_nodes = [case['node_path'] for case in critical_cases]
                summary += f"Critical cases: {', '.join(critical_nodes)}."
            
            return summary
            
        except Exception as e:
            logger.error(f"Error creating summary: {e}")
            return f"Summary generation failed: {str(e)}"
    
    def export_targets_config(self) -> Dict[str, Any]:
        """
        Exporta la configuración actual de targets
        
        Returns:
            Dict con configuración de targets
        """
        return {
            'targets_config': self.targets_config.copy(),
            'min_surveys_threshold': self.min_surveys_threshold,
            'significance_levels': self.significance_levels.copy(),
            'export_timestamp': datetime.now().isoformat()
        }
    
    def import_targets_config(self, config: Dict[str, Any]):
        """
        Importa configuración de targets
        
        Args:
            config: Configuración a importar
        """
        if 'targets_config' in config:
            self.targets_config = config['targets_config']
            
        if 'min_surveys_threshold' in config:
            self.min_surveys_threshold = config['min_surveys_threshold']
            
        if 'significance_levels' in config:
            self.significance_levels = config['significance_levels']
            
        logger.info("Imported targets configuration")
    
    def get_node_target_history(self, node_path: str, 
                              history_days: int = 30) -> Dict[str, Any]:
        """
        Obtiene el historial de rendimiento vs target para un nodo específico
        
        Args:
            node_path: Nodo a analizar
            history_days: Días de historial a obtener
            
        Returns:
            Dict con historial de rendimiento
        """
        try:
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=history_days)
            
            # Obtener datos históricos diarios
            daily_data = self.pbi_collector.collect_daily_nps_data(
                start_date=start_date.isoformat(),
                end_date=end_date.isoformat(),
                node_path=node_path
            )
            
            if daily_data.empty:
                return {'history': [], 'summary': 'No historical data available'}
            
            node_level = self._extract_node_level(node_path)
            target_config = self.targets_config.get(node_level, {'target': 70.0, 'tolerance': 5.0})
            target_nps = target_config['target']
            tolerance = target_config['tolerance']
            
            history = []
            for _, row in daily_data.iterrows():
                current_nps = row['nps']
                difference = current_nps - target_nps
                
                # Determinar estado
                if abs(difference) <= tolerance:
                    status = 'on_target'
                elif difference > tolerance:
                    status = 'above_target'
                else:
                    status = 'below_target'
                
                history.append({
                    'date': row['date'],
                    'nps': round(current_nps, 1),
                    'target': target_nps,
                    'difference': round(difference, 1),
                    'status': status,
                    'surveys_count': int(row.get('surveys_count', 0))
                })
            
            # Estadísticas del período
            total_days = len(history)
            days_on_target = len([h for h in history if h['status'] == 'on_target'])
            avg_difference = np.mean([h['difference'] for h in history])
            
            summary = f"Target performance over {total_days} days: "
            summary += f"{days_on_target}/{total_days} days on target "
            summary += f"(avg difference: {avg_difference:.1f})"
            
            return {
                'history': history,
                'summary': summary,
                'statistics': {
                    'total_days': total_days,
                    'days_on_target': days_on_target,
                    'target_compliance_rate': round(days_on_target / total_days * 100, 1) if total_days > 0 else 0,
                    'average_difference': round(avg_difference, 1)
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting node target history: {e}")
            return {'history': [], 'summary': f'Error: {str(e)}'} 