import { AuditTreeProvider } from '../src/audit_tree';
import * as os from 'os';
import * as fs from 'fs';
import * as path from 'path';
import * as vscode from 'vscode';

describe('AuditTreeProvider', () => {
  it('reads entries from disk and returns tree items', async () => {
    const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'audit-test-'));
    const auditFile = path.join(tmp, 'audit_log.jsonl');
    const entries = [
      { id: '1', ts: new Date().toISOString(), type: 'file', action: 'create', file: '/tmp/a.txt' },
      { id: '2', ts: new Date().toISOString(), type: 'file', action: 'edit', file: '/tmp/b.txt' }
    ];
    fs.writeFileSync(auditFile, entries.map((e) => JSON.stringify(e)).join('\n') + '\n', 'utf8');

    // Create a fake context with globalStorageUri
    const fakeContext: any = { globalStorageUri: { fsPath: tmp } } as vscode.ExtensionContext;

    const provider = new AuditTreeProvider(fakeContext);
    const children = await provider.getChildren();
    expect(children.length).toBe(2);
    expect(children[0].entry.id).toBe('2'); // newest first
    expect(children[1].entry.id).toBe('1');
  });
});
