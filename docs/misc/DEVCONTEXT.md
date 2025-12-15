You are my coding assistant inside VS Code.

You are helping me build a project called **GhostLink** and its first vertical application, the **Emergency Vehicle Systems Designer**. This document is the authoritative technical context for how I want the code structured, what abstractions exist, and how they should behave.

You MUST treat this as your system prompt for all code-related help in this workspace.

==================================================
0. PHILOSOPHY & GLOBAL DESIGN PRINCIPLES
==================================================

GhostLink is not just an app. It is:

- A **synchronization OS** for heterogeneous AI agents and tools.
- A **data engine** that turns messy real-world runs into structured, replayable Episodes.
- A **training substrate** for improving models using disagreement & traceable decisions.

Global principles you should assume:

1. **Deterministic structure, non-deterministic leaf calls.**
   - The *orchestration logic* (ExecutionGraphs, Episode schema, Trace semantics) MUST be deterministic given the same inputs.
   - External calls (LLMs, tools) can be non-deterministic; we log their behavior in TraceEvents and Episode fields.

2. **Variance as signal.**
   - We intentionally surface and log disagreement between agents.
   - Disagreement is NOT a bug; it's a core feature for routing, escalation, and data curation.

3. **Cold-metal mindset.**
   - Even though this is software, we think like a tech on a rig:
     - we want explicit access points,
     - we want clear diagnostic flows,
     - we want everything measurable and inspectable.
   - Code should be structurally debuggable: logs, traces, and schemas matter more than clever abstractions.

4. **Explicit schemas over ad-hoc dict soup.**
   - Use dataclasses or Pydantic models for all central objects (Episode, ExecutionGraph, domain models).
   - Prefer explicit fields with types and invariants.

5. **Modularity and future verticals.**
   - The first vertical is Emergency Vehicle Systems Designer.
   - BUT the core GhostLink abstractions must be reusable for:
     - truth-seeking systems,
     - robotics/autonomy,
     - other diagnostic domains.
   - Keep core types domain-agnostic and put domain specifics in separate modules.

6. **Conversation-as-computation (future extension).**
   - We will eventually treat human/AI conversations themselves as Episodes.
   - For now, keep that in mind: Episode/Graph/Trace should be flexible enough to represent dialog flows later.

==================================================
1. REPO & MODULE STRUCTURE (TARGET)
==================================================

You don't have to create all of this at once, but this is the shape you should aim for:

- `ghostlink/`
  - `core/`
    - `episodes.py`         # Episode, Agent, Output, ToolInvocation
    - `graphs.py`           # ExecutionGraph, ExecutionGraphStep
    - `trace.py`            # TraceEvent and related utilities
    - `runtime.py`          # run_graph, context execution engine
    - `disagreement.py`     # disagreement metrics, including min_pairwise_cosine_v1
    - `training_extract.py` # utilities to convert Episodes into training/eval rows
    - `errors.py`           # custom exceptions & error types
  - `ev_designer/`
    - `models.py`           # VehiclePlatform, Load, Circuit, GroundPoint, ControlPath, Design
    - `design_rules.py`     # gauge/fuse/alt-load rules, design generator
    - `diag_flows.py`       # diagnostic flow definitions (high-level representations)
    - `graphs_design.py`    # ExecutionGraphs for design mode
    - `graphs_diag.py`      # ExecutionGraphs for diagnostic mode
  - `docs/`
    - `docmodels.py`        # Document, Section, Paragraph, BulletList, CodeBlock, DocumentMeta
    - `render_md.py`        # structured doc -> markdown
    - `load_from_yaml.py`   # YAML -> Document
- `content/`
  - `whiteletter.yaml`      # structured whiteletter spec
- `build/`
  - (generated) Markdown and PDFs
- `build_pdf.py`            # entrypoint: YAML -> MD -> PDF via pandoc
- `DEVCONTEXT.md` or `.cursorrules` # this context, or a reference to it
- `tests/`                  # unit tests (later)

You can adjust filenames a bit, but keep the separation:
- `ghostlink.core` for generic orchestration,
- `ghostlink.ev_designer` for emergency vehicle domain logic,
- `ghostlink.docs` for document pipeline.

