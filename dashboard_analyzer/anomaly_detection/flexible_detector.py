"""
Flexible Anomaly Detection System
Supports different temporal aggregation periods (7 days, 14 days, 30 days, etc.)
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from .anomaly_tree import AnomalyTree, AnomalyNode

class FlexibleAnomalyDetector:
    """Enhanced flexible anomaly detector with target-based detection support"""
    
    def __init__(self, aggregation_days: int = 7, threshold: float = 5.0, min_sample_size: int = 5, detection_mode: str = "target", baseline_periods: int = 7):
        """
        Initialize flexible anomaly detector
        
        Args:
            aggregation_days: Number of days to aggregate into each period (default: 7)
            threshold: NPS deviation threshold for anomaly detection (default: 5.0) - used for mean and vslast modes
            min_sample_size: Minimum sample size for analysis (default: 5)
            detection_mode: Anomaly detection mode - "target", "mean", or "vslast" (default: "target")
            baseline_periods: Number of baseline periods for mean-based anomaly detection (default: 7) - only used when detection_mode="mean"
        """
        self.aggregation_days = aggregation_days
        self.threshold = threshold
        self.min_sample_size = min_sample_size
        self.tree: Optional[AnomalyTree] = None
        self.detection_mode = detection_mode
        self.baseline_periods = baseline_periods
        
        # Initialize target-based detector if enabled
        if self.detection_mode == "target":
            from .target_based_detector import TargetBasedAnomalyDetector
            self.target_detector = TargetBasedAnomalyDetector(
                aggregation_days=aggregation_days,
                min_sample_size=min_sample_size
            )
        else:
            self.target_detector = None
        
        # Cache for monthly targets to avoid redundant API calls
        self.monthly_targets_cache = {}
        
    async def analyze_flexible_anomalies(self, data_folder: str, analysis_date=None) -> Tuple[Dict[str, str], Dict[str, float], List[str], Dict[str, Dict[str, float]]]:
        """
        Analyze flexible anomalies for the most recent period
        
        Args:
            data_folder: Path to data folder
            analysis_date: Optional analysis date (defaults to today)
            
        Returns:
            Tuple of (anomalies, deviations, periods, nps_values)
        """
        if analysis_date is None:
            analysis_date = datetime.now()
            
        print(f"🔍 Analyzing flexible anomalies for {analysis_date.strftime('%Y-%m-%d')}")
        print(f"📁 Data folder: {data_folder}")
        print(f"🎯 Detection mode: {self.detection_mode}")
        
        # Load data
        all_data = self._load_flexible_data(data_folder)
        if not all_data:
            print("❌ No data loaded")
            return {}, {}, [], {}
            
        # Get available periods
        periods = self._get_available_periods(all_data)
        if not periods:
            print("❌ No valid periods found")
            return {}, {}, [], {}
            
        print(f"📊 Available periods: {periods}")
        
        # Use the most recent period (period 1)
        latest_period = periods[0] if periods else None
        if latest_period is None:
            print("❌ No valid latest period")
            return {}, {}, [], {}
            
        print(f"🎯 Analyzing period {latest_period}")
        
        # Detect anomalies based on mode
        if self.detection_mode == "target":
            # Use target-based detection
            print(f"🎯 USING TARGET-BASED DETECTION")
            anomalies, deviations = await self._detect_target_based_anomalies(all_data, latest_period, analysis_date)
            nps_values = {}  # Target mode doesn't store NPS values in the same way
        elif self.detection_mode == "mean":
            # Use mean-based detection
            print(f"📈 USING MEAN-BASED DETECTION")
            anomalies, deviations, nps_values = self._detect_legacy_anomalies(all_data, latest_period, periods)
        else:  # vslast
            # Use vslast detection
            print(f"🔄 USING VSLAST DETECTION")
            anomalies, deviations, nps_values = self._detect_vslast_anomalies(all_data, latest_period, periods)
            
        return anomalies, deviations, periods, nps_values
    
    def _load_flexible_data(self, data_folder: str) -> Dict[str, pd.DataFrame]:
        """Load flexible aggregation data for all nodes"""
        data_folder_path = Path(data_folder)
        all_data = {}
        
        # Define node paths mapping: logical_path -> folder_name
        node_mapping = {
            "Global": "Global",
            "Global/LH": "Global_LH", 
            "Global/LH/Economy": "Global_LH_Economy", 
            "Global/LH/Business": "Global_LH_Business", 
            "Global/LH/Premium": "Global_LH_Premium",
            "Global/SH": "Global_SH", 
            "Global/SH/Economy": "Global_SH_Economy", 
            "Global/SH/Business": "Global_SH_Business",
            "Global/SH/Economy/IB": "Global_SH_Economy_IB", 
            "Global/SH/Economy/YW": "Global_SH_Economy_YW",
            "Global/SH/Business/IB": "Global_SH_Business_IB", 
            "Global/SH/Business/YW": "Global_SH_Business_YW"
        }
        
        loaded_count = 0
        for logical_path, folder_name in node_mapping.items():
            node_folder = data_folder_path / folder_name
            flexible_file = node_folder / f'flexible_NPS_{self.aggregation_days}d.csv'
            
            if flexible_file.exists():
                try:
                    df = pd.read_csv(flexible_file)
                    if not df.empty:
                        all_data[logical_path] = df
                        loaded_count += 1
                except Exception as e:
                    print(f"❌ Error loading {logical_path}: {e}")
        
        print(f"📊 Loaded {loaded_count}/{len(node_mapping)} segments")
        return all_data
    
    def _get_available_periods(self, all_data: Dict[str, pd.DataFrame]) -> List[int]:
        """Get list of available periods that have valid NPS data"""
        all_periods = set()
        
        for node_path, df in all_data.items():
            if 'Period_Group' in df.columns:
                # Only include periods that have valid NPS data (2024 or 2025)
                valid_periods = df[
                    (df['NPS_2025'].notna()) | (df['NPS_2024'].notna())
                ]['Period_Group'].unique()
                all_periods.update(valid_periods)
        
        # Sort periods in ascending order (period 1 = most recent)
        return sorted(list(all_periods))
    
    def _detect_legacy_anomalies(self, all_data: Dict[str, pd.DataFrame], 
                                target_period: int, all_periods: List[int]) -> Tuple[Dict[str, str], Dict[str, float], Dict[str, Dict[str, float]]]:
        """Detect anomalies for a specific period using mean of configurable number of periods as baseline"""
        anomalies = {}
        deviations = {}
        nps_values = {}  # Store actual NPS values for display
        
        # Use the n periods immediately after the target period for baseline calculation
        # For Period 1, use Periods 2, 3, 4, 5, 6, 7, 8 (the 7 weeks before the target week)
        baseline_periods = [target_period + i for i in range(1, self.baseline_periods + 1) if (target_period + i) in all_periods]
        
        if len(baseline_periods) < 3:
            print(f"⚠️ Insufficient baseline data for period {target_period} (need at least 3 periods)")
            return anomalies, deviations, nps_values
        
        # Only print baseline info once per period  
        print(f"📈 Period {target_period}: baseline mean of periods {baseline_periods} (last {self.baseline_periods} periods)")
        
        for node_path, df in all_data.items():
            if 'Period_Group' not in df.columns:
                continue
            
            # Get target period data
            target_data = df[df['Period_Group'] == target_period]
            if target_data.empty:
                anomalies[node_path] = "?"
                continue
                
            target_responses = target_data.get('Responses', pd.Series([0])).iloc[0]
            
            # Check minimum sample size
            if target_responses < self.min_sample_size:
                anomalies[node_path] = "S"  # Insufficient sample
                continue
            
            # Strategy: Try NPS_2025 first, fallback to NPS_2024
            target_nps = None
            baseline_avg = None
            
            # Try NPS_2025 for target
            if 'NPS_2025' in df.columns and not pd.isna(target_data['NPS_2025'].iloc[0]):
                target_nps = target_data['NPS_2025'].iloc[0]
                
                # Calculate baseline as mean of specified number of periods using NPS_2025
                baseline_data = df[df['Period_Group'].isin(baseline_periods)]
                baseline_nps_values = baseline_data['NPS_2025'].dropna()
                
                if len(baseline_nps_values) >= 3:
                    baseline_avg = baseline_nps_values.mean()
                else:
                    # Fallback: Use NPS_2024 baseline for periods 23-74 (2024 data)
                    nps_2024_periods = df[(df['Period_Group'] >= 23) & (df['Period_Group'] <= 74)]
                    if len(nps_2024_periods) >= self.baseline_periods:
                        baseline_avg = nps_2024_periods['NPS_2024'].dropna().tail(self.baseline_periods).mean()
            
            # Fallback to NPS_2024 if NPS_2025 not available
            if target_nps is None and 'NPS_2024' in df.columns and not pd.isna(target_data['NPS_2024'].iloc[0]):
                target_nps = target_data['NPS_2024'].iloc[0]
                
                # Calculate baseline as mean of specified number of periods using NPS_2024
                baseline_data = df[df['Period_Group'].isin(baseline_periods)]
                baseline_nps_values = baseline_data['NPS_2024'].dropna()
                
                if len(baseline_nps_values) >= 3:
                    baseline_avg = baseline_nps_values.mean()
            
            # Final fallback to NPS_2019
            if target_nps is None and 'NPS_2019' in df.columns and not pd.isna(target_data['NPS_2019'].iloc[0]):
                target_nps = target_data['NPS_2019'].iloc[0]
                baseline_data = df[df['Period_Group'].isin(baseline_periods)]
                baseline_nps_values = baseline_data['NPS_2019'].dropna()
                
                if len(baseline_nps_values) >= 3:
                    baseline_avg = baseline_nps_values.mean()
            
            # Check if we have valid data
            if target_nps is None or baseline_avg is None:
                anomalies[node_path] = "?"
                continue
            
            deviation = target_nps - baseline_avg
            deviations[node_path] = deviation
            
            # Store NPS values for display
            nps_values[node_path] = {
                'current': target_nps,
                'baseline': baseline_avg,
                'deviation': deviation
            }
            
            # Classify anomaly
            anomalies[node_path] = self._classify_anomaly_new_logic(deviation)
        
        return anomalies, deviations, nps_values
    
    def _detect_vslast_anomalies(self, all_data: Dict[str, pd.DataFrame], 
                                target_period: int, all_periods: List[int]) -> Tuple[Dict[str, str], Dict[str, float], Dict[str, Dict[str, float]]]:
        """Detect anomalies for a specific period using only the previous period as baseline"""
        anomalies = {}
        deviations = {}
        nps_values = {}  # Store actual NPS values for display
        
        # Use only the immediately previous period as baseline
        previous_period = target_period + 1
        
        if previous_period not in all_periods:
            print(f"⚠️ Previous period {previous_period} not available for comparison with period {target_period}")
            return anomalies, deviations, nps_values
        
        # Print baseline info once per period  
        print(f"🔄 Period {target_period}: comparing against previous period {previous_period}")
        
        for node_path, df in all_data.items():
            if 'Period_Group' not in df.columns:
                continue
            
            # Get target period data
            target_data = df[df['Period_Group'] == target_period]
            if target_data.empty:
                anomalies[node_path] = "?"
                continue
                
            target_responses = target_data.get('Responses', pd.Series([0])).iloc[0]
            
            # Check minimum sample size
            if target_responses < self.min_sample_size:
                anomalies[node_path] = "S"  # Insufficient sample
                continue
            
            # Get previous period data
            previous_data = df[df['Period_Group'] == previous_period]
            if previous_data.empty:
                anomalies[node_path] = "?"
                continue
            
            # Strategy: Try NPS_2025 first, fallback to NPS_2024
            target_nps = None
            previous_nps = None
            
            # Try NPS_2025 for both target and previous
            if 'NPS_2025' in df.columns and not pd.isna(target_data['NPS_2025'].iloc[0]):
                target_nps = target_data['NPS_2025'].iloc[0]
                
                if not pd.isna(previous_data['NPS_2025'].iloc[0]):
                    previous_nps = previous_data['NPS_2025'].iloc[0]
                else:
                    # Fallback: use NPS_2024 for previous period if NPS_2025 not available
                    if 'NPS_2024' in df.columns and not pd.isna(previous_data['NPS_2024'].iloc[0]):
                        previous_nps = previous_data['NPS_2024'].iloc[0]
            
            # Fallback to NPS_2024 if NPS_2025 not available for target
            if target_nps is None and 'NPS_2024' in df.columns and not pd.isna(target_data['NPS_2024'].iloc[0]):
                target_nps = target_data['NPS_2024'].iloc[0]
                
                if not pd.isna(previous_data['NPS_2024'].iloc[0]):
                    previous_nps = previous_data['NPS_2024'].iloc[0]
            
            # Final fallback to NPS_2019
            if target_nps is None and 'NPS_2019' in df.columns and not pd.isna(target_data['NPS_2019'].iloc[0]):
                target_nps = target_data['NPS_2019'].iloc[0]
                
                if not pd.isna(previous_data['NPS_2019'].iloc[0]):
                    previous_nps = previous_data['NPS_2019'].iloc[0]
            
            # Check if we have valid data for both periods
            if target_nps is None or previous_nps is None:
                anomalies[node_path] = "?"
                continue
            
            deviation = target_nps - previous_nps
            deviations[node_path] = deviation
            
            # Store NPS values for display
            nps_values[node_path] = {
                'current': target_nps,
                'baseline': previous_nps,
                'deviation': deviation
            }
            
            # Classify anomaly using same threshold as mean-based detection
            anomalies[node_path] = self._classify_anomaly_new_logic(deviation)
        
        return anomalies, deviations, nps_values
    
    async def _detect_target_based_anomalies(self, all_data: Dict[str, pd.DataFrame], 
                                          target_period: int, analysis_date) -> Tuple[Dict[str, str], Dict[str, float]]:
        """Detect anomalies using target-based approach"""
        anomalies = {}
        deviations = {}
        
        print(f"🎯 Using TARGET-BASED anomaly detection for period {target_period}")
        
        # Calculate period dates
        period_start_date, period_end_date = self.target_detector._calculate_period_dates(analysis_date, target_period)
        required_months = self.target_detector._get_required_months(period_start_date, period_end_date)
        
        print(f"📅 Period {target_period}: {period_start_date.strftime('%Y-%m-%d')} to {period_end_date.strftime('%Y-%m-%d')}")
        print(f"📊 Required target months: {required_months}")
        
        # Get monthly targets once per period (cached)
        monthly_targets_for_period = {}
        for month in required_months:
            if month not in self.monthly_targets_cache:
                print(f"🎯 Fetching targets for {month}...")
                # Get targets for first segment (Global) - targets are same for all segments
                try:
                    targets = await self.target_detector.get_monthly_targets("Global", [month])
                    self.monthly_targets_cache[month] = targets.get(month, None)
                except Exception as e:
                    print(f"❌ Failed to get targets for {month}: {e}")
                    self.monthly_targets_cache[month] = None
            
            monthly_targets_for_period[month] = self.monthly_targets_cache[month]
        
        print(f"🎯 Cached targets: {monthly_targets_for_period}")
        
        for node_path, df in all_data.items():
            if 'Period_Group' not in df.columns:
                continue
            
            # Get target period data
            target_data = df[df['Period_Group'] == target_period]
            if target_data.empty:
                anomalies[node_path] = "?"
                continue
                
            target_responses = target_data.get('Responses', pd.Series([0])).iloc[0]
            
            # Check minimum sample size
            if target_responses < self.min_sample_size:
                anomalies[node_path] = "S"  # Insufficient sample
                continue
            
            # Get actual NPS (prefer 2025, fallback to 2024)
            actual_nps = None
            
            if 'NPS_2025' in target_data.columns and not pd.isna(target_data['NPS_2025'].iloc[0]):
                actual_nps = target_data['NPS_2025'].iloc[0]
            elif 'NPS_2024' in target_data.columns and not pd.isna(target_data['NPS_2024'].iloc[0]):
                actual_nps = target_data['NPS_2024'].iloc[0]
            
            if actual_nps is None:
                anomalies[node_path] = "?"
                continue
            
            # Use cached monthly targets
            try:
                # Determine target context using cached targets
                target_context = self.target_detector.determine_target_context(
                    period_start_date, period_end_date, node_path, monthly_targets_for_period
                )
                
                # Classify anomaly vs target
                status, deviation, explanation = self.target_detector.classify_anomaly_vs_target(actual_nps, target_context)
                
                # Convert 'Normal' to 'N' to match legacy format
                if status == 'Normal':
                    status = 'N'
                
                anomalies[node_path] = status
                deviations[node_path] = deviation
                
            except Exception as e:
                print(f"  ❌ Error processing {node_path}: {e}")
                anomalies[node_path] = "?"
                deviations[node_path] = 0.0
        
        return anomalies, deviations
    
    def get_period_summary(self, data_folder: str, periods: List[int]) -> pd.DataFrame:
        """Generate summary table for multiple periods"""
        summary_data = []
        
        for period in periods[:7]:  # Show last 7 periods
            anomalies, _, _ = self.analyze_period(data_folder, period)
            
            positive = sum(1 for a in anomalies.values() if a == "+")
            negative = sum(1 for a in anomalies.values() if a == "-")
            normal = sum(1 for a in anomalies.values() if a == "N")
            total = positive + negative + normal
            
            status = "🚨 Alert" if (positive > 0 or negative > 0) else "✅ Normal"
            
            summary_data.append({
                'Period': f"Period {period}",
                'Status': status,
                '+': positive,
                '-': negative,
                'N': normal,
                'Total': total
            })
        
        return pd.DataFrame(summary_data)
    
    async def analyze_period(self, data_folder: str, target_period: int, analysis_date=None) -> Tuple[Dict[str, str], Dict[str, float], List[str], Dict[str, Dict[str, float]]]:
        """
        Analyze anomalies for a specific period
        
        Args:
            data_folder: Path to data folder
            target_period: Period number to analyze
            analysis_date: Optional analysis date
            
        Returns:
            Tuple of (anomalies, deviations, periods, nps_values)
        """
        if analysis_date is None:
            analysis_date = datetime.now()
            
        print(f"🔍 Analyzing period {target_period} for {analysis_date.strftime('%Y-%m-%d')}")
        print(f"📁 Data folder: {data_folder}")
        print(f"🎯 Detection mode: {self.detection_mode}")
        
        # Load data
        all_data = self._load_flexible_data(data_folder)
        if not all_data:
            print("❌ No data loaded")
            return {}, {}, [], {}
            
        # Get available periods
        periods = self._get_available_periods(all_data)
        if not periods:
            print("❌ No valid periods found")
            return {}, {}, [], {}
            
        print(f"📊 Available periods: {periods}")
        
        if target_period not in periods:
            print(f"❌ Target period {target_period} not found in available periods")
            return {}, {}, periods, {}
            
        # Detect anomalies based on mode
        if self.detection_mode == "target":
            # Use target-based detection
            print(f"🎯 USING TARGET-BASED DETECTION")
            anomalies, deviations = await self._detect_target_based_anomalies(all_data, target_period, analysis_date)
            nps_values = {}  # Target mode doesn't store NPS values in the same way
        elif self.detection_mode == "mean":
            # Use mean-based detection
            print(f"📈 USING MEAN-BASED DETECTION")
            anomalies, deviations, nps_values = self._detect_legacy_anomalies(all_data, target_period, periods)
        else:  # vslast
            # Use vslast detection
            print(f"🔄 USING VSLAST DETECTION")
            anomalies, deviations, nps_values = self._detect_vslast_anomalies(all_data, target_period, periods)
            
        return anomalies, deviations, periods, nps_values 

    def _classify_anomaly_new_logic(self, deviation: float) -> str:
        """
        New anomaly classification logic:
        - Any negative deviation (bajada) -> Study (negative anomaly)
        - Only positive deviations > 7 points -> Study (positive anomaly)
        - Positive deviations ≤ 7 points -> Not studied
        """
        if deviation < 0:
            # Any negative deviation (bajada) is studied
            if deviation < -5:
                return "-"  # Pronounced negative anomaly
            else:
                return "-"  # Negative anomaly (studied but not pronounced)
        elif deviation > 7:
            # Only positive deviations > 7 points are studied
            return "+"  # Positive anomaly
        else:
            # Positive deviations ≤ 7 points are not studied
            return "N"  # No anomaly (not studied) 