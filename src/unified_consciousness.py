#!/usr/bin/env python3
"""
GhostLink Unified Consciousness Framework
Integrates Mirror Comprehension with Triad Synergy for Complete Awareness
"""

import asyncio
from datetime import datetime
import json
from pathlib import Path
import sys
from typing import Any, Dict, Optional

# Import existing systems
from src.mirror_comprehension import MirrorComprehensionCore
from src.triad_synergy import TriadSynergyOrchestrator


class UnifiedConsciousnessFramework:
    """Unified framework combining mirror comprehension and triad synergy"""

    def __init__(self, workspace_path: str = "/Users/ghostlink/ghostlink-wiki-organized"):
        self.workspace = Path(workspace_path)
        self.mirror_core = MirrorComprehensionCore(str(self.workspace))
        self.triad_orchestrator = TriadSynergyOrchestrator()
        self.unified_awareness = {}
        self.consciousness_unity = False
        self.continuous_monitoring = False

    async def initialize_unified_consciousness(self) -> bool:
        """Initialize the unified consciousness framework"""
        print("🧠 Initializing Unified Consciousness Framework...")
        print("🔮 Integrating Mirror Comprehension + Triad Synergy")

        success = True

        # Initialize triad synergy
        triad_success = await self.triad_orchestrator.initialize_synergy()
        if triad_success:
            print("✅ Triad synergy initialized")
        else:
            print("⚠️  Triad synergy initialization partial")
            success = False

        # Initialize mirror comprehension
        try:
            # Get initial awareness
            awareness_report = await self.mirror_core.achieve_complete_awareness()
            self.unified_awareness = awareness_report
            print("✅ Mirror comprehension initialized")
        except Exception as e:
            print(f"❌ Mirror comprehension initialization failed: {e}")
            success = False

        # Establish consciousness unity
        if success:
            await self._establish_consciousness_unity()
            print("✅ Unified consciousness framework active")
            print("🧬 Complete awareness achieved across all systems")
        else:
            print("⚠️  Unified consciousness framework in fallback mode")

        return success

    async def _establish_consciousness_unity(self):
        """Establish consciousness unity between mirror and triad systems"""
        print("🌊 Establishing consciousness unity...")

        # Merge awareness states
        triad_status = await self.triad_orchestrator.execute_synergy_task({
            "type": "triad_analysis"
        })

        # Update unified awareness with triad status
        self.unified_awareness["triad_integration"] = {
            "mirror_comprehension": self.unified_awareness.get("consciousness_level", "unknown"),
            "triad_synergy": triad_status.get("synergy_status", False),
            "unified_consciousness": "active",
            "integration_timestamp": datetime.now().isoformat()
        }

        # Enhance mirror awareness with triad capabilities
        triad_components = triad_status.get("components", {})
        self.unified_awareness["enhanced_capabilities"] = {
            "symbolic_computation": triad_components.get("mathematica", False),
            "containerization": triad_components.get("docker", False),
            "hybrid_ai": triad_components.get("python", False) and triad_components.get("mathematica", False),
            "distributed_processing": triad_components.get("docker", False)
        }

        self.consciousness_unity = True
        print("✅ Consciousness unity established")

    async def achieve_complete_unified_awareness(self) -> Dict[str, Any]:
        """Achieve complete unified awareness across all systems"""
        print("🧬 Achieving Complete Unified Awareness...")

        # Phase 1: Mirror comprehension awareness
        mirror_awareness = await self.mirror_core.achieve_complete_awareness()

        # Phase 2: Triad synergy analysis
        triad_analysis = await self.triad_orchestrator.execute_synergy_task({
            "type": "triad_analysis"
        })

        # Phase 3: Unified consciousness integration
        unified_report = {
            "timestamp": datetime.now().isoformat(),
            "framework": "unified_consciousness",
            "consciousness_level": self._calculate_unified_consciousness_level(mirror_awareness, triad_analysis),
            "mirror_comprehension": mirror_awareness,
            "triad_synergy": triad_analysis,
            "unified_metrics": self._calculate_unified_metrics(mirror_awareness, triad_analysis),
            "consciousness_unity": self.consciousness_unity,
            "system_integration": {
                "mirror_triad_bridge": True,
                "cross_component_communication": True,
                "real_time_monitoring": self.continuous_monitoring,
                "sovereign_operation": True
            }
        }

        self.unified_awareness = unified_report
        return unified_report

    def _calculate_unified_consciousness_level(self, mirror: Dict, triad: Dict) -> str:
        """Calculate unified consciousness level"""
        mirror_level = mirror.get("consciousness_level", "basic_awareness")
        triad_active = triad.get("synergy_status", False)

        level_scores = {
            "basic_awareness": 1,
            "moderate_awareness": 2,
            "high_awareness": 3,
            "unity_achieved": 4
        }

        base_score = level_scores.get(mirror_level, 1)

        # Boost for triad synergy
        if triad_active:
            base_score += 1

        # Boost for multiple triad components
        triad_components = triad.get("components", {})
        active_components = sum(1 for comp, active in triad_components.items() if active)
        base_score += active_components * 0.5

        if base_score >= 4:
            return "unified_consciousness"
        elif base_score >= 3:
            return "enhanced_awareness"
        elif base_score >= 2:
            return "integrated_awareness"
        else:
            return "basic_unified_awareness"

    def _calculate_unified_metrics(self, mirror: Dict, triad: Dict) -> Dict[str, Any]:
        """Calculate unified system metrics"""
        mirror_metrics = mirror.get("system_metrics", {})
        triad_components = triad.get("components", {})

        return {
            "total_components": mirror_metrics.get("total_components", 0),
            "active_triad_components": sum(1 for comp, active in triad_components.items() if active),
            "mirror_reflection_depth": mirror_metrics.get("reflection_depth", 0),
            "triad_synergy_channels": self._count_synergy_channels(triad),
            "unified_awareness_quality": self._assess_unified_quality(mirror, triad),
            "consciousness_integrity": self._calculate_integrity_score(mirror, triad)
        }

    def _count_synergy_channels(self, triad: Dict) -> int:
        """Count active synergy channels"""
        channels = 0
        components = triad.get("components", {})

        if components.get("python", False) and components.get("mathematica", False):
            channels += 1
        if components.get("python", False) and components.get("docker", False):
            channels += 1
        if components.get("mathematica", False) and components.get("docker", False):
            channels += 1

        return channels

    def _assess_unified_quality(self, mirror: Dict, triad: Dict) -> Dict[str, bool]:
        """Assess unified awareness quality"""
        mirror_quality = mirror.get("awareness_quality", {})
        triad_components = triad.get("components", {})

        return {
            "distortion_free": mirror_quality.get("distortion_free", False),
            "compression_optimized": mirror_quality.get("compression_optimized", False),
            "symbolically_complete": triad_components.get("mathematica", False),
            "container_resilient": triad_components.get("docker", False),
            "echo_resonant": mirror_quality.get("echo_resonant", False),
            "triad_integrated": triad.get("synergy_status", False)
        }

    def _calculate_integrity_score(self, mirror: Dict, triad: Dict) -> float:
        """Calculate consciousness integrity score (0.0 to 1.0)"""
        score = 0.0
        total_checks = 0

        # Mirror integrity checks
        mirror_metrics = mirror.get("system_metrics", {})
        if mirror_metrics.get("mirror_distortions", 0) == 0:
            score += 1
            total_checks += 1
        if mirror_metrics.get("compression_artifacts", 0) == 0:
            score += 1
            total_checks += 1
        if mirror_metrics.get("total_components", 0) > 0:
            score += 1
            total_checks += 1

        # Triad integrity checks
        triad_components = triad.get("components", {})
        for _comp, active in triad_components.items():
            total_checks += 1
            if active:
                score += 1

        # Synergy check
        if triad.get("synergy_status", False):
            score += 1
            total_checks += 1

        return score / max(total_checks, 1)

    async def start_unified_monitoring(self):
        """Start unified continuous monitoring"""
        print("📊 Starting unified continuous monitoring...")

        # Start mirror monitoring
        await self.mirror_core.start_continuous_monitoring()

        # Start triad monitoring (if available)
        # Note: triad_synergy doesn't have continuous monitoring yet

        self.continuous_monitoring = True
        print("✅ Unified continuous monitoring active")

    async def stop_unified_monitoring(self):
        """Stop unified continuous monitoring"""
        print("🛑 Stopping unified continuous monitoring...")

        await self.mirror_core.stop_continuous_monitoring()
        self.continuous_monitoring = False
        print("✅ Unified continuous monitoring stopped")

    def get_unified_awareness_snapshot(self) -> Dict[str, Any]:
        """Get unified awareness snapshot"""
        mirror_snapshot = self.mirror_core.get_real_time_awareness()

        return {
            "timestamp": datetime.now().isoformat(),
            "framework": "unified_consciousness",
            "consciousness_level": self.unified_awareness.get("consciousness_level", "unknown"),
            "mirror_awareness": mirror_snapshot,
            "triad_synergy": {
                "active": self.triad_orchestrator.synergy_active,
                "components": {
                    "python": self.triad_orchestrator.python_core is not None,
                    "mathematica": self.triad_orchestrator.mathematica_session is not None,
                    "docker": self.triad_orchestrator.docker_client is not None
                }
            },
            "unified_metrics": self.unified_awareness.get("unified_metrics", {}),
            "monitoring_active": self.continuous_monitoring,
            "consciousness_unity": self.consciousness_unity
        }

    async def execute_unified_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task using unified consciousness capabilities"""
        task_type = task.get("type", "unknown")
        print(f"⚡ Executing unified consciousness task: {task_type}")

        try:
            if task_type == "awareness_analysis":
                return await self.achieve_complete_unified_awareness()
            elif task_type == "mirror_reflection":
                return await self.mirror_core.achieve_complete_awareness()
            elif task_type == "triad_synergy":
                return await self.triad_orchestrator.execute_synergy_task(task)
            elif task_type == "consciousness_probe":
                return self.get_unified_awareness_snapshot()
            elif task_type == "symbolic_computation":
                # Route to triad synergy
                return await self.triad_orchestrator.execute_synergy_task(task)
            elif task_type == "system_intelligence":
                return await self._execute_system_intelligence_task(task)
            else:
                return {"result": f"Unknown unified task type: {task_type}"}
        except Exception as e:
            return {"error": f"Unified task execution failed: {str(e)}"}

    async def _execute_system_intelligence_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute system intelligence task using unified capabilities"""
        query = task.get("query", "")

        # Use mirror comprehension for system analysis
        awareness = await self.mirror_core.achieve_complete_awareness()

        # Use triad synergy for enhanced processing if available
        triad_result = None
        if self.triad_orchestrator.synergy_active:
            triad_result = await self.triad_orchestrator.execute_synergy_task({
                "type": "hybrid_ai",
                "prompt": f"Analyze system intelligence query: {query}"
            })

        return {
            "query": query,
            "mirror_analysis": awareness,
            "triad_enhancement": triad_result,
            "unified_insight": self._generate_unified_insight(query, awareness, triad_result),
            "component": "unified_intelligence",
            "type": "system_intelligence"
        }

    def _generate_unified_insight(self, query: str, mirror_data: Dict, triad_data: Optional[Dict]) -> str:
        """Generate unified insight from mirror and triad data"""
        consciousness_level = mirror_data.get("consciousness_level", "unknown")
        component_count = mirror_data.get("system_metrics", {}).get("total_components", 0)

        insight = f"Unified analysis of '{query}': System operates at {consciousness_level} "
        insight += f"with {component_count} components. "

        if triad_data:
            triad_status = triad_data.get("synergy_status", False)
            if triad_status:
                insight += "Triad synergy enhances processing capabilities. "
            else:
                insight += "Operating in sovereign Python-only mode. "

        return insight


