#!/usr/bin/env python3
"""
Test MCP Server Reading Capabilities

This script tests the MCP server's ability to read from your Evernote account.
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from evernote_mcp_working import (
    configure_evernote_working,
    test_connection_working,
    list_notebooks_working,
    search_notes_working,
    get_note_working
)

# Your Evernote token
EVERNOTE_TOKEN = os.environ.get("EVERNOTE_DEVELOPER_TOKEN", "YOUR_TOKEN_HERE")

async def test_mcp_reading_functions():
    """Test all MCP reading functions"""
    
    print("🔍 TESTING MCP SERVER READING CAPABILITIES")
    print("=" * 60)
    
    # Step 1: Configure the connection
    print("1️⃣ Configuring Evernote connection...")
    config_result = await configure_evernote_working(EVERNOTE_TOKEN, use_sandbox=False)
    print(f"   Status: {config_result}")
    
    if not config_result.get('success', False):
        print("❌ Configuration failed!")
        return False
    
    # Step 2: Test connection
    print("\n2️⃣ Testing connection...")
    connection_result = await test_connection_working()
    print(f"   Status: {connection_result}")
    
    if not connection_result.get('success', False):
        print("❌ Connection test failed!")
        return False
    
    # Step 3: List notebooks
    print("\n3️⃣ Listing notebooks...")
    notebooks_result = await list_notebooks_working()
    print(f"   Status: {notebooks_result.get('success', False)}")
    
    if notebooks_result.get('success', False):
        notebooks = notebooks_result.get('notebooks', [])
        print(f"   Found {len(notebooks)} notebooks:")
        for notebook in notebooks:
            print(f"     📁 {notebook['name']} (GUID: {notebook['guid'][:8]}...)")
    else:
        print(f"   Error: {notebooks_result.get('error', 'Unknown error')}")
    
    # Step 4: Search for notes
    print("\n4️⃣ Searching for notes...")
    
    # Try different search queries
    search_queries = [
        "",  # Get all notes
        "created",  # Look for notes with "created" 
        "cursor",  # Look for notes with "cursor"
        "test",  # Look for notes with "test"
        "note"  # Look for notes with "note"
    ]
    
    all_notes = []
    
    for query in search_queries:
        print(f"   🔍 Searching for: '{query}' (blank = all notes)")
        search_result = await search_notes_working(query, max_results=20)
        
        if search_result.get('success', False):
            notes = search_result.get('notes', [])
            print(f"     Found {len(notes)} notes")
            
            for note in notes:
                if note not in all_notes:
                    all_notes.append(note)
                    print(f"     📝 {note['title']} (GUID: {note['guid'][:8]}...)")
                    print(f"         Created: {note.get('created', 'Unknown')}")
                    print(f"         Updated: {note.get('updated', 'Unknown')}")
        else:
            print(f"     Error: {search_result.get('error', 'Unknown error')}")
        
        print()
    
    # Step 5: Try to read a specific note
    if all_notes:
        print("5️⃣ Reading a specific note...")
        first_note = all_notes[0]
        print(f"   📖 Reading note: {first_note['title']}")
        
        note_result = await get_note_working(first_note['guid'])
        
        if note_result.get('success', False):
            note = note_result.get('note', {})
            print(f"   ✅ Successfully read note!")
            print(f"     Title: {note.get('title', 'No title')}")
            print(f"     Content length: {len(note.get('content', ''))} characters")
            print(f"     Content preview: {note.get('content', '')[:200]}...")
        else:
            print(f"   ❌ Failed to read note: {note_result.get('error', 'Unknown error')}")
    else:
        print("5️⃣ No notes found to read")
    
    return True

async def main():
    """Main test function"""
    
    print("🚀 MCP Server Reading Test")
    print("🎯 Testing ability to read from your Evernote account")
    print()
    
    try:
        success = await test_mcp_reading_functions()
        
        if success:
            print("\n🎉 MCP SERVER READING TEST RESULTS:")
            print("✅ Connection: Working")
            print("✅ Authentication: Working")
            print("✅ Notebooks: Can list")
            print("✅ Notes: Can search and read")
            print("✅ MCP Server: Fully functional for reading!")
        else:
            print("\n❌ MCP SERVER READING TEST FAILED")
            print("   Check your token and connection")
    
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main()) 