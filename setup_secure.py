#!/usr/bin/env python3
"""
Secure Setup Script

This script helps users set up their environment variables securely.
"""

import os
import shutil
from pathlib import Path

def setup_environment():
    """Set up environment variables"""
    
    print("🔐 SECURE ENVIRONMENT SETUP")
    print("=" * 50)
    
    # Check if .env.example exists
    if not os.path.exists('.env.example'):
        print("❌ .env.example file not found!")
        return False
    
    # Create .env from template if it doesn't exist
    if not os.path.exists('.env'):
        shutil.copy('.env.example', '.env')
        print("✅ Created .env from template")
    
    # Prompt user for token
    print("\n🔑 EVERNOTE TOKEN SETUP")
    print("Get your token from: https://dev.evernote.com/doc/articles/dev_tokens.php")
    
    token = input("Enter your Evernote Developer Token: ").strip()
    
    if not token:
        print("❌ No token provided!")
        return False
    
    # Update .env file
    try:
        with open('.env', 'r') as f:
            content = f.read()
        
        content = content.replace('YOUR_EVERNOTE_TOKEN_HERE', token)
        
        with open('.env', 'w') as f:
            f.write(content)
        
        print("✅ Token saved to .env file")
        print("⚠️  IMPORTANT: Never commit the .env file to version control!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating .env: {e}")
        return False

def setup_claude_desktop():
    """Set up Claude Desktop configuration"""
    
    print("\n🤖 CLAUDE DESKTOP SETUP")
    print("=" * 50)
    
    # Get token from environment
    token = os.environ.get('EVERNOTE_DEVELOPER_TOKEN')
    if not token:
        print("❌ No token found in environment!")
        print("💡 Run this script first to set up your .env file")
        return False
    
    # Create Claude Desktop config
    current_dir = Path.cwd()
    mcp_server_path = current_dir / "working_mcp_server.py"
    
    if not mcp_server_path.exists():
        print(f"❌ MCP server file not found: {mcp_server_path}")
        return False
    
    claude_config_dir = Path.home() / "AppData" / "Roaming" / "Claude"
    claude_config_file = claude_config_dir / "claude_desktop_config.json"
    
    claude_config_dir.mkdir(parents=True, exist_ok=True)
    
    config = {
        "mcpServers": {
            "evernote": {
                "command": "python",
                "args": [str(mcp_server_path)],
                "env": {
                    "EVERNOTE_DEVELOPER_TOKEN": token
                }
            }
        }
    }
    
    import json
    with open(claude_config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Claude Desktop configured: {claude_config_file}")
    return True

def main():
    """Main setup function"""
    
    print("🚀 EVERNOTE MCP SERVER SETUP")
    print("Setting up secure environment for your MCP server")
    print()
    
    # Step 1: Set up environment
    if setup_environment():
        print("\n✅ Environment setup complete!")
        
        # Load the .env file
        if os.path.exists('.env'):
            with open('.env', 'r') as f:
                for line in f:
                    if line.strip() and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        os.environ[key] = value
        
        # Step 2: Set up Claude Desktop
        if setup_claude_desktop():
            print("\n🎉 SETUP COMPLETE!")
            print("=" * 40)
            print("✅ Environment variables configured")
            print("✅ Claude Desktop configured")
            print("✅ MCP server ready to use")
            print()
            print("🚀 Next steps:")
            print("1. Open Claude Desktop")
            print("2. Test: 'Test my Evernote connection'")
            print("3. Create notes with natural language!")
        else:
            print("\n⚠️  Environment setup complete, but Claude Desktop setup failed")
    else:
        print("\n❌ Setup failed!")

if __name__ == "__main__":
    main()
