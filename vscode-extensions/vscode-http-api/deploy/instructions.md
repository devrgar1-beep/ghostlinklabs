# Deploying the VSCode HTTP API Extension

This guide covers running the extension in different environments and how to expose the editor as an API safely.

## Local Development (Dev instance)

1. Install dependencies: `npm install` in the extension folder.
2. Build: `npm run compile`.
3. Open the extension folder in VS Code and press `F5` to run a new Extension Development Host with the extension loaded.

## Running in `code-server` (Remote Web VS Code)

1. Use `code-server` or `coder` and install this extension into the remote environment.
2. Configure `vscodeHttpApi.allowRemote: true` only if you have proper firewall and TLS.
3. Configure your reverse proxy to forward only expected routes and require authentication.

## Running on Linux Remote Host

1. Install `code-server` and set up a non-root account for running the server.
2. Add firewall rules (ufw/iptables) to restrict access to your management endpoints.
3. Use systemd to manage `code-server` or developer workflows.

### Example Systemd service for code-server (Ubuntu)

```
[Unit]
Description=code-server
After=network.target

[Service]
User=youruser
Environment=PASSWORD=yourpassword
ExecStart=/usr/bin/code-server --bind-addr 127.0.0.1:8080 --auth password --extensions-dir /path/to/extensions
Restart=always

[Install]
WantedBy=multi-user.target
```

## Recommendations

- Do not expose `vscodeHttpApi` to public internet without proper authentication, IP whitelisting and TLS.
- Consider using a gateway like OAuth2 Proxy + NGINX to front the code-server instance.
- Keep back-ups and snapshots before running experimentation in production.
