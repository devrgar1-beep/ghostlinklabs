import { generateRollbackPreview } from '../src/audit_preview';

describe('generateRollbackPreview with diffs', () => {
  it('shows diff for file edit with before and after', () => {
    const entry = {
      id: '1',
      ts: '2025-11-24T00:00:00Z',
      type: 'file',
      action: 'edit',
      file: '/tmp/test.txt',
      before: 'line1\nline2\nline3',
      after: 'line1\nmodified\nline3'
    };
    const out = generateRollbackPreview(entry);
    expect(out.markdown).toContain('Diff');
    expect(out.markdown).toContain('- modified');
    expect(out.markdown).toContain('+ line2');
  });

  it('handles file create without diff', () => {
    const entry = { id: '2', ts: '2025-11-24T00:00:00Z', type: 'file', action: 'create', file: '/tmp/new.txt' };
    const out = generateRollbackPreview(entry);
    expect(out.markdown).toContain('DELETE');
    expect(out.markdown).not.toContain('Diff');
  });

  it('handles settings rollback', () => {
    const entry = {
      id: '3',
      ts: '2025-11-24T00:00:00Z',
      type: 'settings',
      changes: [
        { key: 'editor.fontSize', before: 12 },
        { key: 'editor.tabSize', before: 2 }
      ]
    };
    const out = generateRollbackPreview(entry);
    expect(out.markdown).toContain('Restore 2 settings');
    expect(out.markdown).toContain('editor.fontSize');
    expect(out.markdown).toContain('editor.tabSize');
  });
});
