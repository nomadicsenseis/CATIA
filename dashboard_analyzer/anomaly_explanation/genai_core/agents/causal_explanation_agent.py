"""
Clean Causal Explanation Agent
==============================

A rewritten agent following the clean separated workflow pattern from the notebook.
Key improvements:
- Clean conversation flow: USER -> AI reflection -> USER instruction -> AI tool call
- For reflections, sends only system prompt + previous explanations (not full history)
- Proper handling of OpenAI tool call format
- Sequential tool execution with proper reflection phases
"""

import logging
import asyncio
import yaml
import pandas as pd
import os
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
import json
import time
import re
import traceback

from pydantic import BaseModel, Field

# Core imports
from dashboard_analyzer.anomaly_explanation.genai_core.llms.openai_llm import OpenAiLLM  
from dashboard_analyzer.anomaly_explanation.genai_core.llms.aws_llm import AWSLLM
from dashboard_analyzer.anomaly_explanation.genai_core.utils.enums import LLMType, MessageType, AgentName, get_default_llm_type
from dashboard_analyzer.anomaly_explanation.genai_core.message_history import MessageHistory
from dashboard_analyzer.anomaly_explanation.genai_core.agents.agent import Agent

# Data collection imports
from dashboard_analyzer.data_collection.pbi_collector import PBIDataCollector
from dashboard_analyzer.data_collection.chatbot_verbatims_collector import ChatbotVerbatimsCollector
from dashboard_analyzer.data_collection.ncs_collector import NCSDataCollector

# Additional imports needed for tools
import time
import re
from datetime import datetime
import traceback

class CausalAnalysisResult(BaseModel):
    """Structured output for causal analysis results"""
    primary_cause: str = Field(description="Primary identified cause of the anomaly")
    confidence_level: str = Field(description="Confidence level: High/Medium/Low")
    supporting_evidence: List[str] = Field(description="List of evidence supporting the conclusion")
    next_investigation_step: Optional[str] = Field(description="Next tool/data source to investigate, if needed")
    final_explanation: str = Field(description="Complete causal explanation for the anomaly")


class CleanConversationTracker:
    """Track the clean conversation workflow"""
    
    def __init__(self):
        self.conversation_log = []
        self.iteration_count = 0
        self.previous_explanations = []
        self.identified_routes = []  # Nuevos campos para tracking
        self.last_tool_context = None  # Contexto del último tool ejecutado
        
    def reset_tracker(self):
        """Reset for new investigation"""
        self.conversation_log = []
        self.iteration_count = 0
        self.previous_explanations = []
        self.identified_routes = []
        self.last_tool_context = None
        
    def reset(self):
        """Resets the agent's state for a new analysis run."""
        self.anomaly_type = "unknown"
        self.collected_data = {
            "explanatory_drivers": None,
            "ncs": None,
            "routes": None,
            "customer_profile": None,
            "operative_data": None,
            "verbatims": None
        }
        self.conversation_log = []
        self.iteration_count = 0
        self.previous_explanations = []
        self.identified_routes = []
        self.last_tool_context = None
        
    def reset(self):
        """Resets the agent's state for a new analysis run."""
        self.anomaly_type = "unknown"
        self.collected_data = {
            "explanatory_drivers": None,
            "ncs": None,
            "routes": None,
            "customer_profile": None,
            "operative_data": None,
            "verbatims": None
        }
        self.conversation_log = []
        self.iteration_count = 0
        self.previous_explanations = []
        self.identified_routes = []
        self.last_tool_context = None
        
    def log_message(self, message_type: str, content: str, metadata: Optional[Dict] = None):
        """Log a message in the conversation"""
        self.conversation_log.append({
            'iteration': self.iteration_count,
            'type': message_type,
            'content': content,
            'metadata': metadata or {},
            'timestamp': datetime.now().strftime('%H:%M:%S')
        })
    
    def add_explanation(self, explanation: str):
        """Add an explanation to the clean context"""
        self.previous_explanations.append(explanation)
    
    def get_clean_context(self, system_prompt: str) -> List[Dict]:
        """Get clean context: system prompt + previous explanations only"""
        messages = [{"role": "system", "content": system_prompt}]
        
        for i, explanation in enumerate(self.previous_explanations):
            messages.append({
                "role": "assistant", 
                "content": f"Previous analysis {i+1}: {explanation}"
            })
            
        return messages
    
    def next_iteration(self):
        """Move to next iteration"""
        self.iteration_count += 1

    def set_tool_context(self, tool_name: str, result: str):
        """Set context of last executed tool"""
        self.last_tool_context = {
            'tool_name': tool_name,
            'result': result,
            'iteration': self.iteration_count
        }
        
        # Extract routes if mentioned in NCS or verbatims results
        if tool_name in ['ncs_tool', 'verbatims_tool']:
            routes = self._extract_routes_from_result(result)
            if routes:
                self.identified_routes.extend(routes)
                
    def _extract_routes_from_result(self, result: str) -> List[str]:
        """Extract route identifiers from tool results including Spanish city names"""
        import re
        
        # Common route patterns: XXX-YYY (e.g., MAD-UIO, LAX-MAD)
        route_patterns = [
            r'\b[A-Z]{3}-[A-Z]{3}\b',  # Standard IATA format
            r'from [A-Z]{3} to [A-Z]{3}',  # Narrative format
            r'route [A-Z]{3}-[A-Z]{3}',  # Explicit route mention
        ]
        
        # Spanish city patterns for NCS verbatims
        spanish_city_patterns = [
            r'Madrid-Nueva York',
            r'Madrid-Bogotá',
            r'Madrid-Bogota',  # without accent
            r'Madrid-Montevideo',
            r'Madrid-Santiago',
            r'Madrid-Caracas',
            r'Madrid-Lima',
            r'Madrid-Quito',
            r'Madrid-Buenos Aires',
            r'Madrid-México',
            r'Madrid-Mexico',  # without accent
            r'Barcelona-[\w\s]+',
            r'Bilbao-[\w\s]+',
            r'[\w\s]+-Madrid',  # Routes TO Madrid
            # Generic patterns
            r'ruta Madrid-[\w\s]+',
            r'vuelos? (?:de|desde) Madrid (?:a|hacia) [\w\s]+',
            r'conexión Madrid-[\w\s]+',
        ]
        
        routes = []
        
        # Extract standard IATA routes
        for pattern in route_patterns:
            matches = re.findall(pattern, result, re.IGNORECASE)
            routes.extend(matches)
        
        # Extract Spanish city routes and try to map to IATA
        for pattern in spanish_city_patterns:
            matches = re.findall(pattern, result, re.IGNORECASE)
            for match in matches:
                # Clean up the match
                clean_match = match.replace('ruta ', '').replace('vuelos de ', '').replace('vuelos desde ', '').replace(' a ', '-').replace(' hacia ', '-').replace('conexión ', '')
                routes.append(clean_match)
        
        # Simple city to IATA mapping for common Spanish cities
        city_mapping = {
            'madrid': 'MAD',
            'nueva york': 'JFK',  # or LGA/EWR
            'bogotá': 'BOG',
            'bogota': 'BOG',
            'montevideo': 'MVD',
            'santiago': 'SCL',
            'caracas': 'CCS',
            'lima': 'LIM',
            'quito': 'UIO',
            'buenos aires': 'EZE',  # or AEP
            'méxico': 'MEX',
            'mexico': 'MEX',
            'barcelona': 'BCN',
            'bilbao': 'BIO'
        }
        
        # Try to convert Spanish routes to IATA
        iata_routes = []
        for route in routes:
            if '-' in route:
                origin, destination = route.split('-', 1)
                origin_clean = origin.lower().strip()
                destination_clean = destination.lower().strip()
                
                origin_iata = city_mapping.get(origin_clean, origin.upper())
                destination_iata = city_mapping.get(destination_clean, destination.upper())
                
                # Only add if it looks like a valid route
                if len(origin_iata) <= 4 and len(destination_iata) <= 4:
                    iata_routes.append(f"{origin_iata}-{destination_iata}")
            else:
                iata_routes.append(route.upper())
        
        # Clean and deduplicate
        cleaned_routes = list(set([route.upper().replace('FROM ', '').replace(' TO ', '-').replace('ROUTE ', '') for route in iata_routes]))
        return [route for route in cleaned_routes if route and '-' in route]
        
    def has_identified_routes(self) -> bool:
        """Check if routes have been identified in previous tools"""
        return len(self.identified_routes) > 0
        
    def should_validate_routes_after_tool(self, tool_name: str) -> bool:
        """Determine if routes_tool should be called after this tool"""
        return (tool_name in ['ncs_tool', 'verbatims_tool'] and self.has_identified_routes())


