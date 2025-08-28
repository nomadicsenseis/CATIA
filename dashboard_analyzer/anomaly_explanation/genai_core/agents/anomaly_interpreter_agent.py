"""
Anomaly Interpreter Agent

A specialized AI agent for interpreting NPS anomaly trees and generating conclusions
about operational desempeño and customer perception correlations.
"""

import asyncio
import os
import yaml
import logging
import json
import re
from typing import Optional, Dict, Any, List
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Import GenAI Core components (adjusted for new location)
from ..agents.agent import Agent
from ..llms.openai_llm import OpenAiLLM
from ..llms.aws_llm import AWSLLM
from ..utils.enums import LLMType, MessageType, AgentName
from ..message_history import MessageHistory

# Helper function to find a file from the project root
def find_project_root(marker_file=".git"):
    """Find the project root by searching for a marker file."""
    path = Path(__file__).resolve()
    while not (path / marker_file).exists():
        if path.parent == path:
            return None  # Reached the filesystem root
        path = path.parent
    return path

class HierarchicalConversationTracker:
    """Track hierarchical conversation workflow with generation-by-generation analysis"""
    
    def __init__(self):
        self.conversation_log = []
        self.generation_count = 0
        self.hierarchy_structure = {}
        self.generation_reflections = []
        self.generation_analysis = {}
        
    def reset_tracker(self):
        """Reset for new hierarchical investigation"""
        self.conversation_log = []
        self.generation_count = 0
        self.hierarchy_structure = {}
        self.generation_reflections = []
        self.generation_analysis = {}
        
    def log_message(self, message_type: str, content: str, metadata: Optional[Dict] = None):
        """Log a message in the hierarchical conversation"""
        self.conversation_log.append({
            'generation': self.generation_count,
            'type': message_type,
            'content': content,
            'metadata': metadata or {},
            'timestamp': datetime.now().strftime('%H:%M:%S')
        })
    
    def set_hierarchy_structure(self, hierarchy: Dict[str, Any]):
        """Store the parsed hierarchy structure"""
        self.hierarchy_structure = hierarchy
    
    def start_generation(self, generation_level: int, nodes: List[str]):
        """Start analysis of a new generation"""
        self.generation_count = generation_level
        self.log_message("GENERATION_START", f"Starting analysis of generation {generation_level}", {
            'generation_level': generation_level,
            'nodes': nodes,
            'node_count': len(nodes)
        })
    
    def add_generation_reflection(self, generation: int, nodes: List[str], reflection: str):
        """Add a reflection for a specific generation"""
        reflection_data = {
            'generation': generation,
            'nodes': nodes,
            'reflection': reflection,
            'timestamp': datetime.now().isoformat(),
            'reflection_length': len(reflection)
        }
        self.generation_reflections.append(reflection_data)
        self.log_message("GENERATION_REFLECTION", f"Generation {generation} reflection captured", {
            'generation': generation,
            'nodes': nodes,
            'reflection_length': len(reflection)
        })
    
    def add_generation_analysis(self, generation: int, analysis_data: Dict[str, Any]):
        """Add detailed analysis data for a generation"""
        self.generation_analysis[generation] = analysis_data
    
    def get_conversation_summary(self) -> Dict[str, int]:
        """Get summary of conversation message types"""
        summary = {}
        for entry in self.conversation_log:
            msg_type = entry['type']
            summary[msg_type] = summary.get(msg_type, 0) + 1
        return summary
    
    def get_hierarchy_summary(self) -> Dict[str, Any]:
        """Get summary of the hierarchy analyzed"""
        if not self.hierarchy_structure:
            return {}
        
        return {
            'total_nodes': len(self.hierarchy_structure),
            'generations_analyzed': len(set(entry['generation'] for entry in self.generation_reflections)),
            'nodes_by_level': {
                level: [path for path, data in self.hierarchy_structure.items() if data.get('level') == level]
                for level in set(data.get('level', 0) for data in self.hierarchy_structure.values())
            },
            'parent_child_relationships': {
                path: data.get('children', []) 
                for path, data in self.hierarchy_structure.items() 
                if data.get('children')
            }
        }


