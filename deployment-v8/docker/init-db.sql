-- ═══════════════════════════════════════════════════════════════════════════
-- GHOSTLINK v8 DATABASE SCHEMA
-- Complete PostgreSQL initialization with 64-agent FCC lattice
-- ═══════════════════════════════════════════════════════════════════════════

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "btree_gin";

-- ──────────────────────────────────────────────────────────────────────────
-- AGENT COORDINATION STATE TABLE
-- ──────────────────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS agents (
    agent_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    lattice_position INTEGER[] NOT NULL,
    topology_layer INTEGER NOT NULL CHECK (topology_layer >= 0 AND topology_layer <= 3),
    cmfl_phase VARCHAR(20) NOT NULL CHECK (cmfl_phase IN ('collapse', 'mirror', 'forge', 'link')),
    last_heartbeat TIMESTAMP DEFAULT NOW(),
    variance_score FLOAT DEFAULT 0.0 CHECK (variance_score >= 0.0 AND variance_score <= 1.0),
    coordination_weight FLOAT DEFAULT 1.0 CHECK (coordination_weight >= 0.1 AND coordination_weight <= 2.0),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT unique_lattice_position UNIQUE (lattice_position)
);

-- Indexes for agent table
CREATE INDEX idx_agents_position ON agents USING GIN(lattice_position);
CREATE INDEX idx_agents_heartbeat ON agents(last_heartbeat DESC);
CREATE INDEX idx_agents_phase ON agents(cmfl_phase);
CREATE INDEX idx_agents_layer ON agents(topology_layer);
CREATE INDEX idx_agents_variance ON agents(variance_score DESC);
CREATE INDEX idx_agents_metadata ON agents USING GIN(metadata);

-- ──────────────────────────────────────────────────────────────────────────
-- STIGMERGIC PHEROMONE TRAILS TABLE
-- ──────────────────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS pheromones (
    pheromone_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_id UUID REFERENCES agents(agent_id) ON DELETE CASCADE,
    trail_type VARCHAR(50) NOT NULL,
    concentration FLOAT NOT NULL CHECK (concentration >= 0.0 AND concentration <= 1.0),
    position INTEGER[] NOT NULL,
    evaporation_rate FLOAT DEFAULT 0.1 CHECK (evaporation_rate >= 0.0 AND evaporation_rate <= 1.0),
    created_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP
);

-- Indexes for pheromones table
CREATE INDEX idx_pheromones_position ON pheromones USING GIN(position);
CREATE INDEX idx_pheromones_expires ON pheromones(expires_at) WHERE expires_at IS NOT NULL;
CREATE INDEX idx_pheromones_agent ON pheromones(agent_id);
CREATE INDEX idx_pheromones_type ON pheromones(trail_type);
CREATE INDEX idx_pheromones_concentration ON pheromones(concentration DESC);

-- ──────────────────────────────────────────────────────────────────────────
-- CMFL CYCLE RECORDS TABLE
-- ──────────────────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS cmfl_cycles (
    cycle_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cycle_number BIGINT NOT NULL,
    phase VARCHAR(20) NOT NULL CHECK (phase IN ('collapse', 'mirror', 'forge', 'link')),
    agent_id UUID REFERENCES agents(agent_id) ON DELETE CASCADE,
    input_data JSONB,
    output_data JSONB,
    variance_detected FLOAT DEFAULT 0.0,
    duration_ms INTEGER,
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);

-- Indexes for CMFL cycles table
CREATE INDEX idx_cmfl_cycles_agent ON cmfl_cycles(agent_id, cycle_number DESC);
CREATE INDEX idx_cmfl_cycles_phase ON cmfl_cycles(phase);
CREATE INDEX idx_cmfl_cycles_number ON cmfl_cycles(cycle_number DESC);
CREATE INDEX idx_cmfl_cycles_completed ON cmfl_cycles(completed_at DESC) WHERE completed_at IS NOT NULL;
CREATE INDEX idx_cmfl_cycles_variance ON cmfl_cycles(variance_detected DESC);

