#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
const chalk = require('chalk');

// Get the directory where this package is installed
const packageDir = path.dirname(__dirname);
const mainPyPath = path.join(packageDir, 'main.py');

function runMCPServer() {
    console.log(chalk.blue.bold('🪟 Darbot Windows MCP Server'));
    console.log(chalk.gray('    Desktop automation for AI agents'));
    console.log('');
    
    // Check if UV is available
    const uvProcess = spawn('uv', ['--version'], { stdio: 'pipe' });
    
    uvProcess.on('close', (code) => {
        let command, args;
        
        if (code === 0) {
            // UV is available
            console.log(chalk.green('✅ UV detected - using optimized startup'));
            command = 'uv';
            args = ['--directory', packageDir, 'run', 'python', mainPyPath];
        } else {
            // Fall back to Python
            console.log(chalk.yellow('⚠️  UV not found - using standard Python'));
            command = 'python';
            args = [mainPyPath];
        }
        
        console.log(chalk.gray(`Starting: ${command} ${args.join(' ')}`));
        
        // Start the MCP server
        const mcpProcess = spawn(command, args, {
            stdio: 'inherit',
            cwd: packageDir
        });
        
        mcpProcess.on('error', (error) => {
            console.error(chalk.red('❌ Failed to start MCP server:'), error.message);
            if (error.code === 'ENOENT') {
                console.error(chalk.yellow('\n💡 Troubleshooting:'));
                console.error('• Run "darbot-setup" to install Python dependencies');
                console.error('• Make sure Python 3.12+ is installed and in PATH');
                console.error('• Download Python from: https://www.python.org/downloads/');
            }
            process.exit(1);
        });
        
        mcpProcess.on('close', (code) => {
            if (code !== 0) {
                console.error(chalk.red(`❌ MCP server exited with code ${code}`));
                if (code === 1) {
                    console.error(chalk.yellow('\n💡 This might be due to missing Python dependencies.'));
                    console.error('Run "darbot-setup" to install required dependencies.');
                }
                process.exit(code);
            }
        });
        
        // Handle graceful shutdown
        process.on('SIGINT', () => {
            console.log(chalk.yellow('\n🛑 Shutting down MCP server...'));
            mcpProcess.kill('SIGINT');
        });
        
        process.on('SIGTERM', () => {
            mcpProcess.kill('SIGTERM');
        });
    });
    
    uvProcess.on('error', () => {
        // UV command not found, fall back to Python
        console.log(chalk.yellow('⚠️  UV not found - using standard Python'));
        
        const mcpProcess = spawn('python', [mainPyPath], {
            stdio: 'inherit',
            cwd: packageDir
        });
        
        mcpProcess.on('error', (error) => {
            console.error(chalk.red('❌ Failed to start MCP server:'), error.message);
            if (error.code === 'ENOENT') {
                console.error(chalk.yellow('\n💡 Troubleshooting:'));
                console.error('• Run "darbot-setup" to install Python dependencies');
                console.error('• Make sure Python 3.12+ is installed and in PATH');
                console.error('• Download Python from: https://www.python.org/downloads/');
            }
            process.exit(1);
        });
    });
}

// Handle command line arguments
const args = process.argv.slice(2);

if (args.includes('--help') || args.includes('-h')) {
    console.log(chalk.blue.bold('🪟 Darbot Windows MCP Server'));
    console.log('');
    console.log('Usage:');
    console.log('  darbot-windows-mcp          Start the MCP server');
    console.log('  darbot-windows-mcp --help   Show this help message');
    console.log('  darbot-setup                Run the setup wizard');
    console.log('');
    console.log('For more information, visit: https://github.com/darbotlabs/Darbot-Windows-MCP');
} else {
    runMCPServer();
}
