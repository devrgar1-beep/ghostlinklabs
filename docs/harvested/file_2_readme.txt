═══════════════════════════════════════════════════════════════════
  GHOSTLINK STARTER - SETUP INSTRUCTIONS
═══════════════════════════════════════════════════════════════════

Thank you for purchasing GHOSTLINK Starter!

This package contains everything you need to start automating complex 
tasks with AI agent orchestration.

═══════════════════════════════════════════════════════════════════
  WHAT'S INCLUDED
═══════════════════════════════════════════════════════════════════

📦 Package Contents:
  → kernel.json - Core configuration (20 agents, 5 pipelines)
  → README.txt - This file
  → QUICK_REFERENCE.txt - Cheat sheet
  → examples/ - Working example workflows
  → docs/ - Detailed documentation

═══════════════════════════════════════════════════════════════════
  QUICK START (5 MINUTES)
═══════════════════════════════════════════════════════════════════

STEP 1: Verify Requirements
----------------------------
✓ Python 3.8 or higher installed
✓ Basic command line knowledge
✓ Text editor or IDE

Check Python version:
  python --version
  (or python3 --version on Mac/Linux)

STEP 2: Explore the Kernel
----------------------------
Open kernel.json in any text editor to see:
  • 20 specialized agents with descriptions
  • 5 execution pipelines
  • Complete configuration

STEP 3: Load in Python
----------------------------
import json

# Load the kernel
with open('kernel.json', 'r') as f:
    kernel = json.load(f)

# See available agents
for agent in kernel['agents']:
    print(f"Agent {agent['id']}: {agent['role']}")

# See available pipelines
for pipeline in kernel['pipelines']:
    print(f"Pipeline {pipeline['name']}: {pipeline['purpose']}")

STEP 4: Try an Example
----------------------------
Look in examples/ folder for working workflows:
  • csv_processor.json - Batch process CSV files
  • data_validator.json - Validate data quality
  • workflow_orchestrator.json - Multi-step automation

═══════════════════════════════════════════════════════════════════
  THE 20 AGENTS (QUICK OVERVIEW)
═══════════════════════════════════════════════════════════════════

CORE AGENTS:
  1  - Recursive: Break tasks into subtasks
  4  - Validation: Verify quality
  8  - Clarifier: Resolve ambiguity
  13 - Planner: Create execution plans
  17 - Execution: Run tasks

DATA AGENTS:
  21 - Translation: Convert formats (CSV↔JSON↔XML)
  25 - Compression: Package files
  5  - Transformation: Modify data

SYSTEM AGENTS:
  11 - Integrity: Verify data integrity
  12 - Security: Control access
  30 - Channel: Route work
  40 - Observer: Log activity

STATE AGENTS:
  50 - Recovery: Restore from backups
  51 - Snapshot: Save state
  52 - Replay: Reproduce events

INTERFACE AGENTS:
  57 - Interface: Create displays
  61 - Awareness: Monitor health
  62 - Adaptation: Optimize
  63 - OperatorFlow: Maintain control
  64 - Synthesizer: Combine results

═══════════════════════════════════════════════════════════════════
  THE 5 PIPELINES (QUICK OVERVIEW)
═══════════════════════════════════════════════════════════════════

P-01 MAP
  Purpose: Parse and structure input
  Stages: skeleton → lex → ast → normalize → index
  Use: Understanding unstructured input

P-02 CLEANSE
  Purpose: Clean and validate data
  Stages: trim → dedup → validate → sanitize
  Use: Data quality assurance

P-03 SURGE
  Purpose: Accelerate execution
  Stages: batch → parallel → throttle → optimize
  Use: High-performance processing

P-04 LOCK
  Purpose: Apply constraints
  Stages: check_caps → enforce_scope → rate_limit
  Use: Safety and resource control

P-05 SILENCE
  Purpose: Control output
  Stages: filter → suppress → mute
  Use: Reduce noise, focus on signals

═══════════════════════════════════════════════════════════════════
  TYPICAL WORKFLOW
═══════════════════════════════════════════════════════════════════

1. DECOMPOSE (Agent 1 - Recursive)
   Break complex task into subtasks
   
2. PLAN (Agent 13 - Planner)
   Create execution sequence with dependencies
   
3. ROUTE (Agent 30 - Channel)
   Distribute work to appropriate agents
   
4. PROCESS (Pipelines P-01 through P-05)
   Execute via appropriate pipeline
   
5. VALIDATE (Agent 4 - Validation)
   Verify output meets requirements
   
6. SYNTHESIZE (Agent 64 - Synthesizer)
   Combine results into final output

═══════════════════════════════════════════════════════════════════
  EXAMPLE USE CASES
═══════════════════════════════════════════════════════════════════

✓ CSV Batch Processing
  Use: Agents 1,13,30 + Pipeline P-02 + Agent 64
  
✓ Data Validation Pipeline
  Use: Pipeline P-02 + Agent 4
  
✓ Multi-Format Conversion
  Use: Agent 21 + Pipeline P-01
  
✓ Parallel File Processing
  Use: Agent 30 + Pipeline P-03
  
✓ System Monitoring
  Use: Agent 40 + Agent 61
  
✓ Backup and Recovery
  Use: Agent 51 + Agent 50

