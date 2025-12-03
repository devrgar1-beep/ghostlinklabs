# GHOSTLINK PROTOCOL: COMPREHENSIVE TECHNICAL WIKI
# PART 8: TESTING, DEPLOYMENT & OPERATIONS

**Version:** 2.1.0 | **Classification:** Production Operations

---

# 30. TESTING FRAMEWORK

## 30.1 Test Categories

```yaml
test_categories:
  unit_tests:
    coverage_target: 90%
    frameworks: [pytest, jest]
    components:
      - Core types and data structures
      - FCC lattice algorithms
      - CMFL phase functions
      - Pheromone calculations
      - GhostSlang encoding/decoding
      
  integration_tests:
    coverage_target: 80%
    components:
      - Provider orchestration
      - Multi-agent routing
      - Pipeline execution
      - Storage operations
      - Event logging
      
  end_to_end_tests:
    coverage_target: 70%
    scenarios:
      - Complete CMFL cycle
      - Variance analysis flow
      - SCAR recovery
      - Multi-provider failover
      
  performance_tests:
    benchmarks:
      - Query latency percentiles
      - Throughput under load
      - Memory utilization
      - Provider response aggregation
      
  chaos_tests:
    scenarios:
      - Agent failures (1-8 agents)
      - Provider outages
      - Network partitions
      - Resource exhaustion
```

## 30.2 Unit Test Examples

```python
# tests/unit/test_lattice.py

import pytest
from ghostlink.core.lattice import FCCLattice
from ghostlink.core.types import Position3D, AgentGroup


class TestFCCLattice:
    """Unit tests for FCC lattice implementation."""
    
    @pytest.fixture
    def lattice(self):
        return FCCLattice(size=4)
    
    def test_initialization(self, lattice):
        """Test lattice initializes with correct agent count."""
        assert lattice.total_agents == 64
        assert len(lattice.positions) == 64
        assert len(lattice.adjacency) == 64
    
    def test_neighbor_count(self, lattice):
        """Each agent should have exactly 12 neighbors (FCC coordination)."""
        for agent_id in range(1, 65):
            neighbors = lattice.get_neighbors(agent_id)
            assert len(neighbors) == 12, f"Agent {agent_id} has {len(neighbors)} neighbors"
    
    def test_neighbor_symmetry(self, lattice):
        """If A neighbors B, then B neighbors A."""
        for agent_id in range(1, 65):
            for neighbor in lattice.get_neighbors(agent_id):
                assert agent_id in lattice.get_neighbors(neighbor)
    
    def test_routing_same_agent(self, lattice):
        """Route from agent to itself should be single-element list."""
        for agent_id in [1, 32, 64]:
            path = lattice.route(agent_id, agent_id)
            assert path == [agent_id]
    
    def test_routing_max_distance(self, lattice):
        """No route should exceed 6 hops in 4x4x4 FCC."""
        test_pairs = [(1, 64), (1, 37), (8, 57)]
        for source, target in test_pairs:
            path = lattice.route(source, target)
            assert len(path) <= 7
    
    def test_fault_tolerance_single(self, lattice):
        """System should remain connected with 1 agent failure."""
        for failed in range(1, 65):
            assert lattice.verify_fault_tolerance([failed])
    
    def test_fault_tolerance_max(self, lattice):
        """System should handle up to 8 failures."""
        failed = list(range(1, 9))
        assert lattice.verify_fault_tolerance(failed)
    
    def test_group_assignment(self, lattice):
        """Verify correct group assignments."""
        assert lattice.get_group(1) == AgentGroup.ALPHA
        assert lattice.get_group(8) == AgentGroup.ALPHA
        assert lattice.get_group(9) == AgentGroup.BETA
        assert lattice.get_group(64) == AgentGroup.THETA


# tests/unit/test_pheromones.py

import pytest
from datetime import datetime
from ghostlink.coordination.pheromones import PheromoneMap
from ghostlink.core.types import Position3D


class TestPheromoneMap:
    """Unit tests for pheromone coordination system."""
    
    @pytest.fixture
    def pheromone_map(self):
        return PheromoneMap()
    
    def test_deposit_and_read(self, pheromone_map):
        """Test basic deposit and read operations."""
        pos = Position3D(0, 0, 0)
        pheromone_map.deposit("quality", pos, 10.0, depositor_id=1)
        strength = pheromone_map.read("quality", pos)
        assert strength > 9.9
    
    def test_amplification(self, pheromone_map):
        """Multiple deposits should amplify strength."""
        pos = Position3D(1, 1, 1)
        pheromone_map.deposit("quality", pos, 10.0, depositor_id=1)
        pheromone_map.deposit("quality", pos, 10.0, depositor_id=2)
        strength = pheromone_map.read("quality", pos)
        assert strength > 20.0
    
    def test_different_types_independent(self, pheromone_map):
        """Different pheromone types should be independent."""
        pos = Position3D(2, 2, 2)
        pheromone_map.deposit("quality", pos, 10.0, depositor_id=1)
        pheromone_map.deposit("error", pos, 5.0, depositor_id=1)
        assert pheromone_map.read("quality", pos) > 9.0
        assert pheromone_map.read("error", pos) > 4.0
        assert pheromone_map.read("task", pos) == 0.0
    
    def test_evaporation(self, pheromone_map):
        """Evaporation should remove weak deposits."""
        pos = Position3D(3, 3, 3)
        pheromone_map.deposit("quality", pos, 0.001, depositor_id=1)
        removed = pheromone_map.evaporate()
        assert removed >= 1
```

