"""
MCP Server implementation for Claude Desktop API integration
"""
import os
import logging
import json
from typing import Dict, List, Optional, Any, Union
from mcp.server.fastmcp import FastMCP
import anthropic
from pydantic import BaseModel

# Initialize logging
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("ClaudeAPI")

# Get API key from environment
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    logger.error("ANTHROPIC_API_KEY environment variable not set. Please set it in .env file.")
    raise ValueError("ANTHROPIC_API_KEY environment variable not set")

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=api_key)

# Get available models
AVAILABLE_MODELS = {
    "claude-3-opus-20240229": "Claude 3 Opus",
    "claude-3-sonnet-20240229": "Claude 3 Sonnet",
    "claude-3-haiku-20240307": "Claude 3 Haiku",
    "claude-3-5-sonnet-20240620": "Claude 3.5 Sonnet",
    "claude-3-haiku-20240307": "Claude 3 Haiku",
}

# Default model to use
DEFAULT_MODEL = "claude-3-sonnet-20240229"

class KnowledgeBase:
    """
    Knowledge base to store conversation history
    """
    def __init__(self):
        self.conversations: Dict[str, List[Dict[str, Any]]] = {}
    
    def add_message(self, conversation_id: str, message: Dict[str, Any]) -> None:
        """Add a message to the conversation history"""
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []
        self.conversations[conversation_id].append(message)
    
    def get_conversation(self, conversation_id: str) -> List[Dict[str, Any]]:
        """Get the conversation history for a specific ID"""
        return self.conversations.get(conversation_id, [])
    
    def clear_conversation(self, conversation_id: str) -> bool:
        """Clear a specific conversation history"""
        if conversation_id in self.conversations:
            self.conversations[conversation_id] = []
            return True
        return False
    
    def list_conversations(self) -> List[str]:
        """List all available conversation IDs"""
        return list(self.conversations.keys())

# Initialize knowledge base
kb = KnowledgeBase()

@mcp.tool()
async def query_claude(
    prompt: str, 
    conversation_id: str = "default", 
    system_prompt: Optional[str] = None,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.7,
    max_tokens: int = 4096
) -> str:
    """
    Query Claude API with a prompt and optional system prompt
    
    Args:
        prompt: The user's query
        conversation_id: Unique identifier for the conversation
        system_prompt: Optional system prompt to guide Claude's behavior
        model: Claude model to use (default: claude-3-sonnet-20240229)
        temperature: Temperature for response generation (0.0-1.0)
        max_tokens: Maximum tokens to generate
    """
    try:
        logger.info(f"Querying Claude API with model {model} for conversation {conversation_id}")
        
        # Validate model
        if model not in AVAILABLE_MODELS:
            logger.warning(f"Model {model} not found. Using default model {DEFAULT_MODEL}")
            model = DEFAULT_MODEL
        
        # Get conversation history
        messages = kb.get_conversation(conversation_id)
        
        # Construct the new message
        message = {
            "role": "user",
            "content": prompt
        }
        
        # Add message to history
        kb.add_message(conversation_id, message)
        
        # Make API call to Claude
        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt if system_prompt else None,
            messages=messages + [message]
        )
        
        # Store Claude's response
        assistant_message = {
            "role": "assistant",
            "content": response.content[0].text
        }
        kb.add_message(conversation_id, assistant_message)
        
        return response.content[0].text
    except Exception as e:
        logger.error(f"Error querying Claude API: {str(e)}", exc_info=True)
        return f"Error querying Claude API: {str(e)}"

@mcp.tool()
async def clear_conversation(conversation_id: str = "default") -> str:
    """
    Clear a specific conversation history
    
    Args:
        conversation_id: Unique identifier for the conversation to clear
    """
    try:
        logger.info(f"Clearing conversation {conversation_id}")
        
        if kb.clear_conversation(conversation_id):
            return f"Conversation {conversation_id} cleared successfully"
        return f"Conversation {conversation_id} not found"
    except Exception as e:
        logger.error(f"Error clearing conversation: {str(e)}", exc_info=True)
        return f"Error clearing conversation: {str(e)}"

@mcp.tool()
async def get_conversation_history(conversation_id: str = "default") -> str:
    """
    Get the conversation history for a specific ID
    
    Args:
        conversation_id: Unique identifier for the conversation
    """
    try:
        logger.info(f"Retrieving conversation history for {conversation_id}")
        
        history = kb.get_conversation(conversation_id)
        return json.dumps(history, indent=2)
    except Exception as e:
        logger.error(f"Error retrieving conversation history: {str(e)}", exc_info=True)
        return f"Error retrieving conversation history: {str(e)}"

@mcp.tool()
async def list_conversations() -> str:
    """
    List all available conversation IDs
    """
    try:
        logger.info("Listing all conversations")
        
        conversations = kb.list_conversations()
        if not conversations:
            return "No conversations found"
        
        return json.dumps(conversations, indent=2)
    except Exception as e:
        logger.error(f"Error listing conversations: {str(e)}", exc_info=True)
        return f"Error listing conversations: {str(e)}"

@mcp.tool()
async def list_available_models() -> str:
    """
    List all available Claude models
    """
    try:
        logger.info("Listing available models")
        
        return json.dumps(AVAILABLE_MODELS, indent=2)
    except Exception as e:
        logger.error(f"Error listing models: {str(e)}", exc_info=True)
        return f"Error listing models: {str(e)}"

def start_server() -> None:
    """Start the MCP server"""
    logger.info("Starting MCP server")
    mcp.run()
