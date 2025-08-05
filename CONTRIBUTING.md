# Contributing to Darbot Windows MCP

Thank you for your interest in contributing to Darbot Windows MCP! This document provides guidelines and instructions for contributing to this project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Issue Guidelines](#issue-guidelines)
- [Documentation Guidelines](#documentation-guidelines)

## Code of Conduct

By participating in this project, you agree to abide by our code of conduct:

- Be respectful and inclusive
- Focus on constructive feedback
- Help maintain a positive community
- Report any unacceptable behavior

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/Darbot-Windows-MCP.git
   cd Darbot-Windows-MCP
   ```
3. **Set up development environment** (see [Development Guide](DEVELOPMENT.md))
4. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## How to Contribute

### Types of Contributions

- 🐛 **Bug fixes** - Fix issues in existing functionality
- ✨ **New features** - Add new tools or capabilities
- 📖 **Documentation** - Improve or add documentation
- 🧪 **Tests** - Add or improve test coverage
- 🎨 **Code quality** - Refactoring, performance improvements

### Areas We Need Help

- Adding new Windows automation tools
- Improving error handling and reliability
- Cross-platform compatibility testing
- Documentation improvements
- Performance optimizations

## Development Setup

See the comprehensive [Development Guide](DEVELOPMENT.md) for detailed setup instructions.

## Pull Request Process

1. **Ensure your fork is up to date:**
   ```bash
   git remote add upstream https://github.com/darbotlabs/Darbot-Windows-MCP.git
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

2. **Create feature branch:**
   ```bash
   git checkout -b feature/descriptive-name
   ```

3. **Make your changes:**
   - Follow coding standards
   - Add tests if applicable
   - Update documentation
   - Test thoroughly

4. **Commit with clear messages:**
   ```bash
   git add .
   git commit -m "Add new tool: ToolName-Tool for specific functionality"
   ```

5. **Push to your fork:**
   ```bash
   git push origin feature/descriptive-name
   ```

6. **Create Pull Request:**
   - Use descriptive title
   - Explain what changes were made and why
   - Reference any related issues
   - Include testing information

### Pull Request Requirements

- ✅ **Code compiles** without errors
- ✅ **Tests pass** (if tests exist)
- ✅ **Documentation updated** for new features
- ✅ **No breaking changes** unless absolutely necessary
- ✅ **Clear commit messages**
- ✅ **Issue references** where applicable

## Issue Guidelines

### Reporting Bugs

When reporting bugs, include:

```
**Bug Description**
Clear description of the issue

**Steps to Reproduce**
1. Step one
2. Step two
3. Expected vs actual result

**System Information**
- Windows version: 
- Python version:
- Installation method:
- VS Code version (if applicable):

**Error Messages**
Include full error messages and stack traces

**Additional Context**
Any other relevant information
```

### Feature Requests

For feature requests, include:

- **Use case**: Why is this feature needed?
- **Proposed solution**: How should it work?
- **Alternatives considered**: Other approaches you've thought about
- **Implementation ideas**: Technical suggestions if you have them

### Good First Issues

Look for issues labeled `good first issue` or `help wanted` if you're new to the project.

## Documentation Guidelines

### Writing Style

- Use clear, concise language
- Include code examples where helpful
- Maintain consistent formatting
- Update table of contents when needed

### Documentation Types

- **README.md** - Project overview and quick start
- **INSTALLATION.md** - Detailed setup instructions
- **TOOLS.md** - Comprehensive tool documentation
- **TROUBLESHOOTING.md** - Problem-solving guide
- **DEVELOPMENT.md** - Development and contribution info

### Code Documentation

- Add docstrings to new functions
- Comment complex logic
- Include type hints
- Update tool descriptions in README

## Recognition

Contributors will be recognized in:

- **CONTRIBUTORS.md** file (if created)
- **Release notes** for significant contributions
- **GitHub contributors page**

## Getting Help

If you need help contributing:

1. **Read existing documentation** thoroughly
2. **Search existing issues** for similar problems
3. **Join discussions** in GitHub Issues/Discussions
4. **Ask questions** in new issues with `question` label

## Thank You

Every contribution helps make Darbot Windows MCP better for everyone. Whether it's fixing a typo, adding a feature, or helping with documentation, your efforts are appreciated!

For detailed development information, see the [Development Guide](DEVELOPMENT.md).