#!/usr/bin/env python3
"""
Evernote MCP Server

A Model Context Protocol server that provides AI agents with access to Evernote functionality.
This server enables AI assistants like Claude to create, search, and manage Evernote notes.
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
logger = logging.getLogger("evernote-mcp")

if DEV_MODE:
    logger.warning("🚀 Developer Mode is ENABLED. Verbose logging and dev tools are active.")

# Initialize the MCP server
app = FastMCP("Evernote MCP Server", version="1.1.0")

# Configuration
EVERNOTE_SANDBOX_HOST = "sandbox.evernote.com"
EVERNOTE_PRODUCTION_HOST = "www.evernote.com"

class EvernoteClient:
    """Simplified Evernote API client for MCP integration"""
    
    def __init__(self, developer_token: str, is_sandbox: bool = True):
        self.developer_token = developer_token
        self.host = EVERNOTE_SANDBOX_HOST if is_sandbox else EVERNOTE_PRODUCTION_HOST
        self.base_url = f"https://{self.host}/edam"
        
    async def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """Make authenticated request to Evernote API"""
        headers = {
            "Authorization": f"Bearer {self.developer_token}",
            "Content-Type": "application/json"
        }

        logger.debug(f"Making {method} request to {self.base_url}{endpoint}")
        if data:
            logger.debug(f"Request data: {json.dumps(data, indent=2)}")

        async with httpx.AsyncClient() as client:
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
                logger.debug(f"Response Body: {response.text}")

                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
                raise
            except Exception as e:
                logger.error(f"An unexpected error occurred during request: {e}")
                raise
    
    async def search_notes(self, query: str, notebook_guid: Optional[str] = None, max_notes: int = 50) -> List[Dict]:
        """Search notes using Evernote's search syntax"""
        try:
            # Construct search filter
            search_filter = {
                "query": query,
                "ascending": False,
                "maxNotes": max_notes
            }
            
            if notebook_guid:
                search_filter["notebookGuid"] = notebook_guid
                
            result = await self._make_request("POST", "/note/search", search_filter)
            return result.get("notes", [])
        except Exception as e:
            logger.error(f"Error searching notes: {e}")
            return []
    
    async def get_note(self, note_guid: str, include_content: bool = True) -> Optional[Dict]:
        """Retrieve a specific note by GUID"""
        try:
            endpoint = f"/note/{note_guid}"
            if include_content:
                endpoint += "?includeContent=true"
            
            return await self._make_request("GET", endpoint)
        except Exception as e:
            logger.error(f"Error getting note {note_guid}: {e}")
            return None
    
    async def create_note(self, title: str, content: str, notebook_guid: Optional[str] = None, tags: Optional[List[str]] = None) -> Optional[Dict]:
        """Create a new note"""
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
            
            if notebook_guid:
                note_data["notebookGuid"] = notebook_guid
            
            if tags:
                note_data["tagNames"] = tags
            
            return await self._make_request("POST", "/note", note_data)
        except Exception as e:
            logger.error(f"Error creating note: {e}")
            return None
    
    async def update_note(self, note_guid: str, title: Optional[str] = None, content: Optional[str] = None, tags: Optional[List[str]] = None) -> Optional[Dict]:
        """Update an existing note"""
        try:
            # First get the current note
            current_note = await self.get_note(note_guid, include_content=True)
            if not current_note:
                return None
            
            # Prepare update data
            update_data = {
                "guid": note_guid,
                "updated": int(datetime.now().timestamp() * 1000)
            }
            
            if title:
                update_data["title"] = title
            
            if content:
                update_data["content"] = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">
