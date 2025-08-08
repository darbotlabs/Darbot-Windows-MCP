# 🛠️ Tools Reference - Darbot Windows MCP

<div align="center">
  <img src="assets/darbot_logo_64.png" alt="Darbot Windows MCP Logo" width="64" height="64">
  <h2>🛠️ Tools Reference</h2>
</div>

This guide provides comprehensive documentation for all 15 tools available in Darbot Windows MCP, including parameters, usage examples, and best practices.

## 📋 Table of Contents

- [Overview](#overview)
- [Application Control Tools](#application-control-tools)
- [UI Interaction Tools](#ui-interaction-tools)
- [Input/Output Tools](#inputoutput-tools)
- [System Tools](#system-tools)
- [Web Tools](#web-tools) 
- [Utility Tools](#utility-tools)
- [Usage Examples](#usage-examples)
- [Best Practices](#best-practices)

## Overview

Darbot Windows MCP provides 15 specialized tools for Windows desktop automation. Each tool is designed for specific tasks and can be combined to create complex automation workflows.

### Tool Categories

| Category | Tools | Purpose |
|----------|-------|---------|
| **Application Control** | Launch-Tool, Switch-Tool | Starting and managing applications |
| **UI Interaction** | Click-Tool, Drag-Tool, Move-Tool | Mouse operations |
| **Input/Output** | Type-Tool, Shortcut-Tool, Key-Tool, Clipboard-Tool | Keyboard and text operations |
| **System** | Powershell-Tool, State-Tool | System information and commands |
| **Web** | Browser-Tool, Scrape-Tool | Web browsing and data extraction |
| **Utility** | Scroll-Tool, Wait-Tool | Support operations |

## Application Control Tools

### Launch-Tool

**Purpose:** Launch applications from the Start menu or by executable name.

**Parameters:**
- `app_name` (string, required): Name of the application to launch

**Usage Examples:**

```javascript
// Launch Notepad
"Launch notepad"

// Launch Calculator
"Launch calculator"

// Launch Microsoft Word
"Launch word"

// Launch File Explorer
"Launch explorer"
```

**AI Agent Examples:**
```
"Open Notepad to create a text file"
"Launch Calculator for some quick math"
"Start File Explorer to browse folders"
```

**Tips:**
- Use common application names (notepad, calculator, word, excel)
- The tool searches Start menu and common locations
- Works with both installed applications and Windows built-ins

---

### Switch-Tool

**Purpose:** Bring a specific window to the foreground by application name.

**Parameters:**
- `window_name` (string, required): Name or title of the window to focus

**Usage Examples:**

```javascript
// Switch to Notepad window
"Switch to notepad"

// Focus on Calculator
"Switch to calculator"

// Bring Chrome to front
"Switch to chrome"
```

**AI Agent Examples:**
```
"Switch to the Notepad window"
"Bring the Calculator to the front"
"Focus on the browser window"
```

**Tips:**
- Use partial window titles or application names
- Case-insensitive matching
- Useful for multi-tasking workflows

## UI Interaction Tools

### Click-Tool

**Purpose:** Perform mouse clicks at specific screen coordinates.

**Parameters:**
- `x` (integer, required): X coordinate to click
- `y` (integer, required): Y coordinate to click
- `button` (string, optional): Mouse button ('left', 'right', 'middle', default: 'left')
- `clicks` (integer, optional): Number of clicks (default: 1)

**Usage Examples:**

```javascript
// Single left click
"Click at 400, 300"

// Double click
"Double click at 500, 200"

// Right click for context menu
"Right click at 600, 400"

// Middle click
"Middle click at 450, 350"
```

**AI Agent Examples:**
```
"Click the OK button at coordinates 500, 400"
"Right-click at 300, 200 to open context menu"
"Double-click the file icon at 450, 300"
```

**Tips:**
- Use State-Tool first to find exact coordinates
- Right-click opens context menus
- Double-click for opening files/folders

---

### Drag-Tool

**Purpose:** Drag from one screen location to another.

**Parameters:**
- `start_x` (integer, required): Starting X coordinate
- `start_y` (integer, required): Starting Y coordinate
- `end_x` (integer, required): Ending X coordinate
- `end_y` (integer, required): Ending Y coordinate

**Usage Examples:**

```javascript
// Drag a file to a folder
"Drag from 100, 200 to 300, 400"

// Move a window
"Drag from 50, 10 to 200, 100"

// Select text by dragging
"Drag from 150, 250 to 350, 280"
```

**AI Agent Examples:**
```
"Drag the file from desktop to the Documents folder"
"Move this window by dragging from title bar"
"Select text by dragging across it"
```

**Tips:**
- Useful for file management and text selection
- Smooth dragging motion for better compatibility
- Can be used to move windows by dragging title bars

---

### Move-Tool

**Purpose:** Move the mouse cursor to specific coordinates without clicking.

**Parameters:**
- `x` (integer, required): X coordinate to move to
- `y` (integer, required): Y coordinate to move to

**Usage Examples:**

```javascript
// Move cursor to position
"Move cursor to 400, 300"

// Position for hover effects
"Move mouse to 250, 150"
```

**AI Agent Examples:**
```
"Move the cursor to hover over the menu item"
"Position mouse at 500, 200 to reveal tooltip"
```

**Tips:**
- Useful for triggering hover effects
- Prepares cursor position for subsequent clicks
- Can reveal tooltips and dynamic content

## Input/Output Tools

### Type-Tool

**Purpose:** Type text into the currently focused input field.

**Parameters:**
- `text` (string, required): Text to type
- `clear` (boolean, optional): Clear existing text before typing (default: false)

**Usage Examples:**

```javascript
// Type text
"Type 'Hello World'"

// Clear field and type new text
"Type 'New content' and clear existing"

// Type multi-line text
"Type 'Line 1\nLine 2\nLine 3'"
```

**AI Agent Examples:**
```
"Type my email address in the field"
"Clear the text box and type the new message"
"Enter the filename 'document.txt'"
```

**Tips:**
- Click on input field first to ensure focus
- Use \n for line breaks
- Clear option prevents text duplication
- Works with any text input (forms, editors, etc.)

---

### Shortcut-Tool

**Purpose:** Send keyboard shortcut combinations.

**Parameters:**
- `keys` (array of strings, required): List of keys to press together

**Usage Examples:**

```javascript
// Copy to clipboard
"Send shortcut ['ctrl', 'c']"

// Paste from clipboard
"Send shortcut ['ctrl', 'v']"

// Save document
"Send shortcut ['ctrl', 's']"

// Open Start menu
"Send shortcut ['win']"

// Alt-Tab to switch windows
"Send shortcut ['alt', 'tab']"

// Select all
"Send shortcut ['ctrl', 'a']"
```

**AI Agent Examples:**
```
"Copy the selected text using Ctrl+C"
"Save the document with Ctrl+S"
"Open Start menu with Windows key"
"Switch to next window with Alt+Tab"
```

**Tips:**
- Common shortcuts: ctrl+c (copy), ctrl+v (paste), ctrl+s (save)
- Use 'win' for Windows key
- Case-insensitive key names
- Supports function keys (f1, f2, etc.)

---

### Key-Tool

**Purpose:** Press individual keys including special keys.

**Parameters:**
- `key` (string, required): Key to press

**Usage Examples:**

```javascript
// Press Enter
"Press enter"

// Press Escape
"Press escape"

// Press Tab
"Press tab"

// Press F1 for help
"Press f1"

// Press arrow keys
"Press up"
"Press down"
"Press left"
"Press right"
```

**AI Agent Examples:**
```
"Press Enter to confirm the dialog"
"Hit Escape to cancel the operation"
"Press Tab to move to next field"
"Press F1 to open help"
```

**Tips:**
- Useful for navigation and dialog control
- Supports all special keys (arrows, function keys, etc.)
- Essential for form navigation

---

### Clipboard-Tool

**Purpose:** Copy text to clipboard or retrieve current clipboard contents.

**Parameters:**
- `action` (string, required): 'copy' or 'paste'
- `text` (string, required for copy): Text to copy to clipboard

**Usage Examples:**

```javascript
// Copy text to clipboard
"Copy 'Hello World' to clipboard"

// Get current clipboard content
"Get clipboard content"

// Copy URL for sharing
"Copy 'https://example.com' to clipboard"
```

**AI Agent Examples:**
```
"Copy this URL to clipboard for later use"
"What's currently in the clipboard?"
"Copy the email address to clipboard"
```

**Tips:**
- Useful for transferring data between applications
- Paste action retrieves current clipboard content
- Works with any text content

## System Tools

### Powershell-Tool

**Purpose:** Execute PowerShell commands and capture output.

**Parameters:**
- `command` (string, required): PowerShell command to execute

**Usage Examples:**

```javascript
// List directory contents
"Run powershell 'Get-ChildItem'"

// Get system information
"Run powershell 'Get-ComputerInfo'"

// Check running processes
"Run powershell 'Get-Process'"

// Get network information
"Run powershell 'Get-NetAdapter'"

// File operations
"Run powershell 'Copy-Item source.txt destination.txt'"
```

**AI Agent Examples:**
```
"Show me the files in the current directory"
"What processes are currently running?"
"Get information about the network adapters"
"Copy this file to another location"
```

**Tips:**
- Full PowerShell command capabilities
- Useful for system administration tasks
- Can perform file operations, system queries
- Output is captured and returned

---

### State-Tool

**Purpose:** Get comprehensive information about the current desktop state, including active applications, UI elements, and optional screenshot.

**Parameters:**
- `include_screenshot` (boolean, optional): Include base64-encoded screenshot (default: false)

**Usage Examples:**

```javascript
// Get basic desktop state
"Get desktop state"

// Get state with screenshot
"Get desktop state with screenshot"

// Check what's currently open
"Show me the current desktop state"
```

**AI Agent Examples:**
```
"What applications are currently open?"
"Show me the desktop state with a screenshot"
"Get information about UI elements on screen"
"What's the current active window?"
```

**Tips:**
- Essential for understanding current desktop context
- Lists all open applications and UI elements
- Screenshot helps AI understand visual context
- Use before performing UI operations

## Web Tools

### Browser-Tool

**Purpose:** Launch Microsoft Edge browser and navigate to a specified URL.

**Parameters:**
- `url` (string, required): URL to navigate to

**Usage Examples:**

```javascript
// Open Google
"Open browser to 'https://google.com'"

// Navigate to GitHub
"Browse to 'https://github.com'"

// Open local file
"Open browser to 'file:///C:/path/to/file.html'"
```

**AI Agent Examples:**
```
"Open Google in the browser"
"Navigate to GitHub homepage"
"Browse to the company website"
```

**Tips:**
- Always include full URL with protocol (https://)
- Supports local file URLs
- Opens in Microsoft Edge by default

---

### Scrape-Tool

**Purpose:** Fetch webpage content and return it as formatted Markdown.

**Parameters:**
- `url` (string, required): URL to scrape

**Usage Examples:**

```javascript
// Scrape news article
"Scrape content from 'https://news.example.com/article'"

// Get documentation
"Scrape 'https://docs.example.com/api'"

// Extract text content
"Get text from 'https://blog.example.com/post'"
```

**AI Agent Examples:**
```
"Extract the text content from this news article"
"Get the documentation from this webpage"
"Scrape the blog post and summarize it"
```

**Tips:**
- Returns clean, formatted Markdown
- Useful for content analysis and extraction
- Works with most public web pages
- Respects website structure and formatting

## Utility Tools

### Scroll-Tool

**Purpose:** Perform vertical or horizontal scrolling at specific coordinates.

**Parameters:**
- `x` (integer, optional): X coordinate for scroll center
- `y` (integer, optional): Y coordinate for scroll center  
- `direction` (string, optional): 'up', 'down', 'left', or 'right' (default: 'down')
- `clicks` (integer, optional): Number of scroll clicks (default: 3)

**Usage Examples:**

```javascript
// Scroll down in window
"Scroll down at 400, 300"

// Scroll up with more clicks  
"Scroll up at 500, 200 for 5 clicks"

// Horizontal scrolling
"Scroll right at 300, 400"
"Scroll left at 300, 400"

// Scroll at current mouse position
"Scroll down"
```

**AI Agent Examples:**
```
"Scroll down to see more content"
"Scroll up to go back to the top"
"Scroll horizontally to see more columns"
```

**Tips:**
- Position coordinates determine scroll target area
- Useful for navigating long documents or web pages
- Horizontal scrolling works with wide content

---

### Wait-Tool

**Purpose:** Pause execution for a specified number of seconds.

**Parameters:**
- `seconds` (number, required): Number of seconds to wait

**Usage Examples:**

```javascript
// Wait for 2 seconds
"Wait 2 seconds"

// Longer pause for app loading
"Wait 5 seconds"

// Brief pause
"Wait 0.5 seconds"
```

**AI Agent Examples:**
```
"Wait a moment for the application to load"
"Pause briefly before continuing"
"Wait for the page to finish loading"
```

**Tips:**
- Essential for timing-sensitive operations
- Use after launching applications
- Allow UI to respond between actions
- Prevents race conditions in automation

## Usage Examples

### Complete Workflow Examples

#### Example 1: Creating and Saving a Document

```javascript
// 1. Launch Notepad
"Launch notepad"

// 2. Wait for it to open
"Wait 2 seconds"

// 3. Type content
"Type 'This is my document content.'"

// 4. Save the document
"Send shortcut ['ctrl', 's']"

// 5. Wait for dialog
"Wait 1 second"

// 6. Type filename
"Type 'my-document.txt'"

// 7. Press Enter to save
"Press enter"
```

#### Example 2: Web Research Workflow

```javascript
// 1. Open browser
"Open browser to 'https://google.com'"

// 2. Wait for page load
"Wait 3 seconds"

// 3. Click search box (get coordinates first with State-Tool)
"Click at 400, 300"

// 4. Type search query
"Type 'Windows automation tools'"

// 5. Press Enter to search
"Press enter"

// 6. Wait for results
"Wait 2 seconds"

// 7. Scrape results page
"Scrape content from current page"
```

#### Example 3: File Management

```javascript
// 1. Launch File Explorer
"Launch explorer"

// 2. Wait for it to open
"Wait 2 seconds"

// 3. Navigate to Documents (using shortcut)
"Send shortcut ['ctrl', 'shift', 'd']"

// 4. Create new folder (right-click)
"Right click at 400, 300"

// 5. Select "New Folder" from context menu
"Click at 450, 350"

// 6. Type folder name
"Type 'My New Folder'"

// 7. Press Enter to confirm
"Press enter"
```

## Best Practices

### Timing and Reliability

1. **Always wait after launching applications**
   ```javascript
   "Launch notepad"
   "Wait 2 seconds"  // Allow app to load
   ```

2. **Use State-Tool before UI interactions**
   ```javascript
   "Get desktop state"  // Understand current context
   "Click at 400, 300"  // Then interact
   ```

3. **Add pauses between rapid actions**
   ```javascript
   "Click at 300, 200"
   "Wait 0.5 seconds"
   "Type 'Hello'"
   ```

### Error Prevention

1. **Verify target application is active**
   ```javascript
   "Switch to notepad"  // Ensure correct window
   "Type 'content'"     // Then interact
   ```

2. **Use appropriate wait times**
   - Application launch: 2-3 seconds
   - Dialog appearance: 1-2 seconds
   - Page loading: 3-5 seconds
   - UI updates: 0.5-1 seconds

3. **Clear input fields when needed**
   ```javascript
   "Type 'new content' and clear existing"
   ```

### Coordinate Management

1. **Use State-Tool to find coordinates**
   ```javascript
   "Get desktop state"  // Find UI element positions
   "Click at [discovered coordinates]"
   ```

2. **Test coordinates on your specific screen resolution**

3. **Use relative positioning when possible**

### Workflow Organization

1. **Break complex tasks into steps**
2. **Add descriptive comments in AI prompts**
3. **Handle errors gracefully with fallback actions**
4. **Test workflows thoroughly before automation**

### Security Considerations

1. **Never automate sensitive operations without verification**
2. **Be cautious with system-level PowerShell commands**
3. **Test in safe environments first**
4. **Understand the implications of each tool**

For more advanced usage and development information, see the [Development Guide](DEVELOPMENT.md).