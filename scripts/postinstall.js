const chalk = require('chalk');

async function postinstall() {
    console.log(chalk.blue.bold('🪟 Darbot Windows MCP'));
    console.log(chalk.gray('    Desktop automation for AI agents'));
    console.log('');
    console.log(chalk.green('✅ Installation complete!'));
    console.log('');
    console.log(chalk.cyan('Quick start:'));
    console.log('  darbot-setup              # Run the setup wizard');  
    console.log('  darbot-windows-mcp         # Start the MCP server');
    console.log('  darbot-windows-mcp --help  # Show help');
    console.log('');
    console.log(chalk.cyan('For more information: https://github.com/darbotlabs/Darbot-Windows-MCP'));
}

if (require.main === module) {
    postinstall();
}

module.exports = { postinstall };