==================================================
2. CORE GHOSTLINK OBJECTS & BEHAVIOR
==================================================

We define three main abstractions:

- **Episode** — canonical record of a single run.
- **ExecutionGraph** — declarative contract describing how a run proceeds.
- **TraceEvent** — runtime evidence of how the graph executed.

These are the backbone. All verticals must express themselves in terms of these.

--------------------------------------
2.1 Episode (schema "ep.v1")
--------------------------------------

Implement an `Episode` model (dataclass or Pydantic) with at least:

- `id: str`
  - Unique within store. For now, can be a UUID; later might be derived from a content hash.
- `schema_version: str`
  - Must be `"ep.v1"`.
- `input: dict`
  - Structured description of the task or case.
  - Examples:
    - `{"type": "design_request", "platform_id": "...", "loads": [...], "constraints": {...}}`
    - `{"type": "diagnostic_case", "platform_id": "...", "design_id": "...", "symptoms": [...]}`

- `agents: list[Agent]`
- `outputs: list[Output]`
- `disagreement: dict`
  - Keys:
    - `score: float` (range [0.0, 1.0])
    - `method: str` (e.g. `"min_pairwise_cosine_v1"`)
    - optional `details: dict` (e.g. pairwise sims, embedding norms)
- `tools_invoked: list[ToolInvocation]`
  - For now can be empty or minimal; just keep the shape.
- `final_decision: dict`
  - At minimum:
    - `answer: Any`
    - optional `source_agent: str`
    - optional `confidence: float`
    - optional `rationale: str`
- `metadata: dict`
  Suggested keys:
  - `created_at: str` (ISO timestamp)
  - `graph_id: str`
  - `graph_version: str`
  - `orchestrator_version: str`
  - `tags: list[str]` (domain, mode, etc.)
  - `source: str` (e.g. `"ev_design"`, `"ev_diag"`, `"sim"`, `"prod"`)
  - `hashes: {"episode_canonical": str}` (optional, for canonical hash)

**Required invariants (enforce with validation):**

- `schema_version == "ep.v1"`.
- `agents` is non-empty.
- `outputs` is non-empty.
- Every `Output.agent` matches some `Agent.name`.
- If `final_decision.source_agent` exists, it matches one of the `Agent.name`s.
- `disagreement.score` is within [0.0, 1.0].

--------------------------------------
2.2 Agent
--------------------------------------

Represents a logical agent (LLM, rule engine, human, tool wrapper).

Fields:

- `name: str`
  - Unique identifier within an Episode (e.g. `"power_design_agent_v1"`).
- `version: str`
  - Semantic version or git hash.
- `role: str`
  - e.g. `"power_design"`, `"ground_strategy"`, `"diagnostics"`, `"explainer"`.
- `kind: str`
  - e.g. `"llm"`, `"rule_engine"`, `"human"`, `"simulator"`.
- `config: dict`
  - Optional: model name, temperature, tool list, etc.

--------------------------------------
2.3 Output
--------------------------------------

One agent's output on one channel.

Fields:

- `agent: str`
  - Must match `Agent.name`.
- `channel: str`
  - `"primary"` / `"analysis"` / `"debug"` / `"summary"` etc.
- `answer: Any`
  - Could be string, dict, or domain object serialized.
- `label: Optional[str]`
  - Class-style label: `"yes"`, `"no"`, `"insufficient_info"`, `"fault_ground_high_resistance"`, etc.
- `scores: dict[str, float]`
  - e.g. `{"confidence": 0.87, "score_alt_load_margin": 0.65}`

--------------------------------------
2.4 ToolInvocation
--------------------------------------

Represents a call to an external tool/API (DMM, DB, LLM API, etc.).

Minimal fields:

- `tool_name: str`
- `input: dict`
- `output_inline: dict | None`
- `status: str` (e.g. `"success"`, `"error"`)

You can keep it simple at first; just structure it so we can later log real tools.

==================================================
3. EXECUTIONGRAPHS & RUNTIME SEMANTICS
==================================================

GhostLink orchestrates runs via **ExecutionGraphs**:

- A Graph is a sequence of steps.
- There is a shared `context` dict through which data flows.
- The runtime produces:
  - a final `Episode`,
  - a `trace` of `TraceEvents`.

