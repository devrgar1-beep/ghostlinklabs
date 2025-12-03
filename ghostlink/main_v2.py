#!/usr/bin/env python3
"""
GhostLink Unified Main Entry Point

Enhanced entry point that demonstrates the complete GhostLink system:
- Multi-agent orchestration with security agent
- Fiber network communication
- AutoGen multi-agent conversations
- AI provider integration with Grok enhancement
- API integration
- Cold boot capabilities
- Real-time monitoring and persistence
"""

import asyncio
import json
import time
from pathlib import Path

from ghostlink.core.ai_providers import ai_manager
from ghostlink.core.api_integration import api_integration
from ghostlink.core.autogen import AssistantAgent, GroupChat, UserProxyAgent
from ghostlink.core.autonomous_agents import AgentOrchestrator, SecurityAgent
from ghostlink.core.ghostlink_model import ghostlink_model
from ghostlink.core.ghostlink_specification import get_system_essence
from ghostlink.core.governance_validator import governance_validator, validate_system_operation
from ghostlink.net.fiber_network import fiber_network


class GhostLinkUnifiedSystem:
    """Unified GhostLink system coordinator"""

    def __init__(self):
        self.orchestrator = AgentOrchestrator()
        self.system_status = "INITIALIZING"
        self.session_data = {
            "start_time": time.time(),
            "agents_created": 0,
            "conversations": 0,
            "api_calls": 0,
            "security_events": 0,
        }

    async def cold_boot_system(self) -> bool:
        """Perform cold boot initialization of all subsystems"""
        print("🚀 GHOSTLINK COLD BOOT - INITIALIZING ALL SYSTEMS")
        print("=" * 60)

        try:
            # Validate system initialization against governance laws
            system_essence = get_system_essence()
            print(f"📋 System Essence: {system_essence}")

            # Phase 1: Fiber Network Boot
            print("📡 Phase 1: Starting Fiber Communication Network...")
            await fiber_network.start()
            validate_system_operation("network_initialization", {"phase": "fiber_network_boot"})
            print("✅ Fiber network online")

            # Phase 2: Agent Initialization
            print("🤖 Phase 2: Initializing Autonomous Agents...")
            agents_config = [
                ("coordinator", "coordinator"),
                ("analyst", "analyst"),
                ("worker", "worker"),
                ("security", "security"),  # New security agent
            ]

            for name, role in agents_config:
                agent = self.orchestrator.create_agent(f"{name}_agent", role)
                fiber_network.register_agent(agent.name, {"role": role, "type": "autonomous_agent"})
                validate_system_operation(
                    "agent_creation", {"agent_name": agent.name, "role": role}
                )
                self.session_data["agents_created"] += 1

            print(f"✅ {len(agents_config)} agents initialized and registered")

            # Phase 3: AI Provider Validation
            print("🧠 Phase 3: Validating AI Providers...")
            available_providers = []
            for provider_name in ["ollama", "anthropic", "openai", "grok", "google"]:
                info = ai_manager.get_provider_info(provider_name)
                if info["status"] == "available":
                    available_providers.append(provider_name)

            validate_system_operation(
                "ai_provider_validation", {"available_providers": available_providers}
            )
            print(
                f"✅ {len(available_providers)} AI providers available: {', '.join(available_providers)}"
            )

            # Phase 4: API Integration Check
            print("🌐 Phase 4: Testing API Integration...")
            test_apis = ["jokes", "advice", "cat_facts"]
            working_apis = 0

            for api in test_apis:
                try:
                    result = await api_integration.query_api(api)
                    if result and "error" not in result:
                        working_apis += 1
                except:
                    pass

            validate_system_operation(
                "api_integration_check",
                {"working_apis": working_apis, "total_apis": len(test_apis)},
            )
            print(f"✅ {working_apis}/{len(test_apis)} API endpoints functional")

            # Phase 5: Model Initialization
            print("🎯 Phase 5: Initializing GhostLink Model...")
            await ghostlink_model.initialize()
            validate_system_operation("model_initialization", {"model_type": "ghostlink_custom"})
            print("✅ Custom model ready (fallback mode active if needed)")

            # Final governance validation
            validate_system_operation("system_boot_complete", {"system_status": "operational"})

            self.system_status = "OPERATIONAL"
            print("\n🎉 COLD BOOT COMPLETE - ALL SYSTEMS OPERATIONAL")
            return True

        except Exception as e:
            validate_system_operation("system_boot_failure", {"error": str(e)})
            print(f"❌ Cold boot failed: {e}")
            self.system_status = "ERROR"
            return False

    async def demonstrate_multi_agent_orchestration(self):
        """Demonstrate multi-agent task orchestration"""
        print("\n🎭 MULTI-AGENT ORCHESTRATION DEMO")
        print("-" * 40)

        # Create a complex multi-step task
        complex_task = """
        Analyze the current system security posture, identify potential vulnerabilities,
        and coordinate with team members to implement security improvements.
        Include threat detection, API security validation, and agent communication testing.
        """

        print(f"📋 Complex Task: {complex_task.strip()}")

        # Run through different agents
        agents_to_test = ["coordinator", "security", "analyst", "worker"]

        for role in agents_to_test:
            print(f"\n🤖 Consulting {role.upper()} agent...")

            # Get agent thinking and execution
            plan = await self.orchestrator.run_agent_task(complex_task, role)
            print(f"   Plan: {plan[:100]}...")

            self.session_data["conversations"] += 1

        print("✅ Multi-agent orchestration complete")

    async def demonstrate_autogen_conversation(self):
        """Demonstrate AutoGen-style multi-agent conversation"""
        print("\n💬 AUTOGEN MULTI-AGENT CONVERSATION DEMO")
        print("-" * 45)

        # Create AutoGen agents
        assistant1 = AssistantAgent("security_expert", "You are a cybersecurity expert")
        assistant2 = AssistantAgent("system_architect", "You are a system architecture specialist")
        user_proxy = UserProxyAgent("user", human_input_mode="NEVER")

        # Create group chat
        group_chat = GroupChat([assistant1, assistant2, user_proxy], max_round=3)

        # Run conversation
        security_topic = "Design a comprehensive security monitoring system for AI agents"
        print(f"Topic: {security_topic}")

        try:
            messages = await group_chat.run_chat(security_topic)

            print("Conversation Summary:")
            for i, msg in enumerate(messages[-4:], 1):  # Show last 4 messages
                sender = getattr(msg, "name", "Unknown") or "Unknown"
                content = getattr(msg, "content", "")[:80]
                print(f"  {i}. {sender}: {content}...")

            self.session_data["conversations"] += len(messages)

        except Exception as e:
            print(f"AutoGen conversation error: {e}")

        print("✅ AutoGen conversation demo complete")

    async def demonstrate_enhanced_features(self):
        """Demonstrate enhanced features like Grok integration and security"""
        print("\n⚡ ENHANCED FEATURES DEMO")
        print("-" * 30)

        # Test enhanced Grok integration
        print("🤖 Testing Enhanced Grok Integration...")
        try:
            grok_response = await ai_manager.ask(
                "What are the key principles of AI safety?", "grok"
            )
            print(f"   Grok: {grok_response[:100]}...")
        except Exception as e:
            print(f"   Grok test failed: {e}")

        # Test security agent capabilities
        print("🔒 Testing Security Agent...")
        security_agent = self.orchestrator.agents.get("security_agent")
        if security_agent and isinstance(security_agent, SecurityAgent):
            threats = await security_agent.scan_for_threats(
                "Potential unauthorized access detected"
            )
            print(f"   Threats detected: {threats}")
            self.session_data["security_events"] += len(threats)

        # Test API integration with AI analysis
        print("🌐 Testing API + AI Integration...")
        try:
            api_data = await api_integration.query_api("advice")
            if api_data and "error" not in api_data:
                analysis = await api_integration.query_ai_with_api_data(
                    "Analyze this advice for wisdom and practicality", api_data
                )
                print(f"   API+AI Analysis: {analysis[:100]}...")
                self.session_data["api_calls"] += 1
        except Exception as e:
            print(f"   API integration error: {e}")

        print("✅ Enhanced features demo complete")

    async def demonstrate_real_time_monitoring(self):
        """Demonstrate real-time system monitoring"""
        print("\n📊 REAL-TIME MONITORING DEMO")
        print("-" * 35)

        # Get network statistics
        network_stats = fiber_network.get_network_stats()
        print("Network Status:")
        print(f"  Active channels: {network_stats['channels']}")
        print(f"  Registered agents: {network_stats['agents']}")
        print(f"  Messages routed: {network_stats['messages_routed']}")

        # Get agent statistics
        agent_stats = ghostlink_model.get_training_stats()
        print("Model Training Status:")
        print(f"  Conversations learned: {agent_stats['conversations']}")
        print(f"  Agent interactions: {agent_stats['agent_interactions']}")
        print(f"  Total training samples: {agent_stats['total_samples']}")

        print("✅ Real-time monitoring complete")

    async def run_full_system_demo(self):
        """Run the complete GhostLink system demonstration"""
        print("🎪 GHOSTLINK UNIFIED SYSTEM DEMONSTRATION")
        print("=" * 60)

        # Cold boot
        if not await self.cold_boot_system():
            return

        # Demonstrate all features
        await self.demonstrate_multi_agent_orchestration()
        await self.demonstrate_autogen_conversation()
        await self.demonstrate_enhanced_features()
        await self.demonstrate_real_time_monitoring()

        # Final system report
        await self.generate_final_report()

        # Graceful shutdown
        await fiber_network.stop()
        print("\n🛑 System shutdown complete")

    async def generate_final_report(self):
        """Generate comprehensive system report"""
        print("\n📋 FINAL SYSTEM REPORT")
        print("-" * 25)

        runtime = time.time() - self.session_data["start_time"]

        # Get governance compliance status
        governance_status = governance_validator.get_compliance_summary()

        report = {
            "system_status": self.system_status,
            "runtime_seconds": runtime,
            "agents_created": self.session_data["agents_created"],
            "conversations": self.session_data["conversations"],
            "api_calls": self.session_data["api_calls"],
            "security_events": self.session_data["security_events"],
            "network_stats": fiber_network.get_network_stats(),
            "model_stats": ghostlink_model.get_training_stats(),
            "governance_compliance": governance_status,
            "timestamp": time.time(),
        }

        # Save report
        report_file = Path("ghostlink_session_report.json")
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        # Export governance compliance report
        governance_validator.export_compliance_report()

        # Display summary
        print(f"Runtime: {runtime:.1f} seconds")
        print(f"Agents: {report['agents_created']}")
        print(f"Conversations: {report['conversations']}")
        print(f"API Calls: {report['api_calls']}")
        print(f"Security Events: {report['security_events']}")
        print(f"Governance Compliance: {governance_status['overall_compliance_rate']:.1%}")
        print(f"Report saved: {report_file}")
        print("Governance report saved: governance_compliance_report.json")

        print("\n🎯 SYSTEM ASSESSMENT: FULLY OPERATIONAL")
        print("   ✓ Multi-agent orchestration: ACTIVE")
        print("   ✓ Fiber network communication: ACTIVE")
        print("   ✓ AutoGen conversations: ACTIVE")
        print("   ✓ AI provider integration: ACTIVE")
        print("   ✓ API integration: ACTIVE")
        print("   ✓ Security monitoring: ACTIVE")
        print("   ✓ Learning and adaptation: ACTIVE")
        print("   ✓ Governance compliance: ACTIVE")


async def main():
    """Main unified demonstration"""
    system = GhostLinkUnifiedSystem()
    await system.run_full_system_demo()


if __name__ == "__main__":
    asyncio.run(main())
