from langchain_openai import AzureChatOpenAI

from ..utils.enums import LLMType
from .llm import LLM


class OpenAiLLM(LLM):
    """
    OpenAiLLM represents a Large Language Model hosted on OpenAI.
    """

    def __init__(self, llm_type: LLMType, api_key: str, api_base: str, api_version: str,
                 api_dep_gpt: str,
                 token_input_price: float = 3.75 / 1000000, token_output_price: float = 15 / 1000000,
                 temperature: float = 0.1, size: int = 4):
        """
        Initialize the OpenAiLLM instance.

        :param llm_type: Specifies the type of LLM.
        :param api_type, api_key, api_base, api_version: Configuration parameters for OpenAI API.
        :param token_input_price: Cost per input token (default is provided).
        :param token_output_price: Cost per output token (default is provided).
        :param temperature: Sampling temperature for model response.
        :param size: Size configuration for the model.
        """
        # Configure OpenAI API
        self.api_base = api_base
        self.api_key = api_key
        self.api_dep_gpt = api_dep_gpt

        self.size = size
        self.api_version = api_version
        self.temperature = temperature

        super().__init__(llm_type, token_input_price, token_output_price)

    def create_llm(self):
        """
        Establish connection with OpenAI and instantiate the appropriate language model.

        :return: Configured LLM from OpenAI.
        """
        return AzureChatOpenAI(
            azure_endpoint=self.api_base,
            openai_api_key=self.api_key,
            deployment_name=self.api_dep_gpt,
            openai_api_version=self.api_version,
            temperature=self.temperature,
            max_completion_tokens=3000
        ) 