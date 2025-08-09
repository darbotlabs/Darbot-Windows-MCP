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
    
    // Check if we're on Windows (non-blocking warning for development)
    if (process.platform !== 'win32') {
        console.log(chalk.yellow('⚠️  This package is designed for Windows'));
        console.log(chalk.gray('   Some features may not work on other platforms'));
    }
    
    // Check Python (non-blocking)
    const spinner = ora('Checking Python installation...').start();
    try {
        const result = await runCommand('python', ['--version']);
        const version = result.stdout.trim();
        
        if (!version.includes('3.12') && !version.includes('3.13') && !version.includes('3.14') && !version.includes('3.15')) {
            spinner.warn('Python 3.12+ recommended but not found');
            console.log(chalk.yellow('⚠️  For full functionality, install Python 3.12+'));
            console.log(chalk.cyan('   Download from: https://www.python.org/downloads/'));
            console.log(chalk.gray('   Run "darbot-setup" after installing Python'));
        } else {
            spinner.succeed(`Found ${version}`);
        }
    } catch (error) {
        spinner.warn('Python not detected');
        console.log(chalk.yellow('⚠️  Python 3.12+ not found in PATH'));
        console.log(chalk.cyan('   For full functionality, install Python 3.12+'));
        console.log(chalk.cyan('   Download from: https://www.python.org/downloads/'));
        console.log(chalk.gray('   Run "darbot-setup" after installing Python'));
    }
    
    console.log(chalk.green('✅ Package installation complete!'));
    console.log(chalk.cyan('\nNext steps:'));
    console.log('1. Run "darbot-setup" to complete setup and configure dependencies');
    console.log('2. Or run "darbot-windows-mcp --help" for manual configuration');
}

if (require.main === module) {
    install().catch((error) => {
        console.error(chalk.yellow('⚠️  Installation completed with warnings:'), error.message);
        console.log(chalk.cyan('\nRun "darbot-setup" to complete the setup process'));
        // Don't exit with failure to allow npm install to succeed
        process.exit(0);
    });
}

module.exports = { install };