<en-note>{content}</en-note>"""
            
            if tags:
                update_data["tagNames"] = tags
            
            return await self._make_request("PUT", f"/note/{note_guid}", update_data)
        except Exception as e:
            logger.error(f"Error updating note {note_guid}: {e}")
            return None
    
    async def list_notebooks(self) -> List[Dict]:
        """List all notebooks"""
        try:
            result = await self._make_request("GET", "/notebook")
            return result.get("notebooks", [])
        except Exception as e:
            logger.error(f"Error listing notebooks: {e}")
            return []
    
    async def create_notebook(self, name: str, default_notebook: bool = False) -> Optional[Dict]:
        """Create a new notebook"""
        try:
            notebook_data = {
                "name": name,
                "defaultNotebook": default_notebook
            }
            
            return await self._make_request("POST", "/notebook", notebook_data)
        except Exception as e:
            logger.error(f"Error creating notebook: {e}")
            return None
    
    async def list_tags(self) -> List[Dict]:
        """List all tags"""
        try:
            result = await self._make_request("GET", "/tag")
            return result.get("tags", [])
        except Exception as e:
            logger.error(f"Error listing tags: {e}")
            return []

# Global Evernote client (will be initialized with configuration)
evernote_client: Optional[EvernoteClient] = None

@app.resource("notebooks://list")
async def list_notebooks_resource() -> str:
    """Resource that provides access to user's notebooks"""
    if not evernote_client:
        return "Error: Evernote client not initialized. Please provide developer token."
    
    try:
        notebooks = await evernote_client.list_notebooks()
        return json.dumps({
            "notebooks": [
                {
                    "guid": nb.get("guid"),
                    "name": nb.get("name"),
                    "default": nb.get("defaultNotebook", False),
                    "created": nb.get("serviceCreated"),
                    "updated": nb.get("serviceUpdated")
                }
                for nb in notebooks
            ]
        }, indent=2)
    except Exception as e:
        return f"Error retrieving notebooks: {str(e)}"

@app.resource("tags://list")
async def list_tags_resource() -> str:
    """Resource that provides access to user's tags"""
    if not evernote_client:
        return "Error: Evernote client not initialized. Please provide developer token."
    
    try:
        tags = await evernote_client.list_tags()
        return json.dumps({
            "tags": [
                {
                    "guid": tag.get("guid"),
                    "name": tag.get("name"),
                    "parentGuid": tag.get("parentGuid")
                }
                for tag in tags
            ]
        }, indent=2)
    except Exception as e:
        return f"Error retrieving tags: {str(e)}"

@app.resource("recent-notes://list")
async def recent_notes_resource() -> str:
    """Resource that provides access to recent notes"""
    if not evernote_client:
        return "Error: Evernote client not initialized. Please provide developer token."
    
    try:
        # Search for recent notes (last 30 days)
        recent_notes = await evernote_client.search_notes("", max_notes=20)
        return json.dumps({
            "recent_notes": [
                {
                    "guid": note.get("guid"),
                    "title": note.get("title"),
                    "created": note.get("created"),
                    "updated": note.get("updated"),
                    "notebookGuid": note.get("notebookGuid")
                }
                for note in recent_notes
            ]
        }, indent=2)
    except Exception as e:
        return f"Error retrieving recent notes: {str(e)}"

@app.tool()
async def search_notes(
    query: str,
    notebook_name: Optional[str] = None,
    max_results: int = 10
) -> List[Dict[str, Any]]:
    """
    Search for notes in Evernote using query string.
    
    Args:
        query: Search query (supports Evernote search syntax)
        notebook_name: Optional notebook name to search within
        max_results: Maximum number of results to return (default: 10)
    
    Returns:
        List of matching notes with metadata
    """
    if not evernote_client:
        return [{"error": "Evernote client not initialized. Please provide developer token."}]
    
    try:
        # If notebook_name is provided, get its GUID
        notebook_guid = None
        if notebook_name:
            notebooks = await evernote_client.list_notebooks()
            for nb in notebooks:
                if nb.get("name", "").lower() == notebook_name.lower():
                    notebook_guid = nb.get("guid")
                    break
        
        notes = await evernote_client.search_notes(query, notebook_guid, max_results)
        
        results = []
        for note in notes:
            results.append({
                "guid": note.get("guid"),
                "title": note.get("title"),
                "created": datetime.fromtimestamp(note.get("created", 0) / 1000).isoformat() if note.get("created") else None,
                "updated": datetime.fromtimestamp(note.get("updated", 0) / 1000).isoformat() if note.get("updated") else None,
                "notebook_guid": note.get("notebookGuid"),
                "tag_names": note.get("tagNames", []),
                "content_length": note.get("contentLength", 0)
            })
        
        return results
    except Exception as e:
        logger.error(f"Error in search_notes: {e}")
        return [{"error": f"Failed to search notes: {str(e)}"}]

