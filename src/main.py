"""
Claude Desktop API Integration via MCP
Main entry point for the MCP server
"""
import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Import after environment variables are loaded
from .server import start_server

if __name__ == "__main__":
    try:
        logger.info("Starting Claude API MCP Server...")
        start_server()
    except Exception as e:
        logger.error(f"Error starting server: {str(e)}", exc_info=True)
