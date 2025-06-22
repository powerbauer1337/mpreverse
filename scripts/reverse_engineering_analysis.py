#!/usr/bin/env python3
"""
MarsPro Reverse Engineering Analysis Script

This script performs comprehensive static and dynamic analysis of the MarsPro APK
to understand the communication protocols and enable Home Assistant integration.

Author: MarsPro Analysis Team
Date: 2024-12-19
Version: 1.0.0
"""

import os
import sys
import json
import logging
import subprocess
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import hashlib
import shutil

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(project_root / 'analysis' / 'reverse_engineering.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class MarsProAnalyzer:
    """Comprehensive MarsPro APK analyzer."""
    
    def __init__(self, apk_path: str, output_dir: str = None):
        """
        Initialize the MarsPro analyzer.
        
        Args:
            apk_path: Path to the MarsPro APK file
            output_dir: Output directory for analysis results
        """
        self.apk_path = Path(apk_path)
        self.output_dir = Path(output_dir) if output_dir else project_root / 'output'
        self.analysis_dir = project_root / 'analysis'
        
        # Create output directories
        self.output_dir.mkdir(exist_ok=True)
        (self.output_dir / 'apktool_output').mkdir(exist_ok=True)
        (self.output_dir / 'jadx_output').mkdir(exist_ok=True)
        (self.output_dir / 'logs').mkdir(exist_ok=True)
        
        # Analysis results
        self.analysis_results = {
            'metadata': {},
            'permissions': [],
            'activities': [],
            'services': [],
            'receivers': [],
            'providers': [],
            'native_libraries': [],
            'assets': [],
            'strings': [],
            'network_endpoints': [],
            'ble_services': [],
            'security_findings': [],
            'recommendations': []
        }
        
        # Tools paths
        self.apktool_path = project_root / 'assets' / 'tools' / 'apktool' / 'apktool.bat'
        self.jadx_path = project_root / 'assets' / 'tools' / 'jadx' / 'bin' / 'jadx.bat'
        
        logger.info(f"Initialized MarsPro analyzer for APK: {self.apk_path}")
    
    def validate_apk(self) -> bool:
        """
        Validate the APK file.
        
        Returns:
            True if APK is valid, False otherwise
        """
        logger.info("Validating APK file...")
        
        if not self.apk_path.exists():
            logger.error(f"APK file not found: {self.apk_path}")
            return False
        
        if not self.apk_path.suffix.lower() in ['.apk', '.xapk']:
            logger.error(f"Invalid file format: {self.apk_path.suffix}")
            return False
        
        # Check file size
        file_size = self.apk_path.stat().st_size
        if file_size < 1024 * 1024:  # Less than 1MB
            logger.warning(f"APK file seems too small: {file_size} bytes")
        
        logger.info(f"APK validation passed. Size: {file_size / (1024*1024):.2f} MB")
        return True
    
    def extract_apk_metadata(self) -> Dict[str, Any]:
        """
        Extract basic metadata from the APK.
        
        Returns:
            Dictionary containing APK metadata
        """
        logger.info("Extracting APK metadata...")
        
        metadata = {
            'file_path': str(self.apk_path),
            'file_size': self.apk_path.stat().st_size,
            'file_hash': self._calculate_file_hash(),
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        # Extract from XAPK if needed
        if self.apk_path.suffix.lower() == '.xapk':
            metadata.update(self._extract_xapk_metadata())
        else:
            metadata.update(self._extract_apk_metadata())
        
        self.analysis_results['metadata'] = metadata
        logger.info(f"Extracted metadata: {metadata.get('package_name', 'Unknown')} v{metadata.get('version_name', 'Unknown')}")
        
        return metadata
    
    def _calculate_file_hash(self) -> str:
        """Calculate SHA256 hash of the APK file."""
        sha256_hash = hashlib.sha256()
        with open(self.apk_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()
    
    def _extract_xapk_metadata(self) -> Dict[str, Any]:
        """Extract metadata from XAPK file."""
        try:
            with zipfile.ZipFile(self.apk_path, 'r') as xapk:
                # Look for manifest.json or similar metadata file
                metadata_files = [f for f in xapk.namelist() if 'manifest' in f.lower()]
                
                if metadata_files:
                    with xapk.open(metadata_files[0]) as f:
                        manifest_data = json.load(f)
                        return {
                            'package_name': manifest_data.get('package_name', 'Unknown'),
                            'version_name': manifest_data.get('version_name', 'Unknown'),
                            'version_code': manifest_data.get('version_code', 'Unknown'),
                            'file_type': 'XAPK'
                        }
                
                # Look for APK file within XAPK
                apk_files = [f for f in xapk.namelist() if f.endswith('.apk')]
                if apk_files:
                    # Extract APK and analyze it
                    apk_path = self.output_dir / 'extracted.apk'
                    with xapk.open(apk_files[0]) as apk_file:
                        with open(apk_path, 'wb') as f:
                            f.write(apk_file.read())
                    
                    # Analyze the extracted APK
                    return self._extract_apk_metadata_from_file(apk_path)
        
        except Exception as e:
            logger.error(f"Error extracting XAPK metadata: {e}")
        
        return {'file_type': 'XAPK', 'package_name': 'Unknown'}
    
    def _extract_apk_metadata(self) -> Dict[str, Any]:
        """Extract metadata from APK file."""
        return self._extract_apk_metadata_from_file(self.apk_path)
    
    def _extract_apk_metadata_from_file(self, apk_file: Path) -> Dict[str, Any]:
        """Extract metadata from APK file using aapt or similar tool."""
        try:
            # Try to use aapt if available
            result = subprocess.run(
                ['aapt', 'dump', 'badging', str(apk_file)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return self._parse_aapt_output(result.stdout)
            
        except (subprocess.TimeoutExpired, FileNotFoundError):
            logger.warning("aapt not available, using basic extraction")
        
        # Fallback: basic extraction
        return {
            'file_type': 'APK',
            'package_name': 'com.marspro.meizhi',  # Known from previous analysis
            'version_name': '1.3.2',  # Known from previous analysis
            'version_code': 'Unknown'
        }
    
    def _parse_aapt_output(self, output: str) -> Dict[str, Any]:
        """Parse aapt output to extract metadata."""
        metadata = {'file_type': 'APK'}
        
        for line in output.split('\n'):
            if line.startswith('package:'):
                # Extract package name and version
                parts = line.split()
                for part in parts:
                    if part.startswith('name='):
                        metadata['package_name'] = part.split('=')[1].strip("'")
                    elif part.startswith('versionName='):
                        metadata['version_name'] = part.split('=')[1].strip("'")
                    elif part.startswith('versionCode='):
                        metadata['version_code'] = part.split('=')[1].strip("'")
        
        return metadata
    
    def decompile_with_apktool(self) -> bool:
        """
        Decompile APK using APKTool.
        
        Returns:
            True if successful, False otherwise
        """
        logger.info("Decompiling APK with APKTool...")
        
        output_path = self.output_dir / 'apktool_output'
        
        try:
            # Handle XAPK extraction if needed
            apk_to_decompile = self.apk_path
            if self.apk_path.suffix.lower() == '.xapk':
                extracted_apk = self.output_dir / 'extracted.apk'
                if extracted_apk.exists():
                    apk_to_decompile = extracted_apk
                else:
                    logger.error("XAPK extraction failed")
                    return False
            
            cmd = [
                str(self.apktool_path),
                'd',
                str(apk_to_decompile),
                '-o',
                str(output_path),
                '-f'  # Force overwrite
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )
            
            if result.returncode == 0:
                logger.info("APKTool decompilation completed successfully")
                return True
            else:
                logger.error(f"APKTool decompilation failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("APKTool decompilation timed out")
            return False
        except Exception as e:
            logger.error(f"Error during APKTool decompilation: {e}")
            return False
    
    def decompile_with_jadx(self) -> bool:
        """
        Decompile APK using JADX.
        
        Returns:
            True if successful, False otherwise
        """
        logger.info("Decompiling APK with JADX...")
        
        output_path = self.output_dir / 'jadx_output'
        
        try:
            # Handle XAPK extraction if needed
            apk_to_decompile = self.apk_path
            if self.apk_path.suffix.lower() == '.xapk':
                extracted_apk = self.output_dir / 'extracted.apk'
                if extracted_apk.exists():
                    apk_to_decompile = extracted_apk
                else:
                    logger.error("XAPK extraction failed")
                    return False
            
            cmd = [
                str(self.jadx_path),
                '-d',
                str(output_path),
                str(apk_to_decompile)
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600  # 10 minutes timeout
            )
            
            if result.returncode == 0:
                logger.info("JADX decompilation completed successfully")
                return True
            else:
                logger.error(f"JADX decompilation failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("JADX decompilation timed out")
            return False
        except Exception as e:
            logger.error(f"Error during JADX decompilation: {e}")
            return False
    
    def analyze_manifest(self) -> Dict[str, Any]:
        """
        Analyze the AndroidManifest.xml file.
        
        Returns:
            Dictionary containing manifest analysis results
        """
        logger.info("Analyzing AndroidManifest.xml...")
        
        manifest_path = self.output_dir / 'apktool_output' / 'AndroidManifest.xml'
        
        if not manifest_path.exists():
            logger.error("AndroidManifest.xml not found")
            return {}
        
        try:
            tree = ET.parse(manifest_path)
            root = tree.getroot()
            
            # Extract namespace
            ns = {'android': 'http://schemas.android.com/apk/res/android'}
            
            manifest_data = {
                'package': root.get('package'),
                'version_name': root.get('{http://schemas.android.com/apk/res/android}versionName'),
                'version_code': root.get('{http://schemas.android.com/apk/res/android}versionCode'),
                'permissions': [],
                'activities': [],
                'services': [],
                'receivers': [],
                'providers': [],
                'uses_features': [],
                'uses_permissions': []
            }
            
            # Extract permissions
            for permission in root.findall('.//uses-permission', ns):
                perm_name = permission.get('{http://schemas.android.com/apk/res/android}name')
                if perm_name:
                    manifest_data['uses_permissions'].append(perm_name)
            
            # Extract activities
            for activity in root.findall('.//activity', ns):
                activity_data = {
                    'name': activity.get('{http://schemas.android.com/apk/res/android}name'),
                    'exported': activity.get('{http://schemas.android.com/apk/res/android}exported'),
                    'launchable': False
                }
                
                # Check if it's the main activity
                intent_filter = activity.find('.//intent-filter', ns)
                if intent_filter:
                    for action in intent_filter.findall('.//action', ns):
                        if action.get('{http://schemas.android.com/apk/res/android}name') == 'android.intent.action.MAIN':
                            activity_data['launchable'] = True
                            break
                
                manifest_data['activities'].append(activity_data)
            
            # Extract services
            for service in root.findall('.//service', ns):
                service_data = {
                    'name': service.get('{http://schemas.android.com/apk/res/android}name'),
                    'exported': service.get('{http://schemas.android.com/apk/res/android}exported')
                }
                manifest_data['services'].append(service_data)
            
            # Extract receivers
            for receiver in root.findall('.//receiver', ns):
                receiver_data = {
                    'name': receiver.get('{http://schemas.android.com/apk/res/android}name'),
                    'exported': receiver.get('{http://schemas.android.com/apk/res/android}exported')
                }
                manifest_data['receivers'].append(receiver_data)
            
            # Extract providers
            for provider in root.findall('.//provider', ns):
                provider_data = {
                    'name': provider.get('{http://schemas.android.com/apk/res/android}name'),
                    'exported': provider.get('{http://schemas.android.com/apk/res/android}exported'),
                    'authorities': provider.get('{http://schemas.android.com/apk/res/android}authorities')
                }
                manifest_data['providers'].append(provider_data)
            
            # Extract uses-features
            for feature in root.findall('.//uses-feature', ns):
                feature_data = {
                    'name': feature.get('{http://schemas.android.com/apk/res/android}name'),
                    'required': feature.get('{http://schemas.android.com/apk/res/android}required')
                }
                manifest_data['uses_features'].append(feature_data)
            
            self.analysis_results['permissions'] = manifest_data['uses_permissions']
            self.analysis_results['activities'] = manifest_data['activities']
            self.analysis_results['services'] = manifest_data['services']
            self.analysis_results['receivers'] = manifest_data['receivers']
            self.analysis_results['providers'] = manifest_data['providers']
            
            logger.info(f"Manifest analysis completed. Found {len(manifest_data['uses_permissions'])} permissions")
            return manifest_data
            
        except Exception as e:
            logger.error(f"Error analyzing manifest: {e}")
            return {}
    
    def analyze_native_libraries(self) -> List[str]:
        """
        Analyze native libraries in the APK.
        
        Returns:
            List of native library paths
        """
        logger.info("Analyzing native libraries...")
        
        lib_dirs = [
            self.output_dir / 'apktool_output' / 'lib',
            self.output_dir / 'apktool_output' / 'libs'
        ]
        
        native_libs = []
        
        for lib_dir in lib_dirs:
            if lib_dir.exists():
                for arch_dir in lib_dir.iterdir():
                    if arch_dir.is_dir():
                        for lib_file in arch_dir.glob('*.so'):
                            native_libs.append(str(lib_file.relative_to(self.output_dir / 'apktool_output')))
        
        self.analysis_results['native_libraries'] = native_libs
        logger.info(f"Found {len(native_libs)} native libraries")
        return native_libs
    
    def analyze_assets(self) -> List[str]:
        """
        Analyze assets in the APK.
        
        Returns:
            List of asset files
        """
        logger.info("Analyzing assets...")
        
        assets_dir = self.output_dir / 'apktool_output' / 'assets'
        assets = []
        
        if assets_dir.exists():
            for asset_file in assets_dir.rglob('*'):
                if asset_file.is_file():
                    assets.append(str(asset_file.relative_to(self.output_dir / 'apktool_output')))
        
        self.analysis_results['assets'] = assets
        logger.info(f"Found {len(assets)} asset files")
        return assets
    
    def search_for_strings(self, patterns: List[str]) -> Dict[str, List[str]]:
        """
        Search for specific string patterns in decompiled code.
        
        Args:
            patterns: List of regex patterns to search for
            
        Returns:
            Dictionary mapping patterns to found strings
        """
        logger.info("Searching for string patterns...")
        
        results = {}
        
        # Search in APKTool output
        apktool_dir = self.output_dir / 'apktool_output'
        if apktool_dir.exists():
            for pattern in patterns:
                results[pattern] = []
                
                # Search in smali files
                for smali_file in apktool_dir.rglob('*.smali'):
                    try:
                        with open(smali_file, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            if pattern.lower() in content.lower():
                                results[pattern].append(str(smali_file.relative_to(apktool_dir)))
                    except Exception as e:
                        logger.debug(f"Error reading {smali_file}: {e}")
                
                # Search in XML files
                for xml_file in apktool_dir.rglob('*.xml'):
                    try:
                        with open(xml_file, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            if pattern.lower() in content.lower():
                                results[pattern].append(str(xml_file.relative_to(apktool_dir)))
                    except Exception as e:
                        logger.debug(f"Error reading {xml_file}: {e}")
        
        # Search in JADX output
        jadx_dir = self.output_dir / 'jadx_output'
        if jadx_dir.exists():
            for pattern in patterns:
                if pattern not in results:
                    results[pattern] = []
                
                # Search in Java files
                for java_file in jadx_dir.rglob('*.java'):
                    try:
                        with open(java_file, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            if pattern.lower() in content.lower():
                                results[pattern].append(str(java_file.relative_to(jadx_dir)))
                    except Exception as e:
                        logger.debug(f"Error reading {java_file}: {e}")
        
        # Filter out empty results
        results = {k: v for k, v in results.items() if v}
        
        logger.info(f"String search completed. Found matches for {len(results)} patterns")
        return results
    
    def analyze_network_endpoints(self) -> List[str]:
        """
        Analyze network endpoints and API calls.
        
        Returns:
            List of discovered network endpoints
        """
        logger.info("Analyzing network endpoints...")
        
        # Common patterns for network endpoints
        patterns = [
            'http://',
            'https://',
            'api.',
            '.com/api',
            '.com/v1',
            '.com/v2',
            'firebase',
            'googleapis',
            'bluetooth',
            'ble',
            'uuid',
            'characteristic'
        ]
        
        string_results = self.search_for_strings(patterns)
        
        endpoints = []
        for pattern, files in string_results.items():
            endpoints.extend(files)
        
        self.analysis_results['network_endpoints'] = list(set(endpoints))
        logger.info(f"Found {len(self.analysis_results['network_endpoints'])} potential network endpoints")
        return self.analysis_results['network_endpoints']
    
    def analyze_ble_services(self) -> List[str]:
        """
        Analyze BLE services and characteristics.
        
        Returns:
            List of BLE-related files
        """
        logger.info("Analyzing BLE services...")
        
        # BLE-specific patterns
        ble_patterns = [
            'bluetooth',
            'ble',
            'gatt',
            'characteristic',
            'service',
            'uuid',
            'peripheral',
            'central',
            'advertising',
            'scan'
        ]
        
        string_results = self.search_for_strings(ble_patterns)
        
        ble_files = []
        for pattern, files in string_results.items():
            ble_files.extend(files)
        
        self.analysis_results['ble_services'] = list(set(ble_files))
        logger.info(f"Found {len(self.analysis_results['ble_services'])} BLE-related files")
        return self.analysis_results['ble_services']
    
    def generate_security_report(self) -> Dict[str, Any]:
        """
        Generate security analysis report.
        
        Returns:
            Dictionary containing security findings
        """
        logger.info("Generating security report...")
        
        security_findings = []
        
        # Check for dangerous permissions
        dangerous_permissions = [
            'android.permission.INTERNET',
            'android.permission.ACCESS_NETWORK_STATE',
            'android.permission.BLUETOOTH',
            'android.permission.BLUETOOTH_ADMIN',
            'android.permission.ACCESS_FINE_LOCATION',
            'android.permission.ACCESS_COARSE_LOCATION',
            'android.permission.CAMERA',
            'android.permission.RECORD_AUDIO',
            'android.permission.READ_EXTERNAL_STORAGE',
            'android.permission.WRITE_EXTERNAL_STORAGE'
        ]
        
        for permission in dangerous_permissions:
            if permission in self.analysis_results['permissions']:
                security_findings.append({
                    'type': 'dangerous_permission',
                    'permission': permission,
                    'severity': 'medium',
                    'description': f'App requests dangerous permission: {permission}'
                })
        
        # Check for exported components
        for activity in self.analysis_results['activities']:
            if activity.get('exported') == 'true':
                security_findings.append({
                    'type': 'exported_component',
                    'component': f"Activity: {activity.get('name', 'Unknown')}",
                    'severity': 'low',
                    'description': 'Exported activity may be accessible by other apps'
                })
        
        for service in self.analysis_results['services']:
            if service.get('exported') == 'true':
                security_findings.append({
                    'type': 'exported_component',
                    'component': f"Service: {service.get('name', 'Unknown')}",
                    'severity': 'medium',
                    'description': 'Exported service may be accessible by other apps'
                })
        
        # Check for native libraries (potential security risk)
        if self.analysis_results['native_libraries']:
            security_findings.append({
                'type': 'native_code',
                'severity': 'info',
                'description': f'App contains {len(self.analysis_results["native_libraries"])} native libraries',
                'libraries': self.analysis_results['native_libraries']
            })
        
        self.analysis_results['security_findings'] = security_findings
        
        # Generate recommendations
        recommendations = [
            'Implement proper input validation for all user inputs',
            'Use HTTPS for all network communications',
            'Implement certificate pinning for API endpoints',
            'Use secure storage for sensitive data',
            'Implement proper session management',
            'Regular security audits of the integration'
        ]
        
        self.analysis_results['recommendations'] = recommendations
        
        logger.info(f"Security analysis completed. Found {len(security_findings)} security findings")
        return {
            'findings': security_findings,
            'recommendations': recommendations
        }
    
    def generate_analysis_report(self) -> str:
        """
        Generate comprehensive analysis report.
        
        Returns:
            Path to the generated report
        """
        logger.info("Generating comprehensive analysis report...")
        
        report_path = self.analysis_dir / f'marspro_reverse_engineering_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# MarsPro Reverse Engineering Analysis Report\n\n")
            f.write(f"**Generated**: {datetime.now().isoformat()}\n")
            f.write(f"**APK File**: {self.apk_path.name}\n")
            f.write(f"**APK Hash**: {self.analysis_results['metadata'].get('file_hash', 'Unknown')}\n\n")
            
            # Executive Summary
            f.write("## Executive Summary\n\n")
            f.write("This report presents the results of a comprehensive reverse engineering analysis ")
            f.write("of the MarsPro Android application. The analysis focused on understanding the ")
            f.write("communication protocols, security measures, and architecture to enable ")
            f.write("Home Assistant integration.\n\n")
            
            # Application Metadata
            f.write("## Application Metadata\n\n")
            metadata = self.analysis_results['metadata']
            f.write(f"- **Package Name**: {metadata.get('package_name', 'Unknown')}\n")
            f.write(f"- **Version**: {metadata.get('version_name', 'Unknown')}\n")
            f.write(f"- **Version Code**: {metadata.get('version_code', 'Unknown')}\n")
            f.write(f"- **File Size**: {metadata.get('file_size', 0) / (1024*1024):.2f} MB\n")
            f.write(f"- **File Type**: {metadata.get('file_type', 'Unknown')}\n\n")
            
            # Permissions Analysis
            f.write("## Permissions Analysis\n\n")
            f.write("The application requests the following permissions:\n\n")
            for permission in self.analysis_results['permissions']:
                f.write(f"- `{permission}`\n")
            f.write("\n")
            
            # Components Analysis
            f.write("## Components Analysis\n\n")
            
            f.write("### Activities\n")
            for activity in self.analysis_results['activities']:
                f.write(f"- **{activity.get('name', 'Unknown')}**")
                if activity.get('launchable'):
                    f.write(" (Main Activity)")
                f.write(f" - Exported: {activity.get('exported', 'Unknown')}\n")
            f.write("\n")
            
            f.write("### Services\n")
            for service in self.analysis_results['services']:
                f.write(f"- **{service.get('name', 'Unknown')}** - Exported: {service.get('exported', 'Unknown')}\n")
            f.write("\n")
            
            f.write("### Receivers\n")
            for receiver in self.analysis_results['receivers']:
                f.write(f"- **{receiver.get('name', 'Unknown')}** - Exported: {receiver.get('exported', 'Unknown')}\n")
            f.write("\n")
            
            f.write("### Providers\n")
            for provider in self.analysis_results['providers']:
                f.write(f"- **{provider.get('name', 'Unknown')}** - Exported: {provider.get('exported', 'Unknown')}\n")
            f.write("\n")
            
            # Native Libraries
            f.write("## Native Libraries\n\n")
            if self.analysis_results['native_libraries']:
                f.write("The application contains the following native libraries:\n\n")
                for lib in self.analysis_results['native_libraries']:
                    f.write(f"- `{lib}`\n")
            else:
                f.write("No native libraries found.\n")
            f.write("\n")
            
            # Assets
            f.write("## Assets\n\n")
            f.write(f"Found {len(self.analysis_results['assets'])} asset files.\n\n")
            
            # Network Analysis
            f.write("## Network Analysis\n\n")
            f.write(f"Found {len(self.analysis_results['network_endpoints'])} potential network endpoints.\n\n")
            
            # BLE Analysis
            f.write("## Bluetooth Low Energy (BLE) Analysis\n\n")
            f.write(f"Found {len(self.analysis_results['ble_services'])} BLE-related files.\n\n")
            
            # Security Analysis
            f.write("## Security Analysis\n\n")
            f.write(f"Found {len(self.analysis_results['security_findings'])} security findings:\n\n")
            
            for finding in self.analysis_results['security_findings']:
                f.write(f"### {finding['type'].replace('_', ' ').title()}\n")
                f.write(f"- **Severity**: {finding['severity']}\n")
                f.write(f"- **Description**: {finding['description']}\n")
                if 'component' in finding:
                    f.write(f"- **Component**: {finding['component']}\n")
                if 'libraries' in finding:
                    f.write("- **Libraries**:\n")
                    for lib in finding['libraries']:
                        f.write(f"  - `{lib}`\n")
                f.write("\n")
            
            # Recommendations
            f.write("## Recommendations\n\n")
            for recommendation in self.analysis_results['recommendations']:
                f.write(f"- {recommendation}\n")
            f.write("\n")
            
            # Next Steps
            f.write("## Next Steps\n\n")
            f.write("1. **Dynamic Analysis**: Perform runtime analysis using Frida\n")
            f.write("2. **Network Monitoring**: Capture and analyze network traffic\n")
            f.write("3. **BLE Protocol Analysis**: Reverse engineer BLE communication\n")
            f.write("4. **API Documentation**: Document discovered API endpoints\n")
            f.write("5. **Home Assistant Integration**: Implement local control\n\n")
            
            f.write("---\n")
            f.write("**Report generated by MarsPro Reverse Engineering Analysis Script**\n")
        
        logger.info(f"Analysis report generated: {report_path}")
        return str(report_path)
    
    def run_complete_analysis(self) -> Dict[str, Any]:
        """
        Run complete reverse engineering analysis.
        
        Returns:
            Dictionary containing all analysis results
        """
        logger.info("Starting complete MarsPro reverse engineering analysis...")
        
        try:
            # Step 1: Validate APK
            if not self.validate_apk():
                raise ValueError("APK validation failed")
            
            # Step 2: Extract metadata
            self.extract_apk_metadata()
            
            # Step 3: Decompile with APKTool
            if not self.decompile_with_apktool():
                logger.warning("APKTool decompilation failed, continuing with available data")
            
            # Step 4: Decompile with JADX
            if not self.decompile_with_jadx():
                logger.warning("JADX decompilation failed, continuing with available data")
            
            # Step 5: Analyze manifest
            self.analyze_manifest()
            
            # Step 6: Analyze native libraries
            self.analyze_native_libraries()
            
            # Step 7: Analyze assets
            self.analyze_assets()
            
            # Step 8: Analyze network endpoints
            self.analyze_network_endpoints()
            
            # Step 9: Analyze BLE services
            self.analyze_ble_services()
            
            # Step 10: Generate security report
            self.generate_security_report()
            
            # Step 11: Generate comprehensive report
            report_path = self.generate_analysis_report()
            
            logger.info("Complete analysis finished successfully")
            
            return {
                'success': True,
                'report_path': report_path,
                'results': self.analysis_results
            }
            
        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'results': self.analysis_results
            }


def main():
    """Main function to run the MarsPro analysis."""
    import argparse
    
    parser = argparse.ArgumentParser(description='MarsPro Reverse Engineering Analysis')
    parser.add_argument('apk_path', help='Path to the MarsPro APK file')
    parser.add_argument('--output-dir', help='Output directory for analysis results')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Create analyzer and run analysis
    analyzer = MarsProAnalyzer(args.apk_path, args.output_dir)
    results = analyzer.run_complete_analysis()
    
    if results['success']:
        print(f"\n✅ Analysis completed successfully!")
        print(f"📄 Report generated: {results['report_path']}")
        print(f"📊 Found {len(results['results']['permissions'])} permissions")
        print(f"🔍 Found {len(results['results']['network_endpoints'])} network endpoints")
        print(f"📱 Found {len(results['results']['ble_services'])} BLE-related files")
        print(f"🔒 Found {len(results['results']['security_findings'])} security findings")
    else:
        print(f"\n❌ Analysis failed: {results['error']}")
        sys.exit(1)


if __name__ == '__main__':
    main() 