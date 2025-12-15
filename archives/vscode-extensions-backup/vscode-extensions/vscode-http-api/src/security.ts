import * as vscode from 'vscode';
import * as pathModule from 'path';

// Input validation and sanitization utilities
export class SecurityValidator {
  private static readonly MAX_PATH_LENGTH = 4096;
  private static readonly MAX_CONTENT_LENGTH = 10 * 1024 * 1024; // 10MB
  private static readonly MAX_COMMAND_LENGTH = 1024;
  private static readonly DANGEROUS_PATH_PATTERNS = [
    /\.\./,  // Directory traversal
    /~\//,   // Home directory shortcuts that could escape workspace
    /\/etc\//i,
    /\/proc\//i,
    /\/sys\//i,
    /\/dev\//i,
    /^\/System\//i,  // macOS system dirs
    /^\/Library\//i,
    /^C:\\Windows\\/i,  // Windows system dirs
    /^C:\\Program Files\\/i
  ];

  static validatePath(path: string, workspaceRoot?: string): { valid: boolean; error?: string; sanitized?: string } {
    if (!path || typeof path !== 'string') {
      return { valid: false, error: 'Path must be a non-empty string' };
    }

    if (path.length > this.MAX_PATH_LENGTH) {
      return { valid: false, error: `Path exceeds maximum length of ${this.MAX_PATH_LENGTH}` };
    }

    // Check for dangerous patterns
    for (const pattern of this.DANGEROUS_PATH_PATTERNS) {
      if (pattern.test(path)) {
        return { valid: false, error: 'Path contains potentially dangerous pattern' };
      }
    }

    // Resolve to absolute path and check it's within workspace
    const absPath = pathModule.resolve(path);
    if (workspaceRoot) {
      const absRoot = pathModule.resolve(workspaceRoot);
      if (!absPath.startsWith(absRoot)) {
        return { valid: false, error: 'Path must be within workspace root' };
      }
    }

    return { valid: true, sanitized: absPath };
  }

  static validateContent(content: any): { valid: boolean; error?: string; sanitized?: string } {
    if (content === null || content === undefined) {
      return { valid: true, sanitized: '' };
    }

    if (typeof content !== 'string') {
      return { valid: false, error: 'Content must be a string' };
    }

    if (content.length > this.MAX_CONTENT_LENGTH) {
      return { valid: false, error: `Content exceeds maximum length of ${this.MAX_CONTENT_LENGTH}` };
    }

    return { valid: true, sanitized: content };
  }

  static validateCommand(command: string): { valid: boolean; error?: string } {
    if (!command || typeof command !== 'string') {
      return { valid: false, error: 'Command must be a non-empty string' };
    }

    if (command.length > this.MAX_COMMAND_LENGTH) {
      return { valid: false, error: `Command exceeds maximum length of ${this.MAX_COMMAND_LENGTH}` };
    }

    // Check for shell injection patterns
    const dangerousChars = /[;&|`$()><]/;
    if (dangerousChars.test(command)) {
      return { valid: false, error: 'Command contains potentially dangerous characters' };
    }

    return { valid: true };
  }

  static sanitizeSettingKey(key: string): { valid: boolean; error?: string; sanitized?: string } {
    if (!key || typeof key !== 'string') {
      return { valid: false, error: 'Setting key must be a non-empty string' };
    }

    // Setting keys should be alphanumeric with dots and hyphens
    if (!/^[a-zA-Z0-9._-]+$/.test(key)) {
      return { valid: false, error: 'Setting key contains invalid characters' };
    }

    if (key.length > 256) {
      return { valid: false, error: 'Setting key too long' };
    }

    return { valid: true, sanitized: key };
  }
}

// Rate limiting for API endpoints
export class RateLimiter {
  private requests: Map<string, number[]> = new Map();
  private readonly windowMs: number;
  private readonly maxRequests: number;

  constructor(windowMs = 60000, maxRequests = 100) {
    this.windowMs = windowMs;
    this.maxRequests = maxRequests;
  }

  check(identifier: string): { allowed: boolean; remaining: number; resetAt: number } {
    const now = Date.now();
    const windowStart = now - this.windowMs;
    
    // Get existing requests for this identifier
    let timestamps = this.requests.get(identifier) || [];
    
    // Filter out expired timestamps
    timestamps = timestamps.filter(ts => ts > windowStart);
    
    // Check if limit exceeded
    const allowed = timestamps.length < this.maxRequests;
    
    if (allowed) {
      timestamps.push(now);
      this.requests.set(identifier, timestamps);
    }

    const remaining = Math.max(0, this.maxRequests - timestamps.length);
    const resetAt = timestamps.length > 0 ? timestamps[0] + this.windowMs : now + this.windowMs;

    return { allowed, remaining, resetAt };
  }

  reset(identifier: string): void {
    this.requests.delete(identifier);
  }

  cleanup(): void {
    const now = Date.now();
    const windowStart = now - this.windowMs;
    
    for (const [identifier, timestamps] of this.requests.entries()) {
      const filtered = timestamps.filter(ts => ts > windowStart);
      if (filtered.length === 0) {
        this.requests.delete(identifier);
      } else {
        this.requests.set(identifier, filtered);
      }
    }
  }
}

// Request size limits
export class RequestSizeValidator {
  private static readonly MAX_JSON_SIZE = 5 * 1024 * 1024; // 5MB
  private static readonly MAX_HEADER_SIZE = 8 * 1024; // 8KB

  static validateSize(contentLength: number): { valid: boolean; error?: string } {
    if (contentLength > this.MAX_JSON_SIZE) {
      return { valid: false, error: `Request body exceeds maximum size of ${this.MAX_JSON_SIZE} bytes` };
    }
    return { valid: true };
  }

  static validateHeaders(headers: any): { valid: boolean; error?: string } {
    const headerStr = JSON.stringify(headers);
    if (headerStr.length > this.MAX_HEADER_SIZE) {
      return { valid: false, error: 'Request headers too large' };
    }
    return { valid: true };
  }
}

// Audit security events
export interface SecurityEvent {
  timestamp: string;
  type: 'blocked_request' | 'rate_limit' | 'validation_error' | 'suspicious_activity';
  details: any;
  source?: string;
}

export class SecurityAuditor {
  private events: SecurityEvent[] = [];
  private readonly maxEvents = 1000;

  log(type: SecurityEvent['type'], details: any, source?: string): void {
    this.events.push({
      timestamp: new Date().toISOString(),
      type,
      details,
      source
    });

    // Keep only recent events
    if (this.events.length > this.maxEvents) {
      this.events = this.events.slice(-this.maxEvents);
    }
  }

  getEvents(filter?: { type?: SecurityEvent['type']; since?: Date }): SecurityEvent[] {
    let filtered = this.events;
    
    if (filter?.type) {
      filtered = filtered.filter(e => e.type === filter.type);
    }
    
    if (filter?.since) {
      const sinceTs = filter.since.getTime();
      filtered = filtered.filter(e => new Date(e.timestamp).getTime() >= sinceTs);
    }
    
    return filtered;
  }

  clear(): void {
    this.events = [];
  }
}
