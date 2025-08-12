import json
import os

from langchain_aws import ChatBedrock
from botocore.config import Config
import boto3

from ..utils.enums import LLMType
from .llm import LLM

# Make BEDROCK_MODELS optional to avoid errors when not using AWS
try:
    BEDROCK_MODELS = json.loads(os.environ.get("BEDROCK_MODELS", "{}"))
except (json.JSONDecodeError, KeyError):
    BEDROCK_MODELS = {}


class AWSLLM(LLM):
    """
    AWSLLM class that uses LangChain's ChatBedrock integration
    """

    def __init__(self, llm_type: LLMType, region_name, aws_access_key_id=None, aws_secret_access_key=None, profile_name=None,
                 token_input_price: float = 11.02 / 1000000, token_output_price: float = 32.68 / 1000000):
        self.region_name = region_name
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.profile_name = profile_name
        self.model_id = None

        super().__init__(llm_type, token_input_price, token_output_price)

    def create_llm(self):
        """Create the LangChain ChatBedrock client for the specified model"""
        self._set_model_id()
        
        # Configure credentials for boto3 session (if needed)
        credentials = {}
        if self.aws_access_key_id and self.aws_secret_access_key:
            credentials["aws_access_key_id"] = self.aws_access_key_id
            credentials["aws_secret_access_key"] = self.aws_secret_access_key
        if self.profile_name:
            credentials["profile_name"] = self.profile_name
        
        # Determine provider based on model ID
        provider = self._get_provider()
        
        # Build a boto3 client with extended timeouts and retries to handle long generations
        read_timeout = int(os.getenv("BEDROCK_READ_TIMEOUT", "300"))
        connect_timeout = int(os.getenv("BEDROCK_CONNECT_TIMEOUT", "15"))
        max_attempts = int(os.getenv("BEDROCK_MAX_RETRIES", "3"))
        cfg = Config(read_timeout=read_timeout, connect_timeout=connect_timeout, retries={"max_attempts": max_attempts, "mode": "standard"})

        session = boto3.Session(
            aws_access_key_id=credentials.get("aws_access_key_id"),
            aws_secret_access_key=credentials.get("aws_secret_access_key"),
            profile_name=credentials.get("profile_name"),
            region_name=self.region_name,
        )
        bedrock_client = session.client("bedrock-runtime", config=cfg)

        # Create ChatBedrock client with custom boto3 client and tunable generation params
        max_tokens = int(os.getenv("BEDROCK_MAX_TOKENS", "15000"))
        temperature = float(os.getenv("BEDROCK_TEMPERATURE", "0.7"))
        return ChatBedrock(
            model_id=self.model_id,
            client=bedrock_client,
            provider=provider,
            model_kwargs={
                "max_tokens": max_tokens,
                "temperature": temperature,
            }
        )
    
    def _get_provider(self):
        """Get the provider name based on the model type"""
        if self.llm_type.value in [
            LLMType.CLAUDE_3_HAIKU.value, 
            LLMType.CLAUDE_3_5_HAIKU.value,
            LLMType.CLAUDE_3_OPUS.value,
            LLMType.CLAUDE_3_5_SONNET.value,
            LLMType.CLAUDE_3_5_SONNET_V2.value,
            LLMType.CLAUDE_SONNET_4.value,
            LLMType.CLAUDE_3_7_SONNET.value
        ]:
            return "anthropic"
        elif self.llm_type.value in [
            LLMType.LLAMA3_70.value,
            LLMType.LLAMA3_1_70.value,
            LLMType.LLAMA3_1_405.value
        ]:
            return "meta"
        else:
            raise ValueError(f"Unknown provider for model: {self.llm_type}")
    
    def _set_model_id(self):
        """Set the appropriate model ID based on the LLM type"""
        if self.llm_type.value == LLMType.CLAUDE_3_HAIKU.value:
            self.model_id = BEDROCK_MODELS.get("anthropic.claude-3-haiku-20240307-v1:0", "anthropic.claude-3-haiku-20240307-v1:0")
        elif self.llm_type.value == LLMType.CLAUDE_3_5_HAIKU.value:
            self.model_id = 'anthropic.claude-3-5-haiku-20241022-v1:0'
        elif self.llm_type.value == LLMType.CLAUDE_3_OPUS.value:
            self.model_id = 'anthropic.claude-3-opus-20240229-v1:0'
        elif self.llm_type.value == LLMType.LLAMA3_70.value:
            self.model_id = "meta.llama3-70b-instruct-v1:0"
        elif self.llm_type.value == LLMType.LLAMA3_1_70.value:
            self.model_id = "meta.llama3-1-70b-instruct-v1:0"
        elif self.llm_type.value == LLMType.LLAMA3_1_405.value:
            self.model_id = "meta.llama3-1-405b-instruct-v1:0"
        elif self.llm_type.value == LLMType.CLAUDE_3_5_SONNET.value:
            self.model_id = BEDROCK_MODELS.get("anthropic.claude-3-5-sonnet-20240620-v1:0", "anthropic.claude-3-5-sonnet-20240620-v1:0")
        elif self.llm_type.value == LLMType.CLAUDE_3_5_SONNET_V2.value:
            self.model_id = "anthropic.claude-3-5-sonnet-20241022-v2:0"
        elif self.llm_type.value == LLMType.CLAUDE_SONNET_4.value:
            self.model_id = "arn:aws:bedrock:us-east-1:737192913161:inference-profile/us.anthropic.claude-sonnet-4-20250514-v1:0"
        elif self.llm_type.value == LLMType.CLAUDE_3_7_SONNET.value:
            # Use MODEL_ARN from environment for inference profile
            model_arn = os.getenv('MODEL_ARN')
            if model_arn:
                self.model_id = model_arn
            else:
                self.model_id = "anthropic.claude-3-7-sonnet-20250219-v1:0"
        else:
            raise ValueError(f"Invalid model: {self.llm_type}")