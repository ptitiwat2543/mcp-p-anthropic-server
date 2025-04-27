# Claude Desktop API Integration via MCP

This project develops a Machine Communication Protocol (MCP) Server to enable seamless integration between Claude Desktop and Claude API, allowing users to access advanced features such as system prompts and conversation management.

## Credits

This project is based on [Claude_Desktop_API_USE_VIA_MCP](https://github.com/mlobo2012/Claude_Desktop_API_USE_VIA_MCP) by [mlobo2012](https://github.com/mlobo2012). Special thanks to the original author for developing this integration approach.

## Key Features

- Direct connection to Claude API through MCP
- Conversation history tracking and management
- System prompt support
- Seamless switching between Professional Plan and API usage
- Easy configuration with Claude Desktop
- Support for latest Claude models (Claude 3 Opus, Sonnet, Haiku)
- Support for Claude 3.5 Sonnet
- FastAPI service for external access

## When to Use

### Professional Plan (Default)
- Regular conversations in Claude Desktop
- Basic usage within plan limitations
- No special configuration required

### API Token (Through this MCP server)
- When you need a longer context window
- When you want to use system prompts
- When you need to bypass rate limits
- When you need advanced conversation management

## Installation Steps

### 1. Clone the Repository

```bash
# Using VS Code
# 1. Press Cmd + Shift + P (macOS) or Ctrl + Shift + P (Windows)
# 2. Type "Git: Clone"
# 3. Paste: [Your URL]

# Or using terminal
git clone [Your URL]
cd mcp-p-anthropic-server
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy environment template
cp .env.example .env
# Edit .env and add your API key
# ANTHROPIC_API_KEY=your_api_key_here
```

### 4. Configure Claude Desktop

#### macOS
Go to `~/Library/Application Support/Claude/`
```bash
# Using Finder
# 1. Press Cmd + Shift + G
# 2. Enter: ~/Library/Application Support/Claude/
```

#### Windows
Go to `%APPDATA%\Claude\`

1. Create or edit `claude_desktop_config.json`
2. Copy content from `config/claude_desktop_config.json`
3. Update paths and API key

## Usage Guide

### Basic Usage

#### Normal Claude Desktop Usage
- Just chat with Claude normally
- Uses your Professional plan
- No special commands needed

#### API Usage
```
@claude-api Please answer using API: What is the capital of France?
```

### Advanced Features

#### Using System Prompts
```
@claude-api {"system_prompt": "You are an expert fitness coach"} Create a workout plan
```

#### Conversation Management
```
# Start a new conversation
@claude-api {"conversation_id": "project1"} Let's talk about Python

# Continue existing conversation
@claude-api {"conversation_id": "project1"} Tell me more

# View conversation history
@claude-api get_conversation_history project1

# Clear conversation
@claude-api clear_conversation project1
```

#### View Available Models
```
@claude-api list_available_models
```

## Cost Management

- API calls will use your Anthropic API credits and may incur charges
- Use Professional plan for general inquiries
- Use `@claude-api` only when you need:
  - Longer context window
  - Custom system prompts
  - Bypass rate limits

## Available MCP Tools

### Claude API Tools

This system includes 5 tools for working with the Claude API that you can invoke via Claude Desktop chat with the `@claude-api` command followed by the tool name and required parameters:

#### 1. query_claude
Allows you to send a query directly to the Claude API with advanced options

```
@claude-api query_claude prompt="Your question" [conversation_id="desired_id"] [system_prompt="Your system prompt"] [model="model_name"] [temperature=0.7] [max_tokens=4096]
```

Parameters:
- `prompt`: The question or request to send (required)
- `conversation_id`: Conversation ID to track the conversation (default: "default")
- `system_prompt`: Optional system prompt to guide Claude's behavior (optional)
- `model`: Claude model to use (default: "claude-3-sonnet-20240229")
- `temperature`: Creativity level of the response (0.0-1.0, default: 0.7)
- `max_tokens`: Maximum tokens to generate (default: 4096)

#### 2. clear_conversation
Clears the specified conversation history

```
@claude-api clear_conversation [conversation_id="default"]
```

Parameters:
- `conversation_id`: Conversation ID to clear (default: "default")

#### 3. get_conversation_history
Retrieves conversation history for the specified ID

```
@claude-api get_conversation_history [conversation_id="default"]
```

Parameters:
- `conversation_id`: Conversation ID to view history (default: "default")

#### 4. list_conversations
Lists all available conversation IDs

```
@claude-api list_conversations
```

No additional parameters required

#### 5. list_available_models
Lists all available Claude models

```
@claude-api list_available_models
```

No additional parameters required

### Advanced Usage Examples

#### Using Custom Model with System Prompt
```
@claude-api query_claude prompt="Analyze this data and provide recommendations" model="claude-3-opus-20240229" system_prompt="You are an expert data analyst, focused on providing concise and actionable insights"
```

#### Tracking Complex Conversation
```
@claude-api query_claude prompt="Start planning a project" conversation_id="project_planning" system_prompt="You are an experienced project manager specializing in software development planning"

@claude-api query_claude prompt="What are the main risks to watch out for?" conversation_id="project_planning"

@claude-api query_claude prompt="Create an initial timeline" conversation_id="project_planning"
```

- `query_claude`: Creates direct API calls to Claude
  - Supports system prompts
  - Conversation tracking

- `clear_conversation`: Resets conversation history
  - Manage multiple conversation threads

- `get_conversation_history`: Retrieves conversation logs
  - Debug conversation flow

- `list_conversations`: Shows all existing conversations

- `list_available_models`: Shows all available Claude models

## Development

The main server imports are in `src/server.py` and the API server is in `src/api_server.py`

To extend functionality, you can add new tools using the `@mcp.tool()` decorator

Example of adding a new tool:

```python
@mcp.tool()
async def custom_tool(param: str) -> str:
    """
    Description of custom tool
    
    Args:
        param: Parameter description
    """
    try:
        # Tool implementation
        return result
    except Exception as e:
        return f"Error: {str(e)}"
```

## Troubleshooting

### API Key Issues
- Check your API key in `.env`
- Check Claude Desktop configuration paths
- Ensure API key has proper permissions

### Connection Issues
- Check if MCP server is running
- Check Python environment
- Check Claude Desktop logs

### Usage Issues
- Check `@claude-api` syntax is correct
- Check conversation IDs
- Check system prompt format

## Support

For issues and questions:
- Open a new issue in the repository
- Check existing discussions
- Review troubleshooting guide