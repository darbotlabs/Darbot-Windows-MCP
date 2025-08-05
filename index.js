const path = require('path');

// Export the main server path for programmatic use
module.exports = {
    serverPath: path.join(__dirname, 'main.py'),
    packageDir: __dirname,
    
    // Start the server programmatically
    start: function(options = {}) {
        const { spawn } = require('child_process');
        const mainPyPath = path.join(__dirname, 'main.py');
        
        // Try UV first, fall back to Python
        const uvProcess = spawn('uv', ['--version'], { stdio: 'pipe' });
        
        return new Promise((resolve, reject) => {
            uvProcess.on('close', (code) => {
                let command, args;
                
                if (code === 0) {
                    command = 'uv';
                    args = ['--directory', __dirname, 'run', 'python', mainPyPath];
                } else {
                    command = 'python';
                    args = [mainPyPath];
                }
                
                const mcpProcess = spawn(command, args, {
                    stdio: options.stdio || 'inherit',
                    cwd: __dirname,
                    ...options
                });
                
                resolve(mcpProcess);
            });
            
            uvProcess.on('error', () => {
                const mcpProcess = spawn('python', [mainPyPath], {
                    stdio: options.stdio || 'inherit',
                    cwd: __dirname,
                    ...options
                });
                
                resolve(mcpProcess);
            });
        });
    }
};
