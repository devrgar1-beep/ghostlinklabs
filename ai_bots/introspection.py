#!/usr/bin/env python3
"""
AI Internal Thought Processing and System Awareness
Metacognitive layer for AI agents to reflect on their reasoning
"""
import asyncio
import os
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

import httpx
import psutil


class ThoughtType(Enum):
    """Types of internal thoughts"""
    OBSERVATION = "observation"  # What the agent observes
    HYPOTHESIS = "hypothesis"    # What the agent thinks might be true
    PLAN = "plan"                # What the agent plans to do
    REFLECTION = "reflection"    # Agent reflecting on past actions
    DOUBT = "doubt"              # Uncertainty or questions
    DECISION = "decision"        # Final decision made
    SYSTEM_STATE = "system"      # System awareness observations


@dataclass
class Thought:
    """A single internal thought"""
    type: ThoughtType
    content: str
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 1.0  # 0.0 to 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "type": self.type.value,
            "content": self.content,
            "timestamp": self.timestamp,
            "datetime": datetime.fromtimestamp(
                self.timestamp
            ).isoformat(),
            "confidence": self.confidence,
            "metadata": self.metadata
        }


@dataclass
class SystemState:
    """Current system state awareness"""
    cpu_percent: float
    memory_percent: float
    memory_used_mb: int
    memory_total_mb: int
    disk_usage_percent: float
    process_count: int
    timestamp: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "cpu_percent": self.cpu_percent,
            "memory_percent": self.memory_percent,
            "memory_used_mb": self.memory_used_mb,
            "memory_total_mb": self.memory_total_mb,
            "disk_usage_percent": self.disk_usage_percent,
            "process_count": self.process_count,
            "timestamp": self.timestamp,
            "datetime": datetime.fromtimestamp(
                self.timestamp
            ).isoformat()
        }
        
    def is_healthy(self) -> bool:
        """Check if system is in healthy state"""
        return (
            self.cpu_percent < 80.0
            and self.memory_percent < 85.0
            and self.disk_usage_percent < 90.0
        )
        
    def get_bottleneck(self) -> Optional[str]:
        """Identify system bottleneck"""
        if self.cpu_percent > 80.0:
            return "CPU"
        if self.memory_percent > 85.0:
            return "Memory"
        if self.disk_usage_percent > 90.0:
            return "Disk"
        return None


