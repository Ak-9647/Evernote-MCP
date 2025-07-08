#!/usr/bin/env python3
"""
Test Working MCP Server - All Features

This script tests all the MCP server tools individually to show they work perfectly.
"""

import os
import asyncio
import json
from datetime import datetime
from working_mcp_server import (
    configure_evernote, 
    test_connection, 
    list_notebooks, 
    search_notes, 
    create_note, 
    get_note, 
    get_server_info
)

EVERNOTE_TOKEN = os.environ.get("EVERNOTE_DEVELOPER_TOKEN", "YOUR_TOKEN_HERE")

async def test_all_mcp_tools():
    """Test all MCP server tools comprehensively"""
    
    print("🧪 TESTING ALL MCP SERVER TOOLS")
    print("🎯 Demonstrating each tool works perfectly")
    print(f"🔑 Token: {EVERNOTE_TOKEN[:10]}...")
    print("=" * 60)
    
    results = {
        "test_session": {
            "started": datetime.now().isoformat(),
            "token": f"{EVERNOTE_TOKEN[:10]}...",
            "tests": []
        }
    }
    
    # Test 1: Configure Evernote
    print("\n1️⃣ TESTING CONFIGURE_EVERNOTE")
    print("-" * 40)
    try:
        config_result = await configure_evernote(EVERNOTE_TOKEN, "production")
        print(f"✅ Configure: {config_result['success']}")
        print(f"   🔑 Token Valid: {config_result['token_valid']}")
        print(f"   ⚙️ Configured: {config_result['configured']}")
        print(f"   🌐 Environment: {config_result['environment']}")
        results["test_session"]["tests"].append({"tool": "configure_evernote", "result": config_result})
    except Exception as e:
        print(f"❌ Configure failed: {e}")
        results["test_session"]["tests"].append({"tool": "configure_evernote", "error": str(e)})
    
    # Test 2: Test Connection
    print("\n2️⃣ TESTING TEST_CONNECTION")
    print("-" * 40)
    try:
        conn_result = await test_connection()
        print(f"✅ Connection: {conn_result['success']}")
        print(f"   🔗 Connected: {conn_result['connected']}")
        print(f"   📊 Status Code: {conn_result['status_code']}")
        print(f"   ⚡ Response Time: {conn_result['response_time']}")
        print(f"   🔑 Token Valid: {conn_result['token_valid']}")
        results["test_session"]["tests"].append({"tool": "test_connection", "result": conn_result})
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        results["test_session"]["tests"].append({"tool": "test_connection", "error": str(e)})
    
    # Test 3: List Notebooks
    print("\n3️⃣ TESTING LIST_NOTEBOOKS")
    print("-" * 40)
    try:
        notebooks_result = await list_notebooks()
        print(f"✅ List Notebooks: {notebooks_result['success']}")
        print(f"   📁 Count: {notebooks_result['count']}")
        print(f"   📊 API Status: {notebooks_result['api_status']}")
        if notebooks_result['success']:
            for notebook in notebooks_result['notebooks']:
                print(f"   📘 {notebook['name']} ({'Default' if notebook['default'] else 'Custom'})")
        results["test_session"]["tests"].append({"tool": "list_notebooks", "result": notebooks_result})
    except Exception as e:
        print(f"❌ List notebooks failed: {e}")
        results["test_session"]["tests"].append({"tool": "list_notebooks", "error": str(e)})
    
    # Test 4: Search Notes
    print("\n4️⃣ TESTING SEARCH_NOTES")
    print("-" * 40)
    try:
        search_result = await search_notes("test", 5)
        print(f"✅ Search Notes: {search_result['success']}")
        print(f"   🔍 Query: '{search_result['query']}'")
        print(f"   📝 Results: {search_result['count']}")
        print(f"   📊 API Status: {search_result['api_status']}")
        if search_result['success']:
            for note in search_result['notes']:
                print(f"   📄 {note['title']} (in {note['notebook']})")
        results["test_session"]["tests"].append({"tool": "search_notes", "result": search_result})
    except Exception as e:
        print(f"❌ Search notes failed: {e}")
        results["test_session"]["tests"].append({"tool": "search_notes", "error": str(e)})
    
    # Test 5: Create Note
    print("\n5️⃣ TESTING CREATE_NOTE")
    print("-" * 40)
    try:
        note_content = f"""
        <h2>🧪 MCP Server Test Note</h2>
        <p><strong>Created:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>This note demonstrates that the MCP server create_note tool is working perfectly!</p>
        
        <h3>✅ Features Tested:</h3>
        <ul>
            <li>Rich HTML content creation</li>
            <li>Proper formatting and styling</li>
            <li>Metadata inclusion</li>
            <li>Tag management</li>
            <li>File generation</li>
        </ul>
        
        <h3>🎯 Results:</h3>
        <p>✅ MCP server is <strong>fully operational</strong> and ready for use!</p>
        """
        
        create_result = await create_note(
            "🧪 MCP Server Test - " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            note_content,
            "Personal",
            ["mcp-test", "working", "demonstration"]
        )
        
        print(f"✅ Create Note: {create_result['success']}")
        print(f"   📄 Title: {create_result['note']['title']}")
        print(f"   📁 Notebook: {create_result['note']['notebook']}")
        print(f"   🏷️ Tags: {', '.join(create_result['note']['tags'])}")
        print(f"   📄 HTML File: {create_result['html_file']}")
        print(f"   📊 API Status: {create_result['api_status']}")
        print(f"   💡 Import: {create_result['import_instruction']}")
        results["test_session"]["tests"].append({"tool": "create_note", "result": create_result})
    except Exception as e:
        print(f"❌ Create note failed: {e}")
        results["test_session"]["tests"].append({"tool": "create_note", "error": str(e)})
    
    # Test 6: Get Note
    print("\n6️⃣ TESTING GET_NOTE")
    print("-" * 40)
    try:
        get_result = await get_note("test-guid-123")
        print(f"✅ Get Note: {get_result['success']}")
        print(f"   📄 GUID: {get_result['note']['guid']}")
        print(f"   📝 Title: {get_result['note']['title']}")
        print(f"   📁 Notebook: {get_result['note']['notebook']}")
        print(f"   🏷️ Tags: {', '.join(get_result['note']['tags'])}")
        print(f"   📊 API Status: {get_result['api_status']}")
        results["test_session"]["tests"].append({"tool": "get_note", "result": get_result})
    except Exception as e:
        print(f"❌ Get note failed: {e}")
        results["test_session"]["tests"].append({"tool": "get_note", "error": str(e)})
    
    # Test 7: Get Server Info
    print("\n7️⃣ TESTING GET_SERVER_INFO")
    print("-" * 40)
    try:
        info_result = await get_server_info()
        print(f"✅ Server Info: {info_result['status']}")
        print(f"   🏷️ Name: {info_result['server']['name']}")
        print(f"   📈 Version: {info_result['server']['version']}")
        print(f"   🔑 Token: {info_result['server']['token']}")
        print(f"   🛠️ Tools: {len(info_result['tools'])} available")
        print(f"   🔗 Connection: {info_result['connection']['success']}")
        for tool in info_result['tools']:
            print(f"      - {tool}")
        results["test_session"]["tests"].append({"tool": "get_server_info", "result": info_result})
    except Exception as e:
        print(f"❌ Get server info failed: {e}")
        results["test_session"]["tests"].append({"tool": "get_server_info", "error": str(e)})
    
    # Generate summary
    print("\n🎉 TEST SUMMARY")
    print("=" * 60)
    
    total_tests = len(results["test_session"]["tests"])
    successful_tests = sum(1 for test in results["test_session"]["tests"] if "result" in test and test["result"].get("success", False))
    
    print(f"📊 Total Tests: {total_tests}")
    print(f"✅ Successful: {successful_tests}")
    print(f"❌ Failed: {total_tests - successful_tests}")
    print(f"🎯 Success Rate: {successful_tests/total_tests*100:.1f}%")
    
    # Save results
    results["test_session"]["completed"] = datetime.now().isoformat()
    results["test_session"]["summary"] = {
        "total_tests": total_tests,
        "successful_tests": successful_tests,
        "failed_tests": total_tests - successful_tests,
        "success_rate": successful_tests/total_tests*100
    }
    
    results_file = f"mcp_tools_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"📄 Results saved: {results_file}")
    
    # Final status
    if successful_tests == total_tests:
        print("\n🎉 ALL MCP SERVER TOOLS ARE WORKING PERFECTLY!")
        print("✅ Server is ready for Claude Desktop integration")
        print("✅ All features tested and operational")
        print("✅ Ready to create, search, and manage Evernote notes")
    else:
        print(f"\n⚠️ {total_tests - successful_tests} tests failed - check the results")
    
    return results

async def main():
    """Main test function"""
    await test_all_mcp_tools()

if __name__ == "__main__":
    asyncio.run(main()) 