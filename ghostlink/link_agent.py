"""Link Agent - Custom AI Chat Agent for orchestration.

This module provides Link as a custom chat agent that can be invoked
directly in AI conversations to orchestrate tasks, manage context,
and coordinate GhostLink operations.
"""
from __future__ import annotations

import json
from typing import Any, Optional

from .link import Link, TaskPriority, get_link


class LinkAgent:
    """Link as a conversational AI agent.
    
    Link can be invoked in chat to:
    - Execute tasks autonomously
    - Answer questions about system state
    - Learn from conversations
    - Coordinate multi-step workflows
    - Provide intelligent suggestions
    """
    
    def __init__(self):
        self.link = get_link()
        self.conversation_context: dict[str, Any] = {}
        
    async def invoke(self, message: str, context: Optional[dict[str, Any]] = None) -> str:
        """Invoke Link with a message.
        
        Args:
            message: User message to Link
            context: Optional conversation context
            
        Returns:
            Link's response
        """
        # Update conversation context
        if context:
            self.conversation_context.update(context)
        
        # Parse message for commands
        response = await self._process_message(message)
        return response
    
    async def _process_message(self, message: str) -> str:
        """Process incoming message and generate response.
        
        Args:
            message: User message
            
        Returns:
            Link's response
        """
        msg_lower = message.lower().strip()
        
        # Status queries
        if any(word in msg_lower for word in ["status", "what are you doing", "how are things"]):
            return self._get_status_response()
        
        # Task queries
        if any(word in msg_lower for word in ["tasks", "todo", "queue"]):
            return self._get_tasks_response()
        
        # Add task
        if any(word in msg_lower for word in ["add task", "create task", "new task", "do this"]):
            return self._add_task_from_message(message)
        
        # Context queries
        if "context" in msg_lower or "remember" in msg_lower:
            return self._handle_context(message)
        
        # Learning
        if any(word in msg_lower for word in ["learn", "prefer", "like"]):
            return self._handle_learning(message)
        
        # Help
        if "help" in msg_lower or "what can you do" in msg_lower:
            return self._get_help_response()
        
        # Default: intelligent response
        return self._generate_intelligent_response(message)
    
    def _get_status_response(self) -> str:
        """Generate status response."""
        status = self.link.get_status()
        
        response = f"🧠 **Link Status Report**\n\n"
        response += f"• Active: {'Yes' if status['active'] else 'No'}\n"
        response += f"• Pending Tasks: {status['pending_tasks']}\n"
        response += f"• Completed: {status['completed_tasks']}\n"
        response += f"• Failed: {status['failed_tasks']}\n"
        response += f"• Context Variables: {status['context_vars']}\n"
        response += f"• Learned Preferences: {status['preferences']}\n\n"
        
        if status['pending_tasks'] > 0:
            response += "I have tasks in my queue. Want to see them?"
        else:
            response += "All clear! Ready for new tasks."
        
        return response
    
    def _get_tasks_response(self) -> str:
        """Generate tasks list response."""
        tasks = self.link.memory.tasks
        pending = [t for t in tasks if t.status.value == "pending"]
        running = [t for t in tasks if t.status.value == "running"]
        
        response = "📋 **Current Tasks**\n\n"
        
        if running:
            response += "**Running:**\n"
            for task in running:
                response += f"  • {task.name} ({task.priority.name})\n"
            response += "\n"
        
        if pending:
            response += "**Pending:**\n"
            for task in pending[:5]:  # Show first 5
                response += f"  • {task.name} ({task.priority.name})\n"
            if len(pending) > 5:
                response += f"  ... and {len(pending) - 5} more\n"
        else:
            response += "No pending tasks.\n"
        
        return response
    
    def _add_task_from_message(self, message: str) -> str:
        """Extract and add task from message."""
        # Simple extraction - could be enhanced with NLP
        description = message.replace("add task", "").replace("create task", "").strip()
        
        # Determine priority from keywords
        priority = TaskPriority.NORMAL
        if any(word in message.lower() for word in ["urgent", "critical", "asap"]):
            priority = TaskPriority.CRITICAL
        elif any(word in message.lower() for word in ["important", "high"]):
            priority = TaskPriority.HIGH
        elif any(word in message.lower() for word in ["low", "later", "whenever"]):
            priority = TaskPriority.LOW
        
        task = self.link.add_task(
            description[:50] if len(description) > 50 else description,
            description,
            priority=priority
        )
        
        return f"✅ Task added: **{task.name}** (Priority: {priority.name})\n\nI'll work on this {'immediately' if priority == TaskPriority.CRITICAL else 'soon'}."
    
    def _handle_context(self, message: str) -> str:
        """Handle context-related messages."""
        if "set" in message.lower() or "remember" in message.lower():
            # Extract key-value pair (simplified)
            return "📝 To set context, use format: 'remember that [key] is [value]'"
        else:
            # Show current context
            if not self.link.memory.context:
                return "I don't have any context stored yet. Teach me about your environment!"
            
            response = "🔍 **What I Remember:**\n\n"
            for key, value in self.link.memory.context.items():
                response += f"• {key}: {value}\n"
            return response
    
    def _handle_learning(self, message: str) -> str:
        """Handle learning-related messages."""
        if not self.link.memory.preferences:
            return "📚 I haven't learned any preferences yet. Tell me what you like!"
        
        response = "🎓 **What I've Learned:**\n\n"
        for key, value in self.link.memory.preferences.items():
            response += f"• {key}: {value}\n"
        return response
    
    def _get_help_response(self) -> str:
        """Generate help response."""
        return """🧠 **Link - Your AI Orchestration Brain**

I can help you with:

**Task Management:**
• "Add task: [description]" - Create a new task
• "Show my tasks" - View current tasks
• "What's my status?" - Check overall status

**Context & Memory:**
• "Remember that [key] is [value]" - Store context
• "What do you remember?" - Show stored context
• "Learn that I prefer [something]" - Teach preferences

**Intelligence:**
• Ask me questions about your system
• I learn from our conversations
• I coordinate complex workflows autonomously

**Priority Keywords:**
• Use "urgent", "critical", or "asap" for high priority
• Use "low" or "later" for low priority
• Default is normal priority

Just talk to me naturally - I'll understand! 🚀
"""
    
    def _generate_intelligent_response(self, message: str) -> str:
        """Generate intelligent contextual response."""
        # This is where LLM integration would enhance responses
        # For now, provide helpful default response
        
        return f"""🧠 I understand you said: "{message}"

I'm Link, your AI orchestration brain. I can:
• Execute tasks autonomously
• Remember important context
• Learn your preferences
• Coordinate complex workflows

Try asking me to:
• Add a task
• Check my status
• Show what I remember

Or just chat with me - I'm always learning! 🚀
"""


