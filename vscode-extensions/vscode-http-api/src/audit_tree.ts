import * as vscode from 'vscode';
import * as fs from 'fs';
import * as pathModule from 'path';

export interface AuditEntry {
  id?: string;
  ts?: string;
  type?: string;
  [k: string]: any;
}

function getAuditPath(context: vscode.ExtensionContext) {
  return context.globalStorageUri ? pathModule.join(context.globalStorageUri.fsPath, 'audit_log.jsonl') : pathModule.join(context.globalStoragePath || '.', 'audit_log.jsonl');
}

async function readAuditFromDisk(context: vscode.ExtensionContext, limit = 200) {
  const auditPath = getAuditPath(context);
  try {
    if (!fs.existsSync(auditPath)) return [];
    const lines = fs.readFileSync(auditPath, 'utf8').split('\n').filter(Boolean);
    const out = lines.map((l) => { try { return JSON.parse(l) as AuditEntry; } catch (e) { return { raw: l } as AuditEntry; } });
    return out.slice(-limit).reverse(); // newest first in view
  } catch (e) { return []; }
}

export class AuditTreeItem extends vscode.TreeItem {
  constructor(public readonly entry: AuditEntry) {
    const label = `${entry.ts || 'n/a'} ${entry.type || 'entry'} ${entry.id || ''}`;
    super(label, vscode.TreeItemCollapsibleState.None);
    this.tooltip = `${entry.type || 'entry'} ${entry.id || ''}`;
    this.description = entry.type || '';
    this.contextValue = 'auditEntry';
    this.command = { command: 'vscodeHttpApi.audit.showDetails', title: 'Show Audit Details', arguments: [this] } as any;
    // Set icon based on entry type
    const type = (entry.type || '').toLowerCase();
    if (type === 'file') {
      this.iconPath = new vscode.ThemeIcon('file');
    } else if (type === 'settings') {
      this.iconPath = new vscode.ThemeIcon('settings-gear');
    } else if (type === 'commit') {
      this.iconPath = new vscode.ThemeIcon('git-commit');
    } else if (type === 'exec') {
      this.iconPath = new vscode.ThemeIcon('terminal');
    } else if (type.includes('yolo') || type.includes('experimental')) {
      this.iconPath = new vscode.ThemeIcon('warning');
    } else if (type === 'rollback') {
      this.iconPath = new vscode.ThemeIcon('debug-reverse-continue');
    } else {
      this.iconPath = new vscode.ThemeIcon('circle-outline');
    }
  }
}

export class AuditTreeProvider implements vscode.TreeDataProvider<AuditTreeItem> {
  private _onDidChangeTreeData: vscode.EventEmitter<AuditTreeItem | undefined | null | void> = new vscode.EventEmitter<AuditTreeItem | undefined | null | void>();
  readonly onDidChangeTreeData: vscode.Event<AuditTreeItem | undefined | null | void> = this._onDidChangeTreeData.event;

  constructor(private context: vscode.ExtensionContext) {}

  refresh(): void {
    this._onDidChangeTreeData.fire();
  }

  async getTreeItem(element: AuditTreeItem): Promise<vscode.TreeItem> { return element; }

  async getChildren(element?: AuditTreeItem): Promise<AuditTreeItem[]> {
    const entries = await readAuditFromDisk(this.context, 500);
    return entries.map((e) => new AuditTreeItem(e));
  }
}
