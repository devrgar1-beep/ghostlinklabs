# GhostLink Helm Chart

A comprehensive Helm chart for deploying the GhostLink AI orchestration platform on Kubernetes with production-grade monitoring, scaling, and security features.

## 🚀 Quick Start

### Prerequisites

- Kubernetes 1.19+
- Helm 3.0+
- Metrics Server (for HPA)
- Storage class configured

### Install

```bash
# Add the repository (if hosted)
helm repo add ghostlink https://charts.ghostlinklabs.com
helm repo update

# Install the chart
helm install ghostlink ./helm

# Or install from repository
helm install ghostlink ghostlink/ghostlink
```

### Access

```bash
# Get service URLs
kubectl get svc -n ghostlink

# Port forward for local access
kubectl port-forward -n ghostlink svc/ghostlink-nginx 80:80
kubectl port-forward -n ghostlink svc/grafana 3000:3000
```

## 📋 Chart Components

### Core Services

- **GhostLink Core**: Main controller service
- **API Server**: REST API with horizontal scaling (2-10 replicas)
- **AI Orchestrator**: Intelligent orchestration (1-3 replicas)

### Monitoring Stack

- **Prometheus**: Metrics collection and alerting
- **Grafana**: Visualization dashboards
- **Nginx**: Load balancer and ingress

### Infrastructure

- **Persistent Volumes**: Storage for logs, data, and monitoring
- **Horizontal Pod Autoscalers**: Auto-scaling based on CPU/memory
- **ConfigMaps**: Application configuration
- **Secrets**: TLS certificates and API keys

## 🔧 Configuration

### Global Settings

| Parameter | Description | Default |
|-----------|-------------|---------|
| `global.imageRegistry` | Global Docker image registry | `""` |
| `global.imagePullSecrets` | Global Docker registry secret names | `[]` |
| `global.storageClass` | Global storage class for PVCs | `""` |

### API Server Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `apiServer.enabled` | Enable API server | `true` |
| `apiServer.replicaCount` | Number of API server replicas | `2` |
| `apiServer.image.repository` | API server image repository | `ghostlink` |
| `apiServer.image.tag` | API server image tag | `"latest"` |
| `apiServer.service.port` | API server port | `3000` |
| `apiServer.resources.limits.cpu` | CPU limit | `1000m` |
| `apiServer.resources.limits.memory` | Memory limit | `1Gi` |
| `apiServer.autoscaling.enabled` | Enable HPA | `true` |
| `apiServer.autoscaling.minReplicas` | Minimum replicas | `2` |
| `apiServer.autoscaling.maxReplicas` | Maximum replicas | `10` |

### Orchestrator Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `orchestrator.enabled` | Enable orchestrator | `true` |
| `orchestrator.replicaCount` | Number of orchestrator replicas | `1` |
| `orchestrator.autoscaling.enabled` | Enable HPA | `true` |
| `orchestrator.autoscaling.maxReplicas` | Maximum replicas | `3` |

### Monitoring Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `prometheus.enabled` | Enable Prometheus | `true` |
| `prometheus.persistence.size` | Prometheus storage size | `50Gi` |
| `grafana.enabled` | Enable Grafana | `true` |
| `grafana.adminPassword` | Grafana admin password | `ghostlink2025` |
| `grafana.persistence.size` | Grafana storage size | `10Gi` |

### Storage Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `storage.logs.enabled` | Enable logs PVC | `true` |
| `storage.logs.size` | Logs storage size | `20Gi` |
| `storage.data.enabled` | Enable data PVC | `true` |
| `storage.data.size` | Data storage size | `100Gi` |

### Ingress Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `ingress.enabled` | Enable ingress | `true` |
| `ingress.className` | Ingress class | `"nginx"` |
| `ingress.hosts[0].host` | API hostname | `api.ghostlink.local` |
| `ingress.hosts[1].host` | Grafana hostname | `grafana.ghostlink.local` |

