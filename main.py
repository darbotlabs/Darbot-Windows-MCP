from live_inspect.watch_cursor import WatchCursor
from contextlib import asynccontextmanager
from fastmcp.utilities.types import Image
from src.desktop.service import Desktop
from humancursor import SystemCursor
from textwrap import dedent
from fastmcp import FastMCP
from typing import Literal
import pyautogui as pg
import asyncio
import click

pg.FAILSAFE=False
pg.PAUSE=1.0

desktop=Desktop()
cursor=SystemCursor()
watch_cursor=WatchCursor()
windows_version=desktop.get_windows_version()
default_language=desktop.get_default_language()

instructions=dedent(f'''
Windows MCP server provides tools to interact directly with the {windows_version} desktop, 
thus enabling to operate the desktop on the user's behalf.
''')

@asynccontextmanager
async def lifespan(app: FastMCP):
    """Runs initialization code before the server starts and cleanup code after it shuts down."""
    try:
        watch_cursor.start()
        await asyncio.sleep(1) # Simulate startup latency
        yield
    finally:
        watch_cursor.stop()

mcp=FastMCP(name='windows-mcp',instructions=instructions,lifespan=lifespan)

@mcp.tool(name="App-Tool", description="Manages Windows applications through launch, resize, and window switching operations.")
def app_tool(mode:Literal['launch','resize','switch'],name:str|None=None,window_loc:list[int]|None=None,window_size:list[int]|None=None):
    return desktop.app(mode,name,window_loc,window_size)
    
@mcp.tool(name='Powershell-Tool', description='Execute PowerShell commands and return the output with status code')
def powershell_tool(command: str) -> str:
    response,status_code=desktop.execute_command(command)
    return f'Response: {response}\nStatus Code: {status_code}'

@mcp.tool(name='State-Tool',description='Capture comprehensive desktop state including default language used by user interface, focused/opened applications, interactive UI elements (buttons, text fields, menus), informative content (text, labels, status), and scrollable areas. Optionally includes visual screenshot when use_vision=True. Essential for understanding current desktop context and available UI interactions.')
def state_tool(use_vision:bool=False):
    desktop_state=desktop.get_state(use_vision=use_vision,as_bytes=True)
    interactive_elements=desktop_state.tree_state.interactive_elements_to_string()
    informative_elements=desktop_state.tree_state.informative_elements_to_string()
    scrollable_elements=desktop_state.tree_state.scrollable_elements_to_string()
    apps=desktop_state.apps_to_string()
    active_app=desktop_state.active_app_to_string()
    return [dedent(f'''
    Default Language of User:
    {default_language} with encoding: {desktop.encoding}
                            
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
    ''')]+([Image(data=desktop_state.screenshot,format='png')] if use_vision else [])

@mcp.tool(name='Click-Tool',description='Click on UI elements at specific coordinates. Supports left/right/middle mouse buttons and single/double/triple clicks. Use coordinates from State-Tool output.')
def click_tool(loc:list[int],button:Literal['left','right','middle']='left',clicks:int=1)->str:
    if len(loc) != 2:
        raise ValueError("Location must be a list of exactly 2 integers [x, y]")
    x,y=loc[0],loc[1]
    desktop.click(loc=loc,button=button,clicks=clicks)
    num_clicks={1:'Single',2:'Double',3:'Triple'}
    return f'{num_clicks.get(clicks)} {button} clicked at ({x},{y}).'

@mcp.tool(name='Type-Tool',description='Type text into input fields, text areas, or focused elements. Set clear=True to replace existing text, False to append. Click on target element coordinates first.')
def type_tool(loc:list[int],text:str,clear:bool=False,press_enter:bool=False)->str:
    if len(loc) != 2:
        raise ValueError("Location must be a list of exactly 2 integers [x, y]")
    x,y=loc[0],loc[1]
    desktop.type(loc=loc,text=text,clear=clear,press_enter=press_enter)
    return f'Typed {text} at ({x},{y}).'

@mcp.tool(name='Scroll-Tool',description='Scroll at specific coordinates or current mouse position. Use wheel_times to control scroll amount (1 wheel = ~3-5 lines). Essential for navigating lists, web pages, and long content.')
def scroll_tool(loc:list[int]=None,type:Literal['horizontal','vertical']='vertical',direction:Literal['up','down','left','right']='down',wheel_times:int=1)->str:
    if loc and len(loc) != 2:
        raise ValueError("Location must be a list of exactly 2 integers [x, y]")
    response=desktop.scroll(loc,type,direction,wheel_times)
    if response:
        return response
    return f'Scrolled {type} {direction} by {wheel_times} wheel times'+f' at ({loc[0]},{loc[1]}).' if loc else ''

@mcp.tool(name='Drag-Tool',description='Drag and drop operation from current coordinates to destination coordinates. Useful for moving files, resizing windows, or drag-and-drop interactions.')
def drag_tool(to_loc:list[int])->str:
    if len(to_loc) != 2:
        raise ValueError("to_loc must be a list of exactly 2 integers [x, y]")
    desktop.drag(to_loc)
    x2,y2=to_loc[0],to_loc[1]
    return f'Dragged the element to ({x2},{y2}).'

@mcp.tool(name='Move-Tool',description='Move mouse cursor to specific coordinates without clicking. Useful for hovering over elements or positioning cursor before other actions.')
def move_tool(to_loc:list[int])->str:
    if len(to_loc) != 2:
        raise ValueError("to_loc must be a list of exactly 2 integers [x, y]")
    x,y=to_loc[0],to_loc[1]
    desktop.move(to_loc)
    return f'Moved the mouse pointer to ({x},{y}).'

@mcp.tool(name='Shortcut-Tool',description='Execute keyboard shortcuts using key combinations. Pass keys as list (e.g., ctrl+c for copy, alt+tab for app switching, win+r for Run dialog, win is for opening the start menu).')
def shortcut_tool(shortcut:str):
    desktop.shortcut(shortcut)
    return f"Pressed {shortcut}."

@mcp.tool(name='Wait-Tool',description='Pause execution for specified duration in seconds. Useful for waiting for applications to load, animations to complete, or adding delays between actions.')
def wait_tool(duration:int)->str:
    pg.sleep(duration)
    return f'Waited for {duration} seconds.'

@mcp.tool(name='Scrape-Tool',description='Fetch and convert webpage content to markdown format. Provide full URL including protocol (http/https). Returns structured text content suitable for analysis.')
def scrape_tool(url:str)->str:
    content=desktop.scrape(url)
    return f'Scraped the contents of the entire webpage:\n{content}'


@click.command()
@click.option(
    "--transport",
    help="The transport layer used by the MCP server.",
    type=click.Choice(['stdio','sse','streamable-http']),
    default='stdio'
)
@click.option(
    "--host",
    help="Host to bind the SSE/Streamable HTTP server.",
    default="localhost",
    type=str,
    show_default=True
)
@click.option(
    "--port",
    help="Port to bind the SSE/Streamable HTTP server.",
    default=8000,
    type=int,
    show_default=True
)
def main(transport, host, port):
    if transport=='stdio':
        mcp.run()
    else:
        mcp.run(transport=transport,host=host,port=port)

if __name__ == "__main__":
    main()
