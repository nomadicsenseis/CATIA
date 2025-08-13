"""
Data Analyzer - Análisis de datos operativos y métricas complementarias
Proporciona contexto operativo para explicar anomalías NPS
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
import logging
from datetime import datetime, timedelta
from pathlib import Path
import os

logger = logging.getLogger(__name__)


class DataAnalyzer:
    """
    Analizador de datos operativos para complementar análisis NPS
    Soporta tanto análisis LEGACY como FLEXIBLE con múltiples modos de comparación
    """

    def __init__(self, pbi_collector=None, comparison_mode: str = "mean", aggregation_days: int = 1):
        """
        Initialize the Data Analyzer

        Args:
            pbi_collector: Power BI data collector instance
            comparison_mode: Modo de comparación - "mean", "vslast", "target"
            aggregation_days: Días de agregación para análisis flexible (1=legacy, >1=flexible)
        """
        self.pbi_collector = pbi_collector
        self.comparison_mode = comparison_mode
        self.aggregation_days = aggregation_days
        
        # Determinar si usar lógica FLEXIBLE o LEGACY
        self.is_flexible = aggregation_days > 1
        
        # Almacenamiento de datos operativos
        self.operative_data = {}
        
        logger.info(f"DataAnalyzer initialized: comparison_mode={comparison_mode}, aggregation_days={aggregation_days}, flexible={self.is_flexible}")

    def load_operative_data(self, data_folder: str, node_path: str) -> bool:
        """
        Carga datos operativos desde archivos CSV
        Soporta tanto formato LEGACY como FLEXIBLE
        
        Args:
            data_folder: Carpeta con datos CSV
            node_path: Ruta del nodo a cargar
            
        Returns:
            True si se cargaron datos exitosamente
        """
        try:
            data_folder_path = Path(data_folder)
            
            if self.is_flexible:
                # Lógica FLEXIBLE: buscar archivos flexible_operative_Xd.csv
                operative_files = list(data_folder_path.glob(f"flexible_operative_{self.aggregation_days}d*.csv"))
                if not operative_files:
                    logger.warning(f"No flexible operative files found for {self.aggregation_days}d in {data_folder}")
                    return False
                    
                # Tomar el archivo más reciente
                operative_file = sorted(operative_files)[-1]
                logger.info(f"Loading FLEXIBLE operative data from: {operative_file}")
                
            else:
                # Lógica LEGACY: buscar operative.csv tradicional
                operative_file = data_folder_path / "operative.csv"
                if not operative_file.exists():
                    logger.warning(f"No legacy operative.csv found in {data_folder}")
                    return False
                    
                logger.info(f"Loading LEGACY operative data from: {operative_file}")
            
            # Cargar el archivo CSV
            operative_data = pd.read_csv(operative_file)
            
            if operative_data.empty:
                logger.warning(f"Empty operative data loaded from {operative_file}")
                return False
            
            # Filtrar por node_path si es necesario
            if 'node_path' in operative_data.columns:
                node_data = operative_data[operative_data['node_path'] == node_path]
                if node_data.empty:
                    logger.warning(f"No data found for node_path: {node_path}")
                    return False
                self.operative_data[node_path] = node_data
            else:
                # Asumir que todos los datos son para este nodo
                self.operative_data[node_path] = operative_data
            
            logger.info(f"Loaded {len(self.operative_data[node_path])} operative records for {node_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading operative data: {e}")
            return False

    def analyze_operative_metrics(self, node_path: str, target_date: str) -> Dict[str, Any]:
        """
        Analiza métricas operativas usando el modo de comparación configurado
        
        Args:
            node_path: Ruta del nodo en el árbol jerárquico
            target_date: Fecha objetivo para el análisis (YYYY-MM-DD)
            
        Returns:
            Dict con análisis de métricas operativas
        """
        try:
            if node_path not in self.operative_data:
                return {"error": f"No operative data available for {node_path}"}
                
            if self.is_flexible:
                # Usar análisis flexible basado en comparison_mode
                if self.comparison_mode == "vslast":
                    return self._analyze_vslast_comparison(node_path, target_date)
                elif self.comparison_mode == "mean":
                    return self._analyze_mean_comparison(node_path, target_date)
                elif self.comparison_mode == "target":
                    return self._analyze_target_comparison(node_path, target_date)
                else:
                    return self._analyze_flexible_comparison(node_path, target_date)
            else:
                # Usar análisis legacy tradicional
                return self._analyze_legacy_operative(node_path, target_date)
                
        except Exception as e:
            logger.error(f"Error analyzing operative metrics: {e}")
            return {"error": str(e)}

    def _analyze_flexible_comparison(self, node_path: str, target_date: str) -> Dict[str, Any]:
        """
        Análisis flexible genérico basado en períodos de agregación
        """
        try:
            data = self.operative_data[node_path]
            target_dt = pd.to_datetime(target_date)
            
            # Limpiar columnas DAX y asegurar formato correcto
            data = self._clean_dax_columns(data)
            
            # Asegurar formato de fecha
            if 'Date' in data.columns:
                data['Date'] = pd.to_datetime(data['Date'])
            elif 'date' in data.columns:
                data['date'] = pd.to_datetime(data['date'])
                data['Date'] = data['date']  # Normalizar
            else:
                return {"error": "No date column found in operative data"}
            
            # Filtrar datos relevantes para el análisis
            # En análisis flexible, cada fila representa un período agregado
            current_period_data = data[data['Date'] <= target_dt].tail(2)  # Último y penúltimo período
            
            if current_period_data.empty:
                return {"error": f"No data available for target date {target_date}"}
            
            current_period = current_period_data.iloc[-1]
            
            metrics = {}
            base_metrics = ['Load_Factor', 'OTP15_adjusted', 'Mishandling', 'Misconex']
            
            for metric in base_metrics:
                if metric in current_period:
                    current_val = pd.to_numeric(current_period[metric], errors='coerce')
                    if pd.notna(current_val):
                        metrics[metric] = {
                            'current': round(current_val, 2),
                            'aggregation_days': self.aggregation_days
                        }
            
            return {
                'mode': 'flexible',
                'comparison_mode': self.comparison_mode,
                'aggregation_days': self.aggregation_days,
                'target_date': target_date,
                'metrics': metrics,
                'summary': self._create_flexible_summary(metrics)
            }
            
        except Exception as e:
            return {"error": f"Error in flexible comparison: {str(e)}"}

    def _analyze_vslast_comparison(self, node_path: str, target_date: str) -> Dict[str, Any]:
        """
        Análisis FLEXIBLE vs período anterior
        """
        try:
            data = self.operative_data[node_path]
            target_dt = pd.to_datetime(target_date)
            
            # Limpiar columnas DAX y asegurar formato correcto
            data = self._clean_dax_columns(data)
            
            # Normalizar columna de fecha
            if 'Date' in data.columns:
                data['Date'] = pd.to_datetime(data['Date'])
            elif 'date' in data.columns:
                data['date'] = pd.to_datetime(data['date'])
                data['Date'] = data['date']
            else:
                return {"error": "No date column found"}
            
            # Ordenar por fecha y obtener los últimos 2 períodos
            data_sorted = data.sort_values('Date')
            recent_periods = data_sorted.tail(2)
            
            if len(recent_periods) < 2:
                return {"error": "Insufficient data for vslast comparison"}
            
            current_period = recent_periods.iloc[-1]
            previous_period = recent_periods.iloc[-2]
            
            metrics = {}
            base_metrics = ['Load_Factor', 'OTP15_adjusted', 'Mishandling', 'Misconex']
            
            for metric in base_metrics:
                if metric in current_period and metric in previous_period:
                    current_val = pd.to_numeric(current_period[metric], errors='coerce')
                    previous_val = pd.to_numeric(previous_period[metric], errors='coerce')
                    
                    if pd.notna(current_val) and pd.notna(previous_val):
                        difference = current_val - previous_val
                        change_pct = (difference / previous_val) * 100 if previous_val != 0 else 0
                        
                        metrics[metric] = {
                            'current': round(current_val, 2),
                            'previous': round(previous_val, 2),
                            'difference': round(difference, 2),
                            'change_pct': round(change_pct, 1)
                        }
            
            return {
                'mode': 'vslast_flexible',
                'aggregation_days': self.aggregation_days,
                'current_period_date': current_period['Date'].strftime('%Y-%m-%d'),
                'previous_period_date': previous_period['Date'].strftime('%Y-%m-%d'),
                'metrics': metrics,
                'summary': self._create_vslast_flexible_summary(metrics)
            }
            
        except Exception as e:
            return {"error": f"Error in vslast flexible comparison: {str(e)}"}

    def _analyze_mean_comparison(self, node_path: str, target_date: str) -> Dict[str, Any]:
        """
        Análisis FLEXIBLE vs media de períodos anteriores
        """
        try:
            data = self.operative_data[node_path]
            target_dt = pd.to_datetime(target_date)
            
            # Limpiar columnas DAX y asegurar formato correcto
            data = self._clean_dax_columns(data)
            
            # Normalizar fecha
            if 'Date' in data.columns:
                data['Date'] = pd.to_datetime(data['Date'])
            elif 'date' in data.columns:
                data['date'] = pd.to_datetime(data['date'])
                data['Date'] = data['date']
            else:
                return {"error": "No date column found"}
            
            # Ordenar y obtener el período actual y los anteriores para calcular media
            data_sorted = data.sort_values('Date')
            
            # Tomar los últimos 4 períodos (1 actual + 3 para media)
            recent_periods = data_sorted.tail(4)
            
            if len(recent_periods) < 2:
                return {"error": "Insufficient data for mean comparison"}
            
            current_period = recent_periods.iloc[-1]
            historical_periods = recent_periods.iloc[:-1]  # Todos excepto el último
            
            metrics = {}
            base_metrics = ['Load_Factor', 'OTP15_adjusted', 'Mishandling', 'Misconex']
            
            for metric in base_metrics:
                if metric in current_period:
                    current_val = pd.to_numeric(current_period[metric], errors='coerce')
                    historical_vals = pd.to_numeric(historical_periods[metric], errors='coerce')
                    historical_mean = historical_vals.mean()
                    
                    if pd.notna(current_val) and pd.notna(historical_mean):
                        difference = current_val - historical_mean
                        change_pct = (difference / historical_mean) * 100 if historical_mean != 0 else 0
                        
                        metrics[metric] = {
                            'current': round(current_val, 2),
                            'historical_mean': round(historical_mean, 2),
                            'difference': round(difference, 2),
                            'change_pct': round(change_pct, 1),
                            'periods_in_mean': len(historical_vals.dropna())
                        }
            
            return {
                'mode': 'mean_flexible',
                'aggregation_days': self.aggregation_days,
                'current_period_date': current_period['Date'].strftime('%Y-%m-%d'),
                'historical_periods': len(historical_periods),
                'metrics': metrics,
                'summary': self._create_mean_flexible_summary(metrics)
            }
            
        except Exception as e:
            return {"error": f"Error in mean flexible comparison: {str(e)}"}

    def _analyze_target_comparison(self, node_path: str, target_date: str) -> Dict[str, Any]:
        """
        Análisis FLEXIBLE vs targets predefinidos
        """
        try:
            data = self.operative_data[node_path]
            
            # Limpiar columnas DAX y asegurar formato correcto
            data = self._clean_dax_columns(data)
            
            # Normalizar fecha
            if 'Date' in data.columns:
                data['Date'] = pd.to_datetime(data['Date'])
            elif 'date' in data.columns:
                data['date'] = pd.to_datetime(data['date'])
                data['Date'] = data['date']
            else:
                return {"error": "No date column found"}
            
            # Obtener el período más reciente
            data_sorted = data.sort_values('Date')
            current_period = data_sorted.iloc[-1]
            
            # Targets operativos estándar
            targets = {
                'Load_Factor': 85.0,
                'OTP15_adjusted': 90.0,
                'Mishandling': 0.5,
                'Misconex': 0.3
            }
            
            metrics = {}
            
            for metric, target_val in targets.items():
                if metric in current_period:
                    current_val = pd.to_numeric(current_period[metric], errors='coerce')
                    
                    if pd.notna(current_val):
                        difference = current_val - target_val
                        performance = 'above_target' if difference > 0 else 'below_target' if difference < 0 else 'on_target'
                        
                        metrics[metric] = {
                            'current': round(current_val, 2),
                            'target': target_val,
                            'difference': round(difference, 2),
                            'performance': performance
                        }
            
            return {
                'mode': 'target_flexible',
                'aggregation_days': self.aggregation_days,
                'current_period_date': current_period['Date'].strftime('%Y-%m-%d'),
                'metrics': metrics,
                'summary': self._create_target_flexible_summary(metrics)
            }
            
        except Exception as e:
            return {"error": f"Error in target flexible comparison: {str(e)}"}

    def _analyze_legacy_operative(self, node_path: str, target_date: str) -> Dict[str, Any]:
        """
        Análisis LEGACY tradicional (aggregation_days = 1)
        """
        try:
            data = self.operative_data[node_path]
            target_dt = pd.to_datetime(target_date)
            
            # Limpiar columnas DAX y asegurar formato correcto
            data = self._clean_dax_columns(data)
            
            # Para análisis legacy, buscar el día específico
            if 'Date' in data.columns:
                data['Date'] = pd.to_datetime(data['Date'])
                target_data = data[data['Date'] == target_dt]
            else:
                return {"error": "No Date column found in legacy data"}
            
            if target_data.empty:
                return {"error": f"No legacy data for target date {target_date}"}
            
            target_row = target_data.iloc[0]
            
            metrics = {}
            base_metrics = ['Load_Factor', 'OTP15_adjusted', 'Mishandling', 'Misconex']
            
            for metric in base_metrics:
                if metric in target_row:
                    val = pd.to_numeric(target_row[metric], errors='coerce')
                    if pd.notna(val):
                        metrics[metric] = {
                            'value': round(val, 2),
                            'date': target_date
                        }
            
            return {
                'mode': 'legacy',
                'target_date': target_date,
                'metrics': metrics,
                'summary': self._create_legacy_summary(metrics)
            }
            
        except Exception as e:
            return {"error": f"Error in legacy analysis: {str(e)}"}

    def get_specific_explanations(self, node_path: str, target_date: str, anomaly_type: str, aggregation_days: int = 7) -> Dict[str, str]:
        """
        Obtiene explicaciones específicas basadas en el tipo de anomalía
        Adaptado para datos agregados por período
        
        Returns:
            Dict con claves 'otp_explanation', 'load_factor_explanation', 'mishandling_explanation'

        Args:
            node_path: Ruta del nodo
            target_date: Fecha objetivo
            anomaly_type: Tipo de anomalía ('positive', 'negative', 'unknown')
            aggregation_days: Días de agregación para el análisis

        Returns:
            Diccionario con explicaciones específicas por métrica
        """
        try:
            result = {
                'otp_explanation': "No OTP data available",
                'load_factor_explanation': "No Load Factor data available", 
                'mishandling_explanation': "No Mishandling data available"
            }

            if node_path not in self.operative_data:
                return result

            data = self.operative_data[node_path]
            if data.empty:
                return result

            # Limpiar columnas DAX y asegurar formato correcto
            data = self._clean_dax_columns(data)
            target_dt = pd.to_datetime(target_date)

            # Para datos agregados por período, buscar el período que contiene la fecha objetivo
            target_row = None
            
            if 'Period_Group' in data.columns and 'Min_Date' in data.columns and 'Max_Date' in data.columns:
                # Convertir Min_Date y Max_Date a datetime para comparación
                data['Min_Date'] = pd.to_datetime(data['Min_Date'])
                data['Max_Date'] = pd.to_datetime(data['Max_Date'])
                
                # Encontrar el período que contiene la fecha objetivo
                target_period = data[
                    (data['Min_Date'] <= target_dt) & 
                    (data['Max_Date'] >= target_dt)
                ]
                
                if target_period.empty:
                    # Si no hay período exacto, buscar el más cercano
                    data['distance'] = abs((data['Min_Date'] + (data['Max_Date'] - data['Min_Date'])/2) - target_dt).dt.days
                    target_period = data.loc[data['distance'].idxmin():data['distance'].idxmin()]
                    self.logger.info(f"📅 No exact period found, using closest period for {target_dt.date()}")
                
                target_row = target_period.iloc[0]
                
            else:
                # Lógica original para datos por fecha exacta
                if 'Date' not in data.columns:
                    return result
                
                target_data = data[data['Date'] == target_dt]
                
                if target_data.empty:
                    return result
                
                target_row = target_data.iloc[0]

            # Análisis específico por métrica
            load_factor_explanation = self._explain_load_factor(target_row, anomaly_type)
            if load_factor_explanation:
                result['load_factor_explanation'] = load_factor_explanation

            otp_explanation = self._explain_otp(target_row, anomaly_type)
            if otp_explanation:
                result['otp_explanation'] = otp_explanation

            mishandling_explanation = self._explain_mishandling(target_row, anomaly_type)
            if mishandling_explanation:
                result['mishandling_explanation'] = mishandling_explanation

            return result

        except Exception as e:
            self.logger.error(f"Error getting specific explanations: {e}")
            return {
                'otp_explanation': f"Error analyzing OTP: {str(e)}",
                'load_factor_explanation': f"Error analyzing Load Factor: {str(e)}",
                'mishandling_explanation': f"Error analyzing Mishandling: {str(e)}"
            }

    def _generate_metric_explanation(self, metric: str, data: Dict, anomaly_type: str, mode: str) -> Optional[str]:
        """Genera explicación específica para una métrica según el modo de análisis"""
        try:
            metric_display = self._get_metric_display_name(metric)
            
            if mode.startswith('vslast'):
                # Explicaciones para comparación vs período anterior
                if 'difference' in data and abs(data['difference']) > 0.1:
                    direction = "aumentó" if data['difference'] > 0 else "disminuyó"
                    return f"{metric_display} {direction} {abs(data['difference'])} vs período anterior"
                    
            elif mode.startswith('mean'):
                # Explicaciones para comparación vs media
                if 'difference' in data and abs(data['difference']) > 0.1:
                    direction = "superior" if data['difference'] > 0 else "inferior"
                    return f"{metric_display} {direction} a la media histórica en {abs(data['difference'])}"
                    
            elif mode.startswith('target'):
                # Explicaciones para comparación vs targets
                if 'performance' in data and data['performance'] != 'on_target':
                    if data['performance'] == 'above_target':
                        return f"{metric_display} superó el target en {data['difference']}"
                    else:
                        return f"{metric_display} por debajo del target en {abs(data['difference'])}"
                        
            elif mode == 'legacy':
                # Explicaciones para modo legacy
                value = data.get('value', 0)
                return self._generate_legacy_explanation(metric, value, anomaly_type)
            
            return None
            
        except Exception:
            return None

    def _generate_legacy_explanation(self, metric: str, value: float, anomaly_type: str) -> Optional[str]:
        """Genera explicaciones específicas para modo legacy"""
        metric_display = self._get_metric_display_name(metric)
        
        if metric == 'Load_Factor':
            if value > 90 and anomaly_type == 'negative':
                return f"{metric_display} muy alto ({value}%) puede haber impactado la experiencia"
            elif value < 70 and anomaly_type == 'positive':
                return f"{metric_display} bajo ({value}%) puede haber mejorado la comodidad"
        
        elif metric == 'OTP15_adjusted':
            if value < 80 and anomaly_type == 'negative':
                return f"{metric_display} baja ({value}%) puede haber generado insatisfacción"
            elif value > 95 and anomaly_type == 'positive':
                return f"{metric_display} excelente ({value}%) contribuyó a la mejora"
        
        elif metric == 'Mishandling':
            if value > 1.0 and anomaly_type == 'negative':
                return f"{metric_display} alta ({value}%) impactó negativamente"
            elif value < 0.3 and anomaly_type == 'positive':
                return f"{metric_display} baja ({value}%) contribuyó a la mejora"
        
        return None

    # Métodos de resumen específicos para cada modo
    def _create_flexible_summary(self, metrics: Dict) -> str:
        """Crea resumen para análisis flexible genérico"""
        if not metrics:
            return f"Análisis flexible ({self.aggregation_days}d): sin datos disponibles"
        
        metrics_count = len(metrics)
        return f"Análisis flexible {self.aggregation_days}d: {metrics_count} métricas analizadas"

    def _create_vslast_flexible_summary(self, metrics: Dict) -> str:
        """Crea resumen para vslast flexible"""
        if not metrics:
            return f"Análisis {self.aggregation_days}d vs período anterior: sin cambios significativos"
        
        changes = []
        for metric, data in metrics.items():
            if abs(data.get('difference', 0)) > 0.1:
                direction = "↑" if data['difference'] > 0 else "↓"
                metric_name = self._get_metric_display_name(metric)
                changes.append(f"{metric_name}{direction}")
        
        if changes:
            return f"Análisis {self.aggregation_days}d vs anterior: {', '.join(changes)}"
        else:
            return f"Análisis {self.aggregation_days}d: métricas estables vs período anterior"

    def _create_mean_flexible_summary(self, metrics: Dict) -> str:
        """Crea resumen para mean flexible"""
        if not metrics:
            return f"Análisis {self.aggregation_days}d vs media: sin datos"
        
        above_mean = sum(1 for data in metrics.values() if data.get('difference', 0) > 0.1)
        below_mean = sum(1 for data in metrics.values() if data.get('difference', 0) < -0.1)
        
        return f"Análisis {self.aggregation_days}d vs media: {above_mean} métricas superiores, {below_mean} inferiores"

    def _create_target_flexible_summary(self, metrics: Dict) -> str:
        """Crea resumen para target flexible"""
        if not metrics:
            return f"Análisis {self.aggregation_days}d vs targets: sin datos"
        
        on_target = sum(1 for data in metrics.values() if data.get('performance') == 'on_target')
        total = len(metrics)
        
        return f"Análisis {self.aggregation_days}d vs targets: {on_target}/{total} en objetivo"

    def _create_legacy_summary(self, metrics: Dict) -> str:
        """Crea resumen para análisis legacy"""
        if not metrics:
            return "Análisis legacy: sin datos operativos"
        
        return f"Análisis legacy: {len(metrics)} métricas operativas disponibles"

    def get_operational_metrics(self, date_range: Tuple[str, str], node_path: str,
                              causal_filter: Optional[str] = None) -> Dict[str, Any]:
        """
        Obtiene métricas operativas para el período y nodo especificado

        Args:
            date_range: Tupla con (start_date, end_date)
            node_path: Ruta del nodo en el árbol jerárquico
            causal_filter: Filtro de comparación para modo comparativo

        Returns:
            Dict con métricas operativas
        """
        try:
            metrics = {}

            # Obtener Load Factor
            load_factor_data = self._get_load_factor(date_range, node_path, causal_filter)
            metrics['load_factor'] = load_factor_data

            # Obtener Mishandling
            mishandling_data = self._get_mishandling_metrics(date_range, node_path, causal_filter)
            metrics['mishandling'] = mishandling_data

            # Obtener OTP (On-Time Performance)
            otp_data = self._get_otp_metrics(date_range, node_path, causal_filter)
            metrics['otp'] = otp_data

            # Obtener cambios de aeronave
            aircraft_changes = self._get_aircraft_changes(date_range, node_path, causal_filter)
            metrics['aircraft_changes'] = aircraft_changes

            # Crear resumen ejecutivo
            metrics['summary'] = self._create_operational_summary(metrics, causal_filter)

            return metrics

        except Exception as e:
            logger.error(f"Error getting operational metrics: {e}")
            return {"error": str(e), "summary": "Error obteniendo métricas operativas"}

    def analyze_customer_segments(self, date_range: Tuple[str, str], node_path: str,
                                anomaly_type: str, causal_filter: Optional[str] = None) -> Dict[str, Any]:
        """
        Analiza segmentos de clientes y su reactividad a la anomalía

        Args:
            date_range: Tupla con fechas
            node_path: Ruta del nodo
            anomaly_type: 'positive' o 'negative'
            causal_filter: Filtro de comparación

        Returns:
            Dict con análisis de segmentos de clientes
        """
        try:
            # Obtener datos de customer profile
            customer_data = self.pbi_collector.collect_customer_profile_data(
                start_date=date_range[0],
                end_date=date_range[1],
                node_path=node_path,
                comparison_filter=causal_filter
            )

            if customer_data.empty:
                return {"segments": [], "summary": "No hay datos de customer profile disponibles"}

            # Procesar segmentos
            segments = self._process_customer_segments(customer_data, anomaly_type, causal_filter)

            # Identificar segmentos más reactivos
            reactive_segments = self._identify_reactive_segments(segments, anomaly_type)

            # Crear resumen
            summary = self._create_customer_summary(segments, reactive_segments, anomaly_type)

            return {
                'segments': segments,
                'most_reactive': reactive_segments,
                'summary': summary
            }

        except Exception as e:
            logger.error(f"Error analyzing customer segments: {e}")
            return {"segments": [], "summary": f"Error: {str(e)}"}

    def correlate_operational_with_nps(self, operational_data: Dict, nps_data: Dict,
                                     anomaly_type: str) -> Dict[str, Any]:
        """
        Correlaciona métricas operativas con datos NPS

        Args:
            operational_data: Datos operativos
            nps_data: Datos NPS
            anomaly_type: Tipo de anomalía

        Returns:
            Dict con correlaciones y insights
        """
        try:
            correlations = {}
            insights = []

            # Correlación Load Factor - NPS
            if 'load_factor' in operational_data:
                lf_correlation = self._correlate_load_factor_nps(
                    operational_data['load_factor'], nps_data, anomaly_type
                )
                correlations['load_factor_nps'] = lf_correlation
                if lf_correlation['significant']:
                    insights.append(lf_correlation['insight'])

            # Correlación Mishandling - NPS
            if 'mishandling' in operational_data:
                mh_correlation = self._correlate_mishandling_nps(
                    operational_data['mishandling'], nps_data, anomaly_type
                )
                correlations['mishandling_nps'] = mh_correlation
                if mh_correlation['significant']:
                    insights.append(mh_correlation['insight'])

            # Correlación OTP - NPS
            if 'otp' in operational_data:
                otp_correlation = self._correlate_otp_nps(
                    operational_data['otp'], nps_data, anomaly_type
                )
                correlations['otp_nps'] = otp_correlation
                if otp_correlation['significant']:
                    insights.append(otp_correlation['insight'])

            return {
                'correlations': correlations,
                'key_insights': insights,
                'summary': f"Identificadas {len(insights)} correlaciones significativas"
            }

        except Exception as e:
            logger.error(f"Error correlating operational with NPS: {e}")
            return {"correlations": {}, "key_insights": [], "summary": f"Error: {str(e)}"}

    def _get_load_factor(self, date_range: Tuple[str, str], node_path: str,
                         causal_filter: Optional[str] = None) -> Dict[str, Any]:
        """Obtiene datos de Load Factor"""
        try:
            lf_data = self.pbi_collector.collect_operational_data(
                start_date=date_range[0],
                end_date=date_range[1],
                node_path=node_path,
                metric='load_factor',
                comparison_filter=causal_filter
            )

            if lf_data.empty:
                return {"value": None, "trend": "no_data", "summary": "No hay datos de Load Factor"}

            current_lf = lf_data['load_factor'].mean()

            result = {
                "value": round(current_lf, 1),
                "summary": f"Load Factor promedio: {round(current_lf, 1)}%"
            }

            # Agregar comparación si está en modo comparativo
            if causal_filter and 'load_factor_diff' in lf_data.columns:
                lf_diff = lf_data['load_factor_diff'].mean()
                result["difference"] = round(lf_diff, 1)
                trend = "aumentó" if lf_diff > 0 else "disminuyó" if lf_diff < 0 else "se mantuvo"
                result["summary"] += f", {trend} {abs(round(lf_diff, 1))}pp vs período anterior"
                result["trend"] = "up" if lf_diff > 0 else "down" if lf_diff < 0 else "stable"

            return result

        except Exception as e:
            logger.error(f"Error getting load factor: {e}")
            return {"value": None, "summary": f"Error obteniendo Load Factor: {str(e)}"}

    def _get_mishandling_metrics(self, date_range: Tuple[str, str], node_path: str,
                               causal_filter: Optional[str] = None) -> Dict[str, Any]:
        """Obtiene métricas de Mishandling"""
        try:
            mh_data = self.pbi_collector.collect_operational_data(
                start_date=date_range[0],
                end_date=date_range[1],
                node_path=node_path,
                metric='mishandling',
                comparison_filter=causal_filter
            )

            if mh_data.empty:
                return {"rate": None, "summary": "No hay datos de Mishandling"}

            current_mh = mh_data['mishandling_rate'].mean()

            result = {
                "rate": round(current_mh, 2),
                "summary": f"Tasa de Mishandling: {round(current_mh, 2)}%"
            }

            # Agregar comparación si está disponible
            if causal_filter and 'mishandling_rate_diff' in mh_data.columns:
                mh_diff = mh_data['mishandling_rate_diff'].mean()
                result["difference"] = round(mh_diff, 2)
                trend = "aumentó" if mh_diff > 0 else "disminuyó" if mh_diff < 0 else "se mantuvo"
                result["summary"] += f", {trend} {abs(round(mh_diff, 2))}pp vs período anterior"
                result["trend"] = "up" if mh_diff > 0 else "down" if mh_diff < 0 else "stable"

            return result

        except Exception as e:
            logger.error(f"Error getting mishandling metrics: {e}")
            return {"rate": None, "summary": f"Error obteniendo Mishandling: {str(e)}"}

    def _get_otp_metrics(self, date_range: Tuple[str, str], node_path: str,
                         causal_filter: Optional[str] = None) -> Dict[str, Any]:
        """Obtiene métricas de OTP (On-Time Performance)"""
        try:
            otp_data = self.pbi_collector.collect_operational_data(
                start_date=date_range[0],
                end_date=date_range[1],
                node_path=node_path,
                metric='otp',
                comparison_filter=causal_filter
            )

            if otp_data.empty:
                return {"percentage": None, "summary": "No hay datos de OTP"}

            current_otp = otp_data['otp_percentage'].mean()

            result = {
                "percentage": round(current_otp, 1),
                "summary": f"OTP: {round(current_otp, 1)}%"
            }

            # Agregar comparación si está disponible
            if causal_filter and 'otp_percentage_diff' in otp_data.columns:
                otp_diff = otp_data['otp_percentage_diff'].mean()
                result["difference"] = round(otp_diff, 1)
                trend = "mejoró" if otp_diff > 0 else "empeoró" if otp_diff < 0 else "se mantuvo"
                result["summary"] += f", {trend} {abs(round(otp_diff, 1))}pp vs período anterior"
                result["trend"] = "up" if otp_diff > 0 else "down" if otp_diff < 0 else "stable"

            return result

        except Exception as e:
            logger.error(f"Error getting OTP metrics: {e}")
            return {"percentage": None, "summary": f"Error obteniendo OTP: {str(e)}"}

    def _get_aircraft_changes(self, date_range: Tuple[str, str], node_path: str,
                             causal_filter: Optional[str] = None) -> Dict[str, Any]:
        """Obtiene datos de cambios de aeronave"""
        try:
            ac_data = self.pbi_collector.collect_operational_data(
                start_date=date_range[0],
                end_date=date_range[1],
                node_path=node_path,
                metric='aircraft_changes',
                comparison_filter=causal_filter
            )

            if ac_data.empty:
                return {"count": 0, "summary": "No hay datos de cambios de aeronave"}

            changes_count = ac_data['aircraft_changes_count'].sum()

            result = {
                "count": int(changes_count),
                "summary": f"{int(changes_count)} cambios de aeronave"
            }

            # Agregar comparación si está disponible
            if causal_filter and 'aircraft_changes_diff' in ac_data.columns:
                changes_diff = ac_data['aircraft_changes_diff'].sum()
                result["difference"] = int(changes_diff)
                trend = "más" if changes_diff > 0 else "menos" if changes_diff < 0 else "igual"
                result["summary"] += f", {abs(int(changes_diff))} {trend} que período anterior"
                result["trend"] = "up" if changes_diff > 0 else "down" if changes_diff < 0 else "stable"

            return result

        except Exception as e:
            logger.error(f"Error getting aircraft changes: {e}")
            return {"count": 0, "summary": f"Error obteniendo cambios aeronave: {str(e)}"}

    def _process_customer_segments(self, customer_data: pd.DataFrame, anomaly_type: str,
                                   causal_filter: Optional[str] = None) -> List[Dict]:
        """Procesa segmentos de clientes"""
        segments = []

        try:
            # Agrupar por segmento
            segment_columns = ['customer_segment', 'frequent_flyer_tier', 'booking_channel']

            for col in segment_columns:
                if col in customer_data.columns:
                    grouped = customer_data.groupby(col).agg({
                        'nps': 'mean',
                        'surveys_count': 'sum'
                    }).reset_index()

                    # Agregar diferencias si es modo comparativo
                    if causal_filter and 'nps_diff' in customer_data.columns:
                        nps_diff_data = customer_data.groupby(col)['nps_diff'].mean().reset_index()
                        grouped = grouped.merge(nps_diff_data, on=col)

                    for _, segment in grouped.iterrows():
                        segment_info = {
                            'type': col,
                            'name': segment[col],
                            'nps': round(segment['nps'], 1),
                            'surveys_count': int(segment['surveys_count'])
                        }

                        if causal_filter and 'nps_diff' in segment:
                            segment_info['nps_diff'] = round(segment['nps_diff'], 1)
                            segment_info['reactivity'] = abs(segment['nps_diff'])

                        segments.append(segment_info)

            return segments

        except Exception as e:
            logger.error(f"Error processing customer segments: {e}")
            return []

    def _identify_reactive_segments(self, segments: List[Dict], anomaly_type: str) -> List[Dict]:
        """Identifica segmentos más reactivos"""
        try:
            if not segments:
                return []

            # Filtrar segmentos con datos de reactividad
            reactive_segments = [s for s in segments if 'reactivity' in s and s['surveys_count'] >= 10]

            if not reactive_segments:
                return []

            # Ordenar por reactividad (mayor diferencia absoluta)
            reactive_segments.sort(key=lambda x: x['reactivity'], reverse=True)

            # Tomar los top 5 más reactivos
            return reactive_segments[:5]

        except Exception as e:
            logger.error(f"Error identifying reactive segments: {e}")
            return []

    def _create_operational_summary(self, metrics: Dict, causal_filter: Optional[str] = None) -> str:
        """Crea resumen ejecutivo de métricas operativas"""
        try:
            summary_parts = []

            # Load Factor
            if 'load_factor' in metrics and metrics['load_factor'].get('value'):
                lf_summary = metrics['load_factor']['summary']
                summary_parts.append(f"Load Factor: {lf_summary}")

            # Mishandling
            if 'mishandling' in metrics and metrics['mishandling'].get('rate'):
                mh_summary = metrics['mishandling']['summary']
                summary_parts.append(f"Mishandling: {mh_summary}")

            # OTP
            if 'otp' in metrics and metrics['otp'].get('percentage'):
                otp_summary = metrics['otp']['summary']
                summary_parts.append(f"Puntualidad: {otp_summary}")

            # Aircraft Changes
            if 'aircraft_changes' in metrics:
                ac_summary = metrics['aircraft_changes']['summary']
                summary_parts.append(f"Cambios aeronave: {ac_summary}")

            if summary_parts:
                full_summary = ". ".join(summary_parts) + "."
                if causal_filter:
                    full_summary += f" Análisis comparativo {causal_filter}."
                return full_summary
            else:
                return "No hay datos operativos disponibles para el período analizado."

        except Exception as e:
            logger.error(f"Error creating operational summary: {e}")
            return "Error generando resumen operativo."

    def _create_customer_summary(self, segments: List[Dict], reactive_segments: List[Dict],
                               anomaly_type: str) -> str:
        """Crea resumen de análisis de clientes"""
        try:
            if not segments:
                return "No hay datos de segmentos de clientes disponibles."

            total_segments = len(segments)
            summary = f"Analizados {total_segments} segmentos de clientes."

            if reactive_segments:
                most_reactive = reactive_segments[0]
                summary += f" Segmento más reactivo: {most_reactive['name']} "
                summary += f"({most_reactive['type']}) con cambio de {abs(most_reactive.get('nps_diff', 0))} puntos NPS."

            return summary

        except Exception as e:
            logger.error(f"Error creating customer summary: {e}")
            return "Error generando resumen de clientes."

    def _correlate_load_factor_nps(self, lf_data: Dict, nps_data: Dict, anomaly_type: str) -> Dict:
        """Correlaciona Load Factor con NPS"""
        try:
            # Lógica simplificada de correlación
            correlation = {
                'significant': False,
                'correlation_strength': 'none',
                'insight': ''
            }

            if lf_data.get('trend') and lf_data.get('difference'):
                lf_change = lf_data['difference']

                # Correlación inversa típica: más load factor, menor NPS
                if anomaly_type == 'negative' and lf_change > 2:
                    correlation['significant'] = True
                    correlation['correlation_strength'] = 'moderate'
                    correlation['insight'] = f"El aumento del Load Factor (+{lf_change}pp) puede haber contribuido a la caída del NPS"
                elif anomaly_type == 'positive' and lf_change < -2:
                    correlation['significant'] = True
                    correlation['correlation_strength'] = 'moderate'
                    correlation['insight'] = f"La reducción del Load Factor ({lf_change}pp) puede haber contribuido a la mejora del NPS"

            return correlation

        except Exception as e:
            logger.error(f"Error correlating load factor: {e}")
            return {'significant': False, 'correlation_strength': 'error', 'insight': ''}

    def _correlate_mishandling_nps(self, mh_data: Dict, nps_data: Dict, anomaly_type: str) -> Dict:
        """Correlaciona Mishandling con NPS"""
        try:
            correlation = {
                'significant': False,
                'correlation_strength': 'none',
                'insight': ''
            }

            if mh_data.get('trend') and mh_data.get('difference'):
                mh_change = mh_data['difference']

                # Correlación directa: más mishandling, menor NPS
                if anomaly_type == 'negative' and mh_change > 0.1:
                    correlation['significant'] = True
                    correlation['correlation_strength'] = 'strong'
                    correlation['insight'] = f"El aumento del Mishandling (+{mh_change}pp) correlaciona con la caída del NPS"
                elif anomaly_type == 'positive' and mh_change < -0.1:
                    correlation['significant'] = True
                    correlation['correlation_strength'] = 'strong'
                    correlation['insight'] = f"La reducción del Mishandling ({mh_change}pp) correlaciona con la mejora del NPS"

            return correlation

        except Exception as e:
            logger.error(f"Error correlating mishandling: {e}")
            return {'significant': False, 'correlation_strength': 'error', 'insight': ''}

    def _correlate_otp_nps(self, otp_data: Dict, nps_data: Dict, anomaly_type: str) -> Dict:
        """Correlaciona OTP con NPS"""
        try:
            correlation = {
                'significant': False,
                'correlation_strength': 'none',
                'insight': ''
            }

            if otp_data.get('trend') and otp_data.get('difference'):
                otp_change = otp_data['difference']

                # Correlación directa: mejor OTP, mejor NPS
                if anomaly_type == 'positive' and otp_change > 2:
                    correlation['significant'] = True
                    correlation['correlation_strength'] = 'moderate'
                    correlation['insight'] = f"La mejora del OTP (+{otp_change}pp) correlaciona con la subida del NPS"
                elif anomaly_type == 'negative' and otp_change < -2:
                    correlation['significant'] = True
                    correlation['correlation_strength'] = 'moderate'
                    correlation['insight'] = f"El deterioro del OTP ({otp_change}pp) correlaciona con la caída del NPS"

            return correlation

        except Exception as e:
            logger.error(f"Error correlating OTP: {e}")
            return {'significant': False, 'correlation_strength': 'error', 'insight': ''}

    def _get_metric_display_name(self, metric: str) -> str:
        """Convierte nombres técnicos a nombres de display"""
        display_names = {
            'Load_Factor': 'Load Factor',
            'OTP15_adjusted': 'OTP',
            'Mishandling': 'Mishandling',
            'Misconex': 'Conexiones Perdidas'
        }
        return display_names.get(metric, metric)

    def _clean_dax_columns(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Clean DAX column names and convert to standard format.
        Similar to pbi_collector.py logic.
        """
        # Limpiar nombres de columnas DAX
        if 'Date_Master[Date' in data.columns:
            data.rename(columns={'Date_Master[Date': 'Date_Master'}, inplace=True)
        
        # Convertir Date_Master a Date para compatibilidad
        if 'Date_Master' in data.columns:
            data['Date'] = pd.to_datetime(data['Date_Master']).dt.date
        elif 'Date_Master[Date]' in data.columns:
            data['Date'] = pd.to_datetime(data['Date_Master[Date]']).dt.date
        
        # Para datos operativos flexibles, usar Min_Date como Date principal
        elif 'Min_Date' in data.columns:
            data['Date'] = pd.to_datetime(data['Min_Date']).dt.date
            self.logger.info(f"📅 Using Min_Date as primary Date column for operative data")
            
        # Limpiar otros nombres de columnas comunes
        column_mapping = {
            'Date_Master[Date]': 'Date',
            'Company_Master[Company': 'Company',
            'Cabin_Master[Cabin_Show': 'Cabin',
            'Haul_Master[Haul_Aggr': 'Haul'
        }
        
        for old_col, new_col in column_mapping.items():
            if old_col in data.columns:
                data.rename(columns={old_col: new_col}, inplace=True)
        
        return data


