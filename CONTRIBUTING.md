### 1. Update `manifest.json`
Change the name and description fields.

```json
{
  "name": "Darbot Windows MCP",
  "description": "Lightweight MCP Server that enables Claude to interact with Windows OS"
}
```

### 2. Update `README.md`
Change all instances of "Windows-MCP" to "Darbot Windows MCP". Here’s an updated excerpt:

```markdown
# 🪟 Darbot Windows MCP

**Darbot Windows MCP** is a lightweight, open-source project that enables seamless integration between AI agents and the Windows operating system. Acting as an MCP server bridges the gap between LLMs and the Windows operating system, allowing agents to perform tasks such as **file navigation, application control, UI interaction, QA testing,** and more.

## Updates

- **🆕 VS Code Agent Mode Support** - Darbot Windows MCP now fully supports VS Code's native MCP integration
- **🔧 Schema Validation Fixed** - Resolved all MCP JSON schema validation errors for seamless tool integration
- Try out [Windows-Use](https://github.com/CursorTouch/Windows-Use), the agent build using Darbot Windows MCP.
- Darbot Windows MCP is now featured in Claude Desktop.

### Supported Operating Systems

- Windows 7
- Windows 8, 8.1
- Windows 10
- Windows 11  

## 🏁 Getting Started

### VS Code Agent Mode

VS Code now has native MCP support through agent mode. Follow these steps to set up Darbot Windows MCP:

1. **Clone the repository:**
```shell
git clone https://github.com/CursorTouch/Darbot-Windows-MCP.git
cd Darbot-Windows-MCP
```

2. **Install dependencies:**
```shell
cd Darbot-Windows-MCP
uv sync
```

3. **Configure MCP in VS Code:**

Create or update `.vscode/mcp.json` in your workspace:
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

4. **Configure VS Code settings:**

Create or update `.vscode/settings.json`:
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

5. **Restart VS Code** and start using Darbot Windows MCP tools in agent mode! 🚀
```

### 3. Update `CHANGELOG.md`
Change all instances of "Windows-MCP" to "Darbot Windows MCP". Here’s an updated excerpt:

```markdown
## [v0.2.0] - 2025-07-22

### 🎉 Major Improvements

#### ✅ **Fixed MCP Schema Validation Issues**
- **Fixed JSON Schema Array Type Validation**: Resolved "tool parameters array type must have items" errors
- **Updated Parameter Types**: Replaced `tuple[int,int]` parameters with separate `x: int, y: int` parameters for better MCP compatibility
- **Fixed List Type Annotations**: Changed `list[str]` to `List[str]` with proper import

#### 🆕 **Darbot Windows MCP Integration**
- **Added MCP Configuration**: Created `.vscode/mcp.json` with proper server configuration
- **Updated VS Code Settings**: Fixed `.vscode/settings.json` to properly configure darbot-windows-mcp server
- **Full VS Code Agent Mode Support**: All tools now work seamlessly with VS Code's MCP integration
```

### 4. Update `CONTRIBUTING.md`
Change all instances of "Windows-MCP" to "Darbot Windows MCP". Here’s an updated excerpt:

```markdown
# Contributing to Darbot Windows MCP

Thank you for your interest in contributing to Darbot Windows MCP! This document provides guidelines and instructions for contributing to this project.
```

### 5. Update `mcp.json`
Change the server name from "windows-mcp" to "darbot-windows-mcp".

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

### 6. Update `settings.json`
Change the server name from "windows-mcp" to "darbot-windows-mcp".

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

### Summary of Changes
- **Renamed**: All instances of "Windows-MCP" to "Darbot Windows MCP".
- **Updated**: Configuration files and documentation to reflect the new name.
- **Ensured**: Consistency across all files.

After making these changes, ensure to test the application to confirm that everything is functioning correctly under the new name.