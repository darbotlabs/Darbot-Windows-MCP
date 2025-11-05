#!/usr/bin/env python3
"""
Configuration Validator for Darbot-Windows-MCP
Validates MCP client configurations and provides fixes
"""
import json
import sys
from pathlib import Path
from platform import system
from typing import Dict, List, Tuple, Optional

class ConfigValidator:
    """Validates and fixes MCP client configurations."""
    
    def __init__(self):
        self.project_dir = Path.cwd().resolve()
        self.os_name = system()
        self.issues_found = []
        self.warnings = []
    
    def get_claude_config_path(self) -> Path:
        """Get the Claude Desktop configuration file path."""
        home = Path.home()
        
        if self.os_name == 'Windows':
            return home / "AppData" / "Roaming" / "Claude" / "claude_desktop_config.json"
        elif self.os_name == 'Darwin':  # macOS
            return home / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
        else:  # Linux and others
            return home / ".config" / "Claude" / "claude_desktop_config.json"
    
    def get_gemini_config_path(self) -> Path:
        """Get the Gemini CLI configuration file path."""
        return Path.home() / ".gemini" / "settings.json"
    
    def get_expected_config(self) -> Dict:
        """Get the expected MCP server configuration."""
        return {
            "darbot-windows-mcp": {
                "command": "uv",
                "args": [
                    "--directory",
                    str(self.project_dir),
                    "run",
                    "main.py"
                ]
            }
        }
    
    def validate_json_file(self, file_path: Path) -> Tuple[bool, Optional[Dict]]:
        """Validate that a file contains valid JSON."""
        if not file_path.exists():
            return False, None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return True, config
        except json.JSONDecodeError as e:
            self.issues_found.append(f"Invalid JSON in {file_path}: {e}")
            return False, None
        except Exception as e:
            self.issues_found.append(f"Error reading {file_path}: {e}")
            return False, None
    
    def validate_mcp_server_config(self, config: Dict, server_name: str = "darbot-windows-mcp") -> bool:
        """Validate the MCP server configuration structure."""
        if "mcpServers" not in config:
            self.issues_found.append("Missing 'mcpServers' section in configuration")
            return False
        
        if server_name not in config["mcpServers"]:
            self.issues_found.append(f"Missing '{server_name}' server configuration")
            return False
        
        server_config = config["mcpServers"][server_name]
        expected_config = self.get_expected_config()[server_name]
        
        # Check command
        if server_config.get("command") != expected_config["command"]:
            self.issues_found.append(f"Incorrect command: expected '{expected_config['command']}', got '{server_config.get('command')}'")
        
        # Check args
        if server_config.get("args") != expected_config["args"]:
            self.warnings.append(f"Arguments may be incorrect or using different path")
        
        return len(self.issues_found) == 0
    
    def validate_claude_desktop(self) -> bool:
        """Validate Claude Desktop configuration."""
        print("🔍 Validating Claude Desktop configuration...")
        
        config_path = self.get_claude_config_path()
        print(f"   Config path: {config_path}")
        
        is_valid, config = self.validate_json_file(config_path)
        if not is_valid:
            if config_path.exists():
                return False
            else:
                self.warnings.append(f"Claude Desktop config not found: {config_path}")
                return True  # Not an error if Claude isn't installed
        
        return self.validate_mcp_server_config(config)
    
    def validate_gemini_cli(self) -> bool:
        """Validate Gemini CLI configuration."""
        print("🔍 Validating Gemini CLI configuration...")
        
        config_path = self.get_gemini_config_path()
        print(f"   Config path: {config_path}")
        
        is_valid, config = self.validate_json_file(config_path)
        if not is_valid:
            if config_path.exists():
                return False
            else:
                self.warnings.append(f"Gemini CLI config not found: {config_path}")
                return True  # Not an error if Gemini isn't installed
        
        return self.validate_mcp_server_config(config)
    
    def fix_claude_desktop_config(self) -> bool:
        """Fix Claude Desktop configuration."""
        config_path = self.get_claude_config_path()
        expected_config = self.get_expected_config()
        
        try:
            # Create directory if it doesn't exist
            config_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Read existing config or create new one
            existing_config = {}
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    try:
                        existing_config = json.load(f)
                    except json.JSONDecodeError:
                        print("   ⚠️  Existing config has invalid JSON, creating backup...")
                        backup_path = config_path.with_suffix('.backup.json')
                        config_path.rename(backup_path)
                        existing_config = {}
            
            # Merge configurations
            if "mcpServers" not in existing_config:
                existing_config["mcpServers"] = {}
            
            existing_config["mcpServers"].update(expected_config)
            
            # Write updated config
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(existing_config, f, indent=2)
            
            print(f"   ✅ Fixed Claude Desktop configuration")
            return True
            
        except Exception as e:
            self.issues_found.append(f"Failed to fix Claude Desktop config: {e}")
            return False
    
    def fix_gemini_cli_config(self) -> bool:
        """Fix Gemini CLI configuration."""
        config_path = self.get_gemini_config_path()
        expected_config = self.get_expected_config()
        
        try:
            # Create directory if it doesn't exist
            config_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Read existing config or create new one
            existing_config = {}
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    try:
                        existing_config = json.load(f)
                    except json.JSONDecodeError:
                        print("   ⚠️  Existing config has invalid JSON, creating backup...")
                        backup_path = config_path.with_suffix('.backup.json')
                        config_path.rename(backup_path)
                        existing_config = {}
            
            # Merge configurations
            if "mcpServers" not in existing_config:
                existing_config["mcpServers"] = {}
            
            existing_config["mcpServers"].update(expected_config)
            
            # Write updated config
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(existing_config, f, indent=2)
            
            print(f"   ✅ Fixed Gemini CLI configuration")
            return True
            
        except Exception as e:
            self.issues_found.append(f"Failed to fix Gemini CLI config: {e}")
            return False
    
    def validate_project_setup(self) -> bool:
        """Validate the project setup."""
        print("🔍 Validating project setup...")
        
        # Check main.py exists
        main_py = self.project_dir / "main.py"
        if not main_py.exists():
            self.issues_found.append("main.py not found in current directory")
            return False
        
        # Check UV is available
        import subprocess
        try:
            result = subprocess.run(['uv', '--version'], capture_output=True, text=True)
            if result.returncode != 0:
                self.issues_found.append("UV package manager not working properly")
                return False
        except FileNotFoundError:
            self.issues_found.append("UV package manager not found")
            return False
        
        # Test import
        try:
            result = subprocess.run([
                'uv', 'run', 'python', '-c', 'from main import mcp; print("OK")'
            ], capture_output=True, text=True, cwd=self.project_dir)
            
            if result.returncode != 0:
                error_message = f"Failed to import MCP server: {result.stderr}"
                self.issues_found.append(error_message)
                print(f"❌ {error_message}")
                return False
                
        except Exception as e:
            error_message = f"Failed to test import: {e}"
            self.issues_found.append(error_message)
            print(f"❌ {error_message}")
            return False
        
        print("   ✅ Project setup valid")
        return True
    
    def run_validation(self) -> bool:
        """Run complete validation."""
        print("🔧 Darbot-Windows-MCP Configuration Validator")
        print("=" * 60)
        
        self.issues_found.clear()
        self.warnings.clear()
        
        # Validate project setup
        project_valid = self.validate_project_setup()
        
        # Validate client configurations
        claude_valid = self.validate_claude_desktop()
        gemini_valid = self.validate_gemini_cli()
        
        # Report results
        print("\n📊 Validation Results:")
        print("-" * 30)
        
        if project_valid:
            print("✅ Project setup: Valid")
        else:
            print("❌ Project setup: Issues found")
        
        if claude_valid:
            print("✅ Claude Desktop: Valid")
        else:
            print("❌ Claude Desktop: Issues found")
        
        if gemini_valid:
            print("✅ Gemini CLI: Valid")
        else:
            print("❌ Gemini CLI: Issues found")
        
        # Show issues
        if self.issues_found:
            print("\n❌ Issues Found:")
            for issue in self.issues_found:
                print(f"   - {issue}")
        
        if self.warnings:
            print("\n⚠️  Warnings:")
            for warning in self.warnings:
                print(f"   - {warning}")
        
        return len(self.issues_found) == 0
    
    def run_fixes(self) -> bool:
        """Run automatic fixes."""
        print("\n🔧 Applying Fixes...")
        print("-" * 30)
        
        fixes_applied = 0
        
        # Try to fix Claude Desktop config
        try:
            if self.fix_claude_desktop_config():
                fixes_applied += 1
        except Exception as e:
            print(f"   ❌ Failed to fix Claude Desktop: {e}")
        
        # Try to fix Gemini CLI config
        try:
            if self.fix_gemini_cli_config():
                fixes_applied += 1
        except Exception as e:
            print(f"   ❌ Failed to fix Gemini CLI: {e}")
        
        print(f"\n✅ Applied {fixes_applied} fixes")
        
        # Re-run validation
        print("\n🔍 Re-running validation...")
        return self.run_validation()

def main():
    """Main function."""
    validator = ConfigValidator()
    
    # Run initial validation
    is_valid = validator.run_validation()
    
    if not is_valid:
        print(f"\n🚨 Found {len(validator.issues_found)} issues")
        
        if input("\nWould you like to apply automatic fixes? (y/N): ").strip().lower() == 'y':
            validator.run_fixes()
        else:
            print("\n💡 To fix manually:")
            print("   1. Run setup wizard: python setup_wizard.py")
            print("   2. Check troubleshooting guide: TROUBLESHOOTING.md")
            return 1
    else:
        print("\n🎉 All configurations are valid!")
        print("\n✅ Your MCP server should work correctly with configured clients")
        print("   Remember to restart your MCP clients to apply any changes")
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⏹️  Validation cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)