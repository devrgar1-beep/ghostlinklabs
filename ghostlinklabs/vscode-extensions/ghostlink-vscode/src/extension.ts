import * as vscode from 'vscode';
import * as path from 'path';
import * as child_process from 'child_process';
import axios from 'axios';

export function activate(context: vscode.ExtensionContext) {
    console.log('GhostLink AI Integration extension is now active!');

    // Get configuration
    const config = vscode.workspace.getConfiguration('ghostlink');
    const pythonPath = config.get<string>('pythonPath', 'python3');
    const projectRoot = config.get<string>('projectRoot', '') || getProjectRoot();
    const vscodeApiUrl = config.get<string>('vscodeApiUrl', 'http://localhost:3000');

    // Register commands
    context.subscriptions.push(
        vscode.commands.registerCommand('ghostlink.health', async () => {
            await executeGhostCommand('health', pythonPath, projectRoot, vscodeApiUrl);
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('ghostlink.task', async () => {
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
                } else {
                    await executeGhostCommand(`task --task-type=${taskType}`, pythonPath, projectRoot, vscodeApiUrl);
                }
            }
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('ghostlink.status', async () => {
            await executeGhostCommand('status', pythonPath, projectRoot, vscodeApiUrl);
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('ghostlink.consciousness', async () => {
            await executeGhostCommand('consciousness', pythonPath, projectRoot, vscodeApiUrl);
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('ghostlink.multiagent', async () => {
            await executeGhostCommand('component multi_agent', pythonPath, projectRoot, vscodeApiUrl);
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('ghostlink.deploy', async () => {
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
        })
    );
}

async function executeGhostCommand(command: string, pythonPath: string, projectRoot: string, vscodeApiUrl: string) {
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
            } catch {
                // If not JSON, display as text
                await displayTextResult(result.stdout, command);
            }

            progress.report({ increment: 100, message: 'Complete' });
        });
    } catch (error) {
        vscode.window.showErrorMessage(`GhostLink command failed: ${error}`);
    }
}

async function executeDeployCommand(environment: string, component: string, projectRoot: string) {
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
            } else {
                vscode.window.showErrorMessage(`GhostLink deployment failed: ${result.stderr}`);
            }

            progress.report({ increment: 100, message: 'Complete' });
        });
    } catch (error) {
        vscode.window.showErrorMessage(`GhostLink deployment failed: ${error}`);
    }
}

async function executeCommand(command: string, cwd: string): Promise<{ code: number, stdout: string, stderr: string }> {
    return new Promise((resolve, reject) => {
        child_process.exec(command, { cwd }, (error, stdout, stderr) => {
            if (error) {
                resolve({ code: error.code || 1, stdout, stderr });
            } else {
                resolve({ code: 0, stdout, stderr });
            }
        });
    });
}

async function displayResults(data: any, command: string) {
    // Create output channel
    const channel = vscode.window.createOutputChannel(`GhostLink: ${command}`);
    channel.show();

    // Format and display results
    if (typeof data === 'object') {
        channel.appendLine(JSON.stringify(data, null, 2));
    } else {
        channel.appendLine(String(data));
    }

    // Show summary in notification
    if (data.success !== undefined) {
        if (data.success) {
            vscode.window.showInformationMessage(`GhostLink ${command}: Success`);
        } else {
            vscode.window.showErrorMessage(`GhostLink ${command}: Failed - ${data.error || 'Unknown error'}`);
        }
    }
}

async function displayTextResult(text: string, title: string) {
    const channel = vscode.window.createOutputChannel(`GhostLink: ${title}`);
    channel.show();
    channel.appendLine(text);
}

function getProjectRoot(): string {
    const workspaceFolders = vscode.workspace.workspaceFolders;
    if (workspaceFolders && workspaceFolders.length > 0) {
        return workspaceFolders[0].uri.fsPath;
    }
    return process.cwd();
}

export function deactivate() {
    console.log('GhostLink AI Integration extension deactivated');
}
