import { ChildProcess, spawn } from 'child_process';
import * as vscode from 'vscode';

interface LinkResponse {
    response: string;
    agent: string;
    confidence: number;
    suggestions?: string[];
}

class LinkChatParticipant implements vscode.ChatParticipant {
    private linkProcess: ChildProcess | null = null;
    private pythonPath: string;

    constructor(private context: vscode.ExtensionContext) {
        this.pythonPath = vscode.workspace.getConfiguration('link').get('pythonPath', 'python');
    }

    async handleRequest(
        request: vscode.ChatRequest,
        context: vscode.ChatContext,
        stream: vscode.ChatResponseStream,
        token: vscode.CancellationToken
    ): Promise<void> {
        stream.progress('Thinking...');

        try {
            // Invoke Link agent via Python
            const response = await this.invokeLinkAgent(request.prompt);

            stream.markdown(response.response);

            if (response.suggestions && response.suggestions.length > 0) {
                stream.markdown('\n\n**Suggestions:**');
                response.suggestions.forEach(suggestion => {
                    stream.button({
                        command: 'link.chat',
                        title: suggestion,
                        arguments: [suggestion]
                    });
                });
            }
        } catch (error) {
            stream.markdown(`❌ Error: ${error}`);
        }
    }

    private async invokeLinkAgent(prompt: string): Promise<LinkResponse> {
        return new Promise((resolve, reject) => {
            const pythonScript = `
import asyncio
import sys
import json
sys.path.insert(0, '${vscode.workspace.workspaceFolders?.[0].uri.fsPath.replace(/\\/g, '\\\\')}')
from ghostlink.link_agent import chat_with_link

async def main():
    response = await chat_with_link(${JSON.stringify(prompt)})
    result = {
        "response": response,
        "agent": "Link",
        "confidence": 0.95
    }
    print(json.dumps(result))

asyncio.run(main())
`;

            const proc = spawn(this.pythonPath, ['-c', pythonScript]);
            let output = '';
            let error = '';

            proc.stdout.on('data', (data: Buffer) => {
                output += data.toString();
            });

            proc.stderr.on('data', (data: Buffer) => {
                error += data.toString();
            });

            proc.on('close', (code: number | null) => {
                if (code !== 0) {
                    reject(new Error(`Link agent failed: ${error}`));
                } else {
                    try {
                        const result = JSON.parse(output);
                        resolve(result);
                    } catch (e) {
                        reject(new Error(`Failed to parse Link response: ${output}`));
                    }
                }
            });
        });
    }
}

export function activate(context: vscode.ExtensionContext) {
    console.log('Link Agent extension activated');

    // Register chat participant
    const participant = vscode.chat.createChatParticipant(
        'ghostlink.link',
        async (
            request: vscode.ChatRequest,
            context: vscode.ChatContext,
            stream: vscode.ChatResponseStream,
            token: vscode.CancellationToken
        ) => {
            const handler = new LinkChatParticipant(context);
            return handler.handleRequest(request, context, stream, token);
        });

    participant.iconPath = vscode.Uri.joinPath(context.extensionUri, 'icon.png');

    // Register commands
    context.subscriptions.push(
        vscode.commands.registerCommand('link.chat', async (message?: string) => {
            if (message) {
                vscode.commands.executeCommand('workbench.action.chat.open', {
                    query: `@link ${message}`
                });
            } else {
                vscode.commands.executeCommand('workbench.action.chat.open');
            }
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('link.addTask', async () => {
            const task = await vscode.window.showInputBox({
                prompt: 'Enter task description',
                placeHolder: 'What should Link do?'
            });

            if (task) {
                vscode.commands.executeCommand('workbench.action.chat.open', {
                    query: `@link add task: ${task}`
                });
            }
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('link.showStatus', () => {
            vscode.commands.executeCommand('workbench.action.chat.open', {
                query: '@link status'
            });
        })
    );

    // Auto-start if enabled
    const config = vscode.workspace.getConfiguration('link');
    if (config.get('autoStart')) {
        vscode.window.showInformationMessage('🧠 Link is starting...');
        // Could spawn Link process here
    }
}

export function deactivate() {
    console.log('Link Agent extension deactivated');
}
