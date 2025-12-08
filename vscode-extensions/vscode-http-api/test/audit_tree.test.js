"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
const audit_tree_1 = require("../src/audit_tree");
const os = __importStar(require("os"));
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
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
        const fakeContext = { globalStorageUri: { fsPath: tmp } };
        const provider = new audit_tree_1.AuditTreeProvider(fakeContext);
        const children = await provider.getChildren();
        expect(children.length).toBe(2);
        expect(children[0].entry.id).toBe('2'); // newest first
        expect(children[1].entry.id).toBe('1');
    });
});
//# sourceMappingURL=audit_tree.test.js.map