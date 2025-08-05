# 👨‍💻 Development Guide - Darbot Windows MCP

<div align="center">
  <img src="assets/logo.png" alt="Darbot Windows MCP Logo" width="64" height="64">
  <h2>👨‍💻 Development Guide</h2>
</div>

This comprehensive guide covers development setup, adding new tools, contributing code, and understanding the project architecture.

## 📋 Table of Contents

- [Development Environment Setup](#development-environment-setup)
- [Project Architecture](#project-architecture)
- [Adding New Tools](#adding-new-tools)
- [Testing and Validation](#testing-and-validation)
- [Code Standards](#code-standards)
- [Debugging and Troubleshooting](#debugging-and-troubleshooting)
- [Release Process](#release-process)

## Development Environment Setup

### Prerequisites

- **Windows 11** (Windows 10 may work but is not officially supported)
- **Python 3.13+** with pip
- **Node.js 16+** with npm
- **Git** for version control
- **VS Code** (recommended) with MCP extension

### Initial Setup

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/yourusername/Darbot-Windows-MCP.git
   cd Darbot-Windows-MCP
   ```

2. **Choose your development method:**

   **Option A: UV (Recommended for development)**
   ```bash
   # Install UV
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # Install dependencies
   uv sync
   
   # Run server for testing
   uv run python main.py
   ```

   **Option B: Standard Python**
   ```bash
   # Create virtual environment
   python -m venv venv
   venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Run server for testing
   python main.py
   ```

3. **Set up VS Code for development:**
   
   Create `.vscode/mcp.json`:
   ```json
   {
     "servers": {
       "darbot-windows-mcp": {
         "type": "stdio",
         "command": "uv",
         "args": [
           "--directory",
           "${workspaceFolder}",
           "run",
           "main.py"
         ]
       }
     },
     "inputs": []
   }
   ```

   Create `.vscode/settings.json`:
   ```json
   {
     "mcp.servers": {
       "darbot-windows-mcp": {
         "command": "uv",
         "args": [
           "--directory",
           "${workspaceFolder}",
           "run",
           "main.py"
         ],
         "env": {}
       }
     }
   }
   ```

## Project Architecture

### File Structure

```
Darbot-Windows-MCP/
├── main.py                 # Main MCP server with all tools
├── src/                    # Source code directory
│   └── desktop/            # Desktop automation modules
│       ├── __init__.py
│       └── views.py        # Desktop class implementation
├── bin/                    # NPM package executables
│   ├── darbot-windows-mcp.js
│   └── setup.js
├── scripts/                # NPM package scripts
│   ├── install.js
│   ├── postinstall.js
│   └── test.js
├── templates/              # Configuration templates
│   ├── mcp.json.template
│   ├── settings.json.template
│   └── claude_desktop_config.json.template
├── assets/                 # Images and branding
├── docs/                   # Documentation files
├── package.json            # NPM package configuration
├── pyproject.toml          # Python project configuration
├── requirements.txt        # Python dependencies
└── README.md               # Main documentation
```

### Key Components

#### main.py
The heart of the MCP server containing:
- All 15 tool definitions with `@mcp.tool` decorators
- MCP server setup and configuration
- Tool implementations using desktop automation

#### src/desktop/views.py
Contains the `Desktop` class with methods for:
- Application launching (`launch_app`)
- Window management (`switch_app`)
- UI element interaction
- System information gathering

#### Tool Architecture
Each tool follows this pattern:
```python
@mcp.tool(name='Tool-Name', description='Clear description')
def tool_function(param1: type, param2: type = default) -> str:
    try:
        # Implementation logic
        return f'Success message with details'
    except Exception as e:
        return f'Error: {str(e)}'
```

## Adding New Tools

### Process Overview

1. **Plan the tool** - Define purpose, parameters, and behavior
2. **Implement the tool** - Add function to main.py
3. **Update documentation** - Add to README and TOOLS.md
4. **Test thoroughly** - Validate functionality
5. **Submit PR** - Follow contribution guidelines

### Step-by-Step Tool Addition

#### 1. Tool Planning & Design

- **Identify purpose**: What specific task should the tool accomplish?
- **Choose name**: Follow `<Function>-Tool` pattern (e.g., `Email-Tool`, `Window-Tool`)
- **Define parameters**: What inputs does the tool need?
- **Consider error cases**: How should failures be handled?

#### 2. Implementation

Add your tool to `main.py`:

```python
@mcp.tool(name='NewTool-Tool', description='Description of what the tool does')
def new_tool_function(param1: str, param2: int = 100) -> str:
    """
    Tool implementation with proper error handling.
    
    Args:
        param1: Description of parameter
        param2: Optional parameter with default
        
    Returns:
        Success/error message string
    """
    try:
        # Use existing infrastructure when possible
        # Leverage desktop object methods
        # Handle timing with pg.sleep() if needed
        
        result = desktop.some_method(param1)
        pg.sleep(0.5)  # Allow UI to respond
        
        return f'Successfully completed operation: {result}'
        
    except Exception as e:
        return f'NewTool-Tool error: {str(e)}'
```

#### 3. Key Implementation Guidelines

**Follow MCP Standards:**
- Use `@mcp.tool(name='...', description='...')` decorator
- Always return strings with status information
- Include comprehensive error handling
- Use proper type hints

**Leverage Existing Infrastructure:**
- Use `desktop` object methods when available
- Utilize `pyautogui` as `pg` for mouse/keyboard operations
- Use `uiautomation` as `ua` for Windows UI interaction

**Timing Considerations:**
- Add `pg.sleep()` delays for UI interactions
- Use 2-3 seconds for application launches
- Use 0.5-1 seconds for UI navigation

**Parameter Validation:**
- Include type hints for all parameters
- Handle optional parameters with defaults
- Validate input ranges where appropriate

#### 4. Documentation Updates

**Update README.md tools table:**
```markdown
| NewTool-Tool | Brief description of what the tool does. |
```

**Update tool count in descriptions:**
- Change "15 tools" to "16 tools" throughout documentation

**Add to TOOLS.md:**
- Complete tool documentation with examples
- Usage patterns and best practices
- AI agent interaction examples

#### 5. Example Tool Implementation

Here's a complete example of adding a new tool:

```python
@mcp.tool(name='Window-Resize-Tool', description='Resize a window to specific dimensions')
def window_resize_tool(window_name: str, width: int, height: int) -> str:
    """
    Resize a specific window to given dimensions.
    
    Args:
        window_name: Name of the window to resize
        width: New width in pixels
        height: New height in pixels
        
    Returns:
        Success or error message
    """
    try:
        # Find and focus the window
        import uiautomation as ua
        
        # Find window by name
        window = ua.WindowControl(searchDepth=1, Name=window_name)
        if not window.Exists(0):
            return f'Window "{window_name}" not found'
        
        # Set window to foreground
        window.SetActive()
        pg.sleep(0.5)
        
        # Resize window
        window.Resize(width, height)
        pg.sleep(0.5)
        
        # Verify resize
        rect = window.BoundingRectangle
        actual_width = rect.right - rect.left
        actual_height = rect.bottom - rect.top
        
        return f'Resized "{window_name}" to {actual_width}x{actual_height}'
        
    except Exception as e:
        return f'Window-Resize-Tool error: {str(e)}'
```

### Common Tool Patterns

#### Application Launch Pattern
```python
@mcp.tool(name='App-Tool', description='Launch specific application')
def app_tool(parameter: str = None) -> str:
    try:
        launch_result, status = desktop.launch_app("appname")
        if status != 0:
            return f'Failed to launch application'
        pg.sleep(2)  # Wait for app to load
        # Additional logic here
        return f'Successfully launched application'
    except Exception as e:
        return f'App-Tool error: {str(e)}'
```

#### UI Interaction Pattern
```python
@mcp.tool(name='Action-Tool', description='Perform UI action')
def action_tool(x: int, y: int, text: str) -> str:
    try:
        pg.click(x, y)
        pg.sleep(0.5)
        pg.typewrite(text)
        return f'Performed action at ({x},{y}) with text: {text}'
    except Exception as e:
        return f'Action-Tool error: {str(e)}'
```

#### System Query Pattern
```python
@mcp.tool(name='Query-Tool', description='Query system information')
def query_tool(query_type: str) -> str:
    try:
        if query_type == "processes":
            result, _ = desktop.execute_command("Get-Process")
        elif query_type == "services":
            result, _ = desktop.execute_command("Get-Service")
        else:
            return f'Unknown query type: {query_type}'
        
        return f'Query result: {result[:500]}...'  # Truncate long results
    except Exception as e:
        return f'Query-Tool error: {str(e)}'
```

## Testing and Validation

### Development Testing

1. **Syntax Validation:**
   ```bash
   # Check for syntax errors
   python -m py_compile main.py
   ```

2. **Dependency Check:**
   ```bash
   # With UV
   uv sync
   
   # With pip
   pip install -r requirements.txt
   ```

3. **Server Startup Test:**
   ```bash
   # Test server starts successfully
   uv run python main.py --help
   # Should show server info and tool count
   ```

### Functional Testing

1. **Tool Registration:**
   ```bash
   # Start server and verify tool count
   uv run python main.py
   # Look for "Server running with X tools available"
   ```

2. **VS Code Integration:**
   - Restart VS Code after changes
   - Test tool in agent mode
   - Verify expected behavior

3. **Individual Tool Testing:**
   ```python
   # Quick test script
   def test_new_tool():
       try:
           result = new_tool_function("test_param", 50)
           print(f"Test passed: {result}")
       except Exception as e:
           print(f"Test failed: {e}")
   ```

### Testing Checklist

- [ ] **Syntax validation**: Code compiles without errors
- [ ] **Import verification**: All required imports are present
- [ ] **Parameter testing**: Test with various parameter combinations
- [ ] **Error handling**: Test failure scenarios
- [ ] **Return values**: Verify descriptive return messages
- [ ] **Documentation sync**: All docs reflect new functionality
- [ ] **Tool count**: Total tool count is accurate everywhere
- [ ] **MCP compliance**: Tool follows MCP standards

## Code Standards

### Python Code Style

**Follow PEP 8 standards:**
- 4 spaces for indentation
- Line length limit of 88 characters
- Meaningful variable names
- Comprehensive docstrings

**Type Hints:**
```python
def tool_function(param1: str, param2: int = 100) -> str:
    """Function with proper type hints."""
    pass
```

**Error Handling:**
```python
try:
    # Main logic
    result = some_operation()
    return f'Success: {result}'
except SpecificException as e:
    return f'Specific error: {str(e)}'
except Exception as e:
    return f'General error: {str(e)}'
```

### Documentation Standards

**Tool Descriptions:**
- Clear, action-oriented descriptions
- Mention key parameters
- Consistent with existing style

**Code Comments:**
- Comment complex logic
- Explain timing requirements
- Document UI automation assumptions

**Commit Messages:**
```
Add NewTool-Tool for specific functionality

- Implements parameter validation
- Includes comprehensive error handling  
- Updates documentation and tool count
- Tested with VS Code agent mode
```

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

## Debugging and Troubleshooting

### Common Development Issues

#### Tool Not Appearing in MCP
1. **Check decorator syntax:**
   ```python
   @mcp.tool(name='Tool-Name', description='Description')
   ```

2. **Verify function signature:**
   ```python
   def tool_function(...) -> str:  # Must return str
   ```

3. **Look for Python syntax errors:**
   ```bash
   python -m py_compile main.py
   ```

#### Import Errors
- Most required modules are already imported in main.py
- `desktop` object is pre-initialized
- Use existing imports: `pg` (pyautogui), `ua` (uiautomation)

#### Timing Issues
- Add appropriate `pg.sleep()` delays
- UI operations need time to complete
- Test on different system speeds

### Debugging Tools

**Server Logging:**
```python
# Add debugging output
print(f"Debug: Tool called with parameters: {param1}, {param2}")
```

**VS Code Debugging:**
- Set breakpoints in main.py
- Use VS Code debugger with MCP server
- Check VS Code Developer Console for MCP errors

**Command Line Testing:**
```bash
# Test individual components
python -c "from src.desktop import Desktop; d = Desktop(); print(d.get_active_window())"
```

### Performance Optimization

**Efficient UI Operations:**
- Cache UI element references when possible
- Use direct coordinates instead of element searching
- Minimize sleep delays while maintaining reliability

**Memory Management:**
- Avoid holding large objects in memory
- Clean up resources after operations
- Monitor memory usage during development

## Release Process

### Pre-Release Checklist

- [ ] All tests pass
- [ ] Documentation is updated
- [ ] Version numbers are consistent
- [ ] No breaking changes (or properly documented)
- [ ] Performance benchmarks are acceptable

### Version Management

**Update version in:**
- `package.json`
- `pyproject.toml`
- Release documentation

**Version Numbering:**
- Major: Breaking changes
- Minor: New features, backward compatible
- Patch: Bug fixes, improvements

### NPM Package Release

```bash
# Test package locally
npm pack
npm install -g darbot-windows-mcp-X.X.X.tgz

# Publish to NPM
npm login
npm publish
```

### GitHub Release

1. Create release branch
2. Update CHANGELOG.md
3. Tag version: `git tag v1.0.0`
4. Push tag: `git push origin v1.0.0`
5. Create GitHub release with changelog

## Advanced Development Topics

### Custom Desktop Methods

Add new methods to `src/desktop/views.py`:

```python
class Desktop:
    def custom_operation(self, param1: str) -> tuple[str, int]:
        """
        Custom desktop operation.
        
        Returns:
            Tuple of (result_string, status_code)
        """
        try:
            # Implementation
            return ("Success", 0)
        except Exception as e:
            return (f"Error: {e}", 1)
```

### UI Automation Patterns

**Finding Elements:**
```python
import uiautomation as ua

# Find by name
element = ua.FindControl(Name="Button Name")

# Find by automation ID
element = ua.FindControl(AutomationId="button1") 

# Find by class name
element = ua.FindControl(ClassName="Button")
```

**Element Interaction:**
```python
# Click element
element.Click()

# Get element text
text = element.Name

# Check if element exists
if element.Exists(timeout=5):
    element.Click()
```

### Error Handling Strategies

**Graceful Degradation:**
```python
def robust_tool(param: str) -> str:
    try:
        # Primary method
        return primary_method(param)
    except PrimaryException:
        try:
            # Fallback method
            return fallback_method(param)
        except Exception as e:
            return f"All methods failed: {e}"
```

**Resource Cleanup:**
```python
def resource_tool(param: str) -> str:
    resource = None
    try:
        resource = acquire_resource()
        result = use_resource(resource, param)
        return f"Success: {result}"
    except Exception as e:
        return f"Error: {e}"
    finally:
        if resource:
            release_resource(resource)
```

This development guide provides everything needed to contribute effectively to Darbot Windows MCP. Follow these patterns and practices to maintain code quality and consistency across the project.

For contribution guidelines and pull request process, see [CONTRIBUTING.md](CONTRIBUTING.md).
For installation and setup help, see [INSTALLATION.md](INSTALLATION.md).
For troubleshooting development issues, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).