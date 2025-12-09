import asyncio
import random
import math
import numpy as np
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
import json
import os

@dataclass
class Genome:
    """Represents a genetic sequence for behavior evolution"""
    id: str
    genes: Dict[str, Any]
    fitness: float = 0.0
    generation: int = 0
    parent_ids: List[str] = None
    mutation_history: List[str] = None

    def __post_init__(self):
        if self.parent_ids is None:
            self.parent_ids = []
        if self.mutation_history is None:
            self.mutation_history = []

@dataclass
class BehaviorPhenotype:
    """Physical manifestation of evolved behavior"""
    genome_id: str
    motor_commands: List[Dict]
    sensor_requirements: Dict
    environmental_adaptations: Dict
    fitness_metrics: Dict

@dataclass
class VirtualWorld:
    """Simulated environment for testing evolved behaviors"""
    id: str
    dimensions: Tuple[int, int]
    obstacles: List[Dict]
    goals: List[Dict]
    environmental_conditions: Dict
    physics_parameters: Dict
    magnetic_fields: List[Dict] = None  # Magnetic field sources
    electromagnetic_properties: Dict = None  # EM simulation parameters

    def __post_init__(self):
        if self.magnetic_fields is None:
            self.magnetic_fields = []
        if self.electromagnetic_properties is None:
            self.electromagnetic_properties = {
                'conductivity': 0.01,  # Water conductivity
                'permittivity': 80.0,  # Relative permittivity of water
                'permeability': 1.0,   # Relative permeability
                'field_decay_rate': 0.1
            }

