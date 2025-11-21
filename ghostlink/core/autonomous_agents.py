"""Autonomous Agents for GhostLink"""

from dataclasses import dataclass
from typing import Dict, List

from ..core.ai_providers import ai_manager


@dataclass
class AutonomousAgent:
    """An autonomous AI agent with memory and capabilities"""

    name: str
    role: str
    memory: List[str] = None

    def __post_init__(self):
        if self.memory is None:
            self.memory = []

    async def think(self, task: str) -> str:
        """Agent thinking process"""
        context = f"Role: {self.role}\nTask: {task}\nMemory: {self.memory[-5:]}"
        return await ai_manager.ask(context)

    async def execute(self, plan: str) -> str:
        """Execute agent actions"""
        # Simple execution - in real implementation would parse plan and execute steps
        return f"Executed: {plan}"


class AgentOrchestrator:
    """Orchestrates multiple autonomous agents"""

    def __init__(self):
        self.agents: Dict[str, AutonomousAgent] = {}

    def create_agent(self, name: str, role: str) -> AutonomousAgent:
        """Create a new agent"""
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

        return result


# Global agent orchestrator
agent_orchestrator = AgentOrchestrator()
