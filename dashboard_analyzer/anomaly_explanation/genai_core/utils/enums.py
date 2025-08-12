from enum import Enum

# Global model configuration - change this to switch all agents at once
DEFAULT_LLM_TYPE = "CLAUDE_SONNET_4"  # Options: O4_MINI, CLAUDE_SONNET_4, O3, etc.

class MessageType(Enum):
    """
    Enumerated type representing the possible message types.
    It distinguishes between messages from the user, the AI model, and system-level messages.
    """
    USER = 'USER'
    AI = 'AI'
    SYSTEM = 'SYSTEM'
    TOOL = 'TOOL'

class LLMType(Enum):
    """
    Enumerated type representing the Large Language Models (LLM) types.
    This could be used to choose between different versions or types of AI models for different tasks.
    """
    CLAUDE_V2 = 'CLAUDE_V2'
    CLAUDE_INSTANT = 'CLAUDE_INSTANT'
    CLAUDE_3_HAIKU = 'CLAUDE_3_HAIKU'
    CLAUDE_3_5_HAIKU = 'CLAUDE_3_5_HAIKU'
    CLAUDE_3_OPUS = 'CLAUDE_3_OPUS'
    CLAUDE_3_5_SONNET = 'CLAUDE_3_5_SONNET'
    CLAUDE_3_5_SONNET_V2 = 'CLAUDE_3_5_SONNET_V2'
    CLAUDE_SONNET_4 = 'CLAUDE_SONNET_4'
    GPT3_5 = 'GPT3_5'
    GPT4 = 'GPT4'
    GPT4o = 'GPT4o'
    GPT4o_MINI = 'GPT4o_MINI'
    O1_MINI = 'O1_MINI'  # o1-mini in Azure OpenAI
    O3_MINI = 'O3_MINI'  # o3-mini in Azure OpenAI
    O3 = 'O3'            # o3 in Azure OpenAI
    O4_MINI = 'O4_MINI'  # o4-mini in Azure OpenAI
    LLAMA3_70 = 'LLAMA3_70'
    LLAMA3_1_70 = 'LLAMA3_1_70'
    LLAMA3_1_405 = 'LLAMA3_1_405'
    CLAUDE_3_7_SONNET = 'CLAUDE_3_7_SONNET'

def get_default_llm_type() -> LLMType:
    """Get the default LLM type from the global configuration"""
    try:
        return LLMType[DEFAULT_LLM_TYPE]
    except KeyError:
        # Fallback to O4_MINI if the configured type doesn't exist
        return LLMType.O4_MINI

class AgentName(Enum):
    """
    Enumerated type representing the various agent names.
    This could be used to categorize or distinguish between different functionalities
    or responsibilities of agents within the system.
    """
    CONVERSATIONAL = 'CONVERSATIONAL'
