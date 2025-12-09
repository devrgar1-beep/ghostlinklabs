# GhostLink VS Code Extension

A VS Code extension that integrates the GhostLink AI system with your development environment, providing real-time AI assistance and system control through the Ghost agent.

## Features

- **System Health Monitoring**: Check the status of the GhostLink AI system
- **AI Task Execution**: Run various AI tasks through the Ghost agent
- **Consciousness Analysis**: Analyze the AI consciousness framework
- **Multi-Agent Status**: Monitor the multi-agent orchestration system
- **Infrastructure Deployment**: Deploy GhostLink components to different environments
- **Real-time Integration**: Seamless communication between VS Code and the AI brain

## Prerequisites

1. **GhostLink AI System**: The complete GhostLink AI ecosystem must be installed and running
2. **VS Code HTTP API Extension**: Install the companion `vscode-http-api` extension for programmatic control
3. **Python 3.9+**: Required for the GhostLink integration script

## Installation

1. Clone or download the GhostLink project
2. Navigate to `vscode-extensions/ghostlink-vscode/`
3. Run `npm install` to install dependencies
4. Run `npm run compile` to build the extension
5. Install the extension in VS Code:
   - Open VS Code
   - Go to Extensions (Ctrl+Shift+X)
   - Click the "..." menu and select "Install from VS Code"
   - Select the `vscode-extensions/ghostlink-vscode/` directory

## Configuration

Configure the extension through VS Code settings:

```json
{
  "ghostlink.pythonPath": "python3",
  "ghostlink.projectRoot": "/path/to/ghostlink/project",
  "ghostlink.vscodeApiUrl": "http://localhost:3000"
}
```

## Usage

### Command Palette Commands

Access GhostLink commands through the VS Code Command Palette (Ctrl+Shift+P):

- **GhostLink: Show System Health** - Display comprehensive system status
- **GhostLink: Execute AI Task** - Run AI tasks (consciousness, multi-agent, monitoring, etc.)
- **GhostLink: System Status** - Quick system status check
- **GhostLink: Consciousness Analysis** - Analyze AI consciousness
- **GhostLink: Multi-Agent Status** - Check multi-agent system status
- **GhostLink: Deploy Infrastructure** - Deploy components to environments

### Integration with VS Code HTTP API

The extension integrates with the VS Code HTTP API extension to provide:

- File editing and management
- Terminal command execution
- Git operations
- Real-time feedback in the editor

## Architecture

```
VS Code Extension (ghostlink-vscode)
    ↓
Ghost VS Code Integration (ghost_vscode_integration.py)
    ↓
Ghost Agent Orchestrator (ghost_agent_orchestrator.py)
    ↓
GhostLink AI Brain (cold_boot_orchestrator.py + components)
```

## Development

### Building the Extension

```bash
cd vscode-extensions/ghostlink-vscode
npm install
npm run compile
```

### Testing

```bash
npm run test
```

### Debugging

1. Open the extension directory in VS Code
2. Press F5 to launch extension development host
3. Test commands in the new window

## Troubleshooting

### Common Issues

1. **"GhostLink system not found"**
   - Ensure the GhostLink project is properly installed
   - Check the `ghostlink.projectRoot` setting points to the correct directory

2. **"VS Code API not available"**
   - Install and start the `vscode-http-api` extension
   - Run "VSCode HTTP API: Start" from the command palette

3. **Python path issues**
   - Verify Python 3.9+ is installed
   - Update the `ghostlink.pythonPath` setting if needed

### Logs

Check the VS Code output panel for "GhostLink" channels to see detailed logs and error messages.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This extension is part of the GhostLink AI system. See the main project license for details.