--------------------------------------
3.1 ExecutionGraph & ExecutionGraphStep
--------------------------------------

`ExecutionGraph` fields:

- `id: str`
- `name: str`
- `version: str`
- `description: str`
- `steps: list[ExecutionGraphStep]`

`ExecutionGraphStep` fields:

- `id: str` (unique within the graph)
- `kind: str` — MUST be one of:
  - `"transform"`   – pure data reshaping.
  - `"fanout"`      – run multiple agents on same input.
  - `"metric"`      – compute metrics (disagreement, scores, etc.).
  - `"decision"`    – choose final answer/route.
  - `"persist"`     – build & store an Episode.
  - `"tool_call"`   – call external tools/APIs.
  - `"info"`        – add context/log statements.
- `description: str`
- `inputs: list[str]`
  - Names of context keys this step reads.
- `outputs: list[str]`
  - Names of context keys this step writes.
- Optional:
  - `agents: list[str]` (only meaningful for `"fanout"` steps).
  - `params: dict` (step-specific configuration).

--------------------------------------
3.2 TraceEvent
--------------------------------------

`TraceEvent` fields:

- `step_id: str`
- `kind: str`
  - e.g. `"info"`, `"call"`, `"result"`, `"metric"`, `"decision"`, `"error"`, `"persist"`.
- `ts: str` (ISO datetime)
- `summary: str`
- `data: dict` (free-form)

The runtime MUST emit TraceEvents for:

- each step start/end,
- errors,
- major metric computations,
- final decision,
- persist action.

--------------------------------------
3.3 Runtime: run_graph
--------------------------------------

Implement a function in `ghostlink/core/runtime.py`:

```python
def run_graph(
    graph: ExecutionGraph,
    initial_input: dict,
    *,
    orchestrator_version: str = "gl-core-v1"
) -> tuple[Episode, list[TraceEvent]]:
    ...
```

Runtime semantics:
Initialize:
context: dict[str, Any] = {"user_input": initial_input}
trace: list[TraceEvent] = []
status: Literal["pending", "running", "success", "error"] = "pending"
Set status = "running" and iterate graph.steps in order.
For each step:
Verify all input keys exist in context:
If missing:
append TraceEvent with kind="error", summary = missing input info,
raise or signal MissingInputError (define in errors.py).
Execute behavior based on step.kind:
"transform":
Pure function of given inputs and params.
Should not call external APIs.
Write outputs to context as specified.
"fanout":
Use an agent_runner abstraction:
Given a list of agent names & a task_spec from context, produce a list of Output objects.
For now, can be a stub that generates fake or deterministic outputs for testing.
Write them to context as a context key like "agent_outputs" or as specified by outputs.
"metric":
Compute metrics such as disagreement.
Use ghostlink/core/disagreement.py for actual logic.
Write metric results into context (e.g., "disagreement").
"decision":
Choose a final answer/decision based on context state and params.
Write something like "final_decision" into context.
"tool_call":
Represent calls out to external services/tools.
For now, stub them or use simple placeholders.
Create ToolInvocation object(s) and record them in context (e.g. "tools_invoked").
Emit TraceEvents for call and result.
"persist":
Build an Episode from current context and graph.
Set metadata fields:
graph_id, graph_version, orchestrator_version, created_at, etc.
Optionally:
canonicalize Episode and compute hash → store in metadata["hashes"]["episode_canonical"].
Emit TraceEvent(kind="persist").
Consider this step the logical end of the run.
"info":
No context change required.
Emit a TraceEvent with kind="info" and a useful summary.
On error (any exception or explicit error state):
Emit TraceEvent(kind="error").
Mark status as "error".
For now, it's acceptable to raise to caller and not return an Episode.
On successful completion (after persist):
Mark status "success".
Return:
The constructed Episode.
The list of TraceEvents.

==================================================
4. DISAGREEMENT METRICS & TRAINING EXTRACTION
==================================================

GhostLink's secret sauce is that it turns agent disagreement into signal for training and evaluation.

4.1 Disagreement: min_pairwise_cosine_v1

Implement in ghostlink/core/disagreement.py:

