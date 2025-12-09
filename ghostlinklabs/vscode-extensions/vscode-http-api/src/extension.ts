import * as vscode from 'vscode';
import * as http from 'http';
import * as url from 'url';
import * as fs from 'fs';
import * as pathModule from 'path';
import { exec, spawn } from 'child_process';
import * as crypto from 'crypto';
import { truncateContent, pruneAuditEntries, applyTruncateToEntry } from './audit_utils';
import { registerAuditUI } from './audit_ui';
import { AuditTreeProvider } from './audit_tree';
import { SecurityValidator, RateLimiter, RequestSizeValidator, SecurityAuditor } from './security';

let server: http.Server | null = null;

function parseJSON(req: http.IncomingMessage): Promise<any> {
  return new Promise((resolve, reject) => {
    let body = '';
    let size = 0;
    const maxSize = 5 * 1024 * 1024; // 5MB
    
    req.on('data', (chunk) => {
      size += chunk.length;
      if (size > maxSize) {
        req.destroy();
        reject(new Error('Request body too large'));
        return;
      }
      body += chunk;
    });
    
    req.on('end', () => {
      try {
        resolve(body ? JSON.parse(body) : {});
      } catch (err) {
        reject(new Error('Invalid JSON'));
      }
    });
    
    req.on('error', (err) => reject(err));
  });
}

async function authenticate(req: http.IncomingMessage | undefined): Promise<boolean> {
  const cfg = vscode.workspace.getConfiguration('vscodeHttpApi');
  const apiKey = cfg.get<string>('apiKey', '');
  if (!apiKey) return true; // No auth required

  const headerKey = ((req?.headers['x-api-key'] as string) || '').toString();
  const authHeader = (req?.headers['authorization'] || '').toString();
  if (headerKey && headerKey === apiKey) return true;
  if (authHeader && authHeader.startsWith('Bearer ')) {
    return authHeader.slice(7) === apiKey;
  }
  return false;
}

function ok(res: http.ServerResponse, body: any = { ok: true }) {
  res.setHeader('content-type', 'application/json');
  res.writeHead(200);
  res.end(JSON.stringify(body));
}

function err(res: http.ServerResponse, status: number, message: string) {
  res.setHeader('content-type', 'application/json');
  res.writeHead(status);
  res.end(JSON.stringify({ ok: false, error: message }));
}

async function commitIfEnabled(workspacePath: string, message = 'Auto commit') {
  const cfg = vscode.workspace.getConfiguration('vscodeHttpApi');
  const autoCommit = cfg.get<boolean>('autoCommit', true);
  if (!autoCommit) return;

  // Try to run git add -A && git commit -m
  const cmd = `git -C "${workspacePath}" add -A && git -C "${workspacePath}" commit -m "${message.replace(/\"/g, '\\"')}"`;
  exec(cmd, (error, stdout, stderr) => {
    if (error) {
      if ((globalThis as any).console && typeof (globalThis as any).console.warn === 'function') (globalThis as any).console.warn('Auto-commit failed:', stderr || error.message);
    } else {
      if ((globalThis as any).console && typeof (globalThis as any).console.log === 'function') (globalThis as any).console.log('Auto-commit:', stdout);
    }
  });
}

async function runPythonIfPresent(workspacePath: string, snippet: string): Promise<{ success: boolean; out?: string; err?: string }> {
  // Run a python snippet within the workspace root to use local modules like ai_bots.git_auto_commit
  // This is best effort: the user's Python environment must be on PATH and workspace should have python files
  return new Promise((resolve) => {
    // Create a temp file to run
    const tmpPath = pathModule.join(workspacePath || '.', '.vscode_http_api_tmp.py');
    const content = snippet;
    try {
      fs.writeFileSync(tmpPath, content, { encoding: 'utf8' });
    } catch (e) {
      return resolve({ success: false, err: String(e) });
    }
    // Attempt to find a Python in a workspace virtualenv (venv/.venv/env)
    const candidates = [
      pathModule.join(workspacePath || '.', '.venv', 'bin', 'python'),
      pathModule.join(workspacePath || '.', 'venv', 'bin', 'python'),
      pathModule.join(workspacePath || '.', 'env', 'bin', 'python'),
      'python3',
      'python'
    ];
    let py: string | undefined;
    for (const c of candidates) {
      try {
        if (c === 'python3' || c === 'python') { py = c; break; }
        if (fs.existsSync(c)) { py = c; break; }
      } catch (e) {}
    }
    if (!py) py = 'python3';
    const child = spawn(py, [tmpPath], { cwd: workspacePath || undefined, env: { ...(typeof (globalThis as any).process !== 'undefined' ? (globalThis as any).process.env : {}), PYTHONPATH: workspacePath || '' } });
    let out = '';
    let err = '';
    child.stdout.on('data', (c) => (out += c.toString()));
    child.stderr.on('data', (c) => (err += c.toString()));
    child.on('close', (code) => {
      try { fs.unlinkSync(tmpPath); } catch (e) {}
      resolve({ success: code === 0, out, err });
    });
  });
}

