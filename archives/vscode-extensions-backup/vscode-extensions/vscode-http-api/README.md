# VSCode HTTP API Extension

This extension exposes a minimal HTTP API that allows external programs to interact with VS Code (open, edit, save files; run commands; optional auto-commit) over a local HTTP port.

## Security

### Built-in Protections

- **Authentication**: Use `vscodeHttpApi.apiKey` setting to secure the API with a secret key.
- **Network isolation**: Keep `vscodeHttpApi.allowRemote` set to `false` to listen only on `127.0.0.1`.
- **Rate limiting**: 100 requests per minute per client (configurable via `vscodeHttpApi.enableRateLimiting`).
- **Input validation**: All paths, commands, and content are validated and sanitized.
- **Workspace scoping**: File operations are restricted to workspace directory (configurable via `vscodeHttpApi.enforceWorkspaceScope`).
- **Size limits**: Request bodies limited to 5MB, headers to 8KB (configurable via `vscodeHttpApi.maxRequestSize`).
- **Security auditing**: All blocked requests, rate limits, and validation errors are logged.
- **Directory traversal protection**: Paths with `..`, system directories, and suspicious patterns are blocked.
- **Shell injection protection**: Commands are validated for dangerous characters.

### Security Endpoints

- `GET /security/events` - View security audit log (requires `masterAutoApprove=true`)
  - Query params: `?type=blocked_request|rate_limit|validation_error|suspicious_activity&since=ISO8601`

### Best Practices

WARNING: The `/exec` and `/extensions/experimental` endpoints can change local system state or extension behavior. Do not enable them without proper network, API key and firewall controls.

Installation (local dev)

```bash
# 1. Install dependencies in the extension folder
cd vscode-extensions/vscode-http-api
npm install

# 2. Build TypeScript
npm run compile

# 3. Open VS Code in the project and press F5 to run a dev instance
# Or create a .vsix package to install in your editor
```

## Configuration

- `vscodeHttpApi.port` - port to listen on (default: 8765)
- `vscodeHttpApi.apiKey` - optional pre-shared key for requests
- `vscodeHttpApi.allowRemote` - allow remote network access (dangerous)
- `vscodeHttpApi.autoCommit` - automatically run git add/commit for workspace after changes
- `vscodeHttpApi.auditMaxContentLength` - Maximum characters to store in the audit for `before`/`after` content. Set to `0` to disable truncation; default `16384`.
- `vscodeHttpApi.auditMaxEntries` - Maximum number of audit entries to keep (default: 1000). Set to 0 to keep all entries.
- `vscodeHttpApi.auditRetentionDays` - Prune entries older than N days. Set to 0 to disable. Combined with max entries the prune operation trims the audit.

API Endpoints

- GET /status
  - Returns JSON with status and workspace path

- POST /open
  - Body: { "path": "/full/path/to/file" }
  - Opens the file in the editor

- POST /edit
  - Body: { "path": "/full/path/to/file", "content": "new file content" }
  - Replaces the entire file content and saves

- POST /save
  - Body: { "path": "/full/path/to/file" }
  - Saves the file

- POST /run
  - Body: { "command": "workbench.action.files.save" }
  - Executes a VS Code command

- POST /commit
  - Body: { "message": "commit message" }
  - Attempts to use `ai_bots/git_auto_commit.py` inside the workspace if present. Falls back to `git` CLI if necessary. Commits are recorded in the audit log.

- POST /exec
  - Body: { "command": "ls", "args": ["-la"] }
  - Execute a shell command inside the workspace root. Requires `vscodeHttpApi.allowExec=true` and (optionally) `vscodeHttpApi.execWhitelist`.

- GET /extensions
  - Lists installed extensions (IDs, displayName, version and contributed config)

- POST /extensions/experimental
  - Body: { "enable": true, "extensions": ["publisher.extension"] }
  - Toggles extension-contributed settings that are marked as `experimental`, `beta`, `preview`, or `proposed` (preview by default; send { apply: true } to apply changes)

Additional file-related endpoints

- GET /read?path=/full/path/to/file
  - Returns JSON { content: string }

- GET /list?path=/path/to/dir
  - Lists files in a directory (basic non-recursive listing)

- POST /create
  - Body: { "path": "/path/to/file", "content": "..." }

- POST /delete
  - Body: { "path": "/path/to/file" }