class MutationEngine:
    """Genetic operators for controlled code/behavior mutation"""

    def __init__(self):
        self.mutation_types = {
            'point_mutation': self._point_mutation,
            'duplication': self._duplication,
            'deletion': self._deletion,
            'parameter_tuning': self._parameter_tuning,
            'behavior_fusion': self._behavior_fusion
        }
        self.mutation_rates = {
            'point_mutation': 0.3,
            'duplication': 0.15,
            'deletion': 0.1,
            'parameter_tuning': 0.3,
            'behavior_fusion': 0.15
        }

    def _point_mutation(self, genome: Genome) -> Genome:
        """Random point mutation in behavior parameters"""
        mutated_genes = genome.genes.copy()
        gene_keys = list(mutated_genes.keys())

        if gene_keys:
            # Mutate a random gene
            target_gene = random.choice(gene_keys)
            if isinstance(mutated_genes[target_gene], (int, float)):
                # Numeric mutation
                current_value = mutated_genes[target_gene]
                mutation_strength = random.gauss(0, 0.1)  # Gaussian noise
                mutated_genes[target_gene] = max(0.01, current_value * (1 + mutation_strength))
            elif isinstance(mutated_genes[target_gene], list):
                # List mutation - add/remove/modify elements
                gene_list = mutated_genes[target_gene].copy()
                if gene_list and random.random() < 0.5:
                    # Modify existing element
                    idx = random.randint(0, len(gene_list) - 1)
                    if isinstance(gene_list[idx], (int, float)):
                        gene_list[idx] *= random.uniform(0.8, 1.2)
                elif random.random() < 0.3:
                    # Add new element
                    gene_list.append(random.uniform(0.1, 1.0))
                mutated_genes[target_gene] = gene_list

        new_genome = Genome(
            id=f"{genome.id}_pm_{random.randint(1000, 9999)}",
            genes=mutated_genes,
            generation=genome.generation + 1,
            parent_ids=[genome.id],
            mutation_history=genome.mutation_history + ["point_mutation"]
        )
        return new_genome

    def _crossover(self, parent1: Genome, parent2: Genome) -> Genome:
        """Crossover between two parent genomes"""
        child_genes = {}

        # Crossover each gene
        all_keys = set(parent1.genes.keys()) | set(parent2.genes.keys())
        for key in all_keys:
            if key in parent1.genes and key in parent2.genes:
                # Both parents have this gene - crossover
                if random.random() < 0.5:
                    child_genes[key] = parent1.genes[key]
                else:
                    child_genes[key] = parent2.genes[key]
            elif key in parent1.genes:
                child_genes[key] = parent1.genes[key]
            else:
                child_genes[key] = parent2.genes[key]

        new_genome = Genome(
            id=f"crossover_{random.randint(1000, 9999)}",
            genes=child_genes,
            generation=max(parent1.generation, parent2.generation) + 1,
            parent_ids=[parent1.id, parent2.id],
            mutation_history=["crossover"]
        )
        return new_genome

    def _duplication(self, genome: Genome) -> Genome:
        """Duplicate and modify a gene segment"""
        mutated_genes = genome.genes.copy()
        gene_keys = list(mutated_genes.keys())

        if gene_keys:
            # Duplicate a random gene with modification
            source_gene = random.choice(gene_keys)
            new_gene_key = f"{source_gene}_dup_{random.randint(1, 99)}"

            if isinstance(mutated_genes[source_gene], list):
                # Duplicate list with variation
                duplicated = []
                for item in mutated_genes[source_gene]:
                    if isinstance(item, (int, float)):
                        duplicated.append(item * random.uniform(0.9, 1.1))
                    else:
                        duplicated.append(item)  # Keep non-numeric items as-is
                mutated_genes[new_gene_key] = duplicated
            else:
                # Duplicate scalar with variation
                if isinstance(mutated_genes[source_gene], (int, float)):
                    mutated_genes[new_gene_key] = mutated_genes[source_gene] * random.uniform(0.8, 1.2)
                else:
                    mutated_genes[new_gene_key] = mutated_genes[source_gene]  # Keep as-is

        new_genome = Genome(
            id=f"{genome.id}_dup_{random.randint(1000, 9999)}",
            genes=mutated_genes,
            generation=genome.generation + 1,
            parent_ids=[genome.id],
            mutation_history=genome.mutation_history + ["duplication"]
        )
        return new_genome

    def _deletion(self, genome: Genome) -> Genome:
        """Delete a gene (with safety checks)"""
        mutated_genes = genome.genes.copy()
        gene_keys = list(mutated_genes.keys())

        # Don't delete if we have too few genes
        if len(gene_keys) > 3:
            gene_to_delete = random.choice(gene_keys)
            del mutated_genes[gene_to_delete]

        new_genome = Genome(
            id=f"{genome.id}_del_{random.randint(1000, 9999)}",
            genes=mutated_genes,
            generation=genome.generation + 1,
            parent_ids=[genome.id],
            mutation_history=genome.mutation_history + ["deletion"]
        )
        return new_genome

    def _parameter_tuning(self, genome: Genome) -> Genome:
        """Fine-tune behavior parameters"""
        mutated_genes = genome.genes.copy()

        # Fine-tune all numeric parameters
        for key, value in mutated_genes.items():
            if isinstance(value, (int, float)):
                # Small, controlled adjustment
                adjustment = random.gauss(0, 0.05)  # Smaller variance than point mutation
                mutated_genes[key] = max(0.01, value * (1 + adjustment))
            elif isinstance(value, list):
                # Fine-tune list elements
                for i in range(len(value)):
                    if isinstance(value[i], (int, float)):
                        adjustment = random.gauss(0, 0.03)
                        value[i] = max(0.01, value[i] * (1 + adjustment))
                mutated_genes[key] = value
            # Skip non-numeric values

        new_genome = Genome(
            id=f"{genome.id}_tune_{random.randint(1000, 9999)}",
            genes=mutated_genes,
            generation=genome.generation + 1,
            parent_ids=[genome.id],
            mutation_history=genome.mutation_history + ["parameter_tuning"]
        )
        return new_genome

    def _behavior_fusion(self, genome: Genome) -> Genome:
        """Fuse multiple behavior patterns"""
        mutated_genes = genome.genes.copy()

        # Add fusion parameters
        mutated_genes['fusion_weight'] = random.uniform(0.1, 0.9)
        mutated_genes['behavior_blend_mode'] = random.choice(['additive', 'multiplicative', 'selective'])

        # Add secondary behavior parameters
        mutated_genes['secondary_speed'] = random.uniform(0.1, 0.8)
        mutated_genes['secondary_radius'] = random.uniform(0.2, 1.0)
        mutated_genes['blend_threshold'] = random.uniform(0.3, 0.7)

        new_genome = Genome(
            id=f"{genome.id}_fusion_{random.randint(1000, 9999)}",
            genes=mutated_genes,
            generation=genome.generation + 1,
            parent_ids=[genome.id],
            mutation_history=genome.mutation_history + ["behavior_fusion"]
        )
        return new_genome

    async def mutate(self, genome: Genome, mutation_type: str = None) -> Genome:
        """Apply a mutation to a genome"""
        if mutation_type is None:
            # Random mutation based on rates
            mutation_type = random.choices(
                list(self.mutation_types.keys()),
                weights=list(self.mutation_rates.values())
            )[0]

        if mutation_type in self.mutation_types:
            return self.mutation_types[mutation_type](genome)
        else:
            return genome  # No mutation if type not found

