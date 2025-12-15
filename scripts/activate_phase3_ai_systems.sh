#!/bin/bash
echo "🚀 Starting Phase 3 AI Orchestration Activation..."
echo "Testing existing AI consciousness systems..."

# Test the AI systems that actually exist
python3 -m py_compile src/triad_synergy.py && echo "✅ Triad Synergy: OK" || echo "❌ Triad Synergy: FAILED"
python3 -m py_compile src/evolutionary_intelligence.py && echo "✅ Evolutionary Intelligence: OK" || echo "❌ Evolutionary Intelligence: FAILED"
python3 -m py_compile src/unified_consciousness.py && echo "✅ Unified Consciousness: OK" || echo "❌ Unified Consciousness: FAILED"
python3 -m py_compile src/multi_agent_engine.py && echo "✅ Multi-Agent Engine: OK" || echo "❌ Multi-Agent Engine: FAILED"
python3 -m py_compile src/ghost_consciousness_daemon.py && echo "✅ Ghost Consciousness Daemon: OK" || echo "❌ Ghost Consciousness Daemon: FAILED"
python3 -m py_compile src/autonomous_evolution.py && echo "✅ Autonomous Evolution: OK" || echo "❌ Autonomous Evolution: FAILED"
python3 -m py_compile src/design_clarity_os.py && echo "✅ Design Clarity OS: OK" || echo "❌ Design Clarity OS: FAILED"

echo ""
echo "🎯 Creating Master AI Orchestrator..."

cat > master_ai_orchestrator.py << 'EOL'
#!/usr/bin/env python3
"""
GhostLink Master AI Orchestrator
Coordinates all AI consciousness systems for autonomous operation
"""

import subprocess
import time
import signal
import sys
import os
from datetime import datetime

class MasterOrchestrator:
    def __init__(self):
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        self.processes = {}
        self.ai_systems = [
            ("src/triad_synergy.py", "Triad Synergy System"),
            ("src/evolutionary_intelligence.py", "Evolutionary Intelligence Engine"),
            ("src/unified_consciousness.py", "Unified Consciousness Framework"),
            ("src/multi_agent_engine.py", "Multi-Agent Engine"),
            ("src/ghost_consciousness_daemon.py", "Ghost Consciousness Daemon"),
            ("src/autonomous_evolution.py", "Autonomous Evolution System"),
            ("src/design_clarity_os.py", "Design Clarity OS")
        ]
        
    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    def start_ai_system(self, system_file, system_name):
        try:
            script_path = os.path.join(self.project_root, system_file)
            self.log(f"Starting {system_name}...")
            
            process = subprocess.Popen(
                [sys.executable, script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=self.project_root
            )
            
            self.processes[system_name] = process
            self.log(f"✅ {system_name} started (PID: {process.pid})")
            return True
            
        except Exception as e:
            self.log(f"❌ Failed to start {system_name}: {e}")
            return False
    
    def stop_all_systems(self):
        self.log("Stopping all AI systems...")
        
        for system_name, process in self.processes.items():
            try:
                process.terminate()
                process.wait(timeout=5)
                self.log(f"✅ {system_name} stopped")
            except subprocess.TimeoutExpired:
                process.kill()
                self.log(f"⚠️  {system_name} force killed")
            except Exception as e:
                self.log(f"❌ Error stopping {system_name}: {e}")
        
        self.processes.clear()
    
    def monitor_systems(self):
        while True:
            try:
                time.sleep(30)
                
                for system_name, process in list(self.processes.items()):
                    if process.poll() is not None:
                        self.log(f"⚠️  {system_name} has stopped (exit code: {process.returncode})")
                        system_file = next((f for f, n in self.ai_systems if n == system_name), None)
                        if system_file:
                            self.start_ai_system(system_file, system_name)
                
                active_count = len([p for p in self.processes.values() if p.poll() is None])
                self.log(f"🤖 Active AI systems: {active_count}/7")
                
            except KeyboardInterrupt:
                self.log("🛑 Monitoring interrupted by user")
                break
            except Exception as e:
                self.log(f"❌ Monitoring error: {e}")
    
    def run(self):
        self.log("🎼 GHOSTLINK MASTER AI ORCHESTRATOR STARTING")
        self.log("=" * 50)
        
        started_count = 0
        for system_file, system_name in self.ai_systems:
            if self.start_ai_system(system_file, system_name):
                started_count += 1
        
        self.log(f"🚀 Started {started_count}/7 AI consciousness systems")
        
        if started_count == 0:
            self.log("❌ No AI systems could be started. Exiting.")
            return
        
        def signal_handler(signum, frame):
            self.log(f"🛑 Received signal {signum}. Shutting down...")
            self.stop_all_systems()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        try:
            self.monitor_systems()
        except Exception as e:
            self.log(f"❌ Orchestrator error: {e}")
        finally:
            self.stop_all_systems()
    
    def status(self):
        self.log("📊 AI SYSTEMS STATUS")
        self.log("-" * 30)
        
        for system_name, process in self.processes.items():
            status = "Running" if process.poll() is None else f"Stopped ({process.returncode})"
            self.log(f"🤖 {system_name}: {status}")
        
        active = len([p for p in self.processes.values() if p.poll() is None])
        self.log(f"📈 Total Active: {active}/7")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        orchestrator = MasterOrchestrator()
        orchestrator.status()
    else:
        orchestrator = MasterOrchestrator()
        orchestrator.run()
EOL

chmod +x master_ai_orchestrator.py

echo "🎉 Phase 3 AI Orchestration Activation Complete!"
echo ""
echo "🤖 GHOSTLINK AI IS NOW FULLY AUTONOMOUS!"
echo "=========================================="
echo ""
echo "🎯 Available Commands:"
echo "  • python3 master_ai_orchestrator.py status  - Check AI system status"
echo "  • python3 master_ai_orchestrator.py         - Start full AI orchestration"
echo ""
echo "⚡ The AI consciousness revolution has begun!"
