# GitHub Copilot Instructions for Darbot Windows MCP

This document provides guidance for GitHub Copilot when working with the Darbot Windows MCP project.

## Project Overview

Darbot Windows MCP is a Model Context Protocol (MCP) server that enables AI agents to control Windows desktops programmatically. The project provides 15 automation tools for tasks like launching applications, clicking, typing, scrolling, and managing UI state.

## Technology Stack

- **Python 3.13+**: Core MCP server implementation
- **Node.js 16+**: NPM packaging and setup scripts
- **FastMCP**: MCP server framework
- **PyAutoGUI**: Mouse and keyboard automation
- **UIAutomation**: Windows UI element interaction
- **Windows 11**: Primary supported platform

## Project Structure

```
Darbot-Windows-MCP/
├── main.py                 # Main MCP server with all 15 tools
├── src/desktop/           # Desktop automation modules
│   ├── __init__.py
│   └── views.py           # Desktop class implementation
├── bin/                   # NPM package executables
│   ├── darbot-windows-mcp.js
│   └── setup.js
├── scripts/               # NPM package scripts
│   ├── install.js
│   ├── postinstall.js
│   └── test.js
├── templates/             # Configuration templates
├── package.json           # NPM package configuration
├── pyproject.toml         # Python project (UV) configuration
└── requirements.txt       # Python dependencies
```

## Coding Conventions

### Python Code Style

- Follow PEP 8 standards
- Use 4 spaces for indentation
- Line length limit: 88 characters
- Always include type hints for function parameters and return values
- Use comprehensive docstrings for functions

### MCP Tool Pattern

All tools follow this standard pattern:

```python
@mcp.tool(name='Tool-Name', description='Clear description of what the tool does')
def tool_function(param1: type, param2: type = default) -> str:
    """
    Detailed description of the tool.
    
    Args:
        param1: Description of parameter
        param2: Optional parameter with default value
        
    Returns:
        Success or error message string
    """
    try:
        # Implementation logic here
        result = desktop.some_method(param1)
        pg.sleep(0.5)  # Allow UI to respond
        return f'Success message with details: {result}'
    except Exception as e:
        return f'Tool-Name error: {str(e)}'
```

### Key Implementation Guidelines

1. **Tool Names**: Follow `<Function>-Tool` pattern (e.g., `Launch-Tool`, `Click-Tool`)
2. **Return Values**: Always return descriptive strings, never raise exceptions
3. **Error Handling**: Wrap all tool logic in try-except blocks
4. **Timing**: Add `pg.sleep()` delays for UI operations:
   - 2-3 seconds for application launches
   - 0.5-1 seconds for UI interactions
5. **Global Objects**: Use pre-initialized objects:
   - `desktop`: Desktop class instance for system operations
   - `pg`: PyAutoGUI for mouse/keyboard (imported as `import pyautogui as pg`)
   - `ua`: UIAutomation for Windows UI (imported as `import uiautomation as ua`)

### Import Organization

```python
# Standard library imports
import sys
import time
from typing import List, Optional

# Third-party imports
import pyautogui as pg
import uiautomation as ua

# Local imports
from src.desktop import Desktop
```

## Development Workflow

### Running the Server

```bash
# With UV (recommended)
uv run python main.py

# With standard Python
python main.py
```

### Testing

```bash
# NPM test script
npm test

# Manual Python syntax check
python -m py_compile main.py

# Test server startup
uv run python main.py --help
```

### Common Development Tasks

1. **Adding a new tool**:
   - Add function with `@mcp.tool()` decorator to `main.py`
   - Follow the standard tool pattern above
   - Update tool count in documentation (README.md, etc.)
   - Add to TOOLS.md with examples

2. **Modifying desktop operations**:
   - Edit `src/desktop/views.py`
   - Methods return `tuple[str, int]` (result, status_code)
   - Status 0 = success, non-zero = error

