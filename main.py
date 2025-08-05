"""
🪟 Darbot Windows MCP - Professional Windows Desktop Automation
Desktop automation server for AI agents via Model Context Protocol (MCP)

Copyright (c) 2025 Darbot Labs
Licensed under MIT License
https://github.com/darbotlabs/Darbot-Windows-MCP
"""

from live_inspect.watch_cursor import WatchCursor
from contextlib import asynccontextmanager
from fastmcp.utilities.types import Image
from humancursor import SystemCursor
from platform import system, release
from markdownify import markdownify
from src.desktop import Desktop
from textwrap import dedent
from fastmcp import FastMCP
from typing import Literal, List
import uiautomation as ua
import pyautogui as pg
import pyperclip as pc
import requests
import asyncio
import ctypes

pg.FAILSAFE=False
pg.PAUSE=1.0

os=system()
version=release()

instructions=dedent(f'''
🪟 Darbot Windows MCP - Professional Windows Desktop Automation
Control {os} {version} desktop like a human with 15 powerful automation tools.

This MCP server enables AI agents to interact directly with the Windows desktop,
providing comprehensive automation capabilities including app launching, UI interaction,
system commands, clipboard management, and web integration.

Perfect for building AI assistants that can operate your desktop on your behalf.
''')

desktop=Desktop()
cursor=SystemCursor()
watch_cursor=WatchCursor()
ctypes.windll.user32.SetProcessDPIAware()

@asynccontextmanager
async def lifespan(app: FastMCP):
    """Runs initialization code before the server starts and cleanup code after it shuts down."""
    try:
        watch_cursor.start()
        await asyncio.sleep(1) # Simulate startup latency
        yield
        watch_cursor.stop()
    except Exception:
        watch_cursor.stop()

mcp=FastMCP(name='darbot-windows-mcp',instructions=instructions,lifespan=lifespan)

@mcp.tool(name='Launch-Tool', description='Launch an application from the Windows Start Menu by name (e.g., "notepad", "calculator", "chrome")')
def launch_tool(name: str) -> str:
    _,status=desktop.launch_app(name)
    if status!=0:
        return f'Failed to launch {name.title()}.'
    else:
        return f'Launched {name.title()}.'
    
@mcp.tool(name='Powershell-Tool', description='Execute PowerShell commands and return the output with status code')
def powershell_tool(command: str) -> str:
    response,status=desktop.execute_command(command)
    return f'Status Code: {status}\nResponse: {response}'

@mcp.tool(name='State-Tool',description='Capture comprehensive desktop state including focused/opened applications, interactive UI elements (buttons, text fields, menus), informative content (text, labels, status), and scrollable areas. Optionally includes visual screenshot when use_vision=True. Essential for understanding current desktop context and available UI interactions.')
def state_tool(use_vision:bool=False)->str:
    desktop_state=desktop.get_state(use_vision=use_vision)
    interactive_elements=desktop_state.tree_state.interactive_elements_to_string()
    informative_elements=desktop_state.tree_state.informative_elements_to_string()
    scrollable_elements=desktop_state.tree_state.scrollable_elements_to_string()
    apps=desktop_state.apps_to_string()
    active_app=desktop_state.active_app_to_string()
    
    state_text = dedent(f'''
    Focused App:
    {active_app}

    Opened Apps:
    {apps}

    List of Interactive Elements:
    {interactive_elements or 'No interactive elements found.'}

    List of Informative Elements:
    {informative_elements or 'No informative elements found.'}

    List of Scrollable Elements:
    {scrollable_elements or 'No scrollable elements found.'}
    ''').strip()
    
    # Note: Image support would need to be handled differently in MCP
    # For now, just return the text state
    if use_vision:
        state_text += "\n\n[Screenshot capture requested but not supported in current MCP implementation]"
    
    return state_text
    
