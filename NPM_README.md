# Darbot Windows MCP - NPM Package

This directory contains the npm package that bundles everything needed to install and configure Darbot Windows MCP.

## What's Included

- **Python MCP Server** - The complete [`main.py`](main.py ) and `src/` directory
- **Dependencies** - Both `requirements.txt` and `pyproject.toml` for different installation methods
- **Setup Scripts** - Automated installation and configuration for VS Code and Claude Desktop
- **CLI Tools** - `darbot-windows-mcp` and `darbot-setup` commands

## Installation Methods Supported

1. **UV (Recommended)** - Modern, fast Python dependency management
2. **Standard Python** - Traditional pip + venv workflow

## Commands Available After Installation

```shell
darbot-windows-mcp          # Start the MCP server
darbot-windows-mcp --help   # Show help information
darbot-setup                # Run the interactive setup wizard
```

## Publishing to NPM

```shell
# Test locally first
npm pack
npm install -g darbot-windows-mcp-0.1.69.tgz

# Publish to NPM
npm login
npm publish
```

## Package Structure

```
bin/
  darbot-windows-mcp.js     # Main server launcher
  setup.js                 # Interactive setup wizard
scripts/
  install.js               # Pre-install checks
  postinstall.js           # Post-install instructions
  test.js                  # Installation testing
templates/                 # VS Code and Claude config templates
main.py                    # Python MCP server
src/                       # Python source code
requirements.txt           # Python dependencies
package.json               # NPM package configuration
```