class CausalExplanationAgent:
    """Clean causal explanation agent with separated workflow"""
    
    def __init__(
        self,
        llm_type: Optional[LLMType] = None,
        config_path: str = "dashboard_analyzer/anomaly_explanation/config/prompts/causal_explanation.yaml",
        logger: Optional[logging.Logger] = None,
        silent_mode: bool = False,
        custom_helper_prompts: Optional[Dict[str, Any]] = None,
        detection_mode: str = "mean",
        causal_filter: str = "vs L7d",
        comparison_start_date: datetime = None,
        comparison_end_date: datetime = None,
        study_mode: str = "comparative"
    ):
        # Use default LLM type if none provided
        if llm_type is None:
            llm_type = get_default_llm_type()
        self.llm_type = llm_type
        self.config_path = config_path
        self.logger = logger or self._setup_logger()
        self.silent_mode = silent_mode
        self.detection_mode = detection_mode
        # Handle causal_filter conversion from string 'None' to actual None
        if causal_filter == 'None' or causal_filter == 'none':
            self.causal_filter = None
        else:
            self.causal_filter = causal_filter
        
        self.comparison_start_date = comparison_start_date
        self.comparison_end_date = comparison_end_date
        
        # Debug log the filter value
        self.logger.info(f"🔍 DEBUG CAUSAL_FILTER: Original: {causal_filter}, Processed: {self.causal_filter}")
        self.study_mode = study_mode
        
        # Load configuration
        self.config = self._load_prompt_config(config_path)
        if custom_helper_prompts:
            self._merge_helper_prompts(custom_helper_prompts)
        
        # Initialize data collectors
        self.pbi_collector = PBIDataCollector()
        self.chatbot_collector = self._init_chatbot_collector()
        self.ncs_collector = self._init_ncs_collector()
        
        # Create LLM and agent
        self.llm = self._create_llm(llm_type)
        self.agent = Agent(llm=self.llm, logger=self.logger)
        
        # Initialize tracker
        self.tracker = CleanConversationTracker()
        
        # Current anomaly context
        self.current_anomaly_type = None
        
        # Store data collected during investigation
        self.collected_data = {}
        
        if not self.silent_mode:
            self.logger.info(f"CausalExplanationAgent initialized with {llm_type.value}")
    
    def _setup_logger(self) -> logging.Logger:
        """Setup default logger for the agent."""
        logger = logging.getLogger("causal_explanation")
        logger.setLevel(logging.INFO)  # Restored back to INFO
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _load_prompt_config(self, config_path: str) -> Dict[str, Any]:
        """Load prompt configuration"""
        try:
            full_path = Path(config_path)
            if not full_path.exists():
                full_path = Path("/workspace") / config_path
            
            with open(full_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            self.logger.info(f"Loaded causal explanation configuration from {full_path}")
            return config
            
        except Exception as e:
            self.logger.warning(f"Failed to load config from {config_path}: {e}")
            # Fallback configuration (minimal - should use YAML)
            default_config = {
            'investigation_flow': {
                    'max_iterations': 5,
                    'start_tool': 'explanatory_drivers_tool'
                }
            }
            return default_config
    
    # Removed _create_default_config() method - all configuration now comes from YAML file
    
    def _merge_helper_prompts(self, custom_prompts: Dict[str, Any]):
        """Merge custom helper prompts"""
        if 'helper_prompts' in custom_prompts:
            self.config['helper_prompts'].update(custom_prompts['helper_prompts'])
    
    def _init_chatbot_collector(self):
        """Initialize chatbot collector with simple token management"""
        try:
            # Load token if available
            token = self._load_chatbot_token()
            if token:
                self.logger.info("🔄 Initializing ChatbotVerbatimsCollector with token...")
                return ChatbotVerbatimsCollector(
                    token=token,
                    pbi_collector=self.pbi_collector  # Provide PBI collector as fallback
                )
            else:
                self.logger.info("🔄 No token found - initializing with PBI fallback only...")
                return ChatbotVerbatimsCollector(
                    pbi_collector=self.pbi_collector
                )
                
        except Exception as e:
            self.logger.error(f"Failed to initialize chatbot collector: {e}")
            return None
    
    def _load_chatbot_token(self) -> Optional[str]:
        """Load chatbot token from environment or file"""
        # Try environment variable first
        token = os.getenv("CHATBOT_API_TOKEN")
        if token:
            return token
        
        # Try loading from temp_aws_credentials.env file (primary location)
        try:
            temp_creds_file = "dashboard_analyzer/temp_aws_credentials.env"
            if os.path.exists(temp_creds_file):
                with open(temp_creds_file, 'r') as f:
                    for line in f:
                        if line.startswith('chatbot_jwt_token ='):
                            token = line.split('=', 1)[1].strip().strip('"\'')
                            self.logger.info("✅ Chatbot token loaded from temp_aws_credentials.env")
                            return token
        except Exception as e:
            self.logger.debug(f"Could not load token from temp_aws_credentials.env: {e}")
        
        # Try loading from token file (fallback)
        try:
            token_file_path = os.getenv("CHATBOT_TOKEN_FILE", ".devcontainer/.env")
            if os.path.exists(token_file_path):
                with open(token_file_path, 'r') as f:
                    for line in f:
                        if line.startswith('CHATBOT_API_TOKEN='):
                            token = line.split('=', 1)[1].strip().strip('"\'')
                            self.logger.info("✅ Chatbot token loaded from .env file")
                            return token
        except Exception as e:
            self.logger.debug(f"Could not load token from file: {e}")
        
        self.logger.warning("❌ No chatbot token found in environment variables or files")
        return None
    
    def _init_ncs_collector(self):
        """Initialize NCS collector with AWS credentials from temp file"""
        try:
            temp_creds_file = "dashboard_analyzer/temp_aws_credentials.env"
            collector = NCSDataCollector(temp_env_file=temp_creds_file)
            self.logger.info("✅ NCS collector initialized with temp AWS credentials")
            return collector
        except Exception as e:
            self.logger.error(f"Error initializing NCS collector: {e}")
            self.logger.warning("Using fallback NCS collector without temp credentials")
            return NCSDataCollector()
    
    def _create_llm(self, llm_type: LLMType):
        """Create LLM instance"""
        if llm_type in [LLMType.GPT4o, LLMType.O3, LLMType.O3_MINI, LLMType.O4_MINI]:
            return self._create_openai_llm(llm_type)
        else:
            return self._create_aws_llm(llm_type)
    
    def _create_openai_llm(self, llm_type: LLMType) -> OpenAiLLM:
        """Create OpenAI/Azure OpenAI LLM instance."""
        # Get credentials from environment variables
        api_key = os.getenv("AZURE_OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
        api_base = os.getenv("AZURE_OPENAI_ENDPOINT") or os.getenv("OPENAI_API_BASE")
        api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")
        deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        
        if not all([api_key, api_base, deployment_name]):
            raise ValueError("Missing required OpenAI/Azure OpenAI environment variables")
        
        return OpenAiLLM(
            llm_type=llm_type,
            api_key=api_key or "",
            api_base=api_base or "",
            api_version=api_version,
            api_dep_gpt=deployment_name or "",
            temperature=1.0  # Default temperature for O4-MINI compatibility
        )
    
    def _create_aws_llm(self, llm_type: LLMType) -> AWSLLM:
        """Create AWS Bedrock LLM instance."""
        region_name = os.getenv("AWS_REGION", "us-east-1")
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        profile_name = os.getenv("AWS_PROFILE")
        
        return AWSLLM(
            llm_type=llm_type,
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            profile_name=profile_name
        )
    
    # Removed _create_tools method - tools are now implemented directly

    async def _explanatory_drivers_tool(self, node_path: str, start_date: str, end_date: str, min_surveys: int = 10) -> str:
        """Tool for analyzing explanatory drivers and SHAP values."""
        try:
            if not self.silent_mode:
                self.logger.info(f"Collecting explanatory drivers for {node_path} from {start_date} to {end_date}")
            
            # Convert string dates to datetime
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
            
            # Use the existing explanatory drivers collection method with comparison filter
            print(f"         🔍 DEBUG: Causal agent using causal_filter: '{self.causal_filter}'")
            df = await self.pbi_collector.collect_explanatory_drivers_for_date_range(
                node_path, start_dt, end_dt, 
                comparison_filter=self.causal_filter,
                comparison_start_date=self.comparison_start_date,
                comparison_end_date=self.comparison_end_date
            )
            
            if df.empty:
                return f"No explanatory drivers data found for {node_path} in date range {start_date} to {end_date}"
            
            # Calculate survey count
            survey_count = len(df)
            
            # Analyze SHAP values and satisfaction differences
            analysis_result = []
            analysis_result.append(f"Survey Count: {survey_count} (threshold: {min_surveys})")
            
            # Add statistical reliability warning for low sample sizes
            statistical_warning = ""
            if survey_count < 20:
                statistical_warning = "⚠️ STATISTICAL DISCLAIMER: Sample size < 20 - results subject to high statistical variability"
                analysis_result.append(statistical_warning)
            elif survey_count < min_surveys:
                statistical_warning = "⚠️ CAUTION: Sample size below recommended threshold - results may have increased variability"
                analysis_result.append(statistical_warning)
            
            # Find ALL touchpoints (SHAP values) - no threshold filtering
            # Filter out NPS and NPS Comparative as they are not drivers but period comparisons
            if 'Shapdiff' in df.columns:
                df['Shapdiff'] = pd.to_numeric(df['Shapdiff'], errors='coerce')
                
                # Filter out non-driver touchpoints (NPS values are not explanatory drivers)
                candidate_touchpoint_cols = [
                    'TouchPoint_Master[filtered_name]',
                    'TouchPoint_Master[filtered_name',
                    'filtered_name',
                    'Filtered_name',
                    'TouchPoint_Master filtered_name'
                ]
                touchpoint_col = next((c for c in candidate_touchpoint_cols if c in df.columns), None)
                if touchpoint_col:
                    # Filter out NPS comparison values that are not real touchpoints
                    df_filtered = df[~df[touchpoint_col].isin(['NPS', 'NPS Comparative'])]
                else:
                    df_filtered = df
                
                # Get ALL touchpoints, not just significant ones
                all_touchpoints = df_filtered.copy()
                all_touchpoints['Shapdiff'] = pd.to_numeric(all_touchpoints['Shapdiff'], errors='coerce')
                all_touchpoints = all_touchpoints.dropna(subset=['Shapdiff'])
                
                if len(all_touchpoints) > 0:
                    analysis_result.append("ALL SHAP drivers found (including non-significant):")
                    
                    # Store data for final summary
                    drivers_data = []
                    
                    # Categorize touchpoints for workflow routing
                    operational_drivers = []
                    product_drivers = []
                    significant_drivers = []
                    
                    # Handle both DataFrame and Series/array types
                    try:
                        # Try DataFrame methods first
                        if hasattr(all_touchpoints, 'iterrows'):
                            # Sort by absolute SHAP value (descending) to show most important first
                            all_touchpoints_sorted = all_touchpoints.sort_values(by='Shapdiff', key=lambda x: abs(x), ascending=False)
                            
                            for i, (_, row) in enumerate(all_touchpoints_sorted.iterrows()):
                                # No limit - show all SHAP values
                                if hasattr(row, 'get') and touchpoint_col and touchpoint_col in row:
                                    touchpoint = row.get(touchpoint_col)
                                else:
                                    candidate_cols_in_row = [c for c in all_touchpoints_sorted.columns if isinstance(row.get(c, None), str)]
                                    touchpoint = row.get(candidate_cols_in_row[0]) if candidate_cols_in_row else 'Unknown'
                                shap_value = row['Shapdiff'] if 'Shapdiff' in row else 0.0
                                sat_diff = row.get('Satisfaction diff', 'N/A') if hasattr(row, 'get') else 'N/A'
                                
                                # Mark significance
                                significance_marker = "⭐" if abs(shap_value) > 0.1 else "⚪"
                                analysis_result.append(f"  {significance_marker} {touchpoint}: SHAP={shap_value:.3f}, Sat_diff={sat_diff}")
                                
                                # Store for data summary
                                drivers_data.append({
                                    'touchpoint': touchpoint,
                                    'shap_value': shap_value,
                                    'satisfaction_diff': sat_diff,
                                    'significant': abs(shap_value) > 0.1
                                })
                            
                                # Categorize touchpoint type
                                if touchpoint and isinstance(touchpoint, str):
                                    touchpoint_lower = touchpoint.lower()
                                    if any(op_keyword in touchpoint_lower for op_keyword in 
                                           ['otp', 'delay', 'punctual', 'baggage', 'misconex', 'mishandling', 'load factor', 'operational']):
                                        operational_drivers.append(touchpoint)
                                        if abs(shap_value) > 0.1:
                                            significant_drivers.append(touchpoint)
                                    else:
                                        product_drivers.append(touchpoint)
                                        if abs(shap_value) > 0.1:
                                            significant_drivers.append(touchpoint)
                        else:
                            # Fallback for array-like objects
                            analysis_result.append("Found drivers (limited analysis due to data format)")
                    except Exception as e:
                        analysis_result.append(f"Error processing touchpoints: {str(e)}")
                        self.logger.warning(f"Error processing touchpoints: {e}")
                    
                    # Store collected data
                    self.collected_data['explanatory_drivers'] = {
                        'survey_count': survey_count,
                        'all_drivers': drivers_data,
                        'significant_drivers': significant_drivers,
                        'operational_drivers': operational_drivers,
                        'product_drivers': product_drivers
                    }
                    
                    # Intelligent workflow routing based on significant drivers
                    if significant_drivers:
                        if operational_drivers and product_drivers:
                            analysis_result.append(f"MIXED SIGNIFICANT DRIVERS DETECTED: Operational={operational_drivers}, Product={product_drivers}")
                            analysis_result.append("RECOMMENDATION: Start with operative_data_tool for operational validation, then use verbatims_tool for product insights")
                        elif operational_drivers:
                            analysis_result.append(f"OPERATIONAL SIGNIFICANT DRIVERS DETECTED: {operational_drivers}")
                            analysis_result.append("RECOMMENDATION: Use OPERATIVE WORKFLOW → operative_data_tool to validate operational causes")
                        elif product_drivers:
                            analysis_result.append(f"PRODUCT/SERVICE SIGNIFICANT DRIVERS DETECTED: {product_drivers}")
                            analysis_result.append("RECOMMENDATION: Use PRODUCT WORKFLOW → verbatims_tool to extract concrete service issues")
                    else:
                        analysis_result.append("No significant SHAP drivers found (threshold: 0.1) - showing all drivers for context")
                        analysis_result.append("RECOMMENDATION: Use verbatims_tool for qualitative insights and patterns")
                else:
                    analysis_result.append("No SHAP drivers found at all")
                    analysis_result.append("RECOMMENDATION: Use verbatims_tool for qualitative insights and patterns")
            
            return " | ".join(analysis_result)
            
        except Exception as e:
            return f"Error in explanatory drivers analysis: {str(e)}"


    
    def _determine_next_tool_dynamic(self, current_tool: str, iteration: int, max_tools: int) -> Optional[str]:
        """Determine next tool dynamically based on context and identified routes"""
        
        # Check if we should validate routes after NCS/verbatims
        if self.tracker.should_validate_routes_after_tool(current_tool):
            return "routes_tool"
        
        # Standard tool sequence (fallback)
        standard_sequence = [
            "explanatory_drivers_tool",
            "operative_data_tool",     # ← Add operative tool after explanatory drivers
            "ncs_tool",                # ← First NCS for operational incidents
            "verbatims_tool",          # ← Then verbatims to validate correlation
            "routes_tool",
            "customer_profile_tool"
        ]
        
        # Find current position and return next
        try:
            current_index = standard_sequence.index(current_tool)
            if current_index + 1 < len(standard_sequence) and iteration < max_tools:
                return standard_sequence[current_index + 1]
        except ValueError:
            pass
        
        return None  # No more tools
    
    def _get_single_period_system_prompt(self) -> str:
        """DEPRECATED: Use _get_system_prompt(mode='single') instead"""
        return self._get_system_prompt(mode="single")
    
    def _get_single_period_input_template(self) -> str:
        """DEPRECATED: Use _get_input_template(mode='single') instead"""
        return self._get_input_template(mode="single")
    
    def _get_single_period_tool_result_message(self) -> str:
        """DEPRECATED: Use _get_tool_result_message(mode='single') instead"""
        return self._get_tool_result_message(mode="single")
    

    async def _execute_single_period_tool(
        self, 
        tool_name: str, 
        node_path: str, 
        start_date: str, 
        end_date: str,
        iteration: int
    ) -> str:
        """Execute a tool for single period analysis"""
        try:
            if tool_name == "operative_data_tool":
                # FIX: Define a fixed baseline period (e.g., 14 days prior to the analysis end date)
                end_dt = datetime.strptime(end_date, '%Y-%m-%d')
                baseline_start_dt = end_dt - timedelta(days=14)
                
                return await self._operative_data_tool_single_period(
                    node_path=node_path,
                    start_date=start_date,
                    end_date=end_date,
                    baseline_start_date=baseline_start_dt.strftime('%Y-%m-%d')
                )
            elif tool_name == "ncs_tool":
                return await self._ncs_tool_single_period(
                    node_path=node_path,
                    start_date=start_date,
                    end_date=end_date
                )
            elif tool_name == "routes_tool":
                return await self._routes_tool_single_period(
                    node_path=node_path,
                    start_date=start_date,
                    end_date=end_date,
                    min_surveys=3,
                    anomaly_type=getattr(self, 'current_anomaly_type', 'unknown')
                )
            elif tool_name == "verbatims_tool":
                return await self._verbatims_tool_single_period(
                    node_path=node_path,
                    start_date=start_date,
                    end_date=end_date
                )
            elif tool_name == "customer_profile_tool":
                return await self._customer_profile_tool(
                    node_path=node_path,
                    start_date=start_date,
                    end_date=end_date,
                    min_surveys=3,
                    mode="single"
                )
            else:
                return f"Unknown tool for single period: {tool_name}"
            
        except Exception as e:
            self.logger.error(f"❌ Error executing {tool_name} for single period: {type(e).__name__}: {str(e)}")
            return f"ERROR executing {tool_name} for single period: {type(e).__name__}: {str(e)}"
    
    async def _operative_data_tool_single_period(self, node_path: str, start_date: str, end_date: str, baseline_start_date: str) -> str:
        """Operative data tool for single period analysis (absolute values + correlation analysis)"""
        try:
            self.logger.info(f"Collecting operative data for {node_path} from {baseline_start_date} to {end_date} for single period analysis")
            
            # Convert string dates to datetime
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
            baseline_start_dt = datetime.strptime(baseline_start_date, '%Y-%m-%d')

            # Get operative data for the entire range (baseline + target day)
            operative_data = await self.pbi_collector.collect_operative_data_for_date(
                node_path=node_path,
                target_date=end_dt,
                comparison_days=14,
                use_flexible=True
            )
            
            if operative_data.empty:
                return f"No operative data found for {node_path} in range {baseline_start_date} to {end_date}"
            
            # Pass the full dataset and the specific target date for correlation analysis
            return await self._operative_data_tool_correlation_analysis(node_path, operative_data, end_date)
            
        except Exception as e:
            self.logger.error(f"❌ Error in single period operative data tool: {type(e).__name__}: {str(e)}")
            return f"ERROR in operative data tool: {type(e).__name__}: {str(e)}"
    
    async def _operative_data_tool_correlation_analysis(self, node_path: str, operative_data: pd.DataFrame, target_date_str: str) -> str:
        """Operative data tool with correlation analysis using aggregated period data."""
        try:
            # Clean the data
            cleaned_data = operative_data.copy()
            numeric_columns = ['Load_Factor', 'OTP15_adjusted', 'Misconex', 'Mishandling']
            for col in numeric_columns:
                if col in cleaned_data.columns:
                    cleaned_data[col] = cleaned_data[col].replace('', pd.NA)
                    cleaned_data[col] = pd.to_numeric(cleaned_data[col], errors='coerce')

            # Handle aggregated data by Period_Group (not individual dates)
            if 'Period_Group' not in cleaned_data.columns:
                return f"❌ No Period_Group column found in operative data. Available columns: {list(cleaned_data.columns)}"

            # Convert target date to datetime for period identification
            target_date_dt = datetime.strptime(target_date_str, '%Y-%m-%d').date()

            # Sort data by Period_Group (most recent first)
            cleaned_data = cleaned_data.sort_values('Period_Group', ascending=True)

            # Find the target period (most recent period = period 1)
            # The data is already sorted by Period_Group ascending, so period 1 is the most recent
            if cleaned_data.empty:
                return f"No operative data found for {node_path}"

            # Get target period data (most recent period)
            target_period_data = cleaned_data.iloc[0]  # First row is most recent period

            # Calculate baseline from previous periods (periods 2, 3, 4, etc.)
            baseline_data = cleaned_data.iloc[1:]  # All rows except the most recent

            if len(baseline_data) < 2:
                return f"📊 **DATOS OPERATIVOS - ANÁLISIS PERIODO**\n📅 Fecha: {target_date_str}\n🎯 Segmento: {node_path}\n⚠️ Insuficientes períodos para baseline (solo {len(baseline_data)} períodos disponibles)"
            
            # Format correlation analysis results
            result_parts = []
            result_parts.append(f"📊 **DATOS OPERATIVOS - ANÁLISIS CORRELACIÓN**")
            result_parts.append(f"📅 Fecha: {target_date_str}")
            result_parts.append(f"🎯 Segmento: {node_path}")
            result_parts.append("")
            result_parts.append("**VALORES ABSOLUTOS Y CORRELACIÓN CON NPS:**")
            
            # Analyze each metric for correlation with NPS anomaly using period data
            correlation_analysis = []
            metrics_analysis = []

            # Get period information for context
            target_period = target_period_data.get('Period_Group', 'N/A')
            num_baseline_periods = len(baseline_data)
            target_min_date = target_period_data.get('Min_Date', 'N/A')
            target_max_date = target_period_data.get('Max_Date', 'N/A')

            result_parts.append(f"📊 Período Objetivo: {target_period}")
            result_parts.append(f"📅 Rango del período: {target_min_date} a {target_max_date}")
            result_parts.append(f"📈 Períodos baseline: {num_baseline_periods}")
            result_parts.append("")
            
            for metric in numeric_columns:
                if metric in cleaned_data.columns:
                    baseline_values = baseline_data[metric].dropna()
                    period_value = target_period_data.get(metric)
                    
                    if not baseline_values.empty and not pd.isna(period_value) and len(baseline_values) >= 2:
                        baseline_avg = baseline_values.mean()
                        delta = period_value - baseline_avg
                        
                        # Determine significance threshold
                        thresholds = {
                            'Load_Factor': 3.0,
                            'OTP15_adjusted': 3.0,
                            'Misconex': 1.0,
                            'Mishandling': 0.5
                        }
                        threshold = thresholds.get(metric, 2.0)
                        is_significant = abs(delta) > threshold
                        
                        direction = "↑" if delta > 0 else "↓"
                        significance = " ⚠️" if is_significant else ""
                        
                        # Format metric line
                        metric_line = f"• {metric}: {period_value:.1f}% (media: {baseline_avg:.1f}%, {direction}{abs(delta):.1f}pts){significance}"
                        metrics_analysis.append(metric_line)
                        
                        # Analyze correlation with NPS anomaly (assuming negative NPS anomaly)
                        # For negative NPS anomaly, we expect:
                        # - Lower OTP (worse performance)
                        # - Higher Misconex/Mishandling (worse performance)  
                        # - Higher Load Factor (inversely proportional to NPS)
                        
                        if metric == 'OTP15_adjusted' and delta < 0:
                            correlation_analysis.append(f"✅ {metric}: Correlaciona con caída NPS (peor puntualidad)")
                        elif metric in ['Misconex', 'Mishandling'] and delta > 0:
                            correlation_analysis.append(f"✅ {metric}: Correlaciona con caída NPS (más incidentes)")
                        elif metric == 'Load_Factor' and delta > 0:
                            correlation_analysis.append(f"✅ {metric}: Correlaciona con caída NPS (mayor ocupación, peor experiencia)")
                        elif metric == 'Load_Factor' and delta < 0:
                            correlation_analysis.append(f"❌ {metric}: No correlaciona (menor ocupación vs caída NPS)")
                        else:
                            correlation_analysis.append(f"❌ {metric}: No correlaciona con caída NPS")
            
            # Add metrics analysis
            result_parts.extend(metrics_analysis)
            result_parts.append("")
            result_parts.append("**CORRELACIÓN CON ANOMALÍA NPS:**")
            result_parts.extend(correlation_analysis)
            result_parts.append("")
            result_parts.append("**NOTA:** Análisis de correlación entre métricas operativas y anomalía NPS detectada.")
            
            return "\n".join(result_parts)
            
        except Exception as e:
            self.logger.error(f"❌ Error in correlation analysis operative data tool: {type(e).__name__}: {str(e)}")
            return f"ERROR in correlation analysis operative data tool: {type(e).__name__}: {str(e)}"
    
    async def _ncs_tool_single_period(self, node_path: str, start_date: str, end_date: str) -> str:
        """NCS tool for single period analysis (absolute incidents only)"""
        try:
            self.logger.info(f"Collecting NCS data for {node_path} from {start_date} to {end_date} (single period)")
            
            # Convert string dates to datetime
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
            
            # Get NCS data for the specific period only (without await - it's synchronous)
            ncs_data = self.ncs_collector.collect_ncs_data_for_date_range(
                start_date=start_dt,
                end_date=end_dt
            )
            
            if ncs_data.empty:
                return f"No NCS data found for {node_path} from {start_date} to {end_date}"

            # 2. Apply segment filtering BEFORE analysis
            filtered_ncs_data = await self._filter_ncs_by_segment(ncs_data, node_path)

            if filtered_ncs_data.empty:
                return f"No NCS incidents found for segment {node_path} from {start_date} to {end_date} after filtering"

            # 3. Analyze the FILTERED data
            incident_analysis = self.ncs_collector.analyze_ncs_incidents_for_period(filtered_ncs_data, analysis_focus="all")

            # --- Build the result string from the analysis of filtered data ---
            result_parts = []
            result_parts.append(f"📊 **INCIDENTES NCS - PERIODO ÚNICO**")
            result_parts.append(f"📅 Período: {start_date} a {end_date}")
            result_parts.append(f"🎯 Segmento: {node_path}")
            result_parts.append(f"Total Incidentes (Segmento): {len(filtered_ncs_data)}")
            result_parts.append("")
            result_parts.append("**INCIDENTES DEL PERIODO:**")

            # Count incidents by type from the analysis result
            incident_counts = incident_analysis.get("incident_counts", {})
            for incident_type, count in incident_counts.items():
                result_parts.append(f"• {incident_type}: {count} incidentes")
            
            # Add sample incidents if available
            if "detailed_incidents" in incident_analysis:
                detailed = incident_analysis["detailed_incidents"]
                result_parts.append(f"• Incidentes con descripción detallada: {detailed['count']}")
                
                if detailed.get("sample_incidents"):
                    result_parts.append("• Ejemplos de incidentes:")
                    for i, incident in enumerate(detailed["sample_incidents"][:2], 1):
                        # Truncate long incidents
                        truncated = incident[:150] + "..." if len(incident) > 150 else incident
                        result_parts.append(f"  {i}. {truncated}")
                
                if detailed.get("incident_themes"):
                    result_parts.append("• Temas principales:")
                    for theme in detailed["incident_themes"][:3]:
                        result_parts.append(f"  - {theme}")
            
            # Add route analysis if available
            if "route_analysis" in incident_analysis:
                route_info = incident_analysis["route_analysis"]
                result_parts.append(f"• Rutas afectadas: {route_info['total_routes_affected']}")
                if route_info.get("most_affected_routes"):
                    result_parts.append("• Rutas más impactadas:")
                    for route, count in list(route_info["most_affected_routes"].items())[:3]:
                        result_parts.append(f"  - {route}: {count} incidentes")
            
            # Add summary insights
            if "summary_insights" in incident_analysis:
                result_parts.append("• Resumen de impacto:")
                for insight in incident_analysis["summary_insights"][:3]:
                    result_parts.append(f"  - {insight}")
            
            result_parts.append("")
            result_parts.append("**NOTA:** Estos son incidentes absolutos del período específico, sin comparación temporal.")
            
            return "\n".join(result_parts)
            
        except Exception as e:
            self.logger.error(f"❌ Error in single period NCS tool: {type(e).__name__}: {str(e)}")
            return f"ERROR in NCS tool: {type(e).__name__}: {str(e)}"
    
    async def _routes_tool_single_period(self, node_path: str, start_date: str, end_date: str, min_surveys: int = 2, anomaly_type: str = "unknown") -> str:
        """Routes tool for single period analysis (absolute NPS values only)"""
        try:
            self.logger.info(f"Collecting routes data for {node_path} from {start_date} to {end_date} (single period)")
            
            # Convert string dates to datetime
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
            
            result_parts = []
            result_parts.append(f"📊 **RUTAS - PERIODO ÚNICO**")
            result_parts.append(f"📅 Período: {start_date} a {end_date}")
            result_parts.append(f"🎯 Segmento: {node_path}")
            result_parts.append(f"🔍 Tipo de anomalía: {anomaly_type}")
            result_parts.append("")
            
            # 1. Get routes with NPS data (absolute values only, min_surveys >= 2)
            routes_data = await self.pbi_collector.collect_routes_for_date_range(
                node_path=node_path,
                start_date=start_dt,
                end_date=end_dt,
                comparison_filter=None  # No comparison for single period
            )
            
            if routes_data.empty:
                result_parts.append("❌ No se encontraron datos de rutas con NPS para este período.")
            else:
                # Clean column names (remove brackets)
                routes_data = self._safe_clean_columns(routes_data, method="replace")
                
                # Find key columns
                route_col = self._find_column(routes_data, ['route'])
                nps_col = self._find_column(routes_data, ['nps'])
                pax_col = self._find_column(routes_data, ['pax', 'n (route)'])
                
                if route_col and nps_col:
                    # Filter by minimum surveys (>= 2)
                    if pax_col:
                        routes_data = routes_data[routes_data[pax_col].fillna(0) >= min_surveys]
                    
                    if not routes_data.empty:
                        # Sort by NPS based on anomaly type
                        if anomaly_type.lower() in ['positive', 'high', 'good']:
                            # For positive anomalies: sort high to low (best routes first)
                            routes_data = routes_data.sort_values(nps_col, ascending=False)
                            sort_direction = "mayor a menor NPS"
                        else:
                            # For negative anomalies: sort low to high (worst routes first)
                            routes_data = routes_data.sort_values(nps_col, ascending=True)
                            sort_direction = "menor a mayor NPS"
                        
                        result_parts.append(f"**RUTAS CON NPS (ordenadas {sort_direction}):**")
            
                        for _, route in routes_data.head(10).iterrows():
                            route_name = route.get(route_col, 'Unknown')
                            nps_value = route.get(nps_col, 0)
                            sample_size = route.get(pax_col, 0) if pax_col else 0
                        
                        result_parts.append(f"• {route_name}: NPS {nps_value:.1f} (n={sample_size})")
                    else:
                        result_parts.append("❌ No hay rutas con suficientes encuestas (mínimo 2).")
                else:
                    result_parts.append(f"❌ Columnas requeridas no encontradas. Disponibles: {list(routes_data.columns)}")
            
            # 2. Get NCS routes (operational incidents)
            result_parts.append("")
            result_parts.append("**RUTAS CON INCIDENTES OPERACIONALES (NCS):**")
            
            try:
                # Extract segment info from node_path
                segments = node_path.split('/')
                cabins = []
                companies = []
                hauls = []
                
                # Parse node_path to extract segment info
                if 'SH' in segments:
                    hauls.append('SH')
                if 'LH' in segments:
                    hauls.append('LH')
                if 'Economy' in segments:
                    cabins.append('Economy')
                if 'Business' in segments:
                    cabins.append('Business')
                if 'Premium' in segments:
                    cabins.append('Premium')
                if 'IB' in segments:
                    companies.append('IB')
                if 'YW' in segments:
                    companies.append('YW')
                
                # If no specific segments found, use defaults
                if not hauls:
                    hauls = ['SH', 'LH']
                if not cabins:
                    cabins = ['Economy', 'Business', 'Premium']
                if not companies:
                    companies = ['IB', 'YW']
                
                # Get NCS routes
                ncs_routes_data = await self._get_ncs_routes(node_path, cabins, companies, hauls, start_dt, end_dt)
                
                if ncs_routes_data and 'routes' in ncs_routes_data:
                    ncs_routes = ncs_routes_data['routes']
                    result_parts.append(f"📊 Rutas con incidentes NCS: {len(ncs_routes)}")
                    for route in ncs_routes[:10]:  # Show first 10
                        result_parts.append(f"• {route}")
                else:
                    result_parts.append("✅ No se encontraron incidentes operacionales en este período.")
                    
            except Exception as e:
                self.logger.warning(f"Error getting NCS routes: {str(e)}")
                result_parts.append("⚠️ No se pudieron obtener datos de incidentes operacionales.")
            
            result_parts.append("")
            result_parts.append("**NOTA:** Valores NPS absolutos del período específico, sin comparación temporal.")
            
            return "\n".join(result_parts)
            
        except Exception as e:
            self.logger.error(f"❌ Error in single period routes tool: {type(e).__name__}: {str(e)}")
            return f"ERROR in routes tool: {type(e).__name__}: {str(e)}"
    
    async def _generate_single_period_synthesis(
        self, 
        message_history: MessageHistory,
        node_path: str,
        start_date: str, 
        end_date: str,
        nps_context: str = ""
    ) -> str:
        """Generate final synthesis for single period analysis"""
        try:
            # Build data summary for single period
            data_summary = self._build_single_period_data_summary()
            
            # Get synthesis prompt from YAML config
            synthesis_prompt_template = self.config.get('single_period_prompts', {}).get('synthesis_prompt', 
                "Basándote en el análisis de {node_path} para el período {start_date} a {end_date}, proporciona una síntesis integral.")
            
            # Create synthesis prompt for single period with specific format
            synthesis_prompt = synthesis_prompt_template.format(
                node_path=node_path,
                start_date=start_date,
                end_date=end_date,
                data_summary=data_summary
            )
            
            # Get LLM response using message history with synthesis prompt
            from langchain.schema import HumanMessage
            # Add synthesis prompt to existing conversation context
            synthesis_messages = message_history.get_messages()
            synthesis_messages.append(HumanMessage(content=synthesis_prompt))
            response = await self.llm(synthesis_messages)
            
            if response and hasattr(response, 'content'):
                return f"🤖 **ANÁLISIS PERIODO ÚNICO**\n\n{response.content}"
            else:
                return "🤖 **ANÁLISIS PERIODO ÚNICO**\n\nAnálisis completado pero la síntesis falló."
                
        except Exception as e:
            self.logger.error(f"❌ Error en síntesis de período único: {type(e).__name__}: {str(e)}")
            return "🤖 **ANÁLISIS PERIODO ÚNICO**\n\nSíntesis falló debido a error."
    
    def _build_single_period_data_summary(self) -> str:
        """Build data summary for single period analysis"""
        summary_parts = []
        
        # Add collected data summary
        try:
            data_summary = self._build_collected_data_summary()
            summary_parts.append("📊 **DATOS RECOLECTADOS:**")
            summary_parts.append(data_summary)
        except Exception as e:
            self.logger.error(f"Error building data summary: {e}")
            summary_parts.append("📊 **DATOS RECOLECTADOS:** Error construyendo resumen")
        
        # Add tool reflections
        if self.tracker.previous_explanations:
            summary_parts.append("\n💭 **ANÁLISIS DE HERRAMIENTAS:**")
            for i, reflection in enumerate(self.tracker.previous_explanations, 1):
                summary_parts.append(f"   {i}. {reflection}")
        
        return "\n".join(summary_parts)
    
    def _build_single_period_fallback(self) -> str:
        """Build fallback response for single period analysis"""
        fallback_parts = []
        fallback_parts.append("🤖 **ANÁLISIS PERIODO ÚNICO**")
        fallback_parts.append("Análisis completado con síntesis parcial debido a error de procesamiento")
        fallback_parts.append("")
        
        # Add collected data summary
        try:
            data_summary = self._build_single_period_data_summary()
            fallback_parts.append(data_summary)
        except Exception as summary_error:
            self.logger.error(f"Error building data summary for fallback: {summary_error}")
            fallback_parts.append("❌ Error construyendo resumen de datos")
        
        return "\n".join(fallback_parts)
    
    async def investigate_anomaly(
        self,
        node_path: str,
        start_date: str,
        end_date: str,
        anomaly_type: str,
        anomaly_magnitude: float,
        nps_context: str = "",
        causal_filter: str = "vs L7d",
        comparison_start_date: datetime = None,
        comparison_end_date: datetime = None
    ) -> str:
        """
        Main investigation method that routes to single or comparative mode based on study_mode
        """
        
        # Update instance variables with the passed parameters
        if causal_filter:
            self.causal_filter = causal_filter
        if comparison_start_date:
            self.comparison_start_date = comparison_start_date
        if comparison_end_date:
            self.comparison_end_date = comparison_end_date
        
        # Route to appropriate investigation method based on study_mode
        if self.study_mode == "single":
            return await self._investigate_anomaly_single_period(
                node_path, start_date, end_date, anomaly_type, anomaly_magnitude, nps_context
            )
        else:
            return await self._investigate_anomaly_with_comparison(
                node_path, start_date, end_date, anomaly_type, anomaly_magnitude, nps_context,
                causal_filter, comparison_start_date, comparison_end_date
            )
    
    async def _investigate_anomaly_single_period(
        self,
        node_path: str,
        start_date: str,
        end_date: str,
        anomaly_type: str,
        anomaly_magnitude: float,
        nps_context: str = ""
    ) -> str:
        """
        Single period investigation (no comparison)
        
        Flow:
        1. Analyze hierarchical tree structure (helper prompt)
        2. Skip explanatory drivers (not needed for single period)
        3. Analyze operative data with mean comparison
        4. Analyze NCS incidents for the specific period only
        5. Analyze routes filtered by NPS for the specific period only
        """
        
        try:
            self.logger.info("🎯 Starting single period investigation (no comparison)")
            
            # Reset tracker
            self.tracker.reset_tracker()
            self.current_anomaly_type = anomaly_type
            
            # Create message history for main flow
            message_history = MessageHistory(logger=self.logger)
            
            # 1. SYSTEM MESSAGE - Use single period specific prompt
            system_prompt = self._get_single_period_system_prompt()
            message_history.create_and_add_message(
                content=system_prompt,
                message_type=MessageType.SYSTEM
            )
            self.tracker.log_message("SYSTEM", system_prompt)
            
            # 2. USER MESSAGE: Investigation parameters for single period
            # Extract NPS values from nps_context if available
            current_nps = "N/A"
            baseline_nps = "N/A" 
            nps_difference = "N/A"
            
            if nps_context:
                # Try to extract NPS values from the context
                import re
                current_match = re.search(r'Current NPS:\s*([\d.-]+)', nps_context)
                baseline_match = re.search(r'Baseline NPS:\s*([\d.-]+)', nps_context)
                
                if current_match:
                    current_nps = current_match.group(1)
                if baseline_match:
                    baseline_nps = baseline_match.group(1)
                    
                # Calculate difference if both values are available
                if current_nps != "N/A" and baseline_nps != "N/A":
                    try:
                        current_val = float(current_nps)
                        baseline_val = float(baseline_nps)
                        nps_difference = f"{current_val - baseline_val:.1f}"
                    except ValueError:
                        nps_difference = "N/A"
            
            user_input = self._get_single_period_input_template().format(
                node_path=node_path,
                start_date=start_date,
                end_date=end_date,
                anomaly_type=anomaly_type,
                anomaly_magnitude=anomaly_magnitude,
                current_nps=current_nps,
                baseline_nps=baseline_nps,
                nps_difference=nps_difference
            )
            
            message_history.create_and_add_message(
                content=user_input,
                message_type=MessageType.USER
            )
            self.tracker.log_message("USER", user_input)
            
            # FIRST: Let the agent decide which tool to start with based on the initial context
            self.logger.info("🤔 First step: Agent deciding initial tool to execute (single period)...")
            
            # Create prompt for initial tool decision
            initial_decision_prompt = f"""
            Based on the investigation parameters and context, decide which tool to execute FIRST for single period analysis.
            
            INVESTIGATION CONTEXT:
            - Node Path: {node_path}
            - Period: {start_date} to {end_date}
            - Anomaly Type: {anomaly_type}
            - Anomaly Magnitude: {anomaly_magnitude}
            - Current NPS: {current_nps}
            - Baseline NPS: {baseline_nps}
            - NPS Difference: {nps_difference}
            
            AVAILABLE TOOLS FOR SINGLE PERIOD:
            - operative_data_tool: Analyze operational KPIs (OTP, Load Factor, etc.) for the specific period
            - ncs_tool: Analyze operational incidents and NCS data for the specific period
            - routes_tool: Analyze route-specific performance for the specific period
            - verbatims_tool: Analyze customer feedback and verbatims for the specific period
            - customer_profile_tool: Analyze customer profile impact for the specific period
            
            DECISION CRITERIA:
            - For single period analysis: Start with operative_data_tool to understand operational metrics
            - Consider the anomaly type and magnitude in your decision
            - Focus on tools that provide insights for the specific period without comparison
            
            Respond with ONLY the name of the tool to execute first:
            """
            
            # Get initial tool decision from LLM - NO FALLBACKS, AGENT MUST DECIDE
            try:
                from langchain.schema import HumanMessage
                initial_response = await self.llm([HumanMessage(content=initial_decision_prompt)])
                initial_tool = initial_response.content.strip()
                
                # Clean up the response and validate
                valid_tools = [
                    'operative_data_tool', 'ncs_tool', 'routes_tool',
                    'verbatims_tool', 'customer_profile_tool'
                ]
                
                if initial_tool in valid_tools:
                    current_tool = initial_tool
                    self.logger.info(f"🎯 Agent decided to start with: {current_tool}")
                else:
                    # ❌ NO FALLBACK - AGENT MUST PROVIDE VALID TOOL
                    error_msg = f"Agent provided invalid tool: '{initial_tool}'. Valid tools are: {valid_tools}"
                    self.logger.error(f"❌ {error_msg}")
                    raise ValueError(error_msg)
                    
            except Exception as e:
                # ❌ NO FALLBACK - INVESTIGATION MUST FAIL IF AGENT CANNOT DECIDE
                error_msg = f"Agent failed to decide initial tool: {e}"
                self.logger.error(f"❌ {error_msg}")
                raise RuntimeError(error_msg)
            
            # Now execute tools based on agent decisions
            max_iterations = 5  # Allow up to 5 iterations for dynamic tool selection
            iteration = 0
            
            while current_tool and iteration < max_iterations:
                iteration += 1
                self.tracker.next_iteration()
                
                self.logger.info(f"🔧 Iteration {iteration}: Processing {current_tool} (single period)")
                
                # Execute tool with single period logic
                tool_result = await self._execute_single_period_tool(
                    current_tool, node_path, start_date, end_date, iteration
                )
                
                # Store tool context
                self.tracker.set_tool_context(current_tool, tool_result)
                
                # AI MESSAGE: Reflection using clean context + tool results
                reflection_result = await self._get_clean_reflection(
                    system_prompt=system_prompt,
                    tool_name=current_tool,
                    tool_result=tool_result,
                    message_history=message_history
                )
                
                if reflection_result and isinstance(reflection_result, dict):
                    reflection = reflection_result.get("reflection", "")
                    next_tool_code = reflection_result.get("next_tool_code", "")
                
                    if reflection:
                        self.tracker.add_explanation(reflection)
                        message_history.create_and_add_message(
                            content=reflection,
                            message_type=MessageType.AI,
                            agent=AgentName.CONVERSATIONAL
                        )
                        self.tracker.log_message("AI", f"REFLECTION: {reflection}")
                        self.logger.info(f"💭 Reflection captured for {current_tool}")
                        
                        # Execute next tool code if provided
                        if next_tool_code:
                            self.logger.info(f"🔄 Executing next tool code: {next_tool_code}")

                            # Execute the tool based on the code from reflection
                            try:
                                if next_tool_code == "operative_data_tool":
                                    current_tool = "operative_data_tool"
                                elif next_tool_code == "ncs_tool":
                                    current_tool = "ncs_tool"
                                elif next_tool_code == "verbatims_tool":
                                    current_tool = "verbatims_tool"
                                elif next_tool_code == "routes_tool":
                                    current_tool = "routes_tool"
                                elif next_tool_code == "customer_profile_tool":
                                    current_tool = "customer_profile_tool"
                                else:
                                    self.logger.warning(f"⚠️ Unknown tool code: {next_tool_code}")
                                    # Let agent decide the next tool based on reflection
                                    current_tool = await self._determine_next_tool_from_reflection(
                                        reflection, current_tool, iteration, max_iterations
                                    )
                            except Exception as e:
                                self.logger.error(f"❌ Error executing tool code {next_tool_code}: {e}")
                                # Let agent decide the next tool based on reflection
                                current_tool = await self._determine_next_tool_from_reflection(
                                    reflection, current_tool, iteration, max_iterations
                                )

                            # Execute the tool and get results
                            if current_tool:
                                self.logger.info(f"🔄 Executing tool: {current_tool}")
                                tool_result = await self._execute_single_period_tool(
                                    current_tool, node_path, start_date, end_date, iteration
                                )

                                # Store tool context
                                self.tracker.set_tool_context(current_tool, tool_result)

                                # Get reflection for this tool execution
                                reflection_result = await self._get_clean_reflection(
                        system_prompt=system_prompt,
                        tool_name=current_tool,
                        tool_result=tool_result,
                                    message_history=message_history
                    )
                    
                                if reflection_result and isinstance(reflection_result, dict):
                                    reflection = reflection_result.get("reflection", "")
                                    next_tool_code = reflection_result.get("next_tool_code", "")

                    if reflection:
                        self.tracker.add_explanation(reflection)
                        message_history.create_and_add_message(
                            content=reflection,
                            message_type=MessageType.AI,
                            agent=AgentName.CONVERSATIONAL
                        )
                        self.tracker.log_message("AI", f"REFLECTION: {reflection}")
                        self.logger.info(f"💭 Reflection captured for {current_tool}")

                        # Continue with next iteration
                        continue
                    else:
                        # Let the agent decide the next tool based on reflection and helper prompts
                        current_tool = await self._determine_next_tool_from_reflection(
                            reflection, current_tool, iteration, max_iterations
                        )
                    
                    if current_tool:
                        self.logger.info(f"🔄 Agent decided next tool: {current_tool}")
                    else:
                        self.logger.info(f"✅ Agent decided to end investigation")
                        break

                else:
                    self.logger.warning(f"⚠️ No reflection captured for {current_tool}")
                    # ❌ NO FALLBACK - INVESTIGATION MUST END IF AGENT CANNOT REFLECT
                    self.logger.error(f"❌ Investigation cannot continue without agent reflection")
                    break   
                
            # Final synthesis for single period
            try:
                self.logger.info("🎯 Iniciando síntesis final para análisis de período único...")
                final_response = await self._generate_single_period_synthesis(
                    message_history, node_path, start_date, end_date, nps_context
                )
                
                # Export conversation log
                conversation_file = self.export_conversation(node_path=node_path, start_date=start_date, end_date=end_date)
                if conversation_file:
                    self.logger.info(f"🗂️ Conversación completa guardada: {conversation_file}")
                
                self.logger.info("✅ Investigación de período único completada")
                return final_response
                
            except Exception as e:
                self.logger.error(f"❌ Error en síntesis de período único: {type(e).__name__}: {str(e)}")
                return self._build_single_period_fallback()
            
        except Exception as e:
            self.logger.error(f"❌ Error crítico en investigación de período único: {type(e).__name__}: {e}")
            return self._build_single_period_fallback()
    
    async def _investigate_anomaly_with_comparison(
        self,
        node_path: str,
        start_date: str,
        end_date: str,
        anomaly_type: str,
        anomaly_magnitude: float,
        nps_context: str = "",
        causal_filter: str = "vs L7d",
        comparison_start_date: datetime = None,
        comparison_end_date: datetime = None
    ) -> str:
        """
        Comparative investigation (with comparison to other periods)
        
        Flow:
        1. Analyze hierarchical tree structure (helper prompt)
        2. Analyze explanatory drivers (for comparison)
        3. Analyze operative data with comparison
        4. Analyze NCS incidents with temporal comparison
        5. Analyze routes with explanatory drivers
        6. Optional: Customer profile analysis
        """
        
        try:
            self.logger.info("🎯 Starting comparative investigation (with comparison)")
            
            # Reset tracker
            self.tracker.reset_tracker()
            self.current_anomaly_type = anomaly_type
            
            # Create message history for main flow
            message_history = MessageHistory(logger=self.logger)
            
            # 1. SYSTEM MESSAGE
            system_prompt = self._get_system_prompt(mode="comparative")
            message_history.create_and_add_message(
                content=system_prompt,
                message_type=MessageType.SYSTEM
            )
            self.tracker.log_message("SYSTEM", system_prompt)
            
            # 2. USER MESSAGE: Investigation parameters
            # Extract NPS values from nps_context if available
            current_nps = "N/A"
            baseline_nps = "N/A" 
            nps_difference = "N/A"
            
            self.logger.info(f"🔍 DEBUG COMPARATIVE: nps_context received (length={len(nps_context)}): '{nps_context}'")
            if nps_context:
                # Try to extract NPS values from the context
                import re
                self.logger.info(f"🔍 DEBUG COMPARATIVE: nps_context is not empty, processing...")
                current_match = re.search(r'Current NPS:\s*([\d.-]+)', nps_context)
                baseline_match = re.search(r'Baseline NPS:\s*([\d.-]+)', nps_context)
                
                self.logger.info(f"🔍 DEBUG COMPARATIVE: current_match: {current_match}")
                self.logger.info(f"🔍 DEBUG COMPARATIVE: baseline_match: {baseline_match}")
                
                if current_match:
                    current_nps = current_match.group(1)
                    self.logger.info(f"🔍 DEBUG COMPARATIVE: extracted current_nps: {current_nps}")
                if baseline_match:
                    baseline_nps = baseline_match.group(1)
                    self.logger.info(f"🔍 DEBUG COMPARATIVE: extracted baseline_nps: {baseline_nps}")
                    
                # Calculate difference if both values are available
                if current_nps != "N/A" and baseline_nps != "N/A":
                    try:
                        current_val = float(current_nps)
                        baseline_val = float(baseline_nps)
                        nps_difference = f"{current_val - baseline_val:.1f}"
                    except ValueError:
                        nps_difference = "N/A"
                else:
                    self.logger.info(f"🔍 DEBUG COMPARATIVE: nps_context is EMPTY - will use N/A values")
            
            self.logger.info(f"🔍 DEBUG COMPARATIVE: Final values for template - current_nps: {current_nps}, baseline_nps: {baseline_nps}, nps_difference: {nps_difference}")
            
            user_input = self._get_input_template(mode="comparative").format(
                node_path=node_path,
                start_date=start_date,
                end_date=end_date,
                anomaly_type=anomaly_type,
                anomaly_magnitude=anomaly_magnitude,
                causal_filter=causal_filter,
                current_nps=current_nps,
                baseline_nps=baseline_nps,
                nps_difference=nps_difference
            )
            
            self.logger.info(f"🔍 DEBUG COMPARATIVE: Template output preview: {user_input[:200]}...")
            
            message_history.create_and_add_message(
                content=user_input,
                message_type=MessageType.USER
            )
            self.tracker.log_message("USER", user_input)
            
            # FIRST: Let the agent decide which tool to start with based on the initial context
            self.logger.info("🤔 First step: Agent deciding initial tool to execute...")
            
            # Create prompt for initial tool decision
            initial_decision_prompt = f"""
            Based on the investigation parameters and context, decide which tool to execute FIRST.
            
            INVESTIGATION CONTEXT:
            - Node Path: {node_path}
            - Period: {start_date} to {end_date}
            - Anomaly Type: {anomaly_type}
            - Anomaly Magnitude: {anomaly_magnitude}
            - Comparison Filter: {causal_filter}
            - Current NPS: {current_nps}
            - Baseline NPS: {baseline_nps}
            - NPS Difference: {nps_difference}
            
            AVAILABLE TOOLS:
            - explanatory_drivers_tool: Analyze SHAP values and explanatory drivers (for comparative analysis)
            - operative_data_tool: Analyze operational KPIs (OTP, Load Factor, etc.)
            - ncs_tool: Analyze operational incidents and NCS data
            - verbatims_tool: Analyze customer feedback and verbatims
            - routes_tool: Analyze route-specific performance
            - customer_profile_tool: Analyze customer profile impact
            
            DECISION CRITERIA:
            - For comparative analysis: Start with explanatory_drivers_tool to understand SHAP drivers
            - For single period: Start with operative_data_tool to analyze operational metrics
            - Consider the anomaly type and magnitude in your decision
            
            Respond with ONLY the name of the tool to execute first:
            """
            
            # Get initial tool decision from LLM - NO FALLBACKS, AGENT MUST DECIDE
            try:
                from langchain.schema import HumanMessage
                initial_response = await self.llm([HumanMessage(content=initial_decision_prompt)])
                initial_tool = initial_response.content.strip()
                
                # Clean up the response and validate
                valid_tools = [
                    'explanatory_drivers_tool', 'operative_data_tool', 'ncs_tool',
                    'verbatims_tool', 'routes_tool', 'customer_profile_tool'
                ]
                
                if initial_tool in valid_tools:
                    current_tool = initial_tool
                    self.logger.info(f"🎯 Agent decided to start with: {current_tool}")
                else:
                    # ❌ NO FALLBACK - AGENT MUST PROVIDE VALID TOOL
                    error_msg = f"Agent provided invalid tool: '{initial_tool}'. Valid tools are: {valid_tools}"
                    self.logger.error(f"❌ {error_msg}")
                    raise ValueError(error_msg)
                    
            except Exception as e:
                # ❌ NO FALLBACK - INVESTIGATION MUST FAIL IF AGENT CANNOT DECIDE
                error_msg = f"Agent failed to decide initial tool: {e}"
                self.logger.error(f"❌ {error_msg}")
                raise RuntimeError(error_msg)
            
            # Now execute tools based on agent decisions
            max_iterations = 5  # Maximum iterations to prevent infinite loops
            iteration = 0
            
            while current_tool and iteration < max_iterations:
                iteration += 1
                self.tracker.next_iteration()
                
                self.logger.info(f"🔧 Iteration {iteration}: Processing {current_tool} (comparative)")
                
                # Execute tool with comparative logic
                tool_result = await self._execute_tool_comparative(
                    current_tool, node_path, start_date, end_date, iteration
                )
                
                # Store tool context
                self.tracker.set_tool_context(current_tool, tool_result)
                
                # AI MESSAGE: Reflection using clean context + tool results
                reflection_result = await self._get_clean_reflection(
                    system_prompt=system_prompt,
                    tool_name=current_tool,
                    tool_result=tool_result,
                    message_history=message_history
                )
                
                if reflection_result and isinstance(reflection_result, dict):
                    reflection = reflection_result.get("reflection", "")
                    next_tool_code = reflection_result.get("next_tool_code", "")
                
                    if reflection:
                        self.tracker.add_explanation(reflection)
                        message_history.create_and_add_message(
                            content=reflection,
                            message_type=MessageType.AI,
                            agent=AgentName.CONVERSATIONAL
                        )
                        self.tracker.log_message("AI", f"REFLECTION: {reflection}")
                        self.logger.info(f"💭 Reflection captured for {current_tool}")

                        # Execute next tool code if provided
                        if next_tool_code:
                            self.logger.info(f"🔄 Executing next tool code: {next_tool_code}")
                            
                            # Execute the tool based on the code from reflection
                            try:
                                if next_tool_code == "explanatory_drivers_tool":
                                    current_tool = "explanatory_drivers_tool"
                                elif next_tool_code == "operative_data_tool":
                                    current_tool = "operative_data_tool"
                                elif next_tool_code == "ncs_tool":
                                    current_tool = "ncs_tool"
                                elif next_tool_code == "verbatims_tool":
                                    current_tool = "verbatims_tool"
                                elif next_tool_code == "routes_tool":
                                    current_tool = "routes_tool"
                                elif next_tool_code == "customer_profile_tool":
                                    current_tool = "customer_profile_tool"
                                else:
                                    self.logger.warning(f"⚠️ Unknown tool code: {next_tool_code}")
                                    # Fallback to agent decision
                                    current_tool = await self._determine_next_tool_from_reflection(
                                        reflection, current_tool, iteration, max_iterations
                                    )
                            except Exception as e:
                                self.logger.error(f"❌ Error executing tool code {next_tool_code}: {e}")
                                # Fallback to agent decision
                                current_tool = await self._determine_next_tool_from_reflection(
                                    reflection, current_tool, iteration, max_iterations
                                )
                            
                            # Execute the tool and get results
                            if current_tool:
                                self.logger.info(f"🔄 Executing tool: {current_tool}")
                                tool_result = await self._execute_tool_unified(
                                    current_tool, node_path, start_date, end_date, iteration, "comparative"
                                )
                                
                                # Store tool context
                                self.tracker.set_tool_context(current_tool, tool_result)
                                
                                # Get reflection for this tool execution
                                reflection_result = await self._get_clean_reflection(
                        system_prompt=system_prompt,
                        tool_name=current_tool,
                        tool_result=tool_result,
                                    message_history=message_history,
                                    mode="comparative"
                    )
                    
                                if reflection_result and isinstance(reflection_result, dict):
                                    reflection = reflection_result.get("reflection", "")
                                    next_tool_code = reflection_result.get("next_tool_code", "")

                    if reflection:
                        self.tracker.add_explanation(reflection)
                        message_history.create_and_add_message(
                            content=reflection,
                            message_type=MessageType.AI,
                            agent=AgentName.CONVERSATIONAL
                        )
                        self.tracker.log_message("AI", f"REFLECTION: {reflection}")
                        self.logger.info(f"💭 Reflection captured for {current_tool}")

                        # Continue with next iteration
                        continue
                    else:
                        # Let the agent decide the next tool based on reflection and helper prompts
                        current_tool = await self._determine_next_tool_from_reflection(
                            reflection, current_tool, iteration, max_iterations
                        )
                        
                        if current_tool:
                            self.logger.info(f"🔄 Agent decided next tool: {current_tool}")
                        else:
                            self.logger.info(f"✅ Agent decided to end investigation")
                            break

                else:
                    self.logger.warning(f"⚠️ No reflection captured for {current_tool}")
                    # Fallback: end investigation if no reflection
                    break

        except Exception as e:
            self.logger.error(f"❌ Error crítico en investigación comparativa: {type(e).__name__}: {e}")
            return self._build_collected_data_summary()
            
        # Final synthesis for comparative analysis
        try:
                self.logger.info("🎯 Iniciando síntesis final para análisis comparativo...")
                final_response = await self._generate_final_synthesis(
                    message_history, node_path, start_date, end_date, nps_context
                )
                
                # Export conversation log
                conversation_file = self.export_conversation(node_path=node_path, start_date=start_date, end_date=end_date)
                if conversation_file:
                    self.logger.info(f"🗂️ Conversación completa guardada: {conversation_file}")
                    
                self.logger.info("✅ Investigación comparativa completada")
                return final_response
            
        except Exception as e:
            self.logger.error(f"❌ Error crítico en investigación comparativa: {type(e).__name__}: {e}")
            return self._build_collected_data_summary()
    
    async def _execute_tool_unified(
        self, 
        tool_name: str, 
        node_path: str, 
        start_date: str, 
        end_date: str,
        iteration: int,
        mode: str = "comparative"
    ) -> str:
        """Execute a specific tool using unified mode-aware implementations"""
        try:
            if mode == "single":
                return await self._execute_tool_single_period(tool_name, node_path, start_date, end_date, iteration)
            else:
                return await self._execute_tool_comparative(tool_name, node_path, start_date, end_date, iteration)
        except Exception as e:
            self.logger.error(f"❌ Error executing unified tool {tool_name} in {mode} mode: {type(e).__name__}: {str(e)}")
            return f"ERROR executing {tool_name} in {mode} mode: {type(e).__name__}: {str(e)}"
    
    async def _execute_tool_comparative(
        self, 
        tool_name: str, 
        node_path: str, 
        start_date: str, 
        end_date: str,
        iteration: int
    ) -> str:
        """Execute a specific tool using comparative implementations"""
        try:
            if tool_name == "explanatory_drivers_tool":
                return await self._explanatory_drivers_tool(
                    node_path=node_path,
                    start_date=start_date,
                    end_date=end_date,
                    min_surveys=10
                )
            elif tool_name == "verbatims_tool":
                return await self._verbatims_tool(
                    node_path=node_path,
                    start_date=start_date,
                    end_date=end_date
                )
            elif tool_name == "ncs_tool":
                return await self._ncs_tool(
                    node_path=node_path,
                    start_date=start_date,
                    end_date=end_date
                )
            elif tool_name == "routes_tool":
                return await self._routes_tool(
                    node_path=node_path,
                    start_date=start_date,
                    end_date=end_date,
                    min_surveys=3,
                    anomaly_type=getattr(self, 'current_anomaly_type', 'unknown')
                )
            elif tool_name == "operative_data_tool":
                return await self._operative_data_tool(
                    node_path=node_path,
                    start_date=start_date,
                    end_date=end_date,
                    comparison_mode=self.detection_mode
                )
            elif tool_name == "customer_profile_tool":
                return await self._customer_profile_tool(
                    node_path=node_path,
                    start_date=start_date,
                    end_date=end_date,
                    min_surveys=3,
                    mode="comparative"
                )
            else:
                return f"Unknown tool: {tool_name}"
            
        except Exception as e:
            self.logger.error(f"❌ Error executing {tool_name}: {type(e).__name__}: {str(e)}")
            self.logger.error(f"❌ Tool parameters: node_path={node_path}, start_date={start_date}, end_date={end_date}, iteration={iteration}")
            
            # Try to extract more details from the error
            if hasattr(e, '__dict__'):
                self.logger.error(f"❌ Error details: {e.__dict__}")
            
            # Check if it's an API error
            if hasattr(e, 'response'):
                self.logger.error(f"❌ API Response: {e.response}")
            if hasattr(e, 'status_code'):
                self.logger.error(f"❌ Status Code: {e.status_code}")
            if hasattr(e, 'body'):
                self.logger.error(f"❌ Error Body: {e.body}")
                
            return f"ERROR executing {tool_name}: {type(e).__name__}: {str(e)}"
    
    async def _determine_next_tool_from_reflection(
        self, 
        reflection: str, 
        current_tool: str, 
        iteration: int, 
        max_iterations: int
    ) -> Optional[str]:
        """
        Let the agent decide the next tool based on reflection and helper prompts.
        This replaces the programmatic sequence with intelligent decision making.
        """
        try:
            self.logger.info(f"🤔 AGENT DECISION: Determining next tool after {current_tool}")
            self.logger.info(f"📊 Decision context: iteration={iteration}/{max_iterations}")
            self.logger.info(f"💭 Reflection length: {len(reflection)} chars")
            
            # Get the helper prompt for the current tool to guide the agent
            helper_prompt = self._get_helper_prompt_for_tool(current_tool)
            self.logger.info(f"🔧 Helper prompt length: {len(helper_prompt) if helper_prompt else 0} chars")
            
            # Create a prompt for the agent to decide the next tool
            decision_prompt = f"""
            Based on your reflection and the helper guidance, decide which tool to use next.
            
            CURRENT TOOL: {current_tool}
            ITERATION: {iteration}/{max_iterations}
            REFLECTION: {reflection}
            
            HELPER GUIDANCE: {helper_prompt}
            
            AVAILABLE TOOLS:
            - explanatory_drivers_tool: Analyze SHAP values and explanatory drivers
            - operative_data_tool: Analyze operational KPIs (OTP, Load Factor, etc.)
            - ncs_tool: Analyze operational incidents and NCS data
            - verbatims_tool: Analyze customer feedback and verbatims
            - routes_tool: Analyze route-specific performance
            - customer_profile_tool: Analyze customer profile impact
            
            Based on your analysis, respond with ONLY the name of the next tool to use, or 'END' if the investigation is complete.
            
            NEXT TOOL:
            """
            
            # Use the LLM to decide the next tool
            from langchain.schema import HumanMessage
            response = await self.llm([HumanMessage(content=decision_prompt)])
            next_tool = response.content.strip()
            
            self.logger.info(f"🤖 Agent response: '{next_tool}'")
            
            # Clean up the response
            if next_tool.lower() in ['end', 'none', 'complete', 'finished']:
                self.logger.info(f"✅ Agent decided to END investigation")
                return None
            
            # Validate that it's a valid tool
            valid_tools = [
                'explanatory_drivers_tool', 'operative_data_tool', 'ncs_tool',
                'verbatims_tool', 'routes_tool', 'customer_profile_tool'
            ]
            
            if next_tool in valid_tools:
                self.logger.info(f"✅ Agent decided next tool: {next_tool}")
                return next_tool
            else:
                self.logger.warning(f"⚠️ Agent suggested invalid tool: '{next_tool}', ending investigation")
                self.logger.warning(f"⚠️ Valid tools are: {valid_tools}")
                return None
                
        except Exception as e:
            self.logger.error(f"❌ Error determining next tool: {e}")
            # Fallback: end investigation
            return None
    
    def _get_helper_prompt_for_tool(self, tool_name: str) -> str:
        """
        Get the helper prompt for a specific tool from the YAML configuration.
        The agent will determine the flow type through its analysis and use the appropriate prompt.
        """
        try:
            # Get the tools_prompts from the configuration
            tools_prompts = self.config.get('tools_prompts', {})
            
            if tool_name in tools_prompts:
                tool_config = tools_prompts[tool_name]
                
                # For comparative mode, return the appropriate flow-specific prompt
                # The agent will use its intelligence to determine which flow to follow
                if 'comparative' in tool_config:
                    comparative_prompts = tool_config['comparative']
                    
                    # If it's a dictionary with flow-specific prompts, provide all options
                    # The agent will analyze and choose the appropriate flow
                    if isinstance(comparative_prompts, dict):
                        # For explanatory_drivers_tool, provide all flow options
                        # The agent will analyze the drivers SHAP and choose the appropriate flow
                        if tool_name == 'explanatory_drivers_tool':
                            flow_options = []
                            if 'operative' in comparative_prompts:
                                flow_options.append("OPERATIVE FLOW: " + comparative_prompts['operative'])
                            if 'product' in comparative_prompts:
                                flow_options.append("PRODUCT FLOW: " + comparative_prompts['product'])
                            if 'mixed' in comparative_prompts:
                                flow_options.append("MIXED FLOW: " + comparative_prompts['mixed'])
                            
                            if flow_options:
                                return "\n\n".join(flow_options)
                            else:
                                return str(comparative_prompts)
                        
                        # For other tools, provide the operative prompt as default
                        # The agent will follow the flow based on its previous analysis
                        if 'operative' in comparative_prompts:
                            return comparative_prompts['operative']
                        elif 'mixed' in comparative_prompts:
                            return comparative_prompts['mixed']
                        else:
                            return str(comparative_prompts)
                    else:
                        # If it's a string, return it directly
                        return comparative_prompts
                        
                elif 'single' in tool_config:
                    return tool_config['single']
                else:
                    return tool_config.get('default', 'No specific guidance available.')
            else:
                return f"No helper prompt found for {tool_name}"
                
        except Exception as e:
            self.logger.error(f"❌ Error getting helper prompt for {tool_name}: {e}")
            return "Error retrieving helper guidance."
    
    async def _operative_data_tool(self, node_path: str, start_date, end_date, comparison_days: int = 7, comparison_mode: str = "mean") -> str:
        """
        Tool for analyzing operational metrics using parametrized comparison logic.
        
        This uses the enhanced OperationalDataAnalyzer with configurable comparison modes:
        - 'vslast': Compare against the previous period 
        - 'mean': Compare against 7-day rolling average (default/legacy)
        - 'target': Compare against target values (future implementation)
        
        Args:
            node_path: Node path for analysis
            start_date: Start date for analysis period (str or datetime)
            end_date: End date for analysis period/target_date (str or datetime)
            comparison_days: Number of days for data collection (default: 7)
            comparison_mode: Comparison mode - "vslast", "mean", or "target" (default: "mean")
        """
        try:
            self.logger.info(f"Collecting operational data for {node_path} on {end_date} with {comparison_days}-day window, comparison_mode={comparison_mode}")
            
            # Handle both string and datetime inputs
            if isinstance(start_date, str):
                start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            else:
                start_dt = start_date
                
            if isinstance(end_date, str):
                target_dt = datetime.strptime(end_date, '%Y-%m-%d')
            else:
                target_dt = end_date
            
            # Import the operational analyzer here to avoid circular imports
            from ....anomaly_explanation.data_analyzer import OperationalDataAnalyzer
            
            # Initialize the operational analyzer with specified comparison mode
            operational_analyzer = OperationalDataAnalyzer(comparison_mode=comparison_mode)
            
            # For vslast mode, we need data for BOTH current and previous periods
            # So we need to collect more days to ensure we have both periods
            if comparison_mode == "vslast":
                # For vslast we need current period + previous period data
                # If we're doing 7-day analysis, we need 14 days total (7 + 7)
                extended_days = comparison_days * 2
                self.logger.info(f"VSLAST mode: collecting {extended_days} days to cover both periods")
            else:
                # For mean mode, keep the original logic
                extended_days = comparison_days
            
            # Collect operational data directly from PBI with extended days for vslast
            operational_data = await self.pbi_collector.collect_operative_data_for_date(
                node_path, target_dt, extended_days
            )
            
            if operational_data.empty:
                return f"No operational data available for {end_date}"
            
            # Clean the operational data by replacing empty strings with NaN for numeric columns
            cleaned_data = operational_data.copy()
            numeric_columns = ['Load_Factor', 'OTP15_adjusted', 'Misconex', 'Mishandling']
            for col in numeric_columns:
                if col in cleaned_data.columns:
                    # Replace empty strings with NaN, then convert to numeric
                    cleaned_data[col] = cleaned_data[col].replace('', pd.NA)
                    cleaned_data[col] = pd.to_numeric(cleaned_data[col], errors='coerce')
            
            # Convert date columns if this is flexible aggregated data (to match load_operative_data logic)
            if 'Min_Date' in cleaned_data.columns and 'Max_Date' in cleaned_data.columns:
                # Ensure date columns are datetime.date objects for proper comparison
                cleaned_data['Min_Date'] = pd.to_datetime(cleaned_data['Min_Date']).dt.date
                cleaned_data['Max_Date'] = pd.to_datetime(cleaned_data['Max_Date']).dt.date
                self.logger.info(f"🗓️ Converted date columns to datetime.date for flexible comparison compatibility")
            
            # Set the cleaned operational data directly in the analyzer
            operational_analyzer.operative_data[node_path] = cleaned_data
            
            # Get the enhanced specific explanations (OTP and Load Factor)
            target_date_str = target_dt.strftime('%Y-%m-%d')
            # Use the stored anomaly type instead of "unknown"
            anomaly_type_for_analysis = getattr(self, 'current_anomaly_type', 'unknown')
            
            # Calculate aggregation_days from date range
            aggregation_days = (target_dt - start_dt).days + 1
            self.logger.info(f"📅 Operative date filter: {start_dt.strftime('%Y-%m-%d')} to {target_dt.strftime('%Y-%m-%d')} ({aggregation_days} days for anomaly comparison)")
            
            specific_explanations = operational_analyzer.get_specific_explanations(
                node_path, target_date_str, anomaly_type_for_analysis, aggregation_days
            )
            
            # Get the comprehensive analysis
            analysis = operational_analyzer.analyze_operative_metrics(node_path, target_date_str)
            
            if "error" in analysis:
                return f"Operational analysis error: {analysis['error']}"
            
            # Build enhanced explanation using the parametrized logic
            operative_parts = []
            
            # Add comparison mode info
            comparison_info = f"📊 **OPERATIVE ANALYSIS** (Comparison: {comparison_mode.upper()})"
            if comparison_mode == "vslast":
                comparison_date = analysis.get("comparison_date", "unknown")
                comparison_info += f" vs {comparison_date}"
            elif comparison_mode == "mean":
                comparison_days_used = analysis.get("comparison_days", comparison_days)
                comparison_info += f" vs {comparison_days_used}-day average"
            
            operative_parts.append(comparison_info)
            operative_parts.append("")
            
            # Show all metrics with changes vs previous period
            metrics = analysis.get("metrics", {})
            if metrics:
                operative_parts.append(f"📊 **Métricas Operativas vs Período Anterior**:")
                
                for metric, data in metrics.items():
                    # Skip metrics with no real data (all zeros or identical values)
                    current_val = data.get('current_value', data.get('current', 0))
                    previous_val = data.get('previous_value', data.get('previous', 0))
                    
                    # Skip Mishandling if both current and previous are 0 (no data for this segment)
                    if metric == 'Mishandling' and current_val == 0 and previous_val == 0:
                        continue
                        
                    direction = "↗️" if data['direction'] == 'higher' else "↘️"
                    
                    if comparison_mode == "vslast":
                        delta = data.get('delta', data.get('difference', 0))
                        change_pct = data.get('change_pct', 0)
                        
                        # Determine if change supports or contradicts NPS anomaly
                        correlation_status = "❓"
                        if anomaly_type_for_analysis.lower() == 'negative':
                            if metric in ['OTP15_adjusted']:  # Direct correlation
                                correlation_status = "✅ Explica NPS↓" if delta < 0 else "❌ Contradice NPS↓"
                            elif metric in ['Load_Factor', 'Misconex', 'Mishandling']:  # Inverse correlation
                                correlation_status = "✅ Explica NPS↓" if delta > 0 else "❌ Contradice NPS↓"
                        elif anomaly_type_for_analysis.lower() == 'positive':
                            if metric in ['OTP15_adjusted']:  # Direct correlation
                                correlation_status = "✅ Explica NPS↑" if delta > 0 else "❌ Contradice NPS↑"
                            elif metric in ['Load_Factor', 'Misconex', 'Mishandling']:  # Inverse correlation
                                correlation_status = "✅ Explica NPS↑" if delta < 0 else "❌ Contradice NPS↑"
                        
                        metric_display = metric.replace('_', ' ').replace('adjusted', '').title()
                        operative_parts.append(f"   • **{metric_display}**: {current_val} vs {previous_val} ({direction}{abs(delta):.1f}, {change_pct:+.1f}%) {correlation_status}")
                    else:
                        baseline_value = data.get('week_average', data.get('previous_value', 'N/A'))
                        day_val = data.get('day_value', data.get('current_value', 'N/A'))
                        metric_display = metric.replace('_', ' ').title()
                        operative_parts.append(f"   • **{metric_display}**: {day_val} vs {baseline_value} (referencia)")
            
            # Add correlation summary
            operative_parts.append("")
            correlation_summary = self._generate_correlation_summary(metrics, anomaly_type_for_analysis, comparison_mode)
            operative_parts.append(correlation_summary)
            
            return "\n".join(operative_parts)
            
        except Exception as e:
            self.logger.error(f"Error in operative data tool: {e}")
            return f"Error analyzing operational data: {str(e)}"
    
    def _get_metric_impact_summary(self, metric: str, direction: str) -> str:
        """Get short impact summary for a metric"""
        impact_map = {
            'Misconex': {
                'higher': 'more connection issues',
                'lower': 'fewer connection issues'
            },
            'Mishandling': {
                'higher': 'more baggage problems',  
                'lower': 'fewer baggage problems'
            }
        }
        return impact_map.get(metric, {}).get(direction, 'operational change')
    
    def _generate_correlation_summary(self, metrics: dict, anomaly_type: str, comparison_mode: str) -> str:
        """Generate correlation summary between operative metrics and NPS anomaly"""
        if not metrics:
            return "🤔 **Correlation**: No significant operational changes detected"
        
        supporting_metrics = []
        contradicting_metrics = []
        
        for metric, data in metrics.items():
            if data.get('is_significant', False):
                # Check if metric change supports the NPS anomaly
                if self._metric_supports_anomaly(metric, data['direction'], anomaly_type):
                    supporting_metrics.append(metric.replace('_', ' ').title())
                else:
                    contradicting_metrics.append(metric.replace('_', ' ').title())
        
        if supporting_metrics and not contradicting_metrics:
            return f"✅ **Correlation**: Strong operational explanation - {', '.join(supporting_metrics)} changes explain the {anomaly_type} NPS anomaly"
        elif supporting_metrics and contradicting_metrics:
            return f"🤔 **Correlation**: Mixed signals - {', '.join(supporting_metrics)} support the anomaly, but {', '.join(contradicting_metrics)} show contradictory patterns"
        elif contradicting_metrics:
            return f"❌ **Correlation**: Operational metrics ({', '.join(contradicting_metrics)}) contradict the {anomaly_type} NPS anomaly - other causes likely"
        else:
            return f"🔍 **Correlation**: No significant operational changes detected using {comparison_mode} comparison"
    
    def _metric_supports_anomaly(self, metric: str, direction: str, nps_anomaly_type: str) -> bool:
        """Determine if a metric deviation supports the observed NPS anomaly"""
        
        # For negative NPS anomalies, these directions support the anomaly
        negative_supporting = {
            'Load_Factor': 'higher',      # Higher LF = worse service
            'OTP15_adjusted': 'lower',    # Lower OTP = worse experience  
            'Misconex': 'higher',         # Higher misconex = worse experience
            'Mishandling': 'higher'       # Higher mishandling = worse experience
        }
        
        # For positive NPS anomalies, opposite directions support
        positive_supporting = {
            'Load_Factor': 'lower',       # Lower LF = better service
            'OTP15_adjusted': 'higher',   # Higher OTP = better experience
            'Misconex': 'lower',          # Lower misconex = better experience  
            'Mishandling': 'lower'        # Lower mishandling = better experience
        }
        
        if nps_anomaly_type == "negative":
            return negative_supporting.get(metric) == direction
        elif nps_anomaly_type == "positive":
            return positive_supporting.get(metric) == direction
        else:
            return False
    
    async def _verbatims_tool(self, node_path: str, start_date: str, end_date: str) -> str:
        """
        Enhanced verbatims tool that uses strategic multi-round chatbot conversation
        for comprehensive customer feedback analysis with cross-validation.
        """
        try:
            self.logger.info(f"🤖 VERBATIMS_TOOL CALLED - Enhanced Strategic Analysis")
            self.logger.debug(f"📋 Parameters: node_path={node_path}, start_date={start_date}, end_date={end_date}")
            
            # Determine verbatim type based on explanatory drivers context
            verbatim_type = self._determine_verbatim_type_from_context()
            self.logger.info(f"🎯 Determined verbatim type: {verbatim_type}")
            
            # Try strategic chatbot conversation first if available
            if self.chatbot_collector:
                self.logger.info(f"🤖 Attempting strategic chatbot conversation...")
                
                # Test connection
                connection_success, connection_message = self.chatbot_collector.test_connection()
                self.logger.info(f"🔍 Connection: {connection_message}")
                
                if connection_success:
                    # Conduct comprehensive strategic conversation
                    conversation = await self._conduct_chatbot_conversation(
                        verbatim_type, node_path, start_date, end_date
                    )
                    
                    if conversation:
                        # Synthesize conversation results
                        result = self._synthesize_conversation_results(
                            conversation, verbatim_type, node_path, start_date, end_date
                        )
                        
                        # Store comprehensive conversation data
                        self.collected_data['verbatims'] = result
                        self.logger.info("✅ Strategic chatbot conversation completed successfully")
                        return result
                    else:
                        self.logger.warning("🔄 Chatbot conversation failed, fallback to simple analysis...")
                else:
                    self.logger.warning("🔄 Chatbot connection failed, attempting fallback...")
            else:
                self.logger.warning(f"⚠️ Chatbot collector not available - using fallback methods")
            
            # Fallback to simple chatbot analysis if conversation failed
            if self.chatbot_collector:
                try:
                    self.logger.info(f"🤖 Attempting simple chatbot analysis as fallback...")
                    df = self.chatbot_collector.get_verbatims_data(
                        start_date=start_date, 
                        end_date=end_date, 
                        node_path=node_path,
                        verbatim_type=verbatim_type
                    )
                    
                    if not df.empty:
                        result = self._analyze_chatbot_verbatims(df, node_path, start_date, end_date, verbatim_type)
                        self.collected_data['verbatims'] = result
                        self.logger.info("✅ Simple chatbot analysis completed")
                        return result
                except Exception as e:
                    self.logger.warning(f"🔄 Simple chatbot analysis failed: {e}, falling back to PBI...")
            
            # Final fallback to PBI collector
            self.logger.info(f"📊 Using PBI verbatims collection as final fallback...")
            
            # Convert string dates to datetime for PBI
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
            
            # collect_verbatims_for_date_range is NOT async
            df = self.pbi_collector.collect_verbatims_for_date_range(node_path, start_dt, end_dt)
            
            if df.empty:
                return f"📝 No information available from verbatims tool for {node_path} in date range {start_date} to {end_date}"
            
            # Enhanced PBI analysis
            result = self._analyze_pbi_verbatims(df, node_path, start_date, end_date)
            self.collected_data['verbatims'] = result
            self.logger.info("✅ PBI verbatims analysis completed as fallback")
            return result
            
        except Exception as e:
            self.logger.error(f"💥 Error in verbatims analysis: {str(e)}")
            return f"Error in verbatims analysis: {str(e)}"
    
    async def _verbatims_tool_single_period(self, node_path: str, start_date: str, end_date: str) -> str:
        """
        Single period verbatims tool that analyzes customer feedback for a specific period
        without comparison to other periods.
        """
        try:
            self.logger.info(f"🤖 VERBATIMS_TOOL SINGLE PERIOD CALLED")
            self.logger.debug(f"📋 Parameters: node_path={node_path}, start_date={start_date}, end_date={end_date}")
            
            # Try chatbot analysis for single period
            if self.chatbot_collector:
                self.logger.info(f"🤖 Attempting chatbot analysis for single period...")
                
                # Test connection
                connection_success, connection_message = self.chatbot_collector.test_connection()
                self.logger.info(f"🔍 Connection: {connection_message}")
                
                if connection_success:
                    try:
                        # Get verbatims data for the specific period
                        df = self.chatbot_collector.get_verbatims_data(
                            start_date=start_date, 
                            end_date=end_date, 
                            node_path=node_path
                        )
                        
                        if df is not None and len(df) > 0:
                            self.logger.info(f"📊 Retrieved {len(df)} verbatims for single period analysis")
                            
                            # Analyze verbatims for the specific period only
                            result = await self._analyze_verbatims_single_period(df, node_path, start_date, end_date)
                            
                            # Store data
                            self.collected_data['verbatims'] = result
                            self.logger.info("✅ Single period verbatims analysis completed successfully")
                            return result
                        else:
                            self.logger.warning(f"📊 No verbatims data found for {node_path} in period {start_date} to {end_date}")
                            return f"📝 No customer feedback available for {node_path} during {start_date} to {end_date}"
                            
                    except Exception as e:
                        self.logger.error(f"💥 Error in chatbot analysis: {str(e)}")
                        return f"Error analyzing customer feedback: {str(e)}"
                else:
                    self.logger.warning("🔄 Chatbot connection failed")
                    return f"❌ Unable to connect to customer feedback system for {node_path}"
            else:
                self.logger.warning(f"⚠️ Chatbot collector not available")
                return f"📝 Customer feedback analysis not available for {node_path} during {start_date} to {end_date}"
            
        except Exception as e:
            self.logger.error(f"💥 Error in single period verbatims analysis: {str(e)}")
            return f"Error in single period verbatims analysis: {str(e)}"
    
    async def _analyze_verbatims_single_period(self, df: pd.DataFrame, node_path: str, start_date: str, end_date: str) -> str:
        """Analyze verbatims for a single period without comparison"""
        try:
            # Simple analysis focused on period-specific themes
            total_verbatims = len(df)
            
            # Get basic sentiment/theme analysis
            if hasattr(df, 'sentiment') and 'sentiment' in df.columns:
                sentiment_counts = df['sentiment'].value_counts()
                sentiment_summary = ", ".join([f"{sentiment}: {count}" for sentiment, count in sentiment_counts.head(3).items()])
            else:
                sentiment_summary = "Sentiment data not available"
            
            # Sample of verbatims
            sample_verbatims = df.head(5)['feedback_text'].tolist() if 'feedback_text' in df.columns else ["No feedback text available"]
            
            result = f"""📝 **ANÁLISIS DE VERBATIMS - PERÍODO ÚNICO**

**Período Analizado:** {start_date} a {end_date}
**Segmento:** {node_path}
**Total de comentarios:** {total_verbatims}

**Distribución de sentimientos:**
{sentiment_summary}

**Temas principales identificados durante el período:**
{sample_verbatims[:3]}

**Resumen:** Durante el período {start_date} a {end_date}, se identificaron {total_verbatims} comentarios de clientes para {node_path}. Los principales temas mencionados proporcionan contexto sobre la experiencia del cliente durante este período específico.
"""
            
            return result
            
        except Exception as e:
            self.logger.error(f"💥 Error analyzing single period verbatims: {str(e)}")
            return f"Error analyzing verbatims for period: {str(e)}"
    
    def _determine_verbatim_type_from_context(self) -> str:
        """Determine verbatim type based on explanatory drivers context."""
        explanatory_data = self.collected_data.get('explanatory_drivers', '')
        explanatory_str = str(explanatory_data).lower()
        
        # Simple mapping
        if 'boarding' in explanatory_str:
            return 'boarding'
        elif 'crew' in explanatory_str:
            return 'crew'
        elif 'food' in explanatory_str or 'f&b' in explanatory_str:
            return 'food'
        elif 'checkin' in explanatory_str or 'check-in' in explanatory_str:
            return 'checkin'
        else:
            return 'nps'  # default

    async def _conduct_chatbot_conversation(self, verbatim_type: str, node_path: str, start_date: str, end_date: str) -> List[Dict]:
        """
        Conduct a focused 2-question conversation with the chatbot to identify problematic routes and representative comments.
        
        Question 1: Which routes have the most negative comments?
        Question 2: What are the most representative comments for each of those routes?
        """
        conversation = []
        
        try:
            if not self.chatbot_collector:
                self.logger.error("❌ Chatbot collector no disponible para conversación")
                return []
            
            # PREGUNTA 1: Rutas con comentarios más negativos
            query_1 = self._generate_negative_routes_query(node_path)
            self.logger.info(f"💬 PREGUNTA 1 (Rutas más negativas): '{query_1}'")
            
            df_1 = self.chatbot_collector.get_verbatims_data(
                start_date=start_date, end_date=end_date, node_path=node_path,
                verbatim_type="routes_negative", intelligent_query=query_1
            )
            
            response_1 = self._analyze_single_chatbot_response(df_1, "rutas_negativas")
            self.logger.info(f"🤖 RESPUESTA 1: {response_1}")
            
            conversation.append({
                "round": 1,
                "question": query_1,
                "response": response_1,
                "data_points": len(df_1),
                "purpose": "rutas_negativas"
            })
            
            # PREGUNTA 2: Comentarios representativos de cada ruta
            query_2 = self._generate_representative_comments_query(node_path, response_1)
            self.logger.info(f"💬 PREGUNTA 2 (Comentarios representativos): '{query_2}'")
            
            df_2 = self.chatbot_collector.get_verbatims_data(
                start_date=start_date, end_date=end_date, node_path=node_path,
                verbatim_type="representative_comments", intelligent_query=query_2
            )
            
            response_2 = self._analyze_single_chatbot_response(df_2, "comentarios_representativos")
            self.logger.info(f"🤖 RESPUESTA 2: {response_2}")
            
            conversation.append({
                "round": 2,
                "question": query_2,
                "response": response_2,
                "data_points": len(df_2),
                "purpose": "comentarios_representativos"
            })
            
            return conversation
            
        except Exception as e:
            self.logger.error(f"❌ Error en conversación chatbot: {e}")
            return []
    
    def _generate_negative_routes_query(self, node_path: str) -> str:
        """Generate query to identify routes with the most negative comments."""
        return f"¿Cuáles son las rutas específicas (origen-destino) dentro de {node_path} que tienen los comentarios más negativos durante este período? Ordénalas por negatividad y frecuencia de quejas. Incluye los códigos de aeropuerto (ej: MAD-BCN, LHR-MAD) y el número aproximado de comentarios negativos por ruta."
    
    def _generate_representative_comments_query(self, node_path: str, previous_response: str) -> str:
        """Generate query to get representative comments for each problematic route."""
        return f"Para cada una de las rutas más problemáticas identificadas en la respuesta anterior, ¿puedes mostrarme 2-3 comentarios representativos reales de clientes que ejemplifiquen los problemas específicos de cada ruta? Organiza los comentarios por ruta (ej: MAD-BCN: 'comentario1', 'comentario2'; LHR-MAD: 'comentario1', 'comentario2') y asegúrate de que sean verbatims auténticos que reflejen los problemas más comunes."
    
    def _generate_operational_correlation_query(self, node_path: str, response_1: str, response_2: str) -> str:
        """Generate a query to correlate customer feedback with operational data."""
        operative_data = str(self.collected_data.get('operative_data', ''))
        
        # Extract operational issues
        operational_problems = []
        if 'otp' in operative_data.lower() and 'worsened' in operative_data.lower():
            operational_problems.append("deterioro significativo en puntualidad (OTP)")
        if 'mishandling' in operative_data.lower():
            operational_problems.append("problemas de manejo de equipaje")
        if 'delay' in operative_data.lower() or 'retrasos' in operative_data.lower():
            operational_problems.append("retrasos operacionales")
        
        problems_text = " y ".join(operational_problems) if operational_problems else "problemas operacionales detectados"
        
        return f"Los datos operacionales muestran {problems_text} en {node_path} durante este período. ¿Están los clientes mencionando específicamente estos problemas operacionales en sus comentarios? ¿Cómo describen el impacto de estos problemas en su experiencia de viaje?"
    
    def _generate_route_specific_query(self, node_path: str, response_1: str, response_2: str, response_3: str) -> str:
        """Generate a query to identify route-specific concentrations of problems."""
        
        # Analyze previous responses to identify key issues
        combined_responses = f"{response_1} {response_2} {response_3}".lower()
        
        route_focus = ""
        if "madrid" in combined_responses or "mad" in combined_responses:
            route_focus = "especialmente en rutas que conectan con Madrid"
        elif "barcelona" in combined_responses or "bcn" in combined_responses:
            route_focus = "especialmente en rutas que conectan con Barcelona"
        elif "london" in combined_responses or "lhr" in combined_responses:
            route_focus = "especialmente en rutas hacia/desde Londres"
        elif any(keyword in combined_responses for keyword in ["european", "europa", "continental"]):
            route_focus = "especialmente en rutas europeas"
        else:
            route_focus = "en rutas específicas"
        
        return f"Basándome en los problemas identificados en {node_path}, ¿puedes identificar si hay rutas específicas donde se concentran más las quejas de clientes? ¿Los verbatims mencionan destinos, aeropuertos, o rutas particulares {route_focus} donde los problemas son más frecuentes o severos?"
    
    def _generate_synthesis_additional_causes_query(self, node_path: str, response_1: str, response_2: str, response_3: str, response_4: str) -> str:
        """Generate a synthesis query to uncover hidden causes and complete the analysis."""
        
        # Extract cabin type from node_path dynamically
        cabin_type = "clientes"  # default
        if "/Economy" in node_path:
            cabin_type = "clientes de Economy Class"
        elif "/Business" in node_path:
            cabin_type = "clientes de Business Class"
        elif "/Premium" in node_path:
            cabin_type = "clientes de Premium Class"
        
        return f"Para completar el análisis de {node_path}, ¿existen causas subyacentes o factores sorprendentes que los clientes mencionan y que podrían no haber sido capturados en las preguntas anteriores? ¿Hay patrones estacionales, problemas de comunicación, expectativas no cumplidas, o aspectos específicos de la experiencia que los {cabin_type} mencionan como problemáticos? Busca insights únicos que no sean obvios en las métricas tradicionales."
    
    def _analyze_single_chatbot_response(self, df: pd.DataFrame, purpose: str) -> str:
        """Analyze a single chatbot analysis response focusing on the conversation context."""
        if df.empty:
            return f"No se obtuvo análisis del chatbot para {purpose}"
        
        # El chatbot devuelve análisis, no verbatims individuales
        if 'chatbot_analysis' in df.columns and not df['chatbot_analysis'].empty:
            analysis_text = df['chatbot_analysis'].iloc[0]
            data_points = len(df)
            
            # Extract key insights from the analysis
            analysis_summary = f"Análisis del chatbot: {analysis_text}"
            
            return analysis_summary
        elif 'verbatim_text' in df.columns and not df['verbatim_text'].empty:
            # Fallback for old format - deprecated
            total_comments = len(df)
            sample_feedback = df['verbatim_text'].iloc[0][:100] + "..."
            return f"{total_comments} comentarios analizados. Ejemplo: '{sample_feedback}'"
        else:
            return f"Respuesta del chatbot recibida pero sin contenido analizable para {purpose}"
    
    def _synthesize_conversation_results(self, conversation: List[Dict], verbatim_type: str, node_path: str, start_date: str, end_date: str) -> str:
        """Synthesize the multi-round strategic conversation into a comprehensive analysis."""
        
        if not conversation:
            return "❌ No se pudo establecer conversación con el chatbot de verbatims"
        
        # Build comprehensive response
        result_parts = []
        
        # Header
        total_data_points = sum(exchange.get('data_points', 0) for exchange in conversation)
        result_parts.append(f"🤖 CONVERSACIÓN ESTRATÉGICA COMPLETADA: {len(conversation)} rondas analizando {total_data_points} verbatims en {node_path}")
        
        # Conversation flow with better emojis
        result_parts.append("📋 FLUJO CONVERSACIONAL ESTRATÉGICO:")
        purpose_emojis = {
            "exploración_abierta": "🔍", 
            "validación_cruzada": "🔄", 
            "correlación_operacional": "⚙️",
            "rutas_específicas": "🛫",
            "síntesis_causas_ocultas": "🎯"
        }
        
        for exchange in conversation:
            emoji = purpose_emojis.get(exchange['purpose'], "💬")
            result_parts.append(f"   {emoji} Ronda {exchange['round']} ({exchange['purpose']}): {exchange['data_points']} verbatims")
            result_parts.append(f"      Pregunta: {exchange['question']}")
            result_parts.append(f"      Respuesta: {exchange['response']}")
        
        # Enhanced synthesis based on strategic conversation
        result_parts.append("🔗 SÍNTESIS ESTRATÉGICA:")
        
        # Cross-validation status
        responses_text = " ".join([ex['response'] for ex in conversation])
        if "negativ" in responses_text.lower():
            result_parts.append("   ✅ VALIDACIÓN CRUZADA EXITOSA: Los verbatims confirman los problemas identificados en explanatory drivers y datos operacionales")
        elif "positiv" in responses_text.lower():
            result_parts.append("   ⚠️ VALIDACIÓN PARCIAL: Los verbatims muestran perspectivas mixtas, requiere análisis más profundo")
        else:
            result_parts.append("   🤔 VALIDACIÓN INCONCLUSA: Los verbatims proporcionan información compleja que requiere investigación adicional")
        
        # Strategic insights from conversation (full responses)
        result_parts.append("💡 INSIGHTS ESTRATÉGICOS COMPLETOS:")
        if len(conversation) >= 1:
            result_parts.append(f"   • Exploración abierta: {conversation[0]['response']}")
        if len(conversation) >= 2:
            result_parts.append(f"   • Validación cruzada: {conversation[1]['response']}")
        if len(conversation) >= 3:
            result_parts.append(f"   • Correlación operacional: {conversation[2]['response']}")
        if len(conversation) >= 4:
            result_parts.append(f"   • Rutas específicas: {conversation[3]['response']}")
        if len(conversation) >= 5:
            result_parts.append(f"   • Causas ocultas: {conversation[4]['response']}")
        
        # Store enhanced conversation data
        self.collected_data['verbatims_conversation'] = {
            'source': 'strategic_chatbot_conversation',
            'strategy': 'cross_validation_exploration',
            'verbatim_type': verbatim_type,
            'total_exchanges': len(conversation),
            'total_data_points': total_data_points,
            'conversation_log': conversation,
            'date_range': f"{start_date} to {end_date}",
            'node_path': node_path,
            'synthesis_summary': " | ".join(result_parts)
        }
        
        return " | ".join(result_parts)
    
    def _analyze_chatbot_verbatims(self, df: pd.DataFrame, node_path: str, start_date: str, end_date: str, verbatim_type: str) -> str:
        """Analyze chatbot analysis responses with enhanced conversational structure."""
        total_analyses = len(df)
        analysis_result = []
        
        # Get the intelligent query that was used
        explanatory_context = self.collected_data.get('explanatory_drivers', '')
        operative_context = self.collected_data.get('operative_data', '')
        
        # Header with conversational context
        if not df.empty and 'is_sample' in df.columns:
            is_sample = df['is_sample'].iloc[0] if not df['is_sample'].empty else False
        else:
            is_sample = False
        source_info = "🤖 CHATBOT ANÁLISIS COMPLETADO"
        if is_sample:
            source_info += " (datos de ejemplo - desarrollo en progreso)"
        
        analysis_result.append(f"{source_info}: {total_analyses} análisis sobre {verbatim_type.upper()} en {node_path}")
        
        # Conversational context linking to previous findings
        if explanatory_context and operative_context:
            analysis_result.append(f"🔗 CONEXIÓN CON HALLAZGOS: Validando con el análisis del chatbot los problemas operacionales detectados")
        
        # Process chatbot analysis content
        if 'chatbot_analysis' in df.columns and not df['chatbot_analysis'].empty:
            analysis_text = df['chatbot_analysis'].iloc[0]
            analysis_result.append(f"💡 ANÁLISIS DEL CHATBOT: {analysis_text}")
            
            # Extract insights from analysis text
            if 'problem' in analysis_text.lower() or 'issue' in analysis_text.lower() or 'problema' in analysis_text.lower():
                analysis_result.append("🚨 FINDING: El chatbot identifica problemas en los verbatims - confirma hipótesis negativas")
            elif 'positive' in analysis_text.lower() or 'good' in analysis_text.lower() or 'excellent' in analysis_text.lower():
                analysis_result.append("✅ FINDING: El chatbot identifica aspectos positivos - respalda service excellence")
        
        # Field-specific analysis
        if 'field_name' in df.columns:
            field_info = df['field_name'].iloc[0] if not df['field_name'].empty else verbatim_type
            analysis_result.append(f"📊 Campo analizado: {field_info}")
        
        # Analysis type and source
        if 'analysis_type' in df.columns:
            analysis_type = df['analysis_type'].iloc[0] if not df['analysis_type'].empty else 'verbatim_summary'
            analysis_result.append(f"🔍 Tipo de análisis: {analysis_type}")
        
        result = " | ".join(analysis_result)
        
        # Store collected data with enhanced metadata
        self.collected_data['verbatims_data'] = {
            'source': 'chatbot_api',
            'verbatim_type': verbatim_type,
            'is_sample': is_sample,
            'analysis_summary': result,
            'total_analyses': total_analyses,
            'chatbot_analysis_content': df['chatbot_analysis'].iloc[0] if 'chatbot_analysis' in df.columns and not df['chatbot_analysis'].empty else None,
            'date_range': f"{start_date} to {end_date}",
            'node_path': node_path
        }
        
        return result
    
    def _analyze_pbi_verbatims(self, df: pd.DataFrame, node_path: str, start_date: str, end_date: str) -> str:
        """Analyze verbatims from PBI (fallback method) - original logic."""
        total_verbatims = len(df)
        analysis_result = []
        analysis_result.append(f"📊 PBI FALLBACK - Verbatims Analysis: {total_verbatims} customer comments")
        
        # Original PBI sentiment analysis
        if 'verbatims_sentiment[sentiment]' in df.columns:
            sentiment_counts = df['verbatims_sentiment[sentiment]'].value_counts()
            negative_count = int(sentiment_counts.get('Negative', 0) or 0)
            positive_count = int(sentiment_counts.get('Positive', 0) or 0)
            neutral_count = int(sentiment_counts.get('Neutral', 0) or 0)
            
            sentiment_summary = f"Sentiment: Positive({positive_count}) Negative({negative_count}) Neutral({neutral_count})"
            analysis_result.append(sentiment_summary)
            
            # Determine dominant sentiment
            if negative_count > positive_count and negative_count > neutral_count:
                analysis_result.append("FINDING: Predominantly NEGATIVE sentiment - indicates customer dissatisfaction")
            elif positive_count > negative_count and positive_count > neutral_count:
                analysis_result.append("FINDING: Predominantly POSITIVE sentiment - supports positive anomaly")
        
        # Original PBI topic analysis
        if 'verbatims_sentiment[topic]' in df.columns:
            topic_counts = df['verbatims_sentiment[topic]'].value_counts()
            if not topic_counts.empty:
                top_topics = topic_counts.head(3)
                topics_summary = ", ".join([f"{topic}({count})" for topic, count in top_topics.items()])
                analysis_result.append(f"Top Issues: {topics_summary}")
        
        result = " | ".join(analysis_result)
        
        # Store collected data
        self.collected_data['verbatims_data'] = {
            'source': 'pbi_fallback',
            'analysis_summary': result,
            'total_verbatims': total_verbatims,
            'date_range': f"{start_date} to {end_date}",
            'node_path': node_path
        }
        
        return result
    
    async def _ncs_tool(self, node_path: str, start_date: str, end_date: str, analysis_focus: str = "flights", temporal_comparison: bool = True) -> str:
        """
        Enhanced NCS tool for causal analysis that extracts:
        1. DISRUPTION CAUSES: Identifies root causes from incident patterns
        2. AFFECTED ROUTES: Maps specific routes impacted by incidents
        3. TEMPORAL COMPARISON: Compares current period vs previous period (NEW)
        
        For multi-day analysis (aggregation-days > 1), processes each day individually
        and consolidates results for comprehensive period analysis.
        
        Args:
            temporal_comparison: If True, compares current period with previous period of same length
        """
        try:
            print(f"🔧 DEBUG: NCS tool called for {node_path} from {start_date} to {end_date}")
            print(f"🔧 DEBUG: Temporal comparison: {'ENABLED' if temporal_comparison else 'DISABLED'}")
            self.logger.info(f"Collecting NCS operational incidents for {node_path} from {start_date} to {end_date}")
            
            # Convert string dates to datetime
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
            
            # Calculate number of days in the range
            total_days = (end_dt - start_dt).days + 1
            print(f"📅 DEBUG: Processing {total_days} days of NCS data (from {start_date} to {end_date})")
            
            # Import NCS collector
            from ....data_collection.ncs_collector import NCSDataCollector
            
            # Initialize NCS collector with temp credentials
            temp_creds_file = "dashboard_analyzer/temp_aws_credentials.env"
            ncs_collector = NCSDataCollector(temp_env_file=temp_creds_file)
            
            # Calculate comparison period dates if temporal comparison is enabled
            comparison_data = None
            comparison_start_dt = None
            comparison_end_dt = None
            
            if temporal_comparison:
                # Calculate previous period of same length
                comparison_end_dt = start_dt - timedelta(days=1)  # Day before current period
                comparison_start_dt = comparison_end_dt - timedelta(days=total_days - 1)  # Same length backwards
                
                comparison_start_date = comparison_start_dt.strftime('%Y-%m-%d')
                comparison_end_date = comparison_end_dt.strftime('%Y-%m-%d')
                
                print(f"📅 DEBUG: Comparison period: {comparison_start_date} to {comparison_end_date}")
                self.logger.info(f"Temporal comparison enabled - comparing with period {comparison_start_date} to {comparison_end_date}")
            
            # Collect NCS data for the current period (processes each day individually)
            print(f"🔍 DEBUG: Starting day-by-day NCS data collection for CURRENT period...")
            
            try:
                ncs_data = ncs_collector.collect_ncs_data_for_date_range(start_dt, end_dt)
                print(f"✅ DEBUG: Current period data collected: {len(ncs_data)} rows")
                # 🔄 Filter current period data by segment immediately
                ncs_data = await self._filter_ncs_by_segment(ncs_data, node_path)
                print(f"🔧 DEBUG: After segment filter ({node_path}) rows: {len(ncs_data)}")
                if ncs_data.empty:
                    print(f"⚠️ WARNING: Current period data is EMPTY - no incidents found for period {start_dt.strftime('%Y-%m-%d')} to {end_dt.strftime('%Y-%m-%d')}")
                else:
                    print(f"✅ DEBUG: Current period data sample columns: {list(ncs_data.columns)}")
                access_error = False
                error_msg = None
            except Exception as e:
                error_msg = str(e)
                print(f"❌ ERROR: NCS data collection failed: {error_msg}")
                
                # Check if it's an AWS access error
                if any(aws_error in error_msg.lower() for aws_error in ['invalidaccesskeyid', 'access denied', 'credentials', 'token']):
                    access_error = True
                    error_type = "AWS_ACCESS_ERROR"
                    print(f"🔑 Detected AWS access error - credentials may be expired")
                else:
                    access_error = True
                    error_type = "GENERAL_ERROR"
                
                # Create empty DataFrame for error case
                ncs_data = pd.DataFrame()
            
            # Collect comparison period data if temporal comparison is enabled and no access error
            if temporal_comparison and not access_error and comparison_start_dt is not None and comparison_end_dt is not None:
                print(f"🔍 DEBUG: Starting day-by-day NCS data collection for COMPARISON period...")
                print(f"🔍 DEBUG: Comparison period dates: {comparison_start_dt.strftime('%Y-%m-%d')} to {comparison_end_dt.strftime('%Y-%m-%d')}")
                try:
                    comparison_data = ncs_collector.collect_ncs_data_for_date_range(comparison_start_dt, comparison_end_dt)
                    print(f"✅ DEBUG: Comparison data collected: {len(comparison_data)} rows")
                    # 🔄 Filter comparison data by segment immediately
                    comparison_data = await self._filter_ncs_by_segment(comparison_data, node_path)
                    print(f"🔧 DEBUG: After segment filter ({node_path}) rows: {len(comparison_data)}")
                    if comparison_data.empty:
                        print(f"⚠️ WARNING: Comparison data is EMPTY - no incidents found for period {comparison_start_dt.strftime('%Y-%m-%d')} to {comparison_end_dt.strftime('%Y-%m-%d')}")
                    else:
                        print(f"✅ DEBUG: Comparison data sample columns: {list(comparison_data.columns)}")
                except Exception as e:
                    print(f"⚠️ ERROR: Comparison period data collection failed with exception: {str(e)}")
                    print(f"⚠️ ERROR: Exception type: {type(e).__name__}")
                    import traceback
                    print(f"⚠️ ERROR: Full traceback:\n{traceback.format_exc()}")
                    comparison_data = pd.DataFrame()  # Continue with current period only
            else:
                comparison_data = pd.DataFrame()
                print(f"🔍 DEBUG: Comparison data skipped - temporal_comparison={temporal_comparison}, access_error={access_error}")
                print(f"🔍 DEBUG: comparison_start_dt={comparison_start_dt}, comparison_end_dt={comparison_end_dt}")
                
                # Show why comparison was skipped
                if not temporal_comparison:
                    print(f"⚠️ Comparison skipped: temporal_comparison is False")
                elif access_error:
                    print(f"⚠️ Comparison skipped: access_error is True (current period failed)")
                elif comparison_start_dt is None or comparison_end_dt is None:
                    print(f"⚠️ Comparison skipped: comparison dates are None")
            
            # CASE 2: Access error - cannot interpret
            if access_error:
                self.collected_data['ncs_data'] = {
                    'analysis_summary': f"❌ NCS data source unavailable for {start_date} to {end_date} ({total_days} days)",
                    'identified_causes': [],
                    'affected_routes': [],
                    'route_impact_details': {},
                    'touchpoint_correlations': {},
                    'causal_confidence': 'no_data_source',
                    'explanation': f'Fuente de datos NCS no accesible - credenciales temporales pueden haber expirado o error de conectividad para período de {total_days} días',
                    'data_source_status': 'unavailable',
                    'error_details': error_msg[:200] if error_msg else 'Unknown error',
                    'days_analyzed': total_days,
                    'date_range': f"{start_date} to {end_date}",
                    'temporal_comparison_enabled': temporal_comparison,
                    'temporal_comparison_successful': False
                }
                return f"❌ NCS data source unavailable for the {total_days}-day period {start_date} to {end_date}. Access error prevents analysis of operational incidents. Technical details: {error_msg[:100] if error_msg else 'Unknown error'}"
            
            # CASE 1: No NCS data found for the entire period - could be good operational performance  
            if ncs_data.empty:
                # Store empty results with explanation - this is CASE 1: File found but no incidents
                self.collected_data['ncs_data'] = {
                    'analysis_summary': f"📅 No NCS operational incidents found for {start_date} to {end_date} ({total_days} days analyzed)",
                    'identified_causes': [],
                    'affected_routes': [],
                    'route_impact_details': {},
                    'touchpoint_correlations': {},
                    'causal_confidence': 'file_found_no_incidents',
                    'explanation': f'Archivos NCS revisados para {total_days} días pero sin incidentes operacionales - puede interpretarse como operación estable durante todo el período',
                    'data_source_status': 'available_but_empty',
                    'days_analyzed': total_days,
                    'date_range': f"{start_date} to {end_date}"
                }
                return f"📅 No NCS operational incidents found for the {total_days}-day period {start_date} to {end_date}. This could indicate good operational performance during the anomaly period."
            
            # TEMPORAL COMPARISON ANALYSIS (NEW)
            temporal_analysis = None
            comparison_successful = False
            
            if temporal_comparison and comparison_data is not None and not comparison_data.empty and comparison_start_dt is not None and comparison_end_dt is not None:
                print(f"📊 DEBUG: Starting temporal comparison analysis...")
                # Filter both current and comparison data by segment for consistent analysis
                filtered_current_data_for_temporal = await self._filter_ncs_by_segment(ncs_data, node_path)
                filtered_comparison_data_for_temporal = await self._filter_ncs_by_segment(comparison_data, node_path)
                print(f"🔧 DEBUG: Temporal analysis using filtered data - Current: {len(filtered_current_data_for_temporal)}, Comparison: {len(filtered_comparison_data_for_temporal)}")
                
                temporal_analysis = self._create_temporal_ncs_comparison(
                    filtered_current_data_for_temporal, filtered_comparison_data_for_temporal, node_path, 
                    start_date, end_date, 
                    comparison_start_dt.strftime('%Y-%m-%d'), comparison_end_dt.strftime('%Y-%m-%d')
                )
                comparison_successful = True
                print(f"✅ DEBUG: Temporal comparison completed successfully")
            elif temporal_comparison:
                print(f"⚠️ DEBUG: Temporal comparison enabled but comparison data unavailable")
            
            # Filter NCS data by segment routes using Routes Dictionary
            filtered_ncs_data = await self._filter_ncs_by_segment(ncs_data, node_path)
            
            if filtered_ncs_data.empty:
                # SUBCASO 3A: Incidentes existen globalmente pero no en el segmento específico
                total_global_incidents = len(ncs_data)
                
                self.collected_data['ncs_data'] = {
                    'analysis_summary': f"📊 Incidentes operacionales detectados en otras rutas durante {total_days} días - {node_path} no afectado",
                    'identified_causes': [],
                    'affected_routes': [],
                    'route_impact_details': {},
                    'touchpoint_correlations': {},
                    'causal_confidence': 'file_found_no_segment_incidents',
                    'explanation': f'Se encontraron {total_global_incidents} incidentes operacionales pero ninguno en rutas del segmento {node_path}',
                    'data_source_status': 'available_but_empty_for_segment',
                    'incidents_in_other_segments': True,
                    'non_correlated_incidents': total_global_incidents,
                    'days_analyzed': total_days,
                    'date_range': f"{start_date} to {end_date}"
                }
                return f"📊 Se encontraron {total_global_incidents} incidentes operacionales durante el período de {total_days} días ({start_date} a {end_date}), pero ninguno afectó las rutas del segmento {node_path}. Esto sugiere que los problemas operacionales ocurrieron en otros segmentos."
            
            # EXTRACT STRUCTURED NCS DATA for multi-day aggregation analysis
            incident_col = self._find_column(filtered_ncs_data, ['incident', 'incidents', ''])
            if incident_col is None:
                incident_col = filtered_ncs_data.columns[0] if not filtered_ncs_data.empty else ''
            
            all_incidents_text = "\n".join(filtered_ncs_data[incident_col].astype(str).tolist()) if not filtered_ncs_data.empty else ""
            structured_ncs_data = self._extract_structured_ncs_data(all_incidents_text)
            
            # ENHANCED CAUSAL ANALYSIS - Try new agent reflection approach first
            # Get anomaly type from stored attribute or default to unknown
            current_anomaly_type = getattr(self, 'current_anomaly_type', 'unknown')
            
            try:
                # First, try the new agent reflection approach
                self.logger.info(f"🤖 Trying new NCS agent reflection approach...")
                self.logger.info(f"📊 MAIN: About to send to agent reflection - data shape: {filtered_ncs_data.shape}")
                causal_analysis = await self._ncs_reflection_with_agent(filtered_ncs_data, node_path, current_anomaly_type, total_days)
                
                # INTEGRATE STRUCTURED NCS DATA into causal analysis
                causal_analysis['structured_ncs_data'] = structured_ncs_data
                
                # If agent reflection fails or returns no results, fall back to pattern matching
                if (not causal_analysis.get('identified_causes') and 
                    not causal_analysis.get('affected_routes') and
                    causal_analysis.get('confidence_level') != 'high_agent_analysis'):
                    self.logger.info(f"🔄 Agent reflection returned empty results, falling back to pattern matching...")
                    causal_analysis = await self._extract_ncs_causal_insights_workflow_aware(filtered_ncs_data, node_path, current_anomaly_type)
                else:
                    self.logger.info(f"✅ Agent reflection successful: {len(causal_analysis.get('identified_causes', []))} causes, {len(causal_analysis.get('affected_routes', []))} routes")
                    
            except Exception as e:
                self.logger.error(f"Error in NCS agent reflection, falling back to pattern matching: {str(e)}")
            causal_analysis = await self._extract_ncs_causal_insights_workflow_aware(filtered_ncs_data, node_path, current_anomaly_type)
            
            # Format results for agent understanding with WORKFLOW-AWARE FOCUS
            analysis_result = []
            analysis_result.append(f"🎯 NCS SEGMENT ANALYSIS: {node_path}")
            analysis_result.append(f"📅 Period: {start_date} to {end_date}")
            
            # Show workflow match status
            if causal_analysis.get('workflow_match'):
                incident_nature = causal_analysis.get('incident_nature', 'unknown')
                analysis_result.append(f"✅ WORKFLOW MATCH: {incident_nature.upper()} incidents found matching {incident_nature} analysis workflow")
            elif causal_analysis.get('workflow_mismatch'):
                current_workflow = causal_analysis.get('current_workflow', 'unknown')
                available_types = causal_analysis.get('available_incident_types', [])
                analysis_result.append(f"⚠️ WORKFLOW MISMATCH: Current workflow is {current_workflow.upper()}, but available incidents are {', '.join(available_types)}")
                analysis_result.append(f"🔄 Consider switching to appropriate workflow or incidents may not be relevant to current analysis")
            
            # PRIORITY 1: DISRUPTION CAUSES IDENTIFICADAS
            if causal_analysis['identified_causes']:
                analysis_result.append(f"🚨 DISRUPTION CAUSES IDENTIFICADAS:")
                for i, cause in enumerate(causal_analysis['identified_causes'][:3], 1):
                    analysis_result.append(f"  {i}. {cause}")
            
            # PRIORITY 2: AFFECTED ROUTES MAPPED
            if causal_analysis['affected_routes']:
                analysis_result.append(f"🛤️ AFFECTED ROUTES ({len(causal_analysis['affected_routes'])} routes):")
                route_impacts = causal_analysis['route_impact_summary']
                for route, impact in list(route_impacts.items())[:4]:  # Show top 4
                    analysis_result.append(f"  • {route}: {impact}")
            
            # STRUCTURED NCS BREAKDOWN - Information aggregated from actual fields
            structured_breakdown = causal_analysis.get('structured_ncs_data', {})
            if structured_breakdown and structured_breakdown.get('summary', {}).get('total_incidents', 0) > 0:
                summary = structured_breakdown['summary']
                categories = structured_breakdown.get('categories', {})
                motives = structured_breakdown.get('motives_breakdown', {})
                passengers = structured_breakdown.get('passenger_impact', {})
                delays = structured_breakdown.get('delay_statistics', {})
                
                analysis_result.append(f"📊 NCS STRUCTURED BREAKDOWN:")
                
                # Categories breakdown
                if categories:
                    cat_summary = [f"{cat}: {count}" for cat, count in categories.items() if count > 0]
                    if cat_summary:
                        analysis_result.append(f"   📋 Categorías: {', '.join(cat_summary)}")
                
                # Top motives 
                if motives:
                    top_motives = sorted(motives.items(), key=lambda x: x[1], reverse=True)[:3]
                    motive_summary = [f"{motive}: {count}" for motive, count in top_motives]
                    analysis_result.append(f"   🔧 Motivos principales: {', '.join(motive_summary)}")
                
                # Passenger impact
                if passengers.get('total', 0) > 0:
                    pax_breakdown = f"J:{passengers.get('j_class', 0)}, W:{passengers.get('w_class', 0)}, Y:{passengers.get('y_class', 0)} = {passengers['total']} pax"
                    analysis_result.append(f"   👥 Pasajeros afectados: {pax_breakdown}")
                
                # Delay statistics  
                if delays.get('count', 0) > 0:
                    analysis_result.append(f"   ⏱️ Retrasos: {delays['count']} vuelos, promedio {delays.get('avg_delay', 0):.1f} min, total {delays.get('total_minutes', 0)} min")
                
                # Most affected route from structured data
                if summary.get('most_affected_route'):
                    route, count = summary['most_affected_route']
                    analysis_result.append(f"   🛫 Ruta más afectada: {route} ({count} incidentes)")
                
                # ENHANCED: ALL affected routes with detailed incident breakdown by type
                route_incident_breakdown = structured_breakdown.get('route_incident_breakdown', {})
                route_disruptions = structured_breakdown.get('route_disruptions', {})
                
                if route_incident_breakdown:
                    # Intelligent sorting: by total incidents (desc), then by severity of incident types
                    def route_sort_key(item):
                        route, breakdown = item
                        total = breakdown['total']
                        # Weight by incident severity: cancelaciones > desvios > limitacion > retrasos > otras
                        severity_weight = (breakdown['cancelaciones'] * 5 + 
                                         breakdown['desvios'] * 4 + 
                                         breakdown['limitacion_aeronave'] * 3 + 
                                         breakdown['retrasos'] * 2 + 
                                         breakdown['otras_incidencias'] * 1)
                        return (total, severity_weight)
                    
                    sorted_routes = sorted(route_incident_breakdown.items(), key=route_sort_key, reverse=True)
                    
                    # Build detailed route list with incident type breakdown
                    routes_details = []
                    for route, breakdown in sorted_routes:
                        # Create compact breakdown showing only non-zero incident types
                        incident_parts = []
                        if breakdown['cancelaciones'] > 0:
                            incident_parts.append(f"C:{breakdown['cancelaciones']}")
                        if breakdown['desvios'] > 0:
                            incident_parts.append(f"D:{breakdown['desvios']}")
                        if breakdown['retrasos'] > 0:
                            incident_parts.append(f"R:{breakdown['retrasos']}")
                        if breakdown['otras_incidencias'] > 0:
                            incident_parts.append(f"O:{breakdown['otras_incidencias']}")
                        if breakdown['limitacion_aeronave'] > 0:
                            incident_parts.append(f"L:{breakdown['limitacion_aeronave']}")
                        
                        incident_detail = '|'.join(incident_parts) if incident_parts else f"{breakdown['total']}"
                        routes_details.append(f"{route}({incident_detail})")
                    
                    analysis_result.append(f"   🛫 RUTAS AFECTADAS: {', '.join(routes_details)}")
                    analysis_result.append(f"   📝 Leyenda: C=Cancelaciones, D=Desvíos, R=Retrasos, O=Otras, L=Limitación aeronave")
                    analysis_result.append(f"   📊 TOTAL: {len(sorted_routes)} rutas, {sum([b['total'] for b in route_incident_breakdown.values()])} incidentes")
                    
                elif route_disruptions:
                    # Fallback to simple route count if detailed breakdown not available
                    sorted_routes = sorted(route_disruptions.items(), key=lambda x: x[1], reverse=True)
                    routes_text = ', '.join([f"{route}({count})" for route, count in sorted_routes])
                    analysis_result.append(f"   🛫 RUTAS AFECTADAS: {routes_text}")
                    analysis_result.append(f"   📊 TOTAL: {len(sorted_routes)} rutas, {sum(route_disruptions.values())} incidentes")
            
            # Show incident count for segment with multi-day context
            segment_incident_count = len(filtered_ncs_data)
            # Store total for narrative use
            self._ncs_total_incidents = segment_incident_count
            
            if total_days > 1:
                analysis_result.append(f"📊 SEGMENT INCIDENTS: {segment_incident_count} incidents found on {node_path} routes across {total_days} days ({start_date} to {end_date})")
            else:
                analysis_result.append(f"📊 SEGMENT INCIDENTS: {segment_incident_count} incidents found on {node_path} routes")
            
            # Add temporal comparison to stored data if available
            if temporal_analysis is not None:
                causal_analysis['temporal_comparison'] = temporal_analysis
                causal_analysis['temporal_comparison_successful'] = comparison_successful
                
                # Add temporal comparison to analysis result - make it more prominent
                if temporal_analysis.get('analysis_summary'):
                    # Replace the pipe separators with newlines for better readability
                    temporal_summary = temporal_analysis['analysis_summary'].replace(' | ', '\n')
                    analysis_result.append(f"\n{temporal_summary}")
                    
                # Skip redundant temporal insights as they're now included in the comprehensive summary
                
                # Add combined comments summary for operational narrative
                if temporal_comparison and comparison_start_dt and comparison_end_dt and comparison_data is not None:
                    # Filter comparison data by segment to ensure consistent filtering
                    filtered_comparison_data = await self._filter_ncs_by_segment(comparison_data, node_path)
                    print(f"🔧 DEBUG: Filtered comparison data for segment {node_path}: {len(filtered_comparison_data)}/{len(comparison_data)} incidents")
                    
                    combined_comments = self._combine_and_summarize_ncs_comments(
                        filtered_ncs_data, filtered_comparison_data,
                        start_date, end_date,
                        comparison_start_dt.strftime('%Y-%m-%d'), comparison_end_dt.strftime('%Y-%m-%d')
                    )
                    if combined_comments and "Error" not in combined_comments:
                        analysis_result.append(f"\n📋 **NARRATIVA OPERATIVA COMBINADA:**")
                        analysis_result.append(combined_comments)
            
            # Store comprehensive data
            self.collected_data['ncs_data'] = causal_analysis
            
            result = " | ".join(analysis_result)
            return result
            
        except Exception as e:
            import traceback
            self.logger.error(f"💥 Error in NCS analysis: {str(e)}")
            self.logger.error(f"💥 Full traceback: {traceback.format_exc()}")
            return f"Error in NCS analysis: {str(e)}"

    async def _routes_tool(self, node_path: str, start_date: str, end_date: str, min_surveys: int = 2, anomaly_type: str = "unknown") -> str:
        """
        Enhanced tool for analyzing route-specific NPS performance from ALL sources:
        1. Routes from explanatory drivers (ordered by NPS and touchpoint satisfactions)
        2. Routes from NCS data (routes mentioned in operational incidents)
        3. Routes from verbatims (routes mentioned in customer feedback)
        """
        try:
            self.logger.info(f"🛫 ROUTES_TOOL CALLED - Enhanced comprehensive routes analysis")
            self.logger.debug(f"📋 Parameters: node_path={node_path}, start_date={start_date}, end_date={end_date}, anomaly_type={anomaly_type}")
            
            # Convert string dates to datetime
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
            
            # Collect routes from all three sources
            all_routes_analysis = await self._consolidate_routes_from_all_sources(
                node_path, start_dt, end_dt, anomaly_type, min_surveys
            )
            
            # Store comprehensive data for cross-references
            self.collected_data['routes_data'] = all_routes_analysis
            
            return all_routes_analysis['analysis_summary']
                
        except Exception as e:
            self.logger.error(f"💥 Error in comprehensive routes analysis: {str(e)}")
            return f"Error in comprehensive routes analysis: {str(e)}"

    async def _consolidate_routes_from_all_sources(self, node_path: str, start_dt, end_dt, anomaly_type: str, min_surveys: int) -> dict:
        """
        Consolidate and analyze routes from all three sources:
        1. Explanatory drivers routes (based on main touchpoint drivers)
        2. NCS routes (from operational incidents)  
        3. Verbatims routes (from customer feedback)
        """
        
        cabins, companies, hauls = self.pbi_collector._get_node_filters(node_path)
        start_date = start_dt.strftime('%Y-%m-%d')
        end_date = end_dt.strftime('%Y-%m-%d')
        
        # 1. EXPLANATORY DRIVERS ROUTES - Get routes ordered by main touchpoint drivers
        exp_drivers_routes = await self._get_explanatory_drivers_routes(
            node_path, cabins, companies, hauls, start_dt, end_dt, anomaly_type, min_surveys
        )
        
        # 2. NCS ROUTES - Get routes from operational incidents
        ncs_routes = await self._get_ncs_routes(
            node_path, cabins, companies, hauls, start_dt, end_dt
        )
        
        # 3. VERBATIMS ROUTES - Get routes from customer feedback
        verbatims_routes = await self._get_verbatims_routes(
            node_path, cabins, companies, hauls, start_dt, end_dt
        )
        
        # 4. CONSOLIDATE ALL ROUTES
        consolidated_analysis = self._create_consolidated_routes_analysis(
            exp_drivers_routes, ncs_routes, verbatims_routes, 
            node_path, start_date, end_date, anomaly_type
        )
        
        return consolidated_analysis

    async def _get_explanatory_drivers_routes(self, node_path: str, cabins: List[str], companies: List[str], 
                                            hauls: List[str], start_dt, end_dt, anomaly_type: str, min_surveys: int) -> dict:
        """
        Get routes analysis based on explanatory drivers touchpoints.
        For each significant driver, identify the top 5 routes with biggest CSAT changes vs comparison period.
        For negative anomalies: worst CSAT routes first (biggest drops)
        For positive anomalies: best CSAT routes first (biggest improvements)
        """
        try:
            # Get main touchpoint drivers from collected explanatory drivers data
            main_touchpoints = []
            if 'explanatory_drivers' in self.collected_data:
                significant_drivers = self.collected_data['explanatory_drivers'].get('significant_drivers', [])
                # significant_drivers is a list of strings (touchpoints), not dictionaries
                main_touchpoints = significant_drivers[:3]  # Top 3 drivers
            
            if not main_touchpoints:
                self.logger.info("No main touchpoints found from explanatory drivers - using general routes query")
                return await self._get_general_routes_with_touchpoints(cabins, companies, hauls, start_dt, end_dt, anomaly_type, min_surveys)
            
            self.logger.info(f"🎯 Analyzing routes based on main touchpoint drivers: {main_touchpoints}")
            
            # Debug logging
            self.logger.info(f"🔍 DEBUG ROUTES: node_path={node_path}, start_date={start_dt}, end_date={end_dt}")
            self.logger.info(f"🔍 DEBUG ROUTES: causal_filter={self.causal_filter}, comparison_start_date={self.comparison_start_date}, comparison_end_date={self.comparison_end_date}")
            self.logger.info(f"🔍 DEBUG ROUTES: cabins={cabins}, companies={companies}, hauls={hauls}")
            
            # Use the pbi_collector method that properly handles comparison_filter
            df = await self.pbi_collector.collect_routes_for_date_range(
                node_path=node_path,
                start_date=start_dt,
                end_date=end_dt,
                comparison_filter=self.causal_filter,  # Use the causal_filter from the agent
                comparison_start_date=self.comparison_start_date,
                comparison_end_date=self.comparison_end_date
            )
            
            # Debug logging for returned data
            self.logger.info(f"🔍 DEBUG ROUTES: DataFrame shape={df.shape}, columns={list(df.columns) if not df.empty else 'empty'}")
            if not df.empty:
                self.logger.info(f"🔍 DEBUG ROUTES: First few rows: {df.head(3).to_dict('records')}")
            
            if df.empty:
                return {"routes": [], "analysis": "❌ No explanatory drivers routes data found", "source": "explanatory_drivers"}
                
            # Clean column names
            df.columns = [col.replace('[', '').replace(']', '') for col in df.columns]
            
            # Find key columns
            route_col = self._find_column(df, ['route', 'Route', 'ROUTE'])
            nps_col = self._find_column(df, ['nps', 'NPS', 'Nps'])
            nps_diff_col = self._find_column(df, ['NPS diff', 'nps diff', 'nps_diff', 'vs'])
            pax_col = self._find_column(df, ['pax', 'n (route)', 'Pax', 'PAX'])
            
            if not route_col:
                return {"routes": [], "analysis": f"❌ Missing route column. Available: {list(df.columns)}", "source": "explanatory_drivers"}
            
            # Filter by minimum surveys
            if pax_col:
                df = df[df[pax_col].fillna(0) >= min_surveys]
            
            # Find touchpoint satisfaction columns for each driver (use CSAT diff for ordering)
            touchpoint_cols = {}
            touchpoint_abs_cols = {}  # Store absolute CSAT columns for display
            for touchpoint in main_touchpoints:
                # Map touchpoint names to CSAT diff column names (for ordering)
                touchpoint_diff_mapping = {
                    'check-in': 'Check_in_diff',
                    'check_in': 'Check_in_diff',
                    'lounge': 'Lounge_diff',
                    'boarding': 'Boarding_diff',
                    'aircraft interior': 'Aircraft_interior_diff',
                    'aircraft_interior': 'Aircraft_interior_diff',
                    'wi-fi': 'Wi-Fi_diff',
                    'wifi': 'Wi-Fi_diff',
                    'ife': 'IFE_diff',
                    'f&b': 'F&B_diff',
                    'fb': 'F&B_diff',
                    'crew': 'Crew_diff',
                    'cabin crew': 'Crew_diff',
                    'arrivals': 'Arrivals_diff',
                    'arrivals experience': 'Arrivals_diff',
                    'connections': 'Connections_diff',
                    'connections experience': 'Connections_diff',
                    'punctuality': 'Operative_diff'
                    # Note: Other touchpoints not available in routes data
                }
                
                # Map touchpoint names to absolute CSAT column names (for display)
                touchpoint_abs_mapping = {
                    'check-in': 'Check_in',
                    'check_in': 'Check_in',
                    'lounge': 'Lounge',
                    'boarding': 'Boarding',
                    'aircraft interior': 'Aircraft_interior',
                    'aircraft_interior': 'Aircraft_interior',
                    'wi-fi': 'Wi-Fi',
                    'wifi': 'Wi-Fi',
                    'ife': 'IFE',
                    'f&b': 'F&B',
                    'fb': 'F&B',
                    'crew': 'Crew',
                    'cabin crew': 'Crew',
                    'arrivals': 'Arrivals',
                    'arrivals experience': 'Arrivals',
                    'connections': 'Connections',
                    'connections experience': 'Connections',
                    'punctuality': 'Operative'
                    # Note: Other touchpoints not available in routes data
                }
                
                # Try to find the CSAT diff column (for ordering)
                exact_diff_col = touchpoint_diff_mapping.get(touchpoint.lower())
                if exact_diff_col and exact_diff_col in df.columns:
                    touchpoint_cols[touchpoint] = exact_diff_col
                    self.logger.info(f"✅ Found CSAT diff column for {touchpoint}: {exact_diff_col}")
                else:
                    self.logger.warning(f"⚠️ No CSAT diff column found for touchpoint: {touchpoint}")
                    continue
                
                # Try to find the absolute CSAT column (for display)
                exact_abs_col = touchpoint_abs_mapping.get(touchpoint.lower())
                if exact_abs_col and exact_abs_col in df.columns:
                    touchpoint_abs_cols[touchpoint] = exact_abs_col
                    self.logger.info(f"✅ Found absolute CSAT column for {touchpoint}: {exact_abs_col}")
                else:
                    self.logger.warning(f"⚠️ No absolute CSAT column found for touchpoint: {touchpoint}")
            
            if not touchpoint_cols:
                return {"routes": [], "analysis": f"❌ No touchpoint columns found for drivers: {main_touchpoints}. Available: {list(df.columns)}", "source": "explanatory_drivers"}
            
            # Prepare route analysis for each driver
            routes_analysis = []
            analysis_summary = f"🎯 EXPLANATORY DRIVERS ROUTES:\n"
            analysis_summary += f"   📊 Total routes analyzed: {len(df)}\n"
            analysis_summary += f"   🎯 Main touchpoint drivers: {', '.join(main_touchpoints)}\n"
            
            for touchpoint, col in touchpoint_cols.items():
                # Determine sorting direction based on SHAP value and anomaly type
                # Get SHAP value for this touchpoint from explanatory drivers data
                shap_value = 0.0
                if 'explanatory_drivers' in self.collected_data:
                    drivers_data = self.collected_data['explanatory_drivers'].get('all_drivers', [])
                    self.logger.info(f"🔍 DEBUG SHAP: Looking for touchpoint '{touchpoint}' in {len(drivers_data)} drivers")
                    for driver in drivers_data:
                        driver_touchpoint = driver.get('touchpoint', '')
                        # More robust comparison - check for partial matches
                        if (driver_touchpoint.lower() == touchpoint.lower() or 
                            touchpoint.lower() in driver_touchpoint.lower() or 
                            driver_touchpoint.lower() in touchpoint.lower()):
                            shap_value = driver.get('shap_value', 0.0)
                            self.logger.info(f"✅ DEBUG SHAP: Found match! SHAP value for {touchpoint}: {shap_value}")
                            break
                    if shap_value == 0.0:
                        self.logger.warning(f"⚠️ DEBUG SHAP: No SHAP value found for touchpoint '{touchpoint}'")
                
                # Sort routes by this touchpoint's CSAT difference (not absolute CSAT)
                # For negative SHAP values (negative impact): sort by worst CSAT diff first (biggest drops)
                # For positive SHAP values (positive impact): sort by best CSAT diff first (biggest improvements)
                if shap_value < 0:
                    # Negative SHAP: sort by worst CSAT diff first (biggest drops)
                    sorted_df = df.sort_values(by=col, ascending=True)
                    sort_desc = f"worst {touchpoint} CSAT change first (negative SHAP: {shap_value:.3f})"
                else:
                    # Positive SHAP: sort by best CSAT diff first (biggest improvements)
                    sorted_df = df.sort_values(by=col, ascending=False)
                    sort_desc = f"best {touchpoint} CSAT change first (positive SHAP: {shap_value:.3f})"
            
                # Get top 5 routes for this driver
                top_routes = sorted_df.head(5)
                
                analysis_summary += f"\n   🔝 Top 5 routes by {touchpoint} ({sort_desc}):\n"
                
                for _, route in top_routes.iterrows():
                    # Get absolute CSAT value for display
                    abs_col = touchpoint_abs_cols.get(touchpoint)
                    csat_abs = round(route[abs_col], 1) if abs_col and pd.notna(route[abs_col]) else None
                    
                    route_info = {
                        "route": route[route_col],
                        "driver": touchpoint,
                        "driver_score": csat_abs,  # Absolute CSAT for display
                        "driver_diff": round(route[col], 1) if pd.notna(route[col]) else None,  # CSAT diff (used for ordering)
                        "nps": round(route[nps_col], 1) if nps_col and pd.notna(route[nps_col]) else None,
                        "nps_diff": round(route[nps_diff_col], 1) if nps_diff_col and pd.notna(route[nps_diff_col]) else None,
                        "pax": int(route[pax_col]) if pax_col and pd.notna(route[pax_col]) else 0,
                        "source": "explanatory_drivers"
                    }
                    
                    routes_analysis.append(route_info)
                    
                    # Add to analysis summary
                    driver_score_str = f"{route_info['driver_score']}" if route_info['driver_score'] is not None else "N/A"
                    nps_str = f", NPS {route_info['nps']}" if route_info['nps'] is not None else ""
                    nps_diff_str = f", vs L7d: {route_info['nps_diff']:+.1f}" if route_info['nps_diff'] is not None else ""
                    analysis_summary += f"     • {route_info['route']}: {touchpoint} {driver_score_str}{nps_str}{nps_diff_str}, Pax {route_info['pax']}\n"
            
            return {
                "routes": routes_analysis,
                "analysis": analysis_summary,
                "source": "explanatory_drivers",
                "main_touchpoints": main_touchpoints
            }
            
        except Exception as e:
            self.logger.error(f"Error in explanatory drivers routes analysis: {e}")
            return {"routes": [], "analysis": f"❌ Explanatory drivers routes error: {str(e)[:100]}", "source": "explanatory_drivers"}

    async def _get_general_routes_with_touchpoints(self, cabins: List[str], companies: List[str], 
                                                 hauls: List[str], start_dt, end_dt, anomaly_type: str, min_surveys: int) -> dict:
        """Fallback method for general routes analysis when no specific touchpoints are available"""
        try:
            # Use the pbi_collector method with comparison filter
            df = await self.pbi_collector.collect_routes_for_date_range(
                "Global", start_dt, end_dt,
                comparison_filter=self.causal_filter,
                comparison_start_date=self.comparison_start_date,
                comparison_end_date=self.comparison_end_date
            )
            
            if df.empty:
                return {"routes": [], "analysis": "❌ No general routes data found", "source": "explanatory_drivers"}
            
            # Clean column names safely
            df = self._safe_clean_columns(df, method="strip")
            route_col = self._find_column(df, ['route'])
            nps_col = self._find_column(df, ['nps'])
            pax_col = self._find_column(df, ['pax', 'n (route)'])
            
            if pax_col:
                df = df[df[pax_col].fillna(0) >= min_surveys]
            
            # Sort by NPS and NPS diff if available
            nps_diff_col = self._find_column(df, ['NPS diff', 'nps diff'])
            
            if anomaly_type in ['-', 'negative', 'neg']:
                sort_cols = [nps_col]
                sort_ascending = [True]
                if nps_diff_col:
                    sort_cols.append(nps_diff_col)
                    sort_ascending.append(True)  # Most negative diff first
                df = df.sort_values(by=sort_cols, ascending=sort_ascending)
            else:
                sort_cols = [nps_col]
                sort_ascending = [False]
                if nps_diff_col:
                    sort_cols.append(nps_diff_col)
                    sort_ascending.append(False)  # Most positive diff first
                df = df.sort_values(by=sort_cols, ascending=sort_ascending)
            
            routes_analysis = []
            for _, route in df.head(5).iterrows():
                routes_analysis.append({
                    "route": route[route_col],
                    "nps": round(route[nps_col], 1),
                    "pax": int(route[pax_col]) if pax_col else 0,
                    "touchpoint_scores": {}
                })
            
            return {
                "routes": routes_analysis,
                "analysis": f"📊 General routes analysis: {len(routes_analysis)} routes",
                "source": "explanatory_drivers"
            }
            
        except Exception as e:
            return {"routes": [], "analysis": f"❌ General routes error: {str(e)[:100]}", "source": "explanatory_drivers"}

    async def _get_ncs_routes(self, node_path: str, cabins: List[str], companies: List[str], hauls: List[str], start_dt, end_dt) -> dict:
        """Get routes from NCS operational incidents data"""
        try:
            # Get identified routes from NCS analysis
            identified_routes = getattr(self.tracker, 'identified_routes', [])
            ncs_routes_from_data = []
            if hasattr(self, 'collected_data') and 'ncs_data' in self.collected_data:
                ncs_routes_from_data = self.collected_data['ncs_data'].get('affected_routes', [])
            
            all_ncs_routes = list(set(identified_routes + ncs_routes_from_data))
            
            if not all_ncs_routes:
                return {"routes": [], "analysis": "📊 No routes identified from NCS incidents", "source": "ncs"}
            
            self.logger.info(f"🎯 Analyzing NCS-specific routes: {all_ncs_routes}")
            
            # Get data for these specific routes using the same method as explanatory drivers
            # to ensure we get the correct NPS_diff values
            df_ncs = await self.pbi_collector.collect_routes_for_date_range(
                node_path=node_path,
                start_date=start_dt,
                end_date=end_dt,
                comparison_filter=self.causal_filter,
                comparison_start_date=self.comparison_start_date,
                comparison_end_date=self.comparison_end_date
            )
            
            if df_ncs.empty:
                return {"routes": [], "analysis": f"❌ No data found for NCS routes: {', '.join(all_ncs_routes)}", "source": "ncs"}
            
            # Clean column names safely
            df_ncs = self._safe_clean_columns(df_ncs, method="replace")
            
            # Filter to only include the NCS routes
            route_col = self._find_column(df_ncs, ['route', 'Route', 'ROUTE'])
            if route_col:
                df_ncs = df_ncs[df_ncs[route_col].isin(all_ncs_routes)]
            
            if df_ncs.empty:
                return {"routes": [], "analysis": f"❌ No data found for NCS routes after filtering: {', '.join(all_ncs_routes)}", "source": "ncs"}
            
            nps_col = self._find_column(df_ncs, ['nps', 'NPS', 'Nps'])
            nps_diff_col = self._find_column(df_ncs, ['NPS diff', 'nps diff', 'nps_diff', 'vs'])
            pax_col = self._find_column(df_ncs, ['pax', 'n (route)', 'Pax', 'PAX'])
            
            routes_analysis = []
            for _, route in df_ncs.iterrows():
                route_info = {
                    "route": route[route_col] if route_col else "Unknown",
                    "nps": round(route[nps_col], 1) if nps_col and pd.notna(route[nps_col]) else None,
                    "pax": int(route[pax_col]) if pax_col and pd.notna(route[pax_col]) else 0,
                    "nps_diff": round(route[nps_diff_col], 1) if nps_diff_col and pd.notna(route[nps_diff_col]) else None
                }
                routes_analysis.append(route_info)
            
            analysis_summary = f"🚨 NCS OPERATIONAL INCIDENTS ROUTES:\n"
            analysis_summary += f"   📊 Routes found: {len(routes_analysis)}/{len(all_ncs_routes)}\n"
            analysis_summary += f"   🎯 Identified from operational incidents: {', '.join(all_ncs_routes)}\n"
            
            if routes_analysis:
                analysis_summary += f"   📈 Route details:\n"
                for route_info in routes_analysis:
                    nps_str = f"NPS {route_info['nps']}" if route_info['nps'] is not None else "NPS N/A"
                    nps_diff_str = f", vs L7d: {route_info['nps_diff']:+.1f}" if route_info['nps_diff'] is not None else ""
                    analysis_summary += f"     • {route_info['route']}: {nps_str}{nps_diff_str}, Pax {route_info['pax']}\n"
            
            return {
                "routes": routes_analysis,
                "analysis": analysis_summary,
                "source": "ncs",
                "identified_routes": all_ncs_routes
            }
            
        except Exception as e:
            self.logger.error(f"Error in NCS routes analysis: {e}")
            return {"routes": [], "analysis": f"❌ NCS routes error: {str(e)[:100]}", "source": "ncs"}

    async def _get_verbatims_routes(self, node_path: str, cabins: List[str], companies: List[str], hauls: List[str], start_dt, end_dt) -> dict:
        """Get routes mentioned in verbatims/customer feedback"""
        try:
            # Get routes identified from verbatims conversation
            verbatims_routes = []
            if 'verbatims_conversation' in self.collected_data:
                conversation_data = self.collected_data['verbatims_conversation']
                conversation_log = conversation_data.get('conversation_log', [])
                
                # Extract routes mentioned in conversation responses
                for exchange in conversation_log:
                    response = exchange.get('response', '')
                    routes_in_response = self.tracker._extract_routes_from_result(response)
                    verbatims_routes.extend(routes_in_response)
            
            # Remove duplicates
            verbatims_routes = list(set(verbatims_routes))
            
            if not verbatims_routes:
                return {"routes": [], "analysis": "📊 No routes mentioned in customer verbatims", "source": "verbatims"}
            
            self.logger.info(f"🎯 Analyzing verbatims-mentioned routes: {verbatims_routes}")
            
            # Get data for these routes using the same method as explanatory drivers
            # to ensure we get the correct NPS_diff values
            df_verbatims = await self.pbi_collector.collect_routes_for_date_range(
                node_path=node_path,
                start_date=start_dt,
                end_date=end_dt,
                comparison_filter=self.causal_filter,
                comparison_start_date=self.comparison_start_date,
                comparison_end_date=self.comparison_end_date
            )
            
            if df_verbatims.empty:
                return {"routes": [], "analysis": f"❌ No data found for verbatims routes: {', '.join(verbatims_routes)}", "source": "verbatims"}
            
            # Clean column names
            df_verbatims.columns = [col.replace('[', '').replace(']', '') for col in df_verbatims.columns]
            
            # Filter to only include the verbatims routes
            route_col = self._find_column(df_verbatims, ['route', 'Route', 'ROUTE'])
            if route_col:
                df_verbatims = df_verbatims[df_verbatims[route_col].isin(verbatims_routes)]
            
            if df_verbatims.empty:
                return {"routes": [], "analysis": f"❌ No data found for verbatims routes after filtering: {', '.join(verbatims_routes)}", "source": "verbatims"}
            
            nps_col = self._find_column(df_verbatims, ['nps', 'NPS', 'Nps'])
            nps_diff_col = self._find_column(df_verbatims, ['NPS diff', 'nps diff', 'nps_diff', 'vs'])
            pax_col = self._find_column(df_verbatims, ['pax', 'n (route)', 'Pax', 'PAX'])
            
            routes_analysis = []
            for _, route in df_verbatims.iterrows():
                route_info = {
                    "route": route[route_col] if route_col else "Unknown",
                    "nps": round(route[nps_col], 1) if nps_col and pd.notna(route[nps_col]) else None,
                    "pax": int(route[pax_col]) if pax_col and pd.notna(route[pax_col]) else 0,
                    "nps_diff": round(route[nps_diff_col], 1) if nps_diff_col and pd.notna(route[nps_diff_col]) else None
                }
                routes_analysis.append(route_info)
            
            analysis_summary = f"💬 CUSTOMER VERBATIMS ROUTES:\n"
            analysis_summary += f"   📊 Routes found: {len(routes_analysis)}/{len(verbatims_routes)}\n"
            analysis_summary += f"   🎯 Mentioned in customer feedback: {', '.join(verbatims_routes)}\n"
            
            if routes_analysis:
                analysis_summary += f"   📈 Route details:\n"
                for route_info in routes_analysis:
                    nps_str = f"NPS {route_info['nps']}" if route_info['nps'] is not None else "NPS N/A"
                    nps_diff_str = f", vs L7d: {route_info['nps_diff']:+.1f}" if route_info['nps_diff'] is not None else ""
                    analysis_summary += f"     • {route_info['route']}: {nps_str}{nps_diff_str}, Pax {route_info['pax']}\n"
            
            return {
                "routes": routes_analysis,
                "analysis": analysis_summary,
                "source": "verbatims",
                "identified_routes": verbatims_routes
            }
            
        except Exception as e:
            self.logger.error(f"Error in verbatims routes analysis: {e}")
            return {"routes": [], "analysis": f"❌ Verbatims routes error: {str(e)[:100]}", "source": "verbatims"}

    def _create_consolidated_routes_analysis(self, exp_drivers_routes: dict, ncs_routes: dict, 
                                           verbatims_routes: dict, node_path: str, 
                                           start_date: str, end_date: str, anomaly_type: str) -> dict:
        """Create comprehensive analysis consolidating all route sources"""
        
        # Collect all unique routes
        all_routes = {}
        
        # Add explanatory drivers routes
        for route_info in exp_drivers_routes.get('routes', []):
            route_name = route_info['route']
            all_routes[route_name] = {
                'route': route_name,
                'nps': route_info['nps'],
                'pax': route_info['pax'],
                'vs': None,
                'touchpoint_scores': route_info.get('touchpoint_scores', {}),
                'sources': ['explanatory_drivers']
            }
        
        # Add NCS routes
        for route_info in ncs_routes.get('routes', []):
            route_name = route_info['route']
            if route_name in all_routes:
                all_routes[route_name]['sources'].append('ncs')
                if route_info.get('vs') is not None:
                    all_routes[route_name]['vs'] = route_info['vs']
            else:
                all_routes[route_name] = {
                    'route': route_name,
                    'nps': route_info['nps'],
                    'pax': route_info['pax'],
                    'vs': route_info.get('vs'),
                    'touchpoint_scores': {},
                    'sources': ['ncs']
                }
        
        # Add verbatims routes
        for route_info in verbatims_routes.get('routes', []):
            route_name = route_info['route']
            if route_name in all_routes:
                all_routes[route_name]['sources'].append('verbatims')
                if route_info.get('vs') is not None and all_routes[route_name]['vs'] is None:
                    all_routes[route_name]['vs'] = route_info['vs']
            else:
                all_routes[route_name] = {
                    'route': route_name,
                    'nps': route_info['nps'],
                    'pax': route_info['pax'],
                    'vs': route_info.get('vs'),
                    'touchpoint_scores': {},
                    'sources': ['verbatims']
                }
        
        # Create similarities analysis
        similarities_analysis = self._analyze_route_similarities(all_routes, exp_drivers_routes, ncs_routes, verbatims_routes)
        
        # Build comprehensive summary
        summary_parts = []
        summary_parts.append(f"🛫 COMPREHENSIVE ROUTES ANALYSIS")
        summary_parts.append(f"📅 Period: {start_date} to {end_date}")
        summary_parts.append(f"🎯 Segment: {node_path}")
        summary_parts.append(f"📊 Anomaly type: {anomaly_type}")
        summary_parts.append("")
        
        # Add individual source analyses
        summary_parts.append(exp_drivers_routes.get('analysis', ''))
        summary_parts.append("")
        summary_parts.append(ncs_routes.get('analysis', ''))
        summary_parts.append("")
        summary_parts.append(verbatims_routes.get('analysis', ''))
        summary_parts.append("")
        
        # Add consolidated routes list
        if all_routes:
            summary_parts.append("🔄 CONSOLIDATED ROUTES FROM ALL SOURCES:")
            summary_parts.append(f"   📊 Total unique routes: {len(all_routes)}")
            summary_parts.append("")
            
            for route_name, route_data in all_routes.items():
                sources_str = ", ".join(route_data['sources'])
                vs_str = f", VS {route_data['vs']}" if route_data['vs'] is not None else ""
                touchpoint_str = ""
                if route_data['touchpoint_scores']:
                    touchpoint_scores = ", ".join([f"{tp}: {score}" for tp, score in route_data['touchpoint_scores'].items()])
                    touchpoint_str = f", Touchpoints: [{touchpoint_scores}]"
                
                summary_parts.append(f"   • {route_name}: NPS {route_data['nps']}, Pax {route_data['pax']}{vs_str}{touchpoint_str}")
                summary_parts.append(f"     Sources: {sources_str}")
                summary_parts.append("")
        
        # Add similarities analysis
        summary_parts.append(similarities_analysis)
        
        consolidated_summary = "\n".join(summary_parts)
        
        return {
            'analysis_summary': consolidated_summary,
            'all_routes': all_routes,
            'exp_drivers_routes': exp_drivers_routes,
            'ncs_routes': ncs_routes,
            'verbatims_routes': verbatims_routes,
            'similarities_analysis': similarities_analysis,
            'total_routes': len(all_routes),
            'date_range': f"{start_date} to {end_date}",
            'node_path': node_path,
            'anomaly_type': anomaly_type
        }

    def _analyze_route_similarities(self, all_routes: dict, exp_drivers_routes: dict, 
                                  ncs_routes: dict, verbatims_routes: dict) -> str:
        """Analyze similarities and patterns among routes from different sources"""
        
        analysis_parts = []
        analysis_parts.append("🔍 ROUTES SIMILARITY ANALYSIS:")
        
        # Find routes mentioned in multiple sources
        multi_source_routes = {name: data for name, data in all_routes.items() if len(data['sources']) > 1}
        
        if multi_source_routes:
            analysis_parts.append(f"   🎯 Routes mentioned in multiple sources: {len(multi_source_routes)}")
            for route_name, route_data in multi_source_routes.items():
                sources_str = " + ".join(route_data['sources'])
                analysis_parts.append(f"     • {route_name}: Found in {sources_str}")
        else:
            analysis_parts.append("   📊 No routes found in multiple sources - each source identifies different routes")
        
        # Geographic patterns
        route_patterns = self._identify_route_patterns(list(all_routes.keys()))
        if route_patterns:
            analysis_parts.append(f"   🌍 Geographic patterns:")
            for pattern, routes in route_patterns.items():
                analysis_parts.append(f"     • {pattern}: {', '.join(routes)}")
        
        # Performance correlation analysis
        if len(all_routes) > 1:
            nps_values = [data['nps'] for data in all_routes.values()]
            nps_range = max(nps_values) - min(nps_values)
            avg_nps = sum(nps_values) / len(nps_values)
            
            analysis_parts.append(f"   📈 Overall NPS performance:")
            analysis_parts.append(f"     • Range: {min(nps_values):.1f} to {max(nps_values):.1f} (spread: {nps_range:.1f} pts)")
            analysis_parts.append(f"     • Average: {avg_nps:.1f}")
        
        # Source-specific insights
        exp_count = len(exp_drivers_routes.get('routes', []))
        ncs_count = len(ncs_routes.get('routes', []))
        verbatims_count = len(verbatims_routes.get('routes', []))
        
        analysis_parts.append(f"   📊 Source distribution:")
        analysis_parts.append(f"     • Explanatory drivers: {exp_count} routes")
        analysis_parts.append(f"     • NCS incidents: {ncs_count} routes")  
        analysis_parts.append(f"     • Customer verbatims: {verbatims_count} routes")
        
        return "\n".join(analysis_parts)

    def _identify_route_patterns(self, routes: List[str]) -> dict:
        """Identify geographic patterns in routes by destination regions"""
        patterns = {}
        
        # América del Norte (North America)
        north_america_destinations = ['JFK', 'LGA', 'EWR', 'MIA', 'ORD', 'DFW', 'LAX', 'BOS', 'IAD', 'YUL', 'YYZ']
        north_america_routes = [r for r in routes if any(dest in r.upper() for dest in north_america_destinations)]
        if north_america_routes:
            patterns['América del Norte'] = north_america_routes
        
        # Latinoamérica (Latin America) 
        latin_america_destinations = ['BOG', 'LIM', 'SCL', 'EZE', 'AEP', 'GRU', 'CGH', 'GIG', 'MEX', 'CCS', 'MVD', 'UIO', 'ASU', 'LPB']
        latin_america_routes = [r for r in routes if any(dest in r.upper() for dest in latin_america_destinations)]
        if latin_america_routes:
            patterns['Latinoamérica'] = latin_america_routes
        
        # Caribe (Caribbean)
        caribbean_destinations = ['SDQ', 'HAV', 'PUJ', 'STI', 'CUN', 'SJO', 'PTY', 'GUA', 'SAL', 'TGU', 'MGA']
        caribbean_routes = [r for r in routes if any(dest in r.upper() for dest in caribbean_destinations)]
        if caribbean_routes:
            patterns['Caribe'] = caribbean_routes
        
        # Europa (Europe)
        europe_destinations = ['LHR', 'CDG', 'FRA', 'AMS', 'FCO', 'MXP', 'ZUR', 'VIE', 'MUC', 'DUS', 'BRU', 'LIS', 'OPO', 
                             'DBV', 'ZAG', 'ATH', 'SKG', 'IST', 'WAW', 'PRG', 'BUD', 'OTP', 'SOF', 'TLV', 'CAI', 'CMN', 'ALG', 'TUN']
        europe_routes = [r for r in routes if any(dest in r.upper() for dest in europe_destinations)]
        if europe_routes:
            patterns['Europa'] = europe_routes
        
        return patterns

    def _find_column(self, df, possible_names: List[str]) -> str:
        """Find a column by trying multiple possible names (case-insensitive)"""
        for col in df.columns:
            for name in possible_names:
                # Handle empty string case explicitly
                if name == '' and col == '':
                    return col
                elif name != '' and name.lower() in col.lower():
                    return col
        return None
    
    async def _customer_profile_tool(self, node_path: str, start_date: str, end_date: str, min_surveys: int = 3, profile_dimension: str = "Multiple", mode: str = "comparative") -> str:
        """
        Tool for analyzing customer profile segments.
        - Comparative mode: NPS impact vs comparison filter (L7d, LM, etc.)
        - Single mode: Absolute NPS values for the period
        """
        try:
            self.logger.info(f"👥 CUSTOMER_PROFILE_TOOL CALLED - Mode: {mode}")
            self.logger.debug(f"📋 Parameters: node_path={node_path}, start_date={start_date}, end_date={end_date}, mode={mode}")
            
            # Convert string dates to datetime
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
            
            # Define key dimensions for NPS impact analysis
            # Available dimensions: Tier, Bound, Travel hour, Group age, Residence Region, 
            # Choosing reason, Business/Leisure, Travel reason, Fleet, CodeShare, Region, 
            # Channel, Demand spaces, Corporate, Connection, Fare Family, Issue Type, Travelling with
            if profile_dimension == "Multiple":
                dimensions = ["Business/Leisure", "Fleet", "Residence Region", "CodeShare"]
            else:
                dimensions = [profile_dimension]
            
            results = []
            nps_impact_summary = []
            
            for dimension in dimensions:
                try:
                    self.logger.info(f"Analyzing NPS impact for dimension: {dimension}")
                    
                    # collect_customer_profile_for_date_range IS async
                    if mode == "comparative":
                        df = await self.pbi_collector.collect_customer_profile_for_date_range(
                            node_path, start_dt, end_dt, dimension,
                            comparison_filter=self.causal_filter,
                            comparison_start_date=self.comparison_start_date,
                            comparison_end_date=self.comparison_end_date
                        )
                    else:  # single mode
                        df = await self.pbi_collector.collect_customer_profile_for_date_range(
                            node_path, start_dt, end_dt, dimension,
                            comparison_filter=None,  # No comparison in single mode
                            comparison_start_date=None,
                            comparison_end_date=None
                    )
                    
                    if df.empty:
                        results.append(f"❌ {dimension}: No data found")
                        continue
                    
                    # Clean column names (remove brackets) - same as routes_tool
                    df = self._safe_clean_columns(df, method="replace")
                    
                    # Filter by minimum surveys
                    if 'Pax' in df.columns:
                        df_filtered = df[df['Pax'].fillna(0) >= min_surveys]
                    else:
                        df_filtered = df
                    
                    if df_filtered.empty:
                        results.append(f"❌ {dimension}: No segments with sufficient surveys (>={min_surveys})")
                        continue
                    
                    # Find category column for profile names (after cleaning)
                    category_col = self._find_column(df_filtered, ['category', 'customer_profile'])
                    
                    if mode == "comparative":
                        # COMPARATIVE MODE: Focus on NPS impact vs comparison filter
                        nps_diff_col = self._find_column(df_filtered, ['nps diff', 'nps_diff', 'diff'])
                        if nps_diff_col:
                        # Sort by NPS diff to show impact order (highest to lowest)
                            df_sorted = df_filtered.sort_values(nps_diff_col, ascending=False)
                        
                        results.append(f"📊 {dimension}: {len(df_filtered)} segments analyzed")
                        
                            # Show EACH individual profile with its NPS_diff vs comparison filter  
                        for _, segment in df_sorted.iterrows():
                            # Safely get segment name
                            if category_col and category_col in segment:
                                segment_name = str(segment[category_col]) if segment[category_col] is not None else 'Unknown'
                            else:
                                segment_name = 'Unknown'
                            
                                # Safely convert NPS current, NPS diff and Pax count
                                try:
                                    nps_diff_raw = segment.get(nps_diff_col, 0)
                                    nps_diff = float(nps_diff_raw) if nps_diff_raw is not None and str(nps_diff_raw).lower() not in ['nan', 'none', ''] else 0.0
                                except (ValueError, TypeError):
                                    nps_diff = 0.0
                                
                                # Also get current NPS value
                                nps_current_col = self._find_column(df_filtered, ['nps'])
                                try:
                                    nps_current_raw = segment.get(nps_current_col, 0) if nps_current_col else 0
                                    nps_current = float(nps_current_raw) if nps_current_raw is not None and str(nps_current_raw).lower() not in ['nan', 'none', ''] else 0.0
                                except (ValueError, TypeError):
                                    nps_current = 0.0
                                
                                # Calculate baseline NPS (current - diff)
                                nps_baseline = nps_current - nps_diff
                                
                                try:
                                    pax_count = int(segment.get('Pax', 0))
                                except (ValueError, TypeError):
                                    pax_count = 0
                            
                                # Format with both NPS values and difference
                                nps_diff_str = f"{nps_diff:+.1f}" if nps_diff != 0 else "0.0"
                                filter_text = self.causal_filter if self.causal_filter else "período de referencia"
                                results.append(f"   • {segment_name}: NPS {nps_baseline:.1f} → {nps_current:.1f} (diff {nps_diff_str} vs {filter_text}) ({pax_count} surveys)")
                        
                            # Store impact data for summary
                        if len(df_filtered) >= 2:
                            max_impact = df_filtered[nps_diff_col].max()
                            min_impact = df_filtered[nps_diff_col].min()
                            impact_spread = max_impact - min_impact
                            
                            nps_impact_summary.append({
                                'dimension': dimension,
                                'impact_spread': impact_spread,
                                'avg_impact': df_filtered[nps_diff_col].mean(),
                                'max_impact': max_impact,
                                'min_impact': min_impact,
                                'segments_analyzed': len(df_filtered)
                            })
                        elif len(df_filtered) == 1:
                            # Single segment case
                            single_impact = df_filtered[nps_diff_col].iloc[0]
                            nps_impact_summary.append({
                                'dimension': dimension,
                                'impact_spread': 0.0,
                                'avg_impact': single_impact,
                                'max_impact': single_impact,
                                'min_impact': single_impact,
                                'segments_analyzed': 1
                            })
                        else:
                            # Fallback: show current NPS spread if diff not available
                            nps_col_fallback = self._find_column(df_filtered, ['nps'])
                            if nps_col_fallback:
                                nps_spread = df_filtered[nps_col_fallback].max() - df_filtered[nps_col_fallback].min()
                                avg_nps = df_filtered[nps_col_fallback].mean()
                                
                                results.append(f"✅ {dimension}: Current NPS Analysis (comparison not available)")
                                results.append(f"   📊 NPS spread: {nps_spread:.1f} pts, Average: {avg_nps:.1f}")
                            else:
                                results.append(f"❌ {dimension}: No NPS data available")
                                continue
                    
                    else:  # SINGLE MODE
                        # SINGLE MODE: Show absolute NPS values for the period (no comparison)
                        nps_col = self._find_column(df_filtered, ['nps'])
                        if nps_col:
                            # Sort by NPS value (highest to lowest) 
                            df_sorted = df_filtered.sort_values(nps_col, ascending=False)
                            
                            results.append(f"📊 {dimension}: {len(df_filtered)} segments analyzed")
                            
                            # Show EACH individual profile with its absolute NPS value
                            for _, segment in df_sorted.iterrows():
                                # Safely get segment name
                                if category_col and category_col in segment:
                                    segment_name = str(segment[category_col]) if segment[category_col] is not None else 'Unknown'
                                else:
                                    segment_name = 'Unknown'
                                
                                # Safely convert NPS value and Pax count
                                try:
                                    nps_raw = segment.get(nps_col, 0)
                                    nps_value = float(nps_raw) if nps_raw is not None and str(nps_raw).lower() not in ['nan', 'none', ''] else 0.0
                                except (ValueError, TypeError):
                                    nps_value = 0.0
                                
                                try:
                                    pax_count = int(segment.get('Pax', 0))
                                except (ValueError, TypeError):
                                    pax_count = 0
                                
                                results.append(f"   • {segment_name}: NPS {nps_value:.1f} ({pax_count} surveys)")
                            
                            # Calculate NPS spread for summary
                            if len(df_filtered) >= 2:
                                nps_spread = df_filtered[nps_col].max() - df_filtered[nps_col].min()
                                avg_nps = df_filtered[nps_col].mean()
                                
                                nps_impact_summary.append({
                                    'dimension': dimension,
                                    'impact_spread': nps_spread,
                                    'avg_impact': avg_nps,
                                    'max_impact': df_filtered[nps_col].max(),
                                    'min_impact': df_filtered[nps_col].min(),
                                    'segments_analyzed': len(df_filtered)
                                })
                            elif len(df_filtered) == 1:
                                single_nps = df_filtered[nps_col].iloc[0]
                                nps_impact_summary.append({
                                    'dimension': dimension,
                                    'impact_spread': 0.0,
                                    'avg_impact': single_nps,
                                    'max_impact': single_nps,
                                    'min_impact': single_nps,
                                    'segments_analyzed': 1
                                })
                        else:
                            results.append(f"❌ {dimension}: No NPS data available")
                            continue
                    
                except Exception as e:
                    results.append(f"❌ {dimension}: Error - {str(e)[:50]}")
                    continue
            
            # Build focused result summary
            if mode == "comparative":
                filter_text = self.causal_filter if self.causal_filter else "período de referencia"
                result = f"👥 CUSTOMER PROFILE - NPS IMPACT vs {filter_text.upper()}:\n"
            else:
                result = f"👥 CUSTOMER PROFILE - ABSOLUTE NPS VALUES:\n"
            result += f"📅 Period: {start_date} to {end_date}\n"
            result += f"🎯 Segment: {node_path}\n"
            result += f"📊 Dimensions analyzed: {len(nps_impact_summary)}/{len(dimensions)}\n\n"
            
            # Add dimension details
            result += "\n".join(results)
            
            # Add overall impact summary - CATEGORY COMPARISON
            if nps_impact_summary:
                if mode == "comparative":
                    filter_text = self.causal_filter if self.causal_filter else "período de referencia"
                    result += f"\n\n📈 REACTIVIDAD POR CATEGORÍA (NPS_diff vs {filter_text}):\n"
                else:
                    result += f"\n\n📈 DISPERSIÓN NPS POR CATEGORÍA (valores absolutos):\n"
                
                # Sort dimensions by impact spread (most reactive first)
                sorted_dimensions = sorted(nps_impact_summary, key=lambda x: x['impact_spread'], reverse=True)
                
                if mode == "comparative":
                    result += f"   🏆 RANKING DE REACTIVIDAD:\n"
                else:
                    result += f"   🏆 RANKING DE DISPERSIÓN NPS:\n"
                for i, dim_data in enumerate(sorted_dimensions, 1):
                    dimension = dim_data['dimension']
                    spread = dim_data['impact_spread']
                    max_impact = dim_data['max_impact']
                    min_impact = dim_data['min_impact']
                    segments = dim_data['segments_analyzed']
                    
                    # Show spread and range for context
                    result += f"   {i}. {dimension}: Spread {spread:.1f} pts "
                    result += f"(rango: {min_impact:+.1f} a {max_impact:+.1f}, {segments} perfiles)\n"
                
                # Overall summary
                total_avg_spread = sum([d['impact_spread'] for d in nps_impact_summary]) / len(nps_impact_summary)
                result += f"\n   📊 Reactividad promedio: {total_avg_spread:.1f} pts entre categorías"
            
            # Store data for cross-references
            self.collected_data['customer_profile'] = {
                'analysis_summary': result,
                'nps_impact_data': nps_impact_summary,
                'focus': 'nps_impact_vs_last_days'
            }
            return result
            
        except Exception as e:
            self.logger.error(f"💥 Error in customer profile NPS impact analysis: {str(e)}")
            return f"Error in customer profile NPS impact analysis: {str(e)}"
    
    def _safe_clean_columns(self, df: pd.DataFrame, method: str = "strip") -> pd.DataFrame:
        """
        Safely clean column names by removing brackets, handling None columns
        
        Args:
            df: DataFrame to clean
            method: "strip" for .strip('[]') or "replace" for .replace('[', '').replace(']', '')
        """
        if df.empty:
            return df
            
        cleaned_columns = []
        for col in df.columns:
            if col is not None and isinstance(col, str):
                if method == "strip":
                    cleaned_columns.append(col.strip('[]'))
                elif method == "replace":
                    cleaned_columns.append(col.replace('[', '').replace(']', ''))
                else:
                    cleaned_columns.append(col)
            else:
                # Log problematic columns and use a safe default
                self.logger.warning(f"⚠️ Found None/invalid column name: {col}, using default")
                cleaned_columns.append(f"Column_{len(cleaned_columns)}")
        df.columns = cleaned_columns
        return df

    def _create_temporal_ncs_comparison(self, current_data: pd.DataFrame, comparison_data: pd.DataFrame, 
                                      node_path: str, current_start: str, current_end: str, 
                                      comparison_start: str, comparison_end: str) -> dict:
        """
        Create temporal comparison analysis of NCS data between two periods.
        Generates the Route × Incident Type matrix with deltas as requested.
        
        Returns:
            Dict with temporal comparison analysis including route-incident matrix and deltas
        """
        try:
            print(f"🔄 Creating temporal NCS comparison for {node_path}")
            
            # Extract structured data for both periods
            current_structured = self._extract_structured_ncs_data_for_comparison(current_data, "current")
            comparison_structured = self._extract_structured_ncs_data_for_comparison(comparison_data, "comparison")
            
            # Create route × incident type matrix
            route_incident_matrix = self._create_route_incident_matrix(current_structured, comparison_structured)
            
            # Calculate global deltas by incident type
            incident_type_deltas = self._calculate_incident_type_deltas(current_structured, comparison_structured)
            
            # Identify patterns and trends
            improvement_patterns = self._identify_improvement_patterns(route_incident_matrix, incident_type_deltas)
            
            # Create comprehensive analysis
            temporal_analysis = {
                'current_period': f"{current_start} to {current_end}",
                'comparison_period': f"{comparison_start} to {comparison_end}",
                'route_incident_matrix': route_incident_matrix,
                'incident_type_deltas': incident_type_deltas,
                'improvement_patterns': improvement_patterns,
                'current_structured': current_structured,
                'comparison_structured': comparison_structured,
                'analysis_summary': self._generate_temporal_summary(route_incident_matrix, incident_type_deltas, improvement_patterns)
            }
            
            return temporal_analysis
            
        except Exception as e:
            self.logger.error(f"Error creating temporal NCS comparison: {str(e)}")
            return {
                'error': str(e),
                'current_period': f"{current_start} to {current_end}",
                'comparison_period': f"{comparison_start} to {comparison_end}",
                'analysis_summary': f"❌ Error in temporal comparison: {str(e)}"
                         }
    
    def _extract_structured_ncs_data_for_comparison(self, data: pd.DataFrame, period_label: str) -> dict:
        """Extract structured NCS data optimized for temporal comparison"""
        if data.empty:
            return {
                'period': period_label,
                'total_incidents': 0,
                'route_incidents': {},
                'incident_types': {
                    'cancelaciones': 0,
                    'retrasos': 0,
                    'desvios': 0,
                    'limitacion_aeronave': 0,
                    'otras_incidencias': 0
                },
                'routes': []
            }
        
        # Process incident types directly from DataFrame columns
        incident_types = {
            'cancelaciones': 0,
            'retrasos': 0, 
            'desvios': 0,
            'limitacion_aeronave': 0,
            'otras_incidencias': 0
        }
        
        # Map DataFrame columns to incident types
        column_mapping = {
            'Cancelaciones': 'cancelaciones',
            'Retrasos': 'retrasos', 
            'Desvíos': 'desvios',
            'Desvios': 'desvios',
            'Otras incidencias': 'otras_incidencias',
            'Limitación de la aeronave': 'limitacion_aeronave'
        }
        
        # Count incidents by type from DataFrame columns
        for col in data.columns:
            if col in column_mapping:
                incident_type = column_mapping[col]
                # Sum non-null values in the column
                count = data[col].notna().sum()
                incident_types[incident_type] = count
        
        # Extract routes from incident text
        route_incidents = {}
        incident_col = self._find_column(data, ['incident', 'incidents', ''])
        if incident_col and incident_col in data.columns:
            # Extract routes from incident descriptions
            route_pattern = r'\b([A-Z]{3})\s*[-–]\s*([A-Z]{3})\b'
            all_routes = set()
            
            for incident_text in data[incident_col].dropna():
                if isinstance(incident_text, str):
                    routes = re.findall(route_pattern, incident_text, re.IGNORECASE)
                    for origin, dest in routes:
                        route_code = f"{origin.upper()}-{dest.upper()}"
                        all_routes.add(route_code)
                        
                        if route_code not in route_incidents:
                            route_incidents[route_code] = {
                                'cancelaciones': 0, 'desvios': 0, 'retrasos': 0,
                                'otras_incidencias': 0, 'limitacion_aeronave': 0, 'total': 0
                            }
                        
                        # Simple classification based on keywords in incident text
                        incident_lower = incident_text.lower()
                        if any(word in incident_lower for word in ['cancel', 'cancelación']):
                            route_incidents[route_code]['cancelaciones'] += 1
                        elif any(word in incident_lower for word in ['retraso', 'delay']):
                            route_incidents[route_code]['retrasos'] += 1
                        elif any(word in incident_lower for word in ['desvío', 'desvio', 'divert']):
                            route_incidents[route_code]['desvios'] += 1
                        elif any(word in incident_lower for word in ['limitación', 'limitacion']):
                            route_incidents[route_code]['limitacion_aeronave'] += 1
                        else:
                            route_incidents[route_code]['otras_incidencias'] += 1
                        
                        route_incidents[route_code]['total'] += 1
        
        return {
            'period': period_label,
            'total_incidents': len(data),
            'route_incidents': route_incidents,
            'incident_types': incident_types,
            'routes': list(route_incidents.keys())
        }
    
    def _create_route_incident_matrix(self, current: dict, comparison: dict) -> dict:
        """Create the Route × Incident Type matrix with deltas"""
        matrix = {}
        
        # Get all unique routes from both periods
        all_routes = set(current['routes'] + comparison['routes'])
        
        for route in all_routes:
            current_breakdown = current['route_incidents'].get(route, {
                'cancelaciones': 0, 'retrasos': 0, 'desvios': 0, 
                'limitacion_aeronave': 0, 'otras_incidencias': 0, 'total': 0
            })
            comparison_breakdown = comparison['route_incidents'].get(route, {
                'cancelaciones': 0, 'retrasos': 0, 'desvios': 0,
                'limitacion_aeronave': 0, 'otras_incidencias': 0, 'total': 0
            })
            
            # Calculate deltas for each incident type
            deltas = {}
            for incident_type in ['cancelaciones', 'retrasos', 'desvios', 'limitacion_aeronave', 'otras_incidencias']:
                current_count = current_breakdown.get(incident_type, 0)
                comparison_count = comparison_breakdown.get(incident_type, 0)
                delta = current_count - comparison_count
                
                # Calculate percentage change
                if comparison_count > 0:
                    pct_change = (delta / comparison_count) * 100
                elif current_count > 0:
                    pct_change = float('inf')  # New incidents
                else:
                    pct_change = 0
                
                deltas[incident_type] = {
                    'current': current_count,
                    'previous': comparison_count,
                    'delta': delta,
                    'pct_change': pct_change
                }
            
            # Calculate total delta
            current_total = current_breakdown.get('total', 0)
            comparison_total = comparison_breakdown.get('total', 0)
            total_delta = current_total - comparison_total
            total_pct_change = (total_delta / comparison_total * 100) if comparison_total > 0 else (float('inf') if current_total > 0 else 0)
            
            matrix[route] = {
                'deltas': deltas,
                'total_delta': {
                    'current': current_total,
                    'previous': comparison_total,
                    'delta': total_delta,
                    'pct_change': total_pct_change
                }
            }
        
        return matrix
    
    def _calculate_incident_type_deltas(self, current: dict, comparison: dict) -> dict:
        """Calculate global deltas by incident type"""
        deltas = {}
        
        for incident_type in ['cancelaciones', 'retrasos', 'desvios', 'limitacion_aeronave', 'otras_incidencias']:
            current_count = current['incident_types'].get(incident_type, 0)
            comparison_count = comparison['incident_types'].get(incident_type, 0)
            delta = current_count - comparison_count
            
            if comparison_count > 0:
                pct_change = (delta / comparison_count) * 100
            elif current_count > 0:
                pct_change = float('inf')
            else:
                pct_change = 0
            
            deltas[incident_type] = {
                'current': current_count,
                'previous': comparison_count,
                'delta': delta,
                'pct_change': pct_change
            }
        
        return deltas
    
    def _identify_improvement_patterns(self, route_matrix: dict, type_deltas: dict) -> dict:
        """Identify improvement and deterioration patterns"""
        patterns = {
            'major_improvements': [],  # Significant reductions in incidents
            'moderate_improvements': [],
            'deteriorations': [],  # Increases in incidents
            'new_problems': [],  # Routes with new incidents
            'resolved_problems': []  # Routes that had incidents but now don't
        }
        
        for route, data in route_matrix.items():
            # Safety check for data structure
            if not isinstance(data, dict) or 'total_delta' not in data:
                self.logger.warning(f"⚠️ Invalid route data structure for {route}: {data}")
                continue
                
            total_delta_obj = data['total_delta']
            if not isinstance(total_delta_obj, dict) or 'delta' not in total_delta_obj:
                self.logger.warning(f"⚠️ Invalid total_delta structure for {route}: {total_delta_obj}")
                continue
                
            total_delta = total_delta_obj['delta']
            if total_delta is None:
                self.logger.warning(f"⚠️ None delta value for route {route}")
                continue
            
            if total_delta < -5:  # Major improvement
                patterns['major_improvements'].append({
                    'route': route,
                    'delta': total_delta,
                    'current': data['total_delta']['current'],
                    'previous': data['total_delta']['previous']
                })
            elif total_delta < 0:  # Moderate improvement
                patterns['moderate_improvements'].append({
                    'route': route,
                    'delta': total_delta,
                    'current': data['total_delta']['current'],
                    'previous': data['total_delta']['previous']
                })
            elif total_delta > 0:  # Deterioration
                patterns['deteriorations'].append({
                    'route': route,
                    'delta': total_delta,
                    'current': data['total_delta']['current'],
                    'previous': data['total_delta']['previous']
                })
        
        return patterns
    
    def _generate_temporal_summary(self, route_matrix: dict, type_deltas: dict, patterns: dict) -> str:
        """Generate comprehensive VS temporal comparison analysis for NCS data"""
        summary_parts = []
        
        # HEADER
        summary_parts.append("📊 **ANÁLISIS COMPARATIVO NCS - PERÍODO ACTUAL vs ANTERIOR**")
        summary_parts.append("")
        
        # SECTION 1: GLOBAL COMPARISON BY INCIDENT TYPE
        summary_parts.append("📈 **RESUMEN GLOBAL POR TIPO DE INCIDENTE:**")
        
        if type_deltas:
            total_current = sum(delta_info.get('current', 0) for delta_info in type_deltas.values())
            total_previous = sum(delta_info.get('previous', 0) for delta_info in type_deltas.values())
            total_delta = total_current - total_previous
            
            summary_parts.append(f"   🎯 **TOTAL**: {total_previous} → {total_current} ({total_delta:+d}, {((total_current/total_previous-1)*100 if total_previous > 0 else 0):+.1f}%)")
            summary_parts.append("")
            
            # Detailed breakdown by type with NPS impact validation
            for incident_type, delta_info in sorted(type_deltas.items(), key=lambda x: abs(x[1].get('delta', 0)), reverse=True):
                current = delta_info.get('current', 0)
                previous = delta_info.get('previous', 0)
                delta = delta_info.get('delta', 0)
                pct_change = delta_info.get('pct_change', 0)
                
                if current > 0 or previous > 0:  # Only show types that had incidents
                    status_icon = "🔴" if delta > 0 else ("🟢" if delta < 0 else "⚪")
                    pct_str = f"{pct_change:+.1f}%" if pct_change != float('inf') and abs(pct_change) > 0 else "N/A"
                    
                    # Add NPS impact validation
                    nps_impact = self._get_nps_impact_validation(incident_type, delta)
                    
                    summary_parts.append(f"   {status_icon} **{incident_type.upper()}**: {previous} → {current} ({delta:+d}, {pct_str}) {nps_impact}")
        
        summary_parts.append("")
        
        # SECTION 2: ROUTE-LEVEL ANALYSIS
        summary_parts.append("🛣️ **RUTAS MÁS AFECTADAS:**")
        
        if route_matrix:
            # Sort routes by total impact
            route_impacts = {}
            for route, incidents in route_matrix.items():
                total_delta = sum(abs(inc.get('delta', 0)) for inc in incidents.values())
                route_impacts[route] = total_delta
            
            sorted_routes = sorted(route_impacts.items(), key=lambda x: x[1], reverse=True)
            
            shown_routes = 0
            for route, impact in sorted_routes:
                if impact > 0 and shown_routes < 5:  # Show top 5 affected routes
                    incidents = route_matrix[route]
                    route_changes = []
                    for inc_type, inc_data in incidents.items():
                        if inc_data.get('delta', 0) != 0:
                            delta = inc_data.get('delta', 0)
                            route_changes.append(f"{inc_type}({delta:+d})")
                    
                    summary_parts.append(f"   🛫 **{route}**: {', '.join(route_changes)}")
                    shown_routes += 1
        
        # SECTION 3: KEY INSIGHTS
        summary_parts.append("")
        summary_parts.append("🔍 **INSIGHTS:**")
        
        if patterns.get('major_improvements'):
            improvements = patterns['major_improvements'][:2]
            routes_improved = [f"{item['route']} ({item['delta']:+d})" for item in improvements]
            summary_parts.append(f"   ✅ Mejoras: {', '.join(routes_improved)}")
        
        if patterns.get('deteriorations'):
            deteriorations = patterns['deteriorations'][:2] 
            routes_worse = [f"{item['route']} ({item['delta']:+d})" for item in deteriorations]
            summary_parts.append(f"   ⚠️ Deterioros: {', '.join(routes_worse)}")
        
        return " | ".join(summary_parts)
    
    def _get_nps_impact_validation(self, incident_type: str, delta: int) -> str:
        """Get NPS impact validation for incident type changes"""
        
        # Simple validation: more incidents = lower NPS, fewer incidents = higher NPS
        if delta > 0:
            return "📉 Valida una bajada de NPS"
        elif delta < 0:
            return "📈 Valida una subida de NPS"
        else:
            return "⚪ Sin impacto en NPS"
    
    async def _get_clean_reflection(self, system_prompt: str, tool_name: str, tool_result: str, message_history: MessageHistory, mode: str = "comparative") -> Optional[Dict[str, str]]:
        """Get AI reflection using clean context + tool results"""
        try:
            self.logger.info(f"🤔 Starting reflection for {tool_name}...")
            
            # Create clean message history for reflection
            clean_messages = self.tracker.get_clean_context(system_prompt)
            
            # Add current tool context with helper prompt and results using new mode-specific template
            # Try to determine flow type from context for comparative mode
            flow_type = None
            if mode == "comparative" and tool_name == "explanatory_drivers_tool":
                # For explanatory drivers, we need to analyze the result to determine flow
                flow_type = self._determine_flow_type_from_drivers(tool_result)
            
            reflection_template = self._get_reflection_prompt(mode, tool_name, flow_type)
            self.logger.info(f"🔍 DEBUG LLM: reflection_template length={len(reflection_template) if reflection_template else 0}")
            
            if reflection_template:
                # Ensure causal_filter has a safe value for template formatting
                safe_causal_filter = self.causal_filter if self.causal_filter else "período de referencia"
                reflection_prompt = reflection_template.format(
                tool_name=tool_name.upper(),
                tool_result=tool_result,
                    causal_filter=safe_causal_filter,
                    comparison_filter=safe_causal_filter  # For backwards compatibility
            )
                self.logger.info(f"🔍 DEBUG LLM: reflection_prompt formatted successfully, length={len(reflection_prompt)}")
            else:
                reflection_prompt = f"Analiza los resultados de {tool_name.upper()}\n\n{tool_result}"
                self.logger.warning(f"🔍 DEBUG LLM: Using fallback reflection_prompt, length={len(reflection_prompt)}")
            
            # Check reflection prompt size
            prompt_size = len(reflection_prompt)
            self.logger.info(f"🔍 DEBUG LLM: Final reflection_prompt size: {prompt_size} chars")
            self.logger.info(f"🔍 DEBUG LLM: reflection_prompt preview: {reflection_prompt[:500]}...")
            
            if prompt_size > 60000:  # 60KB limit for reflection
                self.logger.warning(f"⚠️ Reflection prompt very large ({prompt_size} chars) - truncating tool result")
                truncated_result = tool_result[:30000] + "\n\n[... TOOL RESULT TRUNCATED DUE TO SIZE ...]"
                reflection_template = self._get_reflection_prompt(mode, tool_name, flow_type)
                if reflection_template:
                    # Ensure causal_filter has a safe value for template formatting
                    safe_causal_filter = self.causal_filter if self.causal_filter else "período de referencia"
                    reflection_prompt = reflection_template.format(
                    tool_name=tool_name.upper(),
                    tool_result=truncated_result,
                        causal_filter=safe_causal_filter,
                        comparison_filter=safe_causal_filter  # For backwards compatibility
                )
                else:
                    reflection_prompt = f"Analiza los resultados de {tool_name.upper()}\n\n{truncated_result}"
                self.logger.debug(f"📏 Truncated reflection prompt size: {len(reflection_prompt)} chars")
            
            clean_messages.append({
                "role": "user",
                "content": reflection_prompt
            })
            
            # Add timeout to prevent hanging reflections
            self.logger.debug(f"🕒 Starting LLM call for {tool_name} reflection with 60s timeout")
            
            response, _, _ = await asyncio.wait_for(
                self.agent.invoke(
                    messages=clean_messages,
                    tools=[],  # No tools for reflection
                    structured_output=None  # No structured output for reflections
                ),
                timeout=300.0  # 5 minute timeout for reflections
            )
            
            self.logger.debug(f"✅ Reflection response received for {tool_name}")
            
            # Check if response content is valid
            if response.content and isinstance(response.content, str) and response.content.strip():
                self.logger.info(f"🤔 Reflection completed for {tool_name}: {len(response.content)} chars")
                self.logger.info(f"🔍 DEBUG LLM OUTPUT: Raw response preview: {response.content[:500]}...")
                
                # Parse the structured response to extract reflection and next tool code
                reflection, next_tool_code = self._parse_reflection_response(response.content)
                self.logger.info(f"🔍 DEBUG LLM OUTPUT: Parsed reflection length={len(reflection) if reflection else 0}")
                self.logger.info(f"🔍 DEBUG LLM OUTPUT: Parsed next_tool_code length={len(next_tool_code) if next_tool_code else 0}")
                
                # Store reflection in message history
                if reflection:
                    message_history.create_and_add_message(
                        content=f"REFLECTION: {reflection}",
                        message_type=MessageType.AI,
                        agent=AgentName.CONVERSATIONAL
                    )
                
                # Return both reflection and next tool code
                return {
                    "reflection": reflection,
                    "next_tool_code": next_tool_code
                }
            else:
                self.logger.warning(f"⚠️ No valid reflection content for {tool_name}")
                return None
                
        except asyncio.TimeoutError:
            self.logger.error(f"⏰ Reflection for {tool_name} timed out after 120 seconds")
            return f"Reflection timed out for {tool_name} - tool result too complex"
        except Exception as e:
            self.logger.error(f"❌ Error getting clean reflection for {tool_name}: {type(e).__name__}: {e}")
            return None
    
    async def _generate_final_synthesis(
        self, 
        message_history: MessageHistory,
        node_path: str,
        start_date: str, 
        end_date: str,
        nps_context: str = ""
    ) -> str:
        """Generate final synthesis with collected data"""
        
        # Build comprehensive data summary from collected_data
        try:
            data_summary = self._build_collected_data_summary()
            self.logger.info(f"📊 Data summary built successfully: {len(data_summary)} chars")
        except Exception as e:
            self.logger.error(f"❌ Error building data summary: {e}")
            data_summary = "Error building data summary - using minimal fallback"
        
        # FINAL USER MESSAGE: Summary request with collected data
        enhanced_final_request = f"""
{self.config.get('final_synthesis_prompt', 'Genera un informe causal consolidado basado en los datos recolectados.')}

📊 **DATOS RECOLECTADOS DURANTE LA INVESTIGACIÓN:**

{data_summary}

**INSTRUCCIONES ESPECÍFICAS:**
- Usa TODOS los datos numéricos recolectados arriba
- Incluye valores SHAP exactos, rutas específicas, números de incidentes, etc.
- NO hagas afirmaciones sin datos concretos
- Integra los hallazgos de todas las herramientas ejecutadas
- **IMPORTANTE**: Menciona los NPS específicos del período analizado y el período de comparación{nps_context}
"""
        
        # Check if request is too large
        request_size = len(enhanced_final_request)
        self.logger.info(f"📏 Final request size: {request_size} chars")
        
        if request_size > 100000:  # 100KB limit
            self.logger.warning(f"⚠️ Final request very large ({request_size} chars) - truncating data summary")
            # Truncate data summary to prevent LLM overload
            truncated_summary = data_summary[:25000] + "\n\n[... DATA TRUNCATED DUE TO SIZE ...]"
            enhanced_final_request = f"""
{self.config.get('final_synthesis_prompt', 'Genera un informe causal consolidado basado en los datos recolectados.')}

📊 **DATOS RECOLECTADOS DURANTE LA INVESTIGACIÓN:**

{truncated_summary}

**INSTRUCCIONES ESPECÍFICAS:**
- Usa TODOS los datos numéricos recolectados arriba
- Incluye valores SHAP exactos, rutas específicas, números de incidentes, etc.
- NO hagas afirmaciones sin datos concretos
- Integra los hallazgos de todas las herramientas ejecutadas
- **IMPORTANTE**: Menciona los NPS específicos del período analizado y el período de comparación{nps_context}
"""
            self.logger.info(f"📏 Truncated request size: {len(enhanced_final_request)} chars")
        
        message_history.create_and_add_message(
            content=enhanced_final_request,
            message_type=MessageType.USER
        )
        
        self.tracker.log_message("USER", f"ENHANCED_FINAL_SYNTHESIS_REQUEST: {enhanced_final_request}")
        
        # FINAL AI MESSAGE: Synthesis
        try:
            self.logger.info("🎯 Starting final synthesis with LLM...")
            self.logger.debug(f"📊 Enhanced final request length: {len(enhanced_final_request)} chars")
            self.logger.debug(f"📊 Message history length: {len(message_history.get_messages())} messages")
            
            # Add timeout to prevent hanging
            import asyncio
            final_response, final_structured_response, _ = await asyncio.wait_for(
                self.agent.invoke(
                    messages=message_history.get_messages(),
                    tools=[],
                    structured_output=None  # Remove structured output to get narrative content
                ),
                timeout=1800.0  # 30 minute timeout for very complex final synthesis
            )
            
            self.logger.info("✅ LLM response received")
            
            # Log the full response for debugging
            self.logger.info(f"🔍 LLM Response Type: {type(final_response)}")
            self.logger.info(f"🔍 LLM Response Content: {final_response.content}")
            self.logger.info(f"🔍 LLM Response Length: {len(final_response.content) if final_response.content else 0}")
            
            if final_response.content:
                self.tracker.log_message("AI", f"FINAL_SYNTHESIS: {final_response.content}")
                self.logger.info("🎯 Final synthesis completed successfully")
                self.logger.debug(f"📊 Final response length: {len(final_response.content)} chars")
                return final_response.content
            else:
                self.logger.warning("⚠️ Empty response content from LLM")
                self.logger.error(f"❌ LLM returned empty content. Full response object: {final_response}")
                return "No final synthesis generated - empty LLM response"
                
        except asyncio.TimeoutError:
            self.logger.error(f"⏰ Final synthesis timed out after 15 minutes")
            return f"Final synthesis timed out - request too complex for LLM processing"
        except Exception as e:
            self.logger.error(f"❌ Error generating final synthesis: {type(e).__name__}: {str(e)}")
            self.logger.error(f"❌ Enhanced request preview: {enhanced_final_request[:200]}...")
            self.logger.error(f"❌ Request size: {len(enhanced_final_request)} chars")
            self.logger.error(f"❌ Message history length: {len(message_history.get_messages())} messages")
            
            # Try to extract more details from the error
            if hasattr(e, '__dict__'):
                self.logger.error(f"❌ Error details: {e.__dict__}")
            
            # Check if it's an API error
            if hasattr(e, 'response'):
                self.logger.error(f"❌ API Response: {e.response}")
            if hasattr(e, 'status_code'):
                self.logger.error(f"❌ Status Code: {e.status_code}")
            if hasattr(e, 'body'):
                self.logger.error(f"❌ Error Body: {e.body}")
                
            return f"Error in final synthesis: {type(e).__name__}: {str(e)}"
    
    def _build_collected_data_summary(self) -> str:
        """Build a comprehensive summary of all collected data with specific details"""
        summary_parts = []
        
        # Explanatory Drivers Data
        if 'explanatory_drivers' in self.collected_data:
            drivers_data = self.collected_data['explanatory_drivers']
            summary_parts.append(f"🔍 **EXPLANATORY DRIVERS EJECUTADO:**")
            if isinstance(drivers_data, dict):
                summary_parts.append(f"   📊 Encuestas analizadas: {drivers_data.get('survey_count', 'N/A')}")
                significant_drivers = drivers_data.get('significant_drivers', [])
                if significant_drivers:
                    summary_parts.append(f"   🎯 Drivers significativos: {significant_drivers}")
                operational_drivers = drivers_data.get('operational_drivers', [])
                if operational_drivers:
                    summary_parts.append(f"   ⚙️ Drivers operacionales: {operational_drivers}")
                product_drivers = drivers_data.get('product_drivers', [])
                if product_drivers:
                    summary_parts.append(f"   🛎️ Drivers de producto/servicio: {product_drivers}")
            else:
                summary_parts.append(f"   {drivers_data}")
        
        # Verbatims Data
        if 'verbatims' in self.collected_data:
            verbatims_data = self.collected_data['verbatims']
            summary_parts.append(f"💬 **VERBATIMS EJECUTADO:**")
            summary_parts.append(f"   {verbatims_data}")
        elif 'verbatims_conversation' in self.collected_data:
            conversation_data = self.collected_data['verbatims_conversation']
            summary_parts.append(f"💬 **CONVERSACIÓN CHATBOT EJECUTADA:**")
            summary_parts.append(f"   📡 Fuente: {conversation_data.get('source', 'Unknown')}")
            summary_parts.append(f"   🔄 Total intercambios: {conversation_data.get('total_exchanges', 0)}")
            summary_parts.append(f"   📊 Total verbatims analizados: {conversation_data.get('total_data_points', 0)}")
            summary_parts.append(f"   🎯 Tipo de verbatim: {conversation_data.get('verbatim_type', 'N/A')}")
            # Include key insights from conversation
            conversation_log = conversation_data.get('conversation_log', [])
            if conversation_log:
                summary_parts.append(f"   💡 Principales hallazgos del chatbot:")
                for i, exchange in enumerate(conversation_log[:3], 1):  # First 3 exchanges
                    response = exchange.get('response', '')[:200] + '...' if len(exchange.get('response', '')) > 200 else exchange.get('response', '')
                    summary_parts.append(f"      Q{i}: {response}")
        
        # NCS Data
        if 'ncs_data' in self.collected_data:
            ncs_data = self.collected_data['ncs_data']
            summary_parts.append(f"🚨 **NCS EJECUTADO:**")
            if isinstance(ncs_data, dict):
                summary_parts.append(f"   🔍 Causas identificadas: {ncs_data.get('identified_causes', [])}")
                summary_parts.append(f"   🛫 Rutas afectadas: {ncs_data.get('affected_routes', [])}")
                summary_parts.append(f"   📅 Días analizados: {ncs_data.get('days_analyzed', 'N/A')}")
                summary_parts.append(f"   ⚙️ Estado fuente datos: {ncs_data.get('data_source_status', 'N/A')}")
                analysis_summary = ncs_data.get('analysis_summary', 'No disponible')
                if len(analysis_summary) > 300:
                    analysis_summary = analysis_summary[:300] + '...'
                summary_parts.append(f"   📊 Análisis: {analysis_summary}")
            else:
                summary_parts.append(f"   {ncs_data}")
        
        # Routes Data - Enhanced comprehensive analysis
        if 'routes_data' in self.collected_data:
            routes_data = self.collected_data['routes_data']
            summary_parts.append(f"🛫 **ROUTES EJECUTADO - ANÁLISIS CONSOLIDADO:**")
            if isinstance(routes_data, dict):
                summary_parts.append(f"   📊 Total rutas únicas analizadas: {routes_data.get('total_routes', 0)}")
                
                # Summary by source
                exp_drivers_count = len(routes_data.get('exp_drivers_routes', {}).get('routes', []))
                ncs_count = len(routes_data.get('ncs_routes', {}).get('routes', []))
                verbatims_count = len(routes_data.get('verbatims_routes', {}).get('routes', []))
                
                summary_parts.append(f"   🎯 Distribución por fuente:")
                summary_parts.append(f"      • Explanatory Drivers: {exp_drivers_count} rutas")
                summary_parts.append(f"      • NCS Incidentes: {ncs_count} rutas")
                summary_parts.append(f"      • Verbatims Clientes: {verbatims_count} rutas")
                
                # All routes consolidated
                all_routes = routes_data.get('all_routes', {})
                if all_routes:
                    summary_parts.append(f"   📋 Rutas consolidadas:")
                    for route_name, route_data in list(all_routes.items())[:5]:  # Show first 5
                        sources_str = ", ".join(route_data.get('sources', []))
                        vs_str = f", VS {route_data['vs']}" if route_data.get('vs') is not None else ""
                        touchpoint_str = ""
                        if route_data.get('touchpoint_scores'):
                            touchpoint_scores = ", ".join([f"{tp}: {score}" for tp, score in route_data['touchpoint_scores'].items()])
                            touchpoint_str = f", [{touchpoint_scores}]"
                        summary_parts.append(f"      • {route_name}: NPS {route_data['nps']}, Pax {route_data['pax']}{vs_str}{touchpoint_str} (Fuentes: {sources_str})")
                
                # Similarities analysis
                similarities = routes_data.get('similarities_analysis', '')
                if similarities:
                    similarities_summary = similarities[:200] + '...' if len(similarities) > 200 else similarities
                    summary_parts.append(f"   🔍 Análisis similitudes: {similarities_summary}")
            else:
                summary_parts.append(f"   {routes_data}")
        
        # Customer Profile Data
        if 'customer_profile' in self.collected_data:
            profile_data = self.collected_data['customer_profile']
            summary_parts.append(f"👥 **CUSTOMER PROFILE EJECUTADO:**")
            if len(str(profile_data)) > 400:
                profile_summary = str(profile_data)[:400] + '...'
            else:
                profile_summary = str(profile_data)
            summary_parts.append(f"   {profile_summary}")
        
        if not summary_parts:
            return "❌ No se recolectaron datos durante la investigación"
        
        return "\n".join(summary_parts)
    
    def get_conversation_log(self) -> List[Dict]:
        """Get the conversation log"""
        return self.tracker.conversation_log
    
    def export_conversation(self, filename: Optional[str] = None, node_path: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None) -> str:
        """Export the conversation log to JSON file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if filename is None:
                # Create a descriptive filename with period and segment
                safe_node_path = node_path.replace('/', '_') if node_path else "unknown"
                period_info = f"{start_date}_{end_date}" if start_date and end_date else timestamp[:8]
                filename = f"causal_{period_info}_{safe_node_path}_{timestamp}.json"
            
            # Create agent_conversations directory structure
            base_dir = Path(__file__).parent.parent.parent.parent.parent / 'dashboard_analyzer' / 'agent_conversations' / 'causal_explanation'
            base_dir.mkdir(parents=True, exist_ok=True)
            
            full_path = base_dir / filename
            
            conversation_data = {
            "metadata": {
                            "agent_type": "causal_explanation",
                            "analysis_type": "separated_workflow_investigation",
                "export_timestamp": datetime.now().isoformat(),
                            "node_path": node_path,
                            "start_date": start_date,
                            "end_date": end_date,
                "total_iterations": self.tracker.iteration_count,
                "llm_type": self.llm_type.value,
                            "anomaly_type": self.current_anomaly_type,
                            "total_messages": len(self.tracker.conversation_log),
                            "tools_used": list(set([msg.get('metadata', {}).get('tool_name') for msg in self.tracker.conversation_log if msg.get('metadata', {}).get('tool_name')])),
                            "investigation_success": len(self.tracker.previous_explanations) > 0
            },
            "conversation_log": self.tracker.conversation_log,
                        "clean_explanations": self.tracker.previous_explanations,
                        "collected_data_summary": self._build_collected_data_summary() if hasattr(self, 'collected_data') else {},
                        "conversation_summary": self._get_conversation_summary()
        }
        
            with open(full_path, 'w', encoding='utf-8') as f:
                json.dump(conversation_data, f, indent=2, ensure_ascii=False)
            self.logger.info(f"📝 Conversation exported to: {full_path}")
            return str(full_path)
        except Exception as e:
            self.logger.error(f"❌ Failed to export conversation: {e}")
            return ""
    
    def _get_conversation_summary(self) -> Dict[str, int]:
        """Get summary of conversation message types"""
        summary = {}
        for entry in self.tracker.conversation_log:
            msg_type = entry['type']
            summary[msg_type] = summary.get(msg_type, 0) + 1
        return summary

    async def _filter_ncs_by_segment(self, ncs_data: pd.DataFrame, node_path: str) -> pd.DataFrame:
        """
        Simple NCS filtering by segment characteristics without external dependencies.
        Focuses on the specific incidents for the analyzed segment.
        """
        try:
            # Check if we have NCS data to process
            if ncs_data.empty:
                return ncs_data
            
            # Get the first column (usually contains incident text)
            incident_col = ncs_data.columns[0] if len(ncs_data.columns) > 0 else None
            if incident_col is None:
                return ncs_data
            
            self.logger.info(f"Starting NCS filtering for segment: {node_path}")
            self.logger.info(f"Total NCS incidents to filter: {len(ncs_data)}")
            
            # Get segment filters to understand what routes/characteristics are relevant
            cabins, companies, hauls = self.pbi_collector._get_node_filters(node_path)
            
            # Apply contextual filtering based on segment characteristics
            filtered_ncs = await self._apply_contextual_filtering(ncs_data, node_path)
            
            # Log filtering results
            if len(filtered_ncs) < len(ncs_data):
                reduction_rate = (1 - len(filtered_ncs) / len(ncs_data)) * 100
                self.logger.info(f"Filtered NCS data for {node_path}: {len(filtered_ncs)}/{len(ncs_data)} incidents ({reduction_rate:.1f}% reduction)")
            else:
                self.logger.info(f"No filtering applied - returning all {len(ncs_data)} incidents for analysis")
            
            return filtered_ncs
            
        except Exception as e:
            self.logger.error(f"Error in NCS segment filtering: {str(e)}")
            # Return original data on error to ensure analysis continues
            return ncs_data
    
    async def _apply_contextual_filtering(self, ncs_data: pd.DataFrame, node_path: str) -> pd.DataFrame:
        """
        Apply contextual filtering with the correct NCS logic:
        1. ALWAYS filter by haul (Global, LH, SH) based on routes/airports
        2. ONLY filter by cabin when we're at cabin level AND the incident specifies it affects ONLY another cabin
        3. NEVER discard incidents just because they don't mention cabin
        """
        try:
            # Get segment filters
            cabins, companies, hauls = self.pbi_collector._get_node_filters(node_path)
            
            if ncs_data.empty or len(ncs_data.columns) == 0:
                return ncs_data
            
            incident_col = ncs_data.columns[0]
            filtered_ncs = ncs_data.copy()
            
            # STEP 1: ALWAYS apply haul-based filtering using Routes Dictionary (Global, LH, SH)
            if hauls and len(hauls) == 1:
                haul_type = hauls[0]
                
                # Use routes dictionary instead of hardcoded keywords
                filtered_ncs = await self._filter_using_routes_dictionary(
                    filtered_ncs, haul_type, incident_col
                )
            
            # STEP 2: Apply cabin filtering ONLY when we're at cabin level AND need to exclude incidents that affect ONLY other cabins
            if cabins and len(cabins) == 1:
                cabin_type = cabins[0].lower()
                
                # Define keywords for each cabin type
                cabin_keywords = {
                    'business': ['business', 'ejecutiva', 'premium', 'preferente', 'clase.*business'],
                    'economy': ['economy', 'turista', 'económica', 'clase.*turista'],
                    'premium': ['premium', 'preferente', 'plus', 'premium.*economy']
                }
                
                if cabin_type in cabin_keywords:
                    # Find incidents that mention OTHER cabins (to potentially exclude them)
                    other_cabin_patterns = []
                    for other_cabin, keywords in cabin_keywords.items():
                        if other_cabin != cabin_type:
                            other_cabin_patterns.extend(keywords)
                    
                    if other_cabin_patterns:
                        # Pattern to find incidents that mention ONLY other cabins (exclusive language)
                        exclusive_keywords = ['solo', 'solamente', 'únicamente', 'exclusivamente', 'solo.*clase', 'solo.*cabina']
                        exclusive_pattern = '|'.join([f'\\b{kw}\\b' for kw in exclusive_keywords])
                        
                        # Combine patterns to find incidents that mention other cabins with exclusive language
                        other_cabin_pattern = '|'.join([f'\\b{kw}\\b' for kw in other_cabin_patterns])
                        combined_pattern = f"({exclusive_pattern}).*({other_cabin_pattern})|({other_cabin_pattern}).*({exclusive_pattern})"
                        
                        # Find incidents to potentially exclude
                        exclusive_mask = filtered_ncs[incident_col].str.contains(combined_pattern, na=False, regex=True, case=False)
                        incidents_to_exclude = filtered_ncs[exclusive_mask]
                        
                        if len(incidents_to_exclude) > 0:
                            self.logger.info(f"Cabin exclusion filtering: {len(incidents_to_exclude)} incidents mention ONLY other cabins, excluding them")
                            # Remove these incidents from our filtered data
                            filtered_ncs = filtered_ncs[~exclusive_mask]
                        
                        self.logger.info(f"After cabin filtering: {len(filtered_ncs)} incidents remain (keeping incidents that don't specify cabin or affect our cabin)")
            
            # STEP 3: If no incidents remain after filtering, return original data for Global analysis
            if len(filtered_ncs) == 0 and "Global" in node_path:
                self.logger.info("No incidents remain after filtering, returning all NCS data for Global analysis")
                return ncs_data
            
            self.logger.info(f"Final NCS filtering result: {len(filtered_ncs)}/{len(ncs_data)} incidents after contextual filtering")
            return filtered_ncs
            
        except Exception as e:
            self.logger.error(f"Error in contextual filtering: {str(e)}")
            return ncs_data

    async def _extract_ncs_causal_insights_workflow_aware(self, filtered_ncs_data: pd.DataFrame, node_path: str, anomaly_type: str) -> dict:
        """
        Extract causal insights from NCS data with workflow awareness:
        1. Classify incidents as operative vs product-related
        2. Filter by current workflow type
        3. Interpret based on anomaly direction
        4. Handle workflow mismatches by finding operational causes of product issues
        """
        try:
            if filtered_ncs_data.empty:
                return {
                    'identified_causes': [],
                    'affected_routes': [],
                    'route_impact_summary': {},
                    'touchpoint_correlations': {},
                    'confidence_level': 'low'
                }
            
            incident_col = filtered_ncs_data.columns[0] if len(filtered_ncs_data.columns) > 0 else None
            if incident_col is None:
                return {
                    'identified_causes': [],
                    'affected_routes': [],
                    'route_impact_summary': {},
                    'touchpoint_correlations': {},
                    'confidence_level': 'low'
                }
            
            # Combine all incident text for analysis
            all_incidents_text = "\n".join(filtered_ncs_data[incident_col].astype(str).tolist())
            
            # 1. EXTRACT STRUCTURED NCS DATA (categorías, motivos, rutas, vuelos)
            structured_ncs_data = self._extract_structured_ncs_data(all_incidents_text)
            
            # 2. CLASSIFY INCIDENTS by nature (operative vs product)
            incident_classification = self._classify_ncs_incidents_by_nature(all_incidents_text)
            
            # 3. LOG STRUCTURED NCS DATA for visibility
            self.logger.info(f"📊 NCS STRUCTURED DATA EXTRACTED:")
            self.logger.info(f"   - Categories: {structured_ncs_data.get('categories', {})}")
            self.logger.info(f"   - Total incidents: {structured_ncs_data.get('summary', {}).get('total_incidents', 0)}")
            self.logger.info(f"   - Most affected route: {structured_ncs_data.get('summary', {}).get('most_affected_route', 'None')}")
            self.logger.info(f"   - Main motive: {structured_ncs_data.get('summary', {}).get('main_motive', 'None')}")
            self.logger.info(f"   - Total passengers affected: {structured_ncs_data.get('passenger_impact', {}).get('total', 0)}")
            self.logger.info(f"   - Average delay: {structured_ncs_data.get('delay_statistics', {}).get('avg_delay', 0)} min")
            
            # 4. DETERMINE CURRENT WORKFLOW TYPE from explanatory drivers
            current_workflow = self._determine_current_workflow_type()
            
            # 3. HANDLE WORKFLOW MATCHING WITH SMART CORRELATION
            workflow_match = False
            relevant_incidents_text = ""
            incident_nature = "unknown"
            analysis_approach = "direct"
            
            if current_workflow == "operative" and incident_classification['operative_incidents']:
                # Direct match: operative workflow + operative incidents
                relevant_incidents_text = incident_classification['operative_incidents_text']
                incident_nature = "operative"
                workflow_match = True
                analysis_approach = "direct"
            elif current_workflow == "product" and incident_classification['product_incidents']:
                # Direct match: product workflow + product incidents
                relevant_incidents_text = incident_classification['product_incidents_text']
                incident_nature = "product"
                workflow_match = True
                analysis_approach = "direct"
            elif current_workflow == "product" and incident_classification['operative_incidents']:
                # SMART CORRELATION: product issues caused by operative incidents
                relevant_incidents_text = incident_classification['operative_incidents_text']
                incident_nature = "operative_causing_product"
                workflow_match = True  # This is actually a valuable correlation
                analysis_approach = "causal_correlation"
                self.logger.info(f"🔗 SMART CORRELATION: Found operational incidents that likely caused the detected product/service issues")
            elif current_workflow == "operative" and incident_classification['product_incidents']:
                # Less common but possible: operative issues manifest as product improvements
                relevant_incidents_text = incident_classification['product_incidents_text']
                incident_nature = "product_affecting_operative"
                workflow_match = True
                analysis_approach = "reverse_correlation"
            else:
                # Try to use any available incidents with lower confidence
                if incident_classification['operative_incidents']:
                    relevant_incidents_text = incident_classification['operative_incidents_text']
                    incident_nature = "operative"
                    analysis_approach = "fallback"
                elif incident_classification['product_incidents']:
                    relevant_incidents_text = incident_classification['product_incidents_text']
                    incident_nature = "product"
                    analysis_approach = "fallback"
                else:
                    # Truly no usable incidents
                    return {
                    'identified_causes': [],
                    'affected_routes': [],
                    'route_impact_summary': {},
                    'touchpoint_correlations': {},
                        'confidence_level': 'no_relevant_incidents',
                    'workflow_mismatch': True,
                    'current_workflow': current_workflow,
                    'available_incident_types': list(incident_classification.keys())
                }
            
            # 4. EXTRACT INSIGHTS from relevant incidents
            identified_causes = self._identify_disruption_causes(relevant_incidents_text)
            route_analysis = self._extract_route_impacts(relevant_incidents_text)
            touchpoint_correlations = self._correlate_ncs_with_touchpoints(relevant_incidents_text)
            
            # 5. ENHANCE INTERPRETATIONS FOR CAUSAL CORRELATIONS
            if analysis_approach == "causal_correlation":
                # Enhance causes to show operational → product causation
                enhanced_causes = []
                for cause in identified_causes:
                    enhanced_causes.append(f"🔗 OPERATIONAL ROOT CAUSE of product issues: {cause}")
                identified_causes = enhanced_causes
                
                # Add correlation insight
                touchpoint_correlations['causal_insight'] = f"Operational incidents ({len(filtered_ncs_data)} incidents) likely caused the detected product/service touchpoint issues. This is a deeper root cause analysis."
            
            # 6. INTERPRET BASED ON ANOMALY DIRECTION
            interpreted_causes = self._interpret_causes_by_anomaly_direction(
                identified_causes, incident_nature, anomaly_type
            )
            
            # 7. ASSESS CONFIDENCE LEVEL (boost confidence for smart correlations)
            base_confidence = self._assess_ncs_confidence(
                len(filtered_ncs_data), 
                len(interpreted_causes), 
                len(route_analysis['affected_routes'])
            )
            
            # Adjust confidence based on analysis approach
            if analysis_approach == "causal_correlation":
                if "low" in base_confidence:
                    confidence_level = base_confidence.replace("low", "medium")
                elif "medium" in base_confidence:
                    confidence_level = base_confidence.replace("medium", "high")
                else:
                    confidence_level = base_confidence
                confidence_level += " (enhanced by operational-product correlation)"
            else:
                confidence_level = base_confidence
            
            return {
                'identified_causes': interpreted_causes,
                'affected_routes': route_analysis['affected_routes'],
                'route_impact_summary': route_analysis['route_impact_summary'],
                'touchpoint_correlations': touchpoint_correlations,
                'confidence_level': confidence_level,
                'incident_nature': incident_nature,
                'workflow_match': workflow_match,
                'analysis_approach': analysis_approach,
                'current_workflow': current_workflow
            }
            
        except Exception as e:
            self.logger.error(f"Error extracting workflow-aware NCS causal insights: {str(e)}")
            return {
                'identified_causes': [],
                'affected_routes': [],
                'route_impact_summary': {},
                'touchpoint_correlations': {},
                'confidence_level': 'low'
            }

    # Simplified stub methods for NCS analysis - these can be enhanced later
    def _classify_ncs_incidents_by_nature(self, incidents_text: str) -> dict:
        """Classify NCS incidents as operative vs product-related."""
        return {
            'operative_incidents': True,
            'product_incidents': False,
            'operative_incidents_text': incidents_text,
            'product_incidents_text': ""
        }
    
    def _determine_current_workflow_type(self) -> str:
        """Determine workflow type from explanatory drivers."""
        explanatory_data = str(self.collected_data.get('explanatory_drivers', ''))
        if 'punctuality' in explanatory_data.lower() or 'otp' in explanatory_data.lower():
            return 'operative'
        elif 'crew' in explanatory_data.lower() or 'food' in explanatory_data.lower():
            return 'product'
        else:
            return 'unknown'
    
    def _identify_disruption_causes(self, incidents_text: str) -> list:
        """Extract disruption causes from incident text."""
        causes = []
        if 'delay' in incidents_text.lower():
            causes.append('Flight delays')
        if 'cancel' in incidents_text.lower():
            causes.append('Flight cancellations')
        if 'weather' in incidents_text.lower():
            causes.append('Weather disruptions')
        if 'maintenance' in incidents_text.lower():
            causes.append('Maintenance issues')
        return causes or ['Operational incidents detected']
    
    def _extract_route_impacts(self, incidents_text: str) -> dict:
        """Extract affected routes from incident text with enhanced patterns for LH routes."""
        import re
        
        routes = []
        route_impact_summary = {}
        
        # Enhanced route patterns for long-haul routes
        # Pattern 1: Standard XXX-YYY format
        route_pattern = r'\b([A-Z]{3})\s*[-–]\s*([A-Z]{3})\b'
        route_matches = re.findall(route_pattern, incidents_text, re.IGNORECASE)
        
        for origin, dest in route_matches:
            route_code = f"{origin.upper()}-{dest.upper()}"
            routes.append(route_code)
            route_impact_summary[route_code] = 'Route-specific operational incidents'
        
        # Pattern 2: Individual airport codes mentioned (for LH segment)
        lh_airports = {
            # Americas
            'JFK': 'New York', 'MIA': 'Miami', 'EZE': 'Buenos Aires', 'BOG': 'Bogotá',
            'LIM': 'Lima', 'SCL': 'Santiago', 'GRU': 'São Paulo', 'MEX': 'Mexico City',
            'ORD': 'Chicago', 'DFW': 'Dallas', 'LAX': 'Los Angeles', 'CCS': 'Caracas',
            'SDQ': 'Santo Domingo', 'HAV': 'Havana', 'BOS': 'Boston', 'YUL': 'Montreal',
            # Africa/Middle East  
            'CAI': 'Cairo', 'JNB': 'Johannesburg', 'CMN': 'Casablanca', 'ALG': 'Algiers',
            'TUN': 'Tunis', 'DAR': 'Dar es Salaam', 'ADD': 'Addis Ababa',
            # Asia/Pacific
            'NRT': 'Tokyo', 'PVG': 'Shanghai', 'ICN': 'Seoul', 'BKK': 'Bangkok',
            'SIN': 'Singapore', 'HKG': 'Hong Kong', 'DEL': 'Delhi', 'BOM': 'Mumbai'
        }
        
        # Look for specific LH airport mentions
        for airport_code, city_name in lh_airports.items():
            if re.search(rf'\b{airport_code}\b', incidents_text, re.IGNORECASE):
                # Create route as MAD-XXX (assuming MAD as hub)
                route_code = f"MAD-{airport_code}"
                if route_code not in routes:
                    routes.append(route_code)
                    route_impact_summary[route_code] = f'Incidents affecting {city_name} route'
        
        # Pattern 3: City/country names to airport mapping
        city_to_airport = {
            'new york': 'JFK', 'miami': 'MIA', 'buenos aires': 'EZE', 'bogota': 'BOG',
            'lima': 'LIM', 'santiago': 'SCL', 'sao paulo': 'GRU', 'mexico': 'MEX',
            'chicago': 'ORD', 'dallas': 'DFW', 'los angeles': 'LAX', 'caracas': 'CCS',
            'tokyo': 'NRT', 'shanghai': 'PVG', 'seoul': 'ICN', 'bangkok': 'BKK'
        }
        
        for city_name, airport_code in city_to_airport.items():
            if re.search(rf'\b{city_name}\b', incidents_text, re.IGNORECASE):
                route_code = f"MAD-{airport_code}"
                if route_code not in routes:
                    routes.append(route_code)
                    route_impact_summary[route_code] = f'Incidents mentioned for {city_name.title()}'
        
        # Deduplicate routes
        unique_routes = list(dict.fromkeys(routes))
        
        return {
            'affected_routes': unique_routes,
            'route_impact_summary': route_impact_summary
        }
    
    def _correlate_ncs_with_touchpoints(self, incidents_text: str) -> dict:
        """Correlate NCS incidents with known touchpoints."""
        correlations = {}
        if 'punctuality' in incidents_text.lower():
            correlations['Punctuality'] = 'NCS incidents affecting punctuality'
        if 'boarding' in incidents_text.lower():
            correlations['Boarding'] = 'NCS incidents affecting boarding'
        return correlations
    
    def _interpret_causes_by_anomaly_direction(self, identified_causes: list, incident_nature: str, anomaly_type: str) -> list:
        """Interpret causes based on anomaly direction."""
        return identified_causes  # Simple passthrough for now
    
    def _get_routes_query_for_date_range(self, cabins: List[str], companies: List[str], hauls: List[str], start_date: datetime, end_date: datetime) -> str:
        """Generate DAX query for routes data using date range and Rutas.txt template."""
        try:
            # Load the routes template from PBI collector
            template = self.pbi_collector._load_query_template("Rutas.txt")
            
            # Replace placeholders with actual values
            cabins_str = '", "'.join(cabins)
            companies_str = '", "'.join(companies)
            hauls_str = '", "'.join(hauls)
            
            # Replace the template placeholders
            query = template.replace(
                'TREATAS({"Business", "Economy", "Premium EC"}, \'Cabin_Master\'[Cabin_Show])',
                f'TREATAS({{"{cabins_str}"}}, \'Cabin_Master\'[Cabin_Show])'
            ).replace(
                'TREATAS({"IB","YW"}, \'Company_Master\'[Company])',
                f'TREATAS({{"{companies_str}"}}, \'Company_Master\'[Company])'
            ).replace(
                'TREATAS({"SH","LH"}, \'Haul_Master\'[Haul_Aggr])',
                f'TREATAS({{"{hauls_str}"}}, \'Haul_Master\'[Haul_Aggr])'
            ).replace(
                '\'Date_Master\'[Date] =date(2025,05,12)',
                f'\'Date_Master\'[Date] >= date({start_date.year},{start_date.month},{start_date.day}) && \'Date_Master\'[Date] <= date({end_date.year},{end_date.month},{end_date.day})'
            )
            
            return query
            
        except Exception as e:
            self.logger.error(f"Error generating routes query: {e}")
            # Fallback: return a basic query structure if template fails
            return f"""
            EVALUATE
            SUMMARIZECOLUMNS(
                'Route_Master'[route],
                'Measure'[NPS (Route)],
                'Measure'[n (Route)]
            )
            """
    
    def _get_ncs_routes_query(self, ncs_routes: List[str], cabins: List[str], companies: List[str], hauls: List[str], start_date, end_date) -> str:
        """
        Generate simplified DAX query for NCS-specific routes using date range filter.
        This is different from the general routes query and filters for specific routes.
        """
        try:
            # Create route filter for specific NCS routes
            routes_str = '", "'.join(ncs_routes)
            cabins_str = '", "'.join(cabins)
            companies_str = '", "'.join(companies)
            hauls_str = '", "'.join(hauls)
            
            # Convert datetime to date components
            if hasattr(start_date, 'year'):
                start_year, start_month, start_day = start_date.year, start_date.month, start_date.day
                end_year, end_month, end_day = end_date.year, end_date.month, end_date.day
            else:
                # Fallback for string dates
                from datetime import datetime
                start_dt = datetime.strptime(str(start_date)[:10], '%Y-%m-%d')
                end_dt = datetime.strptime(str(end_date)[:10], '%Y-%m-%d')
                start_year, start_month, start_day = start_dt.year, start_dt.month, start_dt.day
                end_year, end_month, end_day = end_dt.year, end_dt.month, end_dt.day
            
            # Simplified DAX query with date range filter (for NCS and verbatims routes)
            query = f"""
DEFINE
    VAR __DS0FilterTable =
        TREATAS({{"{cabins_str}"}}, 'Cabin_Master'[Cabin_Show])
    
    VAR __DS0FilterTable2 =
        TREATAS({{"{companies_str}"}}, 'Company_Master'[Company])
    
    VAR __DS0FilterTable3 =
        TREATAS({{"{hauls_str}"}}, 'Haul_Master'[Haul_Aggr])
    
    VAR __DS0FilterTableRoutes =
        TREATAS({{"{routes_str}"}}, 'Route_Master'[route])

EVALUATE
SUMMARIZECOLUMNS(
    'Route_Master'[route],
    __DS0FilterTable,
    __DS0FilterTable2,
    __DS0FilterTable3,
    __DS0FilterTableRoutes,
    FILTER('Date_Master', 'Date_Master'[Date] >= date({start_year},{start_month},{start_day}) && 'Date_Master'[Date] <= date({end_year},{end_month},{end_day})),
    "NPS", 'Measure'[NPS (Route)],
    "VS", [Monthly_Satisfaction],
    "Pax", 'Measure'[n (Route)]
)
ORDER BY 'Route_Master'[route]
"""
            return query
            
        except Exception as e:
            self.logger.error(f"Error generating NCS routes query: {e}")
            # Fallback: simplified query with route filter
            routes_str = '", "'.join(ncs_routes)
            return f"""
EVALUATE
SUMMARIZECOLUMNS(
    'Route_Master'[route],
    TREATAS({{"{routes_str}"}}, 'Route_Master'[route]),
    "NPS", 'Measure'[NPS (Route)],
    "VS", [Monthly_Satisfaction],
    "Pax", 'Measure'[n (Route)]
)
ORDER BY 'Route_Master'[route]
            """
    
    def _assess_ncs_confidence(self, incident_count: int, cause_count: int, route_count: int) -> str:
        """Assess confidence level of NCS analysis."""
        if incident_count > 5 and cause_count > 0:
            return "high"
        elif incident_count > 2:
            return "medium"
        else:
            return "low"

    def _extract_multiple_causal_touchpoints_from_history(self) -> list:
        """Extract multiple causal touchpoints from analysis history."""
        # Simple placeholder - return empty list for now
        return []

    async def _ncs_reflection_with_agent(self, filtered_ncs_data: pd.DataFrame, node_path: str, anomaly_type: str, total_days: int) -> dict:
        """
        Send filtered NCS data to agent with helper prompt for reflection.
        This bypasses the pattern-matching pipeline and lets the LLM analyze raw data directly.
        """
        try:
            # DEBUG: Log actual data structure
            self.logger.info(f"🔍 DEBUG: NCS data shape: {filtered_ncs_data.shape}")
            self.logger.info(f"🔍 DEBUG: NCS columns: {list(filtered_ncs_data.columns) if not filtered_ncs_data.empty else 'EMPTY'}")
            if not filtered_ncs_data.empty:
                self.logger.info(f"🔍 DEBUG: First few rows:\n{filtered_ncs_data.head(2).to_string()}")
            
            if filtered_ncs_data.empty:
                self.logger.info("❌ DEBUG: NCS data is completely empty after filtering")
                return {
                    'identified_causes': [],
                    'affected_routes': [],
                    'route_impact_summary': {},
                    'touchpoint_correlations': {},
                    'confidence_level': 'no_data',
                    'analysis_summary': 'No NCS incidents found for this segment'
                }
            
            # Get incident column (first column, which may have no name)
            if len(filtered_ncs_data.columns) == 0:
                self.logger.error("❌ DEBUG: No columns found in NCS data")
                return {
                    'identified_causes': [],
                    'affected_routes': [],
                    'route_impact_summary': {},
                    'touchpoint_correlations': {},
                    'confidence_level': 'no_data',
                    'analysis_summary': 'NCS data structure invalid - no columns found'
                }
            
            # Get incident text from first column (handles empty column names)
            incident_col = filtered_ncs_data.columns[0]
            self.logger.info(f"🔍 DEBUG: Using incident column: '{incident_col}' (empty name is normal)")
            
            # Prepare sample of incidents for agent analysis
            incident_count = len(filtered_ncs_data)
            sample_size = min(20, incident_count)  # Show up to 20 incidents
            
            # Extract incidents using iloc to handle empty column names
            sample_incidents = filtered_ncs_data.iloc[:sample_size, 0].tolist()
            
            # Filter out empty/null incidents
            sample_incidents = [str(incident).strip() for incident in sample_incidents if pd.notna(incident) and str(incident).strip()]
            
            self.logger.info(f"🔍 DEBUG: Extracted {len(sample_incidents)} valid incidents from {sample_size} samples")
            
            # ENHANCEMENT: Pre-analyze routes for disruption counting
            all_incidents_text = "\n".join(sample_incidents)
            route_disruption_summary = self._extract_route_disruption_counts(all_incidents_text)
            
            # Create enhanced NCS helper prompt with route disruption data
            ncs_helper_prompt = f"""
🚨 **ANÁLISIS NCS - REFLEXIÓN REQUERIDA**

📊 **DATOS DISPONIBLES:**
- Segmento: {node_path}
- Período: {total_days} días
- Incidentes filtrados: {incident_count} incidentes operacionales
- Tipo de anomalía: {anomaly_type}

📈 **CONTEO DE DISRUPCIONES POR RUTA:**"""
            
            if route_disruption_summary:
                ncs_helper_prompt += "\n"
                for route, count in list(route_disruption_summary.items())[:10]:  # Show top 10
                    ncs_helper_prompt += f"\n   • {route}: {count} disrupciones"
                if len(route_disruption_summary) > 10:
                    ncs_helper_prompt += f"\n   ... y {len(route_disruption_summary) - 10} rutas adicionales"
            else:
                ncs_helper_prompt += "\n   • No se encontraron patrones de ruta claros en los datos"

            ncs_helper_prompt += f"""

📋 **MUESTRA DE INCIDENTES (primeros {sample_size}):**"""
            
            for i, incident in enumerate(sample_incidents, 1):
                # Truncate very long incidents
                incident_text = str(incident)[:200] + "..." if len(str(incident)) > 200 else str(incident)
                ncs_helper_prompt += f"\n{i}. {incident_text}"
            
            if incident_count > sample_size:
                ncs_helper_prompt += f"\n... y {incident_count - sample_size} incidentes adicionales"
            
            ncs_helper_prompt += f"""

🎯 **SOLICITUD DE ANÁLISIS:**

Por favor analiza estos incidentes operacionales y proporciona:

1. **CAUSAS PRINCIPALES**: ¿Qué tipos de problemas operacionales identificas? (retrasos, cancelaciones, problemas técnicos, equipaje, tripulación, etc.)

2. **RUTAS AFECTADAS**: ¿Qué rutas específicas (formato XXX-YYY) menciona en los incidentes? 
   - Usa el conteo de disrupciones arriba para priorizar las rutas más impactadas
   - Explica qué tipo de problemas afectó a cada ruta

3. **CORRELACIÓN CON ANOMALÍA {anomaly_type.upper()}**: 
   - Si anomalía POSITIVA: ¿Los incidentes son aislados/no relevantes, o indican mejoras operacionales?
   - Si anomalía NEGATIVA: ¿Los incidentes explican la caída del NPS? ¿Qué rutas con más disrupciones correlacionan con peor NPS?

4. **TOUCHPOINTS AFECTADOS**: ¿Qué aspectos del viaje impactaron? (puntualidad, equipaje, embarque, tripulación, etc.)

5. **ANÁLISIS CUANTITATIVO**: Conecta los números de disrupciones por ruta con el impacto esperado en NPS

📝 **FORMATO DE RESPUESTA:**
Proporciona un análisis estructurado que pueda usarse para explicar la anomalía NPS, incluyendo datos específicos de disrupciones por ruta.
"""
            
            self.logger.info(f"🤖 Enviando {incident_count} incidentes NCS al agente para reflexión con datos de disrupciones por ruta")
            
            # Check if we have valid incidents
            if not sample_incidents:
                self.logger.error("❌ DEBUG: No valid incidents found after extraction and filtering")
                return {
                    'identified_causes': [],
                    'affected_routes': [],
                    'route_impact_summary': {},
                    'touchpoint_correlations': {},
                    'confidence_level': 'no_data',
                    'analysis_summary': 'No valid NCS incidents found after extraction'
                }
            
            # Use the existing LLM to analyze the incidents
            from ..message_history import MessageHistory  
            from ..utils.enums import MessageType
            
            message_history = MessageHistory(logger=self.logger)
            
            # System prompt for NCS analysis
            system_prompt = """Eres un experto analista de incidentes operacionales de aerolíneas. 
Tu tarea es analizar incidentes NCS (Network Control Center) y extraer insights causales relevantes para anomalías de NPS.

Enfócate en:
- Identificar causas operacionales concretas con datos cuantitativos
- Extraer rutas específicas afectadas con conteos de disrupciones
- Correlacionar incidentes con impacto en satisfacción del cliente
- Distinguir entre incidentes relevantes vs aislados
- Usar los datos de conteo de disrupciones para priorizar análisis

Proporciona análisis estructurado, específico y respaldado por números."""
            
            message_history.create_and_add_message(
                content=system_prompt,
                message_type=MessageType.SYSTEM
            )
            
            message_history.create_and_add_message(
                content=ncs_helper_prompt,
                message_type=MessageType.USER
            )
            
            # Get LLM analysis
            self.logger.info(f"🔄 DEBUG: About to call LLM with {len(sample_incidents)} incidents and route disruption data...")
            
            response, _, _ = await self.agent.invoke(
                messages=message_history.get_messages(),
                tools=[],  # No tools needed for this reflection
                structured_output=None
            )
            
            llm_analysis = str(response.content) if response.content is not None else "No analysis provided"
            
            self.logger.info(f"✅ Reflexión NCS completada: {len(llm_analysis)} caracteres")
            self.logger.info(f"🔍 DEBUG: LLM response preview: {llm_analysis[:200]}...")
            
            # Extract structured data from LLM response (simple extraction)
            identified_causes = self._extract_causes_from_llm_response(llm_analysis)
            affected_routes = self._extract_routes_from_llm_response(llm_analysis)
            
            self.logger.info(f"🔍 DEBUG: Extracted {len(identified_causes)} causes and {len(affected_routes)} routes")
            
            return {
                'identified_causes': identified_causes,
                'affected_routes': affected_routes,
                'route_impact_summary': {route: f'Incident reported in NCS analysis - {route_disruption_summary.get(route, 0)} disruptions' for route in affected_routes},
                'touchpoint_correlations': self._extract_touchpoints_from_llm_response(llm_analysis),
                'confidence_level': 'high_agent_analysis',
                'analysis_summary': llm_analysis,
                'incident_count': incident_count,
                'sample_size': sample_size,
                'route_disruption_counts': route_disruption_summary,
                'method': 'agent_reflection'
            }
            
        except Exception as e:
            self.logger.error(f"Error in NCS agent reflection: {str(e)}")
            return {
                'identified_causes': [],
                'affected_routes': [],
                'route_impact_summary': {},
                'touchpoint_correlations': {},
                'confidence_level': 'error',
                'analysis_summary': f'Error en reflexión NCS: {str(e)}',
                'method': 'agent_reflection_failed'
            }

    def _extract_structured_ncs_data(self, incidents_text: str) -> dict:
        """Extract structured NCS data with categories, motives, routes, and aggregated counts"""
        import re
        
        structured_data = {
            "categories": {},
            "route_disruptions": {},
            "motives_breakdown": {},
            "operator_breakdown": {},
            "passenger_impact": {"j_class": 0, "w_class": 0, "y_class": 0, "total": 0},
            "delay_statistics": {"total_minutes": 0, "count": 0, "avg_delay": 0},
            "summary": {}
        }
        
        # Extract category totals (Cancelaciones, Retrasos, Desvíos, etc.)
        category_patterns = {
            "cancelaciones": r'Cancelaciones\s*Total\s*(\d+)',
            "retrasos": r'Retrasos\s*Total\s*(\d+)', 
            "desvios": r'Desvíos\s*Total\s*(\d+)',
            "otras_incidencias": r'Otras incidencias\s*Total\s*(\d+)',
            "limitacion_aeronave": r'Limitación de la aeronave\s*Total\s*(\d+)'
        }
        
        for category, pattern in category_patterns.items():
            match = re.search(pattern, incidents_text, re.IGNORECASE)
            if match:
                structured_data["categories"][category] = int(match.group(1))
        
        # Extract route patterns with incident type breakdown
        route_pattern = r'\b([A-Z]{3})\s*[-–]\s*([A-Z]{3})\b'
        
        # Enhanced route extraction with incident type classification
        route_incident_breakdown = {}
        
        # Split text into sections by incident type for better classification
        sections = {
            'cancelaciones': re.findall(r'Cancelaciones.*?(?=Desvíos|Retrasos|Otras incidencias|Limitación|\Z)', incidents_text, re.DOTALL | re.IGNORECASE),
            'desvios': re.findall(r'Desvíos.*?(?=Cancelaciones|Retrasos|Otras incidencias|Limitación|\Z)', incidents_text, re.DOTALL | re.IGNORECASE),
            'retrasos': re.findall(r'Retrasos.*?(?=Cancelaciones|Desvíos|Otras incidencias|Limitación|\Z)', incidents_text, re.DOTALL | re.IGNORECASE),
            'otras_incidencias': re.findall(r'Otras incidencias.*?(?=Cancelaciones|Desvíos|Retrasos|Limitación|\Z)', incidents_text, re.DOTALL | re.IGNORECASE),
            'limitacion_aeronave': re.findall(r'Limitación de la aeronave.*?(?=Cancelaciones|Desvíos|Retrasos|Otras incidencias|\Z)', incidents_text, re.DOTALL | re.IGNORECASE)
        }
        
        # Process each section to extract routes by incident type
        for incident_type, sections_text in sections.items():
            for section in sections_text:
                routes_in_section = re.findall(route_pattern, section, re.IGNORECASE)
                for origin, dest in routes_in_section:
                    route_code = f"{origin.upper()}-{dest.upper()}"
                    
                    if route_code not in route_incident_breakdown:
                        route_incident_breakdown[route_code] = {
                            'cancelaciones': 0, 'desvios': 0, 'retrasos': 0, 
                            'otras_incidencias': 0, 'limitacion_aeronave': 0, 'total': 0
                        }
                    
                    route_incident_breakdown[route_code][incident_type] += 1
                    route_incident_breakdown[route_code]['total'] += 1
        
        # Fallback: if no structured sections found, do general route extraction
        if not route_incident_breakdown:
            route_matches = re.findall(route_pattern, incidents_text, re.IGNORECASE)
            for origin, dest in route_matches:
                route_code = f"{origin.upper()}-{dest.upper()}"
                structured_data["route_disruptions"][route_code] = structured_data["route_disruptions"].get(route_code, 0) + 1
        else:
            # Use the detailed breakdown
            for route, breakdown in route_incident_breakdown.items():
                structured_data["route_disruptions"][route] = breakdown['total']
            
            # Store detailed breakdown separately
            structured_data["route_incident_breakdown"] = route_incident_breakdown
        
        # Extract passenger impact by class
        passenger_patterns = {
            "j_class": r'J\s*(\d+)',
            "w_class": r'W\s*(\d+)', 
            "y_class": r'Y\s*(\d+)'
        }
        
        for class_type, pattern in passenger_patterns.items():
            matches = re.findall(pattern, incidents_text, re.IGNORECASE)
            if matches:
                structured_data["passenger_impact"][class_type] = sum(int(match) for match in matches)
        
        # Calculate total passengers
        structured_data["passenger_impact"]["total"] = (
            structured_data["passenger_impact"]["j_class"] + 
            structured_data["passenger_impact"]["w_class"] + 
            structured_data["passenger_impact"]["y_class"]
        )
        
        # Extract delay minutes for statistics
        delay_pattern = r'(\d+)\s*minutos'
        delay_matches = re.findall(delay_pattern, incidents_text, re.IGNORECASE)
        if delay_matches:
            delays = [int(match) for match in delay_matches]
            structured_data["delay_statistics"]["total_minutes"] = sum(delays)
            structured_data["delay_statistics"]["count"] = len(delays)
            structured_data["delay_statistics"]["avg_delay"] = round(sum(delays) / len(delays), 1) if delays else 0
        
        # Extract common motives
        motive_patterns = {
            "tecnicas": r'causas técnicas|técnicos|mantenimiento',
            "operativas": r'causas operativas|operativo',
            "meteorologia": r'meteorología|meteorológic',
            "rotacion_avion": r'rotación de avión|rotación',
            "atc": r'\bATC\b',
            "equipaje": r'equipaje|maletas'
        }
        
        for motive, pattern in motive_patterns.items():
            count = len(re.findall(pattern, incidents_text, re.IGNORECASE))
            if count > 0:
                structured_data["motives_breakdown"][motive] = count
        
        # Extract operators (Privilege, Iberojet, etc.)
        operator_patterns = {
            "privilege": r'Privilege',
            "iberojet": r'Iberojet', 
            "iberia": r'IB\d+'  # Regular Iberia flights
        }
        
        for operator, pattern in operator_patterns.items():
            count = len(re.findall(pattern, incidents_text, re.IGNORECASE))
            if count > 0:
                structured_data["operator_breakdown"][operator] = count
        
        # Create summary with enhanced multi-day aggregation
        total_incidents = sum(structured_data["categories"].values())
        most_affected_route = max(structured_data["route_disruptions"].items(), key=lambda x: x[1]) if structured_data["route_disruptions"] else None
        main_motive = max(structured_data["motives_breakdown"].items(), key=lambda x: x[1]) if structured_data["motives_breakdown"] else None
        
        # ENHANCED: Multi-day route prioritization for routes_tool
        priority_routes_for_investigation = []
        if structured_data["route_disruptions"]:
            # Sort routes by frequency (most disrupted first)
            sorted_routes = sorted(structured_data["route_disruptions"].items(), key=lambda x: x[1], reverse=True)
            
            # Categorize routes by disruption frequency for investigation priority
            for route, count in sorted_routes:
                if count >= 5:  # High priority: 5+ incidents
                    priority_routes_for_investigation.append({"route": route, "incidents": count, "priority": "HIGH"})
                elif count >= 3:  # Medium priority: 3-4 incidents  
                    priority_routes_for_investigation.append({"route": route, "incidents": count, "priority": "MEDIUM"})
                elif count >= 2:  # Low priority: 2 incidents
                    priority_routes_for_investigation.append({"route": route, "incidents": count, "priority": "LOW"})
        
        structured_data["summary"] = {
            "total_incidents": total_incidents,
            "most_affected_route": most_affected_route,
            "main_motive": main_motive,
            "total_passengers_affected": structured_data["passenger_impact"]["total"],
            "avg_delay_minutes": structured_data["delay_statistics"]["avg_delay"],
            "priority_routes_for_investigation": priority_routes_for_investigation,
            "routes_requiring_nps_analysis": [r["route"] for r in priority_routes_for_investigation if r["priority"] in ["HIGH", "MEDIUM"]]
        }
        
        return structured_data

    def _extract_route_disruption_counts(self, incidents_text: str) -> dict:
        """Extract route disruption counts from incident text for enhanced analysis"""
        import re
        
        route_disruptions = {}
        
        # Enhanced route pattern to capture XXX-YYY format
        route_pattern = r'\b([A-Z]{3})\s*[-–]\s*([A-Z]{3})\b'
        route_matches = re.findall(route_pattern, incidents_text, re.IGNORECASE)
        
        for origin, dest in route_matches:
            route_code = f"{origin.upper()}-{dest.upper()}"
            route_disruptions[route_code] = route_disruptions.get(route_code, 0) + 1
        
        # Enhanced patterns for hub routes (MAD as origin/destination)
        mad_patterns = [
            r'MAD[O-]\s*([A-Z]{3})',  # MAD-XXX or MADO XXX
            r'([A-Z]{3})\s*[-O]\s*MAD',  # XXX-MAD or XXX O MAD  
            r'Madrid\s*[-–]\s*([A-Z]{3})',  # Madrid-XXX
            r'([A-Z]{3})\s*[-–]\s*Madrid',  # XXX-Madrid
        ]
        
        for pattern in mad_patterns:
            matches = re.findall(pattern, incidents_text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    # Handle tuple matches from multiple capture groups
                    for airport in match:
                        if airport and airport != 'MAD':
                            route_code = f"MAD-{airport.upper()}"
                            route_disruptions[route_code] = route_disruptions.get(route_code, 0) + 1
                else:
                    # Single airport code
                    if match and match != 'MAD':
                        route_code = f"MAD-{match.upper()}"
                        route_disruptions[route_code] = route_disruptions.get(route_code, 0) + 1
        
        # Sort by disruption count (highest first)
        sorted_disruptions = dict(sorted(route_disruptions.items(), key=lambda x: x[1], reverse=True))
        
        return sorted_disruptions

    def _extract_causes_from_llm_response(self, llm_response: str) -> list:
        """Extract identified causes from LLM analysis response"""
        import re
        causes = []
        
        # Look for common cause indicators in the response
        cause_patterns = [
            r'retraso[s]?|delay[s]?',
            r'cancelaci[oó]n[es]?|cancellation[s]?',  
            r'problema[s]?\s+t[eé]cnico[s]?|technical\s+issue[s]?',
            r'equipaje|baggage',
            r'tripulaci[oó]n|crew',
            r'embarque|boarding',
            r'mantenimiento|maintenance',
            r'clima|weather'
        ]
        
        for pattern in cause_patterns:
            if re.search(pattern, llm_response, re.IGNORECASE):
                # Extract context around the match
                matches = re.finditer(pattern, llm_response, re.IGNORECASE)
                for match in matches:
                    start = max(0, match.start() - 30)
                    end = min(len(llm_response), match.end() + 30)
                    context = llm_response[start:end].strip()
                    causes.append(context[:100])  # Limit length
                    break  # One example per pattern
        
        return causes[:5]  # Return top 5
    
    def _extract_routes_from_llm_response(self, llm_response: str) -> list:
        """Extract affected routes from LLM analysis response"""
        import re
        
        # Extract routes in XXX-YYY format
        route_pattern = r'\b([A-Z]{3})-([A-Z]{3})\b'
        routes = re.findall(route_pattern, llm_response)
        
        # Convert to route format and deduplicate
        route_list = []
        for origin, dest in routes:
            route = f"{origin}-{dest}"
            if route not in route_list:
                route_list.append(route)
        
        return route_list[:10]  # Return top 10
    
    def _extract_touchpoints_from_llm_response(self, llm_response: str) -> dict:
        """Extract touchpoint correlations from LLM analysis response"""
        import re
        touchpoints = {}
        
        touchpoint_patterns = {
            'Punctuality': r'puntualidad|punctuality|retraso|delay',
            'Baggage': r'equipaje|baggage|maleta',
            'Boarding': r'embarque|boarding|puerta|gate',
            'Crew': r'tripulaci[oó]n|crew|personal',
            'Aircraft': r'avi[oó]n|aircraft|aeronave|t[eé]cnico'
        }
        
        for touchpoint, pattern in touchpoint_patterns.items():
            if re.search(pattern, llm_response, re.IGNORECASE):
                touchpoints[touchpoint] = f'Mentioned in NCS analysis'
        
        return touchpoints

    async def _filter_using_routes_dictionary(self, ncs_data: pd.DataFrame, target_haul: str, incident_col: str) -> pd.DataFrame:
        """
        Filtra NCS usando el diccionario de rutas en lugar de keywords hardcodeados
        
        Args:
            ncs_data: DataFrame con incidentes NCS
            target_haul: Haul objetivo ("LH" o "SH")
            incident_col: Nombre de la columna con texto de incidentes
            
        Returns:
            DataFrame filtrado por rutas del haul objetivo
        """
        try:
            self.logger.info(f"🗺️ Filtering NCS using routes dictionary for haul: {target_haul}")
            
            # 1. Obtener diccionario de rutas
            routes_dict = await self.pbi_collector.collect_routes_dictionary()
            
            if routes_dict.empty:
                self.logger.warning("❌ Routes dictionary is empty, falling back to original data")
                return ncs_data
            
            # 2. Filtrar rutas del haul objetivo
            target_routes = routes_dict[routes_dict['haul_aggr'] == target_haul]
            
            if target_routes.empty:
                self.logger.warning(f"❌ No routes found for haul {target_haul} in dictionary")
                return ncs_data
                
            target_route_codes = target_routes['route'].tolist()
            self.logger.info(f"📊 Found {len(target_route_codes)} routes for {target_haul}")
            
            # 3. Extraer códigos de aeropuerto de las rutas (MAD-BCN → MAD, BCN)
            airport_codes = set()
            for route in target_route_codes:
                if '-' in route:
                    origin, dest = route.split('-', 1)
                    airport_codes.add(origin.strip().upper())
                    airport_codes.add(dest.strip().upper())
            
            if not airport_codes:
                self.logger.warning(f"❌ No airport codes extracted from {target_haul} routes")
                return ncs_data
                
            self.logger.info(f"✈️ Extracted {len(airport_codes)} airport codes for {target_haul}: {sorted(list(airport_codes))[:10]}...")
            
            # 4. Crear patrón regex con códigos reales del diccionario
            # Usar \b para word boundaries para evitar falsos positivos
            pattern = '|'.join([f'\\b{code}\\b' for code in airport_codes])
            
            # 5. Filtrar incidentes que contengan estos códigos de aeropuerto
            mask = ncs_data[incident_col].str.contains(pattern, na=False, regex=True, case=False)
            filtered_data = ncs_data[mask]
            
            # 6. Log resultados
            if len(filtered_data) > 0:
                reduction_rate = (1 - len(filtered_data) / len(ncs_data)) * 100
                self.logger.info(f"✅ {target_haul} dictionary filtering: {len(filtered_data)}/{len(ncs_data)} incidents ({reduction_rate:.1f}% reduction)")
                return filtered_data
            else:
                self.logger.warning(f"⚠️ No incidents found for {target_haul} airports, returning original data")
                return ncs_data
                
        except Exception as e:
            self.logger.error(f"❌ Error filtering with routes dictionary: {e}")
            # Fallback: devolver datos originales para que el análisis continúe
            return ncs_data

    def _combine_and_summarize_ncs_comments(self, current_data: pd.DataFrame, comparison_data: pd.DataFrame, 
                                          current_start: str, current_end: str, 
                                          comparison_start: str, comparison_end: str) -> str:
        """
        Combine and summarize NCS comments from both current and comparison periods.
        This provides operational narrative support for the temporal comparison.
        
        Args:
            current_data: DataFrame with current period NCS data
            comparison_data: DataFrame with comparison period NCS data
            current_start/end: Current period date range
            comparison_start/end: Comparison period date range
            
        Returns:
            String with combined and summarized comments narrative
        """
        try:
            # Extract incident text from both periods
            current_incidents = []
            comparison_incidents = []
            
            if not current_data.empty:
                self.logger.info(f"🔍 DEBUG NCS NARRATIVE: current_data columns: {list(current_data.columns)}")
                incident_col = self._find_column(current_data, ['incident', 'incidents', ''])
                self.logger.info(f"🔍 DEBUG NCS NARRATIVE: incident_col found: {incident_col}")
                if incident_col is not None:
                    current_incidents = current_data[incident_col].astype(str).tolist()
                    self.logger.info(f"🔍 DEBUG NCS NARRATIVE: current_incidents sample: {current_incidents[:3] if current_incidents else 'Empty'}")
            
            if not comparison_data.empty:
                self.logger.info(f"🔍 DEBUG NCS NARRATIVE: comparison_data columns: {list(comparison_data.columns)}")
                incident_col = self._find_column(comparison_data, ['incident', 'incidents', ''])
                self.logger.info(f"🔍 DEBUG NCS NARRATIVE: comparison incident_col found: {incident_col}")
                if incident_col is not None:
                    comparison_incidents = comparison_data[incident_col].astype(str).tolist()
                    self.logger.info(f"🔍 DEBUG NCS NARRATIVE: comparison_incidents sample: {comparison_incidents[:3] if comparison_incidents else 'Empty'}")
            
            # Debug: Check incident data
            self.logger.info(f"🔍 DEBUG NCS NARRATIVE: current_incidents count: {len(current_incidents)}")
            self.logger.info(f"🔍 DEBUG NCS NARRATIVE: comparison_incidents count: {len(comparison_incidents)}")
            
            # Combine all incidents for summary
            all_current_incidents = "\n".join([inc for inc in current_incidents if inc and inc.strip() and inc != 'nan'])
            all_comparison_incidents = "\n".join([inc for inc in comparison_incidents if inc and inc.strip() and inc != 'nan'])
            
            self.logger.info(f"🔍 DEBUG NCS NARRATIVE: all_current_incidents length: {len(all_current_incidents)}")
            self.logger.info(f"🔍 DEBUG NCS NARRATIVE: all_comparison_incidents length: {len(all_comparison_incidents)}")
            
            # Create summary narrative
            summary_parts = []
            
            # Current period summary
            if all_current_incidents:
                current_count = len([inc for inc in current_incidents if inc and inc.strip() and inc != 'nan'])
                summary_parts.append(f"📅 **Período Actual ({current_start} a {current_end}):** {current_count} incidentes operativos")
                
                # Extract key themes from current period
                current_themes = self._extract_operational_themes(all_current_incidents)
                if current_themes:
                    summary_parts.append(f"🔍 **Temas principales:** {', '.join(current_themes)}")
            else:
                # If no detailed incidents available, but we have total count from analysis
                if hasattr(self, '_ncs_total_incidents') and self._ncs_total_incidents > 0:
                    summary_parts.append(f"📅 **Período Actual ({current_start} a {current_end}):** {self._ncs_total_incidents} incidentes registrados (sin detalles narrativos disponibles)")
                else:
                    summary_parts.append(f"📅 **Período Actual ({current_start} a {current_end}):** Sin incidentes registrados")
            
            # Comparison period summary
            if all_comparison_incidents:
                comparison_count = len([inc for inc in comparison_incidents if inc and inc.strip() and inc != 'nan'])
                summary_parts.append(f"📅 **Período Comparativo ({comparison_start} a {comparison_end}):** {comparison_count} incidentes operativos")
                
                # Extract key themes from comparison period
                comparison_themes = self._extract_operational_themes(all_comparison_incidents)
                if comparison_themes:
                    summary_parts.append(f"🔍 **Temas principales:** {', '.join(comparison_themes)}")
            else:
                summary_parts.append(f"📅 **Período Comparativo ({comparison_start} a {comparison_end}):** Sin incidentes registrados")
            
            # Combined narrative
            if all_current_incidents or all_comparison_incidents:
                summary_parts.append("\n📋 **Narrativa Operativa Combinada:**")
                
                # Create combined narrative using LLM if available
                if hasattr(self, 'llm') and self.llm:
                    combined_narrative = self._generate_combined_narrative(
                        all_current_incidents, all_comparison_incidents,
                        current_start, current_end, comparison_start, comparison_end
                    )
                    summary_parts.append(combined_narrative)
                else:
                    # Fallback to simple summary
                    total_current = len([inc for inc in current_incidents if inc and inc.strip() and inc != 'nan'])
                    total_comparison = len([inc for inc in comparison_incidents if inc and inc.strip() and inc != 'nan'])
                    
                    if total_current > 0 or total_comparison > 0:
                        summary_parts.append(f"📊 **Resumen:** {total_current} incidentes en período actual vs {total_comparison} en período comparativo")
                        
                        if total_current > total_comparison:
                            summary_parts.append("📈 **Tendencia:** Aumento en incidentes operativos")
                        elif total_current < total_comparison:
                            summary_parts.append("📉 **Tendencia:** Reducción en incidentes operativos")
                        else:
                            summary_parts.append("➡️ **Tendencia:** Nivel similar de incidentes operativos")
            
            return "\n".join(summary_parts)
            
        except Exception as e:
            self.logger.error(f"Error combining NCS comments: {str(e)}")
            return f"❌ Error al combinar comentarios NCS: {str(e)}"
    
    def _extract_operational_themes(self, incidents_text: str) -> List[str]:
        """Extract key operational themes from NCS incidents text"""
        if not incidents_text or not incidents_text.strip():
            return []
        
        themes = []
        text_lower = incidents_text.lower()
        
        # Define theme keywords
        theme_keywords = {
            'cancelaciones': ['cancelado', 'cancelación', 'cancelados'],
            'retrasos': ['retraso', 'retrasos', 'demora', 'demoras'],
            'desvios': ['desvío', 'desvios', 'desviado'],
            'equipos': ['a330', 'a350', 'a359', 'equipo', 'aircraft'],
            'conexiones': ['conexión', 'conexiones', 'conecta'],
            'técnicos': ['técnico', 'técnica', 'técnicas', 'técnicos'],
            'operativos': ['operativo', 'operativa', 'operacional']
        }
        
        # Count theme occurrences
        theme_counts = {}
        for theme, keywords in theme_keywords.items():
            count = sum(1 for keyword in keywords if keyword in text_lower)
            if count > 0:
                theme_counts[theme] = count
        
        # Return top 3 themes by frequency
        sorted_themes = sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)
        return [theme for theme, count in sorted_themes[:3]]
    
    def _generate_combined_narrative(self, current_incidents: str, comparison_incidents: str,
                                   current_start: str, current_end: str, 
                                   comparison_start: str, comparison_end: str) -> str:
        """Generate combined narrative using LLM"""
        try:
            from langchain.schema import HumanMessage
            
            prompt_text = f"""
            Analiza los incidentes operativos de dos períodos y genera una narrativa operativa combinada.
            
            Período Actual ({current_start} a {current_end}):
            {current_incidents[:2000] if current_incidents else "Sin incidentes"}
            
            Período Comparativo ({comparison_start} a {comparison_end}):
            {comparison_incidents[:2000] if comparison_incidents else "Sin incidentes"}
            
            Genera una narrativa operativa que:
            1. Identifique los principales tipos de incidentes en cada período
            2. Compare las tendencias entre períodos
            3. Destaque cambios significativos en operaciones
            4. Proporcione contexto operativo relevante
            
            Responde en español de manera concisa y profesional.
            """
            
            # Use LangChain invoke method with proper message format
            messages = [HumanMessage(content=prompt_text)]
            # self.llm is the LLM wrapper, self.llm.llm is the actual LangChain ChatBedrock instance
            response = self.llm.llm.invoke(messages)
            return response.content.strip()
            
        except Exception as e:
            self.logger.error(f"Error generating combined narrative: {str(e)}")
            return "📝 Narrativa operativa no disponible debido a error en procesamiento"



    def _get_system_prompt(self, mode: str = "comparative") -> str:
        """Get system prompt for specified mode"""
        if mode == "single":
            return self.config.get('single_prompts', {}).get('system_prompt', '')
        else:
            return self.config.get('comparative_prompts', {}).get('system_prompt', '')
    
    def _get_input_template(self, mode: str = "comparative") -> str:
        """Get input template for specified mode"""
        if mode == "single":
            return self.config.get('single_prompts', {}).get('input_template', '')
        else:
            return self.config.get('comparative_prompts', {}).get('input_template', '')
    
    def _get_tool_result_message(self, mode: str = "comparative") -> str:
        """Get tool result message template for specified mode"""
        if mode == "single":
            return self.config.get('single_prompts', {}).get('tool_result_message', '📊 RESULTADO {tool_name}:\n{tool_result}')
        else:
            return self.config.get('comparative_prompts', {}).get('tool_result_message', '📊 RESULTADO DE HERRAMIENTA: {tool_name}\n{tool_result}')
    
    def _get_reflection_prompt(self, mode: str = "comparative", tool_name: str = None, flow_type: str = None) -> str:
        """Get reflection prompt for specified mode with dynamic tool-specific guidance"""
        base_prompt = ""
        if mode == "single":
            base_prompt = self.config.get('single_prompts', {}).get('reflection_prompt', '')
        else:
            base_prompt = self.config.get('comparative_prompts', {}).get('reflection_prompt', '')
        
        # DEBUG: Log the base prompt
        self.logger.info(f"🔍 DEBUG REFLECTION: mode={mode}, tool_name={tool_name}, flow_type={flow_type}")
        self.logger.info(f"🔍 DEBUG REFLECTION: base_prompt length={len(base_prompt)}")
        
        # If tool_name is provided, add dynamic tool-specific guidance
        if tool_name and base_prompt:
            tool_prompt = self._get_tool_prompt(tool_name, mode, flow_type)
            self.logger.info(f"🔍 DEBUG REFLECTION: tool_prompt length={len(tool_prompt) if tool_prompt else 0}")
            
            if tool_prompt:
                # Add the tool-specific guidance to the base reflection prompt
                enhanced_prompt = f"{base_prompt}\n\n🎯 GUÍA ESPECÍFICA DE LA HERRAMIENTA:\n{tool_prompt}"
                self.logger.info(f"🔍 DEBUG REFLECTION: enhanced_prompt length={len(enhanced_prompt)}")
                return enhanced_prompt
            else:
                self.logger.warning(f"🔍 DEBUG REFLECTION: No tool_prompt found for {tool_name}")
        
        self.logger.info(f"🔍 DEBUG REFLECTION: Returning base_prompt (no enhancement)")
        return base_prompt
    
    def _get_synthesis_prompt(self, mode: str = "comparative") -> str:
        """Get synthesis prompt for specified mode"""
        if mode == "single":
            return self.config.get('single_prompts', {}).get('synthesis_prompt', '')
        else:
            return self.config.get('comparative_prompts', {}).get('synthesis_prompt', '')
    
    def _determine_flow_type_from_drivers(self, tool_result: str) -> str:
        """Determine flow type from explanatory drivers tool result"""
        try:
            result_lower = tool_result.lower()
            self.logger.info(f"🔍 DEBUG FLOW: Analyzing tool_result of length {len(tool_result)}")
            
            # Check for operational drivers
            operational_keywords = ['punctuality', 'otp', 'delay', 'baggage', 'mishandling', 'misconex', 'load factor', 'connections', 'arrivals']
            operational_count = sum(1 for keyword in operational_keywords if keyword in result_lower)
            self.logger.info(f"🔍 DEBUG FLOW: Found {operational_count} operational keywords")
            
            # Check for product drivers
            product_keywords = ['crew', 'food', 'comfort', 'entertainment', 'service', 'cleanliness', 'seating', 'amenities']
            product_count = sum(1 for keyword in product_keywords if keyword in result_lower)
            self.logger.info(f"🔍 DEBUG FLOW: Found {product_count} product keywords")
            
            # Determine flow based on driver types
            if operational_count > 0 and product_count > 0:
                flow_type = 'mixed'
            elif operational_count > 0:
                flow_type = 'operative'
            elif product_count > 0:
                flow_type = 'product'
            else:
                # Default to operative if unclear
                flow_type = 'operative'
            
            self.logger.info(f"🔍 DEBUG FLOW: Determined flow_type: {flow_type}")
            return flow_type
                
        except Exception as e:
            self.logger.warning(f"Could not determine flow type from drivers: {e}")
            return 'operative'  # Default fallback
    
    def _get_tool_prompt(self, tool_name: str, mode: str = "comparative", flow_type: str = None) -> str:
        """Get tool-specific prompt for specified mode and flow type"""
        self.logger.info(f"🔍 DEBUG TOOL_PROMPT: tool_name={tool_name}, mode={mode}, flow_type={flow_type}")
        
        tool_prompts = self.config.get('tools_prompts', {}).get(tool_name, {})
        self.logger.info(f"🔍 DEBUG TOOL_PROMPT: Found tool_prompts for {tool_name}: {bool(tool_prompts)}")
        
        if mode not in tool_prompts:
            self.logger.warning(f"🔍 DEBUG TOOL_PROMPT: Mode {mode} not found in tool_prompts for {tool_name}")
            return ''
        
        mode_prompts = tool_prompts[mode]
        self.logger.info(f"🔍 DEBUG TOOL_PROMPT: mode_prompts type={type(mode_prompts)}, content preview={str(mode_prompts)[:100]}...")
        
        # If flow_type is specified and exists, return that specific flow
        if flow_type and isinstance(mode_prompts, dict) and flow_type in mode_prompts:
            self.logger.info(f"🔍 DEBUG TOOL_PROMPT: Returning specific flow_type={flow_type}")
            return mode_prompts[flow_type]
        
        # If no flow_type specified, return the mode prompt (could be string or dict)
        if isinstance(mode_prompts, str):
            self.logger.info(f"🔍 DEBUG TOOL_PROMPT: Returning string mode_prompts")
            return mode_prompts
        elif isinstance(mode_prompts, dict):
            # For comparative mode with flows, provide guidance on how to choose
            if tool_name == 'explanatory_drivers_tool':
                # For explanatory drivers, provide all flow options
                flow_options = []
                for flow, prompt in mode_prompts.items():
                    flow_options.append(f"**{flow.upper()} FLOW:**\n{prompt}")
                self.logger.info(f"🔍 DEBUG TOOL_PROMPT: explanatory_drivers_tool - returning {len(flow_options)} flow options")
                return "\n\n".join(flow_options)
            else:
                # For other tools, return the operative flow as default
                operative_prompt = mode_prompts.get('operative', str(mode_prompts))
                self.logger.info(f"🔍 DEBUG TOOL_PROMPT: Returning operative flow as default")
                return operative_prompt
        
        self.logger.info(f"🔍 DEBUG TOOL_PROMPT: Returning str(mode_prompts)")
        return str(mode_prompts)

    def _parse_reflection_response(self, response: str) -> Tuple[str, str]:
        """Parse reflection response to extract reflection and next tool code"""
        import re
        
        reflection = ""
        next_tool_code = ""
        
        # DEBUG: Log the raw response
        self.logger.info(f"🔍 DEBUG PARSE: Parsing response of length {len(response)}")
        
        # Extract reflection from ```reflection``` block
        reflection_match = re.search(r'```reflection\s*\n(.*?)\n```', response, re.DOTALL)
        if reflection_match:
            reflection = reflection_match.group(1).strip()
            self.logger.info(f"🔍 DEBUG PARSE: Found reflection block, length={len(reflection)}")
        else:
            self.logger.warning(f"🔍 DEBUG PARSE: No reflection block found in response")
        
        # Extract next tool code from ```next_tool``` block
        next_tool_code_match = re.search(r'```next_tool\s*\n(.*?)\n```', response, re.DOTALL)
        if next_tool_code_match:
            next_tool_code = next_tool_code_match.group(1).strip()
            self.logger.info(f"🔍 DEBUG PARSE: Found next_tool block, length={len(next_tool_code)}")
            self.logger.info(f"🔍 DEBUG PARSE: next_tool_code content: {next_tool_code}")
        else:
            self.logger.warning(f"🔍 DEBUG PARSE: No next_tool block found in response")
        
        self.logger.info(f"🔍 DEBUG PARSE: Final result - reflection: {len(reflection)}, next_tool: {len(next_tool_code)}")
        return reflection, next_tool_code


# Convenience function
async def investigate_anomaly_causally(
    node_path: str,
    start_date: str,
    end_date: str,
    anomaly_type: str,
    anomaly_magnitude: float,
    llm_type: LLMType = LLMType.CLAUDE_SONNET_4,
    custom_helper_prompts: Optional[Dict[str, Any]] = None
) -> str:
    """
    Clean causal investigation with separated workflow
    """
    agent = CausalExplanationAgent(
        llm_type=llm_type,
        custom_helper_prompts=custom_helper_prompts
    )
    
    result = await agent.investigate_anomaly(
        node_path=node_path,
        start_date=start_date,
        end_date=end_date,
        anomaly_type=anomaly_type,
        anomaly_magnitude=anomaly_magnitude
    )
    
    return result


# Example usage
if __name__ == "__main__":
    async def main():
        # Test the clean causal investigation
        result = await investigate_anomaly_causally(
            node_path="Global/LH/Business",
            start_date="2025-05-15",
            end_date="2025-05-15", 
            anomaly_type="negative",
            anomaly_magnitude=-15.0,
            llm_type=get_default_llm_type()
        )
        
        print("🎯 Investigation Result:")
        print(result)
    
    asyncio.run(main()) 