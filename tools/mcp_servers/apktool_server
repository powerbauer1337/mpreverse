#!/usr/bin/env python3
"""
Simple Apktool MCP Server for APK decompilation and analysis
"""

import asyncio
import json
import logging
import os
import subprocess
import sys
from typing import Any, Dict, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleApktoolMCPServer:
    def __init__(self):
        self.tools = [
            {
                "name": "decompile_apk",
                "description": "Decompile an APK file using apktool",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "apk_path": {
                            "type": "string",
                            "description": "Path to the APK file"
                        },
                        "output_dir": {
                            "type": "string",
                            "description": "Output directory for decompiled files"
                        }
                    },
                    "required": ["apk_path"]
                }
            },
            {
                "name": "analyze_manifest",
                "description": "Analyze AndroidManifest.xml from decompiled APK",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "decompiled_dir": {
                            "type": "string",
                            "description": "Path to decompiled APK directory"
                        }
                    },
                    "required": ["decompiled_dir"]
                }
            }
        ]

    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP requests"""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")

        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "apktool-mcp-server",
                        "version": "1.0.0"
                    }
                }
            }
        
        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "tools": self.tools
                }
            }
        
        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            try:
                if tool_name == "decompile_apk":
                    result = await self.decompile_apk(arguments)
                elif tool_name == "analyze_manifest":
                    result = await self.analyze_manifest(arguments)
                else:
                    result = {"error": f"Unknown tool: {tool_name}"}
                
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": result.get("text", str(result))
                            }
                        ]
                    }
                }
            except Exception as e:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -1,
                        "message": str(e)
                    }
                }
        
        else:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }

    async def decompile_apk(self, arguments: Dict[str, Any]) -> Dict[str, str]:
        """Decompile APK using apktool"""
        apk_path = arguments["apk_path"]
        output_dir = arguments.get("output_dir", f"{apk_path}_decompiled")
        
        if not os.path.exists(apk_path):
            return {"text": f"APK file not found: {apk_path}"}
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Build apktool command
        cmd = ["apktool", "d", apk_path, "-o", output_dir, "-f"]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return {
                "text": f"Successfully decompiled APK to {output_dir}\n\nOutput:\n{result.stdout}"
            }
        except subprocess.CalledProcessError as e:
            return {
                "text": f"Failed to decompile APK: {e.stderr}"
            }

    async def analyze_manifest(self, arguments: Dict[str, Any]) -> Dict[str, str]:
        """Analyze AndroidManifest.xml"""
        decompiled_dir = arguments["decompiled_dir"]
        manifest_path = os.path.join(decompiled_dir, "AndroidManifest.xml")
        
        if not os.path.exists(manifest_path):
            return {"text": f"AndroidManifest.xml not found in {decompiled_dir}"}
        
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Basic analysis
            analysis = []
            analysis.append("## AndroidManifest.xml Analysis")
            analysis.append(f"**File Size:** {len(content)} bytes")
            analysis.append(f"**Location:** {manifest_path}")
            
            # Extract package name
            if 'package=' in content:
                package_start = content.find('package="') + 9
                package_end = content.find('"', package_start)
                package_name = content[package_start:package_end]
                analysis.append(f"**Package Name:** {package_name}")
            
            # Count activities
            activity_count = content.count('<activity')
            analysis.append(f"**Activities:** {activity_count}")
            
            # Count services
            service_count = content.count('<service')
            analysis.append(f"**Services:** {service_count}")
            
            # Count permissions
            permission_count = content.count('<uses-permission')
            analysis.append(f"**Permissions:** {permission_count}")
            
            return {"text": "\n".join(analysis)}
        except Exception as e:
            return {"text": f"Error analyzing manifest: {str(e)}"}

async def main():
    """Main function"""
    server = SimpleApktoolMCPServer()
    
    # Read from stdin, write to stdout
    while True:
        try:
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            if not line:
                break
            
            request = json.loads(line.strip())
            response = await server.handle_request(request)
            
            await asyncio.get_event_loop().run_in_executor(
                None, lambda: sys.stdout.write(json.dumps(response) + "\n")
            )
            await asyncio.get_event_loop().run_in_executor(None, sys.stdout.flush)
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON: {e}")
        except Exception as e:
            logger.error(f"Error processing request: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 