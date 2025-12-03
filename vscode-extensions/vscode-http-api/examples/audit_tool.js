#!/usr/bin/env node
const { execSync } = require('child_process');

const URL = 'http://127.0.0.1:8765';
const API_KEY = process.env.VSCODE_HTTP_API_KEY || '';
const k = API_KEY ? `-H "x-api-key: ${API_KEY}"` : '';

function curl(method, path, data) {
  const url = `${URL}${path}`;
  let cmd = `curl -s -X ${method} ${k} -H "Content-Type: application/json"`;
  if (data) cmd += ` -d '${JSON.stringify(data).replace(/'/g, "'\\''")}'`;
  cmd += ` '${url}'`;
  return execSync(cmd, { encoding: 'utf8' });
}

const args = process.argv.slice(2);
if (args.length === 0) {
  console.log('Usage: node audit_tool.js <cmd> [args]');
  console.log('Commands: list [limit], get <id>, rollback <id>');
  process.exit(1);
}

const cmd = args[0];
try {
  switch (cmd) {
    case 'list': {
      const limit = args[1] || 200;
      console.log(curl('GET', `/audit?limit=${limit}`));
      break;
    }
    case 'get': {
      const id = args[1];
      if (!id) throw new Error('Missing id');
      console.log(curl('GET', `/audit?id=${id}`));
      break;
    }
    case 'rollback': {
      const id = args[1];
      if (!id) throw new Error('Missing id');
      console.log(curl('POST', '/rollback', { id }));
      break;
    }
    case 'prune': {
      // Prune local audit file via extension endpoint - requires masterAutoApprove
      console.log(curl('POST', '/audit/prune', {}));
      break;
    }
    case 'stats': {
      console.log(curl('GET', '/audit/stats'));
      break;
    }
    default:
      console.log('Unknown command', cmd);
  }
} catch (e) {
  console.error('Error:', e.message);
}
