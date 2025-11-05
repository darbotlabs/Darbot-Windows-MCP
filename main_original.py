from live_inspect.watch_cursor import WatchCursor
from contextlib import asynccontextmanager
from fastmcp.utilities.types import Image
from humancursor import SystemCursor
from platform import system, release
from markdownify import markdownify
from textwrap import dedent
from fastmcp import FastMCP
from typing import Literal
import requests
import asyncio
import sys

# Platform detection
os_name = system()
version = release()

# Check if running on Windows
if os_name != 'Windows':
    print(f"⚠️  Warning: Darbot-Windows-MCP is designed for Windows. Running on {os_name} may have limited functionality.")
    print("Some features may not work correctly. For full functionality, please use Windows.")

# Import Windows-specific modules with error handling
try:
    from src.desktop import Desktop
    import uiautomation as ua
    import pyautogui as pg
    import pyperclip as pc
    import ctypes
    
    # Configure pyautogui if available
    pg.FAILSAFE = False
    pg.PAUSE = 1.0
    
    # Set DPI awareness if on Windows
    if os_name == 'Windows':
        ctypes.windll.user32.SetProcessDPIAware()
    
    WINDOWS_AVAILABLE = True
    
except ImportError as e:
    print(f"⚠️  Windows-specific dependencies not available: {e}")
    print("Running in limited mode - some tools will not function.")
    WINDOWS_AVAILABLE = False
    
    # Mock classes for non-Windows environments
    class MockDesktop:
        def get_state(self, use_vision=False):
            return None
        def get_element_under_cursor(self):
            return None
        def execute_command(self, command):
            return "Not available on non-Windows systems", 1
        def launch_app(self, name):
            return f"Cannot launch {name} on non-Windows systems", 1
        def switch_app(self, name):
            return f"Cannot switch to {name} on non-Windows systems", 1
    
    Desktop = MockDesktop
    
    class MockControl:
        Name = "Mock Control"
        ControlTypeName = "Mock"
    
    class MockCursor:
        def start(self): pass
        def stop(self): pass
        def move_to(self, loc): pass
        def click_on(self, loc): pass
        def drag_and_drop(self, from_loc, to_loc): pass
    
    # Mock Windows-specific modules
    class MockPyAutoGUI:
        def mouseDown(self): pass
        def click(self, button='left', clicks=1): pass
        def mouseUp(self): pass
        def hotkey(self, *keys): pass
        def press(self, key): pass
        def typewrite(self, text, interval=0.1): pass
        def keyDown(self, key): pass
        def keyUp(self, key): pass
        def sleep(self, duration): pass
        def screenshot(self): return None
    
    class MockPyperclip:
        def copy(self, text): pass
        def paste(self): return ""
    
    class MockUA:
        def WheelUp(self, times): pass
        def WheelDown(self, times): pass
    
    pg = MockPyAutoGUI()
    pc = MockPyperclip()
    ua = MockUA()

instructions = dedent(f'''
Windows MCP server provides tools to interact directly with the {os_name} {version} desktop, 
thus enabling to operate the desktop on the user's behalf.

Note: This server is optimized for Windows systems. 
Running on {os_name} may have limited functionality.
''')

# Initialize desktop and cursor with error handling
desktop = Desktop()

if WINDOWS_AVAILABLE:
    try:
        cursor = SystemCursor()
        watch_cursor = WatchCursor()
    except Exception as e:
        print(f"⚠️  Warning: Could not initialize cursor controls: {e}")
        cursor = MockCursor()
        watch_cursor = MockCursor()
else:
    cursor = MockCursor()
    watch_cursor = MockCursor()

@asynccontextmanager
async def lifespan(app: FastMCP):
    """Runs initialization code before the server starts and cleanup code after it shuts down."""
    try:
        if WINDOWS_AVAILABLE:
            watch_cursor.start()
        await asyncio.sleep(1)  # Simulate startup latency
        yield
    except Exception as e:
        print(f"⚠️  Error during lifespan management: {e}")
        yield
    finally:
        if WINDOWS_AVAILABLE:
            try:
                watch_cursor.stop()
            except Exception as e:
                print(f"⚠️  Error stopping watch cursor: {e}")

mcp = FastMCP(name='darbot-windows-mcp', instructions=instructions, lifespan=lifespan)

def ensure_windows_available(func):
    """Decorator to ensure Windows functionality is available."""
    def wrapper(*args, **kwargs):
        if not WINDOWS_AVAILABLE:
            return f"This tool requires Windows. Currently running on {os_name}."
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return f"Error executing {func.__name__}: {str(e)}"
    return wrapper

