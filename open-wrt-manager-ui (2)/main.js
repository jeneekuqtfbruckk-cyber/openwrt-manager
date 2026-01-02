const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const http = require('http');

let mainWindow;
let pythonProcess;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        titleBarStyle: 'hidden', // macOS style traffic lights
        title: "OpenWrt Manager",
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
        },
        frame: false, // Frameless
        transparent: true, // Enable transparency for rounded corners
        backgroundColor: '#00000000', // Fully transparent background
    });

    // Window Control IPC
    const { ipcMain } = require('electron');
    ipcMain.on('window-min', () => mainWindow.minimize());
    ipcMain.on('window-max', () => {
        if (mainWindow.isMaximized()) {
            mainWindow.unmaximize();
        } else {
            mainWindow.maximize();
        }
    });
    ipcMain.on('window-close', () => mainWindow.close());

    // Load Next.js dev server or static build
    if (app.isPackaged) {
        mainWindow.loadFile(path.join(__dirname, 'out', 'index.html'));
    } else {
        const startUrl = process.env.ELECTRON_START_URL || 'http://localhost:3000';
        setTimeout(() => {
            mainWindow.loadURL(startUrl);
        }, 1000);
    }

    mainWindow.on('closed', function () {
        mainWindow = null;
    });
}

function startBackend() {
    // Spawn Python FastAPI Backend
    let cmd;
    let args;
    let cwd;

    if (app.isPackaged) {
        // In release, backend.exe is placed in resources/ (by electron-builder extraResources)
        const exePath = path.join(process.resourcesPath, 'backend.exe');
        console.log('Spawning Packaged Backend:', exePath);
        cmd = exePath;
        args = [];
        // Optional: set cwd to resources path or let it be default
        cwd = process.resourcesPath;
    } else {
        // In dev, use the batch file
        const batchPath = path.join(__dirname, '..', 'backend', 'run_server.bat');
        console.log('Spawning Backend via Batch:', batchPath);
        cmd = 'cmd.exe';
        args = ['/c', batchPath];
        cwd = path.join(__dirname, '..', 'backend');
    }

    pythonProcess = spawn(cmd, args, {
        cwd: cwd,
        stdio: 'inherit',
        shell: false,
        env: process.env
    });

    // pythonProcess.stderr is null because of stdio: 'inherit'
    // Errors will appear directly in the console
}

// App Lifecycle
app.disableHardwareAcceleration(); // Fix for GPU crashes on some Windows systems
app.on('ready', () => {
    startBackend();
    createWindow();
});

app.on('window-all-closed', function () {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', function () {
    if (mainWindow === null) {
        createWindow();
    }
});

app.on('will-quit', () => {
    // Kill Python subprocess
    if (pythonProcess) {
        pythonProcess.kill();
    }
});
