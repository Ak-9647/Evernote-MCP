#!/usr/bin/env python3
"""
Setup script for Evernote MCP Server

This script helps users install dependencies and configure the server.
"""

import os
import sys
import subprocess
import json
from pathlib import Path


def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def get_claude_config_path():
    """Get the Claude Desktop configuration path based on OS"""
    if sys.platform == "win32":
        # Windows
        appdata = os.environ.get("APPDATA")
        if appdata:
            return Path(appdata) / "Claude" / "claude_desktop_config.json"
    elif sys.platform == "darwin":
        # macOS
        home = Path.home()
        return home / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    else:
        # Linux (not officially supported by Claude Desktop, but just in case)
        home = Path.home()
        return home / ".config" / "claude" / "claude_desktop_config.json"
    
    return None


def setup_claude_config():
    """Help user set up Claude Desktop configuration"""
    print("\n🔧 Setting up Claude Desktop configuration...")
    
    config_path = get_claude_config_path()
    if not config_path:
        print("❌ Could not determine Claude Desktop config path for your OS")
        return False
    
    # Get absolute path to the server script
    server_path = Path(__file__).parent.absolute() / "evernote_mcp_server.py"
    
    # Template configuration
    config = {
        "mcpServers": {
            "evernote": {
                "command": "python",
                "args": [str(server_path)],
                "env": {}
            }
        }
    }
    
    print(f"📍 Claude config will be saved to: {config_path}")
    
    # Check if config file exists
    if config_path.exists():
        print("⚠️  Claude Desktop config file already exists.")
        response = input("Do you want to merge with existing config? (y/n): ").lower().strip()
        
        if response == 'y':
            try:
                with open(config_path, 'r') as f:
                    existing_config = json.load(f)
                
                # Merge configurations
                if "mcpServers" not in existing_config:
                    existing_config["mcpServers"] = {}
                
                existing_config["mcpServers"]["evernote"] = config["mcpServers"]["evernote"]
                config = existing_config
                
            except Exception as e:
                print(f"❌ Error reading existing config: {e}")
                return False
    else:
        # Create directory if it doesn't exist
        config_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write configuration
    try:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print("✅ Claude Desktop configuration updated!")
        print(f"📄 Config saved to: {config_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error writing config file: {e}")
        return False


def get_evernote_token():
    """Help user set up Evernote developer token"""
    print("\n🔑 Evernote API Setup")
    print("=" * 50)
    print("To use this MCP server, you need an Evernote developer token.")
    print("\n📋 Steps to get your token:")
    print("1. Visit https://dev.evernote.com/")
    print("2. Fill out the contact form to request API access")
    print("3. Provide these details:")
    print("   - Application name: 'Personal MCP Server'")
    print("   - Description: 'MCP server for AI assistant integration'")
    print("   - Access level: Choose Basic or Full based on your needs")
    print("4. You'll receive a developer token via email")
    
    print(f"\n💡 Once you have your token, you can configure it in Claude by saying:")
    print("   'Configure Evernote with my developer token: YOUR_TOKEN_HERE'")
    
    response = input("\nDo you want to continue with the setup? (y/n): ").lower().strip()
    return response == 'y'


def main():
    """Main setup function"""
    print("🚀 Evernote MCP Server Setup")
    print("=" * 40)
    
    # Step 1: Install dependencies
    if not install_dependencies():
        return
    
    # Step 2: Set up Claude configuration
    if not setup_claude_config():
        print("⚠️  Claude configuration failed, but you can set it up manually.")
        print("See README.md for manual configuration instructions.")
    
    # Step 3: Evernote token setup
    if not get_evernote_token():
        print("⚠️  Skipping Evernote token setup.")
    
    print("\n🎉 Setup complete!")
    print("\n📖 Next steps:")
    print("1. Get your Evernote developer token (see instructions above)")
    print("2. Restart Claude Desktop")
    print("3. In Claude, say: 'Configure Evernote with my developer token: YOUR_TOKEN'")
    print("4. Start creating, searching, and managing notes with AI!")
    
    print(f"\n📚 For more details, see README.md")


if __name__ == "__main__":
    main() 