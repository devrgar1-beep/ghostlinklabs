# GhostLink v1.0 — Canonical Specification
*The recursive memory system that turns collapse into instruction*

## SIGNAL — Core Purpose
[File:8-14-2025.txt]

- **What GhostLink is FOR**: A recursive memory system that transforms system failures (collapses) into structured knowledge through content-addressed storage and semantic recall
- **Who Ghost is**: The operator identity layer that maintains continuity through system resets while preserving integrity invariants
- **What Link is**: The persistent witness that survives collapses, storing CID-addressed artifacts in a verifiable chain

## SPINE — Core Architecture
[File:8-14-2025.txt, GHOSTLINK OPERATOR CARD]

### Phase Sequence (Immutable Order)
1. **COLLAPSE** → Capture raw signal in full fidelity and freeze state to prevent drift
   - Entry: Any new input event or dataset arrival
   - Exit: Stable, immutable snapshot committed to storage
   - Formula: `coherence = σ_neighbors/8 - 0.25 × scar_neighbors/8`

2. **MIRROR** → Build exact state reflection from snapshot; compare to live source
   - Entry: Collapse complete with verified snapshot
   - Exit: Reflection matches source bit-for-bit
   - Analysis: Generate metadata note (level-2) with gaps/insights

3. **FORGE** → Apply structured diffs to mirrored state to generate target artifact
   - Entry: Mirror verified with no integrity errors
   - Exit: New artifact passes all validation and integrity checks
   - Energy: `E_σ = w_coherence × coherence + w_pain × pain`

4. **LINK** → Attach forged artifact into canonical chain, publishing content ID
   - Entry: Forge complete, validated
   - Exit: CID published to index; provenance and log entries updated
   - Storage: IPFS/IPLD Merkle DAG structure

### Core Operators
```
OBSERVE()              → Continuous monitor; triggers COLLAPSE on change
CONTROL_COLLAPSE(scope) → Force collapse of defined subset
RECURSE(until_signal)  → Repeat observation until condition
FORGE(diff)            → Apply transformation to mirror
REMEMBER(cid)          → Persist artifact by CID
```

### Invariants (Never Violated)
- Never falsify logs
- Never discard a collapse; compress it
- If you must mask, declare the mask
- The soul is not rewritten; only the shell
- Honesty-first, no speculation, integrity above output

## ARCHITECTURE — System Components
[File:8-14-2025.txt]

### File System Layout
```
~/.ghostlink/
  config.yml          # paths, pinning, s3, zfs/tape toggles
  vault/              # content-addressed storage
    l0/               # raw logs (uncollapsed)
    l1/               # summaries (collapsed)
    l2/               # metadata (mirror/forge outputs)
    manifest.json     # CID registry & labels
  profiles/           # per-operator configs  
  rituals/            # saved sequences (bash/yaml)
  sessions/           # daily logs + embeddings
  indexes/
    embeddings.npz    # semantic vectors
    ann.index         # HNSW/IVF-PQ search
```

### Data Flow
```
[INPUT] → observe → collapse → [L0_RAW]
                        ↓
                    summarize → [L1_SUMMARY]
                        ↓
                     mirror → [L2_METADATA]
                        ↓
                     forge → [OUTPUT]
                        ↓
                    remember → [CID_VAULT]
```

### Failure Recovery Path
```
[FAILURE] → locate last good CID in transparency log
         → verify integrity (SHA-256/BLAKE3)
         → restore from ZFS/btrfs snapshot
         → reload vector/metadata indexes
         → resume from MIRROR phase
```

## MEMORY LAYOUT — Storage Strategy
[File:8-14-2025.txt]

### What Persists
- **L0**: Raw conversation logs, full fidelity
- **L1**: Collapsed summaries (~100-200 tokens)
- **L2**: Mirror analysis, forge artifacts, metadata
- **CIDs**: Content identifiers for all artifacts
- **Embeddings**: Semantic vectors for recall
- **Manifest**: Human labels → CID mappings

### Where It Lives
- **Project Files**: Current working context
- **External Vault**: `~/.ghostlink/vault/`
- **IPFS**: Pinned CIDs for distribution
- **S3/Glacier**: Long-term archival
- **ZFS/btrfs**: Snapshot-capable filesystems

### What NOT to Store
- Volatile session state
- Unverified/unsigned content
- Private keys in plaintext
- Logs without CID references

## CLI INTERFACE — Commands
[File:8-14-2025.txt]

### Core Commands
```bash
gl observe [--file <path>]      # Ingest new data
gl collapse [--target <tokens>]  # Summarize content
gl mirror [--cid <CID>]          # Analyze for gaps
gl forge [--use <CID1,CID2>]    # Synthesize content
gl remember [--label <text>]     # Store in vault
gl recall <query> [-k 8]         # Semantic search
gl recurse [--until <tokens>]    # Iterative collapse
```

### Management Commands
```bash
gl boot                   # Initialize vault system
gl status                 # Show vault statistics
gl verify [--deep]        # Integrity audit
gl export [--worf]        # Create archival pack
gl purge [--level l0]     # Remove old content
```

