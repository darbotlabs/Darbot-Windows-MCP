#!/usr/bin/env python3
"""
Quick tool to inspect MCP tool schemas and identify compliance issues
"""
import json
from main import mcp

def inspect_tools():
    """Inspect the current tool definitions for schema compliance issues."""
    print("🔍 Inspecting MCP tool schemas...")
    
    try:
        # Get tools from the MCP instance
        tools = []
        for tool_name, tool_func in mcp._tools.items():
            # Get the function signature and annotations
            import inspect
            sig = inspect.signature(tool_func)
            
            print(f"\n📋 Tool: {tool_name}")
            print(f"   Parameters: {list(sig.parameters.keys())}")
            
            for param_name, param in sig.parameters.items():
                print(f"   - {param_name}: {param.annotation}")
        
        print("\n✅ Tool inspection complete")
        
    except Exception as e:
        print(f"❌ Error inspecting tools: {e}")

if __name__ == "__main__":
    inspect_tools()
