# Contributing to MarsPro Home Assistant Integration

Thank you for your interest in contributing to the MarsPro reverse engineering and Home Assistant integration project! This document provides guidelines and information for contributors.

## 🎯 Project Goals

- Reverse engineer MarsPro Android app communication protocols
- Create local Home Assistant integration for MarsPro devices
- Provide comprehensive documentation and analysis tools
- Enable community-driven development and improvement

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Home Assistant instance
- Git
- Basic knowledge of Python and Home Assistant development

### Development Setup

1. **Fork the repository**
   ```bash
   git clone https://github.com/your-username/marspro-analysis.git
   cd marspro-analysis
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up development environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install development dependencies
   pip install -r requirements-dev.txt
   ```

## 📁 Project Structure

```
MarsPro/
├── custom_components/marspro/  # Home Assistant integration
├── docs/                       # Documentation
├── scripts/                    # Analysis and utility scripts
├── tests/                      # Test files
└── configuration_samples/      # Configuration examples
```

## 🔧 Development Guidelines

### Code Style

- Follow PEP 8 Python style guidelines
- Use type hints for all function parameters and return values
- Write docstrings for all functions and classes
- Keep functions small and focused

### Home Assistant Integration

- Follow Home Assistant integration development guidelines
- Use async/await patterns
- Implement proper error handling
- Add comprehensive logging

### Testing

- Write unit tests for new features
- Test with real devices when possible
- Include integration tests for Home Assistant components

### Documentation

- Update README.md for new features
- Add configuration examples
- Document any new protocols or APIs discovered

## 🐛 Bug Reports

Before reporting a bug:

1. Check existing issues for similar problems
2. Enable debug logging and include relevant logs
3. Provide device information and environment details
4. Include steps to reproduce the issue

Use the bug report template when creating issues.

## 💡 Feature Requests

When requesting features:

1. Describe the use case and problem being solved
2. Provide device information if relevant
3. Consider implementation complexity
4. Check if the feature aligns with project goals

Use the feature request template when creating issues.

## 🔬 Reverse Engineering Contributions

### Analysis Tools

- **Frida Scripts**: Create hooks for new protocols or APIs
- **Static Analysis**: Improve APK analysis and documentation
- **Protocol Documentation**: Document discovered communication protocols

### Guidelines

- Respect intellectual property and terms of service
- Focus on educational and interoperability purposes
- Document findings thoroughly
- Share tools and methodologies with the community

## 📝 Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow coding guidelines
   - Add tests for new functionality
   - Update documentation

3. **Test your changes**
   ```bash
   # Run tests
   python -m pytest tests/
   
   # Test Home Assistant integration
   # Copy to your Home Assistant config and test
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: brief description"
   ```

5. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Submit pull request**
   - Use descriptive title and description
   - Reference related issues
   - Include testing information

## 🏷️ Commit Message Guidelines

Use conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Maintenance tasks

Examples:
```
feat(api): add support for new device type
fix(ble): resolve connection timeout issue
docs(readme): update installation instructions
```

## 🔍 Code Review Process

1. **Automated checks** must pass
2. **Code review** by maintainers
3. **Testing** with real devices when applicable
4. **Documentation** updates included

## 📚 Resources

- [Home Assistant Developer Documentation](https://developers.home-assistant.io/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Frida Documentation](https://frida.re/docs/)
- [BLE Development Guide](https://developer.android.com/guide/topics/connectivity/bluetooth-le)

## 🤝 Community Guidelines

- Be respectful and inclusive
- Help other contributors
- Share knowledge and findings
- Follow the project's code of conduct

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

## 🙏 Acknowledgments

Thank you for contributing to the MarsPro integration project! Your contributions help make local device control accessible to everyone. 