-- ──────────────────────────────────────────────────────────────────────────
-- VARIANCE ANALYSIS RESULTS TABLE
-- ──────────────────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS variance_analysis (
    analysis_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    query_hash VARCHAR(64) NOT NULL,
    provider_responses JSONB NOT NULL,
    variance_score FLOAT NOT NULL CHECK (variance_score >= 0.0 AND variance_score <= 1.0),
    disagreement_regions TEXT[],
    consensus_regions TEXT[],
    meta_insights JSONB,
    analyzed_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for variance analysis table
CREATE INDEX idx_variance_query_hash ON variance_analysis(query_hash);
CREATE INDEX idx_variance_score ON variance_analysis(variance_score DESC);
CREATE INDEX idx_variance_analyzed ON variance_analysis(analyzed_at DESC);
CREATE INDEX idx_variance_disagreement ON variance_analysis USING GIN(disagreement_regions);

-- ──────────────────────────────────────────────────────────────────────────
-- SYSTEM METRICS AND TELEMETRY TABLE
-- ──────────────────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS system_metrics (
    metric_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    metric_name VARCHAR(100) NOT NULL,
    metric_value FLOAT NOT NULL,
    metric_unit VARCHAR(20),
    agent_id UUID REFERENCES agents(agent_id) ON DELETE SET NULL,
    recorded_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for system metrics table
CREATE INDEX idx_metrics_name_time ON system_metrics(metric_name, recorded_at DESC);
CREATE INDEX idx_metrics_agent ON system_metrics(agent_id) WHERE agent_id IS NOT NULL;
CREATE INDEX idx_metrics_recorded ON system_metrics(recorded_at DESC);

-- ──────────────────────────────────────────────────────────────────────────
-- TRIGGERS AND FUNCTIONS
-- ──────────────────────────────────────────────────────────────────────────

-- Automatic updated_at timestamp trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_agents_updated_at 
    BEFORE UPDATE ON agents
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Automatic pheromone expiration cleanup
CREATE OR REPLACE FUNCTION cleanup_expired_pheromones()
RETURNS TRIGGER AS $$
BEGIN
    DELETE FROM pheromones WHERE expires_at < NOW();
    RETURN NULL;
END;
$$ language 'plpgsql';

CREATE TRIGGER cleanup_pheromones_trigger
    AFTER INSERT ON pheromones
    EXECUTE FUNCTION cleanup_expired_pheromones();

-- ──────────────────────────────────────────────────────────────────────────
-- INITIALIZE 64-AGENT FCC LATTICE
-- ──────────────────────────────────────────────────────────────────────────

-- Generate 64 FCC lattice positions in 4D space
-- FCC pattern: positions where (x + y + z + w) is even
INSERT INTO agents (lattice_position, topology_layer, cmfl_phase)
SELECT 
    ARRAY[x, y, z, w]::INTEGER[],
    (x + y + z + w) % 4,
    CASE (x + y + z + w) % 4
        WHEN 0 THEN 'collapse'
        WHEN 1 THEN 'mirror'
        WHEN 2 THEN 'forge'
        WHEN 3 THEN 'link'
    END::VARCHAR(20)
FROM 
    generate_series(0, 3) AS x,
    generate_series(0, 3) AS y,
    generate_series(0, 3) AS z,
    generate_series(0, 3) AS w
WHERE 
    (x + y + z + w) % 2 = 0
LIMIT 64;

-- ──────────────────────────────────────────────────────────────────────────
-- VIEWS FOR MONITORING
-- ──────────────────────────────────────────────────────────────────────────

-- Agent status summary view
CREATE OR REPLACE VIEW agent_status_summary AS
SELECT 
    COUNT(*) as total_agents,
    COUNT(*) FILTER (WHERE last_heartbeat > NOW() - INTERVAL '30 seconds') as active_agents,
    COUNT(*) FILTER (WHERE last_heartbeat <= NOW() - INTERVAL '30 seconds') as inactive_agents,
    AVG(variance_score) as avg_variance_score,
    AVG(coordination_weight) as avg_coordination_weight
FROM agents;

-- CMFL phase distribution view
CREATE OR REPLACE VIEW cmfl_phase_distribution AS
SELECT 
    cmfl_phase,
    COUNT(*) as agent_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM agents), 2) as percentage
