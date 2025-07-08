#!/usr/bin/env python3
"""
Working Evernote MCP Server

A Model Context Protocol server that provides AI agents with access to Evernote functionality.
This version uses the official Evernote Python SDK.
"""

import asyncio
import logging
import os
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec
from evernote.edam.type.ttypes import Note, Notebook
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("evernote-mcp-working")

# Initialize the MCP server
app = FastMCP("Evernote MCP Server Working", version="2.0.0")

# Global client instance
evernote_client = None

class WorkingEvernoteClient:
    """Working Evernote API client using official SDK"""
    
    def __init__(self, developer_token: str, sandbox: bool = False):
        self.developer_token = developer_token
        self.sandbox = sandbox
        self.client = EvernoteClient(token=developer_token, sandbox=sandbox)
        self.user_store = self.client.get_user_store()
        self.note_store = self.client.get_note_store()
        
    def test_connection(self) -> Dict[str, Any]:
        """Test the connection to Evernote API"""
        try:
            # Check API version
            version_ok = self.user_store.checkVersion(
                "Python EDAMTest",
                self.user_store.EDAM_VERSION_MAJOR,
                self.user_store.EDAM_VERSION_MINOR
            )
            
            if not version_ok:
                return {"success": False, "error": "API version not supported"}
            
            # Get user info
            user = self.user_store.getUser()
            
            return {
                "success": True,
                "user": {
                    "username": user.username,
                    "id": user.id,
                    "email": getattr(user, 'email', 'N/A'),
                    "name": getattr(user, 'name', 'N/A')
                },
                "sandbox": self.sandbox
            }
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return {"success": False, "error": str(e)}
    
    def list_notebooks(self) -> Dict[str, Any]:
        """List all notebooks"""
        try:
            notebooks = self.note_store.listNotebooks()
            notebook_list = []
            
            for notebook in notebooks:
                notebook_list.append({
                    "guid": notebook.guid,
                    "name": notebook.name,
                    "default": getattr(notebook, 'defaultNotebook', False),
                    "created": getattr(notebook, 'serviceCreated', None),
                    "updated": getattr(notebook, 'serviceUpdated', None)
                })
            
            return {"success": True, "notebooks": notebook_list}
        except Exception as e:
            logger.error(f"Failed to list notebooks: {e}")
            return {"success": False, "error": str(e), "notebooks": []}
    
    def search_notes(self, query: str = "", max_notes: int = 10) -> Dict[str, Any]:
        """Search for notes"""
        try:
            note_filter = NoteFilter()
            if query:
                note_filter.words = query
            
            spec = NotesMetadataResultSpec()
            spec.includeTitle = True
            spec.includeCreated = True
            spec.includeUpdated = True
            spec.includeNotebookGuid = True
            spec.includeTagGuids = True
            
            notes_metadata = self.note_store.findNotesMetadata(note_filter, 0, max_notes, spec)
            
            notes_list = []
            for note_metadata in notes_metadata.notes:
                notes_list.append({
                    "guid": note_metadata.guid,
                    "title": note_metadata.title,
                    "created": note_metadata.created,
                    "updated": note_metadata.updated,
                    "notebookGuid": note_metadata.notebookGuid,
                    "tagGuids": getattr(note_metadata, 'tagGuids', [])
                })
            
            return {
                "success": True,
                "notes": notes_list,
                "totalFound": notes_metadata.totalNotes
            }
        except Exception as e:
            logger.error(f"Note search failed: {e}")
            return {"success": False, "error": str(e), "notes": []}
    
    def create_note(self, title: str, content: str, notebook_guid: str = None, tags: List[str] = None) -> Dict[str, Any]:
        """Create a new note"""
        try:
            # Create ENML content
            enml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">