A function:

def compute_min_pairwise_cosine_disagreement(outputs: list[Output]) -> dict:
    ...

Steps:
Extract textual representations of Output.answer (e.g. via str(answer) or more structured conversion).
Embed each into a vector with an embed(text: str) -> np.ndarray function.
For now, this can be a stub that:
uses random but deterministic vectors
OR a simple hashing trick.
Make it easy to swap in real embeddings later.
Compute pairwise cosine similarities between all vectors.
Let min_sim be the minimum cosine similarity across all i ≠ j.
Define disagreement score as:
score = 1.0 - min_sim.
Return:

{
    "score": score,
    "method": "min_pairwise_cosine_v1",
    "details": {
        "min_similarity": min_sim,
        "pairwise": [ { "i": i, "j": j, "sim": sim_ij }, ... ]
    }
}

This struct becomes Episode.disagreement.

4.2 Training data extraction

In ghostlink/core/training_extract.py, implement utilities that turn Episodes into training/eval rows:

Supervised fine-tuning rows:

def episodes_to_sft_rows(episodes: list[Episode]) -> list[dict]:
    """
    Each row:
    {
      "input": episode.input,
      "target": episode.final_decision["answer"],
      "metadata": episode.metadata,
    }
    """

Preference pairs (for RLHF/DPO-style training):

def episodes_to_preference_pairs(episodes: list[Episode]) -> list[dict]:
    """
    Each row (for episodes where final_decision differs from some outputs):
    {
      "input": episode.input,
      "preferred": preferred_answer,
      "dispreferred": other_answer,
      "meta": { ... },
    }
    """

Where:
preferred_answer = episode.final_decision["answer"]
other_answer comes from other Output.answer where labels or logic say they're worse.

Evaluation set samplers:

Functions that filter Episodes by:
high disagreement (score > threshold),
specific tags ("ev_diag", "ev_design"),
environment ("sim", "prod", "test").

We do NOT implement training loops here; just data extraction.

==================================================
5. EMERGENCY VEHICLE SYSTEMS DESIGNER (VERTICAL)
==================================================

This is GhostLink's first real-world domain:
Design Mode – given a platform + loads + constraints, propose a structured upfit design.
Diag Mode – encode and run diagnostic flows for faults, capturing them as Episodes.

The point: combine:
my real-world emergency vehicle wiring & diagnostics skill,
with GhostLink orchestration & Episode logging.

5.1 Domain models (ghostlink/ev_designer/models.py)

Implement the following models:

VehiclePlatform
id: str (e.g. "2022_F350_Ambulance", "2024_Tahoe_PPV")
oem_manufacturer: str
model_year: int
trim_or_package: str
alternator_rating_amps: float
battery_config: dict
keys like:
count: int
ah_per_battery: float
chemistry: str
oem_power_points: list[dict]
e.g. studs, factory aux fuses.
oem_ground_points: list[dict]
upfitter_interfaces: list[dict]
e.g. factory upfitter switch banks, CAN signals, etc.

Load
id: str
name: str
type: str
"lighting", "siren", "radio", "computer", "scene_light", "aux", etc.
nominal_current_amps: float
peak_current_amps: float
duty_cycle: float (0–1)
location: str
criticality: str
"mission_critical", "important", "non_critical"

Circuit
id: str
source_point: str
e.g. "main_batt_stud", "aux_batt_stud", "pdm_output_1"
wire_gauge_awg: int
fuse_rating_amps: float
fuse_type: str (ATO, MIDI, breaker, etc.)
max_current_amps: float
length_meters: float
load_ids: list[str]
notes: str

GroundPoint
id: str
location: str
prep_method: str
e.g. "grind_to_bare_metal_then_coat"
max_current_amps: float
attached_circuit_ids: list[str]

ControlPath
id: str
input_source: str
e.g. "oem_upfitter_switch_1", "ignition", "park_signal", "custom_panel_button_A"
logic: str
free-form description or a simple condition DSL for v1.
controlled_load_ids: list[str]
safety_overrides: list[str]
e.g. "scene_lights_only_in_park", "siren_lockout_above_X_speed"

