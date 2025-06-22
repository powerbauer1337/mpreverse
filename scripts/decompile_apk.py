#!/usr/bin/env python3
"""
Script to decompile MarsPro APK using JADX MCP server
"""

import asyncio
import json
import os
import sys
from pathlib import Path

# Add the tools directory to the path
sys.path.append(str(Path(__file__).parent.parent / "tools" / "jadx-ai-mcp"))

from jadx_ai_mcp import SimpleJadxMCPServer

async def main():
    """Main function to decompile the APK"""
    server = SimpleJadxMCPServer()
    
    # Path to the APK file
    apk_path = "apks/MarsPro_1.3.2_APKPure.xapk"
    output_dir = "output/jadx_output"
    
    print(f"Decompiling APK: {apk_path}")
    print(f"Output directory: {output_dir}")
    
    # Decompile the APK
    result = await server.decompile_apk({
        "apk_path": apk_path,
        "output_dir": output_dir,
        "format": "java"
    })
    
    print("Decompilation result:")
    print(result.get("text", str(result)))
    
    # Analyze the decompiled files
    if os.path.exists(output_dir):
        print("\nAnalyzing decompiled files...")
        analysis_result = await server.analyze_java_files({
            "decompiled_dir": output_dir
        })
        print("Analysis result:")
        print(analysis_result.get("text", str(analysis_result)))
        
        # Find classes related to API/network
        print("\nSearching for API-related classes...")
        classes_result = await server.find_classes({
            "decompiled_dir": output_dir,
            "pattern": "api"
        })
        print("Classes found:")
        print(classes_result.get("text", str(classes_result)))

if __name__ == "__main__":
    asyncio.run(main()) 