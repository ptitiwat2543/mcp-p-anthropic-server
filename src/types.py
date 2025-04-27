"""
Type definitions for Claude API Integration
"""
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field

class Message(BaseModel):
    """Message in a conversation"""
    role: str
    content: str

class SystemPrompt(BaseModel):
    """System prompt for Claude API"""
    content: str

class QueryRequest(BaseModel):
    """Request to query Claude API"""
    prompt: str
    conversation_id: str = Field(default="default", description="Unique identifier for the conversation")
    system_prompt: Optional[str] = Field(default=None, description="Optional system prompt to guide Claude's behavior")
    model: str = Field(default="claude-3-sonnet-20240229", description="Claude model to use")
    temperature: float = Field(default=0.7, description="Temperature for response generation", ge=0.0, le=1.0)
    max_tokens: int = Field(default=4096, description="Maximum tokens to generate", ge=1, le=100000)

class ClaudeResponse(BaseModel):
    """Response from Claude API"""
    response: str
    conversation_id: str
    model: str
    usage: Dict[str, Any]
