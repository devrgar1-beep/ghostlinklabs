"""AutoGen-like Multi-Agent Framework for GhostLink

This module provides Microsoft AutoGen-style functionality with:
- ConversableAgent: Base class for conversational agents
- AssistantAgent: Code-writing and execution agents
- UserProxyAgent: User interaction agents
- GroupChat: Multi-agent conversation orchestration
"""

from abc import ABC, abstractmethod
import asyncio
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..core.ai_providers import ai_manager
from ..net.fiber_network import fiber_network
from ..utils.logging import setup_logging

logger = setup_logging()


@dataclass
class Message:
    """Message structure for agent communication"""

    content: str
    role: str = "user"
    name: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class ConversableAgent(ABC):
    """Base class for conversational agents"""

    def __init__(
        self,
        name: str,
        system_message: str = "",
        description: str = "",
        llm_config: Optional[Dict[str, Any]] = None,
    ):
        self.name = name
        self.system_message = system_message or f"You are {name}, a helpful AI assistant."
        self.description = description or f"Agent {name}"
        self.llm_config = llm_config or {}

        # Conversation state
        self.chat_messages: List[Message] = []

        # Register with fiber network
        fiber_network.register_agent(
            self.name,
            {"role": "autogen_agent", "type": "conversable", "description": self.description},
        )

        logger.info(f"Created ConversableAgent: {self.name}")

    async def send(self, message: Message, recipient: "ConversableAgent") -> Message:
        """Send a message to another agent"""
        self.chat_messages.append(message)

        # Send via fiber network
        payload = {
            "type": "autogen_message",
            "message": {
                "content": message.content,
                "role": message.role,
                "name": message.name,
                "metadata": message.metadata,
            },
            "sender": self.name,
        }

        await fiber_network.send_message(self.name, recipient.name, "fiber_agents", payload)

        return message

    async def receive(self, message: Message, sender: "ConversableAgent") -> Optional[Message]:
        """Receive and process a message"""
        self.chat_messages.append(message)

        # Process the message
        response = await self._process_message(message, sender)
        return response

    @abstractmethod
    async def _process_message(
        self, message: Message, sender: "ConversableAgent"
    ) -> Optional[Message]:
        """Process incoming message"""

    async def generate_reply(
        self, messages: List[Message], sender: "ConversableAgent"
    ) -> Optional[Message]:
        """Generate a reply using LLM"""
        context = self._prepare_llm_context(messages, sender)

        try:
            # WARNING: generated code execution can be dangerous. Ensure inputs are trusted
            # or executed inside a hardened, OS-level sandbox. Avoid exec() on untrusted input.
            response = await ai_manager.ask(context)
            return Message(content=response, role="assistant", name=self.name)
        except Exception as e:
            logger.error(f"Error generating reply for {self.name}: {e}")
            return Message(
                content=f"I encountered an error: {e!s}", role="assistant", name=self.name
            )

    def _prepare_llm_context(self, messages: List[Message], sender: "ConversableAgent") -> str:
        """Prepare context for LLM"""
        context_parts = []

        if self.system_message:
            context_parts.append(f"System: {self.system_message}")

        for msg in messages[-5:]:  # Last 5 messages
            if msg.name:
                context_parts.append(f"{msg.name}: {msg.content}")
            else:
                context_parts.append(f"{msg.role}: {msg.content}")

        return "\n\n".join(context_parts)


class AssistantAgent(ConversableAgent):
    """Assistant agent that can write and execute code"""

    def __init__(self, name: str, system_message: str = "", **kwargs):
        system_message = system_message or (
            "You are a helpful AI assistant. You can write code to solve problems."
        )

        super().__init__(name=name, system_message=system_message, **kwargs)

    async def _process_message(
        self, message: Message, sender: "ConversableAgent"
    ) -> Optional[Message]:
        """Process message and potentially execute code"""
        if self._contains_code(message.content):
            result = await self._execute_code(message.content)
            return Message(
                content=f"Code execution result:\n{result}", role="assistant", name=self.name
            )

        return await self.generate_reply([message], sender)

    def _contains_code(self, content: str) -> bool:
        """Check if content contains code"""
        code_indicators = ["```python", "```", "def ", "import ", "print("]
        return any(indicator in content for indicator in code_indicators)

    async def _execute_code(self, code: str) -> str:
        """Execute code (simplified)"""
        try:
            if "```python" in code:
                code = code.split("```python")[1].split("```")[0].strip()

            local_vars = {}
            exec(code, {"__builtins__": {}}, local_vars)

            result = local_vars.get("result", "Code executed successfully")
            return str(result)

        except Exception as e:
            return f"Code execution error: {e!s}"

        except Exception as e:
            return f"Code execution error: {e!s}"


class UserProxyAgent(ConversableAgent):
    """User proxy agent that represents human users"""

    def __init__(self, name: str, human_input_mode: str = "NEVER", **kwargs):
        system_message = "You are a user proxy agent."

        super().__init__(name=name, system_message=system_message, **kwargs)
        self.human_input_mode = human_input_mode

    async def _process_message(
        self, message: Message, sender: "ConversableAgent"
    ) -> Optional[Message]:
        """Process message and potentially request human input"""
        if self.human_input_mode == "ALWAYS":
            return Message(
                content=f"[HUMAN INPUT NEEDED] Please respond to: {message.content}",
                role="user",
                name=self.name,
            )

        return await self.generate_reply([message], sender)


@dataclass
class GroupChat:
    """Multi-agent group chat"""

    agents: List[ConversableAgent]
    messages: List[Message] = field(default_factory=list)
    max_round: int = 10

    async def run_chat(self, task: str) -> List[Message]:
        """Run a group chat conversation"""
        initial_message = Message(content=task, role="user", name="system")
        self.messages.append(initial_message)

        current_speaker = self.agents[0]

        for round_num in range(self.max_round):
            logger.info(f"Group chat round {round_num + 1}")

            # Select next speaker (simple round-robin)
            current_index = self.agents.index(current_speaker)
            current_speaker = self.agents[(current_index + 1) % len(self.agents)]

            # Get response
            response = await current_speaker.receive(initial_message, current_speaker)

            if response:
                self.messages.append(response)

                if self._is_task_complete(response.content):
                    break

        return self.messages

    def _is_task_complete(self, content: str) -> bool:
        """Check if task is complete"""
        completion_indicators = [
            "task completed",
            "finished",
            "done",
            "complete",
            "solution found",
            "problem solved",
        ]
        content_lower = content.lower()
        return any(indicator in content_lower for indicator in completion_indicators)


# Convenience functions
def initiate_chat(
    recipient: ConversableAgent, message: str, sender: Optional[ConversableAgent] = None
):
    """Initiate a chat between agents"""
    if sender is None:
        sender = UserProxyAgent("temp_user", human_input_mode="NEVER")

    async def _run_chat():
        msg = Message(content=message, role="user", name=sender.name)
        await sender.send(msg, recipient)
        return [msg]

    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            return [Message(content=message, role="user", name=sender.name)]
        return loop.run_until_complete(_run_chat())
    except:
        return [Message(content=message, role="user", name=sender.name)]
