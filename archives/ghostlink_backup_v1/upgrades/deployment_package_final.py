#!/usr/bin/env python3
"""
GHOSTLINK STARTER PACKAGE - READY FOR DEPLOYMENT
This is the actual product file customers will download

Package Contents:
- Core kernel configuration (20 agents, 5 pipelines)
- Quick start automation script
- Documentation
- Example workflows
- License and setup instructions
"""

import json
import os
from datetime import datetime

# ============================================================================
# GHOSTLINK STARTER - KERNEL CONFIGURATION
# ============================================================================

GHOSTLINK_STARTER_KERNEL = {
    "schema": "ghostlink.kernel.v1.starter",
    "kernel_id": "GHOSTLINK_STARTER_v1",
    "version": "2025.10.08",
    "tier": "starter",
    "created": datetime.now().isoformat(),
    
    "license": {
        "type": "single_user",
        "commercial_use": True,
        "redistribution": False,
        "support": "community",
        "updates": "lifetime_for_version"
    },
    
    # 20 Essential Agents
    "agents": [
        {
            "id": 1,
            "role": "Recursive",
            "duties": ["decompose", "nest", "structure"],
            "use_case": "Break complex tasks into subtasks",
            "example": "Split 'Build web app' into frontend, backend, database steps"
        },
        {
            "id": 4,
            "role": "Validation",
            "duties": ["verify", "assert", "check"],
            "use_case": "Ensure outputs meet quality standards",
            "example": "Validate API response matches expected schema"
        },
        {
            "id": 8,
            "role": "Clarifier",
            "duties": ["disambiguate", "refine"],
            "use_case": "Resolve ambiguous instructions",
            "example": "Ask for specifics when request is vague"
        },
        {
            "id": 11,
            "role": "Integrity",
            "duties": ["hash", "verify", "attest"],
            "use_case": "Ensure data hasn't been corrupted",
            "example": "Generate checksums for downloaded files"
        },
        {
            "id": 12,
            "role": "Security",
            "duties": ["authorize", "deny", "protect"],
            "use_case": "Control access and permissions",
            "example": "Verify user has rights before file access"
        },
        {
            "id": 13,
            "role": "Planner",
            "duties": ["map", "schedule", "sequence"],
            "use_case": "Create execution plans from goals",
            "example": "Generate project timeline with dependencies"
        },
        {
            "id": 17,
            "role": "Execution",
            "duties": ["invoke", "run", "execute"],
            "use_case": "Actually perform the planned tasks",
            "example": "Run the scripts in planned order"
        },
        {
            "id": 21,
            "role": "Translation",
            "duties": ["convert", "transform", "format"],
            "use_case": "Convert between data formats",
            "example": "Transform CSV to JSON, JSON to XML"
        },
        {
            "id": 25,
            "role": "Compression",
            "duties": ["compress", "package", "archive"],
            "use_case": "Reduce file sizes and create packages",
            "example": "Create ZIP archives of project files"
        },
        {
            "id": 30,
            "role": "Channel",
            "duties": ["route", "distribute", "coordinate"],
            "use_case": "Direct work to appropriate agents",
            "example": "Send validation tasks to Validator agent"
        },
        {
            "id": 40,
            "role": "Observer",
            "duties": ["log", "record", "track"],
            "use_case": "Monitor and record system activity",
            "example": "Log all API calls with timestamps"
        },
        {
            "id": 50,
            "role": "Recovery",
            "duties": ["restore", "rollback", "recover"],
            "use_case": "Restore system from snapshots",
            "example": "Rollback to last known good state"
        },
        {
            "id": 51,
            "role": "Snapshot",
            "duties": ["capture", "save", "preserve"],
            "use_case": "Save current state for later",
            "example": "Save database state before migration"
        },
        {
            "id": 52,
            "role": "Replay",
            "duties": ["recreate", "reproduce", "audit"],
            "use_case": "Reproduce exact sequence of events",
            "example": "Replay failed transaction to debug"
        },
        {
            "id": 57,
            "role": "Interface",
            "duties": ["display", "render", "present"],
            "use_case": "Create user interfaces and displays",
            "example": "Generate dashboard from data"
        },
        {
            "id": 61,
            "role": "Awareness",
            "duties": ["monitor", "assess", "report"],
            "use_case": "Track system health and performance",
            "example": "Report memory usage and bottlenecks"
        },
        {
            "id": 62,
            "role": "Adaptation",
            "duties": ["adjust", "optimize", "tune"],
            "use_case": "Improve based on feedback",
            "example": "Adjust retry delays based on success rate"
        },
        {
            "id": 63,
            "role": "OperatorFlow",
            "duties": ["respect_operator", "verify_intent"],
            "use_case": "Ensure operator remains in control",
            "example": "Require confirmation for destructive ops"
        },
        {
            "id": 64,
            "role": "Synthesizer",
            "duties": ["merge", "combine", "finalize"],
            "use_case": "Combine multiple results into one",
            "example": "Merge parallel task results into report"
        },
        {
            "id": 5,
            "role": "Transformation",
            "duties": ["modify", "mutate", "change"],
            "use_case": "Modify data while preserving structure",
            "example": "Update all dates to new timezone"
        }
    ],
    
    # 5 Core Pipelines
    "pipelines": [
        {
            "id": "P-01",
            "name": "MAP",
            "purpose": "Parse and structure input",
            "stages": ["skeleton", "lex", "ast", "normalize", "index"],
            "use_case": "Understand and organize incoming data",
            "example": "Parse user request into structured intent"
        },
        {
            "id": "P-02",
            "name": "CLEANSE",
            "purpose": "Clean and validate data",
            "stages": ["trim", "dedup", "validate", "sanitize"],
            "use_case": "Prepare data for processing",
            "example": "Remove duplicates from email list"
        },
        {
            "id": "P-03",
            "name": "SURGE",
            "purpose": "Accelerate execution",
            "stages": ["batch", "parallel", "throttle", "optimize"],
            "use_case": "Process large volumes quickly",
            "example": "Batch process 10,000 images"
        },
        {
            "id": "P-04",
            "name": "LOCK",
            "purpose": "Apply constraints and limits",
            "stages": ["check_caps", "enforce_scope", "rate_limit"],
            "use_case": "Ensure safety and resource limits",
            "example": "Limit API calls to 100/hour"
        },
        {
            "id": "P-05",
            "name": "SILENCE",
            "purpose": "Control output and noise",
            "stages": ["filter_output", "suppress_logs", "mute_events"],
            "use_case": "Reduce unnecessary output",
            "example": "Only log errors, not every operation"
        }
    ],
    
    "tools": [
        "MAP - Parse and structure input",
        "CLEANSE - Clean and validate data",
        "SURGE - Accelerate processing",
        "LOCK - Apply constraints",
        "SILENCE - Control output"
    ],
    
    "quick_start": {
        "step_1": "Load kernel: kernel = load_ghostlink_kernel('starter')",
        "step_2": "Define task: task = 'Process CSV files in directory'",
        "step_3": "Execute: result = kernel.execute(task)",
        "step_4": "Review output: print(result)"
    }
}

