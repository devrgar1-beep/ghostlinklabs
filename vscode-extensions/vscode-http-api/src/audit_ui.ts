import * as vscode from 'vscode';
import * as fs from 'fs';
import * as pathModule from 'path';
import * as http from 'http';

function getAuditPath(context: vscode.ExtensionContext) {
  return context.globalStorageUri ? pathModule.join(context.globalStorageUri.fsPath, 'audit_log.jsonl') : pathModule.join(context.globalStoragePath || '.', 'audit_log.jsonl');
}

export async function readAuditFromDisk(context: vscode.ExtensionContext, limit = 200) {
  const auditPath = getAuditPath(context);
  try {
    if (!fs.existsSync(auditPath)) return [];
    const lines = fs.readFileSync(auditPath, 'utf8').split('\n').filter(Boolean);
    const out = lines.map((l) => { try { return JSON.parse(l); } catch (e) { return { raw: l }; } });
    return out.slice(-limit);
  } catch (e) { return []; }
}

export function postJSON(urlStr: string, body: any, apiKey?: string): Promise<any> {
  return new Promise((resolve, reject) => {
    try {
      const u = new URL(urlStr);
      const data = JSON.stringify(body || {});
      const opts: any = { method: 'POST', hostname: u.hostname, port: Number(u.port || 80), path: u.pathname + (u.search || ''), headers: { 'content-type': 'application/json', 'content-length': Buffer.byteLength(data) } };
      if (apiKey) opts.headers['x-api-key'] = apiKey;
      const req = http.request(opts, (res) => {
        let out = '';
        res.on('data', (c) => (out += c));
        res.on('end', () => {
          try { resolve(JSON.parse(out)); } catch (e) { resolve(out); }
        });
      });
      req.on('error', (e) => reject(e));
      req.write(data);
      req.end();
    } catch (e) { reject(e); }
  });
}

export function registerAuditUI(context: vscode.ExtensionContext) {
  const cmd = vscode.commands.registerCommand('vscodeHttpApi.audit.show', async () => {
    try {
      const entries = await readAuditFromDisk(context, 500);
      if (!entries || entries.length === 0) { vscode.window.showInformationMessage('No audit entries found.'); return; }
      const items = entries.map((e: any) => {
        const label = `${e.ts || 'n/a'} ${e.type || ''} ${e.id || ''}`;
        const detail = e.type === 'file' && e.action ? `${e.action}: ${e.file}` : (e.type === 'settings' ? `settings:${(e.changes || []).length} changes` : JSON.stringify(e).slice(0, 200));
        return { label, detail, entry: e } as any;
      });
      const pick = await vscode.window.showQuickPick(items as any[], { matchOnDescription: true, matchOnDetail: true, placeHolder: 'Select an audit entry to inspect' });
      if (!pick) return;
      const e = pick.entry;
      // show full details in an editor-like webview? For now show quick pick choices: details, rollback
      const action = await vscode.window.showQuickPick(['Show details', 'Rollback', 'Cancel'], { placeHolder: 'Action' });
      if (!action || action === 'Cancel') return;
      if (action === 'Show details') {
        const doc = await vscode.workspace.openTextDocument({ content: JSON.stringify(e, null, 2), language: 'json' as any });
        await vscode.window.showTextDocument(doc, { preview: false });
        return;
      }
      if (action === 'Rollback') {
        const confirm = await vscode.window.showWarningMessage(`Rollback audit id ${e.id}? This will attempt to revert the changes.`, { modal: true }, 'Rollback');
        if (confirm !== 'Rollback') return;
        try {
          // Attempt to show the preview (non-blocking if missing)
          try { const { showRollbackPreviewAndConfirm } = await import('./audit_preview'); const ok = await showRollbackPreviewAndConfirm(context, e); if (!ok) return; } catch (err) {}
          const cfg = vscode.workspace.getConfiguration('vscodeHttpApi');
          const port = cfg.get<number>('port', 8765);
          const apiKey = cfg.get<string>('apiKey', '');
          const r = await postJSON(`http://127.0.0.1:${port}/rollback`, { id: e.id }, apiKey || undefined);
          vscode.window.showInformationMessage(`Rollback result: ${JSON.stringify(r)}`);
        } catch (err: any) {
          vscode.window.showErrorMessage(`Rollback failed: ${String(err)}`);
        }
      }
    } catch (e: any) {
      vscode.window.showErrorMessage('Error reading audit log: ' + String(e));
    }
  });
  context.subscriptions.push(cmd);
}
