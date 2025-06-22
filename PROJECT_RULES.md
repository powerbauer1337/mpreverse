# MarsPro Project Rules & Standards

## 🎯 Project Mission

**Primary Goal**: Reverse engineer MarsPro smart devices to enable local Home Assistant integration without cloud dependency.

**Secondary Goals**:
- Create comprehensive documentation of discovered protocols
- Develop reusable analysis tools and MCP servers
- Establish best practices for reverse engineering workflows
- Maintain high code quality and security standards

## 📋 Core Principles

### 1. Security First
- **Never commit sensitive data** (API keys, credentials, device tokens)
- **Use environment variables** for all configuration
- **Validate all inputs** to prevent injection attacks
- **Follow OWASP guidelines** for web security
- **Document security considerations** in analysis reports

### 2. Documentation Driven
- **Document everything** - protocols, APIs, decisions, workflows
- **Keep documentation up-to-date** with code changes
- **Use clear, consistent formatting** (Markdown with emojis)
- **Include examples** for all documented features
- **Version control documentation** alongside code

### 3. Quality Assurance
- **Write tests for all new code** (unit + integration)
- **Use type hints** in Python code
- **Follow PEP 8** style guidelines
- **Run linters** before committing (black, flake8, mypy)
- **Code review required** for all changes

### 4. Reproducible Analysis
- **Version control all tools** and dependencies
- **Document analysis steps** in detail
- **Store analysis artifacts** in versioned directories
- **Use deterministic tools** where possible
- **Backup analysis results** regularly

## 🏗️ Project Structure Rules

### Directory Organization
```
MarsPro/
├── src/                    # Source code only
├── analysis/               # Analysis results and documentation
├── assets/                 # Static assets (APKs, tools, binaries)
├── config/                 # Configuration files
├── docs/                   # Project documentation
├── scripts/                # Automation and analysis scripts
├── tools/                  # External tools and MCP servers
├── tests/                  # Test suite
└── output/                 # Generated files (gitignored)
```

### File Naming Conventions
- **Python files**: `snake_case.py`
- **Configuration files**: `kebab-case.yaml` or `snake_case.json`
- **Documentation**: `PascalCase.md` for main docs, `snake_case.md` for specific topics
- **Scripts**: `verb_noun.py` (e.g., `analyze_apk.py`, `setup_tools.py`)
- **Directories**: `snake_case/` for Python packages, `kebab-case/` for others

## 🔧 Development Standards

### Python Code Standards
```python
# Required imports order
import os
import sys
from typing import Dict, List, Optional, Union

# Third-party imports
import requests
from homeassistant.core import HomeAssistant

# Local imports
from .const import DOMAIN, CONF_USERNAME
from .api import MarsProAPI

# Type hints required for all functions
def analyze_apk(apk_path: str, output_dir: Optional[str] = None) -> Dict[str, any]:
    """
    Analyze APK file and extract relevant information.
    
    Args:
        apk_path: Path to the APK file
        output_dir: Output directory for results (optional)
        
    Returns:
        Dictionary containing analysis results
        
    Raises:
        FileNotFoundError: If APK file doesn't exist
        ValueError: If APK file is invalid
    """
    pass
```

### Documentation Standards
```markdown
# Section Title

## Subsection

### Code Examples
```python
# Always include working code examples
def example_function():
    return "Hello World"
```

### Configuration Examples
```yaml
# YAML configuration examples
marspro:
  username: user@example.com
  password: !secret marspro_password
```

### Important Notes
> **Note**: Important information goes in blockquotes
> 
> **Warning**: Security warnings and critical information
```

## 🔍 Analysis Workflow Rules

### Phase 1: Static Analysis
1. **APK Validation**
   - Verify APK integrity and signature
   - Extract APK metadata (version, permissions, etc.)
   - Document APK characteristics

2. **Decompilation**
   - Use APKTool for resource extraction
   - Use JADX for Java code decompilation
   - Store outputs in versioned directories
   - Document any decompilation issues

3. **Code Analysis**
   - Identify key classes and methods
   - Map API endpoints and BLE services
   - Document encryption and security measures
   - Create call graphs for critical functions

### Phase 2: Dynamic Analysis
1. **Environment Setup**
   - Use isolated testing environment
   - Document device setup and configuration
   - Establish baseline behavior

2. **Traffic Analysis**
   - Intercept HTTP/HTTPS traffic with Frida
   - Monitor BLE communication
   - Document all network patterns
   - Store traffic logs securely

3. **Behavior Analysis**
   - Test all device functions
   - Document state changes
   - Identify timing dependencies
   - Map user actions to network traffic

### Phase 3: Protocol Documentation
1. **API Documentation**
   - Document all endpoints with examples
   - Map request/response formats
   - Document authentication methods
   - Include error handling patterns

2. **BLE Protocol**
   - Document service UUIDs
   - Map characteristic UUIDs
   - Document data formats
   - Include pairing procedures

3. **Security Analysis**
   - Document encryption methods
   - Identify vulnerabilities
   - Document mitigation strategies
   - Include security recommendations

## 🧪 Testing Standards

