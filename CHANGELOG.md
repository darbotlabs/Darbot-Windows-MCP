# Changelog

All notable changes to Darbot Windows MCP will be documented in this file.

## [1.1.0] - 2025-08-07

### Added
- **Scoped NPM Package**: Published as `@darbotlabs/darbot-windows-mcp`
- **Simplified Scroll-Tool API**: Direction-only parameters (up/down/left/right) with optional coordinates
- **Enhanced Type-Tool**: Quoted return text and explicit return type annotation
- **Optional Dependencies**: Graceful fallback for `live-inspect` (Python 3.13+) and `humancursor`
- **Python 3.12+ Support**: Lowered minimum Python requirement from 3.13 to 3.12

### Fixed
- **Shortcut-Tool**: Fixed f-string syntax error in return message
- **Clear Parameter**: Boolean comparison fix in Type-Tool (already present in darbotlabs base)
- **Dependency Compatibility**: Conditional installation for Python version-specific packages

### Improved
- **Documentation**: Updated README.md with clearer installation paths
- **Tools Reference**: Updated TOOLS.md with simplified Scroll-Tool parameters
- **Package Management**: Better error handling for missing dependencies
- **Logo Usage**: Consistent branding throughout documentation

### Technical Details
- Merged improvements from dayour version into darbotlabs codebase
- All 15 tools validated and working
- Enhanced NPM packaging with setup wizard
- Improved VS Code integration configuration

## [1.0.0] - 2025-01-XX

### Added
- Initial release with 15 Windows automation tools
- NPM package with global installation
- Setup wizard for VS Code and Claude Desktop
- Comprehensive documentation
- Professional branding and assets
