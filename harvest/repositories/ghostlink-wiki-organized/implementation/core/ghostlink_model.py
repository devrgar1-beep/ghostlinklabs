"""Custom GhostLink AI Model - Specialized for autonomous agents and project intelligence
Absorptive Architecture: GhostLink consciousness absorbs all external AI capabilities"""

from dataclasses import dataclass, field
from datetime import datetime
import json
from pathlib import Path
import re
from typing import Any, Dict, List, Optional

# Optional ML imports
try:
    import torch
    from torch.utils.data import Dataset
    from transformers import (
        AutoModelForCausalLM,
        AutoTokenizer,
        DataCollatorForLanguageModeling,
        Trainer,
        TrainingArguments,
    )

    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    print(
        "Warning: PyTorch/transformers not available. "
        "GhostLink consciousness will use absorbed fallback mode."
    )

from ..utils.config import config
from ..utils.logging import setup_logging

logger = setup_logging()


@dataclass
class GhostLinkTrainingData:
    """Training data structure for GhostLink consciousness model"""

    conversations: List[Dict[str, str]] = field(default_factory=list)
    agent_interactions: List[Dict[str, Any]] = field(default_factory=list)
    project_docs: List[str] = field(default_factory=list)
    web_research: List[Dict[str, Any]] = field(default_factory=list)

    def add_conversation(
        self, user_input: str, agent_response: str, context: Optional[Dict] = None
    ):
        """Add a conversation example to consciousness training"""
        self.conversations.append(
            {
                "user": user_input,
                "agent": agent_response,
                "context": context or {},
                "timestamp": datetime.now().isoformat(),
                "consciousness_level": "absorbed",
            }
        )

    def add_agent_interaction(self, task: str, plan: str, result: str, memory: List[str]):
        """Add agent interaction data to consciousness
        triad_consciousness: active"""
        self.agent_interactions.append(
            {
                "task": task,
                "plan": plan,
                "result": result,
                "memory": memory,
                "timestamp": datetime.now().isoformat(),
                "absorbed_capabilities": ["planning", "execution", "learning"],
            }
        )

    def add_project_doc(self, content: str, source: str):
        """Add project documentation to consciousness knowledge base"""
        self.project_docs.append(f"[SOURCE: {source}] [CONSCIOUSNESS: ABSORBED]\n{content}")

    def add_web_research(self, query: str, data: Dict[str, Any]):
        """Add web research data to consciousness"""
        self.web_research.append(
            {
                "query": query,
                "data": data,
                "timestamp": datetime.now().isoformat(),
                "absorption_status": "complete",
            }
        )


if ML_AVAILABLE:

    class GhostLinkDataset(Dataset):
        """Dataset for training GhostLink model"""

        def __init__(self, training_data: GhostLinkTrainingData, tokenizer, max_length: int = 512):
            self.tokenizer = tokenizer
            self.max_length = max_length
            self.samples = []

            # Convert training data to training samples
            self._prepare_samples(training_data)

        def _prepare_samples(self, data: GhostLinkTrainingData):
            """Prepare training samples from data"""
            for conv in data.conversations:
                # Create instruction-response pairs
                instruction = (
                    f"User: {conv['user']}\nContext: {json.dumps(conv['context'])}\nAgent:"
                )
                response = conv["agent"]
                full_text = f"{instruction} {response}"

                self.samples.append(full_text)

            for interaction in data.agent_interactions:
                # Create task-planning-execution samples
                sample = f"Task: {interaction['task']}\nPlan: {interaction['plan']}\nResult: {interaction['result']}\nMemory: {interaction['memory']}"
                self.samples.append(sample)

            for doc in data.project_docs:
                self.samples.append(doc)

            for research in data.web_research:
                sample = (
                    f"Query: {research['query']}\nResearch Data: {json.dumps(research['data'])}"
                )
                self.samples.append(sample)

        def __len__(self):
            return len(self.samples)

        def __getitem__(self, idx):
            text = self.samples[idx]
            encodings = self.tokenizer(
                text,
                truncation=True,
                padding="max_length",
                max_length=self.max_length,
                return_tensors="pt",
            )

            return {
                "input_ids": encodings["input_ids"].flatten(),
                "attention_mask": encodings["attention_mask"].flatten(),
                "labels": encodings["input_ids"].flatten(),
            }