### Test Structure
```python
# tests/unit/test_api.py
import pytest
from unittest.mock import Mock, patch
from src.marspro.api import MarsProAPI

class TestMarsProAPI:
    """Test suite for MarsPro API client."""
    
    @pytest.fixture
    def api_client(self):
        """Create API client for testing."""
        return MarsProAPI("test@example.com", "password")
    
    def test_authentication_success(self, api_client):
        """Test successful authentication."""
        # Test implementation
        pass
    
    def test_authentication_failure(self, api_client):
        """Test authentication failure handling."""
        # Test implementation
        pass
```

### Test Requirements
- **Unit tests**: 90%+ code coverage
- **Integration tests**: All major workflows
- **Mock external dependencies**: No real API calls in tests
- **Test data**: Use fixtures and test data files
- **Performance tests**: For critical functions

## 🔒 Security Rules

### Credential Management
```python
# NEVER do this:
API_KEY = "sk-1234567890abcdef"  # ❌ Hardcoded credentials

# ALWAYS do this:
import os
API_KEY = os.getenv("MARSPRO_API_KEY")  # ✅ Environment variables
```

### Input Validation
```python
def validate_mac_address(mac: str) -> bool:
    """Validate MAC address format."""
    import re
    pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
    return bool(re.match(pattern, mac))

def process_device_data(data: Dict[str, any]) -> Dict[str, any]:
    """Process and validate device data."""
    required_fields = ['mac_address', 'device_type', 'name']
    
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")
    
    if not validate_mac_address(data['mac_address']):
        raise ValueError("Invalid MAC address format")
    
    return data
```

## 📝 Documentation Rules

### Analysis Reports
Every analysis phase must produce:
1. **Executive Summary**: Key findings and recommendations
2. **Technical Details**: Complete technical documentation
3. **Code Examples**: Working code for all discovered APIs
4. **Security Assessment**: Security findings and recommendations
5. **Implementation Guide**: Step-by-step implementation instructions

### Code Documentation
- **Docstrings**: All functions and classes
- **Type hints**: All function parameters and return values
- **Comments**: Complex logic and business rules
- **README files**: All major directories
- **API documentation**: All public APIs

## 🚀 Deployment Rules

### Home Assistant Integration
1. **Version compatibility**: Test with multiple HA versions
2. **Configuration validation**: Validate all user inputs
3. **Error handling**: Graceful error handling and user feedback
4. **Performance**: Optimize for HA performance requirements
5. **Security**: Follow HA security guidelines

### Release Process
1. **Version bump**: Update version in all relevant files
2. **Changelog**: Document all changes
3. **Testing**: Run full test suite
4. **Documentation**: Update all documentation
5. **Tagging**: Create git tag for release

## 🔄 Workflow Rules

### Git Workflow
1. **Branch naming**: `feature/description` or `fix/description`
2. **Commit messages**: Use conventional commits format
3. **Pull requests**: Required for all changes
4. **Code review**: At least one reviewer required
5. **Merge strategy**: Squash and merge for feature branches

### Issue Management
1. **Issue templates**: Use provided templates
2. **Labels**: Use appropriate labels for categorization
3. **Milestones**: Group related issues in milestones
4. **Assignees**: Assign issues to appropriate team members
5. **Progress tracking**: Update issue status regularly

## 📊 Quality Metrics

### Code Quality
- **Coverage**: Minimum 90% test coverage
- **Complexity**: Maximum cyclomatic complexity of 10
- **Duplication**: Maximum 5% code duplication
- **Documentation**: 100% public API documentation
- **Linting**: Zero linting errors

### Analysis Quality
- **Completeness**: All major functions documented
- **Accuracy**: All findings verified
- **Reproducibility**: All analysis steps documented
- **Security**: All security findings documented
- **Usability**: All findings actionable

## 🛠️ Tool Configuration

### Required Tools
- **Python**: 3.8+ with virtual environments
- **Git**: Version control with proper workflow
- **Docker**: For isolated testing environments
- **Frida**: For dynamic analysis
- **APKTool/JADX**: For static analysis
- **Home Assistant**: For integration testing

### Development Tools
- **Black**: Code formatting
- **Flake8**: Linting
- **MyPy**: Type checking
- **Pytest**: Testing framework
- **Pre-commit**: Git hooks
- **Sphinx**: Documentation generation

## 🚨 Emergency Procedures

### Security Incidents
1. **Immediate response**: Isolate affected systems
2. **Assessment**: Evaluate scope and impact
3. **Communication**: Notify stakeholders
4. **Remediation**: Fix security issues
5. **Documentation**: Document incident and lessons learned

### Data Breaches
1. **Containment**: Stop data exfiltration
2. **Investigation**: Determine cause and scope
3. **Notification**: Notify affected parties
4. **Recovery**: Restore systems and data
5. **Prevention**: Implement additional safeguards

## 📚 References

### Standards and Guidelines
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Home Assistant Development Guidelines](https://developers.home-assistant.io/)

### Tools and Resources
- [Frida Documentation](https://frida.re/docs/)
- [APKTool Documentation](https://ibotpeaches.github.io/Apktool/)
- [JADX Documentation](https://github.com/skylot/jadx)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

---

**Last Updated**: 2024-12-19
**Version**: 1.0.0
**Maintainer**: Project Team 