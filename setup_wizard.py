#!/usr/bin/env python3
"""
Darbot-Windows-MCP Installation Wizard
Interactive setup and configuration tool
"""
import sys
import os
import subprocess
import json
from pathlib import Path
from platform import system
from textwrap import dedent

def print_header():
    print("""
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                        🪟 Darbot-Windows-MCP Setup Wizard                     ║
    ║                                                                              ║
    ║         Lightweight MCP Server for Windows Desktop Automation               ║
    ║                           Darbot Labs Edition                               ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
    """)

def check_system_requirements():
    """Check if system meets requirements."""
    print("🔍 Checking system requirements...")
    
    issues = []
    warnings = []
    
    # Check OS
    os_name = system()
    print(f"   Operating System: {os_name}")
    if os_name != 'Windows':
        warnings.append(f"Running on {os_name}. Some features may be limited.")
    
    # Check Python version
    python_version = sys.version_info
    print(f"   Python Version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    if python_version < (3, 8):
        issues.append("Python 3.8+ required")
    elif python_version < (3, 13):
        warnings.append("Python 3.13+ recommended for best performance")
    
    # Check UV
    try:
        result = subprocess.run(['uv', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   UV Package Manager: {result.stdout.strip()}")
        else:
            issues.append("UV package manager not found")
    except FileNotFoundError:
        issues.append("UV package manager not found")
    
    if issues:
        print("\n❌ Critical issues found:")
        for issue in issues:
            print(f"   - {issue}")
        return False
    
    if warnings:
        print("\n⚠️  Warnings:")
        for warning in warnings:
            print(f"   - {warning}")
    
    print("✅ System requirements check passed")
    return True

def install_uv():
    """Install UV package manager if missing."""
    print("\n📦 Installing UV package manager...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'uv'], check=True)
        print("✅ UV installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install UV: {e}")
        return False

def install_dependencies():
    """Install project dependencies."""
    print("\n📦 Installing project dependencies...")
    try:
        subprocess.run(['uv', 'sync'], check=True, cwd=Path.cwd())
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def test_installation():
    """Test if installation is working."""
    print("\n🧪 Testing installation...")
    try:
        result = subprocess.run(['uv', 'run', 'python', '-c', 'from main import mcp; print("✅ Import successful")'], 
                              capture_output=True, text=True, cwd=Path.cwd())
        if result.returncode == 0:
            print("✅ Installation test passed")
            return True
        else:
            print(f"❌ Installation test failed: {result.stderr}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Installation test failed: {e}")
        return False

def get_mcp_client_choice():
    """Get user's preferred MCP client."""
    print("\n🎯 Choose your MCP client:")
    print("1. Claude Desktop (Anthropic)")
    print("2. Gemini CLI (Google)")
    print("3. Other/Manual configuration")
    print("4. Skip client configuration")
    
    while True:
        choice = input("\nEnter your choice (1-4): ").strip()
        if choice in ['1', '2', '3', '4']:
            return choice
        print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")

def configure_claude_desktop():
    """Provide configuration instructions for Claude Desktop."""
    config_path = None
    home_dir = Path.home()
    
    # Try to find Claude Desktop config
    if system() == 'Windows':
        config_path = home_dir / "AppData" / "Roaming" / "Claude" / "claude_desktop_config.json"
    elif system() == 'Darwin':  # macOS
        config_path = home_dir / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    else:  # Linux and others
        config_path = home_dir / ".config" / "Claude" / "claude_desktop_config.json"
    
    current_dir = Path.cwd().resolve()
    
    config = {
        "mcpServers": {
            "darbot-windows-mcp": {
                "command": "uv",
                "args": [
                    "--directory",
                    str(current_dir),
                    "run",
                    "main.py"
                ]
            }
        }
    }
    
    print(f"\n📝 Claude Desktop Configuration:")
    print(f"   Config file location: {config_path}")
    print(f"   Current directory: {current_dir}")
    
    if config_path.exists():
        print("\n⚠️  Existing configuration found.")
        choice = input("Backup existing config and update? (y/N): ").strip().lower()
        if choice == 'y':
            # Backup existing config
            backup_path = config_path.with_suffix('.backup.json')
            config_path.rename(backup_path)
            print(f"   ✅ Backed up to: {backup_path}")
    
    print("\n📄 Add this configuration to your Claude Desktop config:")
    print(json.dumps(config, indent=2))
    
    if input("\nWould you like me to create/update the config file? (y/N): ").strip().lower() == 'y':
        try:
            config_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Read existing config if it exists
            existing_config = {}
            if config_path.exists():
                with open(config_path, 'r') as f:
                    existing_config = json.load(f)
            
            # Merge configurations
            if 'mcpServers' not in existing_config:
                existing_config['mcpServers'] = {}
            existing_config['mcpServers'].update(config['mcpServers'])
            
            # Write updated config
            with open(config_path, 'w') as f:
                json.dump(existing_config, f, indent=2)
            
            print("✅ Configuration updated successfully!")
            print("   Restart Claude Desktop to apply changes.")
            
        except Exception as e:
            print(f"❌ Failed to update config: {e}")
            print("   Please manually add the configuration above.")

def configure_gemini_cli():
    """Provide configuration instructions for Gemini CLI."""
    home_dir = Path.home()
    config_path = home_dir / ".gemini" / "settings.json"
    current_dir = Path.cwd().resolve()
    
    config_snippet = {
        "mcpServers": {
            "darbot-windows-mcp": {
                "command": "uv",
                "args": [
                    "--directory",
                    str(current_dir),
                    "run",
                    "main.py"
                ]
            }
        }
    }
    
    print(f"\n📝 Gemini CLI Configuration:")
    print(f"   Config file location: {config_path}")
    print(f"   Current directory: {current_dir}")
    print(f"\n📄 Add this to your Gemini CLI settings.json:")
    print(json.dumps(config_snippet, indent=2))

def show_manual_config():
    """Show manual configuration instructions."""
    current_dir = Path.cwd().resolve()
    
    print(f"\n📝 Manual Configuration:")
    print(f"   Project directory: {current_dir}")
    print(f"   Start command: uv --directory {current_dir} run main.py")
    print(f"   Server name: darbot-windows-mcp")
    
    print("\n📄 Generic MCP client configuration:")
    print(json.dumps({
        "command": "uv",
        "args": [
            "--directory",
            str(current_dir),
            "run",
            "main.py"
        ]
    }, indent=2))

def show_completion_info():
    """Show completion information and next steps."""
    print(dedent("""
    🎉 Installation Complete!
    
    ✅ Next Steps:
    1. Restart your MCP client (Claude Desktop, Gemini CLI, etc.)
    2. Look for the "darbot-windows-mcp" server in your client
    3. Try basic commands like taking a screenshot or getting desktop state
    
    🛠️  Available Tools:
    - Launch-Tool: Launch applications
    - State-Tool: Capture desktop state
    - Click-Tool, Type-Tool: UI interaction
    - Scroll-Tool, Drag-Tool: Navigation
    - Clipboard-Tool: Copy/paste operations
    - PowerShell-Tool: Execute commands
    - And more...
    
    📚 Documentation:
    - README.md: Basic usage and examples
    - bug_bash_results.md: Known issues and improvements
    
    🐛 Issues or Questions?
    - Check: https://github.com/darbotlabs/Darbot-Windows-MCP/issues
    - Discord: https://discord.gg/darbotlabs
    
    Happy automating! 🚀
    """))

def main():
    """Main installation wizard."""
    print_header()
    
    # Check system requirements
    if not check_system_requirements():
        print("\n❌ System requirements not met.")
        if input("Try to fix issues automatically? (y/N): ").strip().lower() == 'y':
            if not install_uv():
                print("❌ Unable to fix critical issues. Please install UV manually:")
                print("   Recommended steps:")
                print("   1. Ensure you have Python and pip installed.")
                print("   2. Use a virtual environment to avoid permission issues:")
                print("      python -m venv venv && source venv/bin/activate")
                print("   3. Install UV using pip:")
                print("      pip install uv")
                print("   4. If you encounter network restrictions, try offline installation:")
                print("      Download the UV package from PyPI and install it locally:")
                print("      pip install /path/to/uv-package.whl")
                print("   For more help, visit: https://github.com/darbotlabs/Darbot-Windows-MCP/issues")
                return 1
        else:
            return 1
    
    print("\n" + "="*80)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies. Please check your setup.")
        return 1
    
    print("\n" + "="*80)
    
    # Test installation
    if not test_installation():
        print("❌ Installation test failed. Please check the error messages above.")
        return 1
    
    print("\n" + "="*80)
    
    # Configure MCP client
    client_choice = get_mcp_client_choice()
    
    if client_choice == '1':
        configure_claude_desktop()
    elif client_choice == '2':
        configure_gemini_cli()
    elif client_choice == '3':
        show_manual_config()
    else:
        print("⏭️  Skipping client configuration")
    
    print("\n" + "="*80)
    
    # Show completion info
    show_completion_info()
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⏹️  Installation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)