# 📋 Installation Guide - Darbot Windows MCP

<div align="center">
  <img src="assets/logo.png" alt="Darbot Windows MCP Logo" width="64" height="64">
  <h2>📋 Installation Guide</h2>
</div>

This guide provides comprehensive installation instructions for all supported methods to get Darbot Windows MCP running on your system.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Method 1: NPM Installation (Recommended)](#method-1-npm-installation-recommended)
- [Method 2: UV Installation](#method-2-uv-installation)
- [Method 3: Standard Python Installation](#method-3-standard-python-installation)
- [VS Code Configuration](#vs-code-configuration)
- [Claude Desktop Configuration](#claude-desktop-configuration)
- [Testing Your Installation](#testing-your-installation)
- [Common Issues](#common-issues)

## Prerequisites

Before installing Darbot Windows MCP, ensure you have the following:

### System Requirements
- **Windows 11** (Windows 10 may work but is not officially supported)
- **English Windows locale** for consistent UI Automation tree
- **Administrator privileges** (for some installation steps)

### Software Dependencies
- **Node.js 16+** (for NPM installation method)
- **Python 3.13+** (required for the MCP server)
- **Git** (for cloning repository if needed)

### Check Your System

```bash
# Check Node.js version
node --version

# Check Python version
python --version

# Check if Git is installed
git --version
```

## Method 1: NPM Installation (Recommended)

The NPM installation is the easiest and most automated method, now with refined installation process for seamless VSCode MCP integration.

### Option A: Global Installation

```bash
# Install globally
npm install -g @darbotlabs/darbot-windows-mcp
```

### Option B: VSCode MCP Server UI Installation

1. Open VSCode settings (Ctrl+,)
2. Search for "MCP" and click "Add MCP Server"
3. Select "NPM Package" as the server type
4. Enter package name: `@darbotlabs/darbot-windows-mcp`
5. VSCode will automatically install the package

### Step 2: Complete Setup

```bash
# Run the interactive setup wizard
darbot-setup
```

The setup wizard will:
- ✅ Check and guide Python 3.12+ installation if needed
- ✅ Install Python dependencies (UV or pip)
- ✅ Configure VS Code MCP integration
- ✅ Configure Claude Desktop integration
- ✅ Test the installation

**Note:** If Python is not installed, the setup wizard will:
- Provide download links and installation instructions
- Wait for you to install Python
- Allow you to retry the setup process

### Step 3: Start the Server

```bash
# Start the MCP server
darbot-windows-mcp

# Or show help
darbot-windows-mcp --help
```

### Troubleshooting NPM Installation

If you encounter issues:

```bash
# Check if package installed correctly
npm list -g @darbotlabs/darbot-windows-mcp

# Run dependency check manually
npm run install-deps

# Get help
darbot-windows-mcp --help
```

## Method 2: UV Installation

UV is a modern, fast Python package manager that provides faster dependency management.

### Step 1: Install UV

```bash
# Install UV using PowerShell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or install via pip
python -m pip install uv
```

### Step 2: Clone the Repository

```bash
git clone https://github.com/darbotlabs/Darbot-Windows-MCP.git
cd Darbot-Windows-MCP
```

### Step 3: Install Dependencies

```bash
# Sync dependencies with UV
uv sync
```

### Step 4: Test the Installation

```bash
# Run the server to test
uv run python main.py --help
```

## Method 3: Standard Python Installation

Use this method if you prefer traditional Python virtual environments.

### Step 1: Clone the Repository

```bash
git clone https://github.com/darbotlabs/Darbot-Windows-MCP.git
cd Darbot-Windows-MCP
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
# Install from requirements file
python -m pip install -r requirements.txt
```

If `requirements.txt` doesn't work, install dependencies manually:

```bash
python -m pip install fastmcp pyautogui uiautomation pyperclip requests markdownify humancursor live-inspect
```

### Step 4: Test the Installation

```bash
# Test the server
python main.py --help
```

## VS Code Configuration

After installing Darbot Windows MCP, configure it for VS Code agent mode.

### Option A: Automatic Configuration (NPM Users)

If you used the NPM installation and setup wizard, configuration is automatic. Skip to [Testing Your Installation](#testing-your-installation).

### Option B: Manual Configuration

#### 1. Create MCP Configuration

Create or update `.vscode/mcp.json` in your workspace root:

**For UV Installation:**
```json
{
  "servers": {
    "darbot-windows-mcp": {
      "type": "stdio",
      "command": "uv",
      "args": [
        "--directory",
        "${workspaceFolder}/Darbot-Windows-MCP",
        "run",
        "main.py"
      ]
    }
  },
  "inputs": []
}
```

**For Standard Python Installation:**
```json
{
  "servers": {
    "darbot-windows-mcp": {
      "type": "stdio",
      "command": "python",
      "args": [
        "${workspaceFolder}/Darbot-Windows-MCP/main.py"
      ],
      "cwd": "${workspaceFolder}/Darbot-Windows-MCP"
    }
  },
  "inputs": []
}
```

**For NPM Installation:**
```json
{
  "servers": {
    "darbot-windows-mcp": {
      "type": "stdio",
      "command": "darbot-windows-mcp"
    }
  },
  "inputs": []
}
```

#### 2. Configure VS Code Settings

Create or update `.vscode/settings.json` in your workspace root:

**For UV Installation:**
```json
{
  "mcp.servers": {
    "darbot-windows-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "${workspaceFolder}/Darbot-Windows-MCP",
        "run",
        "main.py"
      ],
      "env": {}
    }
  }
}
```

**For Standard Python Installation:**
```json
{
  "mcp.servers": {
    "darbot-windows-mcp": {
      "command": "python",
      "args": [
        "${workspaceFolder}/Darbot-Windows-MCP/main.py"
      ],
      "cwd": "${workspaceFolder}/Darbot-Windows-MCP",
      "env": {}
    }
  }
}
```

**For NPM Installation:**
```json
{
  "mcp.servers": {
    "darbot-windows-mcp": {
      "command": "darbot-windows-mcp",
      "env": {}
    }
  }
}
```

#### 3. Restart VS Code

After configuration, restart VS Code to load the MCP server.

## Claude Desktop Configuration

Configure Darbot Windows MCP for Claude Desktop if needed.

### Automatic Configuration (NPM Users)

The setup wizard handles this automatically for NPM installations.

### Manual Configuration

Add to your Claude Desktop configuration file (usually in `%APPDATA%\Claude\`):

```json
{
  "mcpServers": {
    "darbot-windows-mcp": {
      "command": "darbot-windows-mcp"
    }
  }
}
```

## Testing Your Installation

### Basic Server Test

Test that the server starts correctly:

```bash
# For NPM installation
darbot-windows-mcp --help

# For UV installation
uv run python main.py --help

# For standard Python installation
python main.py --help
```

All should display server information without errors.

### VS Code Agent Mode Test

1. Open VS Code in a workspace with MCP configured
2. Open the Command Palette (`Ctrl+Shift+P`)
3. Look for agent-related commands
4. Try a simple command like "get desktop state"

### Tool Availability Test

Run the server and check that all 15 tools are available:

```bash
# Start server and look for "15 tools" in output
darbot-windows-mcp
```

## Common Issues

### "No module named uv"

**Error:**
```
C:\Users\[username]\AppData\Local\Programs\Python\Python312\python.exe: No module named uv
```

**Solutions:**

1. **Install UV:**
   ```bash
   python -m pip install uv
   ```

2. **Use standalone UV installer:**
   ```bash
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

3. **Switch to standard Python method** (see Method 3 above)

### NPM Installation Fails

**Solutions:**

1. **Clear NPM cache:**
   ```bash
   npm cache clean --force
   npm install -g darbot-windows-mcp --force
   ```

2. **Install from source:**
   ```bash
   git clone https://github.com/darbotlabs/Darbot-Windows-MCP.git
   cd Darbot-Windows-MCP
   npm install
   npm link
   ```

### MCP Server Connection Issues

**Check these items:**

1. **Dependencies installed** - Run dependency installation command for your method
2. **Python version 3.13+** - Check with `python --version`
3. **VS Code restarted** after configuration changes
4. **Correct workspace folder path** in configuration files
5. **No other MCP server running** on the same name

### Permission Errors

**Solutions:**

1. **Run as Administrator** for initial installation
2. **Check antivirus software** - may block automation tools
3. **Windows Security settings** - ensure Python/Node.js are allowed

### VS Code Not Recognizing MCP

**Solutions:**

1. **Check VS Code MCP extension** is installed and enabled
2. **Verify configuration files** are in correct locations
3. **Check file paths** in configuration match your installation
4. **Restart VS Code** after any configuration changes

## Getting Help

If you're still having issues:

1. Check the [Troubleshooting Guide](TROUBLESHOOTING.md)
2. Review the [Issues on GitHub](https://github.com/darbotlabs/Darbot-Windows-MCP/issues)
3. Create a new issue with your system details and error messages

## Next Steps

After successful installation:

- Review the [Tools Reference](TOOLS.md) to understand available functionality
- Check the [Usage Examples](#usage-examples) in the main README
- Try the desktop automation features with your AI assistant
- Explore the [Development Guide](DEVELOPMENT.md) if you want to add custom tools