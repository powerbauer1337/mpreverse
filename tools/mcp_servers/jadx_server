#!/usr/bin/env python3
"""
Simple JADX MCP Server for Java decompilation and analysis
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

class SimpleJadxMCPServer:
    def __init__(self):
        self.tools = [
            {
                "name": "decompile_apk",
                "description": "Decompile an APK file using JADX",
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
                        },
                        "format": {
                            "type": "string",
                            "enum": ["java", "kotlin"],
                            "description": "Output format (java or kotlin)",
                            "default": "java"
                        }
                    },
                    "required": ["apk_path"]
                }
            },
            {
                "name": "analyze_java_files",
                "description": "Analyze Java source files from decompiled APK",
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
            },
            {
                "name": "find_classes",
                "description": "Find and list Java classes in decompiled APK",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "decompiled_dir": {
                            "type": "string",
                            "description": "Path to decompiled APK directory"
                        },
                        "pattern": {
                            "type": "string",
                            "description": "Pattern to search for in class names"
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
                        "name": "jadx-ai-mcp",
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
                elif tool_name == "analyze_java_files":
                    result = await self.analyze_java_files(arguments)
                elif tool_name == "find_classes":
                    result = await self.find_classes(arguments)
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
        """Decompile APK using JADX"""
        apk_path = arguments["apk_path"]
        output_dir = arguments.get("output_dir", f"{apk_path}_jadx")
        format_type = arguments.get("format", "java")
        
        if not os.path.exists(apk_path):
            return {"text": f"APK file not found: {apk_path}"}
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Build JADX command
        cmd = ["jadx", "-d", output_dir, apk_path]
        
        # Add format option if specified
        if format_type == "kotlin":
            cmd.append("--show-bad-code")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return {
                "text": f"Successfully decompiled APK to {output_dir}\n\nOutput:\n{result.stdout}"
            }
        except subprocess.CalledProcessError as e:
            return {
                "text": f"Failed to decompile APK: {e.stderr}"
            }

    async def analyze_java_files(self, arguments: Dict[str, Any]) -> Dict[str, str]:
        """Analyze Java source files"""
        decompiled_dir = arguments["decompiled_dir"]
        
        if not os.path.exists(decompiled_dir):
            return {"text": f"Decompiled directory not found: {decompiled_dir}"}
        
        try:
            java_files = []
            total_lines = 0
            total_classes = 0
            
            # Walk through the directory to find Java files
            for root, dirs, files in os.walk(decompiled_dir):
                for file in files:
                    if file.endswith('.java'):
                        java_files.append(os.path.join(root, file))
            
            # Analyze each Java file
            for java_file in java_files[:10]:  # Limit to first 10 files for performance
                try:
                    with open(java_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        lines = content.split('\n')
                        total_lines += len(lines)
                        
                        # Count classes
                        class_count = content.count('class ') + content.count('interface ')
                        total_classes += class_count
                except Exception as e:
                    logger.warning(f"Error reading {java_file}: {e}")
            
            analysis = []
            analysis.append("## Java Files Analysis")
            analysis.append(f"**Total Java Files:** {len(java_files)}")
            analysis.append(f"**Total Lines of Code:** {total_lines}")
            analysis.append(f"**Total Classes/Interfaces:** {total_classes}")
            
            if java_files:
                analysis.append("\n**Sample Files:**")
                for i, file_path in enumerate(java_files[:5], 1):
                    rel_path = os.path.relpath(file_path, decompiled_dir)
                    analysis.append(f"{i}. {rel_path}")
            
            return {"text": "\n".join(analysis)}
        except Exception as e:
            return {"text": f"Error analyzing Java files: {str(e)}"}

    async def find_classes(self, arguments: Dict[str, Any]) -> Dict[str, str]:
        """Find and list Java classes"""
        decompiled_dir = arguments["decompiled_dir"]
        pattern = arguments.get("pattern", "")
        
        if not os.path.exists(decompiled_dir):
            return {"text": f"Decompiled directory not found: {decompiled_dir}"}
        
        try:
            classes = []
            
            # Walk through the directory to find Java files
            for root, dirs, files in os.walk(decompiled_dir):
                for file in files:
                    if file.endswith('.java'):
                        file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(file_path, decompiled_dir)
                        
                        # Filter by pattern if specified
                        if pattern and pattern.lower() not in rel_path.lower():
                            continue
                        
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                
                                # Extract class names
                                lines = content.split('\n')
                                for line in lines:
                                    if 'class ' in line and not line.strip().startswith('//'):
                                        # Simple class name extraction
                                        class_start = line.find('class ') + 6
                                        class_end = line.find(' ', class_start)
                                        if class_end == -1:
                                            class_end = line.find('{', class_start)
                                        if class_end == -1:
                                            class_end = line.find('\n', class_start)
                                        
                                        if class_end > class_start:
                                            class_name = line[class_start:class_end].strip()
                                            classes.append(f"{class_name} ({rel_path})")
                        except Exception as e:
                            logger.warning(f"Error reading {file_path}: {e}")
            
            analysis = []
            analysis.append("## Java Classes Found")
            analysis.append(f"**Total Classes:** {len(classes)}")
            
            if pattern:
                analysis.append(f"**Filter Pattern:** {pattern}")
            
            if classes:
                analysis.append("\n**Classes:**")
                for i, class_info in enumerate(classes[:20], 1):  # Limit to first 20
                    analysis.append(f"{i}. {class_info}")
                
                if len(classes) > 20:
                    analysis.append(f"\n... and {len(classes) - 20} more classes")
            else:
                analysis.append("\nNo classes found matching the criteria.")
            
            return {"text": "\n".join(analysis)}
        except Exception as e:
            return {"text": f"Error finding classes: {str(e)}"}

async def main():
    """Main function"""
    server = SimpleJadxMCPServer()
    
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