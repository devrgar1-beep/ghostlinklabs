# Running the Editor as an API

This repository includes a minimal VS Code extension (`vscode-extensions/vscode-http-api`) that exposes an HTTP API to interact with the editor and files. This is useful if you want to treat the editor instance as a programmatic tool.

## How it works
- The extension starts a small HTTP server inside the VS Code extension host.
- External clients can send requests to open/edit/save files, run editor commands, and trigger auto-commit behaviors.
- The extension respects `vscodeHttpApi.apiKey` and `vscodeHttpApi.allowRemote` settings.

## Ideal Uses
- Headless automation during CI or remote development with `code-server`.
- Integration with other tooling (scripts, CI jobs) that needs to modify or analyze workspace files.
- Experiments that require an intelligent editor with extensions for code completion, linting, and more.

## Caveats
- This is powerful but offers shell-level access to the editor workspace. Use only on trusted systems and with the recommended security settings.
 - The extension also provides `/exec` for running shell commands and `/extensions/experimental` for toggling extension experimental flags. These endpoints have powerful side effects. Use them only with strong authentication, allowlist configuration, and only on trusted machines.
- Not all VS Code features are supported via the extension API; some UI or OS-level interactions may not be available.

## Alternatives
- Use `code-server` for web-based editing that integrates with existing authentication and proxy setups.
- Use the Language Server Protocol (LSP) for language-specific features without running an editor host.
- Fork & customize VS Code if you need deeper runtime changes (heavy weight, not recommended unless required).

## Example usage
See `vscode-extensions/vscode-http-api/examples/client.py` for a minimal Python client that demonstrates the API endpoints.