Settings and convenience

- POST /settings
  - Body: { "some.setting.key": value }
  - Updates user-level VS Code settings (ConfigurationTarget.Global). Use `{ "apply": true }` in the body to apply changes; otherwise the API returns a preview of the changes.

- GET /audit
  - Returns the last N audit entries written by the extension (JSON lines). Query params:
    - `?limit=<n>` - return up to n entries (default 200)
    - `?id=<audit-id>` - return a single audit entry by id

  - GET /audit/stats
    - Returns JSON with { count, size, latest } representing number of audit entries, file size in bytes, and latest timestamp

- POST /rollback
  - Body: { id: "audit-id" }
  - Reverts changes from a single audit entry (settings + file create/delete/edit rollback). Each audit entry includes previous values where possible to support recovery. The rollback endpoint requires `vscodeHttpApi.masterAutoApprove=true` to be set in settings.json to enable; use with extreme caution.

## Examples

- Use the Node script in `examples/client_node.js` for quick tests; place your API key in `VSCODE_HTTP_API_KEY` env var.
- Use `scripts/enable-experimental.sh <API_KEY>` to bulk enable experimental flags for installed extensions (make sure F5 dev instance is on and extension running).
- You can also use the Node CLI:
  - `node examples/client_node.js experimental true` — enable experimental for all installed extensions
  - `node examples/client_node.js experimental false '["publisher.extension"]'` — disable for specified extension(s)
- The `examples/audit_tool.js` helper script provides shortcuts for audit actions:
  - `node examples/audit_tool.js list 100` — fetch last 100 audit entries
  - `node examples/audit_tool.js get <id>` — fetch a single audit entry by id
  - `node examples/audit_tool.js prune` — trigger a prune using the extension settings (requires `vscodeHttpApi.masterAutoApprove=true`)

### UI & Commands

- Tree view: "VSCode HTTP API Audit Log" in the Explorer shows recent audit entries (requires the extension running).
  - Icons indicate entry type (file, settings, commit, exec, yolo/experimental, rollback).
  - Click any entry to view JSON details.
  - Right-click for context menu options (show details, rollback).
- Command palette commands:
  - "VSCode HTTP API: Show Audit Log" — a quick pick UI for browsing and rolling back entries
  - "VSCode HTTP API: Refresh Audit Log" — refresh the TreeView
  - "VSCode HTTP API: Show Audit Details" — show a JSON view of an audit entry
  - "VSCode HTTP API: Rollback Audit Entry" — attempt a rollback via the local Post /rollback endpoint (requires `masterAutoApprove` config and running extension)
  - Rollbacks show a preview with file diffs and ask for confirmation before attempting to revert changes.
  - "VSCode HTTP API: Prune Audit Log" — manually trigger audit pruning (removes old entries based on `auditMaxEntries` and `auditRetentionDays`).
- Scheduled pruning: If `auditMaxEntries` or `auditRetentionDays` are configured, the extension automatically prunes the audit log hourly.
- Use the built-in Command Palette UI 'VSCode HTTP API: Show Audit Log' to browse recent audit entries, inspect details, and trigger rollbacks (rollbacks require `vscodeHttpApi.masterAutoApprove=true`). This provides a quick way to review recent actions taken by the HTTP API and revert changes from within VS Code.
- Toggle YOLO / master auto-approval for installed extensions and settings (very dangerous):
  - `node examples/client_node.js yolo true` — enable YOLO mode for all installed extensions
  - `node examples/client_node.js master true` — alias command to enable 'master auto-approve' across extensions/settings
  - `python3 scripts/enable-yolo-offline.py --enable true --dry-run` — dry-run offline script, then run without `--dry-run` to apply

Example Request

```bash
curl -X POST http://127.0.0.1:8765/edit \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: YOUR_KEY' \
  -d '{ "path": "/home/user/project/README.md", "content": "New content" }'
```

Enable all experimental flags for installed extensions (use with caution):

```bash
curl -X POST http://127.0.0.1:8765/extensions/experimental \
  -H 'Content-Type: application/json' \
  -H 'x-api-key: YOUR_KEY' \
  -d '{ "enable": true }'
```

## Notes

- This extension is intended for local automation and experimentation. Do not expose it publicly without secure network + auth measures.

- For production / multi-user setups, consider `code-server` or remote IDE instances with explicit RBAC and web gateways.
