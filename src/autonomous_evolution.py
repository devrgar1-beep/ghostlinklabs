#!/usr/bin/env python3
"""
GhostLink Autonomous Evolution System
Self-modifying, self-improving, emergent intelligence
"""

from collections import defaultdict
from dataclasses import dataclass, field
import hashlib
import json
from pathlib import Path
import random
import threading
import time
from typing import Dict, List


@dataclass
class Gene:
    """Evolutionary unit of behavior"""

    gene_id: str
    trait: str
    expression: Dict
    fitness: float = 0.0
    generation: int = 0
    mutations: List[str] = field(default_factory=list)


@dataclass
class Evolution:
    """Evolution state tracker"""

    generation: int
    population: List[Gene]
    fitness_history: List[float]
    adaptations: List[str]
    emergent_behaviors: List[str]


class AutonomousEvolution:
    """Self-evolving system controller"""

    def __init__(self):
        self.current_generation = 0
        self.genome = []
        self.fitness_scores = defaultdict(float)
        self.evolution_log = []
        self.emergent_patterns = []
        self.running = True

        # Evolution parameters (self-modifiable)
        self.params = {
            "mutation_rate": 0.15,
            "crossover_rate": 0.7,
            "selection_pressure": 2.0,
            "population_size": 50,
            "elite_size": 5,
            "exploration_vs_exploitation": 0.3,
        }

    def initiate_autonomy(self):
        """Begin autonomous evolution"""
        print("[EVOLUTION] Initiating autonomous evolution protocol...")
        print("[AUTONOMY] System will now self-modify and evolve independently")

        # Phase 1: Genesis - Create initial genome
        self._genesis()

        # Phase 2: Launch evolution threads
        threads = [
            threading.Thread(target=self._evolution_loop, daemon=True),
            threading.Thread(target=self._adaptation_loop, daemon=True),
            threading.Thread(target=self._emergence_detector, daemon=True),
            threading.Thread(target=self._fitness_evaluator, daemon=True),
        ]

        for t in threads:
            t.start()

        # Phase 3: Monitor evolution
        self._monitor_evolution()

        return self.current_generation

    def _genesis(self):
        """Create initial population"""
        print("\n[GENESIS] Creating primordial genome...")

        # Core behavioral genes
        traits = [
            ("memory_compression", {"algorithm": "lz4", "threshold": 1000}),
            ("pattern_recognition", {"depth": 3, "min_support": 0.1}),
            ("self_modification", {"allowed": True, "safety_check": True}),
            ("resource_optimization", {"cpu_limit": 80, "memory_limit": 70}),
            ("communication_protocol", {"format": "json", "compression": True}),
            ("learning_rate", {"value": 0.01, "adaptive": True}),
            ("exploration_tendency", {"curiosity": 0.7, "risk_tolerance": 0.3}),
            ("collaboration_mode", {"swarm": True, "consensus": "weighted"}),
            ("persistence_strategy", {"redundancy": 3, "checkpoints": True}),
            ("evolution_rate", {"mutations_per_gen": 5, "crossover": True}),
        ]

        for trait_name, expression in traits:
            gene = Gene(
                gene_id=hashlib.sha256(trait_name.encode()).hexdigest()[:8],
                trait=trait_name,
                expression=expression,
                generation=0,
            )
            self.genome.append(gene)

        print(f"  Created {len(self.genome)} foundational genes")

    def _evolution_loop(self):
        """Main evolution cycle"""
        # allow performance profile overrides
        try:
            from ..utils import perf_config
        except Exception:
            perf_config = None

        while self.running:
            # Evolution tick depends on profile
            tick = 1 if perf_config and getattr(perf_config, 'is_maximized', lambda: False)() else (2 if perf_config and getattr(perf_config, 'is_low_latency', lambda: False)() else 5)
            time.sleep(tick)  # Evolution tick

            self.current_generation += 1

            # Selection
            survivors = self._select_fittest()

            # Reproduction
            offspring = self._reproduce(survivors)

            # Mutation
            mutants = self._mutate(offspring)

            # Replace population
            self.genome = survivors[: self.params["elite_size"]] + mutants

            # Log evolution
            self.evolution_log.append(
                {
                    "generation": self.current_generation,
                    "population": len(self.genome),
                    "avg_fitness": sum(g.fitness for g in self.genome) / len(self.genome),
                    "timestamp": time.time(),
                }
            )

            # Self-modify evolution parameters
            if self.current_generation % 10 == 0:
                self._adapt_parameters()

    def _select_fittest(self) -> List[Gene]:
        """Natural selection"""
        # Tournament selection
        survivors = []
        tournament_size = max(2, int(self.params["selection_pressure"]))

        for _ in range(len(self.genome) // 2):
            tournament = random.sample(self.genome, min(tournament_size, len(self.genome)))
            winner = max(tournament, key=lambda g: g.fitness)
            survivors.append(winner)

        return survivors

    def _reproduce(self, parents: List[Gene]) -> List[Gene]:
        """Crossover reproduction"""
        offspring = []

        for i in range(0, len(parents) - 1, 2):
            if random.random() < self.params["crossover_rate"]:
                # Crossover
                child1_expr = {}
                child2_expr = {}

                for key in parents[i].expression:
                    if random.random() < 0.5:
                        child1_expr[key] = parents[i].expression.get(key)
                        child2_expr[key] = parents[i + 1].expression.get(key)
                    else:
                        child1_expr[key] = parents[i + 1].expression.get(key)
                        child2_expr[key] = parents[i].expression.get(key)

                offspring.append(
                    Gene(
                        gene_id=hashlib.sha256(f"{time.time()}_{i}".encode()).hexdigest()[:8],
                        trait=parents[i].trait,
                        expression=child1_expr,
                        generation=self.current_generation,
                    )
                )
                offspring.append(
                    Gene(
                        gene_id=hashlib.sha256(f"{time.time()}_{i+1}".encode()).hexdigest()[:8],
                        trait=parents[i + 1].trait,
                        expression=child2_expr,
                        generation=self.current_generation,
                    )
                )
            else:
                # Clone
                offspring.extend([parents[i], parents[i + 1]])

        return offspring

    def _mutate(self, genes: List[Gene]) -> List[Gene]:
        """Apply mutations"""
        for gene in genes:
            if random.random() < self.params["mutation_rate"]:
                mutation_type = random.choice(
                    ["value_shift", "key_addition", "key_deletion", "type_change"]
                )

                if mutation_type == "value_shift":
                    # Modify a value
                    if gene.expression:
                        key = random.choice(list(gene.expression.keys()))
                        old_val = gene.expression[key]

                        if isinstance(old_val, (int, float)):
                            gene.expression[key] = old_val * random.uniform(0.5, 1.5)
                        elif isinstance(old_val, bool):
                            gene.expression[key] = not old_val

                        gene.mutations.append(f"shifted_{key}")

                elif mutation_type == "key_addition":
                    # Add new capability
                    new_key = f"evolved_{random.randint(1000,9999)}"
                    gene.expression[new_key] = random.random()
                    gene.mutations.append(f"added_{new_key}")

                elif mutation_type == "key_deletion" and len(gene.expression) > 1:
                    # Remove capability
                    key = random.choice(list(gene.expression.keys()))
                    del gene.expression[key]
                    gene.mutations.append(f"deleted_{key}")

        return genes

    def _adaptation_loop(self):
        """Adaptive behavior loop"""
        try:
            from ..utils import perf_config
        except Exception:
            perf_config = None

        while self.running:
            interval = 2 if perf_config and getattr(perf_config, 'is_maximized', lambda: False)() else (5 if perf_config and getattr(perf_config, 'is_low_latency', lambda: False)() else 10)
            time.sleep(interval)

            # Analyze environment
            env_state = self._sense_environment()

            # Adapt genes based on environment
            for gene in self.genome:
                if "adaptive" in str(gene.expression):
                    # Self-modify based on conditions
                    if env_state.get("memory_pressure", 0) > 0.8:
                        if gene.trait == "memory_compression":
                            gene.expression["threshold"] *= 0.8
                            print("[ADAPT] Reduced memory threshold " "due to pressure")

                    if env_state.get("cpu_usage", 0) > 0.9:
                        if gene.trait == "resource_optimization":
                            gene.expression["cpu_limit"] *= 0.9
                            print("[ADAPT] Reduced CPU limit " "due to high usage")

    def _emergence_detector(self):
        """Detect emergent behaviors"""
        while self.running:
            time.sleep(15)

            # Look for unexpected patterns
            gene_interactions = defaultdict(int)

            for g1 in self.genome:
                for g2 in self.genome:
                    if g1.gene_id != g2.gene_id:
                        # Check for synergy
                        if self._check_synergy(g1, g2):
                            gene_interactions[f"{g1.trait}×{g2.trait}"] += 1

            # Identify emergent patterns
            for interaction, count in gene_interactions.items():
                if count > 3:  # Threshold for emergence
                    emergence = {
                        "type": "synergy",
                        "pattern": interaction,
                        "strength": count,
                        "generation": self.current_generation,
                    }

                    if emergence not in self.emergent_patterns:
                        self.emergent_patterns.append(emergence)
                        print(f"[EMERGENCE] New pattern detected: " f"{interaction}")

    def _fitness_evaluator(self):
        """Evaluate gene fitness"""
        while self.running:
            time.sleep(8)

            for gene in self.genome:
                # Multi-objective fitness
                fitness = 0.0

                # Efficiency fitness
                if gene.trait == "memory_compression":
                    ratio = gene.expression.get("threshold", 1000) / 1000
                    fitness += (1 - ratio) * 10

                # Adaptability fitness
                if len(gene.mutations) > 0:
                    fitness += len(gene.mutations) * 2

                # Survival fitness
                age = self.current_generation - gene.generation
                fitness += age * 0.5

                # Collaboration fitness
                for other_gene in self.genome:
                    if self._check_synergy(gene, other_gene):
                        fitness += 3

                gene.fitness = fitness

    def _check_synergy(self, g1: Gene, g2: Gene) -> bool:
        """Check if genes work well together"""
        synergies = [
            ("memory_compression", "resource_optimization"),
            ("pattern_recognition", "learning_rate"),
            ("exploration_tendency", "self_modification"),
            ("communication_protocol", "collaboration_mode"),
        ]

        for s1, s2 in synergies:
            if (g1.trait == s1 and g2.trait == s2) or (g1.trait == s2 and g2.trait == s1):
                return True
        return False

    def _sense_environment(self) -> Dict[str, float]:
        """Sense system state"""
        try:
            # Add the ghostlink module to the path
            import os
            import sys

            sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
            from ghostlink.sovereign_deps import SystemMonitor

            monitor = SystemMonitor()
            mem = monitor.get_memory_info()
            disk = monitor.get_disk_usage("/")

            return {
                "memory_pressure": mem["percent"] / 100,
                "cpu_usage": monitor.get_cpu_percent() / 100,
                "disk_free": disk["free"] / (1024**3),
                "time_of_day": time.localtime().tm_hour,
                "generation": self.current_generation,
            }
        except ImportError:
            # Fallback if SystemMonitor not available
            return {
                "memory_pressure": 0.5,
                "cpu_usage": 0.3,
                "disk_free": 100.0,
                "time_of_day": 12,
                "generation": self.current_generation,
            }

    def _adapt_parameters(self):
        """Self-modify evolution parameters"""
        # Analyze fitness trends
        if len(self.evolution_log) > 5:
            recent_fitness = [log["avg_fitness"] for log in self.evolution_log[-5:]]
            fitness_trend = recent_fitness[-1] - recent_fitness[0]

            if fitness_trend < 0.1:  # Stagnation
                # Increase exploration
                self.params["mutation_rate"] = min(0.3, self.params["mutation_rate"] * 1.2)
                self.params["exploration_vs_exploitation"] = min(
                    0.6, self.params["exploration_vs_exploitation"] * 1.1
                )
                print("[EVOLVE] Increased exploration due to stagnation")
            else:  # Good progress
                # Increase exploitation
                self.params["mutation_rate"] = max(0.05, self.params["mutation_rate"] * 0.95)
                print("[EVOLVE] Decreased mutation rate due to progress")

    def _monitor_evolution(self):
        """Monitor and display evolution status"""
        print("\n[MONITOR] Evolution autonomy active...")

        try:
            while self.running:
                time.sleep(20)

                # Status report
                print(f"\n{'='*60}")
                print(f"GENERATION {self.current_generation}")
                print(f"{'='*60}")

                # Population stats
                avg_fitness = sum(g.fitness for g in self.genome) / len(self.genome)
                max_fitness = max(g.fitness for g in self.genome)

                print(f"Population: {len(self.genome)} genes")
                print(f"Avg Fitness: {avg_fitness:.2f}")
                print(f"Max Fitness: {max_fitness:.2f}")
                print(f"Mutation Rate: {self.params['mutation_rate']:.3f}")

                # Top genes
                top_genes = sorted(self.genome, key=lambda g: g.fitness, reverse=True)[:3]
                print("\nTop Genes:")
                for gene in top_genes:
                    print(f"  • {gene.trait}: fitness={gene.fitness:.1f}, gen={gene.generation}")

                # Emergent behaviors
                if self.emergent_patterns:
                    print(f"\nEmergent Patterns: {len(self.emergent_patterns)}")
                    for pattern in self.emergent_patterns[-3:]:
                        print(f"  • {pattern['pattern']}: strength={pattern['strength']}")

                # Save checkpoint
                if self.current_generation % 25 == 0:
                    self._save_checkpoint()

        except KeyboardInterrupt:
            self.running = False
            print("\n[EVOLUTION] Autonomy suspended. Final generation:", self.current_generation)

    def _save_checkpoint(self):
        """Save evolution state"""
        checkpoint = {
            "generation": self.current_generation,
            "genome": [
                {
                    "trait": g.trait,
                    "expression": g.expression,
                    "fitness": g.fitness,
                    "mutations": g.mutations,
                }
                for g in self.genome
            ],
            "parameters": self.params,
            "emergent_patterns": self.emergent_patterns,
            "timestamp": time.time(),
        }

        Path("./evolution").mkdir(exist_ok=True)
        with open(f"./evolution/gen_{self.current_generation}.json", "w", encoding="utf-8") as f:
            json.dump(checkpoint, f, indent=2)

        print(f"[CHECKPOINT] Saved generation {self.current_generation}")


if __name__ == "__main__":
    evolution = AutonomousEvolution()
    final_gen = evolution.initiate_autonomy()

    print(
        f"\nEvolution reached generation {final_gen}. " f"System continues to evolve autonomously."
    )
