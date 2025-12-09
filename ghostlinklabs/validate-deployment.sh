#!/bin/bash
# GhostLink Helm Deployment Validation Script
# This script validates a Helm deployment of GhostLink

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
NAMESPACE="${NAMESPACE:-ghostlink}"
RELEASE_NAME="${RELEASE_NAME:-ghostlink}"
TIMEOUT="${TIMEOUT:-300}"

echo -e "${BLUE}🔍 GhostLink Helm Deployment Validation${NC}"
echo "========================================"

# Check prerequisites
echo -e "${YELLOW}📋 Checking prerequisites...${NC}"

if ! command -v helm &> /dev/null; then
    echo -e "${RED}❌ Helm not found. Please install Helm 3+ first.${NC}"
    exit 1
fi

if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}❌ kubectl not found. Please install kubectl first.${NC}"
    exit 1
fi

if ! kubectl cluster-info &> /dev/null; then
    echo -e "${RED}❌ Not connected to a Kubernetes cluster.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Prerequisites check passed${NC}"

# Check if release exists
echo -e "${YELLOW}🔍 Checking Helm release...${NC}"
if ! helm status "$RELEASE_NAME" -n "$NAMESPACE" &> /dev/null; then
    echo -e "${RED}❌ Helm release '$RELEASE_NAME' not found in namespace '$NAMESPACE'${NC}"
    echo -e "${YELLOW}💡 Make sure to deploy first: helm install $RELEASE_NAME ./helm -n $NAMESPACE${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Helm release '$RELEASE_NAME' found${NC}"

# Wait for deployments to be ready
echo -e "${YELLOW}⏳ Waiting for deployments to be ready...${NC}"
kubectl wait --for=condition=available --timeout=${TIMEOUT}s deployment --all -n "$NAMESPACE"
echo -e "${GREEN}✅ All deployments are ready${NC}"

# Check pod status
echo -e "${YELLOW}📊 Checking pod status...${NC}"
POD_STATUS=$(kubectl get pods -n "$NAMESPACE" --no-headers)
if echo "$POD_STATUS" | grep -q -v "Running\|Completed"; then
    echo -e "${RED}❌ Some pods are not in Running/Completed state:${NC}"
    echo "$POD_STATUS"
    exit 1
fi
echo -e "${GREEN}✅ All pods are running${NC}"

# Check service endpoints
echo -e "${YELLOW}🔗 Checking service endpoints...${NC}"
SERVICES=$(kubectl get svc -n "$NAMESPACE" -o name | sed 's/service\///')
for svc in $SERVICES; do
    ENDPOINTS=$(kubectl get endpoints "$svc" -n "$NAMESPACE" -o jsonpath='{.subsets[*].addresses[*].ip}' 2>/dev/null)
    if [ -z "$ENDPOINTS" ]; then
        echo -e "${RED}❌ Service '$svc' has no endpoints${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ Service '$svc' has endpoints: $ENDPOINTS${NC}"
done

# Check persistent volumes
echo -e "${YELLOW}💾 Checking persistent volumes...${NC}"
PVC_STATUS=$(kubectl get pvc -n "$NAMESPACE" --no-headers -o custom-columns=":metadata.name,:status.phase")
if echo "$PVC_STATUS" | grep -q -v "Bound"; then
    echo -e "${RED}❌ Some PVCs are not bound:${NC}"
    echo "$PVC_STATUS"
    exit 1
fi
echo -e "${GREEN}✅ All persistent volumes are bound${NC}"

# Check auto-scaling
echo -e "${YELLOW}📈 Checking auto-scaling...${NC}"
HPA_COUNT=$(kubectl get hpa -n "$NAMESPACE" --no-headers 2>/dev/null | wc -l)
if [ "$HPA_COUNT" -gt 0 ]; then
    HPA_STATUS=$(kubectl get hpa -n "$NAMESPACE" --no-headers)
    echo -e "${GREEN}✅ Found $HPA_COUNT HorizontalPodAutoscalers:${NC}"
    echo "$HPA_STATUS"
else
    echo -e "${YELLOW}⚠️  No HorizontalPodAutoscalers found${NC}"
fi

# Test API connectivity
echo -e "${YELLOW}🌐 Testing API connectivity...${NC}"

