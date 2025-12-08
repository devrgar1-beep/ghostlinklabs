# GhostLink Kubernetes Deployment

This directory contains the complete Kubernetes manifests for deploying the GhostLink system to a Kubernetes cluster.

## 🏗️ Architecture

The Kubernetes deployment includes:

- **GhostLink Core**: Main controller service
- **API Server**: REST API with horizontal scaling (2-10 replicas)
- **AI Orchestrator**: Intelligent orchestration service (1-3 replicas)
- **Prometheus**: Metrics collection and monitoring
- **Grafana**: Visualization and dashboards
- **Nginx Load Balancer**: API load balancing and ingress
- **Auto-scaling**: Horizontal Pod Autoscalers for dynamic scaling

## 📁 File Structure

```
k8s/
├── namespace.yaml              # GhostLink namespace
├── configmap.yaml              # Application configuration
├── prometheus-configmap.yaml   # Prometheus configuration
├── autoscaling-configmap.yaml  # Autoscaling rules
├── nginx-configmap.yaml        # Nginx load balancer config
├── persistent-volumes.yaml     # PVCs for storage
├── secrets.yaml                # Secrets for TLS and passwords
├── rbac.yaml                   # RBAC for Prometheus
├── ghostlink-core-deployment.yaml    # Core service deployment
├── ghostlink-api-deployment.yaml     # API server deployment
├── ghostlink-orchestrator-deployment.yaml  # Orchestrator deployment
├── prometheus-deployment.yaml  # Prometheus deployment
├── grafana-deployment.yaml     # Grafana deployment
├── nginx-deployment.yaml       # Nginx load balancer deployment
├── services.yaml               # All service definitions
├── hpa.yaml                    # Horizontal Pod Autoscalers
├── ingress.yaml                # Ingress for external access
└── deploy.sh                   # Deployment script
```

## 🚀 Quick Deployment

### Prerequisites

- Kubernetes cluster (v1.19+)
- `kubectl` configured to access your cluster
- Docker registry access (if using private images)
- Storage class configured for PVCs

### Deploy

```bash
# Make deploy script executable
chmod +x k8s/deploy.sh

# Deploy everything
./k8s/deploy.sh
```

### Manual Deployment

```bash
# Apply in order
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/prometheus-configmap.yaml
kubectl apply -f k8s/autoscaling-configmap.yaml
kubectl apply -f k8s/nginx-configmap.yaml
kubectl apply -f k8s/persistent-volumes.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/rbac.yaml
kubectl apply -f k8s/ghostlink-core-deployment.yaml
kubectl apply -f k8s/ghostlink-api-deployment.yaml
kubectl apply -f k8s/ghostlink-orchestrator-deployment.yaml
kubectl apply -f k8s/prometheus-deployment.yaml
kubectl apply -f k8s/grafana-deployment.yaml
kubectl apply -f k8s/nginx-deployment.yaml
kubectl apply -f k8s/services.yaml
kubectl apply -f k8s/hpa.yaml
kubectl apply -f k8s/ingress.yaml
```

## 🔧 Configuration

### Environment Variables

Key configuration is managed via ConfigMaps:

- `GHOSTLINK_ENV=production`
- `PYTHONPATH=/app`
- `HOST=0.0.0.0`

### Secrets

Update `secrets.yaml` with your actual secrets:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: ghostlink-secrets
  namespace: ghostlink
type: Opaque
data:
  tls.crt: <base64-encoded-cert>
  tls.key: <base64-encoded-key>
  openai-api-key: <base64-encoded-key>
```

### Scaling Configuration

Horizontal Pod Autoscalers are configured for:

- **API Server**: 2-10 replicas, CPU 70%, Memory 80%
- **Orchestrator**: 1-3 replicas, CPU 75%, Memory 85%

## 📊 Monitoring & Access

### Port Forwarding (Development)

```bash
# Grafana
kubectl port-forward -n ghostlink svc/grafana 3000:3000

# Prometheus
kubectl port-forward -n ghostlink svc/prometheus 9090:9090

# API Load Balancer
kubectl port-forward -n ghostlink svc/nginx-load-balancer 80:80
```

### Ingress Access

If using ingress, add to `/etc/hosts`:

```
127.0.0.1 api.ghostlink.local
127.0.0.1 grafana.ghostlink.local
```

### Health Checks

```bash
# Check all pods
kubectl get pods -n ghostlink

# Check services
kubectl get svc -n ghostlink

# Check autoscaling
kubectl get hpa -n ghostlink

# View logs
kubectl logs -n ghostlink deployment/ghostlink-api-prod
```

## 🔄 Scaling Operations

### Manual Scaling

```bash
# Scale API servers
kubectl scale deployment ghostlink-api-prod -n ghostlink --replicas=5

# Scale orchestrator
kubectl scale deployment ghostlink-orchestrator-prod -n ghostlink --replicas=2
```

### Auto-scaling Monitoring

```bash
# View scaling status
kubectl describe hpa ghostlink-api-hpa -n ghostlink

# Check resource usage
kubectl top pods -n ghostlink
```

## 🐛 Troubleshooting

### Common Issues

1. **PVC Pending**: Check storage class availability

   ```bash
   kubectl get storageclass
   ```

2. **Pod CrashLoopBackOff**: Check logs

   ```bash
   kubectl logs -n ghostlink <pod-name> --previous
   ```

3. **Service Not Accessible**: Check endpoints

   ```bash
   kubectl get endpoints -n ghostlink
   ```

4. **Auto-scaling Not Working**: Verify metrics server

   ```bash
   kubectl get apiservice v1beta1.metrics.k8s.io
   ```

### Logs and Debugging

```bash
# All pod logs
kubectl logs -n ghostlink -l app=ghostlink-api --tail=100

# Follow logs
kubectl logs -n ghostlink deployment/ghostlink-api-prod -f

# Debug pod
kubectl exec -it -n ghostlink <pod-name> -- /bin/bash
```

## 🔒 Security Considerations

- RBAC is configured for Prometheus access
- Non-root user (10001) for GhostLink containers
- Security headers in Nginx configuration
- Secrets management for sensitive data
- Network policies recommended for production

## 📈 Performance Tuning

### Resource Limits

Current resource allocations:

- API Server: 500m-1 CPU, 512Mi-1Gi RAM
- Orchestrator: 1-2 CPU, 2-4Gi RAM
- Prometheus: 100m-500m CPU, 512Mi-2Gi RAM
- Grafana: 100m-500m CPU, 256Mi-1Gi RAM

### Storage

- Prometheus: 50Gi for metrics retention
- Grafana: 10Gi for dashboards and data
- Logs/Data: 20Gi/100Gi shared volumes

## 🔄 Updates and Rollbacks

### Rolling Updates

```bash
# Update deployment image
kubectl set image deployment/ghostlink-api-prod api-server=ghostlink:latest -n ghostlink

# Check rollout status
kubectl rollout status deployment/ghostlink-api-prod -n ghostlink
```

### Rollbacks

```bash
# Rollback deployment
kubectl rollout undo deployment/ghostlink-api-prod -n ghostlink

# Check revision history
kubectl rollout history deployment/ghostlink-api-prod -n ghostlink
```

## 📚 Additional Resources

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Prometheus Kubernetes Guide](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#kubernetes-sd-configurations)
- [Grafana Kubernetes](https://grafana.com/docs/grafana/latest/setup-grafana/installation/kubernetes/)
- [Nginx Ingress Controller](https://kubernetes.github.io/ingress-nginx/)

---

**Deployment Date:** December 8, 2025
**Version:** v1.0.0
**Status:** Production Ready
