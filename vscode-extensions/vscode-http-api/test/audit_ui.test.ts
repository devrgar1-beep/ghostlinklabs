import { readAuditFromDisk } from '../src/audit_ui';
import * as os from 'os';
import * as fs from 'fs';
import * as path from 'path';
import * as vscode from 'vscode';

describe('audit_ui', () => {
  it('readAuditFromDisk returns entries', async () => {
    const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'audit-ui-test-'));
    const auditFile = path.join(tmp, 'audit_log.jsonl');
    const entries = [
      { id: 'a', ts: new Date().toISOString(), type: 'file', action: 'create' },
      { id: 'b', ts: new Date().toISOString(), type: 'file', action: 'edit' }
    ];
    fs.writeFileSync(auditFile, entries.map((e) => JSON.stringify(e)).join('\n') + '\n', 'utf8');
    const fakeContext: any = { globalStorageUri: { fsPath: tmp } } as vscode.ExtensionContext;
    const out = await readAuditFromDisk(fakeContext, 10);
    expect(out.length).toBe(2);
  });
});
