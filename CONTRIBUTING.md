# Contributing to Google ADK Deepfake Detection Agent

Thank you for your interest in contributing to our project! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues
1. **Search existing issues** first to avoid duplicates
2. **Use the issue template** when creating new issues
3. **Provide detailed information** including:
   - Steps to reproduce the problem
   - Expected vs actual behavior
   - System information (OS, Python version)
   - Error messages and logs

### Submitting Changes

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/Project-JER.git
   cd Project-JER
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-description
   ```

3. **Make your changes**
   - Follow the code style guidelines
   - Add tests for new functionality
   - Update documentation as needed

4. **Test your changes**
   ```bash
   # Test local web interface
   python google_agent/adk_local.py
   
   # Test terminal interface
   python google_agent/adk_terminal.py
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new detection algorithm"
   # or
   git commit -m "fix: resolve UI status display issue"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Submit a Pull Request**
   - Use descriptive title and description
   - Link related issues
   - Include screenshots for UI changes

## 📝 Code Style Guidelines

### Python Code Style
- Follow **PEP 8** style guidelines
- Use **type hints** where appropriate
- Add **docstrings** for functions and classes
- Keep functions focused and small
- Use meaningful variable names

### Example:
```python
def detect_deepfake(file_path: str, confidence_threshold: float = 0.8) -> dict:
    """
    Detect if an image contains AI-generated content.
    
    Args:
        file_path: Path to the image file
        confidence_threshold: Minimum confidence for positive detection
        
    Returns:
        Dictionary containing detection results and confidence score
    """
    # Implementation here
    pass
```

### File Organization
- Keep related functionality in the same module
- Use clear, descriptive file names
- Organize imports: standard library, third-party, local
- Add type hints and docstrings

### Web Interface Guidelines
- Use semantic HTML elements
- Follow accessibility best practices
- Maintain responsive design
- Include proper error handling

## 🧪 Testing Guidelines

### Before Submitting
1. **Test all interfaces**:
   - Local web interface (`adk_local.py`)
   - Terminal interface (`adk_terminal.py`)
   - Web interface with backend (`adk_web_fixed.py`)

2. **Verify functionality**:
   - File upload and analysis
   - Chat interactions
   - Status indicators
   - Error handling

3. **Check for regressions**:
   - Existing features still work
   - No broken links or UI elements
   - All endpoints respond correctly

### Test Checklist
- [ ] Local web server starts successfully
- [ ] File upload works for images and audio
- [ ] Detection results display correctly
- [ ] Chat interface responds appropriately
- [ ] Status indicators show correct information
- [ ] Error messages are user-friendly
- [ ] No console errors in browser

## 🏗️ Development Setup

### Prerequisites
- Python 3.8+
- Virtual environment tools
- Git

### Local Development
1. **Clone and setup**:
   ```bash
   git clone https://github.com/yourusername/Project-JER.git
   cd Project-JER
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv projectjer
   # Windows
   .\projectjer\Scripts\activate
   # Linux/Mac
   source projectjer/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Start development server**:
   ```bash
   cd google_agent
   python adk_local.py
   ```

### Project Structure
```
google_agent/
├── adk_local.py       # Main local web server
├── adk_terminal.py    # Terminal interface
├── adk_web_fixed.py   # Full web interface
└── templates/         # HTML templates
```

## 📋 Commit Message Guidelines

Use conventional commit messages:

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

### Examples:
```
feat: add real-time audio detection
fix: resolve UI status display issue
docs: update installation instructions
style: format code according to PEP 8
refactor: simplify detection algorithm
test: add unit tests for file upload
chore: update dependencies
```

## 🔍 Code Review Process

### For Contributors
- **Self-review** your code before submitting
- **Test thoroughly** on different browsers/systems
- **Document** any breaking changes
- **Respond promptly** to review feedback

### For Reviewers
- **Be constructive** and specific in feedback
- **Test the changes** locally when possible
- **Check for security** implications
- **Verify documentation** is updated

## 🎯 Areas for Contribution

### High Priority
- **Real ML Integration**: Connect actual detection models
- **Performance Optimization**: Improve response times
- **Error Handling**: Better error messages and recovery
- **Documentation**: More examples and tutorials

### Medium Priority
- **UI/UX Improvements**: Better user experience
- **Additional File Formats**: Support more media types
- **Internationalization**: Multi-language support
- **Accessibility**: Screen reader compatibility

### Low Priority
- **Advanced Features**: Batch processing, analytics
- **Integration**: Third-party service connectors
- **Deployment**: Additional deployment options
- **Monitoring**: Usage analytics and logging

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Documentation**: Check existing docs first
- **Code Comments**: Read inline documentation

## 🙏 Recognition

Contributors will be:
- **Listed** in the project contributors
- **Mentioned** in release notes for significant contributions
- **Credited** in documentation for major features

Thank you for helping make this project better! 🚀