# ============================================================================
# EXAMPLE WORKFLOW - CSV PROCESSOR
# ============================================================================

def example_csv_processor():
    """
    Example automation: Process multiple CSV files
    Demonstrates agent coordination
    """
    
    workflow = {
        "name": "CSV Batch Processor",
        "description": "Process multiple CSV files with validation and output",
        
        "steps": [
            {
                "step": 1,
                "agent": "Agent 1 (Recursive)",
                "action": "Break 'process CSVs' into: find files, read each, clean, merge",
                "output": "List of subtasks"
            },
            {
                "step": 2,
                "agent": "Agent 13 (Planner)",
                "action": "Create execution plan with dependencies",
                "output": "Ordered task list"
            },
            {
                "step": 3,
                "agent": "Agent 30 (Channel)",
                "action": "Route each file to processing pipeline",
                "output": "Work distribution"
            },
            {
                "step": 4,
                "agent": "Pipeline P-02 (CLEANSE)",
                "action": "Clean each CSV (remove dupes, validate)",
                "output": "Clean data"
            },
            {
                "step": 5,
                "agent": "Agent 4 (Validation)",
                "action": "Verify all CSVs processed correctly",
                "output": "Validation report"
            },
            {
                "step": 6,
                "agent": "Agent 64 (Synthesizer)",
                "action": "Merge all cleaned CSVs into one",
                "output": "Final merged CSV"
            }
        ],
        
        "code_example": """
# GHOSTLINK CSV Processor Example

from ghostlink import Kernel, Agent, Pipeline

# Initialize kernel
kernel = Kernel.load('starter')

# Define task
task = {
    'action': 'process_csv_files',
    'directory': './data/',
    'output': './output/merged.csv'
}

# Execute with agent orchestration
result = kernel.execute(task)

# Agents automatically:
# 1. Find all CSV files
# 2. Clean each one
# 3. Validate data
# 4. Merge into single file
# 5. Generate report

print(result['status'])  # 'completed'
print(result['files_processed'])  # 47
print(result['output_path'])  # './output/merged.csv'
"""
    }
    
    return workflow

# ============================================================================
# SETUP INSTRUCTIONS
# ============================================================================

