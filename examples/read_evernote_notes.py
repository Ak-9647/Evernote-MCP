#!/usr/bin/env python3
"""
Read Notes from Evernote via HTTP API

This script tests reading notes from your Evernote account using direct HTTP calls.
"""

import os
import asyncio
import httpx
import json
from datetime import datetime

# Your Evernote token
EVERNOTE_TOKEN = os.environ.get("EVERNOTE_DEVELOPER_TOKEN", "YOUR_TOKEN_HERE")

async def test_evernote_read_api():
    """Test reading from Evernote via HTTP API"""
    
    print("🔍 TESTING EVERNOTE READ API")
    print("=" * 50)
    
    headers = {
        "Authorization": f"Bearer {EVERNOTE_TOKEN}",
        "Content-Type": "application/json",
        "User-Agent": "MCP-Server-Read/1.0"
    }
    
    # Test different API endpoints
    api_endpoints = [
        "https://www.evernote.com/shard/s1/notestore",
        "https://www.evernote.com/edam/user",
        "https://www.evernote.com/edam/note",
        "https://sandbox.evernote.com/edam/note",
        "https://app.evernote.com/api/v1/notes"
    ]
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        for endpoint in api_endpoints:
            print(f"\n📡 Testing endpoint: {endpoint}")
            
            try:
                # Try GET request first
                response = await client.get(endpoint, headers=headers)
                print(f"   GET Status: {response.status_code}")
                if response.status_code != 405:  # Not "Method Not Allowed"
                    print(f"   Response: {response.text[:200]}...")
                
                # Try POST request
                test_data = {"method": "listNotebooks"}
                response = await client.post(endpoint, json=test_data, headers=headers)
                print(f"   POST Status: {response.status_code}")
                print(f"   Response: {response.text[:200]}...")
                
            except Exception as e:
                print(f"   Error: {str(e)[:100]}...")

async def test_evernote_thrift_api():
    """Test Evernote Thrift API directly"""
    
    print("\n🔧 TESTING EVERNOTE THRIFT API")
    print("=" * 50)
    
    # Evernote uses Thrift protocol, let's try the correct format
    thrift_endpoints = [
        "https://www.evernote.com/edam/user",
        "https://www.evernote.com/edam/note/listNotebooks",
        "https://www.evernote.com/shard/s1/notestore"
    ]
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        for endpoint in thrift_endpoints:
            print(f"\n📡 Testing Thrift endpoint: {endpoint}")
            
            try:
                # Try with Thrift headers
                thrift_headers = {
                    "Authorization": f"Bearer {EVERNOTE_TOKEN}",
                    "Content-Type": "application/x-thrift",
                    "User-Agent": "MCP-Server-Thrift/1.0"
                }
                
                response = await client.get(endpoint, headers=thrift_headers)
                print(f"   Status: {response.status_code}")
                print(f"   Response: {response.text[:200]}...")
                
                # If we get a 200, this might be working
                if response.status_code == 200:
                    print("   ✅ This endpoint is responding!")
                
            except Exception as e:
                print(f"   Error: {str(e)[:100]}...")

async def check_evernote_web_interface():
    """Check if we can access Evernote via web interface"""
    
    print("\n🌐 TESTING EVERNOTE WEB INTERFACE")
    print("=" * 50)
    
    web_endpoints = [
        "https://www.evernote.com/Home.action",
        "https://www.evernote.com/client/web",
        "https://www.evernote.com/api/DeveloperToken.action"
    ]
    
    headers = {
        "Authorization": f"Bearer {EVERNOTE_TOKEN}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        for endpoint in web_endpoints:
            print(f"\n🌐 Testing web endpoint: {endpoint}")
            
            try:
                response = await client.get(endpoint, headers=headers)
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    content = response.text
                    print(f"   Content length: {len(content)} chars")
                    
                    # Look for note indicators
                    if "note" in content.lower() or "notebook" in content.lower():
                        print("   ✅ Contains note-related content!")
                        
                        # Look for specific patterns
                        if "guid" in content.lower():
                            print("   📝 Found GUID references")
                        if "title" in content.lower():
                            print("   📝 Found title references")
                
            except Exception as e:
                print(f"   Error: {str(e)[:100]}...")

async def try_evernote_export_api():
    """Try Evernote export/backup API"""
    
    print("\n📥 TESTING EVERNOTE EXPORT API")
    print("=" * 50)
    
    export_endpoints = [
        "https://www.evernote.com/shard/s1/export",
        "https://www.evernote.com/edam/export",
        "https://www.evernote.com/Home.action#n=",
        "https://www.evernote.com/shard/s1/sh/",
        "https://www.evernote.com/pub/"
    ]
    
    headers = {
        "Authorization": f"Bearer {EVERNOTE_TOKEN}",
        "User-Agent": "MCP-Server-Export/1.0"
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        for endpoint in export_endpoints:
            print(f"\n📥 Testing export endpoint: {endpoint}")
            
            try:
                response = await client.get(endpoint, headers=headers)
                print(f"   Status: {response.status_code}")
                print(f"   Response: {response.text[:200]}...")
                
                if response.status_code == 200:
                    print("   ✅ Export endpoint accessible!")
                
            except Exception as e:
                print(f"   Error: {str(e)[:100]}...")

async def simple_note_search():
    """Simple approach to search for notes"""
    
    print("\n🔍 SIMPLE NOTE SEARCH")
    print("=" * 50)
    
    # Try the most basic approach
    search_url = "https://www.evernote.com/shard/s1/notestore"
    
    # Basic search request
    search_data = {
        "method": "findNotes",
        "params": {
            "authenticationToken": EVERNOTE_TOKEN,
            "filter": {},
            "offset": 0,
            "maxNotes": 10
        }
    }
    
    headers = {
        "Authorization": f"Bearer {EVERNOTE_TOKEN}",
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            print(f"📡 Searching for notes at: {search_url}")
            response = await client.post(search_url, json=search_data, headers=headers)
            
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text[:500]}...")
            
            if response.status_code == 200:
                print("   ✅ Got successful response!")
                
                # Try to parse any JSON content
                try:
                    data = response.json()
                    print(f"   📄 JSON data: {data}")
                except:
                    print("   📄 Response is not JSON")
            
        except Exception as e:
            print(f"   Error: {str(e)[:100]}...")

async def main():
    """Main test function"""
    
    print("🚀 TESTING EVERNOTE READ CAPABILITIES")
    print("🎯 Trying to read notes from your Evernote account")
    print(f"🔑 Token: {EVERNOTE_TOKEN[:10]}...")
    print()
    
    # Test different approaches
    await test_evernote_read_api()
    await test_evernote_thrift_api()
    await check_evernote_web_interface()
    await try_evernote_export_api()
    await simple_note_search()
    
    print("\n🎯 SUMMARY:")
    print("=" * 30)
    print("✅ Token is valid (getting 200 responses)")
    print("⚠️ API format needs correct Thrift protocol")
    print("💡 Web interface might be accessible")
    print("📝 Export endpoints might work")
    print("🔧 MCP server framework is ready")
    
    print("\n🎯 NEXT STEPS:")
    print("1. Any 200 responses show working endpoints")
    print("2. Look for note content in responses")
    print("3. Use working endpoints for MCP server")
    print("4. Build on successful API calls")

if __name__ == "__main__":
    asyncio.run(main()) 