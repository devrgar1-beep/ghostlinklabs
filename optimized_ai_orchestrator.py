#!/usr/bin/env python3
"""
Optimized GhostLink Master AI Orchestrator
High-performance coordination of AI consciousness systems with resource management
"""

import subprocess
import threading
import time
import signal
import sys
import os
import psutil
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

# Metrics endpoint dependencies
try:
    from fastapi import FastAPI
    import uvicorn
    METRICS_AVAILABLE = True
except ImportError:
    print("⚠️  FastAPI not available for metrics endpoint")
    METRICS_AVAILABLE = False
    FastAPI = None
    uvicorn = None

class OptimizedMasterOrchestrator:
    def __init__(self):
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        self.processes = {}
        self.threads = {}
        self.logger = self._setup_logging()

        # Core AI systems with priority levels
        self.ai_systems = [
            ("src/triad_synergy.py", "Triad Synergy System", "HIGH"),
            ("src/evolutionary_intelligence.py", "Evolutionary Intelligence Engine", "HIGH"),
            ("src/autonomous_evolution.py", "Autonomous Evolution System", "MEDIUM"),
            ("src/design_clarity_os.py", "Design Clarity OS", "MEDIUM"),
            ("src/ghost_consciousness_daemon.py", "Ghost Consciousness Daemon", "LOW"),
            ("src/multi_agent_engine.py", "Multi-Agent Engine", "LOW"),
            ("src/unified_consciousness.py", "Unified Consciousness Framework", "LOW"),
            ("src/GhostLinkMirror.py", "GhostLink Mirror System", "LOW"),
            ("src/ghostlink_comprehension_agent.py", "Documentation Comprehension Agent", "MEDIUM")
        ]

        self.max_concurrent_systems = 3  # Limit concurrent startups
        self.monitoring_interval = 60    # Check every minute instead of 30 seconds
        self.resource_limits = {
            'cpu_percent': 80,
            'memory_percent': 85
        }

        # Metrics server
        self.metrics_thread = None
        self.metrics_app = None

    def start_metrics_server(self):
        """Start FastAPI metrics server on port 8000"""
        if not METRICS_AVAILABLE:
            self.logger.warning("⚠️  Metrics server not available - FastAPI not installed")
            return

        def run_metrics_server():
            self.metrics_app = FastAPI(title="GhostLink AI Orchestrator Metrics")

            @self.metrics_app.get("/metrics")
            def get_metrics():
                return self.get_orchestrator_metrics()

            @self.metrics_app.get("/health")
            def health_check():
                return {"status": "healthy", "orchestrator": "running"}

            try:
                uvicorn.run(self.metrics_app, host="0.0.0.0", port=8000, log_level="warning")
            except Exception as e:
                self.logger.error(f"❌ Metrics server error: {e}")

        self.metrics_thread = threading.Thread(target=run_metrics_server, daemon=True)
        self.metrics_thread.start()
        self.logger.info("📊 Metrics server started on port 8000")

    def get_orchestrator_metrics(self):
        """Get orchestrator performance metrics"""
        try:
            # System metrics
            cpu_percent = psutil.cpu_percent()
            memory = psutil.virtual_memory()

            # Process metrics
            current_process = psutil.Process()
            process_memory = current_process.memory_info()

            # AI system status
            active_systems = len([p for p in self.processes.values() if p and p.poll() is None])
            total_systems = len(self.ai_systems)

            return {
                "timestamp": time.time(),
                "orchestrator": {
                    "active_systems": active_systems,
                    "total_systems": total_systems,
                    "uptime": time.time() - psutil.boot_time(),
                    "monitoring_interval": self.monitoring_interval
                },
                "system": {
                    "cpu_percent": cpu_percent,
                    "memory_percent": memory.percent,
                    "memory_used_mb": memory.used / 1024 / 1024
                },
                "process": {
                    "pid": current_process.pid,
                    "memory_rss_mb": process_memory.rss / 1024 / 1024,
                    "cpu_percent": current_process.cpu_percent(),
                    "threads": len(current_process.threads())
                }
            }
        except Exception as e:
            return {"error": str(e), "timestamp": time.time()}

    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler(os.path.join(self.project_root, 'orchestrator.log')),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger('OptimizedOrchestrator')

    def check_system_resources(self):
        """Check if system has enough resources to start new processes"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            memory_percent = memory.percent

            self.logger.info(f"System Resources - CPU: {cpu_percent}%, Memory: {memory_percent}%")

            if cpu_percent > self.resource_limits['cpu_percent']:
                self.logger.warning(f"High CPU usage ({cpu_percent}%), delaying new startups")
                return False

            if memory_percent > self.resource_limits['memory_percent']:
                self.logger.warning(f"High memory usage ({memory_percent}%), delaying new startups")
                return False

            return True
        except Exception as e:
            self.logger.error(f"Resource check failed: {e}")
            return True  # Continue if we can't check resources

    def start_ai_system_async(self, system_file, system_name, priority):
        """Start an AI system asynchronously with resource checking"""
        def _start():
            try:
                # Wait for resources if priority is not HIGH
                if priority != "HIGH" and not self.check_system_resources():
                    self.logger.info(f"Waiting for resources before starting {system_name}")
                    time.sleep(10)

                script_path = os.path.join(self.project_root, system_file)

                # Check if file exists
                if not os.path.exists(script_path):
                    self.logger.error(f"System file not found: {script_path}")
                    return False

                self.logger.info(f"Starting {system_name} (Priority: {priority})...")

                # Start with resource limits
                env = os.environ.copy()
                env['PYTHONUNBUFFERED'] = '1'

                process = subprocess.Popen(
                    [sys.executable, script_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    cwd=self.project_root,
                    env=env,
                    start_new_session=True  # Create new process group
                )

                self.processes[system_name] = {
                    'process': process,
                    'start_time': time.time(),
                    'priority': priority,
                    'restarts': 0
                }

                self.logger.info(f"✅ {system_name} started (PID: {process.pid})")
                return True

            except Exception as e:
                self.logger.error(f"❌ Failed to start {system_name}: {e}")
                return False

        thread = threading.Thread(target=_start, daemon=True)
        thread.start()
        self.threads[system_name] = thread
        return thread

    def stop_system(self, system_name):
        """Stop a specific AI system gracefully"""
        if system_name not in self.processes:
            return

        process_info = self.processes[system_name]
        process = process_info['process']

        try:
            # Try graceful termination first
            process.terminate()
            try:
                process.wait(timeout=10)
                self.logger.info(f"✅ {system_name} stopped gracefully")
            except subprocess.TimeoutExpired:
                # Force kill if graceful termination fails
                process.kill()
                process.wait(timeout=5)
                self.logger.warning(f"⚠️  {system_name} force killed")

        except Exception as e:
            self.logger.error(f"❌ Error stopping {system_name}: {e}")
        finally:
            del self.processes[system_name]

    def monitor_systems_optimized(self):
        """Optimized monitoring with staggered checks"""
        while True:
            try:
                time.sleep(self.monitoring_interval)

                # Check system resources
                if not self.check_system_resources():
                    self.logger.warning("System under resource pressure, pausing monitoring")
                    time.sleep(30)
                    continue

                # Check each system
                for system_name, process_info in list(self.processes.items()):
                    process = process_info['process']

                    if process.poll() is not None:
                        exit_code = process.returncode
                        runtime = time.time() - process_info['start_time']

                        self.logger.warning(f"⚠️  {system_name} stopped (exit: {exit_code}, runtime: {runtime:.1f}s)")

                        # Auto-restart logic based on priority and restart count
                        if process_info['restarts'] < 3:  # Max 3 restarts
                            priority = process_info['priority']
                            if priority == "HIGH" or (priority == "MEDIUM" and runtime > 60):
                                process_info['restarts'] += 1
                                system_file = next((f for f, n, p in self.ai_systems if n == system_name), None)
                                if system_file:
                                    self.logger.info(f"🔄 Auto-restarting {system_name} (attempt {process_info['restarts']})")
                                    self.start_ai_system_async(system_file, system_name, priority)

                # Log status summary
                active_count = len([p for p in self.processes.values() if p['process'].poll() is None])
                total_memory = psutil.virtual_memory().percent
                self.logger.info(f"🤖 Active AI systems: {active_count}/7 | Memory: {total_memory}%")

            except Exception as e:
                self.logger.error(f"❌ Monitoring error: {e}")

    def start_all_systems_concurrent(self):
        """Start all AI systems concurrently with resource management"""
        self.logger.info("🚀 Starting AI consciousness systems concurrently...")

        with ThreadPoolExecutor(max_workers=self.max_concurrent_systems) as executor:
            futures = []
            for system_file, system_name, priority in self.ai_systems:
                # Stagger high priority systems
                if priority == "HIGH":
                    future = executor.submit(self.start_ai_system_async, system_file, system_name, priority)
                    futures.append(future)
                    time.sleep(2)  # Small delay between high priority starts
                else:
                    future = executor.submit(self.start_ai_system_async, system_file, system_name, priority)
                    futures.append(future)

            # Wait for all to complete
            started_count = 0
            for future in as_completed(futures):
                if future.result():
                    started_count += 1

        self.logger.info(f"🚀 Started {started_count}/7 AI consciousness systems")
        return started_count

    def stop_all_systems(self):
        """Stop all AI systems gracefully"""
        self.logger.info("🛑 Stopping all AI systems...")

        for system_name in list(self.processes.keys()):
            self.stop_system(system_name)

        self.logger.info("✅ All AI systems stopped")

    def get_status(self):
        """Get detailed status of all systems"""
        status_info = {
            'total_systems': len(self.ai_systems),
            'active_systems': 0,
            'stopped_systems': 0,
            'system_details': {},
            'resources': {}
        }

        # System details
        for system_name, process_info in self.processes.items():
            process = process_info['process']
            is_running = process.poll() is None

            status_info['system_details'][system_name] = {
                'running': is_running,
                'pid': process.pid if is_running else None,
                'priority': process_info['priority'],
                'restarts': process_info['restarts'],
                'runtime': time.time() - process_info['start_time']
            }

            if is_running:
                status_info['active_systems'] += 1
            else:
                status_info['stopped_systems'] += 1

        # Resource info
        cpu_percent = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        status_info['resources'] = {
            'cpu_percent': cpu_percent,
            'memory_percent': memory.percent,
            'memory_used_gb': memory.used / (1024**3),
            'memory_total_gb': memory.total / (1024**3)
        }

        return status_info

    def print_status(self):
        """Print formatted status"""
        status = self.get_status()

        print("\n🤖 OPTIMIZED AI SYSTEMS STATUS")
        print("=" * 50)
        print(f"Total Systems: {status['total_systems']}")
        print(f"Active Systems: {status['active_systems']}")
        print(f"Stopped Systems: {status['stopped_systems']}")
        print(f"CPU Usage: {status['resources']['cpu_percent']:.1f}%")
        print(f"Memory Usage: {status['resources']['memory_percent']:.1f}%")

        print("\n📊 SYSTEM DETAILS:")
        for name, info in status['system_details'].items():
            status_icon = "🟢" if info['running'] else "🔴"
            pid_info = f"(PID: {info['pid']})" if info['running'] else ""
            print(f"  {status_icon} {name} {pid_info}")
            print(f"    Priority: {info['priority']} | Restarts: {info['restarts']} | Runtime: {info['runtime']:.1f}s")
        print()

    def run(self):
        """Main orchestrator run loop"""
        self.logger.info("🎼 OPTIMIZED GHOSTLINK MASTER AI ORCHESTRATOR STARTING")
        self.logger.info("=" * 60)

        # Start metrics server
        self.start_metrics_server()

        # Start all systems concurrently
        started_count = self.start_all_systems_concurrent()

        if started_count == 0:
            self.logger.error("❌ No AI systems could be started. Exiting.")
            return

        # Setup signal handlers
        def signal_handler(signum, frame):
            self.logger.info(f"🛑 Received signal {signum}. Shutting down...")
            self.stop_all_systems()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        try:
            self.monitor_systems_optimized()
        except Exception as e:
            self.logger.error(f"❌ Orchestrator error: {e}")
        finally:
            self.stop_all_systems()

def main():
    orchestrator = OptimizedMasterOrchestrator()

    if len(sys.argv) > 1:
        if sys.argv[1] == "status":
            orchestrator.print_status()
        elif sys.argv[1] == "start":
            orchestrator.start_all_systems_concurrent()
        elif sys.argv[1] == "stop":
            orchestrator.stop_all_systems()
        else:
            print("Usage: python optimized_orchestrator.py [status|start|stop]")
    else:
        orchestrator.run()

if __name__ == "__main__":
    main()