@mcp.tool(name='Launch-Tool', description='Launch an application from the Windows Start Menu by name (e.g., "notepad", "calculator", "chrome")')
@ensure_windows_available
def launch_tool(name: str) -> str:
    """Launch an application from the Windows Start Menu."""
    if not name or not name.strip():
        return "Error: Application name cannot be empty."
    
    try:
        _, status = desktop.launch_app(name.strip())
        if status != 0:
            return f'Failed to launch {name.title()}. Make sure the application exists and you have permission to run it.'
        else:
            return f'Launched {name.title()}.'
    except Exception as e:
        return f'Error launching {name.title()}: {str(e)}'

@mcp.tool(name='Powershell-Tool', description='Execute PowerShell commands and return the output with status code')
@ensure_windows_available
def powershell_tool(command: str) -> str:
    """Execute a PowerShell command and return the result."""
    if not command or not command.strip():
        return "Error: Command cannot be empty."
    
    if os_name != 'Windows':
        return f"PowerShell is not available on {os_name}."
    
    try:
        response, status = desktop.execute_command(command.strip())
        return f'Status Code: {status}\nResponse: {response}'
    except Exception as e:
        return f'Error executing PowerShell command: {str(e)}'

@mcp.tool(name='State-Tool', description='Capture comprehensive desktop state including focused/opened applications, interactive UI elements (buttons, text fields, menus), informative content (text, labels, status), and scrollable areas. Optionally includes visual screenshot when use_vision=True. Essential for understanding current desktop context and available UI interactions.')
@ensure_windows_available
def state_tool(use_vision: bool = False) -> str:
    """Capture the current desktop state and UI elements."""
    try:
        desktop_state = desktop.get_state(use_vision=use_vision)
        
        if not desktop_state:
            return "Unable to capture desktop state. Ensure you're running on Windows."
        
        interactive_elements = desktop_state.tree_state.interactive_elements_to_string()
        informative_elements = desktop_state.tree_state.informative_elements_to_string()
        scrollable_elements = desktop_state.tree_state.scrollable_elements_to_string()
        apps = desktop_state.apps_to_string()
        active_app = desktop_state.active_app_to_string()
        
        result = [dedent(f'''
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
        ''')]
        
        if use_vision and desktop_state.screenshot:
            result.append(Image(data=desktop_state.screenshot, format='png'))
        
        return result
        
    except Exception as e:
        return f"Error capturing desktop state: {str(e)}"
    
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
def click_tool(loc:tuple[int,int],button:Literal['left','right','middle']='left',clicks:int=1)->str:
    x,y=loc
    cursor.move_to(loc)
    control=desktop.get_element_under_cursor()
    pg.mouseDown()
    pg.click(button=button,clicks=clicks)
    pg.mouseUp()
    num_clicks={1:'Single',2:'Double',3:'Triple'}
    return f'{num_clicks.get(clicks)} {button} Clicked on {control.Name} Element with ControlType {control.ControlTypeName} at ({x},{y}).'

@mcp.tool(name='Type-Tool',description='Type text into input fields, text areas, or focused elements. Set clear=True to replace existing text, False to append. Click on target element coordinates first.')
def type_tool(loc:tuple[int,int],text:str,clear:bool=False):
    x,y=loc
    cursor.click_on(loc)
    control=desktop.get_element_under_cursor()
    if clear=='True':
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
def scroll_tool(loc:tuple[int,int]=None,type:Literal['horizontal','vertical']='vertical',direction:Literal['up','down','left','right']='down',wheel_times:int=1)->str:
    if loc:
        cursor.move_to(loc)
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
def drag_tool(from_loc:tuple[int,int],to_loc:tuple[int,int])->str:
    control=desktop.get_element_under_cursor()
    x1,y1=from_loc
    x2,y2=to_loc
    cursor.drag_and_drop(from_loc,to_loc)
    return f'Dragged the {control.Name} element with ControlType {control.ControlTypeName} from ({x1},{y1}) to ({x2},{y2}).'

@mcp.tool(name='Move-Tool',description='Move mouse cursor to specific coordinates without clicking. Useful for hovering over elements or positioning cursor before other actions.')
def move_tool(to_loc:tuple[int,int])->str:
    x,y=to_loc
    cursor.move_to(to_loc)
    return f'Moved the mouse pointer to ({x},{y}).'

@mcp.tool(name='Shortcut-Tool',description='Execute keyboard shortcuts using key combinations. Pass keys as list (e.g., ["ctrl", "c"] for copy, ["alt", "tab"] for app switching, ["win", "r"] for Run dialog).')
def shortcut_tool(shortcut:list[str]):
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

if __name__ == "__main__":
    mcp.run()