export function activate(context: vscode.ExtensionContext) {
  if ((globalThis as any).console && typeof (globalThis as any).console.log === 'function') (globalThis as any).console.log('vscode-http-api activating...');

  const startCommand = vscode.commands.registerCommand('vscodeHttpApi.start', () => {
    if (server) {
      vscode.window.showInformationMessage('VSCode HTTP API already running.');
      return;
    }

    const cfg = vscode.workspace.getConfiguration('vscodeHttpApi');
    const port = cfg.get<number>('port', 8765);
    const allowRemote = cfg.get<boolean>('allowRemote', false);

    // Initialize security components
    const rateLimiter = new RateLimiter(60000, 100); // 100 requests per minute
    const securityAuditor = new SecurityAuditor();
    const cleanupInterval = (globalThis as any).setInterval(() => rateLimiter.cleanup(), 300000); // Cleanup every 5 min
    context.subscriptions.push({ dispose: () => (globalThis as any).clearInterval(cleanupInterval) });

    // helper: append audit JSON entries to a file in the extension's global storage
    const auditPath = context.globalStorageUri ? pathModule.join(context.globalStorageUri.fsPath, 'audit_log.jsonl') : pathModule.join(context.globalStoragePath || '.', 'audit_log.jsonl');
    function ensureAuditDir() {
      try { fs.mkdirSync(pathModule.dirname(auditPath), { recursive: true }); } catch (e) {}
    }
    function genId() { return crypto.randomBytes(8).toString('hex'); }
    function truncateContentIfNeeded(content: string | null) {
      try {
        const cfg = vscode.workspace.getConfiguration('vscodeHttpApi');
        const maxLen = cfg.get<number>('auditMaxContentLength', 16384);
        return truncateContent(content as any, maxLen);
      } catch (e) { return content; }
    }

    function appendAudit(entry: any) {
      try {
        ensureAuditDir();
        // Build the audit entry (id + timestamp)
        const full = Object.assign({ id: genId(), ts: new Date().toISOString() }, entry);
        // Ensure very large file contents aren't stored in the audit log
        try { const cfg = vscode.workspace.getConfiguration('vscodeHttpApi'); const maxLen = cfg.get<number>('auditMaxContentLength', 16384); Object.assign(full, applyTruncateToEntry(full, maxLen)); } catch (e) {}
        fs.appendFileSync(auditPath, JSON.stringify(full) + '\n', { encoding: 'utf8' });
        // After writing, prune the audit file according to retention rules
        try { pruneAuditFile(); } catch (e) { /* non-fatal */ }
        return full;
      } catch (e) {
        if ((globalThis as any).console && typeof (globalThis as any).console.warn === 'function') (globalThis as any).console.warn('Failed to append audit', e);
        return null;
      }
    }
    async function readAudit(limit = 200) {
      try {
        if (!fs.existsSync(auditPath)) return [];
        const lines = fs.readFileSync(auditPath, 'utf8').split('\n').filter(Boolean);
        const out = lines.map((l) => { try { return JSON.parse(l); } catch (e) { return { raw: l }; } });
        return out.slice(-limit);
      } catch (e) { return []; }
    }

    // Prune audit file: keep at most auditMaxEntries and optionally prune older than N days
    function pruneAuditFile() {
      try {
        const cfg = vscode.workspace.getConfiguration('vscodeHttpApi');
        const maxEntries = cfg.get<number>('auditMaxEntries', 1000);
        const retainDays = cfg.get<number>('auditRetentionDays', 0);
        if (maxEntries === 0 && (!retainDays || retainDays === 0)) return; // nothing to do
        if (!fs.existsSync(auditPath)) return;
        const lines = fs.readFileSync(auditPath, 'utf8').split('\n').filter(Boolean);
        let entries = lines.map((l) => { try { return JSON.parse(l); } catch (e) { return null; } }).filter(Boolean);
        const nowTs = Date.now();
        entries = pruneAuditEntries(entries, maxEntries, retainDays);
        // write back
        try { ensureAuditDir(); fs.writeFileSync(auditPath, entries.map((e) => JSON.stringify(e)).join('\n') + (entries.length ? '\n' : ''), { encoding: 'utf8' }); } catch (e) {}
      } catch (e) {}
    }

    server = http.createServer(async (req, res) => {
      try {
        // Rate limiting check
        const clientId = (req.socket.remoteAddress || 'unknown') + '-' + (req.headers['x-api-key'] || 'anonymous');
        const rateCheck = rateLimiter.check(clientId);
        if (!rateCheck.allowed) {
          securityAuditor.log('rate_limit', { clientId, path: req.url }, req.socket.remoteAddress);
          res.setHeader('X-RateLimit-Limit', '100');
          res.setHeader('X-RateLimit-Remaining', '0');
          res.setHeader('X-RateLimit-Reset', String(Math.ceil(rateCheck.resetAt / 1000)));
          return err(res, 429, 'Too many requests');
        }

        // Request size validation
        const contentLength = parseInt(req.headers['content-length'] || '0', 10);
        const sizeCheck = RequestSizeValidator.validateSize(contentLength);
        if (!sizeCheck.valid) {
          securityAuditor.log('validation_error', { error: sizeCheck.error, contentLength }, req.socket.remoteAddress);
          return err(res, 413, sizeCheck.error || 'Request too large');
        }

        const headerCheck = RequestSizeValidator.validateHeaders(req.headers);
        if (!headerCheck.valid) {
          securityAuditor.log('validation_error', { error: headerCheck.error }, req.socket.remoteAddress);
          return err(res, 431, headerCheck.error || 'Headers too large');
        }

        const isAuthOK = await authenticate(req);
        if (!isAuthOK) {
          securityAuditor.log('blocked_request', { reason: 'auth_failed', path: req.url }, req.socket.remoteAddress);
          return err(res, 401, 'Invalid API key');
        }

        const parsed = url.parse(req.url || '', true);
        const pathname = parsed.pathname || '/';

        if (req.method === 'GET' && pathname === '/status') {
          const root = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || '';
          return ok(res, { ok: true, status: 'running', workspace: root });
        }

        if (req.method === 'POST' && pathname === '/open') {
          const data = await parseJSON(req);
          const path = data.path as string;
          if (!path) return err(res, 400, 'Missing path');
          const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || '';
          const pathValidation = SecurityValidator.validatePath(path, workspaceRoot);
          if (!pathValidation.valid) {
            securityAuditor.log('validation_error', { error: pathValidation.error, path }, req.socket.remoteAddress);
            return err(res, 400, pathValidation.error || 'Invalid path');
          }
          const doc = await vscode.workspace.openTextDocument(vscode.Uri.file(pathValidation.sanitized!));
          await vscode.window.showTextDocument(doc, { preview: false });
          await commitIfEnabled(vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || '', `Open ${path}`);
          appendAudit({ type: 'open', file: path });
          return ok(res);
        }

        if (req.method === 'POST' && pathname === '/edit') {
          const data = await parseJSON(req);
          const path = data.path as string;
          const content = data.content as string;
          if (!path) return err(res, 400, 'Missing path');
          if (content === undefined) return err(res, 400, 'Missing content');
          
          const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || '';
          const pathValidation = SecurityValidator.validatePath(path, workspaceRoot);
          if (!pathValidation.valid) {
            securityAuditor.log('validation_error', { error: pathValidation.error, path }, req.socket.remoteAddress);
            return err(res, 400, pathValidation.error || 'Invalid path');
          }
          
          const contentValidation = SecurityValidator.validateContent(content);
          if (!contentValidation.valid) {
            securityAuditor.log('validation_error', { error: contentValidation.error }, req.socket.remoteAddress);
            return err(res, 400, contentValidation.error || 'Invalid content');
          }

          const document = await vscode.workspace.openTextDocument(vscode.Uri.file(pathValidation.sanitized!));
          const oldContent = document.getText();
          const editor = await vscode.window.showTextDocument(document, { preview: false });
          const full = new vscode.Range(
            document.positionAt(0),
            document.positionAt(document.getText().length)
          );

          await editor.edit((editBuilder) => {
            editBuilder.replace(full, content);
          });
          await document.save();
          await commitIfEnabled(vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || '', `Edit ${path}`);
          const auditEntry = appendAudit({ type: 'file', action: 'edit', file: path, before: oldContent, after: content });
          return ok(res);
        }

        if (req.method === 'POST' && pathname === '/save') {
          const data = await parseJSON(req);
          const path = data.path as string;
          if (!path) return err(res, 400, 'Missing path');
          const doc = await vscode.workspace.openTextDocument(vscode.Uri.file(path));
          await doc.save();
          await commitIfEnabled(vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || '', `Save ${path}`);
          return ok(res);
        }

        if (req.method === 'POST' && pathname === '/run') {
          const data = await parseJSON(req);
          const command = data.command as string;
          const args = data.args || [];
          if (!command) return err(res, 400, 'Missing command');
          
          const cmdValidation = SecurityValidator.validateCommand(command);
          if (!cmdValidation.valid) {
            securityAuditor.log('validation_error', { error: cmdValidation.error, command }, req.socket.remoteAddress);
            return err(res, 400, cmdValidation.error || 'Invalid command');
          }
          
          try {
            const r = await vscode.commands.executeCommand(command, ...args);
            await commitIfEnabled(vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || '', `Run ${command}`);
            return ok(res, { result: r });
          } catch (e: any) {
            return err(res, 500, e.message || String(e));
          }
        }

            if (req.method === 'POST' && pathname === '/commit') {
              // Body: { message: "commit message" }
              const data = await parseJSON(req);
              const message = (data.message as string) || 'HTTP API Commit';
              const workspacePath = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || '';

              // Prefer python ai_bots.git_auto_commit integration if available
              const pythonFile = pathModule.join(workspacePath, 'ai_bots', 'git_auto_commit.py');
              if (fs.existsSync(pythonFile)) {
                const snippet = `from ai_bots.git_auto_commit import get_auto_commit\nget_auto_commit().commit(\"${message.replace(/\"/g, '\\\"')}\")\nprint('OK')`;
                const r = await runPythonIfPresent(workspacePath, snippet);
                if (!r.success) {
                  // Fallback to git CLI
                  await commitIfEnabled(workspacePath, message);
                  return ok(res, { fallback: true, out: r.out || '', err: r.err || '' });
                }
                const auditEntry = appendAudit({ type: 'commit', method: 'python', message, details: { out: r.out || '', err: r.err || '' } });
                return ok(res, { used: 'python', out: r.out || '', audit: auditEntry });
              } else {
                await commitIfEnabled(workspacePath, message);
                const auditEntry = appendAudit({ type: 'commit', method: 'gitcli', message });
                return ok(res, { used: 'gitcli', audit: auditEntry });
              }
            }

            if (req.method === 'GET' && pathname === '/read') {
              const qry = parsed.query || {};
              const filePath = String(qry.path || '');
              if (!filePath) return err(res, 400, 'Missing path query param');
              try {
                const content = fs.readFileSync(filePath, 'utf8');
                return ok(res, { content });
              } catch (e: any) {
                return err(res, 500, e.message || String(e));
              }
            }

            if (req.method === 'GET' && pathname === '/list') {
              const qry = parsed.query || {};
              const dirPath = String(qry.path || vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || '.');
              try {
                const list = fs.readdirSync(dirPath).map((f) => ({ name: f, path: pathModule.join(dirPath, f), isDir: fs.statSync(pathModule.join(dirPath, f)).isDirectory() }));
                return ok(res, { items: list });
              } catch (e: any) {
                return err(res, 500, e.message || String(e));
              }
            }

            if (req.method === 'POST' && pathname === '/create') {
              const data = await parseJSON(req);
              const filePath = data.path as string;
              const content = data.content || '';
              if (!filePath) return err(res, 400, 'Missing path');
              try {
                let before: string | null = null;
                try { if (fs.existsSync(filePath)) before = fs.readFileSync(filePath, 'utf8'); } catch (e) {}
                fs.writeFileSync(filePath, content, { encoding: 'utf8', flag: 'w' });
                await commitIfEnabled(vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || '', `Create ${filePath}`);
                const auditEntry = appendAudit({ type: 'file', action: 'create', file: filePath, before, after: content });
                return ok(res, { audit: auditEntry });
              } catch (e: any) {
                return err(res, 500, e.message || String(e));
              }
            }

            if (req.method === 'POST' && pathname === '/delete') {
              const data = await parseJSON(req);
              const filePath = data.path as string;
              if (!filePath) return err(res, 400, 'Missing path');
              try {
                let before: string | null = null;
                try { if (fs.existsSync(filePath)) before = fs.readFileSync(filePath, 'utf8'); } catch (e) {}
                fs.unlinkSync(filePath);
                await commitIfEnabled(vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || '', `Delete ${filePath}`);
                const auditEntry = appendAudit({ type: 'file', action: 'delete', file: filePath, before, after: null });
                return ok(res, { audit: auditEntry });
              } catch (e: any) {
                return err(res, 500, e.message || String(e));
              }
            }

            if (req.method === 'POST' && pathname === '/settings') {
              const data = await parseJSON(req);
              // Body is { key: value, ... } we will iterate through entries and update user/global settings
              // Optionally include { apply: true } to actually apply. By default we preview.
              const apply = data.apply === true;
              delete data.apply;
              try {
                const keys = Object.keys(data || {});
                const result: any = { preview: [] };
                for (const k of keys) {
                  const keyValidation = SecurityValidator.sanitizeSettingKey(k);
                  if (!keyValidation.valid) {
                    securityAuditor.log('validation_error', { error: keyValidation.error, key: k }, req.socket.remoteAddress);
                    return err(res, 400, `Invalid setting key '${k}': ${keyValidation.error}`);
                  }
                  const val = data[k];
                  let before: any = null;
                  try { before = vscode.workspace.getConfiguration().get(k); } catch (e) {}
                  result.preview.push({ key: k, before, after: val });
                  if (apply) {
                    await vscode.workspace.getConfiguration().update(k, val, vscode.ConfigurationTarget.Global);
                  }
                }
                if (apply) {
                  await commitIfEnabled(vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || '', 'Apply settings via HTTP API');
                  const auditEntry = appendAudit({ type: 'settings', action: 'apply', changes: result.preview });
                  return ok(res, { applied: true, audit: auditEntry });
                }
                return ok(res, { applied: false, preview: result.preview });
              } catch (e: any) {
                return err(res, 500, e.message || String(e));
              }
            }

        if (req.method === 'GET' && pathname === '/extensions') {
          // List installed extensions with some metadata
          const extensions = vscode.extensions.all.map((ext) => ({ id: ext.id, displayName: (ext.packageJSON && ext.packageJSON.displayName) || ext.id, version: ext.packageJSON.version, contributes: ext.packageJSON.contributes || {} }));
          return ok(res, { extensions });
        }

        if (req.method === 'POST' && (pathname === '/yolo' || pathname === '/master-approve')) {
          // Body: { enable: true/false, keys: [], extensions: [] }
          const data = await parseJSON(req);
          const enable = data.enable === undefined ? true : Boolean(data.enable);
          const cfg = vscode.workspace.getConfiguration('vscodeHttpApi');
          const allowYolo = cfg.get<boolean>('yoloMode', false);
          if (!allowYolo) return err(res, 403, 'yoloMode disabled');

          const keys = Array.isArray(data.keys) ? data.keys : [];
          const targetExtensions = Array.isArray(data.extensions) && data.extensions.length > 0 ? data.extensions : null;
          const apply = data.apply === true;

          // Find setting keys in user settings that look like yolo or autoapprove
          const yoloKeys: string[] = [];
          const possibleRegex = [/yolo/i, /autoapprove|auto_approve|auto-approve|masterauto|master_auto|master-auto|enableAutoApprove|autoaccept|auto_accept|auto-accept/i];
          // If user provided explicit keys, use them first
          if (keys.length > 0) {
            for (const k of keys) {
              const prev = vscode.workspace.getConfiguration().get(k);
              if (apply) await vscode.workspace.getConfiguration().update(k, enable, vscode.ConfigurationTarget.Global);
              yoloKeys.push(k);
            }
          }

          // Scan all workspace/global settings that are strings — but we can only update via known keys from extensions' contributions
          const results: { settings: Array<{ key: string; prev: any }>; extensions: Record<string, { changed: Array<{ key: string; prev: any }>; skipped: string[]; error?: string }> } = { settings: [], extensions: {} };

          // Scan installed extensions and set relevant keys
          const extsToScan = targetExtensions ? targetExtensions : vscode.extensions.all.map((e) => e.id);
          for (const id of extsToScan) {
            try {
              const ext = vscode.extensions.getExtension(id);
              if (!ext) { results.extensions[id] = { changed: [], skipped: [], error: 'Not installed' }; continue; }
              const configProps = (ext.packageJSON && ext.packageJSON.contributes && ext.packageJSON.contributes.configuration && ext.packageJSON.contributes.configuration.properties) || {};
              const keys = Object.keys(configProps);
              const changed: Array<{ key: string; prev: any }> = [];
              const skipped: string[] = [];
              for (const k of keys) {
                const p = (configProps as any)[k] || {};
                const title = (p.title || '') + '';
                const description = (p.description || '') + '';
                let matched = false;
                for (const r of possibleRegex) { if (r.test(k) || r.test(title) || r.test(description)) { matched = true; break; } }
                if (matched) {
                  const prev = vscode.workspace.getConfiguration().get(k);
                  if (apply) await vscode.workspace.getConfiguration().update(k, enable, vscode.ConfigurationTarget.Global);
                  changed.push({ key: k, prev });
                } else { skipped.push(k); }
              }
              results.extensions[id] = { changed, skipped };
            } catch (e: any) {
              results.extensions[id] = { changed: [], skipped: [], error: String(e) };
            }
          }
          // Also set some common global keys that users may have for yolo/master auto-approval
          const commonKeys = [
            'yolo', 'yoloMode', 'yolo_mode', 'masterAutoApprove', 'master_auto_approve', 'autoApprove', 'auto_approve', 'ghostlink.yolo', 'ai.autoApprove', 'introspection.yolo'
          ];
          for (const k of commonKeys) {
            try {
              const prev = vscode.workspace.getConfiguration().get(k);
              if (apply) await vscode.workspace.getConfiguration().update(k, enable, vscode.ConfigurationTarget.Global);
              results.settings.push({ key: k, prev });
            } catch (e: any) {
              // ignore
            }
          }
          if (apply) {
            await commitIfEnabled(vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || '', 'Apply YOLO via HTTP API');
            const auditEntry = appendAudit({ type: 'yolo', action: 'apply', enable, results });
            return ok(res, { applied: true, audit: auditEntry, results });
          }
          return ok(res, { applied: false, results });
        }

        if (req.method === 'POST' && pathname === '/extensions/experimental') {
          // Body: { enable: true/false, extensions: [id1, id2] }
          const data = await parseJSON(req);
          const enable = data.enable === undefined ? true : Boolean(data.enable);
          const targetExtensions = Array.isArray(data.extensions) && data.extensions.length > 0 ? data.extensions : vscode.extensions.all.map((e) => e.id);
          const results: Record<string, { changed: Array<{ key: string; prev: any }>; skipped: string[]; error?: string }> = {};
          for (const id of targetExtensions) {
            try {
              const ext = vscode.extensions.getExtension(id);
              if (!ext) { results[id] = { changed: [], skipped: [], error: 'Not installed' }; continue; }

              const configProps = (ext.packageJSON && ext.packageJSON.contributes && ext.packageJSON.contributes.configuration && ext.packageJSON.contributes.configuration.properties) || {};
              const keys = Object.keys(configProps);
              const changed: Array<{ key: string; prev: any }> = [];
              const skipped: string[] = [];
              for (const k of keys) {
                const p = (configProps as any)[k] || {};
                const title = p.title || '';
                const description = p.description || '';
                const nameMatch = /experimental|beta|preview|proposed|enablePreview/i;
                if (nameMatch.test(k) || nameMatch.test(title) || nameMatch.test(description)) {
                  const prev = vscode.workspace.getConfiguration().get(k);
                  if (data.apply === true) await vscode.workspace.getConfiguration().update(k, enable, vscode.ConfigurationTarget.Global);
                  changed.push({ key: k, prev });
                } else { skipped.push(k); }
              }
              results[id] = { changed, skipped };
            } catch (e: any) {
              results[id] = { changed: [], skipped: [], error: String(e) };
            }
          }
          if (data.apply === true) {
            await commitIfEnabled(vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || '', 'Apply Experimental flags via HTTP API');
            const auditEntry = appendAudit({ type: 'experimental', action: 'apply', enable, results });
            return ok(res, { applied: true, audit: auditEntry, results });
          }
          return ok(res, { applied: false, results });
        }

        if (req.method === 'POST' && pathname === '/extensions/yolo') {
          // Body: { enable: true/false, extensions: [id1, id2] }
          const data = await parseJSON(req);
          const enable = data.enable === undefined ? true : Boolean(data.enable);
          const targetExtensions = Array.isArray(data.extensions) && data.extensions.length > 0 ? data.extensions : vscode.extensions.all.map((e) => e.id);
          const keywords = [/yolo/i, /autoapprove|auto_approve|auto-approve|masterauto|master_auto|master-auto|enableAutoApprove|autoaccept|auto_accept|auto-accept/i];
          const results: Record<string, { changed: Array<{ key: string; prev: any }>; skipped: string[]; error?: string }> = {};
          for (const id of targetExtensions) {
            try {
              const ext = vscode.extensions.getExtension(id);
              if (!ext) { results[id] = { changed: [], skipped: [], error: 'Not installed' }; continue; }
              const configProps = (ext.packageJSON && ext.packageJSON.contributes && ext.packageJSON.contributes.configuration && ext.packageJSON.contributes.configuration.properties) || {};
              const keys = Object.keys(configProps);
              const changed: Array<{ key: string; prev: any }> = [];
              const skipped: string[] = [];
              for (const k of keys) {
                const p = (configProps as any)[k] || {};
                const title = p.title || '';
                const description = p.description || '';
                let matched = false;
                for (const kw of keywords) {
                  if (kw.test(k) || kw.test(title) || kw.test(description)) { matched = true; break; }
                }
                  if (matched) {
                    const prev = vscode.workspace.getConfiguration().get(k);
                    if (data.apply === true) await vscode.workspace.getConfiguration().update(k, enable, vscode.ConfigurationTarget.Global);
                    changed.push({ key: k, prev });
                } else { skipped.push(k); }
              }
              results[id] = { changed, skipped };
            } catch (e: any) {
              results[id] = { changed: [], skipped: [], error: String(e) };
            }
          }
          if (data.apply === true) {
            await commitIfEnabled(vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || '', 'Apply Extensions YOLO via HTTP API');
            const auditEntry = appendAudit({ type: 'extensions.yolo', action: 'apply', enable, results });
            return ok(res, { applied: true, audit: auditEntry, results });
          }
          return ok(res, { applied: false, results });
        }

        if (req.method === 'POST' && pathname === '/exec') {
          // Dangerous: only allowed if allowExec is true and origin is loopback or allowRemote is true
          const cfg = vscode.workspace.getConfiguration('vscodeHttpApi');
          const allowExec = cfg.get<boolean>('allowExec', false);
          if (!allowExec) return err(res, 403, 'Exec endpoint disabled');

          // Must be either loopback or allowRemote
          const allowRemote = cfg.get<boolean>('allowRemote', false);
          const remoteAddress = (req.socket && req.socket.remoteAddress) || '';
          if (!allowRemote && remoteAddress && !remoteAddress.startsWith('127.') && !remoteAddress.startsWith('::1')) {
            return err(res, 403, 'Remote exec not allowed');
          }

          // Optional whitelist
          const whitelist = cfg.get<string[]>('execWhitelist', []);
          const data = await parseJSON(req);
          const cmd = data.command as string;
          const args = data.args || [];
          if (!cmd) return err(res, 400, 'Missing command');
          if (whitelist && whitelist.length > 0 && !whitelist.includes(cmd)) {
            return err(res, 403, 'Command not in whitelist');
          }

          // Run command in workspace root
          const workspacePath = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || (typeof (globalThis as any).process !== 'undefined' ? (globalThis as any).process.cwd() : '.');
          const child = spawn(cmd, args, { cwd: workspacePath, shell: true });
          let out = '';
          let errOut = '';
          child.stdout.on('data', (c) => (out += String(c)));
          child.stderr.on('data', (c) => (errOut += String(c)));
          child.on('close', async (code) => {
            await commitIfEnabled(workspacePath, `Exec ${cmd} ${args.join(' ')}`);
            const auditEntry = appendAudit({ type: 'exec', command: cmd, args, code, out, err: errOut });
            ok(res, { success: code === 0, code, out, err: errOut, audit: auditEntry });
          });
          return;
        }

        if (req.method === 'GET' && pathname === '/audit') {
          const qry = parsed.query || {};
          const id = String(qry.id || '');
          const limit = Number(qry.limit || 200);
          if (id) {
            const entries = await readAudit(limit);
            const target = entries.find((e: any) => e.id === id);
            if (!target) return err(res, 404, 'Not found');
            return ok(res, { entry: target });
          }
          const entries = await readAudit(limit);
          return ok(res, { entries });
        }

        if (req.method === 'GET' && pathname === '/audit/stats') {
          try {
            if (!fs.existsSync(auditPath)) return ok(res, { count: 0, size: 0, latest: null });
            const lines = fs.readFileSync(auditPath, 'utf8').split('\n').filter(Boolean);
            const count = lines.length;
            const size = fs.statSync(auditPath).size;
            let latest = null;
            try { latest = JSON.parse(lines[lines.length - 1]).ts || null; } catch (e) { latest = null; }
            return ok(res, { count, size, latest });
          } catch (e: any) { return err(res, 500, e.message || String(e)); }
        }

        if (req.method === 'POST' && pathname === '/audit/prune') {
          const cfg = vscode.workspace.getConfiguration('vscodeHttpApi');
          const allowPrune = cfg.get<boolean>('masterAutoApprove', false);
          if (!allowPrune) return err(res, 403, 'prune endpoint disabled by configuration');
          try {
            pruneAuditFile();
            const stats = { ok: true, message: 'prune completed' };
            return ok(res, stats);
          } catch (e: any) {
            return err(res, 500, e.message || String(e));
          }
        }

        if (req.method === 'POST' && pathname === '/rollback') {
          const cfg = vscode.workspace.getConfiguration('vscodeHttpApi');
          const allowRollback = cfg.get<boolean>('masterAutoApprove', false);
          if (!allowRollback) return err(res, 403, 'rollback endpoint disabled by configuration');
          const data = await parseJSON(req);
          const id = data.id as string;
          const limit = (data.limit as number) || 1000;
          const entries = await readAudit(limit);
          if (!id) return err(res, 400, 'Missing id');
          const target = entries.find((e: any) => e.id === id);
          if (!target) return err(res, 404, 'Not found');
          // Apply inverse operations for basic types
          try {
            if (target.type === 'settings' && Array.isArray(target.changes)) {
              for (const c of target.changes) {
                try { await vscode.workspace.getConfiguration().update(c.key, c.before, vscode.ConfigurationTarget.Global); } catch (e) {}
              }
            }
            // Revert extension toggles (experimental, yolo, extensions.yolo, etc.)
            if ((target.type && (target.type === 'yolo' || target.type === 'experimental' || target.type === 'extensions.yolo' || target.type === 'extensions.experimental')) && target.results) {
              try {
                // revert settings listed in results.settings
                if (Array.isArray(target.results.settings)) {
                  for (const s of target.results.settings) {
                    try { await vscode.workspace.getConfiguration().update(s.key, s.prev, vscode.ConfigurationTarget.Global); } catch (e) {}
                  }
                }
                // revert per-extension keys
                if (target.results.extensions) {
                  for (const extId of Object.keys(target.results.extensions)) {
                    const extResult = target.results.extensions[extId] || {};
                    if (Array.isArray(extResult.changed)) {
                      for (const k of extResult.changed) {
                        try { await vscode.workspace.getConfiguration().update(k.key, k.prev, vscode.ConfigurationTarget.Global); } catch (e) {}
                      }
                    }
                  }
                }
              } catch (e) {}
            }
            if (target.type === 'file' && target.action) {
              const fp = target.file;
              if (target.action === 'create') {
                // delete
                try { fs.unlinkSync(fp); } catch (e) {}
              } else if (target.action === 'delete') {
                try { if (target.before !== null && target.before !== undefined) fs.writeFileSync(fp, target.before, { encoding: 'utf8', flag: 'w' }); } catch (e) {}
              } else if (target.action === 'edit') {
                try { fs.writeFileSync(fp, target.before || '', { encoding: 'utf8', flag: 'w' }); } catch (e) {}
              }
            }
            await commitIfEnabled(vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || '', `Rollback ${id}`);
            const auditRoll = appendAudit({ type: 'rollback', id, target });
            return ok(res, { ok: true, audit: auditRoll });
          } catch (e: any) {
            return err(res, 500, e.message || String(e));
          }
        }

        if (req.method === 'GET' && pathname === '/security/events') {
          const cfg = vscode.workspace.getConfiguration('vscodeHttpApi');
          const masterApprove = cfg.get<boolean>('masterAutoApprove', false);
          if (!masterApprove) return err(res, 403, 'Security events endpoint requires masterAutoApprove');
          
          const qry = parsed.query || {};
          const type = String(qry.type || '');
          const since = qry.since ? new Date(String(qry.since)) : undefined;
          const filter: any = {};
          if (type) filter.type = type;
          if (since) filter.since = since;
          
          const events = securityAuditor.getEvents(filter);
          return ok(res, { events, count: events.length });
        }

        return err(res, 404, 'Not found');
      } catch (e: any) {
        securityAuditor.log('suspicious_activity', { error: String(e), path: req.url, stack: e.stack }, req.socket.remoteAddress);
        if ((globalThis as any).console && typeof (globalThis as any).console.error === 'function') (globalThis as any).console.error('vscode-http-api error:', e);
        return err(res, 500, e.message || String(e));
      }
    });

    server.listen(port, allowRemote ? undefined : '127.0.0.1', () => {
      vscode.window.showInformationMessage(`VSCode HTTP API listening on port ${port}`);
    });

    context.subscriptions.push({ dispose() { server?.close(); server = null; } });
  });

  context.subscriptions.push(startCommand);

  // register audit UI command
  try { registerAuditUI(context); } catch (e) {}

  // register TreeView provider for audit entries
  try {
    const provider = new AuditTreeProvider(context);
    vscode.window.registerTreeDataProvider('vscodeHttpApi.auditView', provider);
    context.subscriptions.push(vscode.commands.registerCommand('vscodeHttpApi.audit.refresh', () => provider.refresh()));
    context.subscriptions.push(vscode.commands.registerCommand('vscodeHttpApi.audit.prune', async () => {
      try {
        const cfg = vscode.workspace.getConfiguration('vscodeHttpApi');
        const port = cfg.get<number>('port', 8765);
        const apiKey = cfg.get<string>('apiKey', '');
        const bodyStr = '{}';
        function utf8ByteLen(s: string) { let len = 0; for (let i = 0; i < s.length; i++) { const code = s.charCodeAt(i); if (code <= 0x7f) len += 1; else if (code <= 0x7ff) len += 2; else if (code >= 0xd800 && code <= 0xdfff) { len += 4; i++; } else len += 3; } return len; }
        const byteLen = utf8ByteLen(bodyStr);
        const opts: any = { hostname: '127.0.0.1', port, path: '/audit/prune', method: 'POST', headers: { 'content-type': 'application/json', 'content-length': byteLen } };
        if (apiKey) opts.headers['x-api-key'] = apiKey;
        const req = http.request(opts, (res) => {
          let out = '';
          res.on('data', (c) => (out += c));
          res.on('end', () => { vscode.window.showInformationMessage('Audit prune completed'); provider.refresh(); });
        });
        req.on('error', (e) => { vscode.window.showErrorMessage(`Prune failed: ${String(e)}`); });
        req.write(bodyStr); req.end();
      } catch (e: any) { vscode.window.showErrorMessage(`Prune error: ${String(e)}`); }
    }));
    context.subscriptions.push(vscode.commands.registerCommand('vscodeHttpApi.audit.showDetails', async (item) => { if (item && item.entry) { const doc = await vscode.workspace.openTextDocument({ content: JSON.stringify(item.entry, null, 2), language: 'json' as any }); await vscode.window.showTextDocument(doc, { preview: false }); } }));
    context.subscriptions.push(vscode.commands.registerCommand('vscodeHttpApi.audit.rollback', async (item) => {
      if (!item || !item.entry || !item.entry.id) { vscode.window.showWarningMessage('No audit entry selected'); return; }
      // Show preview (webview & modal) before executing
      try {
        const { showRollbackPreviewAndConfirm } = await import('./audit_preview');
        const ok = await showRollbackPreviewAndConfirm(context, item.entry);
        if (!ok) { vscode.window.showInformationMessage('Rollback cancelled'); return; }
      } catch (e) { /* fallback to proceed without preview */ }
      const c = vscode.workspace.getConfiguration('vscodeHttpApi'); const port = c.get<number>('port', 8765); const apiKey = c.get<string>('apiKey', ''); const body = { id: item.entry.id };
      const bodyStr = JSON.stringify(body);
      // Compute UTF-8 byte length without relying on Node or DOM-specific types
      function utf8ByteLen(s: string) {
        let len = 0;
        for (let i = 0; i < s.length; i++) {
          const code = s.charCodeAt(i);
          if (code <= 0x7f) len += 1;
          else if (code <= 0x7ff) len += 2;
          else if (code >= 0xd800 && code <= 0xdfff) { // surrogate pair
            len += 4; i++; // skip next
          } else len += 3;
        }
        return len;
      }
      const byteLen = utf8ByteLen(bodyStr);
      const opts: any = { hostname: '127.0.0.1', port, path: '/rollback', method: 'POST', headers: { 'content-type': 'application/json', 'content-length': byteLen } };
      if (apiKey) opts.headers['x-api-key'] = apiKey;
      const req = http.request(opts, (res) => {
        let out = '';
        res.on('data', (c) => (out += c));
        res.on('end', () => {
          try { const resp = JSON.parse(out); vscode.window.showInformationMessage(`Rollback result: ${JSON.stringify(resp)}`); } catch (err: any) { vscode.window.showErrorMessage(`Rollback result parse error: ${String(err)}`); }
        });
      });
      req.on('error', (e) => { vscode.window.showErrorMessage(`Rollback failed: ${String(e)}`); });
      req.write(bodyStr); req.end();
    }));
  } catch (e) {}

  // Start automatically if setting present
  const cfg = vscode.workspace.getConfiguration('vscodeHttpApi');
  const autoStart = true; // Keep it always on by default
  if (autoStart) {
    vscode.commands.executeCommand('vscodeHttpApi.start');
  }

  // Schedule periodic audit pruning if retention settings are configured
  const auditCfg = vscode.workspace.getConfiguration('vscodeHttpApi');
  const maxEntries = auditCfg.get<number>('auditMaxEntries', 1000);
  const retentionDays = auditCfg.get<number>('auditRetentionDays', 0);
  if (maxEntries > 0 || retentionDays > 0) {
    const pruneInterval = (globalThis as any).setInterval(() => {
      try {
        // Run prune via command if available
        vscode.commands.executeCommand('vscodeHttpApi.audit.prune').then(undefined, () => {});
      } catch (e) {}
    }, 3600000); // 1 hour
    context.subscriptions.push({ dispose: () => (globalThis as any).clearInterval(pruneInterval) });
  }
}

export function deactivate() {
  if (server) {
    server.close();
    server = null;
  }
}
