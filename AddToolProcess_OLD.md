## Process for Adding New Tools to Darbot Windows MCP

### 1. **Tool Planning & Design**
- **Identify the purpose**: Define what the tool should accomplish
- **Choose appropriate name**: Follow the naming convention `<Function>-Tool` (e.g., Browser-Tool, Launch-Tool)
- **Define parameters**: Determine required and optional parameters with proper types
- **Consider error handling**: Plan for potential failure scenarios

### 2. **Code Implementation**

#### A. **Add the Tool Function in main.py**
```python
@mcp.tool(name='Tool-Name', description='Clear description of what the tool does')
def tool_function(param1: type, param2: type = default) -> str:
    try:
        # Implementation logic
        # Use existing desktop methods or pyautogui functions
        # Handle success/failure cases
        return f'Success message with relevant details'
    except Exception as e:
        return f'Error message: {str(e)}'
```

#### B. **Key Implementation Guidelines**
- **Follow MCP decorator pattern**: Use `@mcp.tool(name='...', description='...')`
- **Use existing infrastructure**: Leverage `desktop` object methods when possible
- **Consistent return types**: Always return strings with status information
- **Proper error handling**: Use try-catch blocks for robust error management
- **Timing considerations**: Add appropriate `pg.sleep()` delays for UI interactions
- **Parameter validation**: Include type hints and handle optional parameters

### 3. **Documentation Updates**

#### A. **Update README.md Tools Table**
```markdown
| Tool | Purpose |
|------|---------|
| New-Tool | Description of what the new tool does. |
```

#### B. **Update Tool Count**
- Update the main description to reflect the new total number of tools
- Ensure consistency across all documentation

### 4. **Integration Steps I Followed**

#### **Step 1: Analyzed Existing Code Structure**
- Examined main.py to understand the MCP tool pattern
- Reviewed existing tools for consistency in implementation
- Studied the `Desktop` class methods in views.py

#### **Step 2: Implemented the Browser-Tool**
- Added the `@mcp.tool` decorator with proper name and description
- Used `desktop.launch_app("msedge")` to launch Edge browser
- Implemented URL navigation using keyboard shortcuts (`Ctrl+L`)
- Added proper timing with `pg.sleep()` for UI responsiveness
- Included comprehensive error handling

#### **Step 3: Updated Documentation**
- Added Browser-Tool to the tools table in README.md
- Updated tool count from 14 to 15 in the main description
- Maintained consistent formatting and style

#### **Step 4: Testing & Validation**
- Synchronized dependencies with `python -m uv sync`
- Started the MCP server in background mode
- Verified the server reported 15 tools (confirming successful integration)

### 5. **Best Practices Identified**

#### **Code Quality**
- **Consistent naming**: Follow `<Function>-Tool` pattern
- **Type safety**: Use proper type hints for all parameters
- **Error messages**: Provide clear, actionable error messages
- **Return consistency**: Always return descriptive strings

#### **Integration Considerations**
- **Leverage existing infrastructure**: Use `desktop` object methods when available
- **Timing sensitivity**: Add appropriate delays for Windows UI interactions
- **Keyboard shortcuts**: Use `pg.hotkey()` for efficient navigation
- **Status reporting**: Provide clear success/failure feedback

#### **Documentation Standards**
- **Update tools table**: Add new tool with clear description
- **Maintain accuracy**: Update tool counts and references
- **Follow formatting**: Maintain consistent markdown style

### 6. **Key Dependencies & Infrastructure**

#### **Required Imports**
- Core MCP functionality already imported
- Leverage existing `pyautogui`, `desktop`, and other utilities
- No additional imports needed for basic automation tasks

#### **Available Resources**
- `desktop` object with methods like `launch_app()`, `switch_app()`, `execute_command()`
- `pyautogui` for mouse/keyboard automation
- `pyperclip` for clipboard operations
- Windows UI Automation through `uiautomation`

### 7. **Verification Process**
1. **Code compilation**: Ensure no syntax errors
2. **Dependency sync**: Run `python -m uv sync`
3. **Server startup**: Verify MCP server starts successfully
4. **Tool count verification**: Confirm new tool appears in available tools
5. **Functional testing**: Test the tool's core functionality

### 8. **GitHub Copilot Agent Mode Considerations**

