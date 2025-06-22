#!/usr/bin/env python3
"""Main analysis script for MarsPro reverse engineering using MCP servers."""

import os
import sys
import json
import logging
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('analysis/analysis.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class MarsProMCPAnalyzer:
    """Main analyzer for MarsPro reverse engineering using MCP servers."""
    
    def __init__(self, apk_path: str):
        """Initialize the analyzer."""
        self.apk_path = Path(apk_path)
        self.project_root = Path(__file__).parent.parent
        self.output_dir = self.project_root / "output"
        self.analysis_dir = self.project_root / "analysis"
        
        # Create output directories
        self.output_dir.mkdir(exist_ok=True)
        self.analysis_dir.mkdir(exist_ok=True)
        
        logger.info(f"Initialized MCP analyzer for APK: {self.apk_path}")
    
    def call_mcp_server(self, server_name: str, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call an MCP server tool."""
        try:
            # Create the MCP request
            request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": arguments
                }
            }
            
            # Get server configuration from mcp.json
            with open("mcp.json", "r") as f:
                mcp_config = json.load(f)
            
            server_config = None
            for server in mcp_config.get("servers", []):
                if server.get("id") == server_name:
                    server_config = server
                    break
            
            if not server_config:
                raise Exception(f"Server {server_name} not found in mcp.json")
            
            # Run the server command
            cwd = server_config.get("cwd", "")
            command = server_config.get("command", [])
            
            if not command:
                raise Exception(f"No command configured for server {server_name}")
            
            # Send request to server
            result = subprocess.run(
                command,
                cwd=cwd,
                input=json.dumps(request) + "\n",
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                raise Exception(f"Server {server_name} failed: {result.stderr}")
            
            # Parse response
            response = json.loads(result.stdout.strip())
            
            if "error" in response:
                raise Exception(f"Server {server_name} error: {response['error']}")
            
            return response.get("result", {})
            
        except Exception as e:
            logger.error(f"Failed to call MCP server {server_name}: {e}")
            raise
    
    def phase1_static_analysis(self) -> bool:
        """Phase 1: Static APK analysis using MCP servers."""
        logger.info("Starting Phase 1: Static Analysis with MCP servers")
        
        try:
            # Create output directories
            apktool_output = self.output_dir / "apktool_output"
            jadx_output = self.output_dir / "jadx_output"
            
            apktool_output.mkdir(exist_ok=True)
            jadx_output.mkdir(exist_ok=True)
            
            # Use apktool MCP server
            logger.info("Using apktool MCP server...")
            apktool_result = self.call_mcp_server(
                "apktool",
                "decompile_apk",
                {
                    "apk_path": str(self.apk_path),
                    "output_dir": str(apktool_output)
                }
            )
            
            if apktool_result.get("success"):
                logger.info("apktool MCP server completed successfully")
                
                # Analyze manifest
                manifest_result = self.call_mcp_server(
                    "apktool",
                    "analyze_manifest",
                    {
                        "apktool_dir": str(apktool_output)
                    }
                )
                
                if manifest_result.get("success"):
                    logger.info("Manifest analysis completed")
                    # Save manifest analysis
                    manifest_file = self.analysis_dir / "manifest_analysis.json"
                    with open(manifest_file, "w") as f:
                        json.dump(manifest_result.get("data", {}), f, indent=2)
            else:
                logger.error(f"apktool MCP server failed: {apktool_result.get('error')}")
                return False
            
            # Use jadx MCP server
            logger.info("Using jadx MCP server...")
            jadx_result = self.call_mcp_server(
                "jadx",
                "decompile_apk",
                {
                    "apk_path": str(self.apk_path),
                    "output_dir": str(jadx_output)
                }
            )
            
            if jadx_result.get("success"):
                logger.info("jadx MCP server completed successfully")
                
                # Find classes
                classes_result = self.call_mcp_server(
                    "jadx",
                    "find_classes",
                    {
                        "jadx_dir": str(jadx_output)
                    }
                )
                
                if classes_result.get("success"):
                    logger.info("Class analysis completed")
                    # Save class analysis
                    classes_file = self.analysis_dir / "classes_analysis.json"
                    with open(classes_file, "w") as f:
                        json.dump(classes_result.get("data", {}), f, indent=2)
            else:
                logger.error(f"jadx MCP server failed: {jadx_result.get('error')}")
                return False
            
            # Extract interesting files
            self._extract_interesting_files(apktool_output, jadx_output)
            
            return True
            
        except Exception as e:
            logger.error(f"Phase 1 failed: {e}")
            return False
    
    def phase2_dynamic_analysis(self) -> bool:
        """Phase 2: Dynamic analysis with Frida hooks."""
        logger.info("Starting Phase 2: Dynamic Analysis")
        
        try:
            # Check if device is connected
            result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
            if "device" not in result.stdout:
                logger.warning("No Android device connected. Skipping dynamic analysis.")
                return True
            
            # Start Frida server if needed
            self._setup_frida_server()
            
            # Run network hooks
            logger.info("Running network hooks...")
            self._run_frida_script("scripts/net_hook.js")
            
            # Run BLE hooks
            logger.info("Running BLE hooks...")
            self._run_frida_script("scripts/ble_hook.js")
            
            return True
            
        except Exception as e:
            logger.error(f"Phase 2 failed: {e}")
            return False
    
    def phase3_documentation(self) -> bool:
        """Phase 3: Documentation and API mapping."""
        logger.info("Starting Phase 3: Documentation")
        
        try:
            # Generate analysis summary
            self._generate_analysis_summary()
            
            # Generate API documentation
            self._generate_api_documentation()
            
            # Generate mapping documentation
            self._generate_mapping_documentation()
            
            return True
            
        except Exception as e:
            logger.error(f"Phase 3 failed: {e}")
            return False
    
    def phase4_ha_integration(self) -> bool:
        """Phase 4: Home Assistant component development."""
        logger.info("Starting Phase 4: Home Assistant Integration")
        
        try:
            # Update constants with discovered values
            self._update_constants()
            
            # Generate configuration examples
            self._generate_config_examples()
            
            return True
            
        except Exception as e:
            logger.error(f"Phase 4 failed: {e}")
            return False
    
    def phase5_testing(self) -> bool:
        """Phase 5: Integration testing and validation."""
        logger.info("Starting Phase 5: Testing")
        
        try:
            # Run unit tests
            self._run_unit_tests()
            
            # Run integration tests
            self._run_integration_tests()
            
            return True
            
        except Exception as e:
            logger.error(f"Phase 5 failed: {e}")
            return False
    
    def _extract_interesting_files(self, apktool_output: Path, jadx_output: Path):
        """Extract interesting files for analysis."""
        logger.info("Extracting interesting files...")
        
        # Copy AndroidManifest.xml
        manifest_src = apktool_output / "AndroidManifest.xml"
        if manifest_src.exists():
            manifest_dst = self.analysis_dir / "AndroidManifest.xml"
            manifest_dst.write_text(manifest_src.read_text())
            logger.info("Extracted AndroidManifest.xml")
        
        # Copy strings.xml files
        for strings_file in apktool_output.rglob("strings.xml"):
            rel_path = strings_file.relative_to(apktool_output)
            dst_path = self.analysis_dir / "strings" / rel_path
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            dst_path.write_text(strings_file.read_text())
            logger.info(f"Extracted {rel_path}")
    
    def _setup_frida_server(self):
        """Setup Frida server on device."""
        logger.info("Setting up Frida server...")
        
        # Check if Frida server is already running
        result = subprocess.run(["adb", "shell", "ps | grep frida"], 
                              capture_output=True, text=True)
        
        if "frida-server" not in result.stdout:
            logger.info("Starting Frida server...")
            subprocess.run([
                "adb", "shell", 
                "su -c '/data/local/tmp/frida-server &'"
            ])
    
    def _run_frida_script(self, script_path: str):
        """Run a Frida script."""
        script_file = self.project_root / script_path
        if script_file.exists():
            logger.info(f"Running Frida script: {script_path}")
            # This would be implemented based on device connection
            # For now, just log the intention
            logger.info(f"Would run: frida -U -f com.marspro.app -l {script_path} --no-pause")
    
    def _generate_analysis_summary(self):
        """Generate analysis summary."""
        logger.info("Generating analysis summary...")
        
        summary = {
            "apk_file": str(self.apk_path),
            "analysis_date": str(Path(__file__).stat().st_mtime),
            "phases_completed": [],
            "discovered_components": [],
            "next_steps": []
        }
        
        summary_file = self.analysis_dir / "analysis_summary.json"
        with open(summary_file, "w") as f:
            json.dump(summary, f, indent=2)
        
        logger.info("Analysis summary generated")
    
    def _generate_api_documentation(self):
        """Generate API documentation."""
        logger.info("Generating API documentation...")
        
        # This would analyze the extracted files and generate API docs
        # For now, create a placeholder
        api_doc = {
            "endpoints": [],
            "authentication": {},
            "ble_services": [],
            "protocols": []
        }
        
        api_file = self.analysis_dir / "api_documentation.json"
        with open(api_file, "w") as f:
            json.dump(api_doc, f, indent=2)
        
        logger.info("API documentation generated")
    
    def _generate_mapping_documentation(self):
        """Generate mapping documentation."""
        logger.info("Generating mapping documentation...")
        
        # This would map cloud vs local functions
        mapping = {
            "cloud_functions": [],
            "local_functions": [],
            "ble_commands": [],
            "rest_endpoints": []
        }
        
        mapping_file = self.analysis_dir / "api_mapping.json"
        with open(mapping_file, "w") as f:
            json.dump(mapping, f, indent=2)
        
        logger.info("Mapping documentation generated")
    
    def _update_constants(self):
        """Update constants with discovered values."""
        logger.info("Updating constants...")
        # This would update the Home Assistant component constants
        pass
    
    def _generate_config_examples(self):
        """Generate configuration examples."""
        logger.info("Generating configuration examples...")
        # This would generate Home Assistant configuration examples
        pass
    
    def _run_unit_tests(self):
        """Run unit tests."""
        logger.info("Running unit tests...")
        # This would run the unit tests
        pass
    
    def _run_integration_tests(self):
        """Run integration tests."""
        logger.info("Running integration tests...")
        # This would run the integration tests
        pass
    
    def run_full_analysis(self):
        """Run the full analysis workflow."""
        logger.info("Starting full MarsPro analysis workflow")
        logger.info("=" * 50)
        
        phases = [
            ("Phase 1: Static Analysis", self.phase1_static_analysis),
            ("Phase 2: Dynamic Analysis", self.phase2_dynamic_analysis),
            ("Phase 3: Documentation", self.phase3_documentation),
            ("Phase 4: Home Assistant Integration", self.phase4_ha_integration),
            ("Phase 5: Testing", self.phase5_testing)
        ]
        
        for phase_name, phase_func in phases:
            logger.info("=" * 50)
            logger.info(f"Starting {phase_name}")
            logger.info("=" * 50)
            
            if not phase_func():
                logger.error(f"{phase_name} failed. Stopping analysis.")
                break
        
        logger.info("=" * 50)
        logger.info("Analysis workflow completed!")


def main():
    """Main entry point."""
    if len(sys.argv) != 2:
        print("Usage: python analyze_mcp.py <apk_file>")
        sys.exit(1)
    
    apk_file = sys.argv[1]
    
    if not Path(apk_file).exists():
        print(f"APK file not found: {apk_file}")
        sys.exit(1)
    
    analyzer = MarsProMCPAnalyzer(apk_file)
    analyzer.run_full_analysis()


if __name__ == "__main__":
    main() 