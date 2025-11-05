from typing import Set

BROWSER_NAMES=set(['msedge.exe','chrome.exe','firefox.exe'])

# Configurable avoided apps - can be customized based on use case
AVOIDED_APPS:Set[str]=set([
    'AgentUI',  # AI agent interfaces (main version)
    'Recording toolbar'  # Media recording tools (copy version)
])

# Comprehensive exclusion list with essential Windows UI components
EXCLUDED_APPS:Set[str]=set([
    'Progman','Shell_TrayWnd','Shell_SecondaryTrayWnd',
    'Microsoft.UI.Content.PopupWindowSiteBridge',
    'Windows.UI.Core.CoreWindow',
    'Program Manager', 'Taskbar'  # Added from copy for broader compatibility
])

PROCESS_PER_MONITOR_DPI_AWARE = 2