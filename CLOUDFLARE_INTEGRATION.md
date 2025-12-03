# Cloudflare Integration for GhostLink

## Overview

GhostLink now includes comprehensive Cloudflare integration for deploying edge virtual machines and leveraging Cloudflare's global network for improved performance and security.

## Configuration

Set the following environment variables to enable Cloudflare integration:

```bash
export CLOUDFLARE_API_TOKEN="your_api_token_here"
export CLOUDFLARE_ACCOUNT_ID="your_account_id_here"
export CLOUDFLARE_ZONE_ID="your_zone_id_here"
```

## Features

### Edge Virtual Machines
- **Cloudflare Workers**: Serverless functions running at the edge
- **Cloudflare Pages**: Static site hosting with edge computing
- **KV Namespaces**: Global key-value storage
- **Durable Objects**: Consistent storage and coordination

### CLI Commands

#### Check Cloudflare Status
```bash
python ghostlink_root_control.py cloudflare-status
```

#### Deploy GhostLink to Edge
```bash
python ghostlink_root_control.py deploy-edge
```

#### Deploy Individual Worker
```bash
python ghostlink_root_control.py deploy-worker --name my-worker --file worker.js
```

#### Create KV Namespace
```bash
python ghostlink_root_control.py create-kv-namespace --title my-namespace
```

## Architecture

### Edge Components
1. **API Worker**: Handles API requests at the edge
2. **Auth Worker**: Manages authentication and authorization
3. **KV Namespaces**: Store session data, cache, and configuration
4. **Pages**: Frontend deployment (future)

### Deployment Process
1. Validate Cloudflare credentials
2. Deploy API and Auth workers
3. Create necessary KV namespaces
4. Configure routing and security rules
5. Update DNS and CDN settings

## Security

- API tokens are stored securely via environment variables
- Workers run in isolated environments
- All edge communications use HTTPS
- Rate limiting and DDoS protection via Cloudflare

## Monitoring

Edge deployments are monitored through:
- Cloudflare dashboard
- Worker analytics
- Real-time logs
- Performance metrics

## Getting Started

1. Create a Cloudflare account
2. Generate an API token with Workers and KV permissions
3. Set environment variables
4. Run `python ghostlink_root_control.py deploy-edge`

## Troubleshooting

### Common Issues
- **API Token Invalid**: Check token permissions and expiration
- **Account/Zone Access**: Verify account and zone IDs
- **Deployment Failures**: Check worker script syntax
- **KV Namespace Errors**: Ensure unique namespace titles

### Logs
Check Cloudflare dashboard for detailed logs and error messages.