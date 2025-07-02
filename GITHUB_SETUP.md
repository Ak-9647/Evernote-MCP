# 🚀 GitHub Setup Guide

## Step 1: Install Prerequisites

### **Install Python (if not already installed)**
- **Windows**: Download from [python.org](https://www.python.org/downloads/) - **IMPORTANT**: Check "Add Python to PATH"
- **macOS**: `brew install python` or download from python.org
- **Linux**: `sudo apt install python3 python3-pip` (Ubuntu/Debian)

### **Install Git (if not already installed)**

### **Windows:**
1. Download Git from [https://git-scm.com/download/win](https://git-scm.com/download/win)
2. Run the installer with default settings
3. Restart your terminal/PowerShell

### **macOS:**
```bash
# Install via Homebrew (recommended)
brew install git

# Or download from https://git-scm.com/download/mac
```

### **Linux:**
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install git

# CentOS/RHEL
sudo yum install git
```

## Step 2: Configure Git (First Time Only)

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## Step 3: Upload to Your GitHub Repository

### **Option A: Push to https://github.com/Ak-9647/Evernote-MCP.git**

```bash
# Navigate to your project directory
cd C:\MCP

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit - Evernote MCP Server"

# Add your GitHub repository as remote
git remote add origin https://github.com/Ak-9647/Evernote-MCP.git

# Set main branch
git branch -M main

# Push to GitHub
git push -u origin main
```

### **Option B: Create Your Own Repository**

1. **Go to GitHub** and create a new repository
2. **Copy the repository URL** (e.g., `https://github.com/yourusername/your-repo.git`)
3. **Run these commands:**

```bash
# Navigate to your project directory
cd C:\MCP

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit - Evernote MCP Server"

# Add your GitHub repository as remote
git remote add origin https://github.com/yourusername/your-repo.git

# Set main branch
git branch -M main

# Push to GitHub
git push -u origin main
```

## Step 4: Verify Upload

1. **Visit your GitHub repository** in a web browser
2. **Check that all files are present:**
   - ✅ `evernote_mcp_server.py`
   - ✅ `README.md`
   - ✅ `requirements.txt`
   - ✅ `setup.py`
   - ✅ `test_server.py`
   - ✅ `LICENSE`
   - ✅ `.gitignore`
   - ✅ `claude_desktop_config.json`

## Step 5: Share with Others

Your repository is now live! Others can install it using:

```bash
git clone https://github.com/Ak-9647/Evernote-MCP.git
cd Evernote-MCP
python setup.py
```

## 🔧 Future Updates

When you make changes to your code:

```bash
# Add changed files
git add .

# Commit changes
git commit -m "Description of your changes"

# Push to GitHub
git push
```

## 🏷️ Creating Releases

1. **Go to your GitHub repository**
2. **Click "Releases"** → **"Create a new release"**
3. **Tag version:** `v1.0.0`
4. **Release title:** `Initial Release`
5. **Description:** 
   ```
   🎉 Initial release of Evernote MCP Server
   
   Features:
   - Full Evernote integration for Claude
   - Search, create, and manage notes
   - Easy setup with automated configuration
   - Comprehensive documentation
   ```

## 🎯 Make it Popular

1. **Add Topics** to your repository:
   - `evernote`
   - `mcp`
   - `claude`
   - `ai`
   - `model-context-protocol`
   - `productivity`

2. **Add a great description:**
   ```
   🤖 Connect Claude AI to your Evernote account! Create, search, and manage notes through natural language conversation.
   ```

3. **Enable GitHub Pages** for documentation (optional)

4. **Add to MCP Server Lists** and communities

---

**Your Evernote MCP Server is now ready to help the world! 🌍✨** 