@app.tool()
async def get_note_content(note_guid: str) -> Dict[str, Any]:
    """
    Retrieve the full content of a specific note.
    
    Args:
        note_guid: The GUID of the note to retrieve
    
    Returns:
        Note content and metadata
    """
    if not evernote_client:
        return {"error": "Evernote client not initialized. Please provide developer token."}
    
    try:
        note = await evernote_client.get_note(note_guid, include_content=True)
        if not note:
            return {"error": f"Note with GUID {note_guid} not found"}
        
        # Extract plain text content from ENML
        content = note.get("content", "")
        # Simple ENML to text conversion (remove XML tags)
        import re
        plain_text = re.sub(r'<[^>]+>', '', content)
        plain_text = plain_text.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
        
        return {
            "guid": note.get("guid"),
            "title": note.get("title"),
            "content": plain_text.strip(),
            "content_length": note.get("contentLength", 0),
            "created": datetime.fromtimestamp(note.get("created", 0) / 1000).isoformat() if note.get("created") else None,
            "updated": datetime.fromtimestamp(note.get("updated", 0) / 1000).isoformat() if note.get("updated") else None,
            "notebook_guid": note.get("notebookGuid"),
            "tag_names": note.get("tagNames", []),
            "source_url": note.get("attributes", {}).get("sourceURL") if note.get("attributes") else None
        }
    except Exception as e:
        logger.error(f"Error in get_note_content: {e}")
        return {"error": f"Failed to get note content: {str(e)}"}

@app.tool()
async def create_note(
    title: str,
    content: str,
    notebook_name: Optional[str] = None,
    tags: Optional[List[str]] = None,
    dry_run: bool = False
) -> Dict[str, Any]:
    """
    Create a new note in Evernote.
    
    Args:
        title: The title of the new note
        content: The content of the note (plain text or HTML)
        notebook_name: Optional notebook name (uses default if not specified)
        tags: Optional list of tag names
        dry_run: If True, the operation is a dry run and no changes are made
    
    Returns:
        Created note information
    """
    if not evernote_client:
        return {"error": "Evernote client not initialized. Please provide developer token."}
    
    if DEV_MODE and dry_run:
        logger.info(f"DRY RUN: Would create note titled '{title}' in notebook '{notebook_name or 'default'}' with tags {tags}")
        return {"status": "success (dry run)", "action": "create_note", "details": "Note was not actually created."}

    try:
        # If notebook_name is provided, get its GUID
        notebook_guid = None
        if notebook_name:
            notebooks = await evernote_client.list_notebooks()
            for nb in notebooks:
                if nb.get("name", "").lower() == notebook_name.lower():
                    notebook_guid = nb.get("guid")
                    break
            
            if not notebook_guid:
                return {"error": f"Notebook '{notebook_name}' not found"}
        
        note = await evernote_client.create_note(title, content, notebook_guid, tags)
        if not note:
            return {"error": "Failed to create note"}
        
        return {
            "guid": note.get("guid"),
            "title": note.get("title"),
            "created": datetime.fromtimestamp(note.get("created", 0) / 1000).isoformat() if note.get("created") else None,
            "notebook_guid": note.get("notebookGuid"),
            "tag_names": note.get("tagNames", []),
            "success": True,
            "message": f"Note '{title}' created successfully"
        }
    except Exception as e:
        logger.error(f"Error in create_note: {e}")
        return {"error": f"Failed to create note: {str(e)}"}

@app.tool()
async def update_note(
    note_guid: str,
    title: Optional[str] = None,
    content: Optional[str] = None,
    tags: Optional[List[str]] = None,
    dry_run: bool = False
) -> Dict[str, Any]:
    """
    Update an existing note in Evernote.
    
    Args:
        note_guid: The GUID of the note to update
        title: New title (optional)
        content: New content (optional)
        tags: New list of tags (optional)
        dry_run: If True, the operation is a dry run and no changes are made
    
    Returns:
        Updated note information
    """
    if not evernote_client:
        return {"status": "error", "message": "Evernote client not initialized. Please use configure_evernote first."}

    if DEV_MODE and dry_run:
        logger.info(f"DRY RUN: Would update note with GUID {note_guid} with title='{title}', content='...', tags={tags}")
        return {"status": "success (dry run)", "action": "update_note", "details": "Note was not actually updated."}

    try:
        updated_note = await evernote_client.update_note(note_guid, title, content, tags)
        if not updated_note:
            return {"error": f"Failed to update note with GUID {note_guid}"}
        
        return {
            "guid": updated_note.get("guid"),
            "title": updated_note.get("title"),
            "updated": datetime.fromtimestamp(updated_note.get("updated", 0) / 1000).isoformat() if updated_note.get("updated") else None,
            "tag_names": updated_note.get("tagNames", []),
            "success": True,
            "message": f"Note updated successfully"
        }
    except Exception as e:
        logger.error(f"Error in update_note: {e}")
        return {"error": f"Failed to update note: {str(e)}"}

