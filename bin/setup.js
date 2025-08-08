#!/usr/bin/env node

const fs = require('fs-extra');
const path = require('path');
const { spawn } = require('child_process');
const chalk = require('chalk');
const ora = require('ora');
const inquirer = require('inquirer');

class DarbotSetup {
    constructor() {
        this.packageDir = path.dirname(__dirname);
        this.workspaceDir = process.cwd();
    }

    async run() {
        console.log(chalk.blue.bold('🪟 Darbot Windows MCP Setup Wizard'));
        console.log(chalk.gray('    Desktop automation for AI agents'));
        console.log('');
        
        // Check system requirements
        await this.checkSystemRequirements();
        
        // Ask user preferences
        const preferences = await this.getUserPreferences();
        
        // Install dependencies
        await this.installDependencies(preferences);
        
        // Configure VS Code
        if (preferences.configureVSCode) {
            await this.configureVSCode(preferences);
        }
        
        // Configure Claude Desktop
        if (preferences.configureClaude) {
            await this.configureClaude();
        }
        
        console.log(chalk.green.bold('\n🎉 Setup completed successfully!'));
        console.log(chalk.cyan('\nNext steps:'));
        console.log('• Restart VS Code if you configured it');
        console.log('• Restart Claude Desktop if you configured it');
        console.log('• Run "darbot-windows-mcp --help" for usage information');
    }

    async checkSystemRequirements() {
        const spinner = ora('Checking system requirements...').start();
        
        try {
            // Check Python
            const pythonResult = await this.runCommand('python', ['--version']);
            const pythonVersion = pythonResult.stdout.trim();
            
            if (!pythonVersion.includes('3.12') && !pythonVersion.includes('3.13') && !pythonVersion.includes('3.14') && !pythonVersion.includes('3.15')) {
                spinner.fail('Python 3.12+ is required');
                console.log(chalk.red('Please install Python 3.12 or higher'));
                process.exit(1);
            }
            
            spinner.succeed(`Found ${pythonVersion}`);
        } catch (error) {
            spinner.fail('Python not found');
            console.log(chalk.red('Please install Python 3.12+ and ensure it\'s in your PATH'));
            process.exit(1);
        }
    }

    async getUserPreferences() {
        return await inquirer.prompt([
            {
                type: 'list',
                name: 'installMethod',
                message: 'Choose installation method:',
                choices: [
                    { name: 'UV (Recommended - faster, modern)', value: 'uv' },
                    { name: 'Standard Python (pip + venv)', value: 'python' }
                ],
                default: 'uv'
            },
            {
                type: 'confirm',
                name: 'configureVSCode',
                message: 'Configure VS Code MCP integration?',
                default: true
            },
            {
                type: 'confirm',
                name: 'configureClaude',
                message: 'Configure Claude Desktop integration?',
                default: true
            }
        ]);
    }

    async installDependencies(preferences) {
        if (preferences.installMethod === 'uv') {
            await this.installWithUV();
        } else {
            await this.installWithPython();
        }
    }

    async installWithUV() {
        let spinner = ora('Installing UV...').start();
        
        try {
            // Check if UV is already installed
            await this.runCommand('uv', ['--version']);
            spinner.succeed('UV already installed');
        } catch (error) {
            try {
                await this.runCommand('python', ['-m', 'pip', 'install', 'uv']);
                spinner.succeed('UV installed successfully');
            } catch (installError) {
                spinner.fail('Failed to install UV');
                throw installError;
            }
        }
        
        spinner = ora('Installing Python dependencies with UV...').start();
        try {
            await this.runCommand('uv', ['sync'], { cwd: this.packageDir });
            spinner.succeed('Dependencies installed successfully');
        } catch (error) {
            spinner.fail('Failed to install dependencies');
            throw error;
        }
    }

