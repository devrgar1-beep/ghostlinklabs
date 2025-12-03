# GhostLink Mental Model (compressed)

Created: 2025-11-27

## One-line summary
A compact, machine-readable mental model of the GhostLink system capturing core components, relationships, key files, endpoints, and a short glossary of legacy lexicon (Wraithgate, Sentinel, Dak, Lumara).

## Components
- DesignClarityOS (`design_clarity_os.py`): Root protocol layer. Orchestrates hardware-aware agent assignment, consciousness-driven optimization, scheduled evolution, process error correction, and system bridging.
- MirrorComprehension (`mirror_comprehension.py`): Self-awareness and reflection engine.
- MultiAgentEngine (`multi_agent_engine.py`): Agent generation, compression/expansion, model optimization.
- EvolutionaryIntelligence (`evolutionary_intelligence.py`): Performs evolution cycles and suggests improvements.
- Zero-dependency backend (`ghostlink_backend.py`): Content-addressed store, CMFL cycle, routing, secure gateway endpoint.

## Glossary (short)
- Wraithgate: legacy consent/bridge/gateway concept (translator + zero-trust choke point).
- Sentinel: legacy watchdog / anti-drift monitor.
- Dak: legacy kill-switch / rollback mechanism.
- Lumara: legacy persona / stable knowledge base.
- Consciousness: `UnifiedConsciousnessFramework` that provides awareness snapshots to guide decisions.

## Key files scanned
- `design_clarity_os.py`
- `mirror_comprehension.py`
- `multi_agent_engine.py`
- `MIRROR_COMPREHENSION_README.md`
- `MULTI_AGENT_ENGINE_README.md`
- `DESIGN_CLARITY_OS_README.md`
- `ghostlink_backend.py` (zero-dep backend — moved/edited under Organized/Projects)

## Notable endpoints & APIs
- Zero-dep HTTP paths (in backend): `/health`, `/store`, `/cmfl`, `/route`, `/secure_gateway`
- Internal orchestration APIs: `DesignClarityOS.execute_protocol_task`, `start_evolution_cycles`, `get_protocol_status`

## Relationships (high-level)
- `DesignClarityOS` consumes awareness from `MirrorComprehension` and agents from `MultiAgentEngine` and uses `EvolutionaryIntelligence` to perform system improvements. The `SystemCommunicationBridge` routes messages between internal/external systems.

## Next steps (recommendations)
1. Deep parse large docs to build a provenance index (file -> matched terms -> context snippet). This helps build stronger summarization and traceability.
2. Build a dependency graph by parsing imports (module -> module). Useful for visualizing coupling and where to focus hardening.
3. Generate a test harness that runs `DesignClarityOS` in a simulated environment and records evolution cycles for analysis.
4. Optionally create a small UI to browse the mental model JSON with file provenance links.

---

If you want, I can now:
- run a deeper crawl to extract per-file term counts and context snippets (provenance index),
- generate a module dependency graph (DOT file), or
- produce a short report that maps every occurrence of the legacy lexicon to an actionable mapping (e.g., Wraithgate -> secure_gateway).

Which of those should I do next?