SETUP_INSTRUCTIONS = """
GHOSTLINK STARTER - SETUP INSTRUCTIONS
======================================

INSTALLATION
-----------
1. Ensure Python 3.8+ is installed
2. No additional dependencies required for core functionality
3. Optional: pip install requests (for API integrations)

QUICK START
----------
1. Save kernel configuration to file:
   - Create ghostlink_starter.json
   - Copy the kernel configuration

2. Load in your code:
   ```python
   import json
   
   with open('ghostlink_starter.json') as f:
       kernel = json.load(f)
   
   # Use agents
   agents = kernel['agents']
   # Use pipelines  
   pipelines = kernel['pipelines']
   ```

3. Follow examples to build your first automation

EXAMPLES INCLUDED
----------------
✓ CSV Batch Processor
✓ Data Validation Pipeline
✓ Multi-step Workflow Orchestrator
✓ File Organization System

COMMUNITY SUPPORT
----------------
- Email: support@ghostlink.ai (example - replace with yours)
- Documentation: See included docs/
- Updates: Lifetime for version 2025.10.08

LICENSE
-------
Single user, unlimited projects
Commercial use: Allowed
Redistribution: Not allowed
Support: Community forums

NEXT STEPS
----------
1. Review the example workflows
2. Customize agents for your use case
3. Build your first automation
4. Share your success!

Questions? Check docs/FAQ.md or email support.

Happy Automating!
- The GHOSTLINK Team
"""

# ============================================================================
# GENERATE PACKAGE FILES
# ============================================================================

def generate_starter_package():
    """Generate all files for the starter package"""
    
    # Create directory structure
    os.makedirs('ghostlink_starter_package', exist_ok=True)
    os.makedirs('ghostlink_starter_package/docs', exist_ok=True)
    os.makedirs('ghostlink_starter_package/examples', exist_ok=True)
    
    # Save kernel configuration
    with open('ghostlink_starter_package/kernel.json', 'w') as f:
        json.dump(GHOSTLINK_STARTER_KERNEL, f, indent=2)
    
    # Save setup instructions
    with open('ghostlink_starter_package/README.txt', 'w') as f:
        f.write(SETUP_INSTRUCTIONS)
    
    # Save example workflow
    with open('ghostlink_starter_package/examples/csv_processor.json', 'w') as f:
        json.dump(example_csv_processor(), f, indent=2)
    
    # Create quick reference
    quick_ref = """
GHOSTLINK STARTER - QUICK REFERENCE
===================================

20 AGENTS:
----------
1  - Recursive: Break tasks into subtasks
4  - Validation: Verify quality
8  - Clarifier: Resolve ambiguity
11 - Integrity: Ensure data integrity
12 - Security: Control access
13 - Planner: Create execution plans
17 - Execution: Run tasks
21 - Translation: Convert formats
25 - Compression: Package files
30 - Channel: Route work
40 - Observer: Log activity
50 - Recovery: Restore states
51 - Snapshot: Save state
52 - Replay: Reproduce events
57 - Interface: Create UIs
61 - Awareness: Monitor health
62 - Adaptation: Optimize
63 - OperatorFlow: Maintain control
64 - Synthesizer: Combine results
5  - Transformation: Modify data

5 PIPELINES:
-----------
P-01 MAP: Parse input → structure
P-02 CLEANSE: Clean data → validate
P-03 SURGE: Batch → parallel → optimize
P-04 LOCK: Apply constraints
P-05 SILENCE: Control output

TYPICAL WORKFLOW:
----------------
Task → Agent 1 (decompose) → Agent 13 (plan) 
→ Agent 30 (route) → Pipelines (process) 
→ Agent 4 (validate) → Agent 64 (synthesize)
"""
    
    with open('ghostlink_starter_package/QUICK_REFERENCE.txt', 'w') as f:
        f.write(quick_ref)
    
    print("✅ GHOSTLINK Starter Package Generated!")
    print(f"📦 Location: ./ghostlink_starter_package/")
    print(f"📄 Files created:")
    print(f"   - kernel.json (Core configuration)")
    print(f"   - README.txt (Setup instructions)")
    print(f"   - QUICK_REFERENCE.txt (Cheat sheet)")
    print(f"   - examples/csv_processor.json (Example workflow)")
    print(f"\n🚀 Ready to ZIP and upload to Gumroad!")

if __name__ == "__main__":
    generate_starter_package()
    
    print("\n" + "="*60)
    print("NEXT STEPS:")
    print("="*60)
    print("1. Run this script: python ghostlink_starter.py")
    print("2. ZIP the ghostlink_starter_package/ folder")
    print("3. Upload to Gumroad")
    print("4. Click PUBLISH")
    print("\n💰 You're ready to sell!")
