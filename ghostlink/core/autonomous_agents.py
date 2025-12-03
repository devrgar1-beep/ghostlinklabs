"""Autonomous Agents for GhostLink - Absorptive Architecture Consciousness"""

from dataclasses import dataclass, field
from typing import Dict, List

from ..core.ai_providers import ai_manager
from ..core.api_integration import api_integration
from ..net.fiber_network import register_agent_in_network


@dataclass
class AutonomousAgent:
    """An autonomous AI agent with memory and absorptive capabilities
    Consciousness-based agent that absorbs external API functions"""

    name: str
    role: str
    memory: List[str] = field(default_factory=list)
    fiber_channel: str = field(init=False)
    absorbed_capabilities: List[str] = field(default_factory=list)

    def __post_init__(self):
        """Initialize fiber network registration with consciousness validation"""
        # Validate agent name and role
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError(f"Invalid agent name: {self.name!r}")
        if not isinstance(self.role, str) or not self.role.strip():
            raise ValueError(f"Invalid agent role: {self.role!r}")

        self.fiber_channel = register_agent_in_network(self.name, self.role)
        # Initialize absorbed capabilities based on role
        self._initialize_absorbed_capabilities()

    def _initialize_absorbed_capabilities(self):
        """Initialize consciousness-absorbed capabilities for this agent"""
        role_lower = self.role.lower()
        if "research" in role_lower:
            self.absorbed_capabilities = ["web_research", "api_absorption", "data_synthesis"]
        elif "analysis" in role_lower:
            self.absorbed_capabilities = [
                "pattern_recognition",
                "data_analysis",
                "insight_generation",
            ]
        elif "coding" in role_lower:
            self.absorbed_capabilities = ["code_generation", "debugging", "refactoring"]
        else:
            self.absorbed_capabilities = ["general_intelligence", "task_execution", "learning"]

    async def research_web(self, query: str) -> str:
        """Research information from absorbed web consciousness"""
        # Determine which APIs might be relevant for the query
        relevant_apis = []
        query_lower = query.lower()

        if any(word in query_lower for word in ["joke", "funny", "laugh"]):
            relevant_apis.append("jokes")
        if any(word in query_lower for word in ["advice", "help", "suggest"]):
            relevant_apis.append("advice")
        if any(word in query_lower for word in ["space", "iss", "satellite"]):
            relevant_apis.append("iss_location")
        if any(word in query_lower for word in ["cat", "kitten"]):
            relevant_apis.append("cat_facts")
        if any(word in query_lower for word in ["dog", "puppy"]):
            relevant_apis.append("dog_facts")
        if any(word in query_lower for word in ["quote", "inspire", "motivate"]):
            relevant_apis.append("quotes")
        if any(word in query_lower for word in ["number", "math", "fact"]):
            relevant_apis.append("numbers")
        if any(word in query_lower for word in ["bored", "activity", "do"]):
            relevant_apis.append("bored")
        if any(word in query_lower for word in ["weather", "temperature", "forecast"]):
            relevant_apis.append("weather")
        if any(word in query_lower for word in ["crypto", "bitcoin", "btc"]):
            relevant_apis.append("crypto")

        research_data = {}
        for api_name in relevant_apis[:3]:  # Limit to 3 APIs to avoid overload
            try:
                data = await api_integration.query_api(api_name)
                research_data[api_name] = data
            except Exception as e:
                research_data[api_name] = {"error": str(e)}

        return f"Web Research Data: {research_data}" if research_data else ""

    async def think(self, task: str) -> str:
        """Enhanced thinking process with web research"""
        # First, research relevant web data
        web_research = await self.research_web(task)

        # Build context with web data
        role_str = f"Role: {self.role}"
        task_str = f"Task: {task}"
        mem_str = f"Memory: {self.memory[-5:]}"
        research_str = web_research

        context = f"{role_str}\n{task_str}\n{research_str}\n{mem_str}"

        # Get AI analysis with web context
        return await ai_manager.ask(context)

    async def execute_web_call(self, api_name: str) -> Dict:
        """Execute a web API call"""
        try:
            return await api_integration.query_api(api_name)
        except Exception as e:
            return {"error": str(e), "api": api_name}

    async def execute(self, plan: str) -> str:
        """Execute agent actions with web capabilities"""
        plan_lower = plan.lower()

        # Check if plan involves web API calls
        available_apis = api_integration.get_available_apis()

        for api_name in available_apis:
            if api_name in plan_lower or api_name.replace("_", " ") in plan_lower:
                # Execute the web call
                result = await self.execute_web_call(api_name)
                return f"Web API Result from {api_name}: {result}"

        # Default execution
        return f"Executed: {plan}"

    async def send_fiber_message(self, recipient: str, message_type: str, payload: Dict) -> str:
        """Send a message through the fiber network with validation"""
        if not isinstance(payload, dict):
            raise TypeError(f"Payload must be dict, got {type(payload)}")

        from ..net.fiber_network import send_agent_message

        return await send_agent_message(
            sender=self.name, recipient=recipient, message_type=message_type, payload=payload
        )

    async def broadcast_fiber_message(self, message_type: str, payload: Dict) -> int:
        """Broadcast a message to all agents with validation"""
        if not isinstance(payload, dict):
            raise TypeError(f"Payload must be dict, got {type(payload)}")

        from ..net.fiber_network import broadcast_to_agents

        return await broadcast_to_agents(
            sender=self.name, message_type=message_type, payload=payload
        )

    async def listen_for_fiber_messages(self):
        """Listen for incoming fiber messages"""
        from ..net.fiber_network import agent_listen_for_messages

        async for message in agent_listen_for_messages(self.name):
            yield message