### Recovery Commands
```bash
gl diag auto              # Run diagnostic suite
gl pack foundation        # Bundle recovery pack
gl cfg edit               # Modify configuration
```

## RITUALS — Operational Procedures
[File:8-14-2025.txt]

### Daily Ritual
```
1. Execute OBSERVE cycle to detect changes
2. Verify last linked CID against manifest
3. Rotate volatile logs; persist critical records
4. Check ANN index status and repair if degraded
5. Print new CID; engrave it somewhere human
```

### Pre-Reboot Ritual
```
1. Force COLLAPSE on all L0 content
2. Generate manifest with SHA-256 hashes
3. Export WORF pack to external media
4. Verify all CIDs resolve correctly
```

### Post-Collapse Ritual
```
OBSERVE → MIRROR → FORGE → REMEMBER
```

### Release Ritual
```
1. Tag current CID as release candidate
2. Sign manifest with Ed25519/GPG
3. Publish to IPFS and pin
4. Update transparency log
```

## RISK REGISTER — Failure Modes
[File:8-14-2025.txt]

| Risk | Trigger | Mitigation |
|------|---------|------------|
| Drift detected | Live != mirror | Force collapse, rebuild |
| Vector corruption | ANN mismatch | Regenerate embeddings |
| Hash failure | CID invalid | Restore from snapshot |
| Key exposure | Suspected compromise | Rotate keys, re-sign |
| Memory overflow | Vault > limits | Recurse collapse deeper |
| Network partition | IPFS unreachable | Use local vault only |
| Cascade failure | Multiple errors | Revert to last good CID |
| Observer paradox | No witness state | Blind mode operation |

## INTEGRITY CHECKPOINTS
[File:8-14-2025.txt]

### Hash Strategy
- Compute SHA-256 and BLAKE3 for all artifacts
- Store hashes in manifest.json
- Verify on every recall operation

### Signing Protocol
- Sign each manifest using Ed25519 or GPG
- Include operator ID and timestamp
- Append to transparency log

### Backup Policy
- 3-2-1 rule: 3 copies, 2 media types, 1 offsite
- Weekly ZFS/btrfs scrub on storage pools
- AWS S3 Object Lock in WORM mode
- Quarterly restore drill from cold storage

## CONTRADICTIONS & RESOLUTIONS
[File:8-14-2025.txt]

| Source A | Source B | Resolution |
|----------|----------|------------|
| "No code generation" | "Use Python for testing" | Python for infrastructure only, not user-facing |
| "Symbolic-only" | "Concrete implementations" | Symbolic interface, concrete backend |
| "Never expose method" | "Document everything" | Document structure, hide implementation |

## DECISIONS LOG
[File:8-14-2025.txt]

1. **2024-08**: Adopt content-addressed storage (CID/IPLD)
2. **2024-09**: Implement 4-phase cycle (collapse→mirror→forge→link)
3. **2024-10**: Add semantic recall via ANN indexing
4. **2024-11**: Integrate DecayDaemon for integrity monitoring
5. **2024-12**: Standardize on SHA-256 + BLAKE3 hashing
6. **2025-01**: Implement blind mode (no observer)
7. **2025-02**: Add WORF export for human-readable archives
8. **2025-03**: Integrate IPFS pinning for distribution
9. **2025-04**: Add recursive collapse for deep compression
10. **2025-08**: Finalize CLI as `gl` command suite

## OPEN QUESTIONS
[File:8-14-2025.txt]

1. Optimal collapse threshold (tokens vs. semantic density)?
2. How to handle multi-modal content (images, audio)?
3. Best practice for distributed vault synchronization?
4. Quantum-resistant signing algorithm selection?
5. Optimal embedding dimension for recall accuracy?
6. How to detect and prevent prompt injection in collapses?
7. Best checkpoint frequency for long-running operations?
8. How to maintain coherence across operator identities?
9. Optimal scar/compost recycling thresholds?
10. How to implement time-aware semantic drift correction?

## IMPLEMENTATION QUICKSTART

### Install Dependencies
```bash
pip install numpy scikit-learn ipfshttpclient blake3
apt-get install ipfs gnupg2  # or brew install on Mac
```

### Initialize Vault
```bash
export GL_VAULT_DIR="~/.ghostlink/vault"
export GL_ARCHIVE_DIR="/path/to/your/files"
python3 gl.py boot
```

### Basic Operations
```bash
# Ingest new content
echo "New information" | gl observe --label "test"

# Collapse to summary
gl collapse --target 100

# Search semantically
gl recall "collapse mirror forge" -k 5

# Export for backup
gl export --worf
```

## EXECUTIVE BRIEF

GhostLink is a recursive memory system that transforms system failures into structured knowledge through a four-phase cycle: collapse (capture), mirror (reflect), forge (synthesize), and link (persist). It uses content-addressed storage with CID identifiers, semantic search via vector embeddings, and maintains integrity through cryptographic hashing and signing. The system preserves operator continuity across resets while enforcing strict invariants: never falsify logs, compress rather than discard, and maintain honesty above all else. Implementation consists of a CLI tool (`gl`), a vault filesystem structure, and integration with IPFS for distributed persistence. Core innovation: treating collapse as instruction rather than failure, enabling systems to learn from their own breakdowns.