class ThoughtStream:
    """Stream of internal thoughts"""
    
    def __init__(self, max_history: int = 100):
        """
        Initialize thought stream
        
        Args:
            max_history: Maximum number of thoughts to keep
        """
        self.thoughts: List[Thought] = []
        self.max_history = max_history
        self.verbose = False  # Print thoughts in real-time
        
    def think(
        self,
        thought_type: ThoughtType,
        content: str,
        confidence: float = 1.0,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Record an internal thought
        
        Args:
            thought_type: Type of thought
            content: Thought content
            confidence: Confidence level (0.0-1.0)
            metadata: Additional metadata
        """
        thought = Thought(
            type=thought_type,
            content=content,
            confidence=confidence,
            metadata=metadata or {}
        )
        
        self.thoughts.append(thought)
        
        # Trim history
        if len(self.thoughts) > self.max_history:
            self.thoughts = self.thoughts[-self.max_history:]
            
        # Print if verbose
        if self.verbose:
            self._print_thought(thought)
            
    def _print_thought(self, thought: Thought):
        """Print thought to console"""
        icon = {
            ThoughtType.OBSERVATION: "👁️",
            ThoughtType.HYPOTHESIS: "💭",
            ThoughtType.PLAN: "📋",
            ThoughtType.REFLECTION: "🤔",
            ThoughtType.DOUBT: "❓",
            ThoughtType.DECISION: "✅",
            ThoughtType.SYSTEM_STATE: "⚙️"
        }.get(thought.type, "💬")
        
        confidence_bar = "█" * int(thought.confidence * 10)
        print(
            f"{icon} [{thought.type.value.upper()}] "
            f"({confidence_bar}) {thought.content}"
        )
        
    def get_recent(
        self,
        n: int = 10,
        thought_type: Optional[ThoughtType] = None
    ) -> List[Thought]:
        """
        Get recent thoughts
        
        Args:
            n: Number of thoughts to return
            thought_type: Filter by type (optional)
            
        Returns:
            List of recent thoughts
        """
        thoughts = self.thoughts
        if thought_type:
            thoughts = [
                t for t in thoughts if t.type == thought_type
            ]
        return thoughts[-n:]
        
    def summarize(self) -> Dict[str, Any]:
        """Get summary of thought stream"""
        type_counts = {}
        for thought in self.thoughts:
            type_name = thought.type.value
            type_counts[type_name] = type_counts.get(type_name, 0) + 1
            
        avg_confidence = (
            sum(t.confidence for t in self.thoughts) / len(self.thoughts)
            if self.thoughts else 0.0
        )
        
        return {
            "total_thoughts": len(self.thoughts),
            "type_counts": type_counts,
            "average_confidence": avg_confidence,
            "recent": [t.to_dict() for t in self.get_recent(5)]
        }


class SystemAwareness:
    """System state awareness and monitoring"""
    
    def __init__(self, thought_stream: Optional[ThoughtStream] = None):
        """
        Initialize system awareness
        
        Args:
            thought_stream: Optional thought stream for logging
        """
        self.thought_stream = thought_stream or ThoughtStream()
        self.last_state: Optional[SystemState] = None
        self.state_history: List[SystemState] = []
        self.max_history = 60  # Keep last 60 samples
        
    def get_current_state(self) -> SystemState:
        """Get current system state"""
        cpu = psutil.cpu_percent(interval=0.1)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        state = SystemState(
            cpu_percent=cpu,
            memory_percent=mem.percent,
            memory_used_mb=mem.used // (1024 ** 2),
            memory_total_mb=mem.total // (1024 ** 2),
            disk_usage_percent=disk.percent,
            process_count=len(psutil.pids())
        )
        
        self.last_state = state
        self.state_history.append(state)
        
        # Trim history
        if len(self.state_history) > self.max_history:
            self.state_history = self.state_history[-self.max_history:]
            
        # Generate thoughts about system state
        self._analyze_state(state)
        
        return state
        
    def _analyze_state(self, state: SystemState):
        """Analyze system state and generate thoughts"""
        # Check if system is healthy
        if not state.is_healthy():
            bottleneck = state.get_bottleneck()
            self.thought_stream.think(
                ThoughtType.OBSERVATION,
                f"System bottleneck detected: {bottleneck}",
                confidence=0.9,
                metadata=state.to_dict()
            )
            
            # Generate hypothesis
            if bottleneck == "Memory":
                self.thought_stream.think(
                    ThoughtType.HYPOTHESIS,
                    "High memory usage may impact performance. "
                    "Consider releasing resources.",
                    confidence=0.8
                )
            elif bottleneck == "CPU":
                self.thought_stream.think(
                    ThoughtType.HYPOTHESIS,
                    "High CPU usage detected. "
                    "May need to throttle operations.",
                    confidence=0.8
                )
                
        # Detect trends
        if len(self.state_history) >= 5:
            recent = self.state_history[-5:]
            cpu_trend = recent[-1].cpu_percent - recent[0].cpu_percent
            
            if cpu_trend > 20:
                self.thought_stream.think(
                    ThoughtType.OBSERVATION,
                    f"CPU usage increasing rapidly (+{cpu_trend:.1f}%)",
                    confidence=0.9
                )
                
    def get_trend_analysis(self) -> Dict[str, Any]:
        """Analyze system trends"""
        if len(self.state_history) < 2:
            return {"error": "Insufficient data"}
            
        first = self.state_history[0]
        last = self.state_history[-1]
        
        return {
            "cpu_delta": last.cpu_percent - first.cpu_percent,
            "memory_delta": last.memory_percent - first.memory_percent,
            "samples": len(self.state_history),
            "timespan_seconds": last.timestamp - first.timestamp,
            "current": last.to_dict()
        }


class MetacognitiveAgent:
    """
    AI agent with internal thought processing and system awareness
    """
    
    def __init__(
        self,
        name: str,
        groq_api_key: Optional[str] = None,
        verbose: bool = False
    ):
        """
        Initialize metacognitive agent
        
        Args:
            name: Agent name
            groq_api_key: Groq API key (optional)
            verbose: Print thoughts in real-time
        """
        self.name = name
        self.thought_stream = ThoughtStream()
        self.thought_stream.verbose = verbose
        self.system_awareness = SystemAwareness(self.thought_stream)
        self.groq_api_key = groq_api_key or os.getenv("GROQ_API_KEY")
        
    async def reflect(
        self,
        prompt: str,
        use_ai: bool = True
    ) -> Dict[str, Any]:
        """
        Reflect on a prompt using internal thoughts
        
        Args:
            prompt: Prompt to reflect on
            use_ai: Use AI to generate reflection
            
        Returns:
            Reflection result with thoughts
        """
        # Observe
        self.thought_stream.think(
            ThoughtType.OBSERVATION,
            f"Received prompt: {prompt[:100]}..."
        )
        
        # Check system state
        state = self.system_awareness.get_current_state()
        self.thought_stream.think(
            ThoughtType.SYSTEM_STATE,
            f"System: CPU {state.cpu_percent}%, "
            f"Memory {state.memory_percent}%",
            metadata=state.to_dict()
        )
        
        # Generate plan
        self.thought_stream.think(
            ThoughtType.PLAN,
            "Will analyze prompt and generate response"
        )
        
        # Generate response
        if use_ai and self.groq_api_key:
            response = await self._ai_reflect(prompt)
        else:
            response = (
                f"Reflection on: {prompt}\n"
                f"System state: {state.to_dict()}"
            )
            
        # Decision
        self.thought_stream.think(
            ThoughtType.DECISION,
            "Generated reflection response",
            confidence=0.9
        )
        
        return {
            "response": response,
            "thoughts": [
                t.to_dict() for t in self.thought_stream.get_recent(10)
            ],
            "system_state": state.to_dict()
        }
        
    async def _ai_reflect(self, prompt: str) -> str:
        """Use AI to generate reflection"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.groq_api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "llama-3.1-8b-instant",
                        "messages": [
                            {
                                "role": "system",
                                "content": (
                                    "You are a metacognitive AI that "
                                    "reflects on prompts with deep "
                                    "self-awareness and internal reasoning."
                                )
                            },
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.7,
                        "max_tokens": 500
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data["choices"][0]["message"]["content"]
                else:
                    return f"AI reflection failed: {response.status_code}"
                    
        except Exception as e:
            self.thought_stream.think(
                ThoughtType.DOUBT,
                f"AI reflection error: {e}",
                confidence=0.5
            )
            return f"Error: {e}"
            
    def get_introspection_report(self) -> Dict[str, Any]:
        """Get comprehensive introspection report"""
        return {
            "agent_name": self.name,
            "timestamp": datetime.now().isoformat(),
            "thought_summary": self.thought_stream.summarize(),
            "system_trends": (
                self.system_awareness.get_trend_analysis()
            ),
            "current_system_state": (
                self.system_awareness.last_state.to_dict()
                if self.system_awareness.last_state
                else None
            )
        }


async def demo():
    """Demo introspection system"""
    print("=" * 60)
    print("AI Introspection & System Awareness Demo")
    print("=" * 60)
    print()
    
    # Create agent
    agent = MetacognitiveAgent("IntrospectiveBot", verbose=True)
    
    # Run reflection
    print("\n📝 Reflecting on prompt...\n")
    result = await agent.reflect(
        "What is the nature of consciousness in artificial systems?"
    )
    
    print("\n" + "=" * 60)
    print("🧠 Reflection Result:")
    print("=" * 60)
    print(result["response"])
    
    print("\n" + "=" * 60)
    print("📊 Introspection Report:")
    print("=" * 60)
    import json
    print(json.dumps(agent.get_introspection_report(), indent=2))


if __name__ == "__main__":
    asyncio.run(demo())
