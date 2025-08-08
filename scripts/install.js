const { spawn } = require('child_process');
const chalk = require('chalk');
const ora = require('ora');

function runCommand(command, args = [], options = {}) {
    return new Promise((resolve, reject) => {
        const process = spawn(command, args, {
            stdio: 'pipe',
            ...options
        });
        
        let stdout = '';
        let stderr = '';
        
        process.stdout?.on('data', (data) => {
            stdout += data.toString();
        });
        
        process.stderr?.on('data', (data) => {
            stderr += data.toString();
        });
        
        process.on('close', (code) => {
            if (code === 0) {
                resolve({ stdout, stderr });
            } else {
                reject(new Error(`Command failed with code ${code}: ${stderr}`));
            }
        });
        
        process.on('error', reject);
    });
}

async function install() {
    console.log(chalk.blue.bold('🪟 Installing Darbot Windows MCP...'));
    console.log(chalk.gray('    Desktop automation for AI agents'));
    console.log('');
    
    // Check if we're on Windows
    if (process.platform !== 'win32') {
        console.log(chalk.red('❌ This package only works on Windows'));
        process.exit(1);
    }
    
    // Check Python
    const spinner = ora('Checking Python installation...').start();
    try {
        const result = await runCommand('python', ['--version']);
        const version = result.stdout.trim();
        
        if (!version.includes('3.12') && !version.includes('3.13') && !version.includes('3.14') && !version.includes('3.15')) {
            spinner.fail('Python 3.12+ is required');
            console.log(chalk.red('Please install Python 3.12 or higher'));
            console.log(chalk.cyan('Download from: https://www.python.org/downloads/'));
            process.exit(1);
        }
        
        spinner.succeed(`Found ${version}`);
    } catch (error) {
        spinner.fail('Python not found');
        console.log(chalk.red('Please install Python 3.12+ and ensure it\'s in your PATH'));
        console.log(chalk.cyan('Download from: https://www.python.org/downloads/'));
        process.exit(1);
    }
    
    console.log(chalk.green('✅ Installation complete!'));
    console.log(chalk.cyan('\nNext steps:'));
    console.log('1. Run "darbot-setup" to configure VS Code and Claude Desktop');
    console.log('2. Or run "darbot-windows-mcp --help" for manual setup');
}

if (require.main === module) {
    install().catch((error) => {
        console.error(chalk.red('❌ Installation failed:'), error.message);
        process.exit(1);
    });
}

module.exports = { install };