    async installWithPython() {
        const spinner = ora('Installing Python dependencies...').start();
        
        try {
            // Create virtual environment in package directory if it doesn't exist
            const venvPath = path.join(this.packageDir, 'venv');
            if (!fs.existsSync(venvPath)) {
                await this.runCommand('python', ['-m', 'venv', 'venv'], { cwd: this.packageDir });
            }
            
            // Install requirements
            const requirementsPath = path.join(this.packageDir, 'requirements.txt');
            const pythonPath = path.join(venvPath, 'Scripts', 'python.exe');
            
            await this.runCommand(pythonPath, ['-m', 'pip', 'install', '-r', requirementsPath]);
            
            spinner.succeed('Dependencies installed successfully');
        } catch (error) {
            spinner.fail('Failed to install dependencies');
            throw error;
        }
    }

    async configureVSCode(preferences) {
        const spinner = ora('Configuring VS Code...').start();
        
        try {
            const vscodeDir = path.join(this.workspaceDir, '.vscode');
            await fs.ensureDir(vscodeDir);
            
            // Create mcp.json
            const mcpConfig = this.createMCPConfig(preferences);
            await fs.writeJSON(path.join(vscodeDir, 'mcp.json'), mcpConfig, { spaces: 2 });
            
            // Create settings.json
            const settingsPath = path.join(vscodeDir, 'settings.json');
            let settings = {};
            
            if (fs.existsSync(settingsPath)) {
                settings = await fs.readJSON(settingsPath);
            }
            
            settings['mcp.servers'] = settings['mcp.servers'] || {};
            settings['mcp.servers']['darbot-windows-mcp'] = this.createSettingsConfig(preferences);
            
            await fs.writeJSON(settingsPath, settings, { spaces: 2 });
            
            spinner.succeed('VS Code configured successfully');
        } catch (error) {
            spinner.fail('Failed to configure VS Code');
            throw error;
        }
    }

    async configureClaude() {
        const spinner = ora('Configuring Claude Desktop...').start();
        
        try {
            const claudeConfigDir = path.join(process.env.APPDATA, 'Claude');
            const claudeConfigPath = path.join(claudeConfigDir, 'claude_desktop_config.json');
            
            await fs.ensureDir(claudeConfigDir);
            
            let config = {};
            if (fs.existsSync(claudeConfigPath)) {
                config = await fs.readJSON(claudeConfigPath);
            }
            
            config.mcpServers = config.mcpServers || {};
            config.mcpServers['darbot-windows-mcp'] = {
                command: 'darbot-windows-mcp',
                args: []
            };
            
            await fs.writeJSON(claudeConfigPath, config, { spaces: 2 });
            
            spinner.succeed('Claude Desktop configured successfully');
        } catch (error) {
            spinner.fail('Failed to configure Claude Desktop');
            console.log(chalk.yellow('You may need to configure Claude Desktop manually'));
        }
    }

    createMCPConfig(preferences) {
        const config = {
            servers: {
                'darbot-windows-mcp': {
                    type: 'stdio'
                }
            },
            inputs: []
        };
        
        if (preferences.installMethod === 'uv') {
            config.servers['darbot-windows-mcp'].command = 'uv';
            config.servers['darbot-windows-mcp'].args = [
                '--directory',
                this.packageDir,
                'run',
                'python',
                path.join(this.packageDir, 'main.py')
            ];
        } else {
            const venvPython = path.join(this.packageDir, 'venv', 'Scripts', 'python.exe');
            config.servers['darbot-windows-mcp'].command = venvPython;
            config.servers['darbot-windows-mcp'].args = [path.join(this.packageDir, 'main.py')];
            config.servers['darbot-windows-mcp'].cwd = this.packageDir;
        }
        
        return config;
    }

    createSettingsConfig(preferences) {
        const config = {
            env: {}
        };
        
        if (preferences.installMethod === 'uv') {
            config.command = 'uv';
            config.args = [
                '--directory',
                this.packageDir,
                'run',
                'python',
                path.join(this.packageDir, 'main.py')
            ];
        } else {
            const venvPython = path.join(this.packageDir, 'venv', 'Scripts', 'python.exe');
            config.command = venvPython;
            config.args = [path.join(this.packageDir, 'main.py')];
            config.cwd = this.packageDir;
        }
        
        return config;
    }

    runCommand(command, args = [], options = {}) {
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
}

// Run setup if called directly
if (require.main === module) {
    const setup = new DarbotSetup();
    setup.run().catch((error) => {
        console.error(chalk.red('❌ Setup failed:'), error.message);
        process.exit(1);
    });
}