class AnomalyInterpreterAgent:
    """
    Specialized agent for interpreting anomaly trees and generating actionable conclusions.
    
    Features:
    - Multi-LLM support (OpenAI, AWS Bedrock)
    - External prompt configuration via YAML
    - Professional anomaly analysis with operational insights
    - Hierarchical generation-by-generation analysis with AI reflections
    - Conversation tracking and export functionality
    """
    
    def __init__(
        self,
        llm_type: Optional[LLMType] = None,
        config_path: str = "dashboard_analyzer/anomaly_explanation/config/prompts/anomaly_interpreter.yaml",
        logger: Optional[logging.Logger] = None,
        study_mode: str = "comparative"
    ):
        """
        Initialize the Anomaly Interpreter Agent.
        
        Args:
            llm_type: Type of LLM to use (supports OpenAI and AWS Bedrock models)
            config_path: Path to YAML configuration file with prompts
            logger: Optional logger instance
            study_mode: Study mode - "single" or "comparative"
        """
        # Use default LLM type if none provided
        if llm_type is None:
            from dashboard_analyzer.anomaly_explanation.genai_core.utils.enums import get_default_llm_type
            llm_type = get_default_llm_type()
        self.llm_type = llm_type
        self.logger = logger or self._setup_logger()
        self.study_mode = study_mode
        
        # Load environment variables from .devcontainer/.env
        project_root = find_project_root()
        if project_root:
            dotenv_path = project_root / '.devcontainer' / '.env'
            if dotenv_path.exists():
                load_dotenv(dotenv_path)
        
        # Load prompt configuration
        self.config = self._load_prompt_config(config_path)
        
        # Initialize LLM based on type
        self.llm = self._create_llm(llm_type)
        
        # Initialize base agent
        self.agent = Agent(llm=self.llm, logger=self.logger)
        
        # Conversation tracking for hierarchical analysis
        self.hierarchical_reflections = []
        self.generation_data = {}
        self.conversation_tracker = HierarchicalConversationTracker()
        
        # desempeño metrics
        self.total_processing_time = 0.0
        self.total_hierarchical_calls = 0
        
        self.logger.info(f"🤖 AnomalyInterpreterAgent initialized with {llm_type.value}")

    def _setup_logger(self) -> logging.Logger:
        """Setup default logger for the agent."""
        logger = logging.getLogger(f"AnomalyInterpreterAgent")
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

    def _load_prompt_config(self, config_path: str) -> Dict[str, Any]:
        """Load prompt configuration from YAML file."""
        try:
            # Construct path from project root
            project_root = find_project_root()
            if not project_root:
                raise FileNotFoundError("Could not find project root (.git folder).")
            
            full_path = project_root / config_path
            
            if not full_path.exists():
                raise FileNotFoundError(f"Prompt config file not found at {full_path}")

            with open(full_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            self.logger.info(f"Prompt configuration loaded from {full_path}")
            
            return config
        except Exception as e:
            self.logger.error(f"Failed to load prompt config from {config_path}: {e}")
            # Return a basic configuration as fallback
            return {
                "system_prompt": "You are an expert anomaly interpreter.",
                "input_template": "Analyze the following anomaly tree: {anomaly_tree}"
            }

    
    def _get_system_prompt(self, mode: str = None) -> str:
        """Get system prompt for specified mode"""
        if mode is None:
            mode = self.study_mode
        
        if mode == "single":
            return self.config.get('single_prompts', {}).get('system_prompt', '')
        else:
            return self.config.get('comparative_prompts', {}).get('system_prompt', '')
    
    def _get_input_template(self, template_name: str, mode: str = None) -> str:
        """Get input template for specified mode and template name"""
        if mode is None:
            mode = self.study_mode
        
        if mode == "single":
            templates = self.config.get('single_prompts', {}).get('input_templates', {})
        else:
            templates = self.config.get('comparative_prompts', {}).get('input_templates', {})
        
        return templates.get(template_name, f"Template {template_name} not found for mode {mode}")
    
    def _get_hierarchical_helper(self, step_name: str) -> str:
        """Get hierarchical diagnostic helper (shared between modes)"""
        helpers = self.config.get('hierarchical_diagnostic_helpers', {})
        return helpers.get(step_name, f"Helper {step_name} not found")

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
    
    async def interpret_anomaly_tree(self, tree_data: str, date: Optional[str] = None, segment: Optional[str] = None) -> str:
        """
        Interpret a causal agent explanation using conversational hierarchical methodology.
        
        Args:
            tree_data: The causal agent explanation/narrative (not an anomaly tree)
            date: Optional date for context (e.g., "2025-05-24")
            segment: Optional segment for analysis
            
        Returns:
            Structured interpretation following the conversational hierarchical methodology
        """
        self.logger.info("🔄 Using CONVERSATIONAL hierarchical interpretation (self-conversation enabled)")
        
        # Always use the conversational method that includes self-conversation
        return await self.interpret_anomaly_tree_hierarchical(tree_data, date, segment)

    async def interpret_anomaly_tree_hierarchical(self, tree_data: str, date: Optional[str] = None, segment: Optional[str] = None) -> str:
        """
        Perform hierarchical interpretation using conversational step-by-step reasoning.
        
        Args:
            tree_data: Combined explanations from multiple hierarchical nodes
            date: Optional date for context
            
        Returns:
            Comprehensive hierarchical interpretation with step-by-step analysis
        """
        start_time = datetime.now()
        self.conversation_tracker.reset_tracker()
        
        try:
            # Parse hierarchy structure from explanations
            hierarchy = self._parse_hierarchy_from_explanations(tree_data)
            
            if not hierarchy:
                return "❌ No se pudo parsear la estructura jerárquica de las explicaciones proporcionadas."
            
            self.conversation_tracker.set_hierarchy_structure(hierarchy)
            self.logger.info(f"🏗️ Hierarchy parsed: {len(hierarchy)} nodes")
            
            # Create message history for conversational analysis
            message_history = MessageHistory(logger=self.logger)
            
            # Add system prompt based on study mode
            system_prompt = self._get_system_prompt()
            message_history.create_and_add_message(
                content=system_prompt,
                message_type=MessageType.SYSTEM
            )
            
            # Step 1: Provide all context to the model and get acknowledgment
            context_message = self._get_input_template('hierarchical_context_setup').format(
                tree_data=tree_data,
                date=date if date else 'No especificada'
            )
            message_history.create_and_add_message(
                content=context_message,
                message_type=MessageType.USER
            )
            self.conversation_tracker.log_message("CONTEXT_SETUP", context_message, {
                'hierarchy_nodes': len(hierarchy),
                'date': date
            })

            # Get AI acknowledgment of context
            context_response, _, _ = await self.agent.invoke(messages=message_history.get_messages())
            message_history.add_message(context_response)
            
            self.conversation_tracker.log_message("CONTEXT_ACKNOWLEDGED", context_response.content, {
                'response_length': len(context_response.content)
            })
            
            self.logger.info(f"💭 Context acknowledged: {context_response.content[:100]}...")

            # Determine applicable steps dynamically using the provided segment
            detected_segment = segment if segment else self._extract_primary_segment_from_data(tree_data)
            applicable_step_keys = self._get_applicable_steps_for_segment(detected_segment)
            
            # Step-by-step conversational analysis
            conversation_steps = []
            step_name_mapping = {
                'step1_company_level_diagnosis': "COMPANY_LEVEL_DIAGNOSIS",
                'step2_cabin_level_diagnosis': "CABIN_LEVEL_DIAGNOSIS", 
                'step3_radio_global_diagnosis': "RADIO_GLOBAL_DIAGNOSIS",
                'step4_detailed_cause_analysis': "DETAILED_CAUSE_ANALYSIS",
                'step5_executive_synthesis': "EXECUTIVE_SYNTHESIS"
            }
            
            for step_key in applicable_step_keys:
                if step_key in step_name_mapping:
                    conversation_steps.append((step_key, step_name_mapping[step_key]))
            
            # Always add step5 for final synthesis if not already included
            if 'step5_executive_synthesis' not in [s[0] for s in conversation_steps]:
                conversation_steps.append(('step5_executive_synthesis', "EXECUTIVE_SYNTHESIS"))
            
            self.logger.info(f"🔄 Using {len(conversation_steps)} applicable steps for segment '{detected_segment}': {[s[0] for s in conversation_steps]}")
            
            step_responses = []
            
            for step_key, step_name in conversation_steps:
                self.logger.info(f"🔍 Executing diagnostic step: {step_name}")
                
                # Get helper prompt for this step
                helper_prompt = self._get_hierarchical_helper(step_key)
                
                message_history.create_and_add_message(
                    content=helper_prompt,
                    message_type=MessageType.USER
                )
                
                self.conversation_tracker.log_message("HELPER_PROMPT", helper_prompt, {
                    'step': step_name,
                    'prompt_length': len(helper_prompt)
                })
                
                self.logger.info(f"💬 Asking AI: {helper_prompt[:100]}...")
                
                # Get AI response for this step
                step_response, _, _ = await self.agent.invoke(
                    messages=message_history.get_messages()
                )
                
                step_content = step_response.content.strip()
                step_responses.append({
                    'step': step_name,
                    'content': step_content
                })
                
                message_history.add_message(step_response)
                
                self.conversation_tracker.log_message("STEP_RESPONSE", step_content, {
                    'step': step_name,
                    'response_length': len(step_content)
                })
                
                self.logger.info(f"💭 AI Response for {step_name}: {step_content[:150]}...")
                self.logger.info(f"✅ {step_name} completed ({len(step_content)} chars)")
            
            # Compile final response from all steps
            final_interpretation = self._compile_final_interpretation(
                step_responses,
                hierarchy
            )
            
            # Update desempeño metrics
            end_time = datetime.now()
            self.total_processing_time = (end_time - start_time).total_seconds()
            self.total_hierarchical_calls += 1
            
            self.logger.info(f"✅ Hierarchical interpretation completed in {self.total_processing_time:.2f}s")
            
            # Export successful conversation for debugging
            conversation_file = self.export_hierarchical_conversation(date=date)
            if conversation_file:
                self.logger.info(f"🗂️ Conversación jerárquica guardada: {conversation_file}")
            
            return final_interpretation
            
        except Exception as e:
            self.logger.error(f"❌ Error in hierarchical interpretation: {str(e)}")
            error_msg = f"Error durante la interpretación jerárquica: {str(e)}"
            
            # Export error conversation for debugging
            self.export_hierarchical_conversation(date, error_msg)
            
            return f"❌ Error en la interpretación jerárquica: {str(e)}"
    
    def _parse_hierarchy_from_explanations(self, tree_data: str) -> Dict[str, Any]:
        """Parse hierarchical structure from combined causal explanations."""
        hierarchy = {}
        # Use regex to find all "NODO: <path>" and their subsequent content.
        # The pattern looks for "NODO:", captures the path until a newline,
        # and then captures all content until the next "NODO:" or the end of the string.
        pattern = re.compile(r"NODO:\s*(.*?)\n(.*?)(?=\nNODO:|\Z)", re.DOTALL)

        matches = pattern.findall(tree_data)
        
        if not matches:
            self.logger.warning("No matches found for 'NODO:' pattern in tree_data.")
            return {}

        for match in matches:
            node_path = match[0].strip()
            content = match[1].strip()
            
            # Determine level
            level = len(node_path.split('/'))
            
            # Determine parent
            parent_path = '/'.join(node_path.split('/')[:-1]) if '/' in node_path else None

            hierarchy[node_path] = {
                'type': 'node',
                'level': level,
                'path': node_path,
                'parent': parent_path,
                'children': [],
                'content': content  # The full explanation for this node
            }

        # Build parent-child relationships
        for node_path, node_data in hierarchy.items():
            parent_path = node_data.get('parent')
            if parent_path and parent_path in hierarchy:
                if node_path not in hierarchy[parent_path]['children']:
                    hierarchy[parent_path]['children'].append(node_path)
        
        return hierarchy
    
    def _format_hierarchy_structure(self, hierarchy: Dict[str, Any]) -> str:
        """Format hierarchy structure for display."""
        result = []
        
        # Find root nodes (no parent)
        root_nodes = [path for path, data in hierarchy.items() if data.get('parent') is None]
        
        def format_node(node_path: str, indent: str = "") -> str:
            node_data = hierarchy.get(node_path, {})
            children = node_data.get('children', [])
            
            lines = [f"{indent}📊 {node_path}"]
            
            for child in children:
                lines.append(format_node(child, indent + "  "))
            
            return '\n'.join(lines)
        
        for root in sorted(root_nodes):
            result.append(format_node(root))
        
        return '\n'.join(result)
    
    def _order_generations_bottom_up(self, hierarchy: Dict[str, Any]) -> List[List[Dict[str, Any]]]:
        """Order nodes by generation level (bottom-up)."""
        # Group by depth level
        levels = {}
        for path, data in hierarchy.items():
            level = data.get('level', 0)
            if level not in levels:
                levels[level] = []
            levels[level].append(data)
        
        # Return in reverse order (deepest first)
        result = []
        for level in sorted(levels.keys(), reverse=True):
            result.append(levels[level])
        
        return result
    
    def _generate_generation_helper_prompt(self, generation_level: int, nodes: List[Dict[str, Any]], hierarchy: Dict[str, Any]) -> str:
        """Generate helper prompt for analyzing a specific generation."""
        
        node_paths = [f"• {node['path']}" for node in nodes]
        
        return self.config['hierarchical_prompts']['generation_analysis'].format(
            generation_level=generation_level + 1,
            node_paths='\n'.join(node_paths)
        )
    
    def _generate_comprehensive_summary_prompt(self, hierarchy: Dict[str, Any]) -> str:
        """Generate comprehensive summary prompt asking for final conclusions, causes, impacts, routes, and profiles."""
        
        total_nodes = len(hierarchy)
        analyzed_segments = ', '.join(hierarchy.keys())
        
        return self.config['hierarchical_prompts']['comprehensive_summary'].format(
            total_nodes=total_nodes,
            analyzed_segments=analyzed_segments
        )
    
    def _generate_synthesis_prompt(self, hierarchy: Dict[str, Any]) -> str:
        """Generate final synthesis prompt across all generations."""
        
        total_nodes = len(hierarchy)
        
        return self.config['hierarchical_prompts']['final_synthesis'].format(
            total_nodes=total_nodes
        )
    
    def _compile_final_interpretation(self, step_responses: List[Dict[str, str]], hierarchy: Dict[str, Any]) -> str:
        """
        Compile final interpretation from all conversational steps.
        
        Args:
            step_responses: List of step responses with step name and content
            hierarchy: Parsed hierarchy structure
            
        Returns:
            Compiled final interpretation with all analysis steps
        """
        try:
            # Header with analysis overview
            total_nodes = len(hierarchy)
            
            final_interpretation = f"""
📊 **ANÁLISIS JERÁRQUICO COMPLETO DE ANOMALÍAS NPS**

**Nodos analizados:** {total_nodes} ({', '.join(sorted(list(hierarchy.keys())))})

---
"""
            
            # Add each step response with proper formatting
            step_titles = {
                'COMPANY_LEVEL_DIAGNOSIS': '📊 DIAGNÓSTICO A NIVEL DE EMPRESA',
                'CABIN_LEVEL_DIAGNOSIS': '💺 DIAGNÓSTICO A NIVEL DE CABINA', 
                'RADIO_GLOBAL_DIAGNOSIS': '🌎 DIAGNÓSTICO GLOBAL POR RADIO',
                'DETAILED_CAUSE_ANALYSIS': '📋 ANÁLISIS DE CAUSAS DETALLADO',
                'EXECUTIVE_SYNTHESIS': '📋 SÍNTESIS EJECUTIVA FINAL'
            }
            
            for step_data in step_responses:
                step_name = step_data['step']
                step_content = step_data['content']
                step_title = step_titles.get(step_name, step_name.replace('_', ' ').title())
                
                final_interpretation += f"""
## {step_title}

{step_content}

---
"""
            
            # Footer with completion summary
            final_interpretation += f"""
✅ **ANÁLISIS COMPLETADO**

- **Nodos procesados:** {total_nodes}
- **Pasos de análisis:** {len(step_responses)}
- **Metodología:** Análisis conversacional paso a paso
- **Resultado:** Interpretación jerárquica completa con razonamiento estructurado

*Este análisis utiliza metodología conversacional para simular el razonamiento paso a paso de un analista experto, similar al proceso de investigación causal.*
"""
            
            return final_interpretation.strip()
            
        except Exception as e:
            self.logger.error(f"❌ Error compiling final interpretation: {str(e)}")
            # Fallback: return the final synthesis step if available
            final_synthesis = next((s['content'] for s in step_responses if s['step'] == 'EXECUTIVE_SYNTHESIS'), None)
            if final_synthesis:
                return f"📋 **SÍNTESIS FINAL**\n\n{final_synthesis}"

            # Last resort: return a generic error
            return "⚠️ **ANÁLISIS PARCIAL** (Error en compilación)"
    
    def export_hierarchical_conversation(self, date: Optional[str] = None, error: Optional[str] = None) -> str:
        """Export the hierarchical conversation log to JSON file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            # Use analysis date if provided, otherwise use current date
            period_identifier = date if date else timestamp[:8]  # Extract YYYYMMDD from timestamp
            filename = f"interpreter_{period_identifier}_{timestamp}.json"
            
            # Create agent_conversations directory structure
            base_dir = Path(__file__).parent.parent.parent.parent.parent / 'dashboard_analyzer' / 'agent_conversations' / 'anomaly_interpreter'
            base_dir.mkdir(parents=True, exist_ok=True)
            
            full_path = base_dir / filename
            
            conversation_data = {
                "metadata": {
                    "agent_type": "anomaly_interpreter",
                    "analysis_type": "hierarchical_generation_by_generation",
                    "export_timestamp": datetime.now().isoformat(),
                    "analysis_date": date,
                    "llm_type": self.llm_type.value,
                    "total_generations": len(set(r['generation'] for r in self.hierarchical_reflections)),
                    "total_nodes_analyzed": len(self.conversation_tracker.hierarchy_structure),
                    "error": error
                },
                "hierarchy_structure": self.conversation_tracker.hierarchy_structure,
                "hierarchy_summary": self.conversation_tracker.get_hierarchy_summary(),
                "conversation_log": self.conversation_tracker.conversation_log,
                "conversation_summary": self.conversation_tracker.get_conversation_summary(),
                "generation_reflections": self.hierarchical_reflections,
                "generation_analysis": self.generation_data
            }
            
            with open(full_path, 'w', encoding='utf-8') as f:
                json.dump(conversation_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"📝 Hierarchical conversation exported to: {full_path}")
            return str(full_path)
            
        except Exception as e:
            self.logger.error(f"❌ Failed to export hierarchical conversation: {e}")
            return ""
    
    def export_conversation(
        self, 
        start_date: str, 
        end_date: str, 
        node_path: str,
        tree_data: str,
        interpretation_result: str,
        study_mode: str = "unknown"
    ) -> str:
        """
        Export interpreter conversation to JSON file with same format as causal agent
        
        Args:
            start_date: Analysis start date
            end_date: Analysis end date  
            node_path: Node path analyzed
            tree_data: Input tree data provided to interpreter
            interpretation_result: Final interpretation result
            study_mode: Analysis mode (single/comparative)
            
        Returns:
            Path to exported JSON file
        """
        try:
            # Create conversations directory if it doesn't exist
            conversations_dir = Path("dashboard_analyzer/agent_conversations/interpreter")
            conversations_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_node_path = node_path.replace("/", "_").replace(" ", "_")
            filename = f"interpreter_{start_date}_{end_date}_{safe_node_path}_{timestamp}.json"
            filepath = conversations_dir / filename
            
            # Build metadata
            metadata = {
                "agent_type": "anomaly_interpreter",
                "analysis_type": "hierarchical_interpretation", 
                "export_timestamp": datetime.now().isoformat(),
                "node_path": node_path,
                "start_date": start_date,
                "end_date": end_date,
                "study_mode": study_mode,
                "total_messages": len(self.conversation_tracker.conversation_log),
                "interpretation_success": bool(interpretation_result and len(interpretation_result) > 0),
                "tree_data_size": len(tree_data)
            }
            
            # Convert conversation log to format similar to causal agent
            conversation_log = []
            for entry in self.conversation_tracker.conversation_log:
                conversation_log.append({
                    "generation": entry.get('generation', 0),
                    "type": entry.get('type', 'UNKNOWN'),
                    "content": entry.get('content', ''),
                    "metadata": entry.get('metadata', {}),
                    "timestamp": entry.get('timestamp', datetime.now().strftime('%H:%M:%S'))
                })
            
            # Export data structure
            export_data = {
                "metadata": metadata,
                "input_tree_data": tree_data,  # Save exact input tree
                "conversation_log": conversation_log,
                "final_interpretation": interpretation_result,
                "conversation_summary": {
                    "total_generations": self.conversation_tracker.generation_count,
                    "hierarchy_structure": self.conversation_tracker.hierarchy_structure,
                    "generation_analysis": self.conversation_tracker.generation_analysis
                }
            }
            
            # Write to JSON file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"✅ Interpreter conversation exported to: {filepath}")
            return str(filepath)
            
        except Exception as e:
            self.logger.error(f"❌ Failed to export interpreter conversation: {e}")
            return ""

    def get_desempeño_metrics(self) -> Dict[str, Any]:
        """Get agent desempeño metrics."""
        return {
            "num_calls": self.agent.num_calls,
            "total_time": self.agent.total_time,
            "avg_time": self.agent.avg_time,
            "last_execution_time": self.agent.last_execution_time,
            "input_tokens": self.agent.input_tokens,
            "output_tokens": self.agent.output_tokens,
            "money_spent": self.agent.money_spent,
            "llm_type": self.llm_type.value,
            "hierarchical_reflections_count": len(self.hierarchical_reflections),
            "conversation_messages_count": len(self.conversation_tracker.conversation_log)
        }

    def _get_applicable_steps_for_segment(self, segment: str) -> List[str]:
        """
        Determina qué pasos del análisis jerárquico aplican según el segmento.
        
        Args:
            segment: El segmento a analizar
            
        Returns:
            Lista de claves de prompts que deben ejecutarse
        """
        segment_mapping = {
            'Global': ['step1_company_level_diagnosis', 'step2_cabin_level_diagnosis', 
                       'step3_radio_global_diagnosis', 'step4_detailed_cause_analysis'],
            'LH': ['step2_cabin_level_diagnosis', 'step4_detailed_cause_analysis'],
            'SH': ['step1_company_level_diagnosis', 'step2_cabin_level_diagnosis', 
                   'step4_detailed_cause_analysis'],
            'Economy LH': ['step4_detailed_cause_analysis'],
            'Business LH': ['step4_detailed_cause_analysis'],
            'Premium LH': ['step4_detailed_cause_analysis'],
            'Economy SH': ['step1_company_level_diagnosis', 'step4_detailed_cause_analysis'],
            'Business SH': ['step1_company_level_diagnosis', 'step4_detailed_cause_analysis'],
            'Premium SH': ['step1_company_level_diagnosis', 'step4_detailed_cause_analysis'],
            'IB': ['step4_detailed_cause_analysis'],
            'YW': ['step4_detailed_cause_analysis'],
        }
        return segment_mapping.get(segment, ['step4_detailed_cause_analysis'])  # default
    
    def _extract_primary_segment_from_data(self, tree_data: str) -> str:
        """
        Determines the primary segment for analysis based on the study mode.
        For a 'comparative' (weekly) study, it's always 'Global'.
        For a 'single' (daily) study, it defaults to the first node found.

        Args:
            tree_data: The hierarchical data containing node explanations.

        Returns:
            The detected primary segment ('Global' or the first node path).
        """
        if self.study_mode == 'comparative':
            self.logger.info("Comparative study mode detected. Setting primary segment to 'Global'.")
            return 'Global'
        
        # For single mode, fall back to the first node found in the hierarchy.
        node_paths = re.findall(r"NODO:\s*([^\n]+)", tree_data)
        primary_segment = node_paths[0] if node_paths else 'Global'
        self.logger.info(f"Single study mode. Using first detected node as primary segment: {primary_segment}")
        return primary_segment

    def _detect_segment_level(self, segment: str) -> str:
        """
        Detecta el nivel jerárquico del segmento.
        
        Args:
            segment: El segmento a analizar
            
        Returns:
            'company', 'cabin', 'radio', 'global'
        """
        if segment in ['IB', 'YW']:
            return 'company'
        elif segment in ['Economy LH', 'Business LH', 'Premium LH', 
                         'Economy SH', 'Business SH', 'Premium SH']:
            return 'cabin'
        elif segment in ['LH', 'SH']:
            return 'radio'
        elif segment == 'Global':
            return 'global'
        else:
            return 'unknown'

    def _get_cabin_sections_for_segment(self, segment: str) -> str:
        """
        Genera las secciones de cabina dinámicas según el segmento seleccionado.
        
        Args:
            segment: El segmento a analizar
            
        Returns:
            String con las secciones de cabina relevantes para el prompt
        """
        cabin_sections = {
            'Global': """
    **ECONOMY SH: [Título]**
    [PÁRRAFO NARRATIVO FLUIDO] La cabina Economy de SH [descripción - para segmentos estables usar: "mantuvo desempeño estable"] durante la semana del [fecha], registrando un NPS de [valor cabina] ([fecha período]) con una [variación de NPS_diff cabina] puntos respecto a la semana anterior. [Para segmentos estables: "No se detectaron cambios significativos, manteniendo niveles consistentes de satisfacción." | Para segmentos con variaciones: "La causa principal fue [hipótesis con datos (drivers, operativa, NCS, verbatims) que la respaldan], complementada por [hipótesis secundarias (si las hubiera)]. Esta [mejora/deterioro] se reflejó especialmente en rutas como [top rutas con NPS y diff], mientras que los perfiles más reactivos incluyen [perfiles específicos]."]
    
    **BUSINESS SH: [Título]**
    [PÁRRAFO NARRATIVO FLUIDO] El segmento Business de SH [descripción - para segmentos estables usar: "mantuvo desempeño estable"], registrando un NPS de [valor cabina] ([fecha]) con una [variación de diff cabina] puntos vs la semana anterior.     [Para segmentos estables: "No se detectaron cambios significativos, manteniendo niveles consistentes de satisfacción." | Para segmentos con variaciones: "Esta evolución se explica principalmente por [causas SHAP], siendo especialmente visible en rutas como [rutas top] y entre perfiles [perfiles reactivos]."]
    
    **ECONOMY LH: [Título]**
    [PÁRRAFO NARRATIVO FLUIDO] La cabina Economy de LH [descripción - para segmentos estables usar: "mantuvo desempeño estable"], registrando un NPS de [valor cabina] ([fecha período]) con una [variación de NPS_diff cabina] puntos respecto a la semana anterior. [Para segmentos estables: "No se detectaron cambios significativos, manteniendo niveles consistentes de satisfacción." | Para segmentos con variaciones: "La causa principal fue [hipótesis con datos (drivers, operativa, NCS, verbatims) que la respaldan], complementada por [hipótesis secundarias (si las hubiera)]. Esta [mejora/deterioro] se reflejó especialmente en rutas como [top rutas con NPS y diff], mientras que los perfiles más reactivos incluyen [perfiles específicos]."]
    
    **BUSINESS LH: [Título]**  
    [PÁRRAFO NARRATIVO FLUIDO] La cabina Business de LH [descripción - para segmentos estables usar: "mantuvo desempeño estable"], registrando un NPS de [valor cabina] ([fecha período]) con una [variación de NPS_diff cabina] puntos respecto al período anterior.     [Para segmentos estables: "No se detectaron cambios significativos, manteniendo niveles consistentes de satisfacción." | Para segmentos con variaciones: "Los drivers principales fueron [causas con SHAP], impactando especialmente las rutas [rutas específicas] y perfiles [perfiles específicos]."]
    
    **PREMIUM LH: [Título]**
    [PÁRRAFO NARRATIVO FLUIDO] El segmento Premium de LH [descripción - para segmentos estables usar: "mantuvo desempeño estable"], registrando un NPS de [valor cabina] ([fecha]) con [diff cabina] puntos de [variación] vs la semana anterior. [Para segmentos estables: "No se detectaron cambios significativos, manteniendo niveles consistentes de satisfacción." | Para segmentos con variaciones: "Las causas dominantes fueron [drivers SHAP], especialmente evidentes en [rutas top] y entre [perfiles reactivos]."]
            """,
            'SH': """
    **ECONOMY SH: [Título]**
    [PÁRRAFO NARRATIVO FLUIDO] La cabina Economy de SH [descripción - para segmentos estables usar: "mantuvo desempeño estable"] durante la semana del [fecha], registrando un NPS de [valor cabina] ([fecha período]) con una [variación de NPS_diff cabina] puntos respecto a la semana anterior. [Para segmentos estables: "No se detectaron cambios significativos, manteniendo niveles consistentes de satisfacción." | Para segmentos con variaciones: "La causa principal fue [hipótesis con datos (drivers, operativa, NCS, verbatims) que la respaldan], complementada por [hipótesis secundarias (si las hubiera)]. Esta [mejora/deterioro] se reflejó especialmente en rutas como [top rutas con NPS y diff], mientras que los perfiles más reactivos incluyen [perfiles específicos]."]
    
    **BUSINESS SH: [Título]**
    [PÁRRAFO NARRATIVO FLUIDO] El segmento Business de SH [descripción - para segmentos estables usar: "mantuvo desempeño estable"], registrando un NPS de [valor cabina] ([fecha]) con una [variación de diff cabina] puntos vs la semana anterior. [Para segmentos estables: "No se detectaron cambios significativos, manteniendo niveles consistentes de satisfacción." | Para segmentos con variaciones: "Esta evolución se explica principalmente por [causas SHAP], siendo especialmente visible en rutas como [rutas top] y entre perfiles [perfiles reactivos]."]
            """,
            'LH': """
    **ECONOMY LH: [Título]**
    [PÁRRAFO NARRATIVO FLUIDO] La cabina Economy de LH [descripción - para segmentos estables usar: "mantuvo desempeño estable"], registrando un NPS de [valor cabina] ([fecha período]) con una [variación de NPS_diff cabina] puntos respecto a la semana anterior. [Para segmentos estables: "No se detectaron cambios significativos, manteniendo niveles consistentes de satisfacción." | Para segmentos con variaciones: "La causa principal fue [hipótesis con datos (drivers, operativa, NCS, verbatims) que la respaldan], complementada por [hipótesis secundarias (si las hubiera)]. Esta [mejora/deterioro] se reflejó especialmente en rutas como [top rutas con NPS y diff], mientras que los perfiles más reactivos incluyen [perfiles específicos]."]
    
    **BUSINESS LH: [Título]**  
    [PÁRRAFO NARRATIVO FLUIDO] La cabina Business de LH [descripción - para segmentos estables usar: "mantuvo desempeño estable"], registrando un NPS de [valor cabina] ([fecha]) con [diff cabina] puntos de [variación] vs período anterior. [Para segmentos estables: "No se detectaron cambios significativos, manteniendo niveles consistentes de satisfacción." | Para segmentos con variaciones: "Los drivers principales fueron [causas con SHAP], impactando especialmente las rutas transatlánticas [rutas específicas] y perfiles [perfiles específicos]."]
    
    **PREMIUM LH: [Título]**
    [PÁRRAFO NARRATIVO FLUIDO] El segmento Premium de LH [descripción - para segmentos estables usar: "mantuvo desempeño estable"], registrando un NPS de [valor cabina] ([fecha]) con [diff cabina] puntos de [variación] vs la semana anterior. [Para segmentos estables: "No se detectaron cambios significativos, manteniendo niveles consistentes de satisfacción." | Para segmentos con variaciones: "Las causas dominantes fueron [drivers SHAP], especialmente evidentes en [rutas top] y entre [perfiles reactivos]."]
            """,
            'Economy SH': """
    **ECONOMY SH: [Título]**
    [PÁRRAFO NARRATIVO FLUIDO] La cabina Economy de SH [descripción - para segmentos estables usar: "mantuvo desempeño estable"] durante la semana del [fecha], registrando un NPS de [valor cabina] ([fecha período]) con una [variación de NPS_diff cabina] puntos respecto a la semana anterior. [Para segmentos estables: "No se detectaron cambios significativos, manteniendo niveles consistentes de satisfacción." | Para segmentos con variaciones: "La causa principal fue [hipótesis con datos (drivers, operativa, NCS, verbatims) que la respaldan], complementada por [hipótesis secundarias (si las hubiera)]. Esta [mejora/deterioro] se reflejó especialmente en rutas como [top rutas con NPS y diff], mientras que los perfiles más reactivos incluyen [perfiles específicos]."]
            """,
            'Business SH': """
    **BUSINESS SH: [Título]**
    [PÁRRAFO NARRATIVO FLUIDO] El segmento Business de SH [descripción - para segmentos estables usar: "mantuvo desempeño estable"], registrando un NPS de [valor cabina] ([fecha]) con una [variación de diff cabina] puntos vs la semana anterior. [Para segmentos estables: "No se detectaron cambios significativos, manteniendo niveles consistentes de satisfacción." | Para segmentos con variaciones: "Esta evolución se explica principalmente por [causas SHAP], siendo especialmente visible en rutas como [rutas top] y entre perfiles [perfiles reactivos]."]
            """,
            'Premium SH': """
    **PREMIUM SH: [Título]**
    [PÁRRAFO NARRATIVO FLUIDO] El segmento Premium de SH [descripción - para segmentos estables usar: "mantuvo desempeño estable"], registrando un NPS de [valor cabina] ([fecha]) con [diff cabina] puntos de [variación] vs la semana anterior. [Para segmentos estables: "No se detectaron cambios significativos, manteniendo niveles consistentes de satisfacción." | Para segmentos con variaciones: "Las causas dominantes fueron [drivers SHAP], especialmente evidentes en [rutas top] y entre perfiles [perfiles reactivos]."]
            """,
            'Economy LH': """
    **ECONOMY LH: [Título]**
    [PÁRRAFO NARRATIVO FLUIDO] La cabina Economy de LH [descripción - para segmentos estables usar: "mantuvo desempeño estable"], registrando un NPS de [valor cabina] ([fecha período]) con una [variación de NPS_diff cabina] puntos respecto a la semana anterior. [Para segmentos estables: "No se detectaron cambios significativos, manteniendo niveles consistentes de satisfacción." | Para segmentos con variaciones: "La causa principal fue [hipótesis con datos (drivers, operativa, NCS, verbatims) que la respaldan], complementada por [hipótesis secundarias (si las hubiera)]. Esta [mejora/deterioro] se reflejó especialmente en rutas como [top rutas con NPS y diff], mientras que los perfiles más reactivos incluyen [perfiles específicos]."]
            """,
            'Business LH': """
    **BUSINESS LH: [Título]**  
    [PÁRRAFO NARRATIVO FLUIDO] La cabina Business de LH [descripción - para segmentos estables usar: "mantuvo desempeño estable"], registrando un NPS de [valor cabina] ([fecha]) con [diff cabina] puntos de [variación] vs período anterior. [Para segmentos estables: "No se detectaron cambios significativos, manteniendo niveles consistentes de satisfacción." | Para segmentos con variaciones: "Los drivers principales fueron [causas con SHAP], impactando especialmente las rutas transatlánticas [rutas específicas] y perfiles [perfiles específicos]."]
            """,
            'Premium LH': """
    **PREMIUM LH: [Título]**
    [PÁRRAFO NARRATIVO FLUIDO] El segmento Premium de LH [descripción - para segmentos estables usar: "mantuvo desempeño estable"], registrando un NPS de [valor cabina] ([fecha]) con [diff cabina] puntos de [variación] vs la semana anterior. [Para segmentos estables: "No se detectaron cambios significativos, manteniendo niveles consistentes de satisfacción." | Para segmentos con variaciones: "Las causas dominantes fueron [drivers SHAP], especialmente evidentes en [rutas top] y entre [perfiles reactivos]."]
            """,
            'IB': """
    **IB: [Título]**
    [PÁRRAFO NARRATIVO FLUIDO] La compañía IB [descripción - para segmentos estables usar: "mantuvo desempeño estable"], registrando un NPS de [valor cabina] ([fecha período]) con una [variación de NPS_diff cabina] puntos respecto a la semana anterior. [Para segmentos estables: "No se detectaron cambios significativos, manteniendo niveles consistentes de satisfacción." | Para segmentos con variaciones: "La causa principal fue [hipótesis con datos (drivers, operativa, NCS, verbatims) que la respaldan], complementada por [hipótesis secundarias (si las hubiera)]. Esta [mejora/deterioro] se reflejó especialmente en rutas como [top rutas con NPS y diff], mientras que los perfiles más reactivos incluyen [perfiles específicos]."]
            """,
            'YW': """
    **YW: [Título]**
    [PÁRRAFO NARRATIVO FLUIDO] La compañía YW [descripción - para segmentos estables usar: "mantuvo desempeño estable"], registrando un NPS de [valor cabina] ([fecha período]) con una [variación de NPS_diff cabina] puntos respecto a la semana anterior. [Para segmentos estables: "No se detectaron cambios significativos, manteniendo niveles consistentes de satisfacción." | Para segmentos con variaciones: "La causa principal fue [hipótesis con datos (drivers, operativa, NCS, verbatims) que la respaldan], complementada por [hipótesis secundarias (si las hubiera)]. Esta [mejora/deterioro] se reflejó especialmente en rutas como [top rutas con NPS y diff], mientras que los perfiles más reactivos incluyen [perfiles específicos]."]
            """
        }
        return cabin_sections.get(segment, "")


async def interpret_anomaly_tree(
    tree_data: str, 
    date: Optional[str] = None,
    segment: Optional[str] = None,
    llm_type: Optional[LLMType] = None
) -> str:
    """
    Convenience function to interpret an anomaly tree without creating an agent instance.
    
    Args:
        tree_data: Anomaly tree data to interpret
        date: Optional date context
        llm_type: LLM type to use
        
    Returns:
        Interpretation result
    """
    # Use default LLM type if none provided
    if llm_type is None:
        from dashboard_analyzer.anomaly_explanation.genai_core.utils.enums import get_default_llm_type
        llm_type = get_default_llm_type()
    agent = AnomalyInterpreterAgent(
        llm_type=llm_type,
        config_path="dashboard_analyzer/anomaly_explanation/config/prompts/anomaly_interpreter.yaml"
    )
    return await agent.interpret_anomaly_tree(tree_data, date, segment)


if __name__ == "__main__":
    # Example usage
    async def main():
        # Example anomaly tree data
        sample_tree = """
        Global: NEGATIVE ANOMALY (-12.5 pts)
          └─ Pattern: Negative anomaly driven by negative LH and negative SH
        
        ├─ LH (LH): NEGATIVE ANOMALY (-15.2 pts)
        │  └─ Analysis: High load factors (85-95%) across major routes
        │  
        │  ├─ Economy: NEGATIVE ANOMALY (-8.4 pts)
        │  │  └─ Analysis: Cabin crew satisfaction issues
        │  │
        │  ├─ Business: NEGATIVE ANOMALY (-22.1 pts)
        │  │  └─ Analysis: Food quality complaints on intercontinental routes
        │  │
        │  └─ Premium: NORMAL (0.2 pts)
        │     └─ Analysis: Maintained service standards
        │
        └─ SH (SH): NEGATIVE ANOMALY (-8.7 pts)
           └─ Analysis: Punctuality issues affecting customer satisfaction
        """
        
        agent = AnomalyInterpreterAgent(
            config_path="../../config/prompts/anomaly_interpreter.yaml"
        )
        result = await agent.interpret_anomaly_tree(sample_tree, "2025-05-24")
        print(result)
    
    asyncio.run(main()) 