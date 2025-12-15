/**
 * GhostLink Local - Electron Main Process
 * 100% Local System - No External Dependencies
 */

const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const http = require('http');

let mainWindow;
let pythonProcess;
const PYTHON_SERVER_PORT = 8765;
const PYTHON_SERVER_URL = `http://127.0.0.1:${PYTHON_SERVER_PORT}`;

// =============================================================================
// PYTHON SERVER MANAGEMENT
// =============================================================================

function startPythonServer() {
    console.log('🚀 Starting Python local server...');
    
    const pythonScript = path.join(__dirname, '..', 'local_server.py');
    
    pythonProcess = spawn('python3', [pythonScript], {
        stdio: ['inherit', 'pipe', 'pipe']
    });
    
    pythonProcess.stdout.on('data', (data) => {
        console.log(`[Python] ${data.toString()}`);
    });
    
    pythonProcess.stderr.on('data', (data) => {
        console.error(`[Python Error] ${data.toString()}`);
    });
    
    pythonProcess.on('close', (code) => {
        console.log(`Python server exited with code ${code}`);
    });
    
    // Wait for server to be ready
    return new Promise((resolve) => {
        const checkServer = setInterval(() => {
            http.get(PYTHON_SERVER_URL, (res) => {
                if (res.statusCode === 200) {
                    clearInterval(checkServer);
                    console.log('✅ Python server is ready');
                    resolve();
                }
            }).on('error', () => {
                // Server not ready yet, keep checking
            });
        }, 500);
    });
}

function stopPythonServer() {
    if (pythonProcess) {
        console.log('🛑 Stopping Python server...');
        pythonProcess.kill();
        pythonProcess = null;
    }
}

// =============================================================================
// WINDOW MANAGEMENT
// =============================================================================

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1400,
        height: 900,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
            enableRemoteModule: true
        },
        titleBarStyle: 'hiddenInset',
        backgroundColor: '#1a1a1a'
    });
    
    mainWindow.loadFile(path.join(__dirname, '..', 'ui', 'index.html'));
    
    // Open DevTools in development
    if (process.argv.includes('--dev')) {
        mainWindow.webContents.openDevTools();
    }
    
    mainWindow.on('closed', () => {
        mainWindow = null;
    });
}

// =============================================================================
// IPC HANDLERS - Communication with Renderer
// =============================================================================

ipcMain.handle('chat', async (event, prompt, mode = 'fast') => {
    try {
        const response = await fetch(`${PYTHON_SERVER_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt, mode })
        });
        return await response.json();
    } catch (error) {
        console.error('Chat error:', error);
        return { error: error.message };
    }
});

ipcMain.handle('analyze-code', async (event, code, language) => {
    try {
        const response = await fetch(`${PYTHON_SERVER_URL}/code/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code, language })
        });
        return await response.json();
    } catch (error) {
        console.error('Analyze error:', error);
        return { error: error.message };
    }
});

ipcMain.handle('refactor-code', async (event, code, language, instructions) => {
    try {
        const response = await fetch(`${PYTHON_SERVER_URL}/code/refactor`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code, language, instructions })
        });
        return await response.json();
    } catch (error) {
        console.error('Refactor error:', error);
        return { error: error.message };
    }
});

ipcMain.handle('health-check', async () => {
    try {
        const response = await fetch(`${PYTHON_SERVER_URL}/health`);
        return await response.json();
    } catch (error) {
        return { status: 'error', message: error.message };
    }
});

// =============================================================================
// APP LIFECYCLE
// =============================================================================

app.on('ready', async () => {
    console.log('🎯 GhostLink Local starting...');
    
    // Start Python server first
    await startPythonServer();
    
    // Then create Electron window
    createWindow();
    
    console.log('✨ GhostLink Local is ready!');
});

app.on('window-all-closed', () => {
    stopPythonServer();
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (mainWindow === null) {
        createWindow();
    }
});

app.on('before-quit', () => {
    stopPythonServer();
});

// Handle crashes gracefully
process.on('uncaughtException', (error) => {
    console.error('Uncaught exception:', error);
    stopPythonServer();
});

console.log('📍 GhostLink Local - 100% Local System');
console.log('🔒 No Docker - No APIs - No Cloud');