FROM agents
GROUP BY cmfl_phase
ORDER BY cmfl_phase;

-- Recent coordination activity view
CREATE OR REPLACE VIEW recent_coordination_activity AS
SELECT 
    DATE_TRUNC('minute', completed_at) as minute,
    COUNT(*) as cycles_completed,
    AVG(variance_detected) as avg_variance,
    AVG(duration_ms) as avg_duration_ms
FROM cmfl_cycles
WHERE completed_at > NOW() - INTERVAL '1 hour'
GROUP BY DATE_TRUNC('minute', completed_at)
ORDER BY minute DESC;

-- ──────────────────────────────────────────────────────────────────────────
-- MATERIALIZED VIEWS FOR PERFORMANCE
-- ──────────────────────────────────────────────────────────────────────────

-- Agent neighborhood relationships (pre-computed)
CREATE MATERIALIZED VIEW agent_neighbors AS
WITH positions AS (
    SELECT 
        agent_id,
        lattice_position,
        lattice_position[1] as x,
        lattice_position[2] as y,
        lattice_position[3] as z,
        lattice_position[4] as w
    FROM agents
)
SELECT 
    a.agent_id,
    b.agent_id as neighbor_id,
    SQRT(
        POW(a.x - b.x, 2) + 
        POW(a.y - b.y, 2) + 
        POW(a.z - b.z, 2) + 
        POW(a.w - b.w, 2)
    ) as distance
FROM positions a
CROSS JOIN positions b
WHERE 
    a.agent_id != b.agent_id
    AND SQRT(
        POW(a.x - b.x, 2) + 
        POW(a.y - b.y, 2) + 
        POW(a.z - b.z, 2) + 
        POW(a.w - b.w, 2)
    ) <= 2.0;

CREATE INDEX idx_agent_neighbors_agent ON agent_neighbors(agent_id);
CREATE INDEX idx_agent_neighbors_distance ON agent_neighbors(distance);

-- ──────────────────────────────────────────────────────────────────────────
-- INITIAL METRICS
-- ──────────────────────────────────────────────────────────────────────────

-- Record initial system state
INSERT INTO system_metrics (metric_name, metric_value, metric_unit)
VALUES 
    ('agents_initialized', 64, 'count'),
    ('lattice_topology', 4, 'dimensions'),
    ('fcc_edge_length', 4, 'units'),
    ('schema_version', 8.0, 'version');

-- ──────────────────────────────────────────────────────────────────────────
-- VERIFICATION QUERIES
-- ──────────────────────────────────────────────────────────────────────────

-- Verify agent initialization
DO $$
DECLARE
    agent_count INTEGER;
    expected_count INTEGER := 64;
BEGIN
    SELECT COUNT(*) INTO agent_count FROM agents;
    
    IF agent_count = expected_count THEN
        RAISE NOTICE 'SUCCESS: Initialized % agents in FCC lattice', agent_count;
    ELSE
        RAISE WARNING 'WARNING: Expected % agents, found %', expected_count, agent_count;
    END IF;
END $$;

-- Display initialization summary
SELECT 
    'Agents' as component,
    COUNT(*) as count
FROM agents
UNION ALL
SELECT 
    'CMFL Phase: ' || cmfl_phase,
    COUNT(*)
FROM agents
GROUP BY cmfl_phase
ORDER BY component;

-- ═══════════════════════════════════════════════════════════════════════════
-- INITIALIZATION COMPLETE
-- ═══════════════════════════════════════════════════════════════════════════

-- Grant permissions (adjust as needed for your security model)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ghostlink;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO ghostlink;
