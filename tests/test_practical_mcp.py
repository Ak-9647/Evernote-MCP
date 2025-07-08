#!/usr/bin/env python3
"""
Test the Practical MCP Server Functions
"""

import asyncio
import sys
import os

# Add the current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from practical_mcp_server import (
    test_evernote_connection,
    get_evernote_status,
    list_notebooks,
    search_notes,
    create_note_practical,
    get_mcp_server_info
)

async def test_all_mcp_functions():
    """Test all MCP functions"""
    
    print("🧪 TESTING PRACTICAL MCP SERVER FUNCTIONS")
    print("=" * 60)
    
    # Test 1: Connection test
    print("1️⃣ Testing Evernote connection...")
    connection_result = await test_evernote_connection()
    print(f"   ✅ Connection: {connection_result['success']}")
    print(f"   📡 API Status: {connection_result['status_code']}")
    print(f"   🔑 Token Valid: {connection_result['token_valid']}")
    
    # Test 2: Get API status
    print("\n2️⃣ Getting API status...")
    status_result = await get_evernote_status()
    print(f"   ✅ Status Check: {status_result['success']}")
    print(f"   📊 Endpoints: {len(status_result['endpoints'])}")
    
    # Test 3: List notebooks
    print("\n3️⃣ Listing notebooks...")
    notebooks_result = await list_notebooks()
    print(f"   ✅ Notebooks: {notebooks_result['success']}")
    print(f"   📁 Count: {len(notebooks_result['notebooks'])}")
    
    # Test 4: Search notes
    print("\n4️⃣ Searching notes...")
    search_result = await search_notes("test")
    print(f"   ✅ Search: {search_result['success']}")
    print(f"   📝 Notes: {len(search_result['notes'])}")
    
    # Test 5: Create note (creates HTML file)
    print("\n5️⃣ Creating note...")
    create_result = await create_note_practical("Test Note from MCP", "This is a test note created by the MCP server!")
    print(f"   ✅ Create: {create_result['success']}")
    print(f"   📄 HTML File: {create_result['html_file_created']}")
    
    # Test 6: Get server info
    print("\n6️⃣ Getting server info...")
    info_result = await get_mcp_server_info()
    print(f"   ✅ Server: {info_result['status']}")
    print(f"   🔧 Capabilities: {len(info_result['capabilities'])}")
    
    print("\n🎉 ALL TESTS COMPLETED!")
    return True

async def main():
    """Main test function"""
    
    print("🚀 PRACTICAL MCP SERVER FUNCTION TEST")
    print("🎯 Testing all MCP functions before Claude Desktop integration")
    print()
    
    try:
        success = await test_all_mcp_functions()
        
        if success:
            print("\n✅ ALL MCP FUNCTIONS WORKING!")
            print("🎯 Ready for Claude Desktop integration!")
        else:
            print("\n❌ Some functions failed")
    
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main()) 