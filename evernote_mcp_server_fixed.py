#!/usr/bin/env python3
"""
Evernote MCP Server (Fixed Version)

A Model Context Protocol server that provides AI agents with access to Evernote functionality.
This version includes fixes for API endpoint issues and improved error handling.
"""

import asyncio
import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional, Sequence
from urllib.parse import quote

import httpx
from mcp.server.fastmcp import FastMCP
from mcp.server.models import InitializationOptions
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    Content
)

# Developer Mode Flag
DEV_MODE = os.getenv("DEV_MODE", "false").lower() == "true"

# Configure logging
log_level = logging.DEBUG if DEV_MODE else logging.INFO
logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("evernote-mcp-fixed")

if DEV_MODE:
    logger.warning("🚀 Developer Mode is ENABLED. Verbose logging and dev tools are active.")

# Initialize the MCP server
app = FastMCP("Evernote MCP Server Fixed", version="1.2.0")

# Configuration
EVERNOTE_SANDBOX_HOST = "sandbox.evernote.com"
EVERNOTE_PRODUCTION_HOST = "www.evernote.com"

# Global client instance
evernote_client = None

class EvernoteClient:
    """Fixed Evernote API client for MCP integration"""
    
    def __init__(self, developer_token: str, is_sandbox: bool = True):
        self.developer_token = developer_token
        self.host = EVERNOTE_SANDBOX_HOST if is_sandbox else EVERNOTE_PRODUCTION_HOST
        self.base_url = f"https://{self.host}/edam"
        self.is_sandbox = is_sandbox
        
    async def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """Make authenticated request to Evernote API with improved error handling"""
        headers = {
            "Authorization": f"Bearer {self.developer_token}",
            "Content-Type": "application/json"
        }

        logger.debug(f"Making {method} request to {self.base_url}{endpoint}")
        if data:
            logger.debug(f"Request data: {json.dumps(data, indent=2)}")

        async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
            try:
                if method.upper() == "GET":
                    response = await client.get(f"{self.base_url}{endpoint}", headers=headers)
                elif method.upper() == "POST":
                    response = await client.post(f"{self.base_url}{endpoint}", headers=headers, json=data)
                elif method.upper() == "PUT":
                    response = await client.put(f"{self.base_url}{endpoint}", headers=headers, json=data)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")

                logger.debug(f"Response Status: {response.status_code}")
                logger.debug(f"Response Headers: {response.headers}")
                logger.debug(f"Response Body: {response.text[:500]}...")

                # Handle different response formats
                if response.status_code == 200:
                    try:
                        response_data = response.json()
                        return response_data
                    except Exception as e:
                        logger.error(f"Failed to parse JSON response: {e}")
                        return {"error": "Failed to parse response", "raw_response": response.text}
                else:
                    response.raise_for_status()
                    
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
                return {"error": f"HTTP {e.response.status_code}: {e.response.text}"}
            except Exception as e:
                logger.error(f"An unexpected error occurred during request: {e}")
                return {"error": f"Request failed: {str(e)}"}
    
    async def test_connection(self) -> Dict:
        """Test the connection to Evernote API"""
        try:
            # Try a simple request to test authentication
            result = await self._make_request("GET", "/user")
            if "error" in result:
                return {"success": False, "error": result["error"]}
            return {"success": True, "user": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def create_note_simple(self, title: str, content: str, tags: Optional[List[str]] = None) -> Dict:
        """Create a simple note with basic content"""
        try:
            # Convert content to ENML format
            enml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">
<en-note>{content}</en-note>"""
            
            note_data = {
                "title": title,
                "content": enml_content,
                "created": int(datetime.now().timestamp() * 1000),
                "updated": int(datetime.now().timestamp() * 1000)
            }
            
            if tags:
                note_data["tagNames"] = tags
            
            result = await self._make_request("POST", "/note", note_data)
            if "error" in result:
                return {"success": False, "error": result["error"]}
            
            return {"success": True, "note": result}
        except Exception as e:
            logger.error(f"Error creating note: {e}")
            return {"success": False, "error": str(e)}
    
    async def search_notes_simple(self, query: str = "*", max_notes: int = 10) -> Dict:
        """Simple note search with basic functionality"""
        try:
            # Use a simple approach for searching
            search_data = {
                "query": query,
                "maxNotes": max_notes
            }
            
            result = await self._make_request("POST", "/note/search", search_data)
            if "error" in result:
                return {"success": False, "error": result["error"], "notes": []}
            
            # Handle different response formats
            if isinstance(result, dict):
                notes = result.get("notes", [])
            elif isinstance(result, list):
                notes = result
            else:
                notes = []
            
            return {"success": True, "notes": notes}
        except Exception as e:
            logger.error(f"Error searching notes: {e}")
            return {"success": False, "error": str(e), "notes": []}
    
    async def list_notebooks_simple(self) -> Dict:
        """Simple notebook listing"""
        try:
            result = await self._make_request("GET", "/notebook")
            if "error" in result:
                return {"success": False, "error": result["error"], "notebooks": []}
            
            # Handle different response formats
            if isinstance(result, dict):
                notebooks = result.get("notebooks", [])
            elif isinstance(result, list):
                notebooks = result
            else:
                notebooks = []
            
            return {"success": True, "notebooks": notebooks}
        except Exception as e:
            logger.error(f"Error listing notebooks: {e}")
            return {"success": False, "error": str(e), "notebooks": []}

# MCP Server Tools
@app.tool()
async def configure_evernote_fixed(developer_token: str, use_sandbox: bool = True) -> Dict[str, Any]:
    """
    Configure the Evernote client with authentication credentials (Fixed Version).
    
    Args:
        developer_token: Your Evernote developer token
        use_sandbox: Whether to use sandbox environment (default: True)
    
    Returns:
        Configuration status
    """
    global evernote_client
    
    try:
        evernote_client = EvernoteClient(developer_token, is_sandbox=use_sandbox)
        
        # Test the connection
        test_result = await evernote_client.test_connection()
        
        if test_result["success"]:
            return {
                "success": True,
                "message": f"Evernote client configured successfully for {'sandbox' if use_sandbox else 'production'} environment",
                "environment": "sandbox" if use_sandbox else "production",
                "user": test_result.get("user", {})
            }
        else:
            evernote_client = None
            return {"success": False, "error": f"Failed to connect: {test_result['error']}"}
            
    except Exception as e:
        logger.error(f"Error configuring Evernote client: {e}")
        evernote_client = None
        return {"success": False, "error": f"Configuration failed: {str(e)}"}

@app.tool()
async def create_note_fixed(
    title: str,
    content: str,
    tags: Optional[List[str]] = None,
    dry_run: bool = False
) -> Dict[str, Any]:
    """
    Create a new note in Evernote (Fixed Version).
    
    Args:
        title: The title of the note
        content: The content of the note
        tags: Optional list of tags
        dry_run: If True, simulate the action without creating the note
    
    Returns:
        Note creation result
    """
    if not evernote_client:
        return {"success": False, "error": "Evernote client not configured. Please use configure_evernote_fixed first."}
    
    if dry_run:
        return {
            "success": True,
            "message": f"DRY RUN: Would create note titled '{title}' with tags {tags}",
            "dry_run": True
        }
    
    try:
        result = await evernote_client.create_note_simple(title, content, tags)
        return result
    except Exception as e:
        logger.error(f"Error in create_note_fixed: {e}")
        return {"success": False, "error": f"Failed to create note: {str(e)}"}

@app.tool()
async def search_notes_fixed(
    query: str = "*",
    max_results: int = 10
) -> Dict[str, Any]:
    """
    Search for notes in Evernote (Fixed Version).
    
    Args:
        query: Search query (default: "*" for all notes)
        max_results: Maximum number of results to return
    
    Returns:
        Search results
    """
    if not evernote_client:
        return {"success": False, "error": "Evernote client not configured. Please use configure_evernote_fixed first."}
    
    try:
        result = await evernote_client.search_notes_simple(query, max_results)
        return result
    except Exception as e:
        logger.error(f"Error in search_notes_fixed: {e}")
        return {"success": False, "error": f"Search failed: {str(e)}", "notes": []}

@app.tool()
async def list_notebooks_fixed() -> Dict[str, Any]:
    """
    List all notebooks in Evernote (Fixed Version).
    
    Returns:
        List of notebooks
    """
    if not evernote_client:
        return {"success": False, "error": "Evernote client not configured. Please use configure_evernote_fixed first."}
    
    try:
        result = await evernote_client.list_notebooks_simple()
        return result
    except Exception as e:
        logger.error(f"Error in list_notebooks_fixed: {e}")
        return {"success": False, "error": f"Failed to list notebooks: {str(e)}", "notebooks": []}

@app.tool()
async def test_connection_fixed() -> Dict[str, Any]:
    """
    Test the connection to Evernote API (Fixed Version).
    
    Returns:
        Connection test result
    """
    if not evernote_client:
        return {"success": False, "error": "Evernote client not configured. Please use configure_evernote_fixed first."}
    
    try:
        result = await evernote_client.test_connection()
        return result
    except Exception as e:
        logger.error(f"Error in test_connection_fixed: {e}")
        return {"success": False, "error": f"Connection test failed: {str(e)}"}

# Resources
@app.resource("status://connection")
async def connection_status() -> str:
    """Get the current connection status"""
    if not evernote_client:
        return "Not connected"
    
    test_result = await evernote_client.test_connection()
    if test_result["success"]:
        return f"Connected to {evernote_client.host}"
    else:
        return f"Connection failed: {test_result['error']}"

if __name__ == "__main__":
    logger.info("Starting Evernote MCP Server (Fixed Version)")
    logger.info("This version includes improved error handling and API endpoint fixes")
    
    if DEV_MODE:
        logger.info("🔧 Developer Mode is active - additional tools and verbose logging enabled")
    
    # Run the FastMCP server using stdio transport (for Claude Desktop integration)
    app.run(transport="stdio") 