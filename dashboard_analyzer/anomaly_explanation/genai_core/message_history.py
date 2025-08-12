from typing import List, Optional, Dict, Any, Union
from .utils.enums import MessageType, AgentName
from langchain.schema import BaseMessage
import os
import base64
import logging

from langchain.schema.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage
)

class MessageHistory:
    """
    Manages a history of messages in a conversation.

    Stores messages along with metadata like the originating agent (for AI messages),
    message type, and visibility status.
    Provides methods for adding messages, retrieving them in different formats,
    and serialization. Supports multimodal content (images).
    """

    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initializes an empty list to store message entries.
        Each entry is a dictionary containing the agent, message object,
        visibility status, and message type.
        
        Args:
            logger: Optional logger instance for logging. If None, logging is disabled.
        """
        self.messages: List[Dict[str, Any]] = []
        self.logger = logger or logging.getLogger("disabled")

        self.logger.debug("MessageHistory initialized")

    def create_and_add_message(
        self,
        content: Union[str, List[Dict[str, Any]]],
        message_type: MessageType,
        agent: Optional[AgentName] = None,
        visible: bool = True,
        tool_call_id: Optional[str] = None,  # Required for ToolMessage
        images: Union[List[str], str] = None  # Image URLs or file paths
    ):
        """
        Adds a new message to the history with support for multimodal content.

        Args:
            content: The content of the message. Can be:
                    - A string for text-only messages
                    - A list of dictionaries for multimodal content, where each dict 
                      represents a content part (text, image)
            message_type: The type of the message (USER, AI, SYSTEM, TOOL).
            agent: The agent that generated the message (required for AI type).
            visible: Whether the message should be visible to the end-user.
                     Defaults to True.
            tool_call_id: The ID associated with a tool call (only for TOOL type).
            images: Optional list of image URLs or file paths, or a single image URL/path.
                    Will be added to the content if provided.
        """
        if message_type == MessageType.AI and agent is None:
            error_msg = "Agent must be specified for AI messages."
            self.logger.error(error_msg)
            raise ValueError(error_msg)
            
        if message_type != MessageType.AI and agent is not None:
            self.logger.warning("Agent specified for non-AI message. Ignoring agent.")
            agent = None
            
        if message_type == MessageType.TOOL and tool_call_id is None:
            error_msg = "tool_call_id must be specified for TOOL messages."
            self.logger.error(error_msg)
            raise ValueError(error_msg)

        # If content is a string and we have images, convert to multimodal format
        if isinstance(content, str) and images:
            content = self._create_multimodal_content(content, images)

        # For System and Tool messages, ensure content is text-only
        if message_type in [MessageType.SYSTEM, MessageType.TOOL]:
            if not isinstance(content, str):
                error_msg = f"{message_type.name} messages must be text only"
                self.logger.error(error_msg)
                raise ValueError(error_msg)

        message: BaseMessage
        if message_type == MessageType.AI:
            message = AIMessage(content=content)
        elif message_type == MessageType.USER:
            message = HumanMessage(content=content)
        elif message_type == MessageType.SYSTEM:
            message = SystemMessage(content=content)
        elif message_type == MessageType.TOOL:
            message = ToolMessage(content=content, tool_call_id=tool_call_id)
        else:
            error_msg = f"Unsupported message type: {message_type}"
            self.logger.error(error_msg)
            raise ValueError(error_msg)

        self.messages.append({
            "agent": agent,
            "message": message,
            "visible": visible,
            "type": message_type
        })
    
    def _create_multimodal_content(
        self, 
        text: str, 
        images: Union[List[str], str] = None
    ) -> List[Dict[str, Any]]:
        """
        Creates a multimodal content structure from text and media items.
        
        Args:
            text: The text content of the message
            images: Single image path/URL or list of image paths/URLs
            
        Returns:
            List of content blocks for multimodal LLM input
        """
        multimodal_content = [{"type": "text", "text": text}]
        
        # Process images
        if images:
            if isinstance(images, str):
                images = [images]  # Convert single image to list
            
            for img in images:
                if os.path.exists(img):  # Local file path
                    # Encode image to base64
                    mime_type = self._get_mime_type(img)
                    with open(img, "rb") as f:
                        img_data = f.read()
                    img_url = f"data:{mime_type};base64,{base64.b64encode(img_data).decode('utf-8')}"
                else:  # Assume it's a URL
                    img_url = img
                
                multimodal_content.append({
                    "type": "image_url",
                    "image_url": {"url": img_url}
                })
        
        return multimodal_content
    
    def _get_mime_type(self, file_path: str) -> str:
        """Determine MIME type based on file extension"""
        extension = os.path.splitext(file_path)[1].lower()
        
        # Image MIME types
        if extension in ['.jpg', '.jpeg']:
            return 'image/jpeg'
        elif extension == '.png':
            return 'image/png'
        elif extension == '.gif':
            return 'image/gif'
        elif extension == '.webp':
            return 'image/webp'
        
        # Default fallback
        else:
            return 'application/octet-stream'

    def add_message(
        self,
        message,
        agent: Optional[AgentName] = None,
        visible: bool = True,
    ):
        """
        Adds a new message to the history.

        Args:
            message: The message. Can be a LangChain message with text-only or 
                   multimodal content.
            agent: The agent that generated the message (required for AI type).
            visible: Whether the message should be visible to the end-user.
                     Defaults to True.
        """
        if isinstance(message, AIMessage):
            message_type = MessageType.AI
        elif isinstance(message, HumanMessage):
            message_type = MessageType.USER
        elif isinstance(message, SystemMessage):
            message_type = MessageType.SYSTEM
        elif isinstance(message, ToolMessage):
            message_type = MessageType.TOOL
        else:
            error_msg = f"Unsupported message object: {type(message)}"
            self.logger.error(error_msg)
            raise ValueError(error_msg)

        self.messages.append({
            "agent": agent,
            "message": message,
            "visible": visible,
            "type": message_type
        })

    def get_messages(self, include_agent_name_in_content: bool = False) -> List[BaseMessage]:
        """
        Retrieves the messages formatted as a list suitable for LLM prompts.

        Args:
            include_agent_name_in_content: If True, prepend the agent's name
                                               to the content of AI messages.

        Returns:
            A list of LangChain BaseMessage objects.
        """
        prompt_messages = []
        for entry in self.messages:
            message = entry["message"]
            agent = entry["agent"]
            message_type = entry["type"]

            if include_agent_name_in_content and message_type == MessageType.AI and agent:
                # Create a new AIMessage with modified content
                # This is more complex with multimodal content
                content = message.content
                
                if isinstance(content, str):
                    # Text-only content
                    modified_content = f"[{agent.name}]: {content}"
                    prompt_messages.append(AIMessage(content=modified_content))
                else:
                    # Multimodal content (list of content blocks)
                    modified_content = list(content)  # Create a copy
                    
                    # Find and modify the first text block
                    for i, block in enumerate(modified_content):
                        if block.get("type") == "text":
                            modified_content[i] = {
                                "type": "text",
                                "text": f"[{agent.name}]: {block['text']}"
                            }
                            break
                    
                    prompt_messages.append(AIMessage(content=modified_content))
            else:
                # Append the original message object
                prompt_messages.append(message)
                
        return prompt_messages

    def to_str(self, visible_only: bool = False) -> str:
        """
        Converts the message history to a formatted string.

        Args:
            visible_only: If True, only include messages marked as visible.

        Returns:
            A string representation of the message history.
        """
        output_lines = []
        for entry in self.messages:
            if visible_only and not entry["visible"]:
                continue

            message = entry["message"]
            agent = entry["agent"]
            message_type = entry["type"]
            visibility = "(internal)" if not entry["visible"] else ""

            prefix = f"{message_type.name}{' [' + agent.name + ']' if agent else ''}: "
            
            content = message.content
            if isinstance(content, str):
                # Text-only content
                output_lines.append(f"{prefix}{content} {visibility}".strip())
            else:
                # Multimodal content
                text_parts = []
                has_image = False
                
                for item in content:
                    if item.get("type") == "text":
                        text_parts.append(item.get("text", ""))
                    elif item.get("type") == "image_url":
                        has_image = True
                
                # Join all text parts
                text_content = " ".join(text_parts)
                
                # Add indicators for multimodal content
                media_str = "[IMAGE]" if has_image else ""
                
                output_lines.append(f"{prefix}{text_content} {media_str} {visibility}".strip())

        return "\n".join(output_lines)

    def to_dict(self) -> Dict[str, Any]:
        """
        Serializes the MessageHistory instance into a dictionary.

        Returns:
            A dictionary representation suitable for persistence (e.g., JSON).
        """
        serialized_messages = []
        for entry in self.messages:
            message = entry["message"]
            
            # Handle both text and multimodal content
            message_data = {"content": message.content}
            
            # Add tool_call_id if it's a ToolMessage
            if isinstance(message, ToolMessage):
                message_data["tool_call_id"] = message.tool_call_id

            serialized_messages.append({
                "agent": entry["agent"].value if entry["agent"] else None,
                "message_data": message_data,  # Store core attributes directly
                "type": entry["type"].value,
                "visible": entry["visible"],
                "message_class": message.__class__.__name__ # Store class name for deserialization
            })

        return {"messages": serialized_messages}

    @classmethod
    def from_dict(cls, data: Dict[str, Any], logger: Optional[logging.Logger] = None) -> 'MessageHistory':
        """
        Deserializes a dictionary (using the simpler format) into a MessageHistory instance.

        Args:
            data: The dictionary containing the serialized message history.
            logger: Optional logger instance for logging.

        Returns:
            A new MessageHistory instance populated with the data.
        """
        if logger:
            logger.debug("Deserializing message history from dictionary")
            
        history = cls(logger=logger)
        message_class_map = {
            "AIMessage": AIMessage,
            "HumanMessage": HumanMessage,
            "SystemMessage": SystemMessage,
            "ToolMessage": ToolMessage
        }

        for entry_data in data.get("messages", []):
            agent_value = entry_data.get("agent")
            message_data = entry_data.get("message_data")
            type_value = entry_data.get("type")
            visible = entry_data.get("visible", True)
            message_class_name = entry_data.get("message_class")

            if not all([message_data, type_value, message_class_name]):
                error_msg = f"Skipping malformed message entry: {entry_data}"
                if logger:
                    logger.warning(error_msg)
                else:
                    print(error_msg)
                continue

            agent = AgentName(agent_value) if agent_value else None
            message_type = MessageType(type_value)

            message_cls = message_class_map.get(message_class_name)
            if not message_cls:
                error_msg = f"Unknown message class '{message_class_name}'. Skipping."
                if logger:
                    logger.warning(error_msg)
                else:
                    print(error_msg)
                continue

            try:
                content = message_data.get("content")
                if content is None:
                    raise ValueError("Message content missing")

                if message_cls == ToolMessage:
                    tool_call_id = message_data.get("tool_call_id")
                    if tool_call_id is None:
                        raise ValueError("tool_call_id missing for ToolMessage")
                    message = ToolMessage(content=content, tool_call_id=tool_call_id)
                else:
                    message = message_cls(content=content)

            except Exception as e:
                error_msg = f"Error reconstructing message: {e}. Skipping entry: {entry_data}"
                if logger:
                    logger.error(error_msg)
                else:
                    print(error_msg)
                continue

            history.messages.append({
                "agent": agent,
                "message": message,
                "visible": visible,
                "type": message_type
            })
            
        if logger:
            logger.debug("Message history deserialized with %d message(s)", len(history.messages))
            
        return history 