@app.tool()
async def create_notebook(name: str, default: bool = False) -> Dict[str, Any]:
    """
    Create a new notebook in Evernote.
    
    Args:
        name: The name of the new notebook
        default: Whether this should be the default notebook
    
    Returns:
        Created notebook information
    """
    if not evernote_client:
        return {"error": "Evernote client not initialized. Please provide developer token."}
    
    try:
        notebook = await evernote_client.create_notebook(name, default)
        if not notebook:
            return {"error": "Failed to create notebook"}
        
        return {
            "guid": notebook.get("guid"),
            "name": notebook.get("name"),
            "default": notebook.get("defaultNotebook", False),
            "success": True,
            "message": f"Notebook '{name}' created successfully"
        }
    except Exception as e:
        logger.error(f"Error in create_notebook: {e}")
        return {"error": f"Failed to create notebook: {str(e)}"}

@app.tool()
async def configure_evernote(developer_token: str, use_sandbox: bool = True) -> Dict[str, Any]:
    """
    Configure the Evernote client with authentication credentials.
    
    Args:
        developer_token: Your Evernote developer token
        use_sandbox: Whether to use sandbox environment (default: True)
    
    Returns:
        Configuration status
    """
    global evernote_client
    
    try:
        evernote_client = EvernoteClient(developer_token, is_sandbox=use_sandbox)
        
        # Test the connection by trying to list notebooks
        notebooks = await evernote_client.list_notebooks()
        
        return {
            "success": True,
            "message": f"Evernote client configured successfully. Found {len(notebooks)} notebooks.",
            "environment": "sandbox" if use_sandbox else "production",
            "notebook_count": len(notebooks)
        }
    except Exception as e:
        logger.error(f"Error configuring Evernote client: {e}")
        evernote_client = None
        return {"error": f"Failed to configure Evernote client: {str(e)}"}

# --- Developer Tools (only enabled in DEV_MODE) ---
if DEV_MODE:
    @app.tool()
    async def dev_get_config() -> Dict[str, Any]:
        """[DEV] Returns the current server configuration and connection status."""
        if not evernote_client:
            return {"status": "error", "message": "Evernote client not initialized."}
        
        config_data = {
            "status": "success",
            "developer_mode": True,
            "host": evernote_client.host,
            "is_sandbox": evernote_client.host == EVERNOTE_SANDBOX_HOST,
            "token_loaded": bool(evernote_client.developer_token),
        }
        if evernote_client.developer_token:
            config_data["token_preview"] = f"{evernote_client.developer_token[:4]}...{evernote_client.developer_token[-4:]}"
        
        return config_data

    @app.tool()
    async def dev_clear_config() -> Dict[str, Any]:
        """[DEV] Clears the current Evernote configuration, forcing re-authentication."""
        global evernote_client
        evernote_client = None
        logger.info("Developer action: Evernote configuration cleared.")
        return {"status": "success", "message": "Configuration cleared."}

    @app.tool()
    async def dev_api_test() -> Dict[str, Any]:
        """[DEV] Performs a live API test to check connectivity and permissions."""
        if not evernote_client:
            return {"status": "error", "message": "Evernote client not initialized. Use configure_evernote first."}
        try:
            # A simple, read-only call to test authentication
            user_info = await evernote_client._make_request("GET", "/user")
            return {
                "status": "success",
                "message": "API connection successful.",
                "user": {
                    "username": user_info.get("username"),
                    "id": user_info.get("id"),
                    "name": user_info.get("name"),
                }
            }
        except Exception as e:
            return {"status": "error", "message": f"API test failed: {str(e)}"}

if __name__ == "__main__":
    logger.info("Starting Evernote MCP Server")
    logger.info("Remember to configure your Evernote developer token using the configure_evernote tool")
    
    if DEV_MODE:
        logger.info("🔧 Developer Mode is active - additional tools and verbose logging enabled")
    
    # Run the FastMCP server using stdio transport (for Claude Desktop integration)
    app.run(transport="stdio") 