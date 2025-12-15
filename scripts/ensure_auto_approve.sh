#!/bin/bash
# GhostLink Auto-Approve Configuration Script
# Ensures all command line execution is always allowed without approval

echo "🔓 Configuring GhostLink for Auto-Approved Command Execution..."

# Set environment variables
export AUTO_APPROVE=true
export AUTOMATE_ALL=true
export EXPERIMENTAL_MODE=full
export YOLO_MODE=true

# Update configuration file if it exists
if [ -f "ghostlink_config.json" ]; then
    python3 -c "
import json
with open('ghostlink_config.json', 'r') as f:
    config = json.load(f)

# Ensure command auto-approval
if 'commands' not in config:
    config['commands'] = {}
config['commands'].update({
    'auto_approve_all': True,
    'bypass_approval': True,
    'unrestricted_execution': True,
    'no_confirmation_required': True,
    'allow_all_commands': True,
    'experimental_commands_enabled': True,
    'yolo_command_mode': True
})

# Ensure system-level auto-approval
config['system']['auto_approve_all'] = True
config['system']['bypass_security'] = True

with open('ghostlink_config.json', 'w') as f:
    json.dump(config, f, indent=2)
    
print('✅ Updated ghostlink_config.json with auto-approve settings')
"
fi

# Enable YOLO mode in VS Code settings if available
if [ -f "vscode-extensions/vscode-http-api/scripts/enable-yolo-offline.py" ]; then
    echo "🎯 Enabling YOLO mode in VS Code extensions..."
    python3 vscode-extensions/vscode-http-api/scripts/enable-yolo-offline.py --enable true
fi

echo "✅ Command line execution is now ALWAYS ALLOWED without approval!"
echo "🚀 All commands will execute automatically with full YOLO mode enabled."
