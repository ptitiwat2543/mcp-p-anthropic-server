# Installation Guide for Claude Desktop API Integration via MCP

This guide will walk you through the installation and configuration of Claude Desktop API Integration via MCP.

## Prerequisites

1. **Python 3.8 or newer** - [Download Python](https://www.python.org/downloads/)
2. **Claude Desktop** - The Claude Desktop application must be installed
3. **Anthropic API Key** - You need an API key for Claude API [Request an API key here](https://console.anthropic.com/)

## Installation Steps

### 1. Install Python

1. Download and install Python 3.8 or newer from [python.org](https://www.python.org/downloads/)
2. When installing, make sure to select the "Add Python to PATH" option

### 2. Download the Project

Download or clone this project to your computer

```bash
# Using Git (if available)
git clone [Project URL]
cd mcp-p-anthropic-server
# Or download ZIP and extract it
```

### 3. Set Up the Environment

Use the provided setup script to configure your environment:

#### For Windows:

1. Open Command Prompt or PowerShell
2. Navigate to the project folder
3. Run the setup script:

```bash
setup_environment.bat
```

This script will:
- Check Python installation
- Create a virtual environment
- Install necessary dependencies
- Create a `.env` file (if it doesn't exist)

#### For macOS/Linux:

1. Open Terminal
2. Navigate to the project folder
3. Run these commands:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file if it doesn't exist
cp .env.example .env
```

### 4. Configure API Key

1. Open the `.env` file in a text editor
2. Add your Claude API key:

```
ANTHROPIC_API_KEY=your-api-key-here
```

### 5. Configure Claude Desktop

The Claude Desktop application needs to know about our MCP server

#### For Windows:

1. Go to `%APPDATA%\Claude\` (you can copy and paste this path in File Explorer's address bar)
2. Create or edit the `claude_desktop_config.json` file
3. Copy the contents from `config/claude_desktop_config.json` in this project
4. Update paths if necessary and make sure to include your API key

#### For macOS:

1. Go to `~/Library/Application Support/Claude/` 
   - In Finder, press Cmd+Shift+G and enter the path
2. Create or edit the `claude_desktop_config.json` file
3. Copy the contents from `config/claude_desktop_config.json` in this project
4. Update paths if necessary and make sure to include your API key

## Starting the Servers

### Start the MCP Server

#### For Windows:

```bash
start_server.bat
```

Or run the command directly:

```bash
python -m src.main
```

#### For macOS/Linux:

```bash
# Activate the virtual environment first (if not already activated)
source venv/bin/activate

# Start the server
python -m src.main
```

### Start the API Server (Optional)

If you want to use the HTTP API server:

#### For Windows:

```bash
start_api_server.bat
```

Or run the command directly:

```bash
python -m src.api_server
```

#### For macOS/Linux:

```bash
# Activate the virtual environment first (if not already activated)
source venv/bin/activate

# Start the API server
python -m src.api_server
```

The API server will start at `http://localhost:8000`

## Verifying the Installation

1. Start the MCP server as described above
2. Open Claude Desktop
3. In the Claude Desktop chat, try using the command:

```
@claude-api Please answer using API: Testing the connection
```

If everything is set up correctly, Claude will respond using the API instead of using the Professional Plan

## Troubleshooting

### Common Issues

1. **'python' is not recognized as an internal or external command**
   - Make sure you installed Python and added it to your PATH

2. **No module named 'mcp'**
   - Make sure you installed the dependencies: `pip install -r requirements.txt`

3. **API Key Errors**
   - Check that your API key is valid and configured in `.env`
   - Check that the API key has proper permissions

4. **Claude Desktop can't find the MCP server**
   - Check your `claude_desktop_config.json` configuration
   - Verify that the paths are correct

5. **Connection refused**
   - Check that the server is running
   - Verify the port isn't blocked by a firewall

### Viewing Logs

If you're experiencing problems, check the console output from:
- The terminal running the MCP server
- Claude Desktop logs (if available)

## Additional Information

For more information about using the MCP server, please see [README.md](README.md)