class WorldSimulator:
    """Physics-based world simulation for behavior testing"""

    def __init__(self):
        self.worlds = {}
        self.physics_engine = {
            'gravity': 9.81,
            'friction_coefficient': 0.3,
            'air_resistance': 0.01,
            'max_velocity': 2.0,
            'collision_elasticity': 0.8
        }

    def create_world(self, world_id: str, width: int = 20, height: int = 20) -> VirtualWorld:
        """Create a new virtual world"""
        obstacles = self._generate_obstacles(width, height)
        goals = self._generate_goals(width, height)
        magnetic_fields = self._generate_magnetic_fields(width, height)

        world = VirtualWorld(
            id=world_id,
            dimensions=(width, height),
            obstacles=obstacles,
            goals=goals,
            environmental_conditions={
                'temperature': random.uniform(15, 30),
                'humidity': random.uniform(30, 80),
                'light_level': random.uniform(0.3, 1.0),
                'water_current': random.uniform(0, 0.5)
            },
            physics_parameters=self.physics_engine.copy(),
            magnetic_fields=magnetic_fields
        )

        self.worlds[world_id] = world
        return world

    def _generate_obstacles(self, width: int, height: int) -> List[Dict]:
        """Generate random obstacles for the world"""
        obstacles = []
        num_obstacles = random.randint(3, 8)

        for _ in range(num_obstacles):
            obstacle = {
                'type': random.choice(['rock', 'coral', 'wreckage', 'plant']),
                'position': (random.uniform(1, width-1), random.uniform(1, height-1)),
                'size': random.uniform(0.5, 2.0),
                'blocking': random.random() < 0.7  # 70% of obstacles block movement
            }
            obstacles.append(obstacle)

        return obstacles

    def _generate_goals(self, width: int, height: int) -> List[Dict]:
        """Generate goal points for the world"""
        goals = []
        num_goals = random.randint(1, 3)

        for _ in range(num_goals):
            goal = {
                'type': random.choice(['food', 'shelter', 'data', 'mate']),
                'position': (random.uniform(2, width-2), random.uniform(2, height-2)),
                'value': random.uniform(10, 100),
                'difficulty': random.uniform(0.1, 1.0)
            }
            goals.append(goal)

        return goals

    def _generate_magnetic_fields(self, width: int, height: int) -> List[Dict]:
        """Generate magnetic field sources for the world"""
        fields = []
        num_fields = random.randint(1, 4)

        for _ in range(num_fields):
            field = {
                'type': random.choice(['coil', 'magnet', 'current_loop', 'solenoid']),
                'position': (random.uniform(2, width-2), random.uniform(2, height-2)),
                'strength': random.uniform(0.1, 1.0),
                'orientation': random.uniform(0, 2*math.pi),
                'range': random.uniform(2, 5),
                'frequency': random.uniform(10, 50) if random.random() < 0.5 else 0.0,  # Some fields oscillate
                'attractive': random.random() < 0.6  # 60% are attractive
            }
            fields.append(field)

        return fields

    async def simulate_behavior(self, world: VirtualWorld, phenotype: BehaviorPhenotype,
                              max_steps: int = 100) -> Dict:
        """Simulate a behavior in the virtual world"""
        # Initialize agent state
        agent_state = {
            'position': (world.dimensions[0]/2, world.dimensions[1]/2),  # Start in center
            'velocity': (0.0, 0.0),
            'orientation': 0.0,  # radians
            'energy': 100.0,
            'health': 100.0,
            'goals_achieved': [],
            'collisions': 0,
            'distance_traveled': 0.0
        }

        simulation_log = []
        start_position = agent_state['position']

        for step in range(max_steps):
            # Execute behavior commands
            if step < len(phenotype.motor_commands):
                command = phenotype.motor_commands[step]
                agent_state = await self._execute_command(agent_state, command, world)

            # Apply physics
            agent_state = self._apply_physics(agent_state, world)

            # Check collisions
            collision_detected = self._check_collisions(agent_state, world)
            if collision_detected:
                agent_state['collisions'] += 1
                agent_state['health'] -= 5  # Damage from collision
                agent_state['velocity'] = (0, 0)  # Stop on collision

            # Check goal achievement
            goals_achieved = self._check_goals(agent_state, world)
            agent_state['goals_achieved'].extend(goals_achieved)

            # Update energy and health
            agent_state['energy'] -= 0.5  # Energy cost per step
            if agent_state['energy'] <= 0:
                break  # Out of energy

            # Log state
            simulation_log.append(agent_state.copy())

            # Early termination conditions
            if agent_state['health'] <= 0:
                break

        # Calculate fitness metrics
        fitness_metrics = self._calculate_fitness(agent_state, world, simulation_log, start_position)

        return {
            'final_state': agent_state,
            'simulation_log': simulation_log,
            'fitness_metrics': fitness_metrics,
            'steps_completed': len(simulation_log)
        }

    async def _execute_command(self, agent_state: Dict, command: Dict, world: VirtualWorld) -> Dict:
        """Execute a motor command in simulation"""
        new_state = agent_state.copy()

        if command.get('type') == 'differential_drive':
            linear = command.get('linear', 0.0)
            angular = command.get('angular', 0.0)

            # Update velocity based on commands
            speed = linear
            turn_rate = angular

            # Convert to velocity components
            new_state['velocity'] = (
                speed * math.cos(new_state['orientation']),
                speed * math.sin(new_state['orientation'])
            )

            # Update orientation
            new_state['orientation'] += turn_rate * 0.1  # Scale angular velocity

        elif command.get('type') == 'direct_motors':
            left_speed = command.get('left', 0.0)
            right_speed = command.get('right', 0.0)

            # Differential drive calculation
            linear = (left_speed + right_speed) / 2
            angular = (right_speed - left_speed) / 2

            new_state['velocity'] = (
                linear * math.cos(new_state['orientation']),
                linear * math.sin(new_state['orientation'])
            )
            new_state['orientation'] += angular * 0.1

        elif command.get('type') == 'propulsion_pulse':
            # Magnetic propulsion pulse
            strength = command.get('strength', 0.5)
            duration = command.get('duration', 1.0)
            frequency = command.get('frequency', 33.0)

            # Calculate magnetic force based on nearby fields
            magnetic_force = self._calculate_magnetic_force(new_state['position'], world, strength, frequency)
            force_x, force_y = magnetic_force

            # Apply force to velocity (impulse)
            impulse_factor = strength * duration * 0.5  # Simplified impulse calculation
            new_state['velocity'] = (
                new_state['velocity'][0] + force_x * impulse_factor,
                new_state['velocity'][1] + force_y * impulse_factor
            )

        elif command.get('type') == 'levitation':
            # Magnetic levitation
            height = command.get('height', 0.1)
            # Reduce downward velocity for levitation effect
            new_state['velocity'] = (
                new_state['velocity'][0],
                max(new_state['velocity'][1] - height * 0.1, -0.1)  # Limit upward velocity
            )

        elif command.get('type') == 'magnetic_gradient':
            # Magnetic field gradient movement
            direction = command.get('direction', 'forward')
            strength = command.get('strength', 0.5)

            # Convert direction to vector
            dir_vectors = {
                'forward': (1, 0),
                'backward': (-1, 0),
                'left': (0, -1),
                'right': (0, 1)
            }
            dir_x, dir_y = dir_vectors.get(direction, (1, 0))

            # Apply gradient force
            gradient_force = strength * 0.3
            new_state['velocity'] = (
                new_state['velocity'][0] + dir_x * gradient_force,
                new_state['velocity'][1] + dir_y * gradient_force
            )

        return new_state

    def _calculate_magnetic_force(self, position: Tuple[float, float], world: VirtualWorld,
                                strength: float, frequency: float) -> Tuple[float, float]:
        """Calculate magnetic force at a position based on world magnetic fields"""
        total_force_x, total_force_y = 0.0, 0.0

        for field in world.magnetic_fields:
            field_pos = field['position']
            field_strength = field['strength']
            field_range = field['range']
            attractive = field.get('attractive', True)

            # Calculate distance and direction to field source
            dx = field_pos[0] - position[0]
            dy = field_pos[1] - position[1]
            distance = math.sqrt(dx*dx + dy*dy)

            if distance < field_range and distance > 0.1:  # Avoid division by zero
                # Force magnitude (inverse square law with some modifications)
                force_magnitude = field_strength * strength / (distance * distance + 1)

                # Frequency resonance effect
                if field.get('frequency', 0) > 0:
                    resonance_factor = 1 + 0.5 * math.exp(-abs(field['frequency'] - frequency) / 10)
                    force_magnitude *= resonance_factor

                # Direction (attractive or repulsive)
                direction_factor = 1 if attractive else -1
                force_x = direction_factor * force_magnitude * (dx / distance)
                force_y = direction_factor * force_magnitude * (dy / distance)

                total_force_x += force_x
                total_force_y += force_y

        return (total_force_x, total_force_y)

    def _apply_physics(self, agent_state: Dict, world: VirtualWorld) -> Dict:
        """Apply physics to agent state"""
        new_state = agent_state.copy()

        # Update position based on velocity
        vx, vy = new_state['velocity']
        px, py = new_state['position']

        new_px = px + vx * 0.1  # Time step
        new_py = py + vy * 0.1

        # Apply world boundaries
        width, height = world.dimensions
        new_px = max(0, min(width, new_px))
        new_py = max(0, min(height, new_py))

        # Calculate distance traveled
        distance = math.sqrt((new_px - px)**2 + (new_py - py)**2)
        new_state['distance_traveled'] += distance

        new_state['position'] = (new_px, new_py)

        # Apply friction and air resistance
        friction = world.physics_parameters['friction_coefficient']
        air_resistance = world.physics_parameters['air_resistance']

        new_vx = vx * (1 - friction * 0.1) * (1 - air_resistance)
        new_vy = vy * (1 - friction * 0.1) * (1 - air_resistance)

        # Clamp velocity
        max_vel = world.physics_parameters['max_velocity']
        speed = math.sqrt(new_vx**2 + new_vy**2)
        if speed > max_vel:
            new_vx = (new_vx / speed) * max_vel
            new_vy = (new_vy / speed) * max_vel

        new_state['velocity'] = (new_vx, new_vy)

        return new_state

    def _check_collisions(self, agent_state: Dict, world: VirtualWorld) -> bool:
        """Check for collisions with obstacles"""
        agent_pos = agent_state['position']

        for obstacle in world.obstacles:
            if obstacle.get('blocking', True):
                obs_pos = obstacle['position']
                obs_size = obstacle['size']

                distance = math.sqrt((agent_pos[0] - obs_pos[0])**2 + (agent_pos[1] - obs_pos[1])**2)
                if distance < obs_size:
                    return True

        return False

    def _check_goals(self, agent_state: Dict, world: VirtualWorld) -> List[Dict]:
        """Check for achieved goals"""
        agent_pos = agent_state['position']
        achieved = []

        for goal in world.goals:
            goal_pos = goal['position']
            distance = math.sqrt((agent_pos[0] - goal_pos[0])**2 + (agent_pos[1] - goal_pos[1])**2)

            if distance < 1.0:  # Goal achievement radius
                achieved.append(goal)

        # Remove achieved goals from world
        for goal in achieved:
            if goal in world.goals:
                world.goals.remove(goal)

        return achieved

    def _calculate_fitness(self, final_state: Dict, world: VirtualWorld,
                          simulation_log: List, start_position: Tuple) -> Dict:
        """Calculate fitness metrics for the behavior"""
        goals_achieved = len(final_state['goals_achieved'])
        total_goal_value = sum(goal.get('value', 0) for goal in final_state['goals_achieved'])

        # Distance efficiency
        total_distance = final_state['distance_traveled']
        net_distance = math.sqrt((final_state['position'][0] - start_position[0])**2 +
                               (final_state['position'][1] - start_position[1])**2)
        efficiency = net_distance / max(total_distance, 0.1)

        # Survival metrics
        survival_time = len(simulation_log)
        final_energy = final_state['energy']
        final_health = final_state['health']
        collisions = final_state['collisions']

        # Magnetic field interaction bonus
        magnetic_interactions = self._calculate_magnetic_interactions(simulation_log, world)
        magnetic_efficiency = magnetic_interactions['efficiency']
        field_utilization = magnetic_interactions['utilization']

        # Composite fitness score
        fitness_score = (
            goals_achieved * 50 +           # Goal achievement (major factor)
            total_goal_value * 0.5 +        # Goal value
            survival_time * 0.1 +           # Survival time
            final_energy * 0.05 +           # Energy conservation
            final_health * 0.1 -            # Health preservation
            collisions * 10 -               # Collision penalty
            (1 - efficiency) * 20 +         # Inefficiency penalty
            magnetic_efficiency * 30 +      # Magnetic efficiency bonus
            field_utilization * 15          # Field utilization bonus
        )

        return {
            'fitness_score': max(0, fitness_score),
            'goals_achieved': goals_achieved,
            'total_goal_value': total_goal_value,
            'survival_time': survival_time,
            'final_energy': final_energy,
            'final_health': final_health,
            'collisions': collisions,
            'efficiency': efficiency,
            'total_distance': total_distance,
            'magnetic_efficiency': magnetic_efficiency,
            'field_utilization': field_utilization
        }

    def _calculate_magnetic_interactions(self, simulation_log: List, world: VirtualWorld) -> Dict:
        """Calculate magnetic field interaction metrics"""
        total_interactions = 0
        effective_interactions = 0
        energy_used = 0

        for state in simulation_log:
            position = state['position']

            for field in world.magnetic_fields:
                field_pos = field['position']
                field_range = field['range']

                distance = math.sqrt((position[0] - field_pos[0])**2 + (position[1] - field_pos[1])**2)

                if distance < field_range:
                    total_interactions += 1

                    # Check if interaction was effective (moved towards/away from field appropriately)
                    velocity = state.get('velocity', (0, 0))

                    # Simple effectiveness metric: moving in direction that could be influenced by field
                    if abs(velocity[0]) > 0.01 or abs(velocity[1]) > 0.01:
                        effective_interactions += 1

                    # Estimate energy used for magnetic interactions
                    field_strength = field['strength']
                    energy_used += field_strength * 0.01  # Simplified energy calculation

        # Calculate metrics
        efficiency = effective_interactions / max(total_interactions, 1)
        utilization = total_interactions / max(len(simulation_log), 1)

        return {
            'efficiency': efficiency,
            'utilization': utilization,
            'total_interactions': total_interactions,
            'effective_interactions': effective_interactions,
            'energy_used': energy_used
        }