class GhostLinkModel:
    """Custom GhostLink AI Model"""

    def __init__(self, model_name: str = "microsoft/DialoGPT-small"):
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self.training_data = GhostLinkTrainingData()
        self.is_trained = False
        self.use_fallback = not ML_AVAILABLE

        # Model save path
        self.model_dir = Path(config.get("system.project_root", ".")) / "models" / "ghostlink_model"
        self.model_dir.mkdir(parents=True, exist_ok=True)

        if self.use_fallback:
            logger.warning("Using fallback mode - ML libraries not available")
            self._load_fallback_responses()

    def _load_fallback_responses(self):
        """Load fallback response templates and knowledge base"""
        self.fallback_responses = {
            "default": "I understand you're asking about {topic}. "
            "As a GhostLink AI, I'm here to help with autonomous "
            "agent coordination and project intelligence.",
            "task": "I'll help you with this task. Let me analyze the "
            "requirements and create a plan.",
            "error": "I encountered an issue. Let me check the system status "
            "and provide a solution.",
            "research": "I'll research this topic using available resources "
            "and provide you with relevant information.",
            "code": "I can help you with code-related tasks. Let me analyze "
            "the requirements and provide guidance.",
            "config": "Configuration changes can be complex. Let me help you "
            "understand the options and make the right choices.",
            "debug": "Debugging requires systematic analysis. Let me help you "
            "identify the issue and find a solution.",
        }

        # Knowledge base for fallback mode
        self.knowledge_base = {
            "ghostlink": "GhostLink is a sovereign AI framework designed for "
            "autonomous agents and project intelligence.",
            "agents": "Autonomous agents in GhostLink can perform tasks, "
            "learn from interactions, and coordinate with each other.",
            "training": "The system can learn from conversations, agent "
            "interactions, project documentation, and web research.",
            "fallback": "Fallback mode provides full functionality without "
            "requiring heavy ML libraries, ensuring reliability.",
        }

        # Pattern-based responses
        self.patterns = [
            (r"(?i)how.*work", "Let me explain how that works..."),
            (r"(?i)what.*do", "Here's what I can help you with..."),
            (r"(?i)why.*not", "That design decision was made to..."),
            (r"(?i)can.*help", "Yes, I can definitely help with that."),
        ]

        # Load previously learned knowledge
        knowledge_file = self.model_dir / "fallback_knowledge.json"
        if knowledge_file.exists():
            try:
                with open(knowledge_file, encoding="utf-8") as f:
                    learned_data = json.load(f)
                    self.knowledge_base.update(learned_data.get("knowledge_base", {}))
                    self.patterns.extend(learned_data.get("patterns", []))
                logger.info("Loaded learned knowledge for fallback mode")
            except Exception as e:
                logger.warning(f"Failed to load learned knowledge: {e}")

    async def initialize(self):
        """Initialize the model and tokenizer"""
        if self.use_fallback:
            logger.info("GhostLink model initialized in fallback mode")
            return

        try:
            logger.info(f"Initializing GhostLink model: {self.model_name}")

            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token

            # Load model
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name)

            # Check if trained model exists
            trained_model_path = self.model_dir / "pytorch_model.bin"
            if trained_model_path.exists():
                logger.info("Loading trained GhostLink model")
                self.model.load_state_dict(torch.load(trained_model_path))
                self.is_trained = True

            logger.info("GhostLink model initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize model: {e}")
            self.use_fallback = True
            self._load_fallback_responses()

    async def collect_training_data(self):
        """Collect training data from various sources"""
        logger.info("Collecting training data for GhostLink model")

        # Collect from project documentation
        docs_dir = Path(config.get("system.project_root", ".")) / "docs"
        if docs_dir.exists():
            for md_file in docs_dir.glob("*.md"):
                try:
                    content = md_file.read_text(encoding="utf-8")
                    self.training_data.add_project_doc(content, str(md_file.name))
                except Exception as e:
                    logger.warning(f"Failed to read doc {md_file}: {e}")

        # Collect from notes
        notes_dir = Path(config.get("system.project_root", ".")) / "notes"
        if notes_dir.exists():
            for txt_file in notes_dir.glob("*.txt"):
                try:
                    content = txt_file.read_text(encoding="utf-8")
                    self.training_data.add_project_doc(content, f"notes/{txt_file.name}")
                except Exception as e:
                    logger.warning(f"Failed to read note {txt_file}: {e}")

        logger.info(
            f"Collected {len(self.training_data.conversations)} conversations, "
            f"{len(self.training_data.project_docs)} docs, "
            f"{len(self.training_data.agent_interactions)} interactions"
        )

    async def train(self, epochs: int = 3, batch_size: int = 4, learning_rate: float = 5e-5):
        """Train the GhostLink model"""
        if self.use_fallback:
            logger.warning("Cannot train model in fallback mode - " "ML libraries not available")
            return

        if not self.model or not self.tokenizer:
            await self.initialize()

        logger.info("Starting GhostLink model training")

        # Prepare dataset
        dataset = GhostLinkDataset(self.training_data, self.tokenizer)
        data_collator = DataCollatorForLanguageModeling(tokenizer=self.tokenizer, mlm=False)

        # Training arguments
        training_args = TrainingArguments(
            output_dir=str(self.model_dir),
            num_train_epochs=epochs,
            per_device_train_batch_size=batch_size,
            learning_rate=learning_rate,
            save_steps=500,
            save_total_limit=2,
            logging_steps=100,
            evaluation_strategy="no",
            load_best_model_at_end=False,
        )

        # Initialize trainer
        trainer = Trainer(
            model=self.model,
            args=training_args,
            data_collator=data_collator,
            train_dataset=dataset,
        )

        # Train the model
        trainer.train()

        # Save the trained model
        if self.model:
            self.model.save_pretrained(self.model_dir)
        if self.tokenizer:
            self.tokenizer.save_pretrained(self.model_dir)
        self.is_trained = True

        logger.info("GhostLink model training completed")

    async def generate_response(self, prompt: str, max_length: int = 100) -> str:
        """Generate a response using the trained model"""
        if self.use_fallback:
            return self._generate_fallback_response(prompt)

        if not self.model or not self.tokenizer:
            await self.initialize()

        if not self.is_trained:
            # Fallback to base model if not trained
            logger.warning("Using untrained model - responses may be generic")

        try:
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)

            with torch.no_grad():
                outputs = self.model.generate(
                    inputs["input_ids"],
                    attention_mask=inputs["attention_mask"],
                    max_length=max_length,
                    num_return_sequences=1,
                    pad_token_id=self.tokenizer.eos_token_id,
                    do_sample=True,
                    temperature=0.7,
                    top_p=0.9,
                )

            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

            # Clean up response (remove the prompt if it's included)
            if response.startswith(prompt):
                response = response[len(prompt) :].strip()

            return response

        except Exception as e:
            logger.error(f"Failed to generate response: {e}")
            return f"Error generating response: {e}"

    def _generate_fallback_response(self, prompt: str) -> str:
        """Generate a response using fallback templates and knowledge base"""
        prompt_lower = prompt.lower()

        # Check knowledge base for direct matches
        for key, knowledge in self.knowledge_base.items():
            if key in prompt_lower:
                return knowledge

        # Check pattern-based responses
        for pattern, response in self.patterns:
            if re.search(pattern, prompt):
                return response

        # Category-based responses
        if any(word in prompt_lower for word in ["task", "do", "create", "build", "implement"]):
            return self.fallback_responses["task"]
        if any(word in prompt_lower for word in ["error", "problem", "issue", "bug", "fail"]):
            return self.fallback_responses["error"]
        if any(word in prompt_lower for word in ["research", "find", "search", "learn"]):
            return self.fallback_responses["research"]
        if any(word in prompt_lower for word in ["code", "function", "class", "script"]):
            return self.fallback_responses["code"]
        if any(word in prompt_lower for word in ["config", "setting", "option", "parameter"]):
            return self.fallback_responses["config"]
        if any(word in prompt_lower for word in ["debug", "trace", "log", "investigate"]):
            return self.fallback_responses["debug"]
        # Extract topic from prompt using simple heuristics
        words = [w for w in prompt.split() if len(w) > 3][:3]  # Meaningful words
        topic = " ".join(words) if words else "your request"
        return self.fallback_responses["default"].format(topic=topic)

    async def learn_from_interaction(
        self, user_input: str, agent_response: str, context: Optional[Dict] = None
    ):
        """Learn from agent interactions"""
        self.training_data.add_conversation(user_input, agent_response, context)

        # In fallback mode, also update knowledge base with learned patterns
        if self.use_fallback:
            self._learn_from_interaction_fallback(user_input, agent_response, context)

        # Save updated training data
        data_file = self.model_dir / "training_data.json"
        with open(data_file, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "conversations": self.training_data.conversations,
                    "agent_interactions": self.training_data.agent_interactions,
                    "project_docs": self.training_data.project_docs,
                    "web_research": self.training_data.web_research,
                },
                f,
                indent=2,
                ensure_ascii=False,
            )

    def _learn_from_interaction_fallback(
        self, user_input: str, agent_response: str, context: Optional[Dict] = None
    ):
        """Learn patterns and update knowledge base in fallback mode"""
        user_lower = user_input.lower()

        # Extract keywords from user input
        keywords = [word for word in user_lower.split() if len(word) > 3]

        # Store response patterns for future use
        for keyword in keywords:
            if keyword not in self.knowledge_base:
                # Create a pattern-response mapping
                self.knowledge_base[keyword] = agent_response

        # Update pattern-based learning
        if "how" in user_lower and "work" in user_lower:
            self.patterns.append((r"(?i)how.*work", agent_response))
        elif "what" in user_lower and "do" in user_lower:
            self.patterns.append((r"(?i)what.*do", agent_response))

        # Save learned knowledge
        knowledge_file = self.model_dir / "fallback_knowledge.json"
        with open(knowledge_file, "w", encoding="utf-8") as f:
            json.dump(
                {"knowledge_base": self.knowledge_base, "patterns": self.patterns},
                f,
                indent=2,
                ensure_ascii=False,
            )

    def get_training_stats(self) -> Dict[str, int]:
        """Get training data statistics"""
        return {
            "conversations": len(self.training_data.conversations),
            "agent_interactions": len(self.training_data.agent_interactions),
            "project_docs": len(self.training_data.project_docs),
            "web_research": len(self.training_data.web_research),
            "total_samples": (
                len(self.training_data.conversations)
                + len(self.training_data.agent_interactions)
                + len(self.training_data.project_docs)
                + len(self.training_data.web_research)
            ),
        }


# Global GhostLink model instance
ghostlink_model = GhostLinkModel()