class OperationalDataAnalyzer:
    """
    Analizador especializado para datos operativos con soporte para múltiples modos de comparación
    Diseñado específicamente para el análisis de métricas operativas en contexto de anomalías NPS
    """

    def __init__(self, comparison_mode: str = "mean"):
        """
        Inicializa el analizador operativo

        Args:
            comparison_mode: Modo de comparación - "mean", "vslast", "target"
        """
        self.comparison_mode = comparison_mode
        self.operative_data = {}  # Almacena datos operativos por nodo
        self.logger = logging.getLogger(__name__)
        
        self.logger.info(f"OperationalDataAnalyzer initialized with comparison_mode: {comparison_mode}")

    def _clean_dax_columns(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Clean DAX column names and convert to standard format.
        Similar to pbi_collector.py logic.
        """
        # Limpiar nombres de columnas DAX
        if 'Date_Master[Date' in data.columns:
            data.rename(columns={'Date_Master[Date': 'Date_Master'}, inplace=True)
        
        # Convertir Date_Master a Date para compatibilidad
        if 'Date_Master' in data.columns:
            data['Date'] = pd.to_datetime(data['Date_Master']).dt.date
        elif 'Date_Master[Date]' in data.columns:
            data['Date'] = pd.to_datetime(data['Date_Master[Date]']).dt.date
        
        # Para datos operativos flexibles, usar Min_Date como Date principal
        elif 'Min_Date' in data.columns:
            data['Date'] = pd.to_datetime(data['Min_Date']).dt.date
            self.logger.info(f"📅 Using Min_Date as primary Date column for operative data")
            
        # Limpiar otros nombres de columnas comunes
        column_mapping = {
            'Date_Master[Date]': 'Date',
            'Company_Master[Company': 'Company',
            'Cabin_Master[Cabin_Show': 'Cabin',
            'Haul_Master[Haul_Aggr': 'Haul'
        }
        
        for old_col, new_col in column_mapping.items():
            if old_col in data.columns:
                data.rename(columns={old_col: new_col}, inplace=True)
        
        return data

    def analyze_operative_metrics(self, node_path: str, target_date: str) -> Dict[str, Any]:
        """
        Analiza métricas operativas para un nodo y fecha específicos

        Args:
            node_path: Ruta del nodo en el árbol jerárquico
            target_date: Fecha objetivo para el análisis (YYYY-MM-DD)

        Returns:
            Dict con análisis de métricas operativas
        """
        try:
            if node_path not in self.operative_data:
                return {"error": f"No operative data available for {node_path}"}

            data = self.operative_data[node_path]
            if data.empty:
                return {"error": f"Empty operative data for {node_path}"}

            # Limpiar columnas DAX y asegurar formato correcto
            data = self._clean_dax_columns(data)

            # Convertir target_date a datetime para comparaciones
            try:
                target_dt = pd.to_datetime(target_date)
            except:
                return {"error": f"Invalid target_date format: {target_date}"}

            # Asegurar que la columna de fecha esté en formato datetime
            if 'Date' in data.columns:
                data['Date'] = pd.to_datetime(data['Date'])
            else:
                return {"error": "No 'Date' column found in operative data"}

            # Análisis según el modo de comparación
            if self.comparison_mode == "vslast":
                return self._analyze_vslast(data, target_dt, node_path)
            elif self.comparison_mode == "mean":
                return self._analyze_mean(data, target_dt, node_path)
            elif self.comparison_mode == "target":
                return self._analyze_target(data, target_dt, node_path)
            else:
                return {"error": f"Unsupported comparison_mode: {self.comparison_mode}"}

        except Exception as e:
            self.logger.error(f"Error analyzing operative metrics: {e}")
            return {"error": str(e)}

    def get_specific_explanations(self, node_path: str, target_date: str, anomaly_type: str, aggregation_days: int = 7) -> Dict[str, str]:
        """
        Obtiene explicaciones específicas basadas en el tipo de anomalía
        Adaptado para datos agregados por período
        
        Returns:
            Dict con claves 'otp_explanation', 'load_factor_explanation', 'mishandling_explanation'

        Args:
            node_path: Ruta del nodo
            target_date: Fecha objetivo
            anomaly_type: Tipo de anomalía ('positive', 'negative', 'unknown')
            aggregation_days: Días de agregación para el análisis

        Returns:
            Diccionario con explicaciones específicas por métrica
        """
        try:
            result = {
                'otp_explanation': "No OTP data available",
                'load_factor_explanation': "No Load Factor data available", 
                'mishandling_explanation': "No Mishandling data available",
                'misconex_explanation': "No Misconex data available"
            }

            if node_path not in self.operative_data:
                return result

            data = self.operative_data[node_path]
            if data.empty:
                return result

            # Limpiar columnas DAX y asegurar formato correcto
            data = self._clean_dax_columns(data)
            target_dt = pd.to_datetime(target_date)

            # Para datos agregados por período, buscar el período que contiene la fecha objetivo
            target_row = None
            
            if 'Period_Group' in data.columns and 'Min_Date' in data.columns and 'Max_Date' in data.columns:
                # Convertir Min_Date y Max_Date a datetime para comparación
                data['Min_Date'] = pd.to_datetime(data['Min_Date'])
                data['Max_Date'] = pd.to_datetime(data['Max_Date'])
                
                # Encontrar el período que contiene la fecha objetivo
                target_period = data[
                    (data['Min_Date'] <= target_dt) & 
                    (data['Max_Date'] >= target_dt)
                ]
                
                if target_period.empty:
                    # Si no hay período exacto, buscar el más cercano
                    data['distance'] = abs((data['Min_Date'] + (data['Max_Date'] - data['Min_Date'])/2) - target_dt).dt.days
                    target_period = data.loc[data['distance'].idxmin():data['distance'].idxmin()]
                    self.logger.info(f"📅 No exact period found, using closest period for {target_dt.date()}")
                
                target_row = target_period.iloc[0]
                
            else:
                # Lógica original para datos por fecha exacta
                if 'Date' not in data.columns:
                    return result
                
                target_data = data[data['Date'] == target_dt]
                
                if target_data.empty:
                    return result
                
                target_row = target_data.iloc[0]

            # Obtener análisis completo para contexto de cambios
            full_analysis = self.analyze_operative_metrics(node_path, target_date)
            metrics_context = full_analysis.get('metrics', {}) if 'error' not in full_analysis else {}

            # Análisis específico por métrica con contexto de cambios
            load_factor_explanation = self._explain_load_factor(target_row, anomaly_type, metrics_context.get('Load_Factor', {}))
            if load_factor_explanation:
                result['load_factor_explanation'] = load_factor_explanation

            otp_explanation = self._explain_otp(target_row, anomaly_type, metrics_context.get('OTP15_adjusted', {}))
            if otp_explanation:
                result['otp_explanation'] = otp_explanation

            mishandling_explanation = self._explain_mishandling(target_row, anomaly_type, metrics_context.get('Mishandling', {}))
            if mishandling_explanation:
                result['mishandling_explanation'] = mishandling_explanation

            misconex_explanation = self._explain_misconex(target_row, anomaly_type, metrics_context.get('Misconex', {}))
            if misconex_explanation:
                result['misconex_explanation'] = misconex_explanation

            return result

        except Exception as e:
            self.logger.error(f"Error getting specific explanations: {e}")
            return {
                'otp_explanation': f"Error analyzing OTP: {str(e)}",
                'load_factor_explanation': f"Error analyzing Load Factor: {str(e)}",
                'mishandling_explanation': f"Error analyzing Mishandling: {str(e)}",
                'misconex_explanation': f"Error analyzing Misconex: {str(e)}"
            }

    def _analyze_vslast(self, data: pd.DataFrame, target_dt: pd.Timestamp, node_path: str) -> Dict[str, Any]:
        """Análisis vs período anterior - Adaptado para datos agregados por período"""
        try:
            # Para datos agregados por período, necesitamos encontrar el período que contiene la fecha objetivo
            if 'Period_Group' in data.columns and 'Min_Date' in data.columns and 'Max_Date' in data.columns:
                # Convertir Min_Date y Max_Date a datetime para comparación
                data['Min_Date'] = pd.to_datetime(data['Min_Date'])
                data['Max_Date'] = pd.to_datetime(data['Max_Date'])
                
                # Encontrar el período que contiene la fecha objetivo
                current_period = data[
                    (data['Min_Date'] <= target_dt) & 
                    (data['Max_Date'] >= target_dt)
                ]
                
                if current_period.empty:
                    # Si no hay período exacto, buscar el más cercano
                    data['distance'] = abs((data['Min_Date'] + (data['Max_Date'] - data['Min_Date'])/2) - target_dt).dt.days
                    current_period = data.loc[data['distance'].idxmin():data['distance'].idxmin()]
                    self.logger.info(f"📅 No exact period found, using closest period for {target_dt.date()}")
                
                current_row = current_period.iloc[0]
                
                # Buscar período anterior (Period_Group mayor = más reciente, menor = más anterior)
                current_period_group = current_row['Period_Group']
                previous_period = data[data['Period_Group'] > current_period_group].sort_values('Period_Group', ascending=True)
                
                if previous_period.empty:
                    return {"error": "No previous period available for comparison"}
                
                previous_row = previous_period.iloc[0]
                
                self.logger.info(f"📊 Comparing Period {current_period_group} vs Period {previous_row['Period_Group']}")
                
            else:
                # Lógica original para datos por fecha exacta
                current_data = data[data['Date'] == target_dt]
                
                if current_data.empty:
                    return {"error": f"No data for target date {target_dt.date()}"}
                
                current_row = current_data.iloc[0]
                
                # Obtener período anterior (día anterior con datos)
                previous_data = data[data['Date'] < target_dt].sort_values('Date', ascending=False)
                
                if previous_data.empty:
                    return {"error": "No previous data available for comparison"}
                
                previous_row = previous_data.iloc[0]

            # Calcular diferencias (misma lógica para ambos casos)
            metrics = {}
            for col in ['Load_Factor', 'OTP15_adjusted', 'Mishandling', 'Misconex']:
                if col in data.columns:
                    current_val = pd.to_numeric(current_row.get(col), errors='coerce')
                    previous_val = pd.to_numeric(previous_row.get(col), errors='coerce')

                    if pd.notna(current_val) and pd.notna(previous_val):
                        difference = current_val - previous_val
                        change_pct = round((difference / previous_val) * 100, 1) if previous_val != 0 else 0
                        
                        # Determinar dirección y significancia
                        direction = 'higher' if difference > 0 else 'lower'
                        is_significant = abs(change_pct) > 5  # Cambio > 5% es significativo
                        
                        metrics[col] = {
                            'current': round(current_val, 2),
                            'previous': round(previous_val, 2),
                            'difference': round(difference, 2),
                            'change_pct': change_pct,
                            # Claves que espera el causal agent
                            'current_value': round(current_val, 2),
                            'previous_value': round(previous_val, 2),
                            'day_value': round(current_val, 2),
                            'delta': round(difference, 2),
                            'direction': direction,
                            'is_significant': is_significant
                        }

            # Determinar fecha de referencia para el resultado
            if 'Period_Group' in data.columns:
                target_date_str = current_row.get('Min_Date', target_dt).strftime('%Y-%m-%d') if hasattr(current_row.get('Min_Date', target_dt), 'strftime') else str(current_row.get('Min_Date', target_dt))[:10]
                previous_date_str = previous_row.get('Min_Date', '').strftime('%Y-%m-%d') if hasattr(previous_row.get('Min_Date', ''), 'strftime') else str(previous_row.get('Min_Date', ''))[:10]
            else:
                target_date_str = target_dt.date().isoformat()
                previous_date_str = previous_row['Date'].date().isoformat()

            return {
                'mode': 'vslast',
                'target_date': target_date_str,
                'previous_date': previous_date_str,
                'metrics': metrics,
                'summary': self._create_vslast_summary(metrics)
            }

        except Exception as e:
            return {"error": f"Error in vslast analysis: {str(e)}"}

    def _analyze_mean(self, data: pd.DataFrame, target_dt: pd.Timestamp, node_path: str) -> Dict[str, Any]:
        """Análisis vs media de período - Adaptado para datos agregados por período"""
        try:
            # Para datos agregados por período, necesitamos encontrar el período que contiene la fecha objetivo
            if 'Period_Group' in data.columns and 'Min_Date' in data.columns and 'Max_Date' in data.columns:
                # Convertir Min_Date y Max_Date a datetime para comparación
                data['Min_Date'] = pd.to_datetime(data['Min_Date'])
                data['Max_Date'] = pd.to_datetime(data['Max_Date'])
                
                # Encontrar el período que contiene la fecha objetivo
                current_period = data[
                    (data['Min_Date'] <= target_dt) & 
                    (data['Max_Date'] >= target_dt)
                ]
                
                if current_period.empty:
                    # Si no hay período exacto, buscar el más cercano
                    data['distance'] = abs((data['Min_Date'] + (data['Max_Date'] - data['Min_Date'])/2) - target_dt).dt.days
                    current_period = data.loc[data['distance'].idxmin():data['distance'].idxmin()]
                    self.logger.info(f"📅 No exact period found, using closest period for {target_dt.date()}")
                
                current_row = current_period.iloc[0]
                
                # Para el análisis de media, usar todos los períodos anteriores (Period_Group mayor)
                current_period_group = current_row['Period_Group']
                historical_data = data[data['Period_Group'] > current_period_group]
                
                if historical_data.empty:
                    return {"error": "No historical data available for mean comparison"}
                
                self.logger.info(f"📊 Comparing Period {current_period_group} vs mean of {len(historical_data)} historical periods")
                
            else:
                # Lógica original para datos por fecha exacta
                current_data = data[data['Date'] == target_dt]
                
                if current_data.empty:
                    return {"error": f"No data for target date {target_dt.date()}"}
                
                current_row = current_data.iloc[0]
                
                # Para análisis de media, usar datos históricos
                historical_data = data[data['Date'] < target_dt]
                
                if historical_data.empty:
                    return {"error": "No historical data available for mean comparison"}

            # Calcular métricas vs media histórica (misma lógica para ambos casos)
            metrics = {}
            for col in ['Load_Factor', 'OTP15_adjusted', 'Mishandling', 'Misconex']:
                if col in data.columns:
                    current_val = pd.to_numeric(current_row.get(col), errors='coerce')
                    historical_vals = pd.to_numeric(historical_data[col], errors='coerce').dropna()

                    if pd.notna(current_val) and len(historical_vals) > 0:
                        mean_val = historical_vals.mean()
                        difference = current_val - mean_val
                        change_pct = round((difference / mean_val) * 100, 1) if mean_val != 0 else 0
                        
                        # Determinar dirección y significancia
                        direction = 'higher' if difference > 0 else 'lower'
                        is_significant = abs(change_pct) > 5  # Cambio > 5% es significativo
                        
                        metrics[col] = {
                            'current': round(current_val, 2),
                            'historical_mean': round(mean_val, 2),
                            'difference': round(difference, 2),
                            'change_pct': change_pct,
                            'historical_periods': len(historical_vals),
                            # Claves que espera el causal agent
                            'current_value': round(current_val, 2),
                            'day_value': round(current_val, 2),
                            'week_average': round(mean_val, 2),
                            'delta': round(difference, 2),
                            'direction': direction,
                            'is_significant': is_significant
                        }

            # Determinar fecha de referencia para el resultado
            if 'Period_Group' in data.columns:
                target_date_str = current_row.get('Min_Date', target_dt).strftime('%Y-%m-%d') if hasattr(current_row.get('Min_Date', target_dt), 'strftime') else str(current_row.get('Min_Date', target_dt))[:10]
            else:
                target_date_str = target_dt.date().isoformat()

            return {
                'mode': 'mean',
                'target_date': target_date_str,
                'metrics': metrics,
                'summary': self._create_mean_summary(metrics)
            }

        except Exception as e:
            return {"error": f"Error in mean analysis: {str(e)}"}

    def _analyze_target(self, data: pd.DataFrame, target_dt: pd.Timestamp, node_path: str) -> Dict[str, Any]:
        """Análisis vs targets predefinidos"""
        try:
            # Targets por defecto (estos podrían venir de configuración)
            targets = {
                'Load_Factor': 85.0,
                'OTP15_adjusted': 90.0,
                'Mishandling': 0.5,
                'Misconex': 0.3
            }

            current_data = data[data['Date'] == target_dt]

            if current_data.empty:
                return {"error": f"No data for target date {target_dt.date()}"}

            current_row = current_data.iloc[0]

            # Comparar con targets
            metrics = {}
            for col, target_val in targets.items():
                if col in data.columns:
                    current_val = pd.to_numeric(current_row.get(col), errors='coerce')

                    if pd.notna(current_val):
                        difference = current_val - target_val
                        metrics[col] = {
                            'current': round(current_val, 2),
                            'target': target_val,
                            'difference': round(difference, 2),
                            'performance': 'above_target' if difference > 0 else 'below_target' if difference < 0 else 'on_target'
                        }

            return {
                'mode': 'target',
                'target_date': target_dt.date().isoformat(),
                'metrics': metrics,
                'summary': self._create_target_summary(metrics)
            }

        except Exception as e:
            return {"error": f"Error in target analysis: {str(e)}"}

    def _create_vslast_summary(self, metrics: Dict) -> str:
        """Crea resumen para análisis vslast"""
        if not metrics:
            return "No se pudieron calcular comparaciones vs período anterior"

        summary_parts = []
        for metric, data in metrics.items():
            change = data['difference']
            metric_name = self._get_metric_display_name(metric)

            if abs(change) > 0.1:  # Solo mencionar cambios significativos
                direction = "aumentó" if change > 0 else "disminuyó"
                summary_parts.append(f"{metric_name} {direction} {abs(change)}")

        if summary_parts:
            return f"vs período anterior: {', '.join(summary_parts)}"
        else:
            return "Métricas operativas estables vs período anterior"

    def _create_mean_summary(self, metrics: Dict) -> str:
        """Crea resumen para análisis mean"""
        if not metrics:
            return "No se pudieron calcular comparaciones vs media histórica"

        summary_parts = []
        for metric, data in metrics.items():
            change = data['difference']
            metric_name = self._get_metric_display_name(metric)

            if abs(change) > 0.1:
                direction = "superior" if change > 0 else "inferior"
                summary_parts.append(f"{metric_name} {direction} a la media en {abs(change)}")

        if summary_parts:
            return f"vs media semanal: {', '.join(summary_parts)}"
        else:
            return "Métricas operativas en línea con la media histórica"

    def _create_target_summary(self, metrics: Dict) -> str:
        """Crea resumen para análisis target"""
        if not metrics:
            return "No se pudieron comparar vs targets"

        on_target = sum(1 for data in metrics.values() if data['performance'] == 'on_target')
        above_target = sum(1 for data in metrics.values() if data['performance'] == 'above_target')
        below_target = sum(1 for data in metrics.values() if data['performance'] == 'below_target')

        total = len(metrics)
        return f"Performance vs targets: {on_target}/{total} en objetivo, {above_target} superando, {below_target} por debajo"

    def _get_metric_display_name(self, metric: str) -> str:
        """Convierte nombres técnicos a nombres de display"""
        display_names = {
            'Load_Factor': 'Load Factor',
            'OTP15_adjusted': 'OTP',
            'Mishandling': 'Mishandling',
            'Misconex': 'Conexiones Perdidas'
        }
        return display_names.get(metric, metric)

    def _explain_load_factor(self, row: pd.Series, anomaly_type: str, metrics_context: dict = None) -> Optional[str]:
        """Genera explicación específica para Load Factor"""
        try:
            lf = pd.to_numeric(row.get('Load_Factor'), errors='coerce')
            if pd.isna(lf):
                return None

            # Construir explicación base
            explanation_parts = []
            
            if lf > 90 and anomaly_type == 'negative':
                explanation_parts.append(f"Load Factor muy alto ({lf}%) puede haber impactado la experiencia del cliente")
            elif lf < 70 and anomaly_type == 'positive':
                explanation_parts.append(f"Load Factor bajo ({lf}%) puede haber mejorado la comodidad del vuelo")
            else:
                explanation_parts.append(f"Load Factor ({lf}%)")

            # Añadir contexto de cambio si está disponible
            if metrics_context and 'previous_value' in metrics_context:
                previous = metrics_context['previous_value']
                difference = metrics_context.get('difference', 0)
                if abs(difference) > 1:  # Solo si hay cambio significativo
                    direction = "aumentó" if difference > 0 else "disminuyó"
                    explanation_parts.append(f"- {direction} {abs(difference):.1f}% vs período anterior ({previous}%)")

            return " ".join(explanation_parts) if explanation_parts else None

        except Exception:
            return None

    def _explain_otp(self, row: pd.Series, anomaly_type: str, metrics_context: dict = None) -> Optional[str]:
        """Genera explicación específica para OTP"""
        try:
            otp = pd.to_numeric(row.get('OTP15_adjusted'), errors='coerce')
            if pd.isna(otp):
                return None

            # Construir explicación base
            explanation_parts = []
            
            if otp < 80 and anomaly_type == 'negative':
                explanation_parts.append(f"Puntualidad baja ({otp:.1f}%) puede haber generado insatisfacción")
            elif otp > 95 and anomaly_type == 'positive':
                explanation_parts.append(f"Excelente puntualidad ({otp:.1f}%) puede haber contribuido a la mejora")
            else:
                explanation_parts.append(f"Puntualidad ({otp:.1f}%)")

            # Añadir contexto de cambio si está disponible
            if metrics_context and 'previous_value' in metrics_context:
                previous = metrics_context['previous_value']
                difference = metrics_context.get('difference', 0)
                if abs(difference) > 0.5:  # Solo si hay cambio significativo
                    direction = "mejoró" if difference > 0 else "empeoró"
                    explanation_parts.append(f"- {direction} {abs(difference):.1f}% vs período anterior ({previous:.1f}%)")

            return " ".join(explanation_parts) if explanation_parts else None

        except Exception:
            return None

    def _explain_mishandling(self, row: pd.Series, anomaly_type: str, metrics_context: dict = None) -> Optional[str]:
        """Genera explicación específica para Mishandling"""
        try:
            mh = pd.to_numeric(row.get('Mishandling'), errors='coerce')
            if pd.isna(mh):
                return None

            # Construir explicación base
            explanation_parts = []
            
            if mh > 1.0 and anomaly_type == 'negative':
                explanation_parts.append(f"Tasa alta de mishandling ({mh:.1f}%) impactó negativamente la experiencia")
            elif mh < 0.3 and anomaly_type == 'positive':
                explanation_parts.append(f"Baja tasa de mishandling ({mh:.1f}%) contribuyó a la mejora del servicio")
            else:
                explanation_parts.append(f"Mishandling ({mh:.1f}%)")

            # Añadir contexto de cambio si está disponible
            if metrics_context and 'previous_value' in metrics_context:
                previous = metrics_context['previous_value']
                difference = metrics_context.get('difference', 0)
                if abs(difference) > 0.1:  # Solo si hay cambio significativo
                    direction = "aumentó" if difference > 0 else "disminuyó"
                    explanation_parts.append(f"- {direction} {abs(difference):.1f}% vs período anterior ({previous:.1f}%)")

            return " ".join(explanation_parts) if explanation_parts else None

        except Exception:
            return None

    def _explain_misconex(self, row: pd.Series, anomaly_type: str, metrics_context: dict = None) -> Optional[str]:
        """Genera explicación específica para Misconex (conexiones perdidas)"""
        try:
            mc = pd.to_numeric(row.get('Misconex'), errors='coerce')
            if pd.isna(mc):
                return None

            # Construir explicación base
            explanation_parts = []
            
            if mc > 0.5 and anomaly_type == 'negative':
                explanation_parts.append(f"Tasa alta de conexiones perdidas ({mc:.1f}%) impactó negativamente la experiencia")
            elif mc < 0.1 and anomaly_type == 'positive':
                explanation_parts.append(f"Baja tasa de conexiones perdidas ({mc:.1f}%) contribuyó a la mejora del servicio")
            else:
                explanation_parts.append(f"Conexiones perdidas ({mc:.1f}%)")

            # Añadir contexto de cambio si está disponible
            if metrics_context and 'previous_value' in metrics_context:
                previous = metrics_context['previous_value']
                difference = metrics_context.get('difference', 0)
                if abs(difference) > 0.1:  # Solo si hay cambio significativo
                    direction = "aumentó" if difference > 0 else "disminuyó"
                    explanation_parts.append(f"- {direction} {abs(difference):.1f}% vs período anterior ({previous:.1f}%)")

            return " ".join(explanation_parts) if explanation_parts else None

        except Exception:
            return None 