class EvolutionaryShard:
    """Main evolutionary intelligence shard"""

    def __init__(self, hardware_interface=None):
        self.hardware = hardware_interface
        self.mutation_engine = MutationEngine()
        self.world_simulator = WorldSimulator()

        self.genomes = {}
        self.population = []
        self.generation = 0
        self.best_genome = None

        # Evolution parameters
        self.population_size = 50
        self.elitism_rate = 0.1
        self.mutation_rate = 0.3
        self.crossover_rate = 0.6

        # Initialize base genome
        self._create_base_genome()

    def _create_base_genome(self):
        """Create the initial base genome"""
        base_genes = {
            'speed': 0.5,
            'turn_rate': 0.3,
            'exploration_radius': 0.8,
            'obstacle_avoidance_distance': 1.0,
            'goal_seeking_priority': 0.7,
            'energy_efficiency': 0.6,
            'behavior_sequence': ['forward', 'magnetic_pulse', 'levitate', 'figure_eight'],
            'parameter_weights': [0.4, 0.3, 0.3],
            # Magnetic propulsion genes
            'magnetic_strength': 0.5,
            'propulsion_frequency': 33.0,
            'coil_configuration': 'sequential',  # 'sequential', 'parallel', 'gradient'
            'levitation_height': 0.1,
            'field_gradient_direction': 'forward',
            'resonance_tuning': 0.8,
            'pulse_duration': 1.0,
            'magnetic_efficiency': 0.7
        }

        base_genome = Genome(
            id="base_genome_v1",
            genes=base_genes,
            fitness=0.0,
            generation=0
        )

        self.genomes[base_genome.id] = base_genome

        # Create initial population with variations
        initial_population = [base_genome]

        # Generate 9 more genomes with slight variations
        for i in range(9):
            varied_genes = base_genes.copy()
            # Add small random variations
            varied_genes['speed'] = max(0.1, min(1.0, base_genes['speed'] + random.gauss(0, 0.1)))
            varied_genes['turn_rate'] = max(0.1, min(0.5, base_genes['turn_rate'] + random.gauss(0, 0.05)))
            varied_genes['exploration_radius'] = max(0.3, min(1.5, base_genes['exploration_radius'] + random.gauss(0, 0.1)))
            # Magnetic variations
            varied_genes['magnetic_strength'] = max(0.1, min(1.0, base_genes['magnetic_strength'] + random.gauss(0, 0.1)))
            varied_genes['propulsion_frequency'] = max(10.0, min(100.0, base_genes['propulsion_frequency'] + random.gauss(0, 5.0)))
            varied_genes['levitation_height'] = max(0.05, min(0.5, base_genes['levitation_height'] + random.gauss(0, 0.05)))
            varied_genes['pulse_duration'] = max(0.5, min(2.0, base_genes['pulse_duration'] + random.gauss(0, 0.2)))

            varied_genome = Genome(
                id=f"initial_genome_{i+1}",
                genes=varied_genes,
                fitness=0.0,
                generation=0
            )

            self.genomes[varied_genome.id] = varied_genome
            initial_population.append(varied_genome)

        self.population = initial_population

    async def evolve_generation(self) -> Dict:
        """Run one generation of evolution"""
        self.generation += 1
        print(f"\n🧬 [EVOLUTION] Generation {self.generation} - Population: {len(self.population)}")

        # Evaluate current population
        fitness_scores = await self._evaluate_population()

        # Select parents
        parents = self._select_parents(fitness_scores)

        # Create offspring
        offspring = await self._create_offspring(parents)

        # Update population
        self.population = self._select_survivors(fitness_scores, offspring)

        # Update best genome
        best_fitness = max(fitness_scores.values())
        best_genome_id = max(fitness_scores, key=fitness_scores.get)
        self.best_genome = self.genomes[best_genome_id]

        print(f"   🏆 [EVOLUTION] Best Fitness: {best_fitness:.2f} (Genome: {best_genome_id})")
        print(f"   📊 [EVOLUTION] Population Stats - Mean: {np.mean(list(fitness_scores.values())):.2f}, "
              f"Std: {np.std(list(fitness_scores.values())):.2f}")

        return {
            'generation': self.generation,
            'best_fitness': best_fitness,
            'population_size': len(self.population),
            'best_genome_id': best_genome_id
        }

    async def _evaluate_population(self) -> Dict[str, float]:
        """Evaluate fitness of all genomes in population"""
        fitness_scores = {}

        for genome in self.population:
            # Create virtual world for testing
            world = self.world_simulator.create_world(f"eval_world_{genome.id}")

            # Convert genome to phenotype
            phenotype = await self._genome_to_phenotype(genome)

            # Simulate behavior
            simulation_result = await self.world_simulator.simulate_behavior(world, phenotype)

            # Update genome fitness
            fitness = simulation_result['fitness_metrics']['fitness_score']
            genome.fitness = fitness
            fitness_scores[genome.id] = fitness

            # Store genome
            self.genomes[genome.id] = genome

        return fitness_scores

    async def _genome_to_phenotype(self, genome: Genome) -> BehaviorPhenotype:
        """Convert genome to executable behavior phenotype"""
        motor_commands = []

        # Generate behavior sequence based on genome
        behavior_sequence = genome.genes.get('behavior_sequence', ['forward'])
        speed = genome.genes.get('speed', 0.5)
        turn_rate = genome.genes.get('turn_rate', 0.3)
        exploration_radius = genome.genes.get('exploration_radius', 0.8)

        # Magnetic parameters
        magnetic_strength = genome.genes.get('magnetic_strength', 0.5)
        propulsion_frequency = genome.genes.get('propulsion_frequency', 33.0)
        levitation_height = genome.genes.get('levitation_height', 0.1)
        gradient_direction = genome.genes.get('field_gradient_direction', 'forward')
        pulse_duration = genome.genes.get('pulse_duration', 1.0)

        for behavior in behavior_sequence:
            if behavior == 'forward':
                motor_commands.append({
                    'type': 'differential_drive',
                    'linear': speed,
                    'angular': 0.0,
                    'duration': 2.0
                })
            elif behavior == 'rotate':
                motor_commands.append({
                    'type': 'differential_drive',
                    'linear': 0.0,
                    'angular': turn_rate,
                    'duration': 1.5
                })
            elif behavior == 'figure_eight':
                # Generate figure-eight pattern
                steps = 20
                for i in range(steps):
                    angle = (i / steps) * 4 * math.pi  # Two full circles
                    linear = speed * 0.8
                    angular = math.sin(angle) * turn_rate
                    motor_commands.append({
                        'type': 'differential_drive',
                        'linear': linear,
                        'angular': angular,
                        'duration': 0.1
                    })
            elif behavior == 'magnetic_pulse':
                motor_commands.append({
                    'type': 'propulsion_pulse',
                    'strength': magnetic_strength,
                    'duration': pulse_duration,
                    'frequency': propulsion_frequency
                })
            elif behavior == 'levitate':
                motor_commands.append({
                    'type': 'levitation',
                    'height': levitation_height
                })
            elif behavior == 'magnetic_move':
                motor_commands.append({
                    'type': 'magnetic_gradient',
                    'direction': gradient_direction,
                    'strength': magnetic_strength
                })

        # Sensor requirements
        sensor_requirements = {
            'vision_range': exploration_radius * 2,
            'obstacle_detection': genome.genes.get('obstacle_avoidance_distance', 1.0),
            'goal_detection': genome.genes.get('goal_seeking_priority', 0.7) * 3
        }

        # Environmental adaptations
        environmental_adaptations = {
            'current_adaptation': genome.genes.get('energy_efficiency', 0.6),
            'temperature_preference': random.uniform(20, 25),
            'depth_adaptation': random.uniform(0, 10)
        }

        return BehaviorPhenotype(
            genome_id=genome.id,
            motor_commands=motor_commands,
            sensor_requirements=sensor_requirements,
            environmental_adaptations=environmental_adaptations,
            fitness_metrics={}
        )

    def _select_parents(self, fitness_scores: Dict[str, float]) -> List[Genome]:
        """Select parents using tournament selection"""
        parents = []
        population_size = len(self.population)

        # If population is too small, just clone all existing genomes
        if population_size < 3:
            return self.population * (population_size // max(1, population_size) + 1)

        # Elitism - keep best performers
        num_elite = int(self.elitism_rate * population_size)
        sorted_genomes = sorted(self.population, key=lambda g: fitness_scores[g.id], reverse=True)
        parents.extend(sorted_genomes[:num_elite])

        # Tournament selection for remaining parents
        while len(parents) < population_size:
            # Select random subset for tournament
            tournament_size = min(5, len(self.population))
            tournament = random.sample(self.population, tournament_size)

            # Select winner
            winner = max(tournament, key=lambda g: fitness_scores[g.id])
            parents.append(winner)

        return parents

    async def _create_offspring(self, parents: List[Genome]) -> List[Genome]:
        """Create offspring through crossover and mutation"""
        offspring = []

        while len(offspring) < len(parents):
            # Select two parents
            parent1, parent2 = random.sample(parents, 2)

            # Crossover
            if random.random() < self.crossover_rate:
                child = self.mutation_engine._crossover(parent1, parent2)
            else:
                child = parent1  # Clone if no crossover

            # Mutation
            if random.random() < self.mutation_rate:
                child = await self.mutation_engine.mutate(child)

            offspring.append(child)
            self.genomes[child.id] = child

        return offspring

    def _select_survivors(self, fitness_scores: Dict[str, float], offspring: List[Genome]) -> List[Genome]:
        """Select survivors for next generation"""
        # Combine parents and offspring
        candidates = self.population + offspring

        # Sort by fitness
        candidates.sort(key=lambda g: fitness_scores.get(g.id, 0), reverse=True)

        # Select top performers
        survivors = candidates[:self.population_size]

        return survivors

    async def deploy_best_behavior(self):
        """Deploy the best evolved behavior to hardware"""
        if not self.best_genome or not self.hardware:
            return False

        print(f"   🚀 [EVOLUTION] Deploying best genome: {self.best_genome.id}")

        try:
            # Convert to phenotype
            phenotype = await self._genome_to_phenotype(self.best_genome)

            # Execute on hardware
            for command in phenotype.motor_commands[:10]:  # Limit to first 10 commands for safety
                if command['type'] == 'differential_drive':
                    await self.hardware.motors.differential_drive(
                        command['linear'],
                        command['angular']
                    )
                    await asyncio.sleep(command.get('duration', 0.5))

                elif command['type'] == 'propulsion_pulse':
                    await self.hardware.execute_magnetic_commands({
                        'propulsion_pulse': {
                            'strength': command['strength'],
                            'duration': command['duration'],
                            'frequency': command.get('frequency')
                        }
                    })
                    await asyncio.sleep(command['duration'])

                elif command['type'] == 'levitation':
                    await self.hardware.execute_magnetic_commands({
                        'levitation': {'height': command['height']}
                    })
                    await asyncio.sleep(2.0)

                elif command['type'] == 'magnetic_gradient':
                    await self.hardware.execute_magnetic_commands({
                        'magnetic_gradient': {
                            'direction': command['direction'],
                            'strength': command['strength']
                        }
                    })
                    await asyncio.sleep(1.0)

                # Stop between commands
                await self.hardware.motors.differential_drive(0.0, 0.0)
                await asyncio.sleep(0.2)

            print("   ✅ [EVOLUTION] Behavior deployment complete")
            return True

        except Exception as e:
            print(f"   ❌ [EVOLUTION] Deployment failed: {e}")
            return False

    async def save_evolution_state(self, filepath: str):
        """Save current evolution state"""
        state = {
            'generation': self.generation,
            'population_size': len(self.population),
            'best_genome_id': self.best_genome.id if self.best_genome else None,
            'genomes': {gid: {
                'id': g.id,
                'genes': g.genes,
                'fitness': g.fitness,
                'generation': g.generation,
                'parent_ids': g.parent_ids,
                'mutation_history': g.mutation_history
            } for gid, g in self.genomes.items()},
            'population_ids': [g.id for g in self.population]
        }

        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)

        print(f"   💾 [EVOLUTION] State saved to {filepath}")

    async def load_evolution_state(self, filepath: str):
        """Load evolution state"""
        if not os.path.exists(filepath):
            return False

        with open(filepath, 'r') as f:
            state = json.load(f)

        self.generation = state['generation']

        # Reconstruct genomes
        self.genomes = {}
        for gid, g_data in state['genomes'].items():
            genome = Genome(
                id=g_data['id'],
                genes=g_data['genes'],
                fitness=g_data['fitness'],
                generation=g_data['generation'],
                parent_ids=g_data['parent_ids'],
                mutation_history=g_data['mutation_history']
            )
            self.genomes[gid] = genome

        # Reconstruct population
        self.population = [self.genomes[gid] for gid in state['population_ids'] if gid in self.genomes]

        # Set best genome
        if state['best_genome_id'] and state['best_genome_id'] in self.genomes:
            self.best_genome = self.genomes[state['best_genome_id']]

        print(f"   📂 [EVOLUTION] State loaded from {filepath}")
        return True