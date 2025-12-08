#!/bin/bash
# GhostLink Kubernetes Deployment Script
# This script deploys the complete GhostLink system to Kubernetes

set -e

echo "🚀 Deploying GhostLink to Kubernetes..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}❌ kubectl not found. Please install kubectl first.${NC}"
    exit 1
fi

# Check if connected to a cluster
if ! kubectl cluster-info &> /dev/null; then
    echo -e "${RED}❌ Not connected to a Kubernetes cluster.${NC}"
    exit 1
fi

echo -e "${YELLOW}📦 Creating namespace...${NC}"
kubectl apply -f k8s/namespace.yaml

echo -e "${YELLOW}🔧 Creating ConfigMaps...${NC}"
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/prometheus-configmap.yaml
kubectl apply -f k8s/autoscaling-configmap.yaml
kubectl apply -f k8s/nginx-configmap.yaml

echo -e "${YELLOW}💾 Creating Persistent Volumes...${NC}"
kubectl apply -f k8s/persistent-volumes.yaml

echo -e "${YELLOW}🔐 Creating Secrets...${NC}"
kubectl apply -f k8s/secrets.yaml

echo -e "${YELLOW}🔒 Setting up RBAC...${NC}"
kubectl apply -f k8s/rbac.yaml

echo -e "${YELLOW}🚀 Deploying core services...${NC}"
kubectl apply -f k8s/ghostlink-core-deployment.yaml
kubectl apply -f k8s/ghostlink-api-deployment.yaml
kubectl apply -f k8s/ghostlink-orchestrator-deployment.yaml

echo -e "${YELLOW}📊 Deploying monitoring stack...${NC}"
kubectl apply -f k8s/prometheus-deployment.yaml
kubectl apply -f k8s/grafana-deployment.yaml

echo -e "${YELLOW}⚖️ Deploying load balancer...${NC}"
kubectl apply -f k8s/nginx-deployment.yaml

echo -e "${YELLOW}🌐 Creating Services...${NC}"
kubectl apply -f k8s/services.yaml

echo -e "${YELLOW}📈 Setting up auto-scaling...${NC}"
kubectl apply -f k8s/hpa.yaml

echo -e "${YELLOW}🚪 Creating Ingress...${NC}"
kubectl apply -f k8s/ingress.yaml

echo -e "${GREEN}✅ Deployment complete!${NC}"
echo ""
echo -e "${GREEN}📋 Next steps:${NC}"
echo "1. Check pod status: kubectl get pods -n ghostlink"
echo "2. Check services: kubectl get svc -n ghostlink"
echo "3. Access Grafana: kubectl port-forward -n ghostlink svc/grafana 3000:3000"
echo "4. Access API: kubectl port-forward -n ghostlink svc/nginx-load-balancer 80:80"
echo "5. Monitor scaling: kubectl get hpa -n ghostlink"
echo ""
echo -e "${YELLOW}⚠️  Note: Update DNS or /etc/hosts for ingress domains${NC}"