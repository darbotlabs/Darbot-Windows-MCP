#!/usr/bin/env python3
"""
Diagnostic script to examine MCP tool schemas
"""
import json
from main import mcp

def diagnose_tools():
    """Examine the current tool schemas to identify compliance issues."""
    print("🔍 Diagnosing MCP tool schemas...")
    
    try:
        # Get tools from FastMCP
        tools = mcp.get_tools()
        
        print(f"Found {len(tools)} tools:")
        
        for tool in tools:
            name = tool.get('name', 'Unknown')
            print(f"\n📋 Tool: {name}")
            
            # Check input schema
            input_schema = tool.get('inputSchema', {})
            if input_schema:
                print(f"   Input Schema Type: {input_schema.get('type', 'Missing')}")
                
                # Check for array type without items
                if input_schema.get('type') == 'array':
                    if 'items' not in input_schema or not input_schema['items']:
                        print(f"   ❌ ERROR: Array type missing 'items' field!")
                    else:
                        print(f"   ✅ Array has items: {input_schema['items']}")
                
                # Print full schema for debugging
                print(f"   Full Schema: {json.dumps(input_schema, indent=4)}")
            else:
                print("   ❌ No input schema found!")
                
    except Exception as e:
        print(f"❌ Error diagnosing tools: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    diagnose_tools()
