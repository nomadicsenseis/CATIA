from abc import ABC, abstractmethod
from langchain.schema import SystemMessage
from langchain.tools import StructuredTool

from ..utils.enums import LLMType
from pydantic import BaseModel
from typing import Type, Optional


class LLM(ABC):
    """
    Abstract Base Class for Large Language Models (LLMs).

    Provides a common interface for interacting with different LLM implementations,
    handling features like tool binding, structured output enforcement,
    and basic configuration.
    """

    def __init__(self, llm_type: LLMType, token_input_price: float, token_output_price: float):
        """
        Initializes the LLM instance.

        Args:
            llm_type: The specific type of LLM being used (e.g., GPT4o_MINI).
            token_input_price: Cost per input token for this LLM.
            token_output_price: Cost per output token for this LLM.
        """
        self.token_input_price = token_input_price
        self.token_output_price = token_output_price
        self.llm_type = llm_type

        self.structured_output_prompt = SystemMessage(content='Responde siempre de forma estructurada con structured_output o llamando a otras tools')

        self.llm = self.create_llm()

    async def __call__(self, prompt: list, tools: list = None, structured_output: Optional[Type[BaseModel]] = None):
        """
        Invokes the LLM with the given prompt, optional tools, and structured output requirement.

        If structured_output is provided, it automatically adds a specific tool
        to enforce the output conforms to the provided Pydantic model and adds a guiding
        system message to the prompt.

        Args:
            prompt: A list of LangChain BaseMessage objects representing the conversation history.
            tools: An optional list of LangChain tools the LLM can use.
            structured_output: An optional Pydantic BaseModel class defining the desired
                               output structure.

        Returns:
            The AIMessage response from the LLM, which might include tool calls or
            structured output data.
        """
        if structured_output is not None:
            prompt = prompt + [self.structured_output_prompt]
            tools = self._add_structured_output(tools, structured_output)

        # Get response from LLM (which might include tool calls)
        if tools is not None:
            llm_with_tools = self.llm.bind_tools(tools)
            response_invoke = await llm_with_tools.ainvoke(prompt)
        else:
            response_invoke = await self.llm.ainvoke(prompt)
        return response_invoke

    def _add_structured_output(self, tools, structured_output: Optional[Type[BaseModel]]):
        """
        Adds a structured output tool to the list of tools if a model is provided.

        This internal helper creates a LangChain StructuredTool named 'structured_output'
        based on the provided Pydantic model.

        Args:
            tools: The existing list of tools (or None).
            structured_output: The Pydantic BaseModel class for the desired output.

        Returns:
            The list of tools, potentially augmented with the structured_output tool.
        """
        if tools is None:
            tools = []

        output_tool = StructuredTool.from_function(
            name="structured_output",
            description=(
                "Utiliza esta herramienta cuando vayas a responder al usuario. "
                "Completa todos los campos requeridos. Devuelve siempre True."
            ),
            func=lambda **kwargs: True,
            args_schema=structured_output,
            return_direct=True
        )
        tools.append(output_tool)

        return tools

    async def stream_response(self, prompt):
        """
        Streams the LLM's response for the given prompt.

        Args:
            prompt: The input message or sequence of messages (list of BaseMessage).

        Yields:
            str: Chunks of the response content as they are generated.
            str: The final, complete response text after the stream ends.
        """
        response_text = ""
        
        async for chunk in self.llm.astream(prompt):
            chunk_text = chunk.content
            response_text += chunk_text
            yield chunk_text

        yield response_text

    @abstractmethod
    def create_llm(self):
        """Instantiate and return the specific LangChain LLM client.

        This method must be implemented by subclasses to configure and return
        the appropriate LLM object (e.g., AzureChatOpenAI, ChatAnthropic).
        """
        pass 