═══════════════════════════════════════════════════════════════════
  INTEGRATION EXAMPLES
═══════════════════════════════════════════════════════════════════

EXAMPLE 1: Simple Task Decomposition
-------------------------------------
import json

kernel = json.load(open('kernel.json'))
recursive_agent = [a for a in kernel['agents'] if a['id'] == 1][0]

task = "Process 100 CSV files, validate data, merge results"

# Use recursive agent concept to decompose
subtasks = [
    "Find all CSV files in directory",
    "For each CSV: read and parse",
    "For each CSV: run validation",
    "Collect all valid records",
    "Merge into single output file"
]

print(f"Original task: {task}")
print(f"\nDecomposed using {recursive_agent['role']} agent:")
for i, subtask in enumerate(subtasks, 1):
    print(f"  {i}. {subtask}")


EXAMPLE 2: Pipeline Selection
------------------------------
import json

kernel = json.load(open('kernel.json'))

def choose_pipeline(task_type):
    """Select appropriate pipeline for task type"""
    
    pipeline_map = {
        'parse': 'P-01 (MAP)',
        'clean': 'P-02 (CLEANSE)',
        'speed': 'P-03 (SURGE)',
        'limit': 'P-04 (LOCK)',
        'quiet': 'P-05 (SILENCE)'
    }
    
    return pipeline_map.get(task_type, 'Unknown')

print("Parsing data?", choose_pipeline('parse'))
print("Need speed?", choose_pipeline('speed'))
print("Data dirty?", choose_pipeline('clean'))


EXAMPLE 3: Agent Coordination
------------------------------
import json

kernel = json.load(open('kernel.json'))

# Simulate multi-agent workflow
workflow = {
    'step_1': {'agent': 1, 'action': 'Decompose task'},
    'step_2': {'agent': 13, 'action': 'Create plan'},
    'step_3': {'agent': 30, 'action': 'Route work'},
    'step_4': {'agent': 17, 'action': 'Execute'},
    'step_5': {'agent': 4, 'action': 'Validate'},
    'step_6': {'agent': 64, 'action': 'Synthesize'}
}

print("Workflow Execution:")
for step, info in workflow.items():
    agent = [a for a in kernel['agents'] if a['id'] == info['agent']][0]
    print(f"{step}: Agent {agent['id']} ({agent['role']}) - {info['action']}")

═══════════════════════════════════════════════════════════════════
  ADVANCED USAGE
═══════════════════════════════════════════════════════════════════

For detailed guides on:
  • Building custom workflows
  • Chaining multiple agents
  • Pipeline optimization
  • Error handling strategies
  • Production deployment

See the docs/ folder for complete documentation.

═══════════════════════════════════════════════════════════════════
  LICENSE & COMMERCIAL USE
═══════════════════════════════════════════════════════════════════

LICENSE TYPE: Single User

What you CAN do:
  ✓ Use in unlimited personal projects
  ✓ Use in commercial applications
  ✓ Modify and customize for your needs
  ✓ Integrate into your software
  ✓ Use at your company/organization

What you CANNOT do:
  ✗ Redistribute or resell GHOSTLINK itself
  ✗ Share your license with others
  ✗ Include in open source packages
  ✗ Use on more than one team without additional licenses

For team licenses or questions, contact: support@ghostlink.example

═══════════════════════════════════════════════════════════════════
  UPDATES & SUPPORT
═══════════════════════════════════════════════════════════════════

VERSION: 2025.10.08 (Starter v1)

UPDATES:
  • Lifetime updates for version 2025.10.08
  • Bug fixes and patches included
  • Major version upgrades sold separately
  • Check your Gumroad library for updates

SUPPORT:
  • Documentation: See docs/ folder
  • Examples: See examples/ folder
  • Community: [Forum link - add yours]
  • Email: support@ghostlink.example (replace with yours)
  • Response time: 24-48 hours

═══════════════════════════════════════════════════════════════════
  UPGRADE OPTIONS
═══════════════════════════════════════════════════════════════════

Want more power?

GHOSTLINK PRO ($99)
  • All 64 agents (vs 20 in Starter)
  • All 12 pipelines (vs 5 in Starter)
  • Advanced orchestration features
  • Priority support
  • 6 months updates

GHOSTLINK ENTERPRISE ($299)
  • Everything in Pro
  • Custom agent development kit
  • White-label licensing
  • API integration templates
  • 1 year updates
  • 24h priority support

Contact for upgrade discount codes!

═══════════════════════════════════════════════════════════════════
  NEXT STEPS
═══════════════════════════════════════════════════════════════════

1. ✓ Read this README (you're here!)
2. → Open QUICK_REFERENCE.txt for cheat sheet
3. → Explore kernel.json configuration
4. → Try examples in examples/ folder
5. → Read docs/ for detailed guides
6. → Build your first automation!

═══════════════════════════════════════════════════════════════════
  QUESTIONS?
═══════════════════════════════════════════════════════════════════

Stuck? Need help?

• Check QUICK_REFERENCE.txt for common patterns
• Look in examples/ for working code
• Read docs/ for detailed explanations
• Email: support@ghostlink.example

═══════════════════════════════════════════════════════════════════

Happy Automating!

The GHOSTLINK Team

═══════════════════════════════════════════════════════════════════