from typing import List, Tuple, Dict, Any
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
import asyncio

from .anomaly_interpreter import AnomalyInterpreter
from ..data_collection.pbi_collector import PBIDataCollector
from ..anomaly_explanation.data_analyzer import OperationalDataAnalyzer
from ..anomaly_explanation.routes_analyzer import RoutesAnalyzer

class FlexibleAnomalyInterpreter:
    """
    Interprets anomalies for flexible time periods (7d, 14d, 30d aggregations)
    Handles date range conversion and multi-source data collection
    Supports dual explanation modes: 'raw' (current detailed data) and 'agent' (intelligent causal analysis)
    """
    
    def __init__(self, data_folder: str, pbi_collector: PBIDataCollector = None, drivers_survey_threshold: int = 100, default_comparison_days: int = 7, explanation_mode: str = "agent", silent_mode: bool = False, detection_mode: str = "mean", causal_filter: str = "vs L7d", comparison_start_date: datetime = None, comparison_end_date: datetime = None, study_mode: str = None):
        print(f"         🔍 DEBUG: FlexibleAnomalyInterpreter.__init__ called with causal_filter: '{causal_filter}'")
        self.data_folder = data_folder
        self.pbi_collector = pbi_collector
        self.operational_analyzer = OperationalDataAnalyzer()
        self.routes_analyzer = RoutesAnalyzer(pbi_collector) if pbi_collector else None
        self.drivers_survey_threshold = drivers_survey_threshold  # Minimum surveys for explanatory drivers
        self.default_comparison_days = default_comparison_days  # Default number of days for operational comparison (7, 5, or 15)
        self.explanation_mode = explanation_mode  # "raw" or "agent"
        self.silent_mode = silent_mode
        self.detection_mode = detection_mode  # "vslast", "mean", or "target" - should align with NPS detection mode
        self.causal_filter = causal_filter  # Comparison filter for causal agent
        self.comparison_start_date = comparison_start_date  # Start date for comparison period
        self.comparison_end_date = comparison_end_date  # End date for comparison period
        self.study_mode = study_mode  # Study mode: "single" or "comparative"
        
        # Cache for explanations
        self.explanation_cache: Dict[Tuple[str, int], str] = {}  # (node_path, period) -> explanation
        
        # Initialize agent lazily (will be created when needed with correct causal_filter)
        self.causal_agent = None
        self._agent_initialized = False
        
    def _initialize_causal_agent(self, causal_filter: str = None, comparison_start_date: datetime = None, comparison_end_date: datetime = None, study_mode: str = None):
        """Initialize the causal agent with the correct filter"""
        if self.explanation_mode == "agent" and not self._agent_initialized:
            try:
                from ..anomaly_explanation.genai_core.agents.causal_explanation_agent import CausalExplanationAgent
                from ..anomaly_explanation.genai_core.utils.enums import LLMType, get_default_llm_type
                
                # Use the provided causal_filter or fall back to instance variable
                agent_causal_filter = causal_filter if causal_filter else self.causal_filter
                agent_comparison_start_date = comparison_start_date if comparison_start_date else self.comparison_start_date
                agent_comparison_end_date = comparison_end_date if comparison_end_date else self.comparison_end_date
                
                # Use the study_mode passed from main.py, or determine based on causal_filter as fallback
                if study_mode:
                    agent_study_mode = study_mode
                elif agent_causal_filter is None:
                    agent_study_mode = "single"
                else:
                    agent_study_mode = "comparative"
                
                self.causal_agent = CausalExplanationAgent(
                    llm_type=get_default_llm_type(), 
                    silent_mode=self.silent_mode, 
                    detection_mode=self.detection_mode, 
                    causal_filter=agent_causal_filter, 
                    comparison_start_date=agent_comparison_start_date, 
                    comparison_end_date=agent_comparison_end_date,
                    study_mode=agent_study_mode
                )
                self._agent_initialized = True
                if not self.silent_mode:
                    print(f"🤖 Causal Explanation Agent initialized with filter: {agent_causal_filter}")
            except ImportError as e:
                print(f"⚠️  Agent mode requested but failed to initialize: {e}")
                print("🔄 Falling back to raw mode")
                self.explanation_mode = "raw"
        
    async def explain_anomaly(self, node_path: str, target_period: int, aggregation_days: int, 
                            anomaly_state: str = None, start_date: datetime = None, end_date: datetime = None, anomaly_magnitude: float = None, nps_context: str = "", causal_filter: str = "vs L7d", comparison_start_date: datetime = None, comparison_end_date: datetime = None) -> str:
        """
        Generate comprehensive explanation for an anomaly in a flexible time period
        
        Args:
            node_path: Path to the node (e.g., "Global/LH/Business")
            target_period: Period number (1 = most recent)
            aggregation_days: Number of days per period (7, 14, 30, etc.)
            anomaly_state: The anomaly state ("+", "-", "N", etc.)
            start_date: Optional direct start date (bypasses period mapping)
            end_date: Optional direct end date (bypasses period mapping)
            anomaly_magnitude: Optional magnitude of the anomaly in NPS points
            
        Returns:
            Comprehensive explanation string (raw data or intelligent agent analysis)
        """
        print(f"         🔍 DEBUG: explain_anomaly method called with node_path: {node_path}, causal_filter: '{causal_filter}'")
        # Check cache first (only for raw mode, agent mode is dynamic)
        cache_key = (node_path, target_period)
        if self.explanation_mode == "raw" and cache_key in self.explanation_cache:
            return self.explanation_cache[cache_key]
        
        # Update instance variables with the passed parameters
        print(f"         🔍 DEBUG: explain_anomaly called with causal_filter: '{causal_filter}'")
        
        # Always reset the causal agent to ensure clean state for each analysis
        if hasattr(self, 'causal_agent') and self.causal_agent:
            print(f"         🔄 Resetting causal agent for clean analysis of segment: {node_path}")
            self.causal_agent.reset()
        
        if causal_filter:
            self.causal_filter = causal_filter
        if comparison_start_date:
            self.comparison_start_date = comparison_start_date
        if comparison_end_date:
            self.comparison_end_date = comparison_end_date
        
        # Initialize or update the causal agent with the correct filter
        if self.explanation_mode == "agent":
            if not self._agent_initialized:
                print(f"         🔍 DEBUG: Initializing causal agent with causal_filter: '{causal_filter}'")
                # Use the study_mode from the instance if available, otherwise determine from causal_filter
                if hasattr(self, 'study_mode') and self.study_mode:
                    study_mode = self.study_mode
                else:
                    study_mode = "single" if causal_filter is None else "comparative"
                self._initialize_causal_agent(causal_filter, comparison_start_date, comparison_end_date, study_mode)
            elif self.causal_agent and causal_filter and self.causal_agent.causal_filter != causal_filter:
                print(f"         🔍 DEBUG: Recreating causal agent - filter changed from '{self.causal_agent.causal_filter}' to '{causal_filter}'")
                # Recreate the agent with the correct filter
                self._agent_initialized = False
                study_mode = "single" if causal_filter is None else "comparative"
                self._initialize_causal_agent(causal_filter, comparison_start_date, comparison_end_date, study_mode)
            elif self.causal_agent and causal_filter:
                print(f"         🔍 DEBUG: Updating causal agent filter from '{self.causal_agent.causal_filter}' to '{causal_filter}'")
                self.causal_agent.causal_filter = causal_filter
                self.causal_agent.comparison_start_date = comparison_start_date
                self.causal_agent.comparison_end_date = comparison_end_date
                # Update study_mode based on causal_filter (but respect the original study_mode if it was set)
                if not hasattr(self.causal_agent, 'study_mode') or self.causal_agent.study_mode is None:
                    self.causal_agent.study_mode = "single" if causal_filter is None else "comparative"
        
        try:
            # 1. Get the date range - use direct dates if provided, otherwise map period
            if start_date and end_date:
                print(f"         📅 Using direct date range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
                date_range = (start_date, end_date)
            else:
                print(f"         🔍 Mapping period {target_period} to date range...")
                date_range = self._get_period_date_range(target_period, aggregation_days)
                if not date_range:
                    return "Could not determine date range for this period"
                print(f"         📅 Mapped to: {date_range[0].strftime('%Y-%m-%d')} to {date_range[1].strftime('%Y-%m-%d')}")
            
            start_date, end_date = date_range
            
            # 2. Determine anomaly type for analysis
            anomaly_type = "unknown"
            if anomaly_state == "+":
                anomaly_type = "positive"
            elif anomaly_state == "-":
                anomaly_type = "negative"
            
            # 3. Choose explanation method based on mode
            if self.explanation_mode == "agent" and self.causal_agent:
                # Agent mode: Use intelligent causal analysis
                print(f"         🤖 Running agent-based causal investigation...")
                
                # For daily periods (aggregation_days = 1), report data availability but proceed with investigation
                if aggregation_days == 1:
                    # Quick data availability check for daily periods
                    try:
                        if self.pbi_collector:
                            verbatims_data = self.pbi_collector.collect_verbatims_for_date_range(
                                node_path, start_date, end_date
                            )
                            survey_count = len(verbatims_data) if not verbatims_data.empty else 0
                            
                            if survey_count < 5:  # Low survey count
                                print(f"         ⚠️ Daily period has low survey data ({survey_count} surveys), proceeding with agent investigation using other tools")
                            else:
                                print(f"         ✅ Daily period has sufficient survey data ({survey_count} surveys)")
                    except Exception as e:
                        print(f"         ⚠️ Could not check data availability: {str(e)[:50]}")
                        # Continue with agent investigation anyway
                
                # Calculate final magnitude
                final_magnitude = anomaly_magnitude if anomaly_magnitude is not None else 0.0
                
                explanation = await self.causal_agent.investigate_anomaly(
                    node_path=node_path,
                    start_date=start_date.strftime('%Y-%m-%d'),
                    end_date=end_date.strftime('%Y-%m-%d'),
                    anomaly_type=anomaly_type,
                    anomaly_magnitude=final_magnitude,
                    nps_context=nps_context,  # Pass the NPS context from main.py
                    causal_filter=causal_filter,
                    comparison_start_date=comparison_start_date,
                    comparison_end_date=comparison_end_date
                )
                
                # Add header to distinguish agent explanations
                explanation = f"🤖 **AGENT CAUSAL ANALYSIS**\n{explanation}"
                
            else:
                # Raw mode: Use detailed data collection (current behavior)
                print(f"         📊 Running raw data collection analysis...")
                
                # 3. Collect operational data for the date range
                operational_explanation = await self._analyze_operational_data(
                    node_path, start_date, end_date, aggregation_days, anomaly_type
                )
                
                # 4. Collect verbatims for the date range
                verbatims_explanation = await self._analyze_verbatims_data(
                    node_path, start_date, end_date
                )
                
                # 5. Collect routes data for the date range with anomaly type
                routes_explanation = await self._analyze_routes_data(
                    node_path, start_date, end_date, anomaly_type
                )
                
                # 6. Collect explanatory drivers data for the date range
                drivers_explanation = await self._analyze_explanatory_drivers_data(
                    node_path, start_date, end_date, anomaly_type
                )
                
                # 7. Combine all explanations
                explanation = self._combine_explanations(
                    node_path, target_period, aggregation_days,
                    operational_explanation, verbatims_explanation, routes_explanation, drivers_explanation
                )
            
            # Cache the result (only for raw mode)
            if self.explanation_mode == "raw":
                self.explanation_cache[cache_key] = explanation
            
            return explanation
            
        except Exception as e:
            error_msg = f"Error generating explanation for {node_path} period {target_period}: {str(e)}"
            print(f"❌ {error_msg}")
            return error_msg
    
    def _get_period_date_range(self, target_period: int, aggregation_days: int) -> Tuple[datetime, datetime]:
        """
        Get the start and end dates for a specific period
        
        Args:
            target_period: Period number (1 = most recent)
            aggregation_days: Days per period
            
        Returns:
            Tuple of (start_date, end_date)
        """
        try:
            # Load one of the CSV files to get the period mapping
            data_folder_path = Path(self.data_folder)
            
            # Try different possible paths for the flexible NPS file
            possible_paths = [
                data_folder_path / "Global" / f'flexible_NPS_{aggregation_days}d.csv',
                data_folder_path / "Global_LH" / f'flexible_NPS_{aggregation_days}d.csv',
                data_folder_path / "Global_SH" / f'flexible_NPS_{aggregation_days}d.csv',
            ]
            
            # Find any existing file from possible paths
            flexible_file = None
            for path in possible_paths:
                if path.exists():
                    flexible_file = path
                    break
            
            if not flexible_file:
                return None
                
            df = pd.read_csv(flexible_file)
            df['Min_Date'] = pd.to_datetime(df['Min_Date'])
            df['Max_Date'] = pd.to_datetime(df['Max_Date'])
            
            # Find the row for our target period
            period_data = df[df['Period_Group'] == target_period]
            if period_data.empty:
                return None
                
            start_date = period_data.iloc[0]['Min_Date']
            end_date = period_data.iloc[0]['Max_Date']
            
            return start_date, end_date
            
        except Exception as e:
            print(f"❌ Error getting date range for period {target_period}: {e}")
            return None
    
    async def _analyze_operational_data(self, node_path: str, start_date: datetime, end_date: datetime, aggregation_days: int, anomaly_type: str = None) -> str:
        """
        Analyze operational data for the date range with comprehensive metrics
        For daily periods (aggregation_days=1), uses enhanced OperationalDataAnalyzer
        """
        try:
            # For daily analysis (1 day aggregation), use the enhanced OperationalDataAnalyzer
            if aggregation_days == 1:
                # Use the configured comparison days (5, 7, or 15 days as mentioned by user)
                return await self._analyze_daily_operational_data(node_path, start_date, end_date, anomaly_type, self.default_comparison_days)
            
            # For longer periods, align operational analysis with NPS aggregation logic
            # This ensures both NPS and operative use the same time periods for comparison
            
            # Calculate the date range for operational data collection
            # We need both current period and previous period data for vslast comparison
            period_days = aggregation_days
            
            # Current period: start_date to end_date
            current_period_start = start_date
            current_period_end = end_date
            
            # Previous period: same duration, immediately before current period
            previous_period_end = start_date - timedelta(days=1)
            previous_period_start = previous_period_end - timedelta(days=period_days-1)
            
            # Total range needed for data collection
            data_collection_start = previous_period_start
            data_collection_end = current_period_end
            
            print(f"         📊 Operational analysis aligned with {period_days}-day NPS aggregation")
            print(f"         📅 Current period: {current_period_start.strftime('%Y-%m-%d')} to {current_period_end.strftime('%Y-%m-%d')}")
            print(f"         📅 Previous period: {previous_period_start.strftime('%Y-%m-%d')} to {previous_period_end.strftime('%Y-%m-%d')}")
            
            # Use PBI collector to get operational data for the extended range
            if self.pbi_collector:
                # Collect operational data for the extended date range
                total_days_needed = (data_collection_end - data_collection_start).days + 1
                operational_data = await self.pbi_collector.collect_operative_data_for_date(
                    node_path, data_collection_end, total_days_needed
                )
                
                if operational_data.empty:
                    return f"🔧 Operational: No operational data available for {period_days}-day period analysis"
                
                # Clean the operational data
                cleaned_data = operational_data.copy()
                numeric_columns = ['Load_Factor', 'OTP15_adjusted', 'Misconex', 'Mishandling']
                for col in numeric_columns:
                    if col in cleaned_data.columns:
                        cleaned_data[col] = cleaned_data[col].replace('', pd.NA)
                        cleaned_data[col] = pd.to_numeric(cleaned_data[col], errors='coerce')
                
                # Initialize operational analyzer with same mode as NPS detection for consistency
                from ..anomaly_explanation.data_analyzer import OperationalDataAnalyzer
                analyzer = OperationalDataAnalyzer(comparison_mode=self.detection_mode)
                analyzer.operative_data[node_path] = cleaned_data
                
                # Analyze using the end date of current period as target
                target_date_str = current_period_end.strftime('%Y-%m-%d')
                analysis = analyzer.analyze_operative_metrics(node_path, target_date_str)
                
                if "error" in analysis:
                    return f"🔧 Operational: {analysis['error']}"
                
                # Get specific explanations with anomaly context
                specific_explanations = analyzer.get_specific_explanations(
                    node_path, target_date_str, anomaly_type or "unknown"
                )
                
                # Build comprehensive explanation
                operative_parts = []
                
                # Add OTP analysis if available
                if specific_explanations['otp_explanation'] != "No OTP data available":
                    operative_parts.append(f"OTP {specific_explanations['otp_explanation']}")
                
                # Add Load Factor analysis if available
                if specific_explanations['load_factor_explanation'] != "No Load Factor data available":
                    operative_parts.append(f"LF {specific_explanations['load_factor_explanation']}")
                
                # Add other significant metrics
                metrics = analysis.get("metrics", {})
                other_metrics = []
                
                for metric_name, metric_data in metrics.items():
                    if metric_name not in ['OTP15_adjusted', 'Load_Factor'] and metric_data.get('is_significant', False):
                        direction = "↑" if metric_data.get('delta', 0) > 0 else "↓"
                        other_metrics.append(f"{metric_name}{direction}{abs(metric_data.get('delta', 0)):.1f}pts")
                
                if other_metrics:
                    operative_parts.append(f"Other: {', '.join(other_metrics[:2])}")  # Limit to 2 other metrics
                
                if operative_parts:
                    result = f"🔧 Operational: {'; '.join(operative_parts)}"
                    # Add comparison context aligned with NPS
                    result += f" (vs previous {period_days}-day period)"
                    return result
                else:
                    # Fallback when no significant metrics found
                    available_count = len(metrics)
                    if available_count > 0:
                        return f"🔧 Operational: No significant changes in {available_count} metrics vs previous {period_days}-day period"
                    else:
                        return f"🔧 Operational: No operational metrics available for {period_days}-day period analysis"
            
            # Fallback to file-based analysis if PBI collector not available
            # Load operational data for this node from files
            data_folder_path = Path(self.data_folder)
            node_folder = data_folder_path / node_path.replace("/", "_")
            operative_file = node_folder / "daily_operative.csv"
            
            if not operative_file.exists():
                return "🔧 Operational: No operational data file available"
            
            df = pd.read_csv(operative_file)
            if df.empty:
                return "🔧 Operational: Operational data file is empty"
                
            df['Date_Master'] = pd.to_datetime(df['Date_Master'])
            
            # Filter data for both current and previous periods
            current_period_data = df[
                (df['Date_Master'] >= current_period_start.date()) & 
                (df['Date_Master'] <= current_period_end.date())
            ]
            
            previous_period_data = df[
                (df['Date_Master'] >= previous_period_start.date()) & 
                (df['Date_Master'] <= previous_period_end.date())
            ]
            
            if current_period_data.empty:
                return f"🔧 Operational: No data found for current {period_days}-day period"
            
            if previous_period_data.empty:
                return f"🔧 Operational: No data found for previous {period_days}-day period"
            
            explanations = []
            
            # Define metrics with their interpretation direction (aligned with NPS relationship)
            metrics_analysis = {
                'Load_Factor': {'name': 'Load Factor', 'unit': '%', 'good_direction': 'stable'},
                'OTP15_adjusted': {'name': 'On-Time Performance', 'unit': '%', 'good_direction': 'higher'}, 
                'Misconex': {'name': 'Misconnection Rate', 'unit': '%', 'good_direction': 'lower'},
                'Mishandling': {'name': 'Baggage Mishandling', 'unit': 'per 1000', 'good_direction': 'lower'}
            }
            
            significant_changes = []
            
            for metric, config in metrics_analysis.items():
                if metric not in df.columns:
                    continue
                
                # Calculate averages for both periods
                current_avg = current_period_data[metric].mean()
                previous_avg = previous_period_data[metric].mean()
                
                if pd.isna(current_avg) or pd.isna(previous_avg):
                    continue
                
                # Calculate change
                change = current_avg - previous_avg
                pct_change = (change / previous_avg) * 100 if previous_avg != 0 else 0
                
                # Determine significance (align with vslast threshold logic)
                is_significant = abs(change) > 1.0  # Adjust threshold as needed
                
                if is_significant:
                    direction = "↑" if change > 0 else "↓"
                    significant_changes.append(f"{config['name']}{direction}{abs(change):.1f}{config['unit']}")
            
            if significant_changes:
                explanations.append(f"Significant changes: {', '.join(significant_changes[:3])}")  # Top 3 changes
            else:
                explanations.append(f"No significant operational changes")
            
            explanations.append(f"vs previous {period_days}-day period")
            
            return f"🔧 Operational: {'; '.join(explanations)}"
                        
        except Exception as e:
            return f"🔧 Operational: Error in {aggregation_days}-day analysis - {str(e)[:100]}"
    
    async def _analyze_daily_operational_data(self, node_path: str, start_date: datetime, end_date: datetime, anomaly_type: str = None, comparison_days: int = 7) -> str:
        """
        Enhanced daily operational analysis using PBI data collection
        For single-day periods, provides detailed metric-by-metric analysis
        """
        try:
            if not self.pbi_collector:
                return "🔧 Operational: PBI collector not available"
            
            print(f"         🔍 Collecting operational data with {comparison_days}-day comparison")
            
            # For daily analysis, we expect start_date and end_date to be the same day
            target_date = start_date
            
            # Collect operational data directly from PBI with configurable comparison days
            operational_data = await self.pbi_collector.collect_operative_data_for_date(
                node_path, target_date, comparison_days
            )
            
            if operational_data.empty:
                return f"🔧 Operational: No operational data available for this date range"
            
            print(f"         ✅ Collected {len(operational_data)} days of operational data")
            
            # Convert to format expected by OperationalDataAnalyzer
            # Save temporarily to a format the analyzer can read
            import tempfile
            import os
            
            # Directly load the data into the analyzer instead of using temp files
            # Clean the operational data first - convert empty strings to NaN for numeric columns
            import pandas as pd
            
            # Clean the operational data by replacing empty strings with NaN for numeric columns
            cleaned_data = operational_data.copy()
            numeric_columns = ['Load_Factor', 'OTP15_adjusted', 'Misconex', 'Mishandling']
            for col in numeric_columns:
                if col in cleaned_data.columns:
                    # Replace empty strings with NaN, then convert to numeric
                    cleaned_data[col] = cleaned_data[col].replace('', pd.NA)
                    cleaned_data[col] = pd.to_numeric(cleaned_data[col], errors='coerce')
            
            # Set the cleaned operational data directly
            self.operational_analyzer.operative_data[node_path] = cleaned_data
            
            # For daily analysis, use the target date
            target_date_str = target_date.strftime('%Y-%m-%d')
            
            # Use the provided anomaly type for better analysis context
            if not anomaly_type:
                anomaly_type = "unknown"
            
            # Get the enhanced specific explanations (OTP and Load Factor)
            specific_explanations = self.operational_analyzer.get_specific_explanations(
                node_path, target_date_str, anomaly_type
            )
            
            # Get the comprehensive analysis
            analysis = self.operational_analyzer.analyze_operative_metrics(node_path, target_date_str)
            
            if "error" in analysis:
                return f"🔧 Operational: {analysis['error']}"
            
            # Build enhanced explanation using the sophisticated logic
            operative_parts = []
            
            # Add OTP analysis if available
            if specific_explanations['otp_explanation'] != "No OTP data available":
                operative_parts.append(f"OTP {specific_explanations['otp_explanation']}")
            
            # Add Load Factor analysis if available
            if specific_explanations['load_factor_explanation'] != "No Load Factor data available":
                operative_parts.append(f"LF {specific_explanations['load_factor_explanation']}")
            
            # Add other significant metrics
            metrics = analysis.get("metrics", {})
            other_metrics = []
            
            for metric_name, metric_data in metrics.items():
                if metric_name not in ['OTP15_adjusted', 'Load_Factor'] and metric_data.get('is_significant', False):
                    direction = "↑" if metric_data['direction'] == 'higher' else "↓"
                    other_metrics.append(f"{metric_name}{direction}{abs(metric_data['delta']):.1f}pts")
            
            if other_metrics:
                operative_parts.append(f"Other: {', '.join(other_metrics[:2])}")  # Limit to 2 other metrics
            
            if operative_parts:
                result = f"🔧 Operational: {'; '.join(operative_parts)}"
                
                # Add comparison days info
                result += f" (vs {comparison_days}-day average)"
                
                return result
            else:
                # Fallback when no significant metrics found
                available_count = len(metrics)
                if available_count > 0:
                    return f"🔧 Operational: No significant changes in {available_count} metrics vs {comparison_days}-day average"
                else:
                    return f"🔧 Operational: No operational metrics available for this date range"
                        
        except Exception as e:
            return f"🔧 Operational: Error in daily analysis - {str(e)[:100]}"
    
    async def _analyze_verbatims_data(self, node_path: str, start_date: datetime, end_date: datetime) -> str:
        """
        Analyze verbatims data for the date range with sentiment and topic analysis
        """
        try:
            if not self.pbi_collector:
                return "💬 Verbatims: PBI collector not available"
            
            print(f"         🔍 Collecting verbatims from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
            
            # Use the new date range collection method - much more efficient!
            try:
                combined_verbatims = self.pbi_collector.collect_verbatims_for_date_range(
                    node_path, start_date, end_date
                )
                
                if combined_verbatims.empty:
                    return f"💬 Verbatims: No customer feedback found for this date range"
                
                total_verbatims = len(combined_verbatims)
                total_days = (end_date - start_date).days + 1
                
            except Exception as e:
                return f"💬 Verbatims: Error collecting data - {str(e)[:100]}"
            
            # Analyze sentiment and topics
            sentiment_analysis = ""
            topic_analysis = ""
            
            if 'verbatims_sentiment[sentiment]' in combined_verbatims.columns:
                sentiment_counts = combined_verbatims['verbatims_sentiment[sentiment]'].value_counts()
                negative_count = sentiment_counts.get('Negative', 0)
                positive_count = sentiment_counts.get('Positive', 0)
                neutral_count = sentiment_counts.get('Neutral', 0)
                
                # Determine dominant sentiment
                if negative_count > positive_count and negative_count > neutral_count:
                    sentiment_analysis = f"predominantly negative ({negative_count}/{total_verbatims})"
                elif positive_count > negative_count and positive_count > neutral_count:
                    sentiment_analysis = f"predominantly positive ({positive_count}/{total_verbatims})"
                else:
                    sentiment_analysis = f"mixed sentiment (P:{positive_count}, N:{negative_count}, Neu:{neutral_count})"
            
            if 'verbatims_sentiment[topic]' in combined_verbatims.columns:
                topic_counts = combined_verbatims['verbatims_sentiment[topic]'].value_counts()
                if not topic_counts.empty:
                    top_topics = topic_counts.head(2)
                    topic_analysis = f"main topics: {', '.join([f'{topic}({count})' for topic, count in top_topics.items()])}"
            
            # Combine analysis
            result = f"💬 Customer feedback: {total_verbatims} verbatims collected ({total_days} day period)"
            if sentiment_analysis:
                result += f", {sentiment_analysis}"
            if topic_analysis:
                result += f", {topic_analysis}"
            
            return result
                
        except Exception as e:
            return f"💬 Verbatims: Error during analysis - {str(e)[:100]}"
    
    async def _analyze_routes_data(self, node_path: str, start_date: datetime, end_date: datetime, anomaly_type: str = None) -> str:
        """
        Analyze routes data for the date range with proper route performance analysis
        """
        try:
            if not self.pbi_collector:
                return "🛣️ Routes: PBI collector not available"
            
            print(f"         🔍 Analyzing route performance from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
            
            # Get the route performance data for the period
            try:
                route_data = await self._collect_routes_data_for_period(node_path, start_date, end_date)
                
                if route_data.empty:
                    return f"🛣️ Routes: No route data found for this period"
                
                # Adjust minimum surveys threshold based on date range
                days_in_range = (end_date - start_date).days + 1
                if days_in_range <= 1:
                    min_surveys_threshold = 3  # Daily analysis - very low threshold
                elif days_in_range <= 7:
                    min_surveys_threshold = 4  # Weekly analysis - low threshold
                else:
                    min_surveys_threshold = 5  # Monthly or longer - normal threshold
                
                # Analyze the route performance with anomaly type and adaptive threshold
                analysis = self._analyze_route_performance(route_data, node_path, anomaly_type, min_surveys_threshold)
                return f"🛣️ Routes: {analysis}"
                
            except Exception as e:
                return f"🛣️ Routes: Error collecting route data - {str(e)[:100]}"
            
        except Exception as e:
            return f"🛣️ Routes: Error during analysis - {str(e)[:100]}"
    
    async def _collect_routes_data_for_period(self, node_path: str, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """
        Collect route data for a specific node and date range with comparison filter
        """
        # Use the PBI collector's method with comparison filter
        df = await self.pbi_collector.collect_routes_for_date_range(
            node_path, start_date, end_date,
            comparison_filter=self.causal_filter,
            comparison_start_date=self.comparison_start_date,
            comparison_end_date=self.comparison_end_date
        )
        
        return df
    

    
    def _analyze_route_performance(self, route_data: pd.DataFrame, node_path: str, anomaly_type: str = None, min_surveys: int = 5) -> str:
        """
        Analyze route performance and identify key insights based on anomaly type
        """
        if route_data.empty:
            return "No routes to analyze"
        
        try:
            # Check available columns
            available_columns = route_data.columns.tolist()
            
            # Find NPS and passenger columns
            nps_col = None
            pax_col = None
            route_col = None
            
            for col in available_columns:
                if col.upper() == 'NPS' or 'nps' in col.lower():
                    nps_col = col
                elif col.upper() == 'PAX' or 'pax' in col.lower() or 'passenger' in col.lower():
                    pax_col = col
                elif 'route' in col.lower() or 'ruta' in col.lower():
                    route_col = col
            
            if not nps_col or not route_col:
                return f"Missing required columns (NPS: {nps_col}, Route: {route_col})"
            
            # Filter routes with enough passengers (using adaptive threshold)
            if pax_col and pax_col in route_data.columns:
                significant_routes = route_data[route_data[pax_col] >= min_surveys].copy()
            else:
                # If no passenger column, assume all routes have enough data
                significant_routes = route_data.copy()
            
            if significant_routes.empty:
                return f"No routes with sufficient survey volume (min {min_surveys} surveys)"
            
            # Calculate overall performance
            total_routes = len(significant_routes)
            avg_nps = significant_routes[nps_col].mean()
            
            # Sort routes by NPS 
            routes_sorted = significant_routes.sort_values(nps_col, ascending=False)
            
            # Build focused analysis based on anomaly type
            analysis_parts = []
            analysis_parts.append(f"{total_routes} routes analyzed (min {min_surveys} surveys), avg NPS: {avg_nps:.1f}")
            
            # For negative anomalies: show worst routes only
            if anomaly_type == "negative" or anomaly_type == "-":
                worst_routes = routes_sorted.tail(3)  # Bottom 3 routes
                
                route_details = []
                for _, route in worst_routes.iterrows():
                    route_name = route[route_col]
                    route_nps = route[nps_col]
                    
                    if pax_col and pax_col in route:
                        route_surveys = route[pax_col]
                        route_details.append(f"{route_name}(NPS:{route_nps:.1f}, surveys:{int(route_surveys)})")
                    else:
                        route_details.append(f"{route_name}(NPS:{route_nps:.1f})")
                
                analysis_parts.append(f"worst routes: {', '.join(reversed(route_details))}")
            
            # For positive anomalies: show best routes only  
            elif anomaly_type == "positive" or anomaly_type == "+":
                best_routes = routes_sorted.head(3)  # Top 3 routes
                
                route_details = []
                for _, route in best_routes.iterrows():
                    route_name = route[route_col]
                    route_nps = route[nps_col]
                    
                    if pax_col and pax_col in route:
                        route_surveys = route[pax_col]
                        route_details.append(f"{route_name}(NPS:{route_nps:.1f}, surveys:{int(route_surveys)})")
                    else:
                        route_details.append(f"{route_name}(NPS:{route_nps:.1f})")
                
                analysis_parts.append(f"best routes: {', '.join(route_details)}")
            
            # If no anomaly type specified, show both (fallback)
            else:
                best_route = routes_sorted.iloc[0] if not routes_sorted.empty else None
                worst_route = routes_sorted.iloc[-1] if not routes_sorted.empty else None
                
                if best_route is not None:
                    analysis_parts.append(f"best: {best_route[route_col]}(NPS:{best_route[nps_col]:.1f})")
                if worst_route is not None:
                    analysis_parts.append(f"worst: {worst_route[route_col]}(NPS:{worst_route[nps_col]:.1f})")
            
            return ", ".join(analysis_parts)
            
        except Exception as e:
            return f"Error analyzing routes: {str(e)[:50]}"
    
    def _analyze_touchpoint_performance(self, route_data: pd.DataFrame) -> str:
        """
        Analyze touchpoint performance across routes
        """
        touchpoint_columns = ['Check_in', 'Lounge', 'Boarding', 'Aircraft_interior', 
                            'Wi-Fi', 'IFE', 'F&B', 'Crew', 'Arrivals', 'Connections', 
                            'Operative', 'NonOperative']
        
        issues = []
        
        for col in touchpoint_columns:
            if col in route_data.columns:
                # Calculate average score for this touchpoint
                avg_score = route_data[col].mean()
                
                # Flag touchpoints with scores below 3.5 (on likely 1-5 scale)
                if pd.notna(avg_score) and avg_score < 3.5:
                    issues.append(f"{col.replace('_', ' ')} ({avg_score:.1f})")
        
        if issues:
            return ", ".join(issues[:3])  # Limit to top 3 issues
        else:
            return ""
    
    def _combine_explanations(self, node_path: str, target_period: int, aggregation_days: int,
                            operational: str, verbatims: str, routes: str, drivers: str) -> str:
        """
        Combine all explanations into a comprehensive summary
        """
        explanation_parts = []
        
        explanation_parts.append(f"Period {target_period} ({aggregation_days}-day aggregation) explanation for {node_path}:")
        
        # Operational factors - always include if we have content (including "No data" messages)
        if operational and "Error" not in operational:
            # Remove the "🔧 Operational: " prefix since we'll add our own "Operational: " prefix
            clean_operational = operational.replace("🔧 Operational: ", "")
            explanation_parts.append(f"Operational: {clean_operational}")
        
        # Customer feedback
        if verbatims and "No " not in verbatims and "Error" not in verbatims:
            explanation_parts.append(f"Customer feedback: {verbatims}")
        
        # Routes - always include if we have content (even if it mentions low survey volume)
        if routes and "Error" not in routes and "not yet implemented" not in routes:
            explanation_parts.append(f"Routes: {routes}")
        
        # Drivers - always include if we have content (even if it mentions insufficient volume)
        if drivers and "Error" not in drivers and "not yet implemented" not in drivers:
            explanation_parts.append(f"Drivers: {drivers}")
        
        # If no explanations found
        if len(explanation_parts) == 1:
            explanation_parts.append("No clear operational or customer feedback explanations found for this anomaly.")
        
        return " | ".join(explanation_parts)
    
    async def _analyze_explanatory_drivers_data(self, node_path: str, start_date: datetime, end_date: datetime, anomaly_type: str = None) -> str:
        """
        Analyze explanatory drivers data for the date range to identify key satisfaction drivers
        Only analyzes if there are enough surveys (minimum threshold)
        """
        try:
            if not self.pbi_collector:
                return "Drivers: PBI collector not available"
            
            print(f"         🔍 Analyzing explanatory drivers from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
            
            # First, check if we have enough survey volume for meaningful driver analysis
            # Adjust threshold based on date range - for daily analysis, use lower threshold
            days_in_range = (end_date - start_date).days + 1
            if days_in_range <= 1:
                # Daily analysis - use much lower threshold
                survey_threshold = 10
            elif days_in_range <= 7:
                # Weekly analysis - moderate threshold
                survey_threshold = 30
            else:
                # Monthly or longer - use full threshold
                survey_threshold = self.drivers_survey_threshold
            
            # Get survey count from verbatims for this period (as a proxy for survey volume)
            try:
                verbatims_data = self.pbi_collector.collect_verbatims_for_date_range(
                    node_path, start_date, end_date
                )
                
                survey_count = len(verbatims_data) if not verbatims_data.empty else 0
                print(f"         📊 Survey count check: {survey_count} surveys (threshold: {survey_threshold} for {days_in_range}-day period)")
                
                if survey_count < survey_threshold:
                    return f"Drivers: Insufficient survey volume ({survey_count} < {survey_threshold}) for meaningful driver analysis"
                
            except Exception as e:
                print(f"         ⚠️ Could not check survey volume: {str(e)[:50]}")
                # Continue with driver analysis anyway if we can't check survey count
            
            # Get the explanatory drivers data for the period
            try:
                print(f"         🔍 DEBUG: Using causal_filter: '{self.causal_filter}'")
                drivers_data = await self.pbi_collector.collect_explanatory_drivers_for_date_range(
                    node_path, start_date, end_date,
                    comparison_filter=self.causal_filter,
                    comparison_start_date=self.comparison_start_date,
                    comparison_end_date=self.comparison_end_date
                )
                
                if drivers_data.empty:
                    return f"Drivers: No explanatory drivers data found for this period"
                
                # Analyze the drivers data
                analysis = self._analyze_drivers_performance(drivers_data, anomaly_type)
                return f"Drivers: {analysis}"
                
            except Exception as e:
                return f"Drivers: Error collecting drivers data - {str(e)[:100]}"
            
        except Exception as e:
            return f"Drivers: Error during analysis - {str(e)[:100]}"
    
    def _analyze_drivers_performance(self, drivers_data: pd.DataFrame, anomaly_type: str = None) -> str:
        """
        Analyze explanatory drivers to identify touchpoints with significant impact on NPS
        Uses SHAP values to determine individual touchpoint contributions
        """
        if drivers_data.empty:
            return "No drivers data to analyze"
        
        try:
            # Check available columns from the Exp. Drivers query
            available_columns = drivers_data.columns.tolist()
            print(f"         🔍 Available columns: {available_columns}")
            
            # Handle the actual column names (with potential formatting issues)
            touchpoint_col = None
            satisfaction_diff_col = 'Satisfaction diff'
            shap_diff_col = 'Shapdiff'
            nps_diff_col = 'NPS diff'
            
            # Find the touchpoint column (it might have formatting issues)
            for col in available_columns:
                if 'TouchPoint_Master' in col and 'filtered_name' in col:
                    touchpoint_col = col
                    break
            
            if not touchpoint_col:
                return f"Missing TouchPoint column. Available: {available_columns}"
            
            # Verify we have the required columns for SHAP analysis
            required_cols = [touchpoint_col, shap_diff_col, satisfaction_diff_col]
            missing_cols = [col for col in required_cols if col not in available_columns]
            
            if missing_cols:
                return f"Missing required columns: {missing_cols}"
            
            # Clean the data
            clean_data = drivers_data.copy()
            
            # Convert SHAP and satisfaction diff to numeric (they might be stored as objects)
            clean_data[shap_diff_col] = pd.to_numeric(clean_data[shap_diff_col], errors='coerce')
            clean_data[satisfaction_diff_col] = pd.to_numeric(clean_data[satisfaction_diff_col], errors='coerce')
            
            # Get the total NPS change for the period
            total_nps_change = clean_data[nps_diff_col].iloc[0] if nps_diff_col in clean_data.columns else 0
            
            # Filter out NPS-related touchpoints (we just want to report the change, not analyze them as drivers)
            nps_exclusions = ['NPS', 'NPS Comparative', 'NPS comparison', 'Overall satisfaction']
            operational_data = clean_data[~clean_data[touchpoint_col].isin(nps_exclusions)].copy()
            
            # Filter out rows with null values in key columns
            operational_data = operational_data.dropna(subset=[touchpoint_col, shap_diff_col, satisfaction_diff_col])
            
            if operational_data.empty:
                return f"NPS change: {total_nps_change:+.1f} points, no operational drivers available"
            
            # Define significance threshold for SHAP values (absolute impact)
            # Use a smaller threshold since we're looking at individual touchpoint contributions
            shap_threshold = 0.1  # Minimum absolute SHAP value to be considered significant
            
            # Filter for significant SHAP impacts
            significant_drivers = operational_data[abs(operational_data[shap_diff_col]) >= shap_threshold].copy()
            
            if significant_drivers.empty:
                return f"NPS change: {total_nps_change:+.1f} points, no significant touchpoint drivers (threshold: {shap_threshold:.1f})"
            
            # Sort by absolute SHAP value (magnitude of impact)
            significant_drivers['abs_shap'] = abs(significant_drivers[shap_diff_col])
            significant_drivers = significant_drivers.sort_values('abs_shap', ascending=False)
            
            total_significant = len(significant_drivers)
            
            # Build analysis based on anomaly type
            analysis_parts = []
            
            # Always start with the NPS change
            analysis_parts.append(f"NPS change: {total_nps_change:+.1f} points")
            
            # For negative anomalies: focus on negative SHAP contributors
            if anomaly_type == "negative" or anomaly_type == "-":
                negative_drivers = significant_drivers[significant_drivers[shap_diff_col] < 0].head(3)
                
                if not negative_drivers.empty:
                    driver_details = []
                    for _, row in negative_drivers.iterrows():
                        touchpoint = str(row[touchpoint_col])[:15]  # Truncate long names
                        shap_value = row[shap_diff_col]
                        sat_diff = row[satisfaction_diff_col]
                        driver_details.append(f"{touchpoint}(SHAP:{shap_value:.1f}, Sat:{sat_diff:+.1f})")
                    
                    analysis_parts.append(f"key negative drivers: {', '.join(driver_details)}")
                else:
                    analysis_parts.append("no significant negative operational drivers")
            
            # For positive anomalies: focus on positive SHAP contributors
            elif anomaly_type == "positive" or anomaly_type == "+":
                positive_drivers = significant_drivers[significant_drivers[shap_diff_col] > 0].head(3)
                
                if not positive_drivers.empty:
                    driver_details = []
                    for _, row in positive_drivers.iterrows():
                        touchpoint = str(row[touchpoint_col])[:15]  # Truncate long names
                        shap_value = row[shap_diff_col]
                        sat_diff = row[satisfaction_diff_col]
                        driver_details.append(f"{touchpoint}(SHAP:{shap_value:.1f}, Sat:{sat_diff:+.1f})")
                    
                    analysis_parts.append(f"key positive drivers: {', '.join(driver_details)}")
                else:
                    analysis_parts.append("no significant positive operational drivers")
            
            # Fallback: show top significant drivers regardless of direction
            else:
                top_drivers = significant_drivers.head(3)
                driver_details = []
                for _, row in top_drivers.iterrows():
                    touchpoint = str(row[touchpoint_col])[:15]
                    shap_value = row[shap_diff_col]
                    sat_diff = row[satisfaction_diff_col]
                    driver_details.append(f"{touchpoint}(SHAP:{shap_value:+.1f}, Sat:{sat_diff:+.1f})")
                
                analysis_parts.append(f"top drivers: {', '.join(driver_details)}")
            
            # Add summary of significant touchpoints found
            if total_significant > 0:
                analysis_parts.append(f"({total_significant} significant touchpoints)")
            
            return ", ".join(analysis_parts)
            
        except Exception as e:
            return f"Error analyzing drivers: {str(e)[:100]}" 