"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const audit_utils_1 = require("../src/audit_utils");
describe('audit_utils', () => {
    test('truncateContent truncates long content', () => {
        const s = 'a'.repeat(100);
        expect((0, audit_utils_1.truncateContent)(s, 10)).toMatch(/\.\.\.\[truncated\]$/);
        expect((0, audit_utils_1.truncateContent)('short', 10)).toBe('short');
        expect((0, audit_utils_1.truncateContent)(null, 10)).toBeNull();
    });
    test('pruneAuditEntries by maxEntries', () => {
        const entries = Array.from({ length: 10 }, (_, i) => ({ ts: new Date(2000 + i, 1, 1).toISOString() }));
        const out = (0, audit_utils_1.pruneAuditEntries)(entries, 5, 0);
        expect(out.length).toBe(5);
    });
    test('pruneAuditEntries by days', () => {
        const now = Date.now();
        const arr = [
            { ts: new Date(now - (1000 * 60 * 60 * 24 * 100)).toISOString() },
            { ts: new Date(now).toISOString() },
        ];
        const out = (0, audit_utils_1.pruneAuditEntries)(arr, 0, 30);
        expect(out.length).toBe(1);
    });
    test('applyTruncateToEntry applies truncation', () => {
        const entry = { before: 'b'.repeat(100), after: 'c'.repeat(200), details: { out: 'd'.repeat(50) } };
        const out = (0, audit_utils_1.applyTruncateToEntry)(entry, 10);
        expect(out.before.length).toBeGreaterThan(0);
        expect(out.before.endsWith('...[truncated]')).toBe(true);
    });
});
//# sourceMappingURL=audit_utils.test.js.map