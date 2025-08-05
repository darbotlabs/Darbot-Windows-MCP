# 🚧 Troubleshooting Guide - Darbot Windows MCP

<div align="center">
  <img src="assets/logo.png" alt="Darbot Windows MCP Logo" width="64" height="64">
  <h2>🚧 Troubleshooting Guide</h2>
</div>

This comprehensive troubleshooting guide helps resolve common issues with Darbot Windows MCP installation, configuration, and usage.

## 📋 Table of Contents

- [Installation Issues](#installation-issues)
- [Configuration Issues](#configuration-issues)
- [Runtime Issues](#runtime-issues)
- [Performance Issues](#performance-issues)
- [Compatibility Issues](#compatibility-issues)
- [VS Code Integration Issues](#vs-code-integration-issues)
- [Claude Desktop Issues](#claude-desktop-issues)
- [Tool-Specific Issues](#tool-specific-issues)
- [Diagnostic Commands](#diagnostic-commands)
- [Getting Help](#getting-help)

## Installation Issues

### NPM Installation Problems

#### Issue: "npm command not found"

**Solution:**
1. Install Node.js from [nodejs.org](https://nodejs.org/)
2. Restart your terminal/command prompt
3. Verify installation: `node --version && npm --version`

#### Issue: "Permission denied" during global install

**Solutions:**

**Option A: Run as Administrator**
```bash
# Open Command Prompt as Administrator
npm install -g darbot-windows-mcp
```

**Option B: Configure npm prefix (Recommended)**
```bash
# Set up user-level global directory
mkdir "%APPDATA%\npm"
npm config set prefix "%APPDATA%\npm"
npm install -g darbot-windows-mcp
```

**Option C: Use npx (No global install)**
```bash
npx darbot-windows-mcp
```

#### Issue: "EACCES: permission denied" on Windows

**Solution:**
```bash
# Clear npm cache and reinstall
npm cache clean --force
npm install -g darbot-windows-mcp --force
```

#### Issue: Package installation fails with network errors

**Solutions:**

1. **Check corporate firewall/proxy:**
   ```bash
   npm config set proxy http://proxy.company.com:8080
   npm config set https-proxy http://proxy.company.com:8080
   ```

2. **Use different registry:**
   ```bash
   npm install -g darbot-windows-mcp --registry https://registry.npmjs.org/
   ```

3. **Install from source:**
   ```bash
   git clone https://github.com/darbotlabs/Darbot-Windows-MCP.git
   cd Darbot-Windows-MCP
   npm install
   npm link
   ```

### Python Installation Problems

#### Issue: "Python not found" or "python is not recognized"

**Solutions:**

1. **Install Python 3.13+:**
   - Download from [python.org](https://python.org)
   - ✅ Check "Add Python to PATH" during installation

2. **Fix PATH issues:**
   ```bash
   # Add Python to PATH manually
   # Add these to System Environment Variables:
   C:\Users\[username]\AppData\Local\Programs\Python\Python313\
   C:\Users\[username]\AppData\Local\Programs\Python\Python313\Scripts\
   ```

3. **Use Python Launcher:**
   ```bash
   py --version
   py -m pip install --upgrade pip
   ```

#### Issue: "No module named uv"

**Error Message:**
```
C:\Users\[username]\AppData\Local\Programs\Python\Python312\python.exe: No module named uv
```

**Solutions:**

**Option 1: Install UV via pip**
```bash
python -m pip install uv
```

**Option 2: Install UV standalone**
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Option 3: Use standard Python instead**
```bash
# Skip UV, use regular pip
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

#### Issue: "Microsoft Visual C++ 14.0 is required"

**Solution:**
1. Install Microsoft C++ Build Tools
2. Or install Visual Studio Community with C++ workload
3. Alternative: Use pre-compiled wheels:
   ```bash
   pip install --only-binary=all -r requirements.txt
   ```

### Dependency Installation Issues

#### Issue: pyautogui installation fails

**Common on Windows systems without proper graphics libraries.**

**Solution:**
```bash
# Install system dependencies first
pip install --upgrade pip setuptools wheel
pip install pillow  # Install Pillow first
pip install pyautogui
```

#### Issue: uiautomation module issues

**Solution:**
```bash
# Reinstall with specific version
pip uninstall uiautomation
pip install uiautomation==2.0.20
```

## Configuration Issues

### VS Code MCP Configuration

#### Issue: VS Code doesn't recognize MCP server

**Checklist:**
1. ✅ VS Code has MCP extension installed
2. ✅ `.vscode/mcp.json` exists in workspace root
3. ✅ `.vscode/settings.json` has correct MCP configuration
4. ✅ File paths in configuration match your installation
5. ✅ VS Code has been restarted after configuration

**Common Configuration Errors:**

1. **Wrong file path separators:**
   ```json
   // ❌ Wrong (Unix paths on Windows)
   "${workspaceFolder}/Darbot-Windows-MCP/main.py"
   
   // ✅ Correct (Windows paths)
   "${workspaceFolder}\\Darbot-Windows-MCP\\main.py"
   // OR
   "${workspaceFolder}/Darbot-Windows-MCP/main.py"  // Both work
   ```

2. **Incorrect working directory:**
   ```json
   // ✅ Make sure cwd is set for Python installations
   {
     "mcp.servers": {
       "darbot-windows-mcp": {
         "command": "python",
         "args": ["main.py"],
         "cwd": "${workspaceFolder}/Darbot-Windows-MCP"
       }
     }
   }
   ```

#### Issue: "Server failed to start" in VS Code

**Diagnostic Steps:**

1. **Test server manually:**
   ```bash
   # For UV installation
   cd Darbot-Windows-MCP
   uv run python main.py --help
   
   # For standard Python
   cd Darbot-Windows-MCP
   python main.py --help
   
   # For NPM installation
   darbot-windows-mcp --help
   ```

2. **Check VS Code Developer Console:**
   - Press `F12` in VS Code
   - Look for MCP-related errors

3. **Verify configuration files:**
   ```bash
   # Check files exist
   dir .vscode\mcp.json
   dir .vscode\settings.json
   ```

### Path and Environment Issues

#### Issue: "command not found" in MCP configuration

**For UV installations:**
```json
// ✅ Full path to UV if not in PATH
{
  "command": "C:\\Users\\[username]\\.cargo\\bin\\uv.exe",
  "args": ["run", "python", "main.py"]
}
```

**For Python installations:**
```json
// ✅ Full path to Python if needed
{
  "command": "C:\\Users\\[username]\\AppData\\Local\\Programs\\Python\\Python313\\python.exe",
  "args": ["main.py"]
}
```

## Runtime Issues

### Server Startup Problems

#### Issue: Server starts but no tools available

**Diagnostic:**
```bash
# Check if server reports 15 tools
darbot-windows-mcp
# Should show: "Server running with 15 tools available"
```

**Solutions:**
1. **Reinstall dependencies:**
   ```bash
   # For UV
   uv sync --force
   
   # For pip
   pip install -r requirements.txt --force-reinstall
   ```

2. **Check Python version compatibility:**
   ```bash
   python --version  # Should be 3.13+
   ```

#### Issue: "ImportError" when starting server

**Common missing modules:**

```bash
# Install missing dependencies
pip install fastmcp pyautogui uiautomation pyperclip requests markdownify humancursor live-inspect
```

#### Issue: Server crashes on first tool usage

**Common causes:**
1. **Windows UI Automation not available**
2. **Antivirus blocking automation**
3. **Insufficient permissions**

**Solutions:**
1. **Run as Administrator (first time only)**
2. **Add Python to antivirus exclusions**
3. **Enable Windows UI Automation:**
   - Check Windows Accessibility settings
   - Enable "Use UI Automation"

### Tool Execution Problems

#### Issue: Click-Tool clicks wrong coordinates

**Causes:**
- Different screen resolution
- DPI scaling issues
- Multi-monitor setups

**Solutions:**
1. **Check DPI scaling:**
   - Right-click desktop → Display settings
   - Note scaling percentage (100%, 125%, 150%)

2. **Use State-Tool to find coordinates:**
   ```javascript
   "Get desktop state"  // Find exact coordinates
   "Click at [discovered coordinates]"
   ```

3. **Account for DPI scaling:**
   ```javascript
   // If scaling is 125%, multiply coordinates by 0.8
   // If scaling is 150%, multiply coordinates by 0.67
   ```

#### Issue: Type-Tool doesn't work in some applications

**Solutions:**
1. **Ensure application has focus:**
   ```javascript
   "Switch to notepad"  // Focus first
   "Type 'hello world'"  // Then type
   ```

2. **Try alternative input method:**
   ```javascript
   "Click at [text field coordinates]"  // Click field first
   "Send shortcut ['ctrl', 'a']"        // Select all
   "Type 'new content'"                 // Then type
   ```

#### Issue: Launch-Tool can't find applications

**Solutions:**
1. **Use exact application names:**
   ```javascript
   // ✅ Good
   "Launch notepad"
   "Launch calculator"
   
   // ❌ May not work
   "Launch text editor"
   "Launch calc"
   ```

2. **Use full executable paths for custom apps:**
   ```javascript
   "Run powershell 'Start-Process \"C:\\Path\\To\\App.exe\"'"
   ```

## Performance Issues

### Slow Response Times

#### Issue: Tools take too long to execute

**Solutions:**
1. **Reduce wait times in workflows:**
   ```javascript
   // Instead of long waits
   "Wait 5 seconds"
   
   // Use shorter, multiple checks
   "Wait 1 second"
   "Get desktop state"  // Check if ready
   ```

2. **Optimize UI interactions:**
   ```javascript
   // Direct coordinate clicks instead of searching
   "Click at 400, 300"  // Faster than finding elements
   ```

#### Issue: High CPU usage

**Causes:**
- Continuous polling
- Inefficient UI queries
- Memory leaks

**Solutions:**
1. **Restart MCP server periodically**
2. **Avoid rapid-fire tool calls**
3. **Use Wait-Tool between operations**

### Memory Issues

#### Issue: "Out of memory" errors

**Solutions:**
1. **Increase Python memory limit:**
   ```bash
   # Set environment variable
   set PYTHONMEMORY=2048
   ```

2. **Restart server after heavy usage**
3. **Avoid large screenshot captures**

## Compatibility Issues

### Windows Version Issues

#### Issue: Tools don't work on Windows 10

**Note:** Windows 11 is officially supported, Windows 10 may have limitations.

**Solutions:**
1. **Update to latest Windows 10 version**
2. **Install latest Windows updates**
3. **Enable Windows UI Automation features**

#### Issue: Different Windows languages

**Limitation:** Best performance with English Windows locale.

**Solutions:**
1. **Change Windows language to English (temporary)**
2. **Use coordinate-based operations instead of UI element names**

### Antivirus and Security Issues

#### Issue: Antivirus blocks automation tools

**Solutions:**
1. **Add Python to exclusions:**
   - Add Python installation directory
   - Add workspace folder
   - Add darbot-windows-mcp executable

2. **Windows Security exclusions:**
   - Windows Security → Virus & threat protection
   - Exclusions → Add folder
   - Add Python and project directories

#### Issue: "Execution policy" errors with PowerShell

**Solution:**
```bash
# Set execution policy (run as Administrator)
powershell -Command "Set-ExecutionPolicy RemoteSigned -Scope CurrentUser"
```

## VS Code Integration Issues

### Extension Problems

#### Issue: MCP extension not working

**Solutions:**
1. **Update VS Code to latest version**
2. **Reinstall MCP extension**
3. **Check extension compatibility**

#### Issue: Agent mode not available

**Solutions:**
1. **Enable GitHub Copilot**
2. **Check MCP extension settings**
3. **Restart VS Code with clean cache:**
   ```bash
   code --disable-extensions --user-data-dir temp_dir
   ```

### Configuration File Issues

#### Issue: Configuration not loading

**Checklist:**
1. ✅ Files in correct location (`.vscode/` in workspace root)
2. ✅ Valid JSON syntax
3. ✅ Correct server name matching
4. ✅ Proper file encoding (UTF-8)

**Validate JSON:**
```bash
# Use online JSON validator or
python -m json.tool .vscode/mcp.json
python -m json.tool .vscode/settings.json
```

## Claude Desktop Issues

### Integration Problems

#### Issue: Claude Desktop doesn't recognize MCP server

**Solutions:**
1. **Check Claude Desktop configuration file location**
2. **Verify JSON syntax in configuration**
3. **Restart Claude Desktop after configuration changes**

#### Issue: "Server not responding" in Claude Desktop

**Solutions:**
1. **Test server independently:**
   ```bash
   darbot-windows-mcp --help
   ```

2. **Check Claude Desktop logs**
3. **Try different server configuration**

## Tool-Specific Issues

### Browser-Tool Issues

#### Issue: Edge doesn't open or navigate

**Solutions:**
1. **Ensure Microsoft Edge is installed**
2. **Set Edge as default browser (temporary)**
3. **Use full URLs with protocol:**
   ```javascript
   // ✅ Correct
   "Open browser to 'https://google.com'"
   
   // ❌ May not work
   "Open browser to 'google.com'"
   ```

### State-Tool Issues

#### Issue: Screenshot capture fails

**Solutions:**
1. **Disable screenshot temporarily:**
   ```javascript
   "Get desktop state"  // Without screenshot
   ```

2. **Check screen permissions**
3. **Run as Administrator (one time)**

### Powershell-Tool Issues

#### Issue: PowerShell commands fail

**Solutions:**
1. **Check execution policy:**
   ```bash
   powershell -Command "Get-ExecutionPolicy"
   ```

2. **Use full PowerShell paths:**
   ```javascript
   "Run powershell 'Get-Process | Select-Object Name'"
   ```

## Diagnostic Commands

### System Diagnostics

```bash
# Check Python installation
python --version
python -c "import sys; print(sys.path)"

# Check UV installation
uv --version

# Check Node.js/npm
node --version
npm --version

# Check package installation
npm list -g darbot-windows-mcp
```

### Server Diagnostics

```bash
# Test server startup
darbot-windows-mcp --help

# Test with debugging
darbot-windows-mcp --verbose

# Test specific installation method
uv run python main.py --help
python main.py --help
```

### VS Code Diagnostics

```bash
# Check VS Code version
code --version

# List installed extensions
code --list-extensions | findstr mcp

# Open with debugging
code --verbose
```

## Getting Help

### Before Asking for Help

1. **Check this troubleshooting guide**
2. **Search existing GitHub issues**
3. **Test with minimal configuration**
4. **Gather system information**

### Information to Include

When reporting issues, include:

```
System Information:
- Windows version: [e.g., Windows 11 22H2]
- Python version: [python --version]
- Node.js version: [node --version]
- Installation method: [NPM/UV/Standard Python]
- VS Code version: [if applicable]

Error Details:
- Full error message
- Steps to reproduce
- Expected vs actual behavior
- Configuration files (sanitized)

Diagnostic Output:
- Output of: darbot-windows-mcp --help
- Output of: python --version
- Any relevant logs
```

### Where to Get Help

1. **GitHub Issues:** [https://github.com/darbotlabs/Darbot-Windows-MCP/issues](https://github.com/darbotlabs/Darbot-Windows-MCP/issues)
2. **Documentation:** [Installation Guide](INSTALLATION.md), [Tools Reference](TOOLS.md)
3. **Community Discussions:** GitHub Discussions tab

### Creating Good Bug Reports

1. **Use descriptive titles**
2. **Include system information**
3. **Provide step-by-step reproduction**
4. **Include error messages verbatim**
5. **Mention any workarounds found**

## Common Solutions Summary

### Quick Fixes

1. **Restart VS Code** after configuration changes
2. **Run as Administrator** for initial setup
3. **Clear caches** (npm, pip, VS Code)
4. **Update all components** (Python, Node.js, VS Code)
5. **Check file paths** in configuration files

### Environment Setup

1. **Add Python to PATH**
2. **Set npm prefix for user installs**
3. **Configure antivirus exclusions**
4. **Enable Windows UI Automation**
5. **Set PowerShell execution policy**

### Configuration Validation

1. **Validate JSON syntax**
2. **Check file locations**
3. **Verify server names match**
4. **Test server independently**
5. **Match installation method to configuration**

Most issues can be resolved by following the appropriate section in this guide. If you're still having problems, don't hesitate to create an issue on GitHub with detailed information.