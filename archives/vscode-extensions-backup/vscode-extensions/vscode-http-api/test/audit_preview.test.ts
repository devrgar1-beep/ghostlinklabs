import { generateRollbackPreview } from '../src/audit_preview';

describe('generateRollbackPreview', () => {
  it('creates preview for file create', () => {
    const entry = { id: '1', ts: '2025-11-24T00:00:00Z', type: 'file', action: 'create', file: '/tmp/a.txt' };
    const out = generateRollbackPreview(entry);
    expect(out.markdown).toContain('DELETE the file created');
    expect(out.markdown).toContain('/tmp/a.txt');
  });
  it('creates preview for file edit', () => {
    const entry = { id: '2', ts: '2025-11-24T00:00:00Z', type: 'file', action: 'edit', file: '/tmp/b.txt', before: 'old' };
    const out = generateRollbackPreview(entry);
    expect(out.markdown).toContain('RESTORE previous contents');
    expect(out.markdown).toContain('/tmp/b.txt');
  });
  it('creates preview for settings', () => {
    const entry = { id: '3', ts: '2025-11-24T00:00:00Z', type: 'settings', changes: [{ key: 'abc', before: 1 }] };
    const out = generateRollbackPreview(entry);
    expect(out.markdown).toContain('Restore 1 settings');
    expect(out.markdown).toContain('abc');
  });
});
