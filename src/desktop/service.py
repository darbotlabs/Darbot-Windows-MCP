from ctypes.wintypes import RECT
from uiautomation import Control, GetRootControl, IsIconic, IsZoomed, IsWindowVisible, ControlType, ControlFromCursor, IsTopLevelWindow, ShowWindow, ControlFromHandle
from src.desktop.config import EXCLUDED_APPS, AVOIDED_APPS, BROWSER_NAMES, PROCESS_PER_MONITOR_DPI_AWARE
from src.desktop.views import DesktopState, App, Size, Status
from PIL.Image import Image as PILImage
from locale import getpreferredencoding
from contextlib import contextmanager
from src.tree.service import Tree
from fuzzywuzzy import process
from typing import Optional
from psutil import Process
from time import sleep
from io import BytesIO
from PIL import Image
import subprocess
import pyautogui
import ctypes
import base64
import csv
import os
import io
import win32gui

class Desktop:
    def __init__(self):
        ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)
        self.encoding=getpreferredencoding()
        self.desktop_state=None
        
    def get_state(self,use_vision:bool=False)->DesktopState:
        tree=Tree(self)
        active_app,apps=self.get_apps()
        tree_state=tree.get_state()
        if use_vision:
            annotated_screenshot=tree.annotated_screenshot(tree_state.interactive_nodes,scale=0.5)
            screenshot=self.screenshot_in_bytes(annotated_screenshot)
        else:
            screenshot=None
        self.desktop_state=DesktopState(apps= apps,active_app=active_app,screenshot=screenshot,tree_state=tree_state)
        return self.desktop_state
    
    def get_window_element_from_element(self,element:Control)->Control|None:
        while element is not None:
            if IsTopLevelWindow(element.NativeWindowHandle):
                return element
            element = element.GetParentControl()
        return None
    
    def get_active_app(self,apps:list[App])->App|None:
        if len(apps)>0 and apps[0].status != Status.MINIMIZED:
            return apps[0]
        return None
    
    def get_active_app_by_win32(self)->App|None:
        try:
            hwnd = win32gui.GetForegroundWindow()
            if hwnd == 0:
                return None
            title = win32gui.GetWindowText(hwnd)
            if not title:
                return None

            # Get window status
            # GetWindowPlacement returns (flags, showCmd, ptMin, ptMax, rcNormal)
            # showCmd (index 1) contains the display status of the window
            placement = win32gui.GetWindowPlacement(hwnd)
            show_cmd = placement[1]
            SW_SHOWMINIMIZED = 2
            SW_SHOWMAXIMIZED = 3

            status = Status.NORMAL
            if show_cmd == SW_SHOWMINIMIZED:
                status = Status.MINIMIZED
            elif show_cmd == SW_SHOWMAXIMIZED:
                status = Status.MAXIMIZED

            size = self.get_app_size_by_hwnd(hwnd)

            return App(
                name=title,
                depth=0, # I don't know what effect it has yet, so I set all of them to 0.
                status=status,
                size=size,
                handle=hwnd
            )

        except Exception as ex:
            print(f"Error: {ex}")
            return None
    
    def get_app_status(self,control:Control)->Status:
        if IsIconic(control.NativeWindowHandle):
            return Status.MINIMIZED
        elif IsZoomed(control.NativeWindowHandle):
            return Status.MAXIMIZED
        elif IsWindowVisible(control.NativeWindowHandle):
            return Status.NORMAL
        else:
            return Status.HIDDEN
    
    def get_cursor_location(self)->tuple[int,int]:
        position=pyautogui.position()
        return (position.x,position.y)
    
    def get_element_under_cursor(self)->Control:
        return ControlFromCursor()
    
    def get_apps_from_start_menu(self)->dict[str,str]:
        command='Get-StartApps | ConvertTo-Csv -NoTypeInformation'
        apps_info,_=self.execute_command(command)
        reader=csv.DictReader(io.StringIO(apps_info))
        return {row.get('Name').lower():row.get('AppID') for row in reader}
    
    def execute_command(self,command:str)->tuple[str,int]:
        try:
            result = subprocess.run(
                ['powershell', '-NoProfile', '-Command', command], 
                capture_output=True, 
                errors='ignore',
                timeout=25,
                cwd=os.path.expanduser(path='~')
            )
            stdout=result.stdout
            stderr=result.stderr
            return (stdout or stderr,result.returncode)
        except subprocess.TimeoutExpired:
            return ('Command execution timed out', 1)
        except Exception as e:
            return ('Command execution failed', 1)
        
    def is_app_browser(self,node:Control):
        process=Process(node.ProcessId)
        return process.name() in BROWSER_NAMES
    
    def get_default_language(self)->str:
        command="Get-Culture | Select-Object Name,DisplayName | ConvertTo-Csv -NoTypeInformation"
        response,_=self.execute_command(command)
        reader=csv.DictReader(io.StringIO(response))
        return "".join([row.get('DisplayName') for row in reader])
    
    def resize_app(self,size:tuple[int,int]=None,loc:tuple[int,int]=None)->tuple[str,int]:
        self.get_state()
        active_app=self.desktop_state.active_app
        if active_app is None:
            return "No active app found",1
        if active_app.status==Status.MINIMIZED:
            return f"{active_app.name} is minimized",1
        elif active_app.status==Status.MAXIMIZED:
            return f"{active_app.name} is maximized",1
        else:
            app_control=ControlFromHandle(active_app.handle)
            if loc is None:
                x=app_control.BoundingRectangle.left
                y=app_control.BoundingRectangle.top
                loc=(x,y)
            if size is None:
                width=app_control.BoundingRectangle.width()
                height=app_control.BoundingRectangle.height()
                size=(width,height)
            x,y=loc
            width,height=size
            app_control.MoveWindow(x,y,width,height)
            return (f'{active_app.name} resized to {width}x{height} at {x},{y}.',0)
    
    def is_app_running(self,name:str)->bool:
        apps={app.name:app for app in [self.desktop_state.active_app]+self.desktop_state.apps if app is not None}
        return process.extractOne(name,list(apps.keys()),score_cutoff=60) is not None
        
    def launch_app(self,name:str)->tuple[str,int]:
        apps_map=self.get_apps_from_start_menu()
        matched_app=process.extractOne(name,apps_map.keys(),score_cutoff=70)
        if matched_app is None:
            return (f'{name.title()} not found in start menu.',1)
        app_name,_=matched_app
        appid=apps_map.get(app_name)
        if appid is None:
            return (name,f'{name.title()} not found in start menu.',1)
        if name.endswith('.exe'):
            response,status=self.execute_command(f'Start-Process {appid}')
        else:
            response,status=self.execute_command(f'Start-Process shell:AppsFolder\\{appid}')
        return response,status
    
    def switch_app(self,name:str):
        self.get_state()
        apps={app.name:app for app in [self.desktop_state.active_app]+self.desktop_state.apps if app is not None}
        matched_app:Optional[tuple[str,float]]=process.extractOne(name,list(apps.keys()),score_cutoff=70)
        if matched_app is None:
            return (f'Application {name.title()} not found.',1)
        app_name,_=matched_app
        app=apps.get(app_name)
        if IsIconic(app.handle):
            ShowWindow(app.handle, cmdShow=9)
            return (f'{app_name.title()} restored from Minimized state.',0)
        else:
            from pywinauto import Application
            app=Application().connect(handle=app.handle)
            app.window().set_focus()
            return (f'Switched to {app_name.title()} window.',0)
    
    def get_app_size(self,control:Control):
        window=control.BoundingRectangle
        if window.isempty():
            return Size(width=0,height=0)
        return Size(width=window.width(),height=window.height())
    
    def get_app_size_by_hwnd(self,hwnd)->Size:
        rect = RECT()
        ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(ctypes.cast(rect, ctypes.POINTER(RECT))))
        width = rect.right - rect.left
        height = rect.bottom - rect.top
        # When the window is maximized, the size is calculated inaccurately
        return Size(width=width,height=height)
    
    def is_app_visible(self,app)->bool:
        is_minimized=self.get_app_status(app)!=Status.MINIMIZED
        size=self.get_app_size(app)
        area=size.width*size.height
        is_overlay=self.is_overlay_app(app)
        return not is_overlay and is_minimized and area>10
    
    def is_overlay_app(self,element:Control) -> bool:
        no_children = len(element.GetChildren()) == 0
        is_name = "Overlay" in element.Name.strip()
        return no_children or is_name
        
    def get_apps(self) -> tuple[App|None,list[App]]:
        try:
            sleep(0.5)
            desktop = GetRootControl()  # Get the desktop control
            elements = desktop.GetChildren()
            apps = []
            for depth, element in enumerate(elements):
                if element.ClassName in EXCLUDED_APPS or element.ClassName in AVOIDED_APPS or self.is_overlay_app(element):
                    continue
                if element.ControlType in [ControlType.WindowControl, ControlType.PaneControl]:
                    status = self.get_app_status(element)
                    size=self.get_app_size(element)
                    apps.append(App(name=element.Name, depth=depth, status=status,size=size,handle=element.NativeWindowHandle))
        except Exception as ex:
            print(f"Error: {ex}")
            apps = []

        active_app=self.get_active_app(apps)
        apps=apps[1:] if len(apps)>1 else []
        return (active_app,apps)
    
    def get_windows_version(self)->str:
        response,status=self.execute_command("(Get-CimInstance Win32_OperatingSystem).Caption")
        if status==0:
            return response.strip()
        return "Windows"
    
    def get_user_account_type(self)->str:
        response,status=self.execute_command("(Get-LocalUser -Name $env:USERNAME).PrincipalSource")
        return "Local Account" if response.strip()=='Local' else "Microsoft Account" if status==0 else "Local Account"
    
    def get_dpi_scaling(self):
        user32 = ctypes.windll.user32
        dpi = user32.GetDpiForSystem()
        return dpi / 96.0
    
    def get_screen_resolution(self)->Size:
        user32 = ctypes.windll.user32
        width = user32.GetSystemMetrics(0)
        height = user32.GetSystemMetrics(1)
        return Size(width=width,height=height)
    
    def screenshot_in_bytes(self,screenshot:PILImage)->bytes:
        buffer=BytesIO()
        screenshot.save(buffer,format='PNG')
        return buffer.getvalue()

    def get_screenshot(self,scale:float=0.7)->Image.Image:
        screenshot=pyautogui.screenshot()
        size=(screenshot.width*scale, screenshot.height*scale)
        screenshot.thumbnail(size=size, resample=Image.Resampling.LANCZOS)
        return screenshot
    
    @contextmanager
    def auto_minimize(self):
        SW_MINIMIZE=6
        SW_RESTORE = 9
        try:
            user32 = ctypes.windll.user32
            hWnd = user32.GetForegroundWindow()
            user32.ShowWindow(hWnd, SW_MINIMIZE)
            yield
        finally:
            user32.ShowWindow(hWnd, SW_RESTORE)
