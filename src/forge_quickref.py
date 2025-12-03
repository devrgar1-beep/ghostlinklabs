"""
GhostLink Toolbox Forge - Quick Reference
==========================================

SYSTEM COMMANDS:
  forge status          - System status overview
  forge health          - Health diagnostics
  forge audit           - Full system audit
  forge audit [path]    - Audit specific path

SERVER COMMANDS:
  forge start-server    - Start FastAPI (port 8001)
  forge stop-server     - Stop all servers

HARDWARE COMMANDS:
  forge void            - Void activation (admin)
  forge bios-bridge     - BIOS/hardware bridge

LINK COMMANDS:
  forge link-start      - Start orchestrator
  forge link-stop       - Stop orchestrator  
  forge link-status     - Link status

GIT COMMANDS:
  forge git-status      - Git status
  forge git-pull        - Pull changes
  forge git-sync        - Full sync

BUILD COMMANDS:
  forge build           - Build all components
  forge clean           - Clean artifacts

DEV COMMANDS:
  forge test            - Run tests
  forge lint            - Run linters
  forge format          - Format code

UTILITY COMMANDS:
  forge shell           - Enable shell integration
  forge history         - Show action history
  forge info            - Toolbox information
  forge                 - Interactive mode

SHORTCUTS:
  gl, link, ghost       - Link CLI
  void                  - Void activation
  gl-start, gl-stop     - Quick Link control
  gl-status, gl-health  - Quick diagnostics
  gl-server             - Quick server start
  gl-bios, gl-void      - Quick hardware access

INTERACTIVE MODE:
  Run 'forge' without arguments for interactive prompt
  Type 'help' for commands, 'exit' to quit
"""

def print_quickref():
    """Print quick reference"""
    print(__doc__)

if __name__ == "__main__":
    print_quickref()
