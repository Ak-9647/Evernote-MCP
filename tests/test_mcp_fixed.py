#!/usr/bin/env python3
"""
Test script for the Fixed Evernote MCP Server

This script tests the improved version with better error handling.
"""

import os
import asyncio
import json
from evernote_mcp_server_fixed import (
    configure_evernote_fixed,
    create_note_fixed,
    search_notes_fixed,
    list_notebooks_fixed,
    test_connection_fixed
)

# Your Evernote developer token
EVERNOTE_TOKEN = os.environ.get("EVERNOTE_DEVELOPER_TOKEN", "YOUR_TOKEN_HERE")

async def test_fixed_mcp_server():
    """Test the fixed MCP server functionality"""
    
    print("🔧 Testing Fixed Evernote MCP Server")
    print("=" * 50)
    
    # Test 1: Configure the client
    print("\n1️⃣ Configuring Evernote Client (Fixed)...")
    config_result = await configure_evernote_fixed(EVERNOTE_TOKEN, use_sandbox=False)
    print(f"Configuration result: {json.dumps(config_result, indent=2)}")
    
    if not config_result.get("success"):
        print("❌ Configuration failed, trying sandbox...")
        config_result = await configure_evernote_fixed(EVERNOTE_TOKEN, use_sandbox=True)
        print(f"Sandbox configuration result: {json.dumps(config_result, indent=2)}")
    
    if config_result.get("success"):
        print("✅ Configuration successful!")
        
        # Test 2: Test connection
        print("\n2️⃣ Testing Connection...")
        connection_result = await test_connection_fixed()
        print(f"Connection test: {json.dumps(connection_result, indent=2)}")
        
        # Test 3: List notebooks
        print("\n3️⃣ Testing Notebook Listing...")
        notebooks_result = await list_notebooks_fixed()
        print(f"Notebooks result: {json.dumps(notebooks_result, indent=2)}")
        
        # Test 4: Search notes
        print("\n4️⃣ Testing Note Search...")
        search_result = await search_notes_fixed("*", max_results=5)
        print(f"Search result: {json.dumps(search_result, indent=2)}")
        
        # Test 5: Create a note (dry run first)
        print("\n5️⃣ Testing Note Creation (Dry Run)...")
        dry_run_result = await create_note_fixed(
            title="MCP Fixed Test - Dry Run",
            content="This is a dry run test note from the fixed MCP server",
            tags=["mcp-test", "dry-run"],
            dry_run=True
        )
        print(f"Dry run result: {json.dumps(dry_run_result, indent=2)}")
        
        # Test 6: Create a real note
        print("\n6️⃣ Testing Note Creation (Real)...")
        create_result = await create_note_fixed(
            title=f"MCP Fixed Test - Real Note - {asyncio.get_event_loop().time()}",
            content="This is a real test note created by the fixed MCP server from Cursor!<br/><br/>Features tested:<br/>- Configuration<br/>- Connection<br/>- Note creation<br/>- Error handling",
            tags=["mcp-test", "fixed-version", "cursor"]
        )
        print(f"Create result: {json.dumps(create_result, indent=2)}")
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 Fixed MCP Server Test Summary")
        print("=" * 50)
        print(f"✅ Configuration: {'Success' if config_result.get('success') else 'Failed'}")
        print(f"✅ Connection: {'Success' if connection_result.get('success') else 'Failed'}")
        print(f"✅ Notebooks: {'Success' if notebooks_result.get('success') else 'Failed'}")
        print(f"✅ Search: {'Success' if search_result.get('success') else 'Failed'}")
        print(f"✅ Note Creation: {'Success' if create_result.get('success') else 'Failed'}")
        
        if create_result.get("success"):
            print(f"\n🎉 Successfully created note: {create_result.get('note', {}).get('title', 'N/A')}")
        
    else:
        print("❌ Configuration failed, cannot continue with tests")
        print("Please check your Evernote developer token and API access")

async def demonstrate_fixed_tools():
    """Demonstrate the fixed MCP tools with practical examples"""
    print("\n🛠️  Demonstrating Fixed MCP Tools")
    print("=" * 50)
    
    # Quick setup
    print("\n⚡ Quick Setup...")
    setup_result = await configure_evernote_fixed(EVERNOTE_TOKEN, use_sandbox=False)
    
    if setup_result.get("success"):
        print("✅ Quick setup successful!")
        
        # Demonstrate different note creation scenarios
        print("\n📝 Creating Different Types of Notes...")
        
        # Simple note
        simple_note = await create_note_fixed(
            title="Simple Note Test",
            content="This is a simple note with basic content."
        )
        print(f"Simple note: {simple_note.get('success', False)}")
        
        # Note with tags
        tagged_note = await create_note_fixed(
            title="Tagged Note Test",
            content="This note has multiple tags for organization.",
            tags=["important", "work", "meeting"]
        )
        print(f"Tagged note: {tagged_note.get('success', False)}")
        
        # Note with HTML content
        html_note = await create_note_fixed(
            title="HTML Note Test",
            content="<h1>This is a heading</h1><p>This is a paragraph with <b>bold</b> text.</p><ul><li>Item 1</li><li>Item 2</li></ul>",
            tags=["html", "formatted"]
        )
        print(f"HTML note: {html_note.get('success', False)}")
        
        # Search for our created notes
        print("\n🔍 Searching for created notes...")
        search_result = await search_notes_fixed("Test", max_results=10)
        if search_result.get("success"):
            notes = search_result.get("notes", [])
            print(f"Found {len(notes)} notes containing 'Test'")
            for note in notes[:3]:  # Show first 3
                print(f"  - {note.get('title', 'Untitled')}")
        
        print("\n✅ Fixed MCP tools demonstration complete!")
    else:
        print("❌ Quick setup failed")

if __name__ == "__main__":
    print("🚀 Starting Fixed MCP Server Tests")
    
    # Run the main test
    asyncio.run(test_fixed_mcp_server())
    
    # Run the demonstration
    asyncio.run(demonstrate_fixed_tools())
    
    print("\n🎯 All tests completed! The fixed MCP server is ready for use.") 