"""
FastAPI server for Claude API operations
Provides an HTTP interface for Claude API operations
"""
import os
import logging
import json
from typing import Dict, List, Optional, Any, Union
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import anthropic
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="Claude API Server",
    description="API server for Claude Desktop API Integration",
    version="1.0.0"
)

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
DEFAULT_MODEL = "claude-3-7-sonnet-20250219"

# Models for API requests and responses
class Message(BaseModel):
    role: str
    content: str

class ConversationRequest(BaseModel):
    prompt: str
    conversation_id: str = "default"
    system_prompt: Optional[str] = None
    model: str = DEFAULT_MODEL
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)
    max_tokens: int = Field(default=4096, ge=1, le=100000)

class ConversationResponse(BaseModel):
    response: str
    conversation_id: str
    model: str
    usage: Dict[str, Any]

class ConversationListResponse(BaseModel):
    conversations: List[str]

class ModelsResponse(BaseModel):
    models: Dict[str, str]

# In-memory storage for conversations
conversations: Dict[str, List[Dict[str, Any]]] = {}

@app.get("/", tags=["Root"])
async def root():
    """API server root endpoint"""
    return {
        "message": "Claude API Server is running",
        "version": "1.0.0"
    }

@app.post("/api/query", response_model=ConversationResponse, tags=["Conversations"])
async def query_claude(request: ConversationRequest):
    """
    Query Claude API with a prompt and manage conversation history
    """
    try:
        # Initialize conversation if it doesn't exist
        conversation_id = request.conversation_id
        if conversation_id not in conversations:
            conversations[conversation_id] = []
        
        # Get conversation history
        messages = conversations[conversation_id]
        
        # Construct the new message
        user_message = {
            "role": "user",
            "content": request.prompt
        }
        
        # Add message to history
        messages.append(user_message)
        
        # Validate model
        model = request.model
        if model not in AVAILABLE_MODELS:
            logger.warning(f"Model {model} not found. Using default model {DEFAULT_MODEL}")
            model = DEFAULT_MODEL
        
        # Make API call to Claude
        response = client.messages.create(
            model=model,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            system=request.system_prompt,
            messages=messages
        )
        
        # Store Claude's response
        assistant_message = {
            "role": "assistant",
            "content": response.content[0].text
        }
        messages.append(assistant_message)
        
        # Create response object
        response_data = {
            "response": response.content[0].text,
            "conversation_id": conversation_id,
            "model": model,
            "usage": {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens
            }
        }
        
        return response_data
    except Exception as e:
        logger.error(f"Error querying Claude API: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error querying Claude API: {str(e)}")

@app.get("/api/conversation/{conversation_id}", tags=["Conversations"])
async def get_conversation(conversation_id: str):
    """
    Get conversation history for a specific ID
    """
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail=f"Conversation {conversation_id} not found")
    
    return {"conversation": conversations[conversation_id]}

@app.delete("/api/conversation/{conversation_id}", tags=["Conversations"])
async def clear_conversation(conversation_id: str):
    """
    Clear conversation history for a specific ID
    """
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail=f"Conversation {conversation_id} not found")
    
    conversations[conversation_id] = []
    return {"message": f"Conversation {conversation_id} cleared successfully"}

@app.get("/api/conversations", response_model=ConversationListResponse, tags=["Conversations"])
async def list_conversations():
    """
    List all available conversation IDs
    """
    return {"conversations": list(conversations.keys())}

@app.get("/api/models", response_model=ModelsResponse, tags=["Models"])
async def get_models():
    """
    Get all available Claude models
    """
    return {"models": AVAILABLE_MODELS}

def start_server(host: str = "0.0.0.0", port: int = None):
    """
    Start the FastAPI server
    """
    if port is None:
        # Get port from environment or use default
        port = int(os.getenv("API_SERVER_PORT", 8000))
    
    # Start the server
    logger.info(f"Starting API server on http://{host}:{port}")
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    start_server()