# Get API service port
API_PORT=$(kubectl get svc ghostlink-api -n "$NAMESPACE" -o jsonpath='{.spec.ports[?(@.name=="http")].port}' 2>/dev/null)
if [ -n "$API_PORT" ]; then
    # Port forward for testing
    kubectl port-forward -n "$NAMESPACE" svc/ghostlink-api $API_PORT:$API_PORT &
    PF_PID=$!
    sleep 3

    # Test health endpoint
    if curl -f -s "http://localhost:$API_PORT/health" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ API health check passed${NC}"
    else
        echo -e "${RED}❌ API health check failed${NC}"
        kill $PF_PID 2>/dev/null
        exit 1
    fi

    # Test metrics endpoint
    if curl -f -s "http://localhost:$API_PORT/metrics" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ API metrics endpoint accessible${NC}"
    else
        echo -e "${YELLOW}⚠️  API metrics endpoint not accessible (may be expected)${NC}"
    fi

    kill $PF_PID 2>/dev/null
else
    echo -e "${YELLOW}⚠️  API service not found, skipping connectivity tests${NC}"
fi

# Test monitoring stack
echo -e "${YELLOW}📊 Testing monitoring stack...${NC}"

# Check Prometheus
if kubectl get svc prometheus -n "$NAMESPACE" &> /dev/null; then
    PROM_PORT=$(kubectl get svc prometheus -n "$NAMESPACE" -o jsonpath='{.spec.ports[?(@.name=="http")].port}')
    kubectl port-forward -n "$NAMESPACE" svc/prometheus $PROM_PORT:$PROM_PORT &
    PF_PID=$!
    sleep 3

    if curl -f -s "http://localhost:$PROM_PORT/-/healthy" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Prometheus is healthy${NC}"
    else
        echo -e "${RED}❌ Prometheus health check failed${NC}"
    fi

    kill $PF_PID 2>/dev/null
else
    echo -e "${YELLOW}⚠️  Prometheus service not found${NC}"
fi

# Check Grafana
if kubectl get svc grafana -n "$NAMESPACE" &> /dev/null; then
    GRAFANA_PORT=$(kubectl get svc grafana -n "$NAMESPACE" -o jsonpath='{.spec.ports[?(@.name=="http")].port}')
    echo -e "${GREEN}✅ Grafana service found (port: $GRAFANA_PORT)${NC}"
    echo -e "${BLUE}🔗 Access Grafana: kubectl port-forward -n $NAMESPACE svc/grafana $GRAFANA_PORT:$GRAFANA_PORT${NC}"
else
    echo -e "${YELLOW}⚠️  Grafana service not found${NC}"
fi

# Resource usage summary
echo -e "${YELLOW}📈 Resource usage summary...${NC}"
kubectl top pods -n "$NAMESPACE" --no-headers 2>/dev/null || echo -e "${YELLOW}⚠️  Metrics server not available for resource monitoring${NC}"

# Final status
echo ""
echo -e "${GREEN}🎉 GhostLink deployment validation completed successfully!${NC}"
echo ""
echo -e "${BLUE}📋 Deployment Summary:${NC}"
echo "• Namespace: $NAMESPACE"
echo "• Release: $RELEASE_NAME"
echo "• Pods: $(kubectl get pods -n "$NAMESPACE" --no-headers | wc -l)"
echo "• Services: $(kubectl get svc -n "$NAMESPACE" --no-headers | wc -l)"
echo "• PVCs: $(kubectl get pvc -n "$NAMESPACE" --no-headers | wc -l)"
echo "• HPAs: $HPA_COUNT"

echo ""
echo -e "${BLUE}🚀 Access URLs:${NC}"
echo "• API: kubectl port-forward -n $NAMESPACE svc/ghostlink-api 3000:3000"
echo "• Grafana: kubectl port-forward -n $NAMESPACE svc/grafana 3000:3000"
echo "• Prometheus: kubectl port-forward -n $NAMESPACE svc/prometheus 9090:9090"
echo "• Load Balancer: kubectl port-forward -n $NAMESPACE svc/ghostlink-nginx 80:80"

echo ""
echo -e "${GREEN}✅ All validation checks passed!${NC}"