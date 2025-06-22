#!/usr/bin/env python3
"""
Test script to verify MCP servers are working correctly
"""

import asyncio
import json
import subprocess
import sys
from pathlib import Path

async def test_mcp_server(server_name: str, server_path: str, server_file: str):
    """Test an MCP server by sending initialization and tools/list requests"""
    print(f"\n🧪 Testing {server_name}...")
    
    # Test initialization
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {}
    }
    
    try:
        # Send initialization request
        result = subprocess.run(
            ["python", server_file],
            input=json.dumps(init_request) + "\n",
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            cwd=server_path,
            timeout=10
        )
        
        if result.returncode != 0:
            print(f"❌ {server_name} failed to start: {result.stderr}")
            return False
        
        # Parse response
        response = json.loads(result.stdout.strip())
        if "result" in response and "serverInfo" in response["result"]:
            server_info = response["result"]["serverInfo"]
            print(f"✅ {server_name} initialized: {server_info['name']} v{server_info['version']}")
        else:
            print(f"❌ {server_name} invalid initialization response")
            return False
        
        # Test tools listing
        tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        
        result = subprocess.run(
            ["python", server_file],
            input=json.dumps(tools_request) + "\n",
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            cwd=server_path,
            timeout=10
        )
        
        if result.returncode != 0:
            print(f"❌ {server_name} tools/list failed: {result.stderr}")
            return False
        
        # Parse tools response
        response = json.loads(result.stdout.strip())
        if "result" in response and "tools" in response["result"]:
            tools = response["result"]["tools"]
            print(f"✅ {server_name} has {len(tools)} tools:")
            for tool in tools:
                print(f"   - {tool['name']}: {tool['description']}")
        else:
            print(f"❌ {server_name} invalid tools response")
            return False
        
        return True
        
    except subprocess.TimeoutExpired:
        print(f"❌ {server_name} timed out")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ {server_name} invalid JSON response: {e}")
        return False
    except Exception as e:
        print(f"❌ {server_name} error: {e}")
        return False

async def main():
    """Test all MCP servers"""
    print("🚀 Testing MCP Servers")
    print("=" * 50)
    
    # Test apktool MCP server
    apktool_success = await test_mcp_server(
        "Apktool MCP Server",
        "tools/apktool-mcp-server",
        "apktool_mcp_server.py"
    )
    
    # Test JADX MCP server
    jadx_success = await test_mcp_server(
        "JADX AI MCP Server",
        "tools/jadx-ai-mcp",
        "jadx_ai_mcp.py"
    )
    
    # Test Review Gate V2 MCP server
    review_gate_success = await test_mcp_server(
        "Review Gate V2 MCP Server",
        "Review-Gate-main/V2",
        "review_gate_v2_mcp.py"
    )
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"   Apktool MCP Server: {'✅ PASS' if apktool_success else '❌ FAIL'}")
    print(f"   JADX AI MCP Server: {'✅ PASS' if jadx_success else '❌ FAIL'}")
    print(f"   Review Gate V2 MCP Server: {'✅ PASS' if review_gate_success else '❌ FAIL'}")
    
    total_tests = 3
    passed_tests = sum([apktool_success, jadx_success, review_gate_success])
    
    print(f"\n🎯 Overall: {passed_tests}/{total_tests} servers working")
    
    if passed_tests == total_tests:
        print("🎉 All MCP servers are working correctly!")
        return 0
    else:
        print("⚠️ Some MCP servers have issues. Check the output above.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code) 