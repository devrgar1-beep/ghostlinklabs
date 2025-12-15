#!/usr/bin/env node
const { execSync } = require('child_process');

const args = process.argv.slice(2);
if (args.length === 0) {
  console.log('Usage: node client_node.js <cmd> [args]');
  console.log('Commands: status, open <path>, read <path>, list <path>, edit <path> <content>, create <path> <content>, delete <path>, commit <message>, settings <json>, audit, rollback <id>');
  process.exit(1);
}

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

const cmd = args[0];
try {
  switch (cmd) {
    case 'status':
      console.log(curl('GET', '/status'));
      break;
    case 'open':
      console.log(curl('POST', '/open', { path: args[1] }));
      break;
    case 'read':
      console.log(curl('GET', `/read?path=${encodeURIComponent(args[1])}`));
      break;
    case 'list':
      console.log(curl('GET', `/list?path=${encodeURIComponent(args[1] || '')}`));
      break;
    case 'edit':
      console.log(curl('POST', '/edit', { path: args[1], content: args[2] }));
      break;
    case 'create':
      console.log(curl('POST', '/create', { path: args[1], content: args[2] }));
      break;
    case 'delete':
      console.log(curl('POST', '/delete', { path: args[1] }));
      break;
    case 'commit':
      console.log(curl('POST', '/commit', { message: args.slice(1).join(' ') }));
      break;
    case 'settings':
      // JSON string
      console.log(curl('POST', '/settings', JSON.parse(args[1])));
      break;
    case 'run':
      console.log(curl('POST', '/run', { command: args[1], args: args.slice(2) }));
      break;
      case 'exec':
        // exec <command> [args...]
        console.log(curl('POST', '/exec', { command: args[1], args: args.slice(2) }));
        break;
      case 'extensions':
        console.log(curl('GET', '/extensions'));
        break;
      case 'experimental':
        // experimental <true|false> <optional JSON array of extension ids>
        const enable = args[1] === 'false' ? false : true;
        const extList = args[2] ? JSON.parse(args[2]) : undefined;
        // Optionally pass 'apply' as third argument (true|false)
        const apply = args[3] === 'true' ? true : false;
        console.log(curl('POST', '/extensions/experimental', { enable, extensions: extList, apply }));
        break;
      case 'yolo':
        // yolo <true|false> [extensions JSON array] [keys JSON array]
        const enable = args[1] === 'false' ? false : true;
        const extList = args[2] ? JSON.parse(args[2]) : undefined;
        const keyList = args[3] ? JSON.parse(args[3]) : undefined;
        const applyY = args[4] === 'true' ? true : false;
        console.log(curl('POST', '/yolo', { enable, extensions: extList, keys: keyList, apply: applyY }));
        break;
      case 'master':
        const en = args[1] === 'false' ? false : true;
        const extL = args[2] ? JSON.parse(args[2]) : undefined;
        const keyL = args[3] ? JSON.parse(args[3]) : undefined;
        const applyM = args[4] === 'true' ? true : false;
        console.log(curl('POST', '/master-approve', { enable: en, extensions: extL, keys: keyL, apply: applyM }));
        break;
    case 'audit':
      // audit [limit|id]
      if (!args[1]) { console.log(curl('GET', '/audit')); break; }
      if (/^[0-9]+$/.test(args[1])) { console.log(curl('GET', `/audit?limit=${args[1]}`)); break; }
      console.log(curl('GET', `/audit?id=${encodeURIComponent(args[1])}`));
      break;
      break;
    case 'rollback':
      // rollback <audit-id>
      console.log(curl('POST', '/rollback', { id: args[1] }));
      break;
    default:
      console.log('Unknown command', cmd);
  }
} catch (e) {
  console.error('Error:', e.message);
}
