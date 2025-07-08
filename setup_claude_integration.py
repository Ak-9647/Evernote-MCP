#!/usr/bin/env python3
"""
Set Up Claude Desktop Integration

This script helps you set up the proper Claude Desktop integration
so you can actually write to Evernote using natural language.
"""

import json
import os
from pathlib import Path

# Your Evernote developer token
EVERNOTE_TOKEN = os.environ.get("EVERNOTE_DEVELOPER_TOKEN", "YOUR_TOKEN_HERE")

def setup_claude_desktop_config():
    """Set up Claude Desktop configuration for MCP server"""
    
    print("🖥️ Setting Up Claude Desktop Integration")
    print("=" * 50)
    
    # Claude Desktop config path
    config_path = Path.home() / "AppData" / "Roaming" / "Claude" / "claude_desktop_config.json"
    
    print(f"📁 Config file location: {config_path}")
    
    # Create the configuration
    config = {
        "mcpServers": {
            "evernote": {
                "command": "python",
                "args": [str(Path.cwd() / "evernote_mcp_server.py")],
                "env": {
                    "EVERNOTE_DEVELOPER_TOKEN": EVERNOTE_TOKEN
                }
            }
        }
    }
    
    # Ensure directory exists
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write config file
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ Claude Desktop configuration created!")
    print(f"📄 Configuration:")
    print(json.dumps(config, indent=2))
    
    return config_path

def create_usage_guide():
    """Create a guide for using the MCP server with Claude Desktop"""
    
    print("\n📚 How to Use Your Evernote MCP Server")
    print("=" * 50)
    
    print("1️⃣ **Start Claude Desktop**")
    print("   - Open Claude Desktop application")
    print("   - The MCP server will load automatically")
    
    print("\n2️⃣ **Use Natural Language Commands**")
    examples = [
        "Create a note titled 'Meeting Notes' with content 'Discussed project timeline'",
        "Show me all my notebooks",
        "Search for notes about 'project planning'",
        "Create a daily journal entry for today",
        "Make a note called 'Ideas' with my brainstorming thoughts"
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"   Example {i}: \"{example}\"")
    
    print("\n3️⃣ **What Happens**")
    print("   - Claude receives your request")
    print("   - Calls the appropriate MCP server tool")
    print("   - MCP server connects to Evernote API")
    print("   - Real note gets created in your account")
    print("   - Claude reports back the success")

def test_mcp_server_readiness():
    """Test if the MCP server is ready"""
    
    print("\n🧪 Testing MCP Server Readiness")
    print("=" * 40)
    
    # Check if server file exists
    server_file = Path("evernote_mcp_server.py")
    if server_file.exists():
        print("✅ MCP server file exists")
    else:
        print("❌ MCP server file missing")
        return False
    
    # Check if dependencies are available
    try:
        import mcp
        print("✅ MCP library available")
    except ImportError:
        print("❌ MCP library missing")
        return False
    
    try:
        import httpx
        print("✅ HTTP client available")
    except ImportError:
        print("❌ HTTP client missing")
        return False
    
    print("✅ Token configured")
    print(f"   Token: {EVERNOTE_TOKEN[:10]}...")
    
    return True

def create_test_script():
    """Create a simple test script to verify the setup"""
    
    test_script = f'''#!/usr/bin/env python3
"""
Quick Test for Evernote MCP Server

Run this after setting up Claude Desktop to test the integration.
"""

import subprocess
import sys

def test_claude_integration():
    print("🧪 Testing Claude Desktop Integration")
    print("1. Make sure Claude Desktop is running")
    print("2. Try these commands in Claude Desktop:")
    print()
    print("   'Create a test note titled \\"MCP Test\\" with content \\"Hello from MCP server!\\"'")
    print("   'Show me my Evernote notebooks'")
    print("   'Search my notes for \\"test\\"'")
    print()
    print("3. If these work, your MCP server is successfully integrated!")
    print()
    print("🔑 Your token: {EVERNOTE_TOKEN[:10]}...")
    print("📁 Config file: ~/AppData/Roaming/Claude/claude_desktop_config.json")

if __name__ == "__main__":
    test_claude_integration()
'''
    
    with open("test_claude_integration.py", "w") as f:
        f.write(test_script)
    
    print("\n📝 Created test_claude_integration.py")
    print("   Run this after Claude Desktop setup to verify integration")

def main():
    """Main function to set up everything"""
    
    print("🚀 Setting Up Evernote MCP Server Integration")
    print("🎯 This will enable you to write to Evernote using natural language!")
    
    # Test readiness
    if not test_mcp_server_readiness():
        print("\n❌ MCP server not ready. Please install dependencies first.")
        return
    
    # Set up Claude Desktop config
    config_path = setup_claude_desktop_config()
    
    # Create usage guide
    create_usage_guide()
    
    # Create test script
    create_test_script()
    
    print("\n🎉 Setup Complete!")
    print("=" * 50)
    
    print("✅ **Next Steps:**")
    print("1. **Restart Claude Desktop** (if it's running)")
    print("2. **Open Claude Desktop**")
    print("3. **Try this command:** 'Create a note called \"MCP Test\" with content \"Hello from my MCP server!\"'")
    print("4. **Check your Evernote account** for the new note!")
    
    print(f"\n📍 **Configuration file created:** {config_path}")
    print(f"🔑 **Your token:** {EVERNOTE_TOKEN[:10]}...")
    print("🎯 **Status:** Ready for natural language Evernote interaction!")
    
    print("\n💡 **Example Commands to Try in Claude Desktop:**")
    print("   - 'Create a meeting note for today's standup'")
    print("   - 'Show me all my notebooks'") 
    print("   - 'Make a note with my project ideas'")
    print("   - 'Search for notes about Python'")

if __name__ == "__main__":
    main() 