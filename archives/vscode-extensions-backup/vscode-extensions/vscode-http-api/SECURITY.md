# Security Guidance

This extension runs an HTTP server inside the VS Code extension host which exposes editor control commands. This is powerful but can be dangerous if not secured correctly.

Recommendations

- Use `vscodeHttpApi.apiKey` to set a strong, random API key and require it in all requests.
- Keep `vscodeHttpApi.allowRemote` set to `false` so the extension listens on `127.0.0.1` only.
- If `allowRemote` is needed, run behind a vetted reverse-proxy with TLS and IP filtering (nginx, traefik). Do not enable it without firewall rules.
- Keep VS Code up to date and review extension permissions for anything you install.
- Use the extension only on trusted systems and networks.

Audit
- The extension intentionally exposes only a small set of endpoints. If you require more, add them in code and review the implementation for security implications before enabling.

Server Hardening
- Consider OS-level firewall rules (pfctl on macOS, ufw/iptables on Linux) to restrict access.
- Run the extension in a development environment if exploring experimental APIs.
