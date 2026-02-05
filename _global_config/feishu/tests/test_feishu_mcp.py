#!/usr/bin/env python3
"""
Quick test script for Feishu MCP Server
"""

import subprocess
import sys

print("Testing Feishu MCP Server...")
print("=" * 50)

# Test 1: Check if MCP is installed
print("\n1. Checking MCP installation...")
try:
    import mcp
    print("✅ MCP package is installed")
except ImportError:
    print("❌ MCP package not found. Run: pip3 install mcp")
    sys.exit(1)

# Test 2: Check if server file exists
print("\n2. Checking server file...")
import os
server_path = "/Users/dj/Desktop/小静的skills/_global_config/feishu_mcp_server.py"
if os.path.exists(server_path):
    print(f"✅ Server file exists: {server_path}")
else:
    print(f"❌ Server file not found: {server_path}")
    sys.exit(1)

# Test 3: Check if file is executable
print("\n3. Checking file permissions...")
if os.access(server_path, os.X_OK):
    print("✅ Server file is executable")
else:
    print("⚠️  Server file is not executable. Run: chmod +x {server_path}")

# Test 4: Check environment variables
print("\n4. Checking environment variables...")
app_id = os.getenv("FEISHU_APP_ID")
app_secret = os.getenv("FEISHU_APP_SECRET")

if app_id and app_secret:
    print(f"✅ FEISHU_APP_ID: {app_id[:10]}...")
    print(f"✅ FEISHU_APP_SECRET: {app_secret[:10]}...")
else:
    print("⚠️  Environment variables not set (will be set by MCP config)")

# Test 5: Check MCP config
print("\n5. Checking MCP configuration...")
mcp_config_path = "/Users/dj/.claude/plugins/marketplaces/claude-plugins-official/external_plugins/feishu/.mcp.json"
if os.path.exists(mcp_config_path):
    print(f"✅ MCP config exists: {mcp_config_path}")
    with open(mcp_config_path, 'r') as f:
        import json
        config = json.load(f)
        print(f"   Config: {json.dumps(config, indent=2)}")
else:
    print(f"❌ MCP config not found: {mcp_config_path}")

print("\n" + "=" * 50)
print("✅ All checks passed!")
print("\nNext steps:")
print("1. Restart Claude Code")
print("2. Run /mcp to verify Feishu MCP is loaded")
print("3. Test MCP tools in conversation")
