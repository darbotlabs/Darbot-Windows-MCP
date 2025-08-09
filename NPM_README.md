# Darbot Windows MCP - NPM Package

<div align="center">
  <img src="assets/logo.png" alt="Darbot Windows MCP Logo" width="64" height="64">
  <h2>🪟 Darbot Windows MCP</h2>
  <p><strong>Professional Windows Desktop Automation for AI Agents</strong></p>
</div>

This directory contains the npm package that bundles everything needed to install and configure Darbot Windows MCP.

## What's Included

- **Python MCP Server** - The complete [`main.py`](main.py ) and `src/` directory
- **Dependencies** - Both `requirements.txt` and `pyproject.toml` for different installation methods
- **Setup Scripts** - Automated installation and configuration for VS Code and Claude Desktop
- **CLI Tools** - `darbot-windows-mcp` and `darbot-setup` commands

## Installation Methods Supported

1. **UV (Recommended)** - Modern, fast Python dependency management
2. **Standard Python** - Traditional pip + venv workflow

## Refined Installation Process

The npm package now supports seamless installation through VSCode MCP UI:

### Phase 1: NPM Package Installation
```shell
npm install @darbotlabs/darbot-windows-mcp
```
- ✅ Installs npm package successfully (no longer requires pre-installed Python)
- ✅ Provides clear post-installation guidance
- ✅ Compatible with VSCode MCP server UI installation

### Phase 2: Dependency Setup
```shell
darbot-setup
```
- Checks and guides Python 3.12+ installation if needed
- Installs Python dependencies (UV or pip+venv)
- Configures VSCode and Claude Desktop integration
- Provides helpful troubleshooting

## Commands Available After Installation

```shell
darbot-windows-mcp          # Start the MCP server
darbot-windows-mcp --help   # Show help information
darbot-setup                # Run the interactive setup wizard
npm run install-deps       # Check Python and provide guidance
```

## VSCode MCP Integration

After npm installation, configure in VSCode:

1. Open VSCode settings (Ctrl+,)
2. Search for "MCP" and add a new server
3. Server name: `darbot-windows-mcp`
4. Command: `darbot-windows-mcp`
5. Run `darbot-setup` to complete dependency installation

## Publishing to NPM

```shell
# Test locally first
npm pack
npm install -g darbot-windows-mcp

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
  install.js               # Non-blocking dependency checks (moved from install to install-deps)
  postinstall.js           # Post-install instructions (enhanced for VSCode)
  test.js                  # Installation testing
templates/                 # VS Code and Claude config templates
main.py                    # Python MCP server
src/                       # Python source code
requirements.txt           # Python dependencies
package.json               # NPM package configuration
```
