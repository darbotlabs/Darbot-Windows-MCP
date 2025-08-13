const chalk = require('chalk');

async function postinstall() {
    console.log(chalk.blue.bold('🪟 Darbot Windows MCP'));
    console.log(chalk.gray('    Desktop automation for AI agents'));
    console.log('');
    console.log(chalk.green('✅ Package installation complete!'));
    console.log('');
    console.log(chalk.cyan('🚀 For VSCode MCP integration:'));
    console.log('  1. Open VSCode settings (Ctrl+,)');
    console.log('  2. Search for "MCP" and add a new server');
    console.log('  3. Use server name: "darbot-windows-mcp"');
    console.log('  4. Command: "darbot-windows-mcp"');
    console.log('');
    console.log(chalk.cyan('🛠️  Complete setup:'));
    console.log('  darbot-setup              # Run the setup wizard (installs Python dependencies)');  
    console.log('');
    console.log(chalk.cyan('💻 Manual usage:'));
    console.log('  darbot-windows-mcp         # Start the MCP server');
    console.log('  darbot-windows-mcp --help  # Show help');
    console.log('');
    console.log(chalk.yellow('⚠️  Important: Run "darbot-setup" to install Python dependencies'));
    console.log(chalk.cyan('For more information: https://github.com/darbotlabs/Darbot-Windows-MCP'));
}

if (require.main === module) {
    postinstall();
}

module.exports = { postinstall };
