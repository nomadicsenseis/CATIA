"""
Agent Base Class - Clase base para todos los agentes GenAI
Proporciona funcionalidades comunes y estructura estándar para agentes
"""

from datetime import datetime
from typing import Optional, Type, List, Any, Union
import logging

from pydantic import BaseModel


class Agent:
    """
    Generic Agent class that can be used directly or extended for specialized agents.
    
    Provides built-in functionality for:
    - Tool/function calling
    - Structured output
    - Performance tracking (tokens, cost, time)
    - Streaming responses
    """

    def __init__(
        self,
        llm,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize the Agent with configurable components.
        
        Args:
            llm: Language model instance to use for generating responses
            logger: Optional logger instance for logging. If None, logging is disabled.
        """
        self.llm = llm
        self.logger = logger or logging.getLogger("disabled")

        # Performance tracking
        self.total_time = 0
        self.last_execution_time = 0
        self.avg_time = 0
        self.num_calls = 0
        self.call_times = []
        self.input_tokens = 0
        self.output_tokens = 0
        self.money_spent = 0
        
        self.logger.debug("Agent initialized with LLM: %s", type(llm).__name__)

    async def invoke(
        self,
        messages: list,
        structured_output: Optional[Type[BaseModel]] = None,
        tools: Optional[List[Any]] = None
    ):
        """
        Process user input and generate a response using the LLM. (non-streaming)

        Args:
            messages: Optional message history
            structured_output: Optional Pydantic model for structured output
            tools: Optional list of available tools

        Returns:
            response, structured_response, tool_calls
        """
        self.logger.debug("Invoking LLM with %d messages", len(messages))
        if structured_output:
            self.logger.debug("Using structured output: %s", structured_output.__name__)
        if tools:
            self.logger.debug("Using %d tools", len(tools))

        # Start measuring execution time
        start_time = datetime.now()

        # Call the LLM with tools and structured output if needed
        response = await self.llm(
            messages,
            tools=tools,
            structured_output=structured_output
        )

        # Calculate execution time
        execution_time = (datetime.now() - start_time).total_seconds()
        self._update_metrics(execution_time)

        # Tokens and money
        self.input_tokens += response.usage_metadata['input_tokens']
        self.output_tokens += response.usage_metadata['output_tokens']
        self.money_spent = self.input_tokens*self.llm.token_input_price + self.output_tokens*self.llm.token_output_price

        self.logger.debug("LLM response received. Input tokens: %d, Output tokens: %d", 
                         response.usage_metadata['input_tokens'], 
                         response.usage_metadata['output_tokens'])

        # Get structured response
        tools = response.tool_calls
        structured_response = [tool for tool in tools if tool['name'] == 'structured_output']
        structured_response = structured_response[0] if len(structured_response) else None

        # Get called tools
        tool_calls = [tool for tool in tools if tool['name'] != 'structured_output']
        tool_calls = tool_calls if len(tool_calls) else None

        if structured_response:
            self.logger.debug("Structured response received")
        if tool_calls:
            self.logger.debug("Tool calls received: %d tool(s)", len(tool_calls))

        return response, structured_response, tool_calls

    async def ainvoke(self, messages: list):
        """
        Process user input and generate a response using the LLM. (streaming)

        Args:
            messages: Optional message history

        Yield:
            Message chunk

        """
        self.logger.debug("Streaming LLM response for %d messages", len(messages))
        
        # Start measuring execution time
        start_time = datetime.now()
            
        # Stream response chunks
        response_text = ""

        async for chunk in self.llm.stream_response(messages):
            response_text += chunk
            yield chunk

        # Calculate execution time and update metrics
        execution_time = (datetime.now() - start_time).total_seconds()
        self._update_metrics(execution_time)
        
        self.logger.debug("Streaming complete. Execution time: %.2f seconds", execution_time)

    def _update_metrics(self, execution_time):
        """Update agent performance metrics."""
        self.num_calls += 1
        self.last_execution_time = execution_time
        self.total_time += execution_time
        self.call_times.append(execution_time)
        self.avg_time = self.total_time / self.num_calls if self.num_calls > 0 else 0

    async def execute_tools(self, mcp_manager, tool_calls):
        """
        Execute tool calls using an MCP manager.
        
        Args:
            mcp_manager: The MCPClientManager instance
            tool_calls: Tool calls

        Returns:
            tools responses
        """
        self.logger.debug("Executing %d tool call(s) with MCP manager", len(tool_calls) if tool_calls else 0)
        
        # Execute tool calls
        tool_responses = await mcp_manager.execute_tool_calls(tool_calls)
        
        self.logger.debug("Tool execution complete. Received %d response(s)", len(tool_responses))
        return tool_responses 