@mcp.tool(name='Clipboard-Tool',description='Copy text to clipboard or retrieve current clipboard content. Use "copy" mode with text parameter to copy, "paste" mode to retrieve.')
def clipboard_tool(mode: Literal['copy', 'paste'], text: str = None)->str:
    if mode == 'copy':
        if text:
            pc.copy(text)  # Copy text to system clipboard
            return f'Copied "{text}" to clipboard'
        else:
            raise ValueError("No text provided to copy")
    elif mode == 'paste':
        clipboard_content = pc.paste()  # Get text from system clipboard
        return f'Clipboard Content: "{clipboard_content}"'
    else:
        raise ValueError('Invalid mode. Use "copy" or "paste".')

@mcp.tool(name='Click-Tool',description='Click on UI elements at specific coordinates. Supports left/right/middle mouse buttons and single/double/triple clicks. Use coordinates from State-Tool output.')
def click_tool(x: int, y: int, button:Literal['left','right','middle']='left',clicks:int=1)->str:
    pg.click(x=x, y=y, button=button, clicks=clicks)
    control=desktop.get_element_under_cursor()
    num_clicks={1:'Single',2:'Double',3:'Triple'}
    return f'{num_clicks.get(clicks)} {button} Clicked on {control.Name} Element with ControlType {control.ControlTypeName} at ({x},{y}).'

@mcp.tool(name='Type-Tool',description='Type text into input fields, text areas, or focused elements. Set clear=True to replace existing text, False to append. Click on target element coordinates first.')
def type_tool(x: int, y: int, text:str,clear:bool=False):
    pg.click(x=x, y=y)
    control=desktop.get_element_under_cursor()
    if clear:  # Fixed: compare boolean directly instead of string
        pg.hotkey('ctrl','a')
        pg.press('backspace')
    pg.typewrite(text,interval=0.1)
    return f'Typed {text} on {control.Name} Element with ControlType {control.ControlTypeName} at ({x},{y}).'

@mcp.tool(name='Switch-Tool',description='Switch to a specific application window (e.g., "notepad", "calculator", "chrome", etc.) and bring to foreground.')
def switch_tool(name: str) -> str:
    _,status=desktop.switch_app(name)
    if status!=0:
        return f'Failed to switch to {name.title()} window.'
    else:
        return f'Switched to {name.title()} window.'

@mcp.tool(name='Scroll-Tool',description='Scroll at specific coordinates or current mouse position. Use wheel_times to control scroll amount (1 wheel = ~3-5 lines). Essential for navigating lists, web pages, and long content.')
def scroll_tool(x: int = None, y: int = None, type:Literal['horizontal','vertical']='vertical',direction:Literal['up','down','left','right']='down',wheel_times:int=1)->str:
    if x is not None and y is not None:
        pg.moveTo(x, y)
    match type:
        case 'vertical':
            match direction:
                case 'up':
                    ua.WheelUp(wheel_times)
                case 'down':
                    ua.WheelDown(wheel_times)
                case _:
                    return 'Invalid direction. Use "up" or "down".'
        case 'horizontal':
            match direction:
                case 'left':
                    pg.keyDown('Shift')
                    pg.sleep(0.05)
                    ua.WheelUp(wheel_times)
                    pg.sleep(0.05)
                    pg.keyUp('Shift')
                case 'right':
                    pg.keyDown('Shift')
                    pg.sleep(0.05)
                    ua.WheelDown(wheel_times)
                    pg.sleep(0.05)
                    pg.keyUp('Shift')
                case _:
                    return 'Invalid direction. Use "left" or "right".'
        case _:
            return 'Invalid type. Use "horizontal" or "vertical".'
    return f'Scrolled {type} {direction} by {wheel_times} wheel times.'

@mcp.tool(name='Drag-Tool',description='Drag and drop operation from source coordinates to destination coordinates. Useful for moving files, resizing windows, or drag-and-drop interactions.')
def drag_tool(from_x: int, from_y: int, to_x: int, to_y: int)->str:
    # Move to start position, press mouse down, drag to end, release
    pg.moveTo(from_x, from_y)
    pg.mouseDown()
    pg.moveTo(to_x, to_y, duration=0.5)
    pg.mouseUp()
    control=desktop.get_element_under_cursor()
    return f'Dragged element from ({from_x},{from_y}) to ({to_x},{to_y}).'

