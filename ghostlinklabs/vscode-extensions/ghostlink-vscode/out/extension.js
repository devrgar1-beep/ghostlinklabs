"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.deactivate = exports.activate = void 0;
const vscode = __importStar(require("vscode"));
const path = __importStar(require("path"));
const child_process = __importStar(require("child_process"));
function activate(context) {
    console.log('GhostLink AI Integration extension is now active!');
    // Get configuration
    const config = vscode.workspace.getConfiguration('ghostlink');
    const pythonPath = config.get('pythonPath', 'python3');
    const projectRoot = config.get('projectRoot', '') || getProjectRoot();
    const vscodeApiUrl = config.get('vscodeApiUrl', 'http://localhost:3000');
    // Register commands
    context.subscriptions.push(vscode.commands.registerCommand('ghostlink.health', async () => {
        await executeGhostCommand('health', pythonPath, projectRoot, vscodeApiUrl);
    }));
    context.subscriptions.push(vscode.commands.registerCommand('ghostlink.task', async () => {
        const taskType = await vscode.window.showQuickPick([
            'consciousness',
            'multiagent',
            'monitoring',
            'deployment',
            'custom'
        ], { placeHolder: 'Select AI task type' });
        if (taskType) {
            if (taskType === 'custom') {
                const customTask = await vscode.window.showInputBox({
                    prompt: 'Enter custom task type',
                    placeHolder: 'e.g., analysis, optimization, learning'
                });
                if (customTask) {
                    await executeGhostCommand(`task --task-type=${customTask}`, pythonPath, projectRoot, vscodeApiUrl);
                }
            }
            else {
                await executeGhostCommand(`task --task-type=${taskType}`, pythonPath, projectRoot, vscodeApiUrl);
            }
        }
    }));
    context.subscriptions.push(vscode.commands.registerCommand('ghostlink.status', async () => {
        await executeGhostCommand('status', pythonPath, projectRoot, vscodeApiUrl);
    }));
    context.subscriptions.push(vscode.commands.registerCommand('ghostlink.consciousness', async () => {
        await executeGhostCommand('consciousness', pythonPath, projectRoot, vscodeApiUrl);
    }));
    context.subscriptions.push(vscode.commands.registerCommand('ghostlink.multiagent', async () => {
        await executeGhostCommand('component multi_agent', pythonPath, projectRoot, vscodeApiUrl);
    }));
    context.subscriptions.push(vscode.commands.registerCommand('ghostlink.deploy', async () => {
        const environment = await vscode.window.showQuickPick([
            'development',
            'staging',
            'production'
        ], { placeHolder: 'Select deployment environment' });
        if (environment) {
            const component = await vscode.window.showQuickPick([
                'core',
                'infrastructure',
                'monitoring',
                'all'
            ], { placeHolder: 'Select component to deploy' });
            if (component) {
                await executeDeployCommand(environment, component, projectRoot);
            }
        }
    }));
}
exports.activate = activate;
async function executeGhostCommand(command, pythonPath, projectRoot, vscodeApiUrl) {
    try {
        // Show progress
        await vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: `GhostLink: Executing ${command}`,
            cancellable: false
        }, async (progress) => {
            progress.report({ increment: 0, message: 'Starting...' });
            // Execute the ghost_vscode_integration.py script
            const scriptPath = path.join(projectRoot, 'ghost_vscode_integration.py');
            const fullCommand = `${pythonPath} "${scriptPath}" ${command}`;
            progress.report({ increment: 25, message: 'Running command...' });
            const result = await executeCommand(fullCommand, projectRoot);
            progress.report({ increment: 75, message: 'Processing results...' });
            // Try to parse JSON output
            try {
                const output = JSON.parse(result.stdout);
                await displayResults(output, command);
            }
            catch {
                // If not JSON, display as text
                await displayTextResult(result.stdout, command);
            }
            progress.report({ increment: 100, message: 'Complete' });
        });
    }
    catch (error) {
        vscode.window.showErrorMessage(`GhostLink command failed: ${error}`);
    }
}
async function executeDeployCommand(environment, component, projectRoot) {
    try {
        await vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: `GhostLink: Deploying ${component} to ${environment}`,
            cancellable: false
        }, async (progress) => {
            progress.report({ increment: 0, message: 'Starting deployment...' });
            const deployScript = path.join(projectRoot, 'deploy', 'deploy.sh');
            const command = `"${deployScript}" ${environment} ${component}`;
            progress.report({ increment: 25, message: 'Running deployment...' });
            const result = await executeCommand(command, projectRoot);
            progress.report({ increment: 75, message: 'Verifying deployment...' });
            if (result.code === 0) {
                vscode.window.showInformationMessage(`GhostLink deployment successful: ${component} to ${environment}`);
                await displayTextResult(result.stdout, `deploy-${environment}-${component}`);
            }
            else {
                vscode.window.showErrorMessage(`GhostLink deployment failed: ${result.stderr}`);
            }
            progress.report({ increment: 100, message: 'Complete' });
        });
    }
    catch (error) {
        vscode.window.showErrorMessage(`GhostLink deployment failed: ${error}`);
    }
}
async function executeCommand(command, cwd) {
    return new Promise((resolve, reject) => {
        child_process.exec(command, { cwd }, (error, stdout, stderr) => {
            if (error) {
                resolve({ code: error.code || 1, stdout, stderr });
            }
            else {
                resolve({ code: 0, stdout, stderr });
            }
        });
    });
}
async function displayResults(data, command) {
    // Create output channel
    const channel = vscode.window.createOutputChannel(`GhostLink: ${command}`);
    channel.show();
    // Format and display results
    if (typeof data === 'object') {
        channel.appendLine(JSON.stringify(data, null, 2));
    }
    else {
        channel.appendLine(String(data));
    }
    // Show summary in notification
    if (data.success !== undefined) {
        if (data.success) {
            vscode.window.showInformationMessage(`GhostLink ${command}: Success`);
        }
        else {
            vscode.window.showErrorMessage(`GhostLink ${command}: Failed - ${data.error || 'Unknown error'}`);
        }
    }
}
async function displayTextResult(text, title) {
    const channel = vscode.window.createOutputChannel(`GhostLink: ${title}`);
    channel.show();
    channel.appendLine(text);
}
function getProjectRoot() {
    const workspaceFolders = vscode.workspace.workspaceFolders;
    if (workspaceFolders && workspaceFolders.length > 0) {
        return workspaceFolders[0].uri.fsPath;
    }
    return process.cwd();
}
function deactivate() {
    console.log('GhostLink AI Integration extension deactivated');
}
exports.deactivate = deactivate;
//# sourceMappingURL=extension.js.map