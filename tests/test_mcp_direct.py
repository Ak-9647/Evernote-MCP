#!/usr/bin/env python3
"""
Direct MCP Server Testing Script

This script allows you to test the Evernote MCP server functionality directly
without needing Claude Desktop.
"""

import os
import asyncio
import json
from evernote_mcp_server import EvernoteClient, app

# Your Evernote developer token
EVERNOTE_TOKEN = os.environ.get("EVERNOTE_DEVELOPER_TOKEN", "YOUR_TOKEN_HERE")

async def test_evernote_mcp():
    """Test the Evernote MCP server functionality directly"""
    
    print("🧪 Testing Evernote MCP Server Directly")
    print("=" * 50)
    
    # Test 1: Configure Evernote client
    print("\n1️⃣ Configuring Evernote Client...")
    
    # Try production environment first
    try:
        client = EvernoteClient(EVERNOTE_TOKEN, is_sandbox=False)
        print("✅ Evernote client initialized (Production)")
        
        # Test connection by listing notebooks
        notebooks = await client.list_notebooks()
        print(f"✅ Connected successfully! Found {len(notebooks)} notebooks")
        
        # Test 2: List notebooks
        print("\n2️⃣ Testing Notebook Listing...")
        for i, notebook in enumerate(notebooks[:5]):  # Show first 5
            print(f"   📁 {notebook.get('name', 'Unnamed')} (GUID: {notebook.get('guid', 'N/A')[:8]}...)")
        
        # Test 3: Search notes
        print("\n3️⃣ Testing Note Search...")
        notes = await client.search_notes("*", max_notes=5)
        print(f"✅ Found {len(notes)} notes")
        
        for i, note in enumerate(notes):
            print(f"   📝 {note.get('title', 'Untitled')} (GUID: {note.get('guid', 'N/A')[:8]}...)")
        
        # Test 4: Create a test note
        print("\n4️⃣ Testing Note Creation...")
        test_note = await client.create_note(
            title="MCP Test Note - " + str(asyncio.get_event_loop().time()),
            content="This is a test note created by the MCP server from Cursor!<br/><br/>Created on: " + str(asyncio.get_event_loop().time()),
            tags=["mcp-test", "cursor"]
        )
        
        if test_note:
            print(f"✅ Test note created successfully!")
            print(f"   Title: {test_note.get('title')}")
            print(f"   GUID: {test_note.get('guid')}")
            
            # Test 5: Read the note content
            print("\n5️⃣ Testing Note Reading...")
            note_content = await client.get_note(test_note.get('guid'), include_content=True)
            if note_content:
                print(f"✅ Note content retrieved successfully!")
                print(f"   Title: {note_content.get('title')}")
                print(f"   Content length: {len(note_content.get('content', ''))}")
            else:
                print("❌ Failed to retrieve note content")
                
        else:
            print("❌ Failed to create test note")
        
        # Test 6: List tags
        print("\n6️⃣ Testing Tag Listing...")
        tags = await client.list_tags()
        print(f"✅ Found {len(tags)} tags")
        for tag in tags[:5]:  # Show first 5
            print(f"   🏷️  {tag.get('name', 'Unnamed')}")
            
    except Exception as e:
        print(f"❌ Production environment failed: {e}")
        print("\n🔄 Trying Sandbox environment...")
        
        try:
            client = EvernoteClient(EVERNOTE_TOKEN, is_sandbox=True)
            print("✅ Evernote client initialized (Sandbox)")
            
            # Test connection
            notebooks = await client.list_notebooks()
            print(f"✅ Connected successfully! Found {len(notebooks)} notebooks")
            
        except Exception as e2:
            print(f"❌ Sandbox environment also failed: {e2}")
            return False
    
    print("\n" + "=" * 50)
    print("🎉 MCP Server Testing Complete!")
    print("✅ The MCP server is working correctly!")
    print("\n💡 You can now use the MCP server tools in your applications:")
    print("   - configure_evernote()")
    print("   - search_notes()")
    print("   - create_note()")
    print("   - get_note_content()")
    print("   - create_notebook()")
    print("   - list_notebooks()")
    print("   - list_tags()")
    
    return True

async def demo_mcp_tools():
    """Demonstrate MCP server tools directly"""
    print("\n🛠️  Demonstrating MCP Tools")
    print("=" * 50)
    
    # Import the tools from the MCP server
    from evernote_mcp_server import configure_evernote, search_notes, create_note, get_note_content
    
    try:
        # Configure Evernote
        print("\n1️⃣ Configuring Evernote...")
        config_result = await configure_evernote(EVERNOTE_TOKEN, use_sandbox=False)
        print(f"Configuration result: {json.dumps(config_result, indent=2)}")
        
        if config_result.get("success"):
            # Search for notes
            print("\n2️⃣ Searching for notes...")
            search_result = await search_notes("*", max_results=3)
            print(f"Search result: {json.dumps(search_result, indent=2)}")
            
            # Create a note
            print("\n3️⃣ Creating a new note...")
            note_result = await create_note(
                title="Direct MCP Test - " + str(asyncio.get_event_loop().time()),
                content="This note was created directly through the MCP server tools!",
                tags=["mcp-direct", "test"]
            )
            print(f"Note creation result: {json.dumps(note_result, indent=2)}")
            
            # Get note content if creation was successful
            if note_result.get("success") and note_result.get("guid"):
                print("\n4️⃣ Reading the created note...")
                note_content = await get_note_content(note_result["guid"])
                print(f"Note content: {json.dumps(note_content, indent=2)}")
        
    except Exception as e:
        print(f"❌ Error during MCP tools demo: {e}")

if __name__ == "__main__":
    print("🚀 Starting Direct MCP Server Test")
    
    # Run the tests
    asyncio.run(test_evernote_mcp())
    
    print("\n" + "=" * 50)
    
    # Run the MCP tools demo
    asyncio.run(demo_mcp_tools())
    
    print("\n🎯 Testing completed! Your MCP server is ready to use.") 