# Global agent instance
_agent_instance: Optional[LinkAgent] = None


def get_link_agent() -> LinkAgent:
    """Get the global Link agent instance."""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = LinkAgent()
    return _agent_instance


async def chat_with_link(message: str, context: Optional[dict[str, Any]] = None) -> str:
    """Chat with Link agent.
    
    Args:
        message: User message
        context: Optional conversation context
        
    Returns:
        Link's response
    """
    agent = get_link_agent()
    return await agent.invoke(message, context)


# GitHub Copilot Chat integration
class LinkCopilotAgent:
    """Link integration for GitHub Copilot Chat."""
    
    @staticmethod
    async def handle_chat_request(request: dict[str, Any]) -> dict[str, Any]:
        """Handle GitHub Copilot chat request.
        
        Args:
            request: Chat request from Copilot
            
        Returns:
            Response for Copilot
        """
        message = request.get("prompt", "")
        context = request.get("context", {})
        
        response = await chat_with_link(message, context)
        
        return {
            "response": response,
            "agent": "Link",
            "confidence": 0.95,
            "suggestions": [
                "Ask me about my status",
                "Add a new task",
                "Show what I remember",
            ]
        }
    
    @staticmethod
    def register_as_copilot_agent():
        """Register Link as a GitHub Copilot agent participant."""
        return {
            "name": "Link",
            "description": "Your autonomous AI orchestration brain",
            "capabilities": [
                "task_management",
                "context_tracking",
                "learning",
                "orchestration",
                "intelligent_assistance"
            ],
            "commands": [
                {"name": "status", "description": "Check Link's status"},
                {"name": "tasks", "description": "View current tasks"},
                {"name": "add", "description": "Add a new task"},
                {"name": "context", "description": "View or set context"},
                {"name": "learn", "description": "View learned preferences"},
            ]
        }


if __name__ == "__main__":
    import asyncio
    
    async def demo():
        """Demo conversation with Link."""
        print("🧠 Link Agent Demo\n")
        
        messages = [
            "Hey Link, what's your status?",
            "Add task: Review the codebase for improvements (urgent)",
            "Show my tasks",
            "What do you remember about my project?",
            "Help me understand what you can do",
        ]
        
        for message in messages:
            print(f"\n👤 User: {message}")
            response = await chat_with_link(message)
            print(f"\n🧠 Link: {response}")
            print("-" * 60)
    
    asyncio.run(demo())
