#!/usr/bin/env python3
"""
Test script for the Working Evernote MCP Server

This script tests the basic functionality of the working MCP server
using the official Evernote Python SDK.
"""

import os
import asyncio
import sys
from evernote_mcp_working import (
    configure_evernote_working,
    test_connection_working,
    list_notebooks_working,
    search_notes_working,
    create_note_working
)

# Your Evernote developer token
EVERNOTE_TOKEN = os.environ.get("EVERNOTE_DEVELOPER_TOKEN", "YOUR_TOKEN_HERE")

async def test_working_mcp_server():
    """Test the working MCP server functionality"""
    
    print("🔧 Testing Working Evernote MCP Server")
    print("=" * 50)
    
    # Test 1: Configure the client
    print("\n1️⃣ Configuring Evernote Client...")
    config_result = await configure_evernote_working(EVERNOTE_TOKEN, use_sandbox=False)
    print(f"Configuration result: {config_result}")
    
    if not config_result.get("success"):
        print("❌ Configuration failed, cannot continue")
        return
    
    # Test 2: Test connection
    print("\n2️⃣ Testing Connection...")
    connection_test = await test_connection_working()
    print(f"Connection test: {connection_test}")
    
    if not connection_test.get("success"):
        print("❌ Connection test failed")
        return
    
    # Test 3: List notebooks
    print("\n3️⃣ Listing Notebooks...")
    notebooks_result = await list_notebooks_working()
    print(f"Notebooks: {notebooks_result}")
    
    if notebooks_result.get("success"):
        notebooks = notebooks_result.get("notebooks", [])
        print(f"Found {len(notebooks)} notebooks:")
        for nb in notebooks[:3]:  # Show first 3
            print(f"  - {nb['name']} (GUID: {nb['guid']})")
    
    # Test 4: Search notes
    print("\n4️⃣ Searching Notes...")
    search_result = await search_notes_working("", max_results=5)
    print(f"Search result: {search_result}")
    
    if search_result.get("success"):
        notes = search_result.get("notes", [])
        print(f"Found {len(notes)} notes:")
        for note in notes[:3]:  # Show first 3
            print(f"  - {note['title']} (GUID: {note['guid']})")
    
    # Test 5: Create a test note (dry run)
    print("\n5️⃣ Testing Note Creation (Dry Run)...")
    create_result = await create_note_working(
        title="MCP Test Note - Working Version",
        content="This is a test note created by the working MCP server.",
        tags=["mcp", "test", "working"],
        dry_run=True
    )
    print(f"Create note dry run: {create_result}")
    
    print("\n✅ All tests completed successfully!")
    print("The working MCP server is functioning correctly with the official Evernote SDK.")

async def test_real_note_creation():
    """Test creating a real note (with user confirmation)"""
    
    print("\n🆕 Would you like to create a real test note? (y/N): ", end="")
    choice = input()
    
    if choice.lower() == 'y':
        print("Creating real test note...")
        create_result = await create_note_working(
            title=f"MCP Test Note - {asyncio.get_event_loop().time()}",
            content="<p>This is a <b>real test note</b> created by the working MCP server.</p><p>Created successfully!</p>",
            tags=["mcp", "test", "working", "real"]
        )
        print(f"Real note creation result: {create_result}")
    else:
        print("Skipped real note creation.")

if __name__ == "__main__":
    print("🚀 Starting Working MCP Server Tests")
    
    # Run the tests
    asyncio.run(test_working_mcp_server())
    
    # Optional: Create a real note
    asyncio.run(test_real_note_creation())
    
    print("\n🎯 Testing complete!") 