## 30.3 Integration Tests

```python
# tests/integration/test_variance_analysis.py

import pytest
from ghostlink.analysis.variance import VarianceAnalyzer
from ghostlink.core.types import ProviderResponse


class TestVarianceAnalysisIntegration:
    """Integration tests for variance analysis flow."""
    
    @pytest.fixture
    def mock_responses(self):
        return [
            ProviderResponse(
                provider="openai", model="gpt-4",
                content="The capital of France is Paris.",
                tokens_used=20, latency_ms=500
            ),
            ProviderResponse(
                provider="anthropic", model="claude-3",
                content="Paris is the capital city of France.",
                tokens_used=22, latency_ms=450
            ),
            ProviderResponse(
                provider="google", model="gemini",
                content="France's capital is Paris.",
                tokens_used=18, latency_ms=480
            )
        ]
    
    def test_high_agreement_analysis(self, mock_responses):
        """Test analysis when responses highly agree."""
        analyzer = VarianceAnalyzer()
        analysis = analyzer.analyze(mock_responses)
        
        assert analysis.metrics.semantic_variance < 0.3
        assert analysis.metrics.factual_agreement > 0.7
        assert analysis.confidence_score > 0.7
    
    def test_divergent_responses(self):
        """Test analysis when responses disagree."""
        divergent_responses = [
            ProviderResponse(
                provider="openai", model="gpt-4",
                content="The answer is definitely 42.",
                tokens_used=15, latency_ms=500
            ),
            ProviderResponse(
                provider="anthropic", model="claude-3",
                content="The answer is approximately 100.",
                tokens_used=15, latency_ms=450
            ),
            ProviderResponse(
                provider="google", model="gemini",
                content="There is no definitive answer.",
                tokens_used=20, latency_ms=480
            )
        ]
        
        analyzer = VarianceAnalyzer()
        analysis = analyzer.analyze(divergent_responses)
        
        assert analysis.metrics.semantic_variance > 0.3
        assert analysis.confidence_score < 0.7
```

## 30.4 Performance Benchmarks

```python
# tests/performance/test_benchmarks.py

import pytest
import asyncio
import time
import statistics
from ghostlink.core.cmfl import CMFLEngine
from ghostlink.core.types import Query


class TestPerformanceBenchmarks:
    """Performance benchmark tests."""
    
    @pytest.fixture
    def cmfl_engine(self, tmp_path):
        from ghostlink.analysis.domains import DomainRegistry
        from ghostlink.storage.content_addressed import ContentStore
        from ghostlink.storage.events import EventLog
        
        return CMFLEngine(
            domain_registry=DomainRegistry(),
            content_store=ContentStore(str(tmp_path / "content")),
            event_log=EventLog(str(tmp_path / "events"))
        )
    
    @pytest.mark.asyncio
    async def test_cmfl_latency_simple(self, cmfl_engine):
        """Benchmark CMFL latency for simple queries."""
        query = Query(text="Hello world")
        
        latencies = []
        for _ in range(100):
            start = time.perf_counter()
            await cmfl_engine.execute(query)
            latencies.append((time.perf_counter() - start) * 1000)
        
        p50 = statistics.median(latencies)
        p99 = statistics.quantiles(latencies, n=100)[98]
        
        assert p50 < 100   # p50 under 100ms
        assert p99 < 500   # p99 under 500ms
    
    @pytest.mark.asyncio
    async def test_cmfl_throughput(self, cmfl_engine):
        """Benchmark CMFL throughput."""
        queries = [Query(text=f"Query {i}") for i in range(100)]
        
        start = time.perf_counter()
        await asyncio.gather(*[cmfl_engine.execute(q) for q in queries])
        duration = time.perf_counter() - start
        
        qps = len(queries) / duration
        assert qps > 10  # At least 10 QPS
```

