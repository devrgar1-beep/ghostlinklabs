export function truncateContent(content: string | null | undefined, maxLen: number): string | null | undefined {
  if (!content || typeof content !== 'string') return content;
  if (!maxLen || maxLen === 0) return content;
  if (content.length <= maxLen) return content;
  return content.slice(0, maxLen) + '...[truncated]';
}

export function pruneAuditEntries(entries: any[], maxEntries: number, retainDays: number): any[] {
  let out = entries.slice();
  const nowTs = Date.now();
  if (retainDays && retainDays > 0) {
    const cutoff = nowTs - (retainDays * 24 * 60 * 60 * 1000);
    out = out.filter((e) => {
      try { return (new Date(e.ts)).getTime() >= cutoff; } catch (e) { return true; }
    });
  }
  if (maxEntries && maxEntries > 0 && out.length > maxEntries) {
    out = out.slice(-maxEntries);
  }
  return out;
}

export function applyTruncateToEntry(entry: any, maxLen: number): any {
  if (!entry || typeof entry !== 'object') return entry;
  const e = JSON.parse(JSON.stringify(entry));
  if (e.before && typeof e.before === 'string') e.before = truncateContent(e.before, maxLen);
  if (e.after && typeof e.after === 'string') e.after = truncateContent(e.after, maxLen);
  if (e.details && typeof e.details === 'object' && e.details.out && typeof e.details.out === 'string') e.details.out = truncateContent(e.details.out, maxLen);
  return e;
}