## 📊 Scaling Behavior

### API Server Scaling

- **Min Replicas**: 2
- **Max Replicas**: 10
- **Scale Up**: CPU > 70% or Memory > 80%
- **Scale Down**: CPU < 20% and Memory < 30% for 15min

### Orchestrator Scaling

- **Min Replicas**: 1
- **Max Replicas**: 3
- **Scale Up**: CPU > 75% or Memory > 85%
- **Scale Down**: CPU < 25% and Memory < 40% for 15min

## 🔒 Security

### TLS Configuration

```yaml
secrets:
  tls:
    enabled: true
    cert: <base64-encoded-cert>
    key: <base64-encoded-key>
```

### API Keys

```yaml
secrets:
  apiKeys:
    enabled: true
    openai: <base64-encoded-key>
    anthropic: <base64-encoded-key>
```

### RBAC

The chart creates necessary RBAC resources for Prometheus to access Kubernetes metrics.

## 📈 Monitoring

### Dashboards

Access Grafana at `http://grafana.ghostlink.local` (admin/ghostlink2025)

### Metrics

- **API Server**: Request latency, throughput, error rates
- **Orchestrator**: AI processing metrics, queue depth
- **Infrastructure**: CPU, memory, disk, network usage

### Alerts

Pre-configured alerts for:

- High CPU/memory usage
- Slow response times
- Service availability
- Storage capacity

## 🔄 Upgrades

```bash
# Upgrade the release
helm upgrade ghostlink ./helm

# Check release status
helm status ghostlink

# Rollback if needed
helm rollback ghostlink
```

## 🐛 Troubleshooting

### Common Issues

1. **PVC Pending**

   ```bash
   kubectl get pvc -n ghostlink
   kubectl describe pvc <pvc-name> -n ghostlink
   ```

2. **Pod CrashLoopBackOff**

   ```bash
   kubectl logs -n ghostlink <pod-name> --previous
   ```

3. **Service Not Accessible**

   ```bash
   kubectl get endpoints -n ghostlink
   ```

4. **Auto-scaling Not Working**

   ```bash
   kubectl get apiservice v1beta1.metrics.k8s.io
   kubectl get hpa -n ghostlink
   ```

### Logs

```bash
# API server logs
kubectl logs -n ghostlink -l app.kubernetes.io/component=api-server

# Orchestrator logs
kubectl logs -n ghostlink -l app.kubernetes.io/component=orchestrator

# All component logs
kubectl logs -n ghostlink -l app.kubernetes.io/name=ghostlink
```

## 📚 Examples

### Development Deployment

```yaml
# values-dev.yaml
apiServer:
  replicaCount: 1
  autoscaling:
    enabled: false

orchestrator:
  replicaCount: 1
  autoscaling:
    enabled: false

ingress:
  enabled: false

prometheus:
  persistence:
    size: 10Gi

grafana:
  persistence:
    size: 5Gi
```

```bash
helm install ghostlink-dev ./helm -f values-dev.yaml
```

### Production Deployment

```yaml
# values-prod.yaml
global:
  imageRegistry: "your-registry.com/"
  storageClass: "fast-ssd"

apiServer:
  replicaCount: 3
  resources:
    limits:
      cpu: "2000m"
      memory: "2Gi"

ingress:
  hosts:
    - host: api.production.com
      paths:
        - path: /
    - host: grafana.production.com
      paths:
        - path: /

secrets:
  tls:
    enabled: true
    cert: <prod-cert>
    key: <prod-key>
```

```bash
helm install ghostlink-prod ./helm -f values-prod.yaml
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes
4. Test with `helm template`
5. Submit a pull request

## 📄 License

This chart is licensed under the MIT License.

---

**Chart Version:** 1.0.0
**App Version:** 1.0.0
**Kubernetes:** 1.19+
**Helm:** 3.0+