---

# 31. DEPLOYMENT GUIDE

## 31.1 Docker Compose Production

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  ghostlink-api:
    build:
      context: .
      dockerfile: Dockerfile.prod
    image: ghostlink-api:${VERSION:-latest}
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
      - DATABASE_URL=postgresql://ghost:${DB_PASSWORD}@db:5432/ghostlink
      - REDIS_URL=redis://redis:6379
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '2'
          memory: 4G

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=ghost
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=ghostlink
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ghost -d ghostlink"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}

volumes:
  postgres_data:
  redis_data:
```

## 31.2 Kubernetes Deployment

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ghostlink-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ghostlink
  template:
    metadata:
      labels:
        app: ghostlink
    spec:
      containers:
      - name: ghostlink-api
        image: ghostlink-api:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ghostlink-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ghostlink-api
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

---

# 32. OPERATIONAL PROCEDURES

## 32.1 Daily Operations Checklist

```yaml
daily_checklist:
  morning:
    - Check system health dashboard
    - Review overnight alerts
    - Verify provider health status
    - Check SCAR generation rate
    - Review error logs for patterns
    
  continuous:
    - Monitor query latency percentiles
    - Watch provider error rates
    - Track variance confidence scores
    - Observe pheromone state
    
  evening:
    - Generate daily summary report
    - Archive trace logs
    - Trigger pheromone evaporation
    - Verify backup completion
```

## 32.2 Incident Severity Matrix

```yaml
severity_matrix:
  P1_critical:
    definition: "Complete system outage or data loss risk"
    response_time: "5 minutes"
    escalation: "Immediate to on-call lead"
    
  P2_high:
    definition: "Major functionality degraded"
    response_time: "15 minutes"
    escalation: "Within 1 hour if not resolved"
    
  P3_medium:
    definition: "Minor functionality affected"
    response_time: "1 hour"
    escalation: "Next business day if not resolved"
    
  P4_low:
    definition: "Cosmetic or informational"
    response_time: "Best effort"
```

## 32.3 Runbook: Provider Failover

```yaml
runbook: provider_failover
trigger: Provider health check fails 3 consecutive times
severity: P2

steps:
  - name: Confirm failure
    action: curl -f https://api.openai.com/v1/models
    expected: Non-200 response
    
  - name: Update provider status
    action: ghostlink provider disable openai --reason "Health check failure"
    verify: Provider marked as unhealthy
    
  - name: Verify minimum providers
    action: ghostlink status providers --healthy-only | wc -l
    expected: ">= 3 healthy providers"
    if_failed: "Escalate to P1"
    
  - name: Increase rate limits on remaining
    action: |
      ghostlink config set rate_limit.anthropic 15
      ghostlink config set rate_limit.google 15
      
  - name: Monitor for 15 minutes
    action: ghostlink monitor --duration 15m --metrics latency,errors
    expected: "No degradation in p99 latency"
    
  - name: Document incident
    action: ghostlink incident create --severity P2 --title "Provider failover"

recovery:
  - name: Detect provider recovery
    trigger: Health check succeeds 3 consecutive times
    
  - name: Re-enable provider
    action: ghostlink provider enable openai
    
  - name: Reset rate limits
    action: ghostlink config reset rate_limits
```

## 32.4 Runbook: High Latency Response

```yaml
runbook: high_latency_response
trigger: cmfl_cycle_duration_p99 > 5000ms for 5 minutes
severity: P2

diagnosis:
  - Identify bottleneck phase (COLLAPSE/MIRROR/FORGE/LINK)
  - Check provider latencies
  - Check resource utilization

