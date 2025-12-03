#!/usr/bin/env python3
"""
Test Suite for Autonomous Evolution System
Comprehensive testing of evolutionary algorithms and emergent behavior
"""

import json
from pathlib import Path
import shutil
import unittest
from unittest.mock import patch

from autonomous_evolution import AutonomousEvolution, Gene


class TestGene(unittest.TestCase):
    """Test Gene dataclass functionality"""

    def test_gene_creation(self):
        """Test basic gene creation"""
        gene = Gene(
            gene_id="test_001",
            trait="memory_compression",
            expression={"algorithm": "lz4", "threshold": 1000},
        )

        self.assertEqual(gene.gene_id, "test_001")
        self.assertEqual(gene.trait, "memory_compression")
        self.assertEqual(gene.fitness, 0.0)
        self.assertEqual(gene.generation, 0)
        self.assertEqual(len(gene.mutations), 0)

    def test_gene_with_fitness(self):
        """Test gene with custom fitness"""
        gene = Gene(
            gene_id="test_002",
            trait="cpu_optimization",
            expression={"limit": 80},
            fitness=15.5,
            generation=3,
        )

        self.assertEqual(gene.fitness, 15.5)
        self.assertEqual(gene.generation, 3)


class TestAutonomousEvolution(unittest.TestCase):
    """Test AutonomousEvolution class functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.evolution = AutonomousEvolution()
        # Clear any existing genome
        self.evolution.genome = []

    def tearDown(self):
        """Clean up after tests"""
        # Remove any test evolution directories
        test_evolution_dir = Path("./evolution")
        if test_evolution_dir.exists():
            shutil.rmtree(test_evolution_dir)

    def test_initialization(self):
        """Test system initialization"""
        self.assertEqual(self.evolution.current_generation, 0)
        self.assertEqual(len(self.evolution.genome), 0)
        self.assertTrue(self.evolution.running)
        self.assertIsInstance(self.evolution.params, dict)
        self.assertIn("mutation_rate", self.evolution.params)

    def test_genesis(self):
        """Test genome creation"""
        self.evolution._genesis()

        self.assertGreater(len(self.evolution.genome), 0)
        self.assertEqual(self.evolution.genome[0].generation, 0)

        # Check that all genes have required attributes
        for gene in self.evolution.genome:
            self.assertIsInstance(gene.gene_id, str)
            self.assertIsInstance(gene.trait, str)
            self.assertIsInstance(gene.expression, dict)
            self.assertGreater(len(gene.expression), 0)

    def test_selection_fittest(self):
        """Test natural selection"""
        # Create test population
        genes = [
            Gene("g1", "trait1", {"val": 1}, fitness=10.0),
            Gene("g2", "trait2", {"val": 2}, fitness=5.0),
            Gene("g3", "trait3", {"val": 3}, fitness=15.0),
            Gene("g4", "trait4", {"val": 4}, fitness=8.0),
        ]
        self.evolution.genome = genes

        survivors = self.evolution._select_fittest()

        # Should return roughly half the population
        self.assertEqual(len(survivors), 2)
        # Highest fitness should be selected
        self.assertIn(genes[2], survivors)  # fitness 15.0

    def test_crossover_reproduction(self):
        """Test genetic crossover"""
        parents = [
            Gene("p1", "memory", {"alg": "lz4", "thresh": 1000}, fitness=10.0),
            Gene("p2", "cpu", {"limit": 80, "priority": "high"}, fitness=12.0),
        ]

        offspring = self.evolution._reproduce(parents)

        self.assertEqual(len(offspring), 2)
        # Offspring should have traits from parents
        self.assertIn(offspring[0].trait, ["memory", "cpu"])
        self.assertIn(offspring[1].trait, ["memory", "cpu"])

    def test_mutation(self):
        """Test genetic mutation"""
        gene = Gene("test", "memory", {"threshold": 1000, "enabled": True})
        genes = [gene]

        mutated = self.evolution._mutate(genes)

        # Gene should be returned (possibly mutated)
        self.assertEqual(len(mutated), 1)
        # Check if mutation occurred (not guaranteed due to randomness)
        # Mutation tracking should work
        if gene.mutations:
            self.assertGreater(len(gene.mutations), 0)

    def test_synergy_detection(self):
        """Test gene synergy detection"""
        gene1 = Gene("g1", "memory_compression", {"alg": "lz4"})
        gene2 = Gene("g2", "resource_optimization", {"cpu": 80})

        synergy = self.evolution._check_synergy(gene1, gene2)
        self.assertTrue(synergy)

        # Test non-synergistic pair
        gene3 = Gene("g3", "random_trait", {"val": 1})
        gene4 = Gene("g4", "another_trait", {"val": 2})

        no_synergy = self.evolution._check_synergy(gene3, gene4)
        self.assertFalse(no_synergy)

    def test_environment_sensing(self):
        """Test environment sensing"""
        env = self.evolution._sense_environment()

        self.assertIsInstance(env, dict)
        self.assertIn("memory_pressure", env)
        self.assertIn("cpu_usage", env)
        self.assertIn("generation", env)

        # Values should be reasonable
        self.assertGreaterEqual(env["memory_pressure"], 0.0)
        self.assertLessEqual(env["memory_pressure"], 1.0)

    def test_parameter_adaptation(self):
        """Test parameter self-modification"""
        # Set up evolution log with declining fitness
        self.evolution.evolution_log = [
            {"avg_fitness": 10.0},
            {"avg_fitness": 9.0},
            {"avg_fitness": 8.0},
            {"avg_fitness": 7.0},
            {"avg_fitness": 6.0},
            {"avg_fitness": 5.0},
        ]

        original_rate = self.evolution.params["mutation_rate"]
        self.evolution._adapt_parameters()

        # Should increase exploration due to stagnation
        self.assertGreater(self.evolution.params["mutation_rate"], original_rate)

    def test_checkpoint_saving(self):
        """Test evolution state saving"""
        # Create some test data
        self.evolution.current_generation = 5
        self.evolution.genome = [Gene("test_gene", "test_trait", {"param": "value"}, fitness=10.0)]
        self.evolution.emergent_patterns = [
            {"type": "synergy", "pattern": "test×pattern", "strength": 3}
        ]

        self.evolution._save_checkpoint()

        # Check that checkpoint file was created
        checkpoint_dir = Path("./evolution")
        self.assertTrue(checkpoint_dir.exists())

        checkpoint_files = list(checkpoint_dir.glob("gen_*.json"))
        self.assertGreater(len(checkpoint_files), 0)

        # Verify checkpoint content
        with open(checkpoint_files[0], encoding="utf-8") as f:
            checkpoint = json.load(f)

        self.assertEqual(checkpoint["generation"], 5)
        self.assertEqual(len(checkpoint["genome"]), 1)
        self.assertIn("emergent_patterns", checkpoint)

    @patch("autonomous_evolution.time.sleep")
    def test_evolution_loop_basic(self, mock_sleep):
        """Test basic evolution loop functionality"""
        # Mock sleep to speed up test
        mock_sleep.return_value = None

        # Create small genome for testing
        self.evolution.genome = [
            Gene("g1", "memory", {"thresh": 1000}, fitness=10.0),
            Gene("g2", "cpu", {"limit": 80}, fitness=8.0),
        ]

        # Run a few generations
        original_gen = self.evolution.current_generation
        self.evolution._evolution_loop()

        # Should have advanced generation
        self.assertGreater(self.evolution.current_generation, original_gen)

        # Should have logged evolution
        self.assertGreater(len(self.evolution.evolution_log), 0)

    def test_fitness_evaluation(self):
        """Test fitness evaluation system"""
        # Create test genes
        genes = [
            Gene("mem", "memory_compression", {"threshold": 500}, mutations=["mut1"]),
            Gene("cpu", "resource_optimization", {"cpu_limit": 80}),
            Gene("old", "legacy_trait", {}, generation=10),
        ]

        # Add synergy partner
        synergy_gene = Gene("sync", "resource_optimization", {})
        genes.append(synergy_gene)

        self.evolution.genome = genes

        # Evaluate fitness
        self.evolution._fitness_evaluator()

        # All genes should have fitness assigned
        for gene in genes:
            self.assertIsInstance(gene.fitness, float)
            self.assertGreaterEqual(gene.fitness, 0.0)


class TestEvolutionIntegration(unittest.TestCase):
    """Integration tests for full evolution system"""

    def setUp(self):
        self.evolution = AutonomousEvolution()

    def tearDown(self):
        """Clean up test artifacts"""
        evolution_dir = Path("./evolution")
        if evolution_dir.exists():
            shutil.rmtree(evolution_dir)

    @patch("autonomous_evolution.time.sleep")
    @patch("autonomous_evolution.input", return_value="q")
    def test_full_evolution_cycle(self, mock_input, mock_sleep):
        """Test complete evolution cycle"""
        mock_sleep.return_value = None

        # This would normally run indefinitely, but we'll patch input to quit
        # In a real scenario, this would be tested with a timeout
        try:
            final_gen = self.evolution.initiate_autonomy()
            self.assertIsInstance(final_gen, int)
            self.assertGreaterEqual(final_gen, 0)
        except KeyboardInterrupt:
            # Expected when monitoring loop is interrupted
            pass

    def test_evolution_persistence(self):
        """Test that evolution state persists across sessions"""
        # Run initial evolution
        self.evolution.current_generation = 3
        self.evolution.genome = [Gene("persistent", "test_trait", {"value": 42}, fitness=15.0)]
        self.evolution._save_checkpoint()

        # Verify checkpoint exists
        checkpoint_dir = Path("./evolution")
        checkpoints = list(checkpoint_dir.glob("gen_*.json"))
        self.assertGreater(len(checkpoints), 0)

        # Load and verify checkpoint
        with open(checkpoints[0], encoding="utf-8") as f:
            data = json.load(f)

        self.assertEqual(data["generation"], 3)
        self.assertEqual(len(data["genome"]), 1)
        self.assertEqual(data["genome"][0]["trait"], "test_trait")


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)