@mcp.tool(name='Move-Tool',description='Move mouse cursor to specific coordinates without clicking. Useful for hovering over elements or positioning cursor before other actions.')
def move_tool(x: int, y: int)->str:
    pg.moveTo(x, y)
    return f'Moved the mouse pointer to ({x},{y}).'

@mcp.tool(name='Shortcut-Tool',description='Execute keyboard shortcuts using key combinations. Pass keys as list (e.g., ["ctrl", "c"] for copy, ["alt", "tab"] for app switching, ["win", "r"] for Run dialog).')
def shortcut_tool(shortcut: List[str]):
    pg.hotkey(*shortcut)
    return f'Pressed {'+'.join(shortcut)}.'

@mcp.tool(name='Key-Tool',description='Press individual keyboard keys. Supports special keys like "enter", "escape", "tab", "space", "backspace", "delete", arrow keys ("up", "down", "left", "right"), function keys ("f1"-"f12").')
def key_tool(key:str='')->str:
    pg.press(key)
    return f'Pressed the key {key}.'

@mcp.tool(name='Wait-Tool',description='Pause execution for specified duration in seconds. Useful for waiting for applications to load, animations to complete, or adding delays between actions.')
def wait_tool(duration:int)->str:
    pg.sleep(duration)
    return f'Waited for {duration} seconds.'

@mcp.tool(name='Scrape-Tool',description='Fetch and convert webpage content to markdown format. Provide full URL including protocol (http/https). Returns structured text content suitable for analysis.')
def scrape_tool(url:str)->str:
    response=requests.get(url,timeout=10)
    html=response.text
    content=markdownify(html=html)
    return f'Scraped the contents of the entire webpage:\n{content}'

@mcp.tool(name='Browser-Tool',description='Launch Microsoft Edge browser and navigate to a specified URL. If no URL is provided, opens Edge to the default home page.')
def browser_tool(url: str = None) -> str:
    try:
        # Launch Edge
        launch_result, status = desktop.launch_app("msedge")
        if status != 0:
            return f'Failed to launch Microsoft Edge.'
        
        # Wait for Edge to load
        pg.sleep(2)
        
        if url:
            # Navigate to the specified URL
            # Focus the address bar (Ctrl+L)
            pg.hotkey('ctrl', 'l')
            pg.sleep(0.5)
            
            # Type the URL
            pg.typewrite(url, interval=0.05)
            pg.sleep(0.5)
            
            # Press Enter to navigate
            pg.press('enter')
            
            return f'Launched Microsoft Edge and navigated to {url}'
        else:
            return 'Launched Microsoft Edge with default home page'
            
    except Exception as e:
        return f'Error launching Edge browser: {str(e)}'

if __name__ == "__main__":
    import sys
    
    # Handle help command
    if "--help" in sys.argv or "-h" in sys.argv:
        print("Darbot Windows MCP Server")
        print("========================")
        print("A Model Context Protocol server for Windows desktop automation.")
        print("")
        print("Usage:")
        print("  python main.py          Start the MCP server in stdio mode")
        print("  python main.py --help   Show this help message")
        print("")
        print("Available Tools:")
        print("  Launch-Tool    - Launch applications from Start menu")
        print("  Powershell-Tool - Run PowerShell commands")
        print("  State-Tool     - Get desktop state and UI elements")
        print("  Clipboard-Tool - Copy/paste clipboard content")
        print("  Click-Tool     - Click at coordinates")
        print("  Type-Tool      - Type text into UI elements")
        print("  Switch-Tool    - Switch between applications")
        print("  Scroll-Tool    - Scroll in windows")
        print("  Drag-Tool      - Drag and drop operations")
        print("  Move-Tool      - Move mouse cursor")
        print("  Shortcut-Tool  - Send keyboard shortcuts")
        print("  Key-Tool       - Press individual keys")
        print("  Wait-Tool      - Pause execution")
        print("  Scrape-Tool    - Fetch webpage content")
        print("  Browser-Tool   - Launch Edge browser")
        print("")
        print("For VS Code integration, see README.md for configuration instructions.")
        sys.exit(0)
    
    # Start the MCP server
    mcp.run()