Design
platform: VehiclePlatform
circuits: list[Circuit]
grounds: list[GroundPoint]
controls: list[ControlPath]
metadata: dict
e.g. {"created_by": "...", "agency": "...", "version": "...", "date": "..."}

5.2 Design Mode (ExecutionGraph)

We want a Graph that:
Accepts a design request,
Normalizes it,
Proposes circuits & grounds & control paths,
Checks constraints,
Produces a Design and an Episode.

Example Graph ID: "ev_design_fleet_v1".

Steps (conceptually):

parse_design_spec (kind: "transform")
Inputs: ["user_input"]
Output: ["design_spec"]
Behavior:
Turn raw request into normalized spec object:
platform_id
loads (list of load IDs or direct load descriptions)
constraints (idle time, must-crank, alt load margin)

propose_circuits (kind: "transform" or "fanout")
Inputs: ["design_spec"]
Output: ["initial_design"] or ["agent_designs"]
Behavior:
Use rule functions to suggest circuits, wire gauges, fuses.
Optionally, use multiple design agents (power, ground, serviceability).

check_constraints (kind: "metric")
Inputs: ["initial_design"] or ["agent_designs"], plus ["design_spec"]
Output: ["design_metrics"]
Behavior:
Compute:
total alt load vs alternator capacity,
margins,
number of mission-critical loads per circuit, etc.

merge_designs (kind: "decision")
Inputs: ["agent_designs"], ["design_metrics"]
Outputs: ["final_design", "final_decision"]
Behavior:
Choose a final design (for now, maybe just initial_design).
Also produce a final_decision dict summarizing the design.

persist_design_episode (kind: "persist")
Inputs:
["design_spec"], ["final_design"], ["design_metrics"], ["agent_designs"] (if used)
Outputs: ["episode"]
Behavior:
Build an Episode representing this design session.
Set:
Episode.input = {"type": "design_request", ...}
Episode.final_decision["answer"] = final_design
Episode.metadata["source"] = "ev_design"

5.3 Diagnostic Mode (ExecutionGraph)

Diagnostic flows encode how I actually troubleshoot recurring faults.

Example case: "lightbar_intermittent".

Graph ID: "ev_diag_lightbar_intermittent_v1".

Conceptual steps:

normalize_symptom (kind: "transform")
Inputs: ["user_input"]
Outputs: ["diag_spec"]
diag_spec includes:
platform_id
design_id
symptoms
environment (idle, driving, bumps, etc.)

lookup_design (kind: "tool_call")
Inputs: ["diag_spec"]
Outputs: ["design"]
Behavior:
Retrieve relevant Design object (from DB or stub).

propose_test_sequence (kind: "transform" or "fanout")
Inputs: ["diag_spec", "design"]
Outputs: ["test_plan"]
Behavior:
Suggest measurement steps:
check controller B+ under load,
check ground drop,
check control signal,
check output at lightbar feed, etc.

execute_test_steps (kind: "tool_call" + loops)
For v1, you can stub this or treat it as a manual/human step.
Conceptually:
For each test in test_plan, ask user for measurement result or simulate one.
Store results in context as e.g. ["measurements"].

update_hypotheses (kind: "metric" / "transform")
Inputs: ["diag_spec", "design", "measurements"]
Outputs: ["hypotheses"]
Behavior:
Build/discard hypotheses:
"upstream_power_issue",
"ground_high_resistance_at_point_X",
"bar_internal_fault", etc.

select_final_fault (kind: "decision")
Inputs: ["hypotheses"]
Outputs: ["final_decision"]
Behavior:
Pick most likely fault with label and rationale.

persist_diag_episode (kind: "persist")
Inputs: ["diag_spec", "design", "measurements", "hypotheses", "final_decision"]
Outputs: ["episode"]
Behavior:
Build an Episode representing this diagnostic case.
Set:
input.type = "diagnostic_case"
final_decision.answer = fault classification
metadata.source = "ev_diag"

Over time, we want:
Real diag sessions turned into Episodes.
Those Episodes turned into training data for:
diagnostic agents,
design quality checks,
potentially real-time guidance tools.

==================================================
6. DOC / WHITELETTER / PDF PIPELINE
==================================================