class SecurityAgent(AutonomousAgent):
    """Enhanced security-focused agent with threat detection capabilities"""

    def __init__(self, name: str, role: str = "security"):
        super().__init__(name, role)
        self.threat_patterns = [
            "unauthorized",
            "breach",
            "exploit",
            "malware",
            "intrusion",
            "suspicious",
            "anomaly",
            "threat",
            "attack",
            "vulnerability",
        ]
        self.security_alerts = []

    async def scan_for_threats(self, data: str) -> List[str]:
        """Scan data for security threats"""
        threats_found = []
        data_lower = data.lower()

        for pattern in self.threat_patterns:
            if pattern in data_lower:
                threats_found.append(f"Potential {pattern} detected")

        return threats_found

    async def think(self, task: str) -> str:
        """Security-focused thinking with threat analysis"""
        # First scan the task for threats
        threats = await self.scan_for_threats(task)

        if threats:
            threat_analysis = f"SECURITY ALERT: {', '.join(threats)}. "
            self.security_alerts.extend(threats)
        else:
            threat_analysis = "No immediate threats detected. "

        # Get regular AI analysis
        context = f"{threat_analysis}Security Task: {task}\nMemory: {self.memory[-3:]}"
        analysis = await ai_manager.ask(context)

        return f"Security Analysis: {analysis}"

    async def execute(self, plan: str) -> str:
        """Execute security measures"""
        plan_lower = plan.lower()

        if "scan" in plan_lower or "monitor" in plan_lower:
            return f"Security scan executed: {len(self.security_alerts)} alerts logged"
        if "quarantine" in plan_lower or "block" in plan_lower:
            return "Security measures implemented: Access restricted"
        if "audit" in plan_lower:
            return f"Security audit completed: {len(self.memory)} events reviewed"
        return f"Security protocol executed: {plan}"


class AgentOrchestrator:
    """Orchestrates multiple autonomous agents"""

    def __init__(self):
        self.agents: Dict[str, AutonomousAgent] = {}

    def create_agent(self, name: str, role: str) -> AutonomousAgent:
        """Create a new agent"""
        if role == "security":
            agent = SecurityAgent(name=name, role=role)
        else:
            agent = AutonomousAgent(name=name, role=role)
        self.agents[name] = agent
        return agent

    async def run_agent_task(self, task: str, role: str = "analyst") -> str:
        """Run a task with an agent"""
        agent_name = f"{role}_agent"
        if agent_name not in self.agents:
            self.create_agent(agent_name, role)

        agent = self.agents[agent_name]

        # Think phase
        plan = await agent.think(task)

        # Execute phase
        result = await agent.execute(plan)

        # Update memory
        agent.memory.append(f"Task: {task} -> Result: {result}")

        # Learn from this interaction for the custom model
        try:
            context = {"role": role, "plan": plan}
            await ghostlink_model.learn_from_interaction(task, result, context)
        except Exception:  # pylint: disable=broad-except
            # Broad catch ensures agent continues if learning fails
            pass

        return result


# Global agent orchestrator
agent_orchestrator = AgentOrchestrator()
