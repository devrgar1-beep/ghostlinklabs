import { truncateContent, pruneAuditEntries, applyTruncateToEntry } from '../src/audit_utils';

describe('audit_utils', () => {
  test('truncateContent truncates long content', () => {
    const s = 'a'.repeat(100);
    expect(truncateContent(s, 10)).toMatch(/\.\.\.\[truncated\]$/);
    expect(truncateContent('short', 10)).toBe('short');
    expect(truncateContent(null as any, 10)).toBeNull();
  });

  test('pruneAuditEntries by maxEntries', () => {
    const entries = Array.from({ length: 10 }, (_, i) => ({ ts: new Date(2000 + i, 1, 1).toISOString() }));
    const out = pruneAuditEntries(entries, 5, 0);
    expect(out.length).toBe(5);
  });

  test('pruneAuditEntries by days', () => {
    const now = Date.now();
    const arr = [
      { ts: new Date(now - (1000 * 60 * 60 * 24 * 100)).toISOString() }, // 100 days ago
      { ts: new Date(now).toISOString() },
    ];
    const out = pruneAuditEntries(arr, 0, 30);
    expect(out.length).toBe(1);
  });

  test('applyTruncateToEntry applies truncation', () => {
    const entry = { before: 'b'.repeat(100), after: 'c'.repeat(200), details: { out: 'd'.repeat(50) } };
    const out = applyTruncateToEntry(entry, 10);
    expect(out.before.length).toBeGreaterThan(0);
    expect(out.before.endsWith('...[truncated]')).toBe(true);
  });
});