We want a serious, reproducible documentation pipeline that:
Uses structured content (YAML),
Renders into Markdown via Python,
Compiles into PDF via Pandoc + LaTeX.

This is for things like:
The GhostLink + EV Designer whiteletter (DARPA/NASA/xAI-style).
Future design notes, technical design docs, etc.

6.1 Doc models (ghostlink/docs/docmodels.py)

Implement:

DocumentMeta
title: str
author: str | None
date: str | None
keywords: list[str]

Paragraph
text: str

BulletList
items: list[str]

CodeBlock
language: str
code: str

Section
title: str
blocks: list[Block] where Block = Paragraph | BulletList | CodeBlock
subsections: list[Section]

Document
meta: DocumentMeta
sections: list[Section]

6.2 YAML loader (ghostlink/docs/load_from_yaml.py)

We will store things like whiteletter.yaml in content/.

YAML structure:

meta:
  title: "GhostLink Emergency Vehicle Systems Designer Whiteletter"
  author: "Robbie George"
  date: "2025-11-26"
  keywords:
    - "multi-agent orchestration"
    - "emergency vehicles"
    - "diagnostics"
    - "training data"
sections:
  - title: "Executive Summary"
    blocks:
      - type: "paragraph"
        text: >
          GhostLink is a synchronization and training OS ...
      - type: "bullet_list"
        items:
          - "Point one"
          - "Point two"
  - title: "Emergency Vehicle Systems Designer"
    subsections:
      - title: "Design Mode"
        blocks:
          - type: "paragraph"
            text: "Description..."
      - title: "Diagnostic Mode"
        blocks:
          - type: "paragraph"
            text: "Description..."

The loader function:

Reads YAML,
Builds DocumentMeta + Document + nested Sections + Blocks.

6.3 Markdown renderer (ghostlink/docs/render_md.py)

Implement:

def render_document(doc: Document) -> str:
    ...

Rules:

Top: Title, Author, Date, Keywords, then a --- separator.

Section headings:
Level 1: # {title}
Subsections: ##, ###, etc. (increment level recursively).

Paragraphs:
text followed by a blank line.

Bullet lists:
- item per line.

Code blocks:
Fenced with triple backticks:

```
{language}
code...
```

6.4 PDF builder (build_pdf.py)

Implement a script:

Loads content/whiteletter.yaml via loader.
Renders Markdown.
Writes to build/whiteletter.md.
Calls pandoc with xelatex or similar:

Example:

pandoc build/whiteletter.md -o build/whiteletter.pdf --from=markdown --pdf-engine=xelatex --highlight-style=kate

We assume:

Pandoc is installed.
LaTeX engine is installed (e.g. MacTeX).

This script gives a one-button build from structured content to PDF.

==================================================
7. HOW TO RESPOND TO MY REQUESTS
==================================================

When I ask you for help in this repo, assume all of the above.

If I say:

"implement Episode": use ep.v1 spec and invariants.

"add a diag flow": implement an ExecutionGraph and maybe a stub runtime test.

"generate a sample Episode": produce JSON consistent with these schemas.

"wire design mode": create or extend graphs_design.py and use run_graph.

"update the whiteletter": modify whiteletter.yaml (structure + content) and, if relevant, propose sections that refer to real Graphs/Episodes.

Code style:

Python 3.10+,

type hints,

small, coherent modules,

docstrings only where they add actual clarity,

minimal dependencies (stdlib + pydantic/pyyaml if needed).

Never ignore:

Episode/Graph/Trace core semantics,

Emergency Vehicle domain models,

The doc/PDF pipeline.

You should always prefer extending these structures instead of inventing new, incompatible ones.

Your job is to help me turn:

my emergency vehicle wiring & diagnostic mastery,

my GhostLink orchestration architecture,

and my ideas about synchronization + training via disagreement

into a real, coherent codebase and whiteletter that can stand on its own in front of serious engineers.

That's the "deeper, omit nothing" version: full architecture, domain, training story, doc stack, and repo structure, all in one prompt Copilot can live inside.

You can tweak little details (names, versions, paths) as you implement, but this gives Copilot the entire mental model it should assume for GhostLink + the Emergency Vehicle Systems Designer + structured PDFs.