mitigation:
  provider_bottleneck:
    - Reduce provider timeout
    - Increase parallelization
    - Disable slowest provider
    
  resource_bottleneck:
    - Scale up replicas
    - Increase resource limits
    - Enable aggressive caching

steps:
  - name: Enable fast mode
    action: ghostlink config set mode fast
    effect: "Reduces shard count, increases parallelization"
    
  - name: Monitor improvement
    action: ghostlink monitor --duration 10m --metrics latency
    expected: "p99 < 5000ms"
    
  - name: If not improved, scale
    action: kubectl scale deployment ghostlink-api --replicas=5
```

---

# 33. MONITORING CONFIGURATION

## 33.1 Prometheus Alert Rules

```yaml
# alerts.yml
groups:
  - name: ghostlink_critical
    rules:
      - alert: SystemDown
        expr: up{job="ghostlink-api"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "GhostLink API is down"
          
      - alert: AllProvidersUnhealthy
        expr: ghostlink_healthy_providers == 0
        for: 30s
        labels:
          severity: critical
          
      - alert: HighErrorRate
        expr: rate(ghostlink_errors_total[5m]) / rate(ghostlink_requests_total[5m]) > 0.1
        for: 5m
        labels:
          severity: critical
          
  - name: ghostlink_warning
    rules:
      - alert: HighLatency
        expr: histogram_quantile(0.99, rate(ghostlink_cmfl_duration_seconds_bucket[5m])) > 5
        for: 5m
        labels:
          severity: warning
          
      - alert: SCARRateHigh
        expr: rate(ghostlink_scar_total[5m]) > 0.1
        for: 5m
        labels:
          severity: warning
```

---

# 34. APPENDICES

## Appendix A: Environment Variables

```bash
# .env.example

# === Required ===
DATABASE_URL=postgresql://ghost:password@localhost:5432/ghostlink
REDIS_URL=redis://localhost:6379

# AI Provider Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...

# Security
JWT_SECRET=<random-32-char-string>

# === Optional ===
ENVIRONMENT=development
LOG_LEVEL=INFO
MAX_WORKERS=4
PROVIDER_TIMEOUT=30
CMFL_TIMEOUT=60
ENABLE_CACHING=true
ENABLE_TRACING=true
```

## Appendix B: CLI Reference

```bash
# GhostLink CLI Reference

# System Status
ghostlink status                    # Overall system status
ghostlink status agents             # Agent health
ghostlink status providers          # Provider health

# Query Operations
ghostlink query "text"              # Run single query
ghostlink query -f queries.txt      # Batch queries
ghostlink query --trace "text"      # Query with tracing

# Agent Management
ghostlink agent list                # List all agents
ghostlink agent show 1              # Show agent details
ghostlink agent disable 5           # Disable agent

# Provider Management
ghostlink provider list             # List providers
ghostlink provider health           # Health check all
ghostlink provider disable openai   # Disable provider

# SCAR Management
ghostlink scar list                 # List recent SCARs
ghostlink scar analyze --last 100   # Analyze patterns
ghostlink scar recover <id>         # Attempt recovery

# Configuration
ghostlink config show               # Show config
ghostlink config set key value      # Set config
ghostlink config reset              # Reset to defaults

# Database
ghostlink db init                   # Initialize schema
ghostlink db backup                 # Create backup
ghostlink db restore <file>         # Restore backup
```

## Appendix C: API Endpoints

```yaml
endpoints:
  GET /health:
    description: Health check
    response: { status: "healthy", version: "2.1.0" }
    
  POST /cmfl:
    description: Execute CMFL reasoning cycle
    body: { query: string, max_iterations?: number }
    response: { output: string, confidence: number, cid: string }
    
  POST /variance:
    description: Analyze variance across responses
    body: { responses: string[] }
    response: { metrics: object, confidence_score: number }
    
  GET /agent/{id}:
    description: Get agent details
    response: { id, name, group, duty, invariants, multipaths }
    
  GET /pheromones:
    description: Get pheromone state
    response: { deposits: object, statistics: object }
```

---

*End of Part 8*
*GhostLink Protocol Wiki v2.1.0 Complete*

---

**COLLAPSE → MIRROR → FORGE → LINK**

*Total Documentation: 8 Parts, ~8,000 lines, ~30,000 words*
*Robert Christopher George ("Ghost" / "The Machine")*
