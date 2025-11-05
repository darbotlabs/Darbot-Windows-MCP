# 🚨 Troubleshooting Guide - Darbot-Windows-MCP

## Quick Fixes

### Installation Issues

#### "UV not found" error
```bash
# Install UV package manager
pip install uv

# Or use the setup wizard
python setup_wizard.py
```

#### Import errors on non-Windows systems
This is expected behavior. The MCP server detects your platform and runs in limited mode:
```
⚠️  Warning: Darbot-Windows-MCP is designed for Windows. Running on Linux may have limited functionality.
```

#### Python version warnings
```bash
# Check your Python version
python --version

# Install Python 3.13+ for best performance
# Or continue with Python 3.8+ (minimum required)
```

### Configuration Issues

#### Claude Desktop not detecting MCP server
1. Check config file location:
   - **Windows**: `%USERPROFILE%\AppData\Roaming\Claude\claude_desktop_config.json`
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`  
   - **Linux**: `~/.config/Claude/claude_desktop_config.json`

2. Verify configuration format:
```json
{
  "mcpServers": {
    "darbot-windows-mcp": {
      "command": "uv",
      "args": [
        "--directory", 
        "/full/path/to/Darbot-Windows-MCP",
        "run",
        "main.py"
      ]
    }
  }
}
```

3. Restart Claude Desktop completely

#### Gemini CLI issues
1. Check settings location: `~/.gemini/settings.json`
2. Ensure proper JSON formatting
3. Restart Gemini CLI

### Runtime Issues

#### Tools returning "This tool requires Windows"
Expected on non-Windows systems. Tools will gracefully degrade:
- Most UI interaction tools will not function
- Web scraping and basic utilities still work
- Wait-Tool works on all platforms

#### Permission denied errors (Windows)
1. Run as administrator if needed
2. Check Windows UAC settings  
3. Verify application has screen access permissions

#### "No interactive elements found"
1. Ensure applications are visible and not minimized
2. Check if running on correct display in multi-monitor setup
3. Try refreshing desktop state

## Detailed Diagnostics

### Environment Check
```bash
# Run comprehensive system check
python setup_wizard.py

# Test basic functionality
python test_bug_bash.py
```

### Server Diagnostics
```bash
# Test server startup
uv run python main.py

# Check for import issues
uv run python -c "from main import mcp; print('Server OK')"
```

### Tool Testing
Individual tool testing is only available on Windows with proper setup.

## Common Error Messages

| Error | Cause | Solution |
|-------|--------|----------|
| `RuntimeError: Could not find libmono` | Non-Windows system trying to load .NET dependencies | Expected - use mock mode |
| `ModuleNotFoundError: No module named 'uiautomation'` | Missing Windows-specific dependencies | Install on Windows or use limited mode |
| `FileNotFoundError: [Errno 2] No such file or directory: 'powershell'` | PowerShell not available | Expected on non-Windows systems |
| `ValueError: Functions with *args are not supported` | Decorator issue with FastMCP | Fixed in current version |

## Performance Issues

### Slow tool responses
1. Check system performance and memory usage
2. Close unnecessary applications
3. Reduce thread pool usage in complex UI traversals

### High CPU usage
1. Limit vision processing (`use_vision=False`)
2. Increase delays between actions
3. Check for excessive UI element scanning

## Security Considerations

### Permissions Required (Windows)
- **Screen Capture**: For screenshot functionality
- **Input Simulation**: For click/type operations  
- **Application Access**: For launching and switching apps
- **PowerShell Execution**: For system commands

### Firewall/Antivirus Issues
Some security software may flag:
- Python executables making system calls
- Screen capture functionality
- Input simulation

**Solutions:**
1. Add exceptions for Python/UV/project directory
2. Run from trusted directories
3. Use allowlist for specific tools only

## Development/Debug Mode

### Enable Detailed Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Debug UI Element Detection
Use the State-Tool with vision enabled to see what elements are detected:
```python
# Through MCP client
state_tool(use_vision=True)
```

### Mock Mode Testing
The server automatically enters mock mode on non-Windows systems for testing.

## Getting Help

### Before Reporting Issues
1. Run setup wizard: `python setup_wizard.py`
2. Check this troubleshooting guide
3. Verify you're on a supported platform
4. Test with minimal configuration

### Information to Include
- Operating system and version
- Python version (`python --version`)
- UV version (`uv --version`)
- Full error messages
- Configuration files
- Steps to reproduce

### Support Channels
- **GitHub Issues**: https://github.com/darbotlabs/Darbot-Windows-MCP/issues
- **Discord**: https://discord.gg/darbotlabs
- **Documentation**: README.md and bug_bash_results.md

## Advanced Configuration

### Custom Tool Filtering
Modify the decorator to disable specific tools:
```python
def ensure_windows_available(func, disabled_on_non_windows=True):
    # Custom implementation
```

### Performance Tuning
```python
# Adjust these settings in config files
THREAD_POOL_SIZE = 4
UI_SCAN_TIMEOUT = 5
SCREENSHOT_SCALE = 0.7
```

### Integration with Other Tools
The MCP server can be integrated with:
- Docker containers (Linux base images)
- CI/CD pipelines (testing/validation)
- Other Python automation frameworks