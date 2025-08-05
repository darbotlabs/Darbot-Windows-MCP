const { spawn } = require('child_process');
const chalk = require('chalk');
const path = require('path');

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

async function test() {
    console.log(chalk.blue.bold('🪟 Testing Darbot Windows MCP Installation'));
    console.log(chalk.gray('    Desktop automation for AI agents'));
    console.log('');
    
    const packageDir = path.dirname(__dirname);
    const mainPyPath = path.join(packageDir, 'main.py');
    
    // Test 1: Check if main.py exists
    console.log(chalk.cyan('1. Checking main.py...'));
    try {
        require('fs').accessSync(mainPyPath);
        console.log(chalk.green('   ✅ main.py found'));
    } catch (error) {
        console.log(chalk.red('   ❌ main.py not found'));
        return false;
    }
    
    // Test 2: Test UV if available
    console.log(chalk.cyan('2. Testing UV...'));
    try {
        await runCommand('uv', ['--version']);
        console.log(chalk.green('   ✅ UV available'));
        
        // Test UV run
        try {
            await runCommand('uv', ['--directory', packageDir, 'run', 'python', mainPyPath, '--help'], { timeout: 10000 });
            console.log(chalk.green('   ✅ UV can run the server'));
        } catch (error) {
            console.log(chalk.yellow('   ⚠️  UV found but server test failed'));
        }
    } catch (error) {
        console.log(chalk.yellow('   ⚠️  UV not available, will use Python'));
    }
    
    // Test 3: Test Python
    console.log(chalk.cyan('3. Testing Python...'));
    try {
        const result = await runCommand('python', ['--version']);
        console.log(chalk.green(`   ✅ Python available: ${result.stdout.trim()}`));
        
        // Test Python run
        try {
            await runCommand('python', [mainPyPath, '--help'], { 
                cwd: packageDir,
                timeout: 10000 
            });
            console.log(chalk.green('   ✅ Python can run the server'));
        } catch (error) {
            console.log(chalk.red('   ❌ Python server test failed'));
            console.log(chalk.red(`   Error: ${error.message}`));
            return false;
        }
    } catch (error) {
        console.log(chalk.red('   ❌ Python not available'));
        return false;
    }
    
    console.log(chalk.green.bold('\n🎉 All tests passed! The installation is working correctly.'));
    console.log(chalk.cyan('\nTo get started:'));
    console.log('• Run "darbot-setup" to configure VS Code and Claude Desktop');
    console.log('• Or run "darbot-windows-mcp" to start the server directly');
    
    return true;
}

if (require.main === module) {
    test().catch((error) => {
        console.error(chalk.red('❌ Test failed:'), error.message);
        process.exit(1);
    });
}

module.exports = { test };