#### **Pre-requisites for Automated Tool Addition**
- Ensure MCP server is not running before making changes
- Have VS Code with GitHub Copilot agent mode enabled
- Working directory must be the Darbot-Windows-MCP folder

#### **Step-by-Step Commands for Copilot**
```bash
# 1. Stop any running MCP server
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *main.py*"

# 2. Make code changes (add tool to main.py)

# 3. Update documentation (README.md)

# 4. Sync dependencies
python -m uv sync

# 5. Run server for testing
python -m uv run main.py

# 6. Test the new tool functionality
```

### 9. **Common Tool Patterns & Templates**

#### **Navigation/Launch Tool Pattern**
```python
@mcp.tool(name='AppName-Tool', description='Launch and control specific application')
def appname_tool(parameter: str = None) -> str:
    try:
        launch_result, status = desktop.launch_app("appname")
        if status != 0:
            return f'Failed to launch AppName.'
        pg.sleep(2)  # Wait for app to load
        # Additional navigation logic
        return f'Successfully launched AppName'
    except Exception as e:
        return f'Error: {str(e)}'
```

#### **UI Interaction Tool Pattern**
```python
@mcp.tool(name='Action-Tool', description='Perform specific UI action')
def action_tool(x: int, y: int, parameter: str) -> str:
    try:
        pg.click(x, y)
        # Perform action
        control = desktop.get_element_under_cursor()
        return f'Performed action on {control.Name} at ({x},{y})'
    except Exception as e:
        return f'Error: {str(e)}'
```

### 10. **Testing Checklist for New Tools**

- [ ] **Syntax validation**: Code compiles without errors
- [ ] **Import verification**: All required imports are present
- [ ] **Parameter testing**: Test with all parameter combinations
- [ ] **Error handling**: Test failure scenarios
- [ ] **Return values**: Verify descriptive return messages
- [ ] **Documentation sync**: README reflects new tool
- [ ] **Tool count**: Total tool count is accurate
- [ ] **MCP compliance**: Tool follows MCP standards

### 11. **Debugging Tips**

#### **Common Issues & Solutions**
1. **Tool not appearing in MCP**:
   - Verify `@mcp.tool` decorator syntax
   - Check for Python syntax errors
   - Ensure function has proper return type hint

2. **Import errors**:
   - Already imported modules: `pyautogui as pg`, `uiautomation as ua`
   - Desktop object is pre-initialized
   - No additional imports needed for basic tasks

3. **Timing issues**:
   - Add `pg.sleep()` after UI actions
   - Use 2-3 seconds for app launches
   - Use 0.5-1 second for UI navigation

### 12. **Code Structure Reference**

#### **File Organization**
```
Darbot-Windows-MCP/
├── main.py          # All MCP tools defined here
├── src/desktop/views.py  # Desktop class implementation
├── README.md        # Documentation with tools table
├── pyproject.toml   # Dependencies
└── .vscode/         # VS Code MCP configuration
```

#### **Key Objects Available**
- `desktop`: Instance of Desktop class from src.desktop
- `pg`: pyautogui for mouse/keyboard automation
- `ua`: uiautomation for Windows UI interaction
- `mcp`: MCP server instance for tool registration

### 13. **Git Workflow for Tool Addition**

```bash
# 1. Create feature branch
git checkout -b add-toolname-tool

# 2. Make changes
# - Add tool to main.py
# - Update README.md

# 3. Test thoroughly
python -m uv sync
python -m uv run main.py

# 4. Commit changes
git add main.py README.md
git commit -m "Add ToolName-Tool for [purpose]"

# 5. Push and create PR
git push origin add-toolname-tool
```

### 14. **Validation Script Template**

```python
# Quick test script for new tool
def test_new_tool():
    """Test the newly added tool"""
    try:
        # Import and run the tool
        result = tool_name(test_parameters)
        print(f"Test passed: {result}")
    except Exception as e:
        print(f"Test failed: {e}")
```

### 15. **Documentation Template for New Tools**

When adding to README.md:
```markdown
| ToolName-Tool | Brief description of what the tool does and when to use it. |
```

Ensure descriptions are:
- Concise but complete
- Action-oriented
- Include key parameters mentioned
- Consistent with existing style

This comprehensive approach ensures new tools integrate seamlessly with the existing Darbot Windows MCP framework while maintaining code quality, documentation accuracy, and consistent user experience. The additional sections provide specific guidance for GitHub Copilot agent mode automation and common development patterns.