"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const security_1 = require("../src/security");
describe('SecurityValidator', () => {
    describe('validatePath', () => {
        it('rejects paths with directory traversal', () => {
            const result = security_1.SecurityValidator.validatePath('../../../etc/passwd');
            expect(result.valid).toBe(false);
            expect(result.error).toContain('dangerous pattern');
        });
        it('rejects paths outside workspace', () => {
            const result = security_1.SecurityValidator.validatePath('/tmp/file.txt', '/home/user/workspace');
            expect(result.valid).toBe(false);
            expect(result.error).toContain('within workspace');
        });
        it('accepts valid paths within workspace', () => {
            const result = security_1.SecurityValidator.validatePath('/home/user/workspace/file.txt', '/home/user/workspace');
            expect(result.valid).toBe(true);
            expect(result.sanitized).toBeTruthy();
        });
        it('rejects system directories', () => {
            expect(security_1.SecurityValidator.validatePath('/etc/shadow').valid).toBe(false);
            expect(security_1.SecurityValidator.validatePath('/System/Library').valid).toBe(false);
            expect(security_1.SecurityValidator.validatePath('C:\\Windows\\System32').valid).toBe(false);
        });
        it('rejects overly long paths', () => {
            const longPath = 'a'.repeat(5000);
            expect(security_1.SecurityValidator.validatePath(longPath).valid).toBe(false);
        });
    });
    describe('validateContent', () => {
        it('accepts valid string content', () => {
            const result = security_1.SecurityValidator.validateContent('Hello world');
            expect(result.valid).toBe(true);
            expect(result.sanitized).toBe('Hello world');
        });
        it('rejects non-string content', () => {
            expect(security_1.SecurityValidator.validateContent(123).valid).toBe(false);
            expect(security_1.SecurityValidator.validateContent({}).valid).toBe(false);
        });
        it('rejects content exceeding size limit', () => {
            const huge = 'x'.repeat(11 * 1024 * 1024);
            expect(security_1.SecurityValidator.validateContent(huge).valid).toBe(false);
        });
        it('handles null and undefined', () => {
            expect(security_1.SecurityValidator.validateContent(null).valid).toBe(true);
            expect(security_1.SecurityValidator.validateContent(undefined).valid).toBe(true);
        });
    });
    describe('validateCommand', () => {
        it('accepts safe commands', () => {
            expect(security_1.SecurityValidator.validateCommand('workbench.action.files.save').valid).toBe(true);
            expect(security_1.SecurityValidator.validateCommand('editor.action.formatDocument').valid).toBe(true);
        });
        it('rejects commands with shell injection chars', () => {
            expect(security_1.SecurityValidator.validateCommand('cmd; rm -rf /').valid).toBe(false);
            expect(security_1.SecurityValidator.validateCommand('cmd && malicious').valid).toBe(false);
            expect(security_1.SecurityValidator.validateCommand('cmd | grep secret').valid).toBe(false);
            expect(security_1.SecurityValidator.validateCommand('cmd `whoami`').valid).toBe(false);
        });
        it('rejects overly long commands', () => {
            const long = 'a'.repeat(2000);
            expect(security_1.SecurityValidator.validateCommand(long).valid).toBe(false);
        });
    });
    describe('sanitizeSettingKey', () => {
        it('accepts valid setting keys', () => {
            expect(security_1.SecurityValidator.sanitizeSettingKey('editor.fontSize').valid).toBe(true);
            expect(security_1.SecurityValidator.sanitizeSettingKey('workbench.colorTheme').valid).toBe(true);
            expect(security_1.SecurityValidator.sanitizeSettingKey('my-extension.setting_name').valid).toBe(true);
        });
        it('rejects keys with invalid characters', () => {
            expect(security_1.SecurityValidator.sanitizeSettingKey('key with spaces').valid).toBe(false);
            expect(security_1.SecurityValidator.sanitizeSettingKey('key/with/slashes').valid).toBe(false);
            expect(security_1.SecurityValidator.sanitizeSettingKey('key;injection').valid).toBe(false);
        });
        it('rejects overly long keys', () => {
            const long = 'a'.repeat(300);
            expect(security_1.SecurityValidator.sanitizeSettingKey(long).valid).toBe(false);
        });
    });
});
describe('RateLimiter', () => {
    it('allows requests under limit', () => {
        const limiter = new security_1.RateLimiter(1000, 5);
        for (let i = 0; i < 5; i++) {
            const result = limiter.check('test-client');
            expect(result.allowed).toBe(true);
        }
    });
    it('blocks requests over limit', () => {
        const limiter = new security_1.RateLimiter(1000, 3);
        limiter.check('test-client');
        limiter.check('test-client');
        limiter.check('test-client');
        const result = limiter.check('test-client');
        expect(result.allowed).toBe(false);
        expect(result.remaining).toBe(0);
    });
    it('resets after window expires', (done) => {
        const limiter = new security_1.RateLimiter(100, 2);
        limiter.check('test-client');
        limiter.check('test-client');
        expect(limiter.check('test-client').allowed).toBe(false);
        setTimeout(() => {
            expect(limiter.check('test-client').allowed).toBe(true);
            done();
        }, 150);
    });
    it('tracks different clients separately', () => {
        const limiter = new security_1.RateLimiter(1000, 2);
        limiter.check('client1');
        limiter.check('client1');
        expect(limiter.check('client1').allowed).toBe(false);
        expect(limiter.check('client2').allowed).toBe(true);
    });
});
describe('RequestSizeValidator', () => {
    it('accepts requests under size limit', () => {
        expect(security_1.RequestSizeValidator.validateSize(1024).valid).toBe(true);
        expect(security_1.RequestSizeValidator.validateSize(1024 * 1024).valid).toBe(true);
    });
    it('rejects oversized requests', () => {
        const result = security_1.RequestSizeValidator.validateSize(10 * 1024 * 1024);
        expect(result.valid).toBe(false);
        expect(result.error).toContain('exceeds maximum size');
    });
    it('validates header size', () => {
        const smallHeaders = { 'content-type': 'application/json' };
        expect(security_1.RequestSizeValidator.validateHeaders(smallHeaders).valid).toBe(true);
        const hugeHeaders = { 'x-huge': 'x'.repeat(10000) };
        expect(security_1.RequestSizeValidator.validateHeaders(hugeHeaders).valid).toBe(false);
    });
});
describe('SecurityAuditor', () => {
    it('logs security events', () => {
        const auditor = new security_1.SecurityAuditor();
        auditor.log('blocked_request', { reason: 'test' });
        const events = auditor.getEvents();
        expect(events.length).toBe(1);
        expect(events[0].type).toBe('blocked_request');
    });
    it('filters events by type', () => {
        const auditor = new security_1.SecurityAuditor();
        auditor.log('blocked_request', {});
        auditor.log('rate_limit', {});
        auditor.log('blocked_request', {});
        const blocked = auditor.getEvents({ type: 'blocked_request' });
        expect(blocked.length).toBe(2);
    });
    it('filters events by time', () => {
        const auditor = new security_1.SecurityAuditor();
        const past = new Date(Date.now() - 1000);
        auditor.log('blocked_request', {});
        const recent = auditor.getEvents({ since: past });
        expect(recent.length).toBe(1);
        const future = new Date(Date.now() + 1000);
        const none = auditor.getEvents({ since: future });
        expect(none.length).toBe(0);
    });
    it('limits stored events', () => {
        const auditor = new security_1.SecurityAuditor();
        for (let i = 0; i < 1500; i++) {
            auditor.log('blocked_request', { index: i });
        }
        const events = auditor.getEvents();
        expect(events.length).toBeLessThanOrEqual(1000);
    });
    it('clears all events', () => {
        const auditor = new security_1.SecurityAuditor();
        auditor.log('blocked_request', {});
        auditor.clear();
        expect(auditor.getEvents().length).toBe(0);
    });
});
//# sourceMappingURL=security.test.js.map