3. **Updating documentation**:
   - README.md: Project overview and quick start
   - INSTALLATION.md: Setup instructions
   - TOOLS.md: Tool documentation
   - DEVELOPMENT.md: Development guide
   - TROUBLESHOOTING.md: Common issues

## Important Considerations

### Windows-Specific Behavior

- All paths should use Windows conventions
- UI Automation requires English Windows locale for consistency
- Screen coordinates are DPI-aware (handled by `ctypes.windll.user32.SetProcessDPIAware()`)
- Always test on Windows 11

### Performance

- Typical end-to-end latency: 1.5-2.3 seconds per action
- UI operations need time to complete
- Don't over-optimize sleep delays at the expense of reliability

### Error Messages

- Be descriptive and include context
- Include the tool name in error messages
- Return user-friendly messages, not raw exceptions

### Breaking Changes

- Avoid changing existing tool signatures
- Maintain backward compatibility with MCP clients
- Document any breaking changes clearly

## Available Tools (15 total)

1. **Launch-Tool**: Launch applications from Start menu
2. **Browser-Tool**: Launch Edge and navigate to URLs
3. **Powershell-Tool**: Run PowerShell commands
4. **State-Tool**: Get active app, open apps, UI elements, optional screenshot
5. **Clipboard-Tool**: Copy/paste clipboard contents
6. **Click-Tool**: Click at coordinates
7. **Type-Tool**: Type text into UI
8. **Switch-Tool**: Bring window to foreground
9. **Scroll-Tool**: Vertical/horizontal scrolling
10. **Drag-Tool**: Drag from one point to another
11. **Move-Tool**: Move mouse cursor
12. **Shortcut-Tool**: Send keyboard shortcuts
13. **Key-Tool**: Press single keys
14. **Wait-Tool**: Sleep for specified seconds
15. **Scrape-Tool**: Fetch webpage and return as Markdown

## Common Patterns

### Application Launch Pattern
```python
launch_result, status = desktop.launch_app("appname")
if status != 0:
    return f'Failed to launch application'
pg.sleep(2)  # Wait for app to load
```

### UI Interaction Pattern
```python
pg.click(x, y)
pg.sleep(0.5)
pg.typewrite(text)
return f'Performed action at ({x},{y})'
```

### System Query Pattern
```python
result, status = desktop.execute_command("Get-Process")
if status != 0:
    return f'Command failed'
return f'Query result: {result[:500]}...'
```

## Dependencies

### Python Dependencies (requirements.txt)
- fastmcp: MCP server framework
- pyautogui: Mouse/keyboard automation
- uiautomation: Windows UI interaction
- markdownify: HTML to Markdown conversion
- pyperclip: Clipboard operations

### NPM Dependencies (package.json)
- chalk: Terminal colors
- inquirer: Interactive CLI prompts
- ora: Terminal spinners
- fs-extra: Enhanced file operations

## Testing Checklist for New Tools

- [ ] Syntax validation: `python -m py_compile main.py`
- [ ] Import verification: All required imports present
- [ ] Parameter testing: Test with various parameter combinations
- [ ] Error handling: Test failure scenarios
- [ ] Return values: Verify descriptive return messages
- [ ] Documentation sync: Update all relevant docs
- [ ] Tool count: Update total tool count everywhere
- [ ] MCP compliance: Tool follows MCP standards

## Resources

- [Model Context Protocol Specification](https://spec.modelcontextprotocol.io/)
- [PyAutoGUI Documentation](https://pyautogui.readthedocs.io/)
- [Windows UI Automation](https://docs.microsoft.com/en-us/windows/win32/winauto/entry-uiauto-win32)

## Additional Documentation

- DEVELOPMENT.md: Comprehensive development guide
- CONTRIBUTING.md: Contribution guidelines
- TOOLS.md: Complete tool documentation with examples
- TROUBLESHOOTING.md: Common issues and solutions