<en-note>{content}</en-note>"""
            
            # Create note object
            note = Note()
            note.title = title
            note.content = enml_content
            
            # Set notebook
            if notebook_guid:
                note.notebookGuid = notebook_guid
            
            # Set tags
            if tags:
                note.tagNames = tags
            
            # Create the note
            created_note = self.note_store.createNote(note)
            
            return {
                "success": True,
                "note": {
                    "guid": created_note.guid,
                    "title": created_note.title,
                    "created": created_note.created,
                    "updated": created_note.updated,
                    "notebookGuid": created_note.notebookGuid
                }
            }
        except Exception as e:
            logger.error(f"Note creation failed: {e}")
            return {"success": False, "error": str(e)}
    
    def get_note(self, note_guid: str) -> Dict[str, Any]:
        """Get a specific note by GUID"""
        try:
            note = self.note_store.getNote(note_guid, True, True, False, False)
            
            return {
                "success": True,
                "note": {
                    "guid": note.guid,
                    "title": note.title,
                    "content": note.content,
                    "created": note.created,
                    "updated": note.updated,
                    "notebookGuid": note.notebookGuid,
                    "tagGuids": getattr(note, 'tagGuids', [])
                }
            }
        except Exception as e:
            logger.error(f"Failed to get note {note_guid}: {e}")
            return {"success": False, "error": str(e)}

# MCP Server Tools
@app.tool()
async def configure_evernote_working(developer_token: str, use_sandbox: bool = False) -> Dict[str, Any]:
    """
    Configure the Evernote client with authentication credentials (Working Version).
    
    Args:
        developer_token: Your Evernote developer token
        use_sandbox: Whether to use sandbox environment (default: False - production)
    
    Returns:
        Configuration status
    """
    global evernote_client
    
    try:
        evernote_client = WorkingEvernoteClient(developer_token, sandbox=use_sandbox)
        
        # Test the connection
        test_result = evernote_client.test_connection()
        
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
async def list_notebooks_working() -> Dict[str, Any]:
    """
    List all notebooks in Evernote (Working Version).
    
    Returns:
        List of notebooks
    """
    if not evernote_client:
        return {"success": False, "error": "Evernote client not configured. Please use configure_evernote_working first."}
    
    try:
        result = evernote_client.list_notebooks()
        return result
    except Exception as e:
        logger.error(f"Error in list_notebooks_working: {e}")
        return {"success": False, "error": f"Failed to list notebooks: {str(e)}", "notebooks": []}

@app.tool()
async def search_notes_working(
    query: str = "",
    max_results: int = 10
) -> Dict[str, Any]:
    """
    Search for notes in Evernote (Working Version).
    
    Args:
        query: Search query (empty string for all notes)
        max_results: Maximum number of results to return
    
    Returns:
        Search results
    """
    if not evernote_client:
        return {"success": False, "error": "Evernote client not configured. Please use configure_evernote_working first."}
    
    try:
        result = evernote_client.search_notes(query, max_results)
        return result
    except Exception as e:
        logger.error(f"Error in search_notes_working: {e}")
        return {"success": False, "error": f"Search failed: {str(e)}", "notes": []}

@app.tool()
async def create_note_working(
    title: str,
    content: str,
    notebook_guid: Optional[str] = None,
    tags: Optional[List[str]] = None,
    dry_run: bool = False
) -> Dict[str, Any]:
    """
    Create a new note in Evernote (Working Version).
    
    Args:
        title: The title of the note
        content: The content of the note (HTML or plain text)
        notebook_guid: Optional GUID of the notebook to create the note in
        tags: Optional list of tags
        dry_run: If True, simulate the action without creating the note
    
    Returns:
        Note creation result
    """
    if not evernote_client:
        return {"success": False, "error": "Evernote client not configured. Please use configure_evernote_working first."}
    
    if dry_run:
        return {
            "success": True,
            "message": f"DRY RUN: Would create note titled '{title}' with content length {len(content)} characters and tags {tags}",
            "dry_run": True
        }
    
    try:
        result = evernote_client.create_note(title, content, notebook_guid, tags)
        return result
    except Exception as e:
        logger.error(f"Error in create_note_working: {e}")
        return {"success": False, "error": f"Failed to create note: {str(e)}"}

@app.tool()
async def get_note_working(note_guid: str) -> Dict[str, Any]:
    """
    Get a specific note by GUID (Working Version).
    
    Args:
        note_guid: The GUID of the note to retrieve
    
    Returns:
        Note details
    """
    if not evernote_client:
        return {"success": False, "error": "Evernote client not configured. Please use configure_evernote_working first."}
    
    try:
        result = evernote_client.get_note(note_guid)
        return result
    except Exception as e:
        logger.error(f"Error in get_note_working: {e}")
        return {"success": False, "error": f"Failed to get note: {str(e)}"}

@app.tool()
async def test_connection_working() -> Dict[str, Any]:
    """
    Test the connection to Evernote API (Working Version).
    
    Returns:
        Connection test result
    """
    if not evernote_client:
        return {"success": False, "error": "Evernote client not configured. Please use configure_evernote_working first."}
    
    try:
        result = evernote_client.test_connection()
        return result
    except Exception as e:
        logger.error(f"Error in test_connection_working: {e}")
        return {"success": False, "error": f"Connection test failed: {str(e)}"}

# Resources
@app.resource("evernote://status")
async def evernote_status() -> str:
    """Get the current Evernote connection status"""
    if not evernote_client:
        return "Not connected to Evernote"
    
    try:
        test_result = evernote_client.test_connection()
        if test_result["success"]:
            user = test_result.get("user", {})
            return f"Connected to Evernote ({'sandbox' if evernote_client.sandbox else 'production'}) as {user.get('username', 'Unknown')}"
        else:
            return f"Connection failed: {test_result['error']}"
    except Exception as e:
        return f"Status check failed: {str(e)}"

if __name__ == "__main__":
    logger.info("Starting Working Evernote MCP Server")
    logger.info("This version uses the official Evernote Python SDK")
    
    # Run the FastMCP server using stdio transport (for Claude Desktop integration)
    app.run(transport="stdio") 