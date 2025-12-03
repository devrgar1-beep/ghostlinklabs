import * as vscode from 'vscode';

function generateDiff(before: string | null, after: string | null, maxLines = 20): string {
  const b = (before || '').split('\n');
  const a = (after || '').split('\n');
  const lines: string[] = [];
  const max = Math.max(b.length, a.length);
  const display = Math.min(max, maxLines);
  for (let i = 0; i < display; i++) {
    const bLine = b[i] !== undefined ? b[i] : '';
    const aLine = a[i] !== undefined ? a[i] : '';
    if (bLine !== aLine) {
      if (bLine) lines.push(`- ${bLine}`);
      if (aLine) lines.push(`+ ${aLine}`);
    } else {
      lines.push(`  ${bLine}`);
    }
  }
  if (max > maxLines) lines.push(`... (${max - maxLines} more lines)`);
  return lines.join('\n');
}

export function generateRollbackPreview(entry: any): { title: string; markdown: string } {
  const lines: string[] = [];
  const id = entry.id || '(unknown)';
  const ts = entry.ts || '(unknown time)';
  lines.push(`### Rollback Preview: ${id}`);
  lines.push(`Timestamp: ${ts}`);
  lines.push('');
  switch ((entry.type || '').toLowerCase()) {
    case 'file':
      const action = (entry.action || '').toLowerCase();
      if (action === 'create') {
        lines.push(`- This rollback will DELETE the file created: \\`${entry.file}\\` (revert of create).`);
      } else if (action === 'delete') {
        lines.push(`- This rollback will RECREATE the deleted file: \\`${entry.file}\\` with previous contents (if present).`);
      } else if (action === 'edit') {
        const beforeLen = entry.before ? String(entry.before).length : 0;
        lines.push(`- This rollback will RESTORE previous contents for file: \`${entry.file}\` (length: ${beforeLen} characters).`);
        if (entry.before && entry.after) {
          lines.push('');
          lines.push('**Diff (current → previous):**');
          lines.push('```diff');
          lines.push(generateDiff(entry.after, entry.before, 15));
          lines.push('```');
        }
      } else {
        lines.push(`- File operation: ${action} — preview not available.`);
      }
      break;
    case 'settings':
      if (Array.isArray(entry.changes)) {
        lines.push(`- Restore ${entry.changes.length} settings to their prior values:`);
        for (const c of entry.changes) {
          lines.push(`  - \\`${c.key}\\`: revert to \\`${JSON.stringify(c.before)}\\``);
        }
      } else {
        lines.push('- Settings rollback: preview not available.');
      }
      break;
    case 'yolo':
    case 'experimental':
    case 'extensions.yolo':
    case 'extensions.experimental':
      lines.push('- This rollback will revert extension and global toggles listed in the `results` field where applicable.');
      if (entry.results) {
        if (Array.isArray(entry.results.settings)) {
          lines.push(`- Settings: ${entry.results.settings.length} items`);
        }
        if (entry.results.extensions) {
          const printExt = Object.keys(entry.results.extensions).length;
          lines.push(`- Per-extension changes: ${printExt} extensions`);
        }
      }
      break;
    case 'commit':
      lines.push('- Commit rollback is non-destructive: this will not undo commits created. Use Git to revert commit if needed.');
      break;
    case 'exec':
      lines.push(`- Exec rollback: this entry ran command: \\`${entry.command} ${(entry.args || []).join(' ')}\\`. Manual review recommended.`);
      break;
    default:
      lines.push('- Unknown or unhandled entry type; manual review recommended.');
  }
  // Add raw details for power users
  lines.push('');
  lines.push('**Raw entry**');
  lines.push('```json');
  try {
    lines.push(JSON.stringify(entry, null, 2));
  } catch (e) {
    lines.push(String(entry));
  }
  lines.push('```');
  return { title: `Rollback Preview (${id})`, markdown: lines.join('\n') };
}

export async function showRollbackPreviewAndConfirm(context: vscode.ExtensionContext, entry: any): Promise<boolean> {
  const { title, markdown } = generateRollbackPreview(entry);
  const panel = vscode.window.createWebviewPanel('vscodeHttpApi.rollbackPreview', title, { viewColumn: vscode.ViewColumn.One, preserveFocus: false }, {});
  panel.webview.html = `<!doctype html><html><body><h2>${title}</h2><pre>${markdown.replace(/</g, '&lt;')}</pre><p><i>Use Command Palette or context menu to trigger the rollback once confirmed.</i></p></body></html>`;
  // Also show a modal confirm prompt with markdown preview (for quick confirmation)
  const yes = 'Rollback';
  const cancel = 'Cancel';
  const opts = { modal: true } as any;
  const choice = await vscode.window.showInformationMessage('Proceed with rollback? This will attempt to revert recorded changes.', yes, cancel);
  panel.dispose();
  return choice === yes;
}
