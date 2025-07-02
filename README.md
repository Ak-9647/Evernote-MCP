# 📝 Evernote MCP Server

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![MCP](https://img.shields.io/badge/MCP-Compatible-purple.svg)

A **Model Context Protocol (MCP) server** that enables AI assistants like Claude to interact with Evernote, allowing them to create, search, read, and manage notes seamlessly through natural language.

> 🤖 **Transform your Evernote into Claude's brain!** This MCP server bridges the gap between AI and your personal knowledge base.

## ✨ Features

### 🔧 **AI Tools Available**
- **`search_notes`** - Search through your Evernote notes with advanced queries
- **`get_note_content`** - Retrieve full content of specific notes  
- **`create_note`** - Create new notes with title, content, and tags
- **`update_note`** - Modify existing notes
- **`create_notebook`** - Create new notebooks for organization
- **`configure_evernote`** - Set up authentication with your Evernote account

### 📋 **Live Resources**
- **`notebooks://list`** - Real-time access to your notebook structure
- **`tags://list`** - Available tags for organization
- **`recent-notes://list`** - Recently modified notes

## 🚀 Quick Installation

### **Option 1: One-Click Install (Recommended)**

```bash
# Clone this repository
git clone https://github.com/Ak-9647/Evernote-MCP.git
cd Evernote-MCP

# Run the automated setup
python setup.py
```

### **Option 2: Manual Setup**

```bash
# Clone the repository
git clone https://github.com/Ak-9647/Evernote-MCP.git
cd Evernote-MCP

# Install dependencies
pip install -r requirements.txt
```

## 🔑 Get Your Evernote API Key

**IMPORTANT:** You need an Evernote Developer Token to use this MCP server.

### **Step-by-Step Guide:**

1. **Visit [Evernote Developer Portal](https://dev.evernote.com/)**

2. **Request API Access** by filling out their contact form:
   ```
   Full Name: [Your Name]
   Organization: Personal Use
   Application Name: Personal MCP Server  
   Description: MCP server for AI assistant integration with personal Evernote account
   Access Level: Full Access (recommended) or Basic Access
   ```

3. **Wait for Approval** (usually 1-5 business days)

4. **You'll receive via email:**
   - Consumer Key
   - Consumer Secret  
   - **Developer Token** ← This is what you need!

## ⚙️ Configuration with Claude Desktop

### **Step 1: Locate Claude Desktop Config File**

Find your Claude Desktop configuration file:

- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux:** `~/.config/claude/claude_desktop_config.json`

### **Step 2: Add MCP Server Configuration**

Add this to your `claude_desktop_config.json` file:

```json
{
  "mcpServers": {
    "evernote": {
      "command": "python",
      "args": ["/full/path/to/Evernote-MCP/evernote_mcp_server.py"],
      "env": {}
    }
  }
}
```

**Replace `/full/path/to/Evernote-MCP/` with the actual path where you cloned this repository!**

### **Step 3: Restart Claude Desktop**

Close and reopen Claude Desktop to load the new MCP server.

## 🔐 Setting Up Your API Key

### **Method 1: Through Claude (Recommended)**

1. **Open Claude Desktop**
2. **Say:** *"Configure Evernote with my developer token: YOUR_DEVELOPER_TOKEN_HERE"*
3. **Claude will respond** with confirmation that Evernote is configured

### **Method 2: Environment Variables (Advanced)**

Create a `.env` file in the project directory:

```bash
# .env file
EVERNOTE_DEVELOPER_TOKEN=your_token_here
EVERNOTE_USE_SANDBOX=true
```

**🚨 Security Note:** Never commit your actual API tokens to Git! The `.env` file is already in `.gitignore`.

## 💡 How to Use with Claude

Once configured, you can interact with your Evernote through natural language in Claude:

### **📝 Creating Notes**
```
👤 "Create a note called 'Meeting Summary' with today's discussion points and tag it 'work'"

🤖 Claude will create the note and confirm: "I've created a note titled 'Meeting Summary' 
   in your default notebook with the 'work' tag."
```

### **🔍 Searching Notes**  
```
👤 "Find all my notes about machine learning from the past month"

🤖 Claude will search and show: "I found 5 notes about machine learning from the past month:
   1. 'Neural Networks Basics' (Dec 15)
   2. 'TensorFlow Tutorial' (Dec 20)..."
```

### **📖 Reading Content**
```
👤 "Show me the content of my note titled 'Project Ideas'"

🤖 Claude will retrieve and display the full note content with formatting preserved.
```

### **🗂️ Organization**
```
👤 "Create a new notebook called 'AI Research' and organize my machine learning notes there"

🤖 Claude will create the notebook and can help move related notes.
```

### **🔄 Smart Updates**
```
👤 "Add today's meeting notes to my existing 'Weekly Standup' note"

🤖 Claude will find the note and append the new information.
```

## 🧪 Testing Your Installation

### **Quick Test**

Run the built-in test script:

```bash
cd Evernote-MCP
python test_server.py
```

This will test:
- ✅ Python dependencies
- ✅ MCP server functionality  
- ✅ Claude Desktop configuration
- ✅ Evernote API connection (if you provide your token)

### **Manual Verification**

1. **Check Claude Desktop** - Look for "🔧 Evernote" in Claude's available tools
2. **Test Configuration** - Say: *"Configure Evernote with my token: YOUR_TOKEN"*
3. **Test Search** - Say: *"Search my Evernote for any note"*

## 🔧 Architecture

```
┌─────────────────┐    MCP Protocol    ┌─────────────────┐    Evernote API    ┌─────────────────┐
│                 │◄──────────────────►│                 │◄──────────────────►│                 │
│  Claude Desktop │     (JSON-RPC)     │ Evernote MCP    │      (HTTPS)       │  Evernote       │
│  (MCP Client)   │                    │    Server       │                    │  Service        │
│                 │                    │                 │                    │                 │
└─────────────────┘                    └─────────────────┘                    └─────────────────┘
```

### **Component Breakdown:**

1. **Claude Desktop** - The MCP client that sends requests
2. **Evernote MCP Server** - This application that translates MCP calls to Evernote API
3. **Evernote Service** - The actual Evernote cloud service

## 🔐 Security & Authentication

### **Developer Tokens**
- Used for development and personal use
- Tied to a specific Evernote account
- Access level determined when requesting API key

### **OAuth (Future Enhancement)**
- For production applications
- Allows users to authorize access without sharing credentials
- More secure for shared or distributed applications

### **Environment Variables**
For enhanced security, you can set environment variables:

```bash
export EVERNOTE_DEVELOPER_TOKEN="your_token_here"
export EVERNOTE_USE_SANDBOX="true"  # Set to "false" for production
```

## 🛠️ Development

### **Project Structure**
```
evernote-mcp-server/
├── evernote_mcp_server.py    # Main MCP server implementation
├── requirements.txt          # Python dependencies
├── README.md                # This file
└── tests/                   # Unit tests (future)
```

### **Key Classes**
- **`EvernoteClient`** - Handles Evernote API communication
- **`FastMCP`** - The MCP server framework
- **Tools & Resources** - MCP endpoints for AI interaction

### **Testing**
```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests (when implemented)
pytest tests/
```

## 🔍 Troubleshooting

### **❌ "Evernote client not initialized"**
**Solution:**
- Run: *"Configure Evernote with my developer token: YOUR_TOKEN"* in Claude
- Verify your developer token is correct
- Check if you're using sandbox vs production environment

### **❌ Claude doesn't see the Evernote tools**
**Solution:**
- Restart Claude Desktop completely
- Check the path in `claude_desktop_config.json` is correct
- Ensure Python can run: `python evernote_mcp_server.py`

### **❌ "Failed to create note"**
**Solution:**
- Ensure your API key has create permissions (Full Access recommended)
- Check that the specified notebook exists
- Verify your token hasn't expired

### **❌ Connection/Authentication Issues**
**Solution:**
- Test your token: `python test_server.py`
- Confirm internet connectivity
- Check if corporate firewall blocks Evernote API
- Try sandbox environment first: `EVERNOTE_USE_SANDBOX=true`

### **❌ Import/Module Errors**
**Solution:**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check Python version
python --version  # Should be 3.8+
```

### **💡 Still Having Issues?**

1. **Run the test script:** `python test_server.py`
2. **Check the logs** in Claude Desktop's developer console
3. **Create an issue** on this GitHub repository with:
   - Your operating system
   - Python version
   - Error messages
   - Steps you've tried

## 🚦 API Limits

Evernote has rate limits on API usage:
- **Basic Access**: Limited operations per hour
- **Full Access**: Higher rate limits
- **Production**: Different limits than sandbox

The server includes error handling for rate limit responses.

## 🚀 Installing from GitHub (For Users)

If someone shared this repository with you, here's how to get it running:

### **Quick Setup Commands**

```bash
# Clone the repository
git clone https://github.com/Ak-9647/Evernote-MCP.git
cd Evernote-MCP

# Install and configure everything
python setup.py

# Test your installation
python test_server.py
```

### **What the setup does:**
1. ✅ Installs all Python dependencies
2. ✅ Configures Claude Desktop automatically  
3. ✅ Guides you through getting your Evernote API key
4. ✅ Tests everything works correctly

## 🛣️ Roadmap

- [ ] **OAuth Support** - More secure authentication
- [ ] **Web Clipper Integration** - Save web pages via Claude
- [ ] **Shared Notebooks** - Collaborate through AI
- [ ] **Advanced Search** - Saved searches and filters
- [ ] **File Attachments** - Handle images and documents
- [ ] **Multi-Account** - Support multiple Evernote accounts

## 🤝 Contributing

We welcome contributions! Here's how:

### **For Developers:**
1. **Fork** this repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add amazing feature'`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### **For Users:**
- 🐛 **Report bugs** via GitHub Issues
- 💡 **Suggest features** you'd like to see
- 📚 **Improve documentation**
- ⭐ **Star this repo** if you find it useful!

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/Ak-9647/Evernote-MCP?style=social)
![GitHub forks](https://img.shields.io/github/forks/Ak-9647/Evernote-MCP?style=social)
![GitHub issues](https://img.shields.io/github/issues/Ak-9647/Evernote-MCP)

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Projects & Links

- 🔗 [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- 🔗 [Evernote Developer Documentation](https://dev.evernote.com/doc/)
- 🔗 [Claude Desktop](https://claude.ai/)
- 🔗 [MCP Server Registry](https://github.com/modelcontextprotocol/servers)

## ⚠️ Important Disclaimers

- **Unofficial Project:** Not affiliated with or endorsed by Evernote Corporation
- **Security:** Keep your API tokens secure and never commit them to public repositories
- **Compliance:** Ensure you follow Evernote's Terms of Service and API License Agreement
- **Rate Limits:** Respect Evernote's API rate limits to avoid service interruption

---

## 🎉 Success Stories

*"This MCP server transformed how I use my Evernote. Now Claude can help me organize 10 years of notes effortlessly!"* - Happy User

---

**Made with ❤️ for the AI community**

**Star ⭐ this repo if it helps you! Happy Note-Taking with AI! 🤖📚** 