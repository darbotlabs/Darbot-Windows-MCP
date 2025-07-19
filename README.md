<div align="center">

  <h1>🪟 Darbot-Windows-MCP</h1>

  <a href="https://github.com/darbotlabs/Darbot-Windows-MCP/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
  </a>
  <img src="https://img.shields.io/badge/python-3.13%2B-blue" alt="Python">
  <img src="https://img.shields.io/badge/platform-Windows%207–11-blue" alt="Platform: Windows 7 to 11">
  <img src="https://img.shields.io/github/last-commit/darbotlabs/Darbot-Windows-MCP" alt="Last Commit">
  <br>
  <a href="https://discord.gg/darbotlabs">
    <img src="https://img.shields.io/badge/Join%20on-Discord-5865F2?logo=discord&logoColor=white&style=flat" alt="Join us on Discord">
  </a>

</div>

<br>

**Darbot-Windows MCP** is a lightweight, open-source project that enables seamless integration between AI agents and the Windows operating system. Acting as an MCP server bridges the gap between LLMs and the Windows operating system, allowing agents to perform tasks such as **file navigation, application control, UI interaction, QA testing,** and more.

## 🎥 Demos

<https://github.com/user-attachments/assets/d0e7ed1d-6189-4de6-838a-5ef8e1cad54e>

<https://github.com/user-attachments/assets/d2b372dc-8d00-4d71-9677-4c64f5987485>

## ✨ Key Features

- **Seamless Windows Integration**  
  Interacts natively with Windows UI elements, opens apps, controls windows, simulates user input, and more.

- **Use Any LLM (Vision Optional)**
   Unlike many automation tools, Darbot-Windows MCP doesn't rely on any traditional computer vision techniques or specific fine-tuned models; it works with any LLMs, reducing complexity and setup time.

- **Rich Toolset for UI Automation**  
  Includes tools for basic keyboard, mouse operation and capturing window/UI state.

- **Lightweight & Open-Source**  
  Minimal dependencies and easy setup with full source code available under MIT license.

- **Customizable & Extendable**  
  Easily adapt or extend tools to suit your unique automation or AI integration needs.

- **Real-Time Interaction**  
  Typical latency between actions (e.g., from one mouse click to the next) ranges from **1.5 to 2.3 secs**, and may slightly vary based on the number of active applications and system load, also the inferencing speed of the llm.

### Supported Operating Systems

- Windows 7
- Windows 8, 8.1
- Windows 10
- Windows 11  

## Installation

### Prerequisites

- Python 3.13+
- Anthropic Claude Desktop app or other MCP Clients
- UV (Package Manager) from Astral, install with `pip install uv`
- DXT (Desktop Extension) from Antropic, install with `npm install -g @anthropic-ai/dxt`
- Set `English` as the default language in Windows

### NPM Installation (Recommended)

```bash
npm install @darbotlabs/darbot-windows-mcp
```

### Manual Installation

1. Clone the repository
2. Install UV package manager
3. Run `uv sync` to install dependencies

## 🏁 Getting Started

### Gemini CLI

1. Navigate to `%USERPROFILE%/.gemini` in File Explorer and open `settings.json`.

2. Add the `darbot-windows-mcp` config in the `settings.json` and save it.

```json
{
  "theme": "Default",
  ...
//MCP Server Config
  "mcpServers": {
    "darbot-windows-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "<path to the darbot-windows-mcp directory>",
        "run",
        "main.py"
      ]
    }
  }
}
```

3. Rerun Gemini CLI in terminal. Enjoy 🥳

### Claude Desktop

1. Clone the repository.

```shell
git clone https://github.com/darbotlabs/Darbot-Windows-MCP.git
cd Darbot-Windows-MCP
```

2. Build Desktop Extension `DXT`:

```shell
npx @anthropic-ai/dxt pack
```

3. Open Claude Desktop:

Go to Claude Desktop: Settings->Extensions->Install Extension (locate the `.dxt` file)-> Install

Finally Enjoy 🥳.

For additional Claude Desktop integration troubleshooting, see the [MCP documentation](https://modelcontextprotocol.io/quickstart/server#claude-for-desktop-integration-issues). The documentation includes helpful tips for checking logs and resolving common issues.

---

## 🛠️MCP Tools

Claude can access the following tools to interact with Windows:

- `Click-Tool`: Click on the screen at the given coordinates.
- `Type-Tool`: Type text on an element (optionally clears existing text).
- `Clipboard-Tool`: Copy or paste using the system clipboard.
- `Scroll-Tool`: Scroll vertically or horizontally on the window or specific regions.
- `Drag-Tool`: Drag from one point to another.
- `Move-Tool`: Move mouse pointer.
- `Shortcut-Tool`: Press keyboard shortcuts (`Ctrl+c`, `Alt+Tab`, etc).
- `Key-Tool`: Press a single key.
- `Wait-Tool`: Pause for a defined duration.
- `State-Tool`: Combined snapshot of active apps and interactive, textual and scrollable elements along with screenshot of the desktop.
- `Screenshot-Tool`: Capture a screenshot of the desktop.
- `Launch-Tool`: To launch an application from the start menu.
- `Shell-Tool`: To execute PowerShell commands.
- `Scrape-Tool`: To scrape the entire webpage for information.

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=darbotlabs/Darbot-Windows-MCP&type=Date)](https://www.star-history.com/#darbotlabs/Darbot-Windows-MCP&Date)

## ⚠️Caution

This MCP interacts directly with your Windows operating system to perform actions. Use with caution and avoid deploying it in environments where such risks cannot be tolerated.

## 📝 Limitations

- Selecting specific sections of the text in a paragraph, as the MCP is relying on a11y tree. (⌛ Working on it.)
- `Type-Tool` is meant for typing text, not programming in IDE because of it types program as a whole in a file. (⌛ Working on it.)

## 🪪License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝Contributing

Contributions are welcome! Please see [CONTRIBUTING](CONTRIBUTING) for setup instructions and development guidelines.

Made with ❤️ by [Darbot Labs](https://github.com/darbotlabs)

## Citation

```bibtex
@software{
  author       = {Darbot Labs},
  title        = {Darbot-Windows-MCP: Lightweight open-source project for integrating LLM agents with Windows},
  year         = {2024},
  publisher    = {GitHub},
  url={https://github.com/darbotlabs/Darbot-Windows-MCP}
}
```
