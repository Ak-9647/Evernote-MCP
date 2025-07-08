#!/usr/bin/env python3
"""
Test script for Evernote MCP Server

This script helps users test their installation and configuration.
It can be run interactively or in a non-interactive mode for CI/CD.
"""

import asyncio
import sys
import json
import os
import argparse
from datetime import datetime

# Try to import required modules
try:
    import httpx
    print("✅ httpx module available")
except ImportError:
    print("❌ httpx module not found. Run: pip install httpx")
    sys.exit(1)

try:
    from mcp.server.fastmcp import FastMCP
    print("✅ MCP framework available")
except ImportError:
    print("❌ MCP framework not found. Run: pip install mcp")
    sys.exit(1)


def setup_parser():
    """Set up command-line argument parser."""
    parser = argparse.ArgumentParser(description="Evernote MCP Server Test Suite")
    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="Run in non-interactive mode for CI/CD."
    )
    parser.add_argument(
        "--token",
        help="Evernote developer token for non-interactive mode. Can also be set via EVERNOTE_DEVELOPER_TOKEN env var.",
        default=os.getenv("EVERNOTE_DEVELOPER_TOKEN")
    )
    parser.add_argument(
        "--sandbox",
        type=lambda x: (str(x).lower() == 'true'),
        default=True,
        help="Use sandbox environment (true/false). Default is true."
    )
    return parser


async def test_evernote_api_connection(developer_token: str, use_sandbox: bool = True):
    """Test connection to Evernote API"""
    host = "sandbox.evernote.com" if use_sandbox else "www.evernote.com"
    base_url = f"https://{host}/edam"
    
    headers = {
        "Authorization": f"Bearer {developer_token}",
        "Content-Type": "application/json"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            # Try to get user info (basic API test)
            response = await client.get(f"{base_url}/user", headers=headers)
            response.raise_for_status()
            user_data = response.json()
            
            print(f"✅ Successfully connected to Evernote API")
            print(f"   User: {user_data.get('username', 'Unknown')}")
            print(f"   Environment: {'Sandbox' if use_sandbox else 'Production'}")
            return True
            
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            print("❌ Authentication failed - check your developer token")
        elif e.response.status_code == 403:
            print("❌ Access forbidden - check your API permissions")
        else:
            print(f"❌ HTTP error {e.response.status_code}: {e.response.text}")
        return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False


async def test_mcp_server():
    """Test the MCP server functionality"""
    try:
        # Import the server module
        from evernote_mcp_server import app, EvernoteClient
        
        print("✅ MCP server module loaded successfully")
        
        # Test server initialization
        server_info = {
            "name": app.name if hasattr(app, 'name') else "Evernote MCP Server",
            "version": getattr(app, 'version', '1.0.0')
        }
        
        print(f"   Server: {server_info['name']}")
        print(f"   Version: {server_info['version']}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Failed to import MCP server: {e}")
        return False
    except Exception as e:
        print(f"❌ MCP server error: {e}")
        return False


def test_claude_config():
    """Test Claude Desktop configuration"""
    import os
    from pathlib import Path
    
    # Determine config path based on OS
    if sys.platform == "win32":
        appdata = os.environ.get("APPDATA")
        if appdata:
            config_path = Path(appdata) / "Claude" / "claude_desktop_config.json"
    elif sys.platform == "darwin":
        home = Path.home()
        config_path = home / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    else:
        home = Path.home()
        config_path = home / ".config" / "claude" / "claude_desktop_config.json"
    
    if not config_path.exists():
        print("⚠️  Claude Desktop config file not found")
        print(f"   Expected location: {config_path}")
        print("   Run setup.py to create the configuration")
        return False
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        if "mcpServers" in config and "evernote" in config["mcpServers"]:
            print("✅ Claude Desktop configuration found")
            print(f"   Config file: {config_path}")
            return True
        else:
            print("⚠️  Evernote MCP server not configured in Claude Desktop")
            print("   Run setup.py to add the configuration")
            return False
            
    except Exception as e:
        print(f"❌ Error reading Claude config: {e}")
        return False


async def main():
    """Main test function"""
    parser = setup_parser()
    args = parser.parse_args()

    print("🧪 Evernote MCP Server Test Suite")
    print("=" * 50)
    
    # Test 1: Python modules
    print("\n1️⃣ Testing Python Dependencies...")
    # Already tested in imports above
    
    # Test 2: MCP server
    print("\n2️⃣ Testing MCP Server...")
    mcp_ok = await test_mcp_server()
    
    # Test 3: Claude configuration
    print("\n3️⃣ Testing Claude Desktop Configuration...")
    claude_ok = test_claude_config()
    
    # Test 4: Evernote API (if token provided)
    print("\n4️⃣ Testing Evernote API Connection...")
    token = args.token
    use_sandbox = args.sandbox

    if not args.non_interactive and not token:
        token = input("Enter your Evernote developer token (or press Enter to skip): ").strip()
        if token:
            use_sandbox_input = input("Use sandbox environment? (y/n, default=y): ").strip().lower()
            use_sandbox = use_sandbox_input != 'n'

    if token:
        evernote_ok = await test_evernote_api_connection(token, use_sandbox)
    else:
        if args.non_interactive:
            print("❌ Non-interactive mode requires a token via --token or EVERNOTE_DEVELOPER_TOKEN env var.")
            evernote_ok = False
        else:
            print("⏭️  Skipping Evernote API test (no token provided)")
            evernote_ok = None
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)
    print(f"✅ Python Dependencies: OK")
    print(f"{'✅' if mcp_ok else '❌'} MCP Server: {'OK' if mcp_ok else 'FAILED'}")
    print(f"{'✅' if claude_ok else '⚠️ '} Claude Configuration: {'OK' if claude_ok else 'NEEDS SETUP'}")
    
    if evernote_ok is not None:
        print(f"{'✅' if evernote_ok else '❌'} Evernote API: {'OK' if evernote_ok else 'FAILED'}")
    else:
        print("⏭️  Evernote API: SKIPPED")
    
    # Recommendations
    print("\n💡 Recommendations:")
    if not mcp_ok:
        print("   • Check that evernote_mcp_server.py is in the same directory")
        print("   • Ensure all dependencies are installed: pip install -r requirements.txt")
    
    if not claude_ok:
        print("   • Run setup.py to configure Claude Desktop")
        print("   • Or manually add the MCP server to Claude's config file")
    
    if evernote_ok is False:
        print("   • Verify your Evernote developer token is correct")
        print("   • Check that you're using the right environment (sandbox vs production)")
        print("   • Ensure your API key has the necessary permissions")
    
    all_passed = mcp_ok and claude_ok and (evernote_ok is not False)
    
    if all_passed:
        print("\n🎉 All critical tests passed! Your Evernote MCP server is ready to use.")
        if not args.non_interactive:
            print("   • Restart Claude Desktop")
            print("   • Configure your token: 'Configure Evernote with my developer token: YOUR_TOKEN'")
            print("   • Start creating and managing notes with AI!")
    else:
        print("\n❌ Some tests failed. Please review the recommendations above.")

    if args.non_interactive and not all_passed:
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main()) 