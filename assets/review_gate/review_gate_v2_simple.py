#!/usr/bin/env python3
"""
Review Gate V2 - Simplified MCP Server
A simplified version that follows the same manual MCP protocol as working servers
"""

import asyncio
import json
import sys
import logging
import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Sequence, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SimpleReviewGateServer:
    def __init__(self):
        self.tools = [
            {
                "name": "review_gate_chat",
                "description": "Open Review Gate chat popup for user feedback and reviews. Returns user input after popup interaction.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "The message to display in the Review Gate popup",
                            "default": "Please provide your review or feedback:"
                        },
                        "title": {
                            "type": "string", 
                            "description": "Title for the Review Gate popup window",
                            "default": "Review Gate V2"
                        },
                        "context": {
                            "type": "string",
                            "description": "Additional context about what needs review",
                            "default": ""
                        },
                        "urgent": {
                            "type": "boolean",
                            "description": "Whether this is an urgent review request",
                            "default": False
                        }
                    },
                    "required": ["message"]
                }
            },
            {
                "name": "quick_input",
                "description": "Get quick user input for simple questions or confirmations",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "prompt": {
                            "type": "string",
                            "description": "The prompt/question to ask the user",
                            "default": "Please provide input:"
                        },
                        "timeout": {
                            "type": "integer",
                            "description": "Timeout in seconds (default: 300)",
                            "default": 300
                        }
                    },
                    "required": ["prompt"]
                }
            }
        ]
        logger.info("🚀 Simple Review Gate V2 server initialized")

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
                        "name": "review-gate-v2-simple",
                        "version": "2.0.0"
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
                if tool_name == "review_gate_chat":
                    result = await self.handle_review_gate_chat(arguments)
                elif tool_name == "quick_input":
                    result = await self.handle_quick_input(arguments)
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

    async def handle_review_gate_chat(self, arguments: Dict[str, Any]) -> Dict[str, str]:
        """Handle Review Gate chat with simplified popup mechanism"""
        message = arguments.get("message", "Please provide your review or feedback:")
        title = arguments.get("title", "Review Gate V2")
        context = arguments.get("context", "")
        urgent = arguments.get("urgent", False)
        
        logger.info(f"🎯 Review Gate Chat activated")
        logger.info(f"📝 Title: {title}")
        logger.info(f"📄 Message: {message}")
        logger.info(f"📋 Context: {context}")
        logger.info(f"🚨 Urgent: {urgent}")
        
        # Create trigger data for Cursor extension
        trigger_id = f"review_gate_{int(datetime.now().timestamp())}"
        trigger_data = {
            "trigger_id": trigger_id,
            "type": "review_gate_chat",
            "title": title,
            "message": message,
            "context": context,
            "urgent": urgent,
            "timestamp": datetime.now().isoformat()
        }
        
        # Write trigger file for Cursor extension
        trigger_file = self.write_trigger_file(trigger_id, trigger_data)
        logger.info(f"📁 Trigger file created: {trigger_file}")
        
        # Simulate user response for testing (in real usage, this would wait for actual user input)
        # For now, return a placeholder response
        response_text = f"Review Gate popup opened with message: '{message}'. User response would be captured here in actual usage."
        
        logger.info(f"✅ Review Gate Chat completed")
        return {"text": response_text}

    async def handle_quick_input(self, arguments: Dict[str, Any]) -> Dict[str, str]:
        """Handle quick input requests"""
        prompt = arguments.get("prompt", "Please provide input:")
        timeout = arguments.get("timeout", 300)
        
        logger.info(f"⚡ Quick Input requested")
        logger.info(f"📝 Prompt: {prompt}")
        logger.info(f"⏱️ Timeout: {timeout}s")
        
        # Create trigger data for quick input
        trigger_id = f"quick_input_{int(datetime.now().timestamp())}"
        trigger_data = {
            "trigger_id": trigger_id,
            "type": "quick_input",
            "prompt": prompt,
            "timeout": timeout,
            "timestamp": datetime.now().isoformat()
        }
        
        # Write trigger file
        trigger_file = self.write_trigger_file(trigger_id, trigger_data)
        logger.info(f"📁 Quick input trigger file created: {trigger_file}")
        
        # Return placeholder response
        response_text = f"Quick input popup opened with prompt: '{prompt}'. User input would be captured here in actual usage."
        
        logger.info(f"✅ Quick Input completed")
        return {"text": response_text}

    def write_trigger_file(self, trigger_id: str, data: dict) -> str:
        """Write trigger file for Cursor extension"""
        # Use system temp directory
        temp_dir = tempfile.gettempdir()
        trigger_file = os.path.join(temp_dir, f"review_gate_{trigger_id}.json")
        
        try:
            with open(trigger_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"📝 Trigger file written: {trigger_file}")
            return trigger_file
        except Exception as e:
            logger.error(f"❌ Failed to write trigger file: {e}")
            return ""

async def main():
    """Main function"""
    server = SimpleReviewGateServer()
    
    # Read from stdin, write to stdout
    while True:
        try:
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            if not line:
                break
            
            request = json.loads(line.strip())
            response = await server.handle_request(request)
            
            # Write response to stdout
            await asyncio.get_event_loop().run_in_executor(None, lambda: sys.stdout.write(json.dumps(response) + '\n'))
            await asyncio.get_event_loop().run_in_executor(None, sys.stdout.flush)
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON: {e}")
            break
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            break

if __name__ == "__main__":
    asyncio.run(main()) 