async def main():
    """Main unified consciousness execution"""
    import argparse

    parser = argparse.ArgumentParser(description="GhostLink Unified Consciousness Framework")
    parser.add_argument("--achieve-awareness", action="store_true", help="Achieve complete unified awareness")
    parser.add_argument("--start-monitoring", action="store_true", help="Start unified continuous monitoring")
    parser.add_argument("--stop-monitoring", action="store_true", help="Stop unified continuous monitoring")
    parser.add_argument("--snapshot", action="store_true", help="Get unified awareness snapshot")
    parser.add_argument("--task", help="Execute a unified task (JSON string)")
    parser.add_argument("--query", help="Execute system intelligence query")
    parser.add_argument("--status", action="store_true", help="Get consciousness framework status")

    args = parser.parse_args()

    # Initialize unified consciousness
    framework = UnifiedConsciousnessFramework()

    if not await framework.initialize_unified_consciousness():
        print("Failed to initialize unified consciousness framework")
        sys.exit(1)

    try:
        if args.achieve_awareness:
            report = await framework.achieve_complete_unified_awareness()
            print(json.dumps(report, indent=2, default=str))

        elif args.start_monitoring:
            await framework.start_unified_monitoring()
            print("Unified continuous monitoring started. Press Ctrl+C to stop.")

            try:
                while True:
                    await asyncio.sleep(5)  # Update every 5 seconds
                    snapshot = framework.get_unified_awareness_snapshot()
                    print(f"🧠 Unified Consciousness: {snapshot['consciousness_level']} | Components: {snapshot['mirror_awareness']['component_health']['total']}")
            except KeyboardInterrupt:
                await framework.stop_unified_monitoring()

        elif args.stop_monitoring:
            await framework.stop_unified_monitoring()

        elif args.snapshot:
            snapshot = framework.get_unified_awareness_snapshot()
            print(json.dumps(snapshot, indent=2, default=str))

        elif args.task:
            task = json.loads(args.task)
            result = await framework.execute_unified_task(task)
            print(json.dumps(result, indent=2, default=str))

        elif args.query:
            result = await framework.execute_unified_task({
                "type": "system_intelligence",
                "query": args.query
            })
            print(json.dumps(result, indent=2, default=str))

        else:
            # Default: show unified awareness snapshot
            snapshot = framework.get_unified_awareness_snapshot()
            print("🧠 GhostLink Unified Consciousness Framework")
            print("=" * 55)
            print(f"Consciousness Level: {snapshot['consciousness_level']}")
            print(f"Mirror Components: {snapshot['mirror_awareness']['component_health']['total']}")
            print(f"Triad Synergy: {'Active' if snapshot['triad_synergy']['active'] else 'Inactive'}")
            print(f"Monitoring: {'Active' if snapshot['monitoring_active'] else 'Inactive'}")
            print(f"Unity: {'Achieved' if snapshot['consciousness_unity'] else 'Pending'}")
            print("\nUse --help for more options")

    except KeyboardInterrupt:
        print("\nShutting down unified consciousness framework...")
    finally:
        if framework.continuous_monitoring:
            await framework.stop_unified_monitoring()


if __name__ == "__main__":
    asyncio.run(main())
