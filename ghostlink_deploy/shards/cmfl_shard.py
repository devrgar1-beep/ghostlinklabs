
import asyncio
from swarm_analysis import analyze_swarm_block, l1_distance

class CMFLCycle:
    def __init__(self, agents, hardware_interface=None):
        self.agents = agents
        self.cycle_count = 0
        self.prev_swarm_grid = None
        self.hardware = hardware_interface
        self.environmental_history = []
        self.vision_history = []

    async def run_cycle(self):
        self.cycle_count += 1
        print(f"\n🔄 [CMFL CYCLE {self.cycle_count}]")

        # Enhanced collapse phase with hardware context
        results = await self.collapse_phase()

        self.visualize_swarm(results)

        # Enhanced mirror phase with sensor fusion
        patterns = await self.mirror_phase(results)

        # Enhanced forge phase with environmental awareness
        action = await self.forge_phase(patterns)

        await self.link_phase(action)

        return action

    def visualize_swarm(self, results):
        print("   🐝 [SWARM INTELLIGENCE] HIVE MIND ACTIVITY MAP")
        print("   " + "-"*66)
        
        grid_chars = [[' ' for _ in range(8)] for _ in range(8)]
        
        for i, res in enumerate(results):
            row = i // 8
            col = i % 8
            if row < 8 and col < 8:
                v = abs(res['variance'])
                if v > 0.2: 
                    char = '█'
                elif v > 0.1: 
                    char = '▓'
                elif v > 0.05: 
                    char = '▒'
                elif v > 0.01: 
                    char = '░'
                else: 
                    char = '·'
                grid_chars[row][col] = char
        
        lines = []
        for row in grid_chars:
            line = "   | " + " ".join(row) + " |"
            print(line)
            lines.append(line)
            
        print("   " + "-"*66)
        
        try:
            stats = analyze_swarm_block(lines, cycle=self.cycle_count)
            
            l1_diff = 0
            if self.prev_swarm_grid:
                l1_diff = l1_distance(self.prev_swarm_grid, stats.grid)
            
            self.prev_swarm_grid = stats.grid
            
            print(f"   📊 [SWARM STATS] Mean: {stats.mean:.2f} | Std: {stats.std:.2f} | High Cells: {stats.high_cells}")
            print(f"   🔗 [CLUSTERS] Count: {stats.cluster_count} | Sizes: {stats.cluster_sizes}")
            if self.cycle_count > 1:
                print(f"   🌊 [DYNAMICS] L1 Delta: {l1_diff}")
                
        except Exception as e:
            print(f"   ⚠️ [SWARM ANALYSIS] Failed: {e}")

        print(f"   🐝 Active Agents: {len(results)} | Collective Variance: {sum(abs(r['variance']) for r in results):.4f}")

    async def collapse_phase(self):
        active_count = 64 
        active_agents = self.agents
        
        tasks = [agent.process(f"Tick_{self.cycle_count}") for agent in active_agents]
        return await asyncio.gather(*tasks)

    async def mirror_phase(self, results):
        total_variance = sum(abs(r['variance']) for r in results) / len(results) if results else 0

        # Enhanced pattern analysis with hardware context
        hardware_patterns = await self._analyze_hardware_patterns()

        # Calculate agent role distribution
        role_variance = {}
        hardware_influence = {}

        for result in results:
            role = result.get('role', 'Unknown')
            variance = result.get('variance', 0)
            hw_influenced = result.get('hardware_influenced', False)

            if role not in role_variance:
                role_variance[role] = []
                hardware_influence[role] = 0

            role_variance[role].append(variance)
            if hw_influenced:
                hardware_influence[role] += 1

        # Calculate role-specific statistics
        role_stats = {}
        for role, variances in role_variance.items():
            if variances:
                role_stats[role] = {
                    'mean_variance': sum(variances) / len(variances),
                    'hw_influence_ratio': hardware_influence[role] / len(variances),
                    'agent_count': len(variances)
                }

        return {
            "variance_level": total_variance,
            "role_statistics": role_stats,
            "hardware_patterns": hardware_patterns,
            "environmental_stability": hardware_patterns.get('stability_index', 1.0),
            "vision_quality": hardware_patterns.get('vision_sharpness', 0.5)
        }

    async def forge_phase(self, patterns):
        variance = patterns['variance_level']
        environmental_stability = patterns.get('environmental_stability', 1.0)
        vision_quality = patterns.get('vision_quality', 0.5)

        # Enhanced decision making with hardware context
        base_action = "MAINTAIN"

        # Variance-based decisions
        if variance > 0.15:
            base_action = "ADAPT"
        elif variance < 0.02:
            base_action = "STAGNATION_WARNING"

        # Hardware-modulated decisions
        if environmental_stability < 0.7:
            # Environmental instability detected
            if base_action == "MAINTAIN":
                base_action = "ENVIRONMENTAL_ADAPT"
            print(f"   🌡️ [FORGE] Environmental instability detected (stability: {environmental_stability:.2f})")

        if vision_quality < 0.3:
            # Poor vision conditions
            if base_action == "MAINTAIN":
                base_action = "VISION_OPTIMIZE"
            print(f"   👁️ [FORGE] Vision quality suboptimal (quality: {vision_quality:.2f})")

        # Role-based analysis
        role_stats = patterns.get('role_statistics', {})
        sensory_hw_ratio = role_stats.get('Sensory', {}).get('hw_influence_ratio', 0)
        if sensory_hw_ratio < 0.5:
            print(f"   🧠 [FORGE] Low hardware influence on sensory agents ({sensory_hw_ratio:.1%})")

        return base_action

    async def _analyze_hardware_patterns(self):
        """Analyze hardware sensor patterns for decision making"""
        patterns = {}

        if not self.hardware:
            return patterns

        try:
            # Environmental pattern analysis
            env_data = await self.hardware.read_environmental_sensors()
            self.environmental_history.append(env_data)
            if len(self.environmental_history) > 10:
                self.environmental_history.pop(0)

            if len(self.environmental_history) >= 3:
                # Analyze environmental trends
                temps = [d.get('temperature', 25) for d in self.environmental_history[-5:]]
                pressures = [d.get('pressure', 1013) for d in self.environmental_history[-5:]]

                temp_trend = (temps[-1] - temps[0]) / len(temps) if temps[0] != temps[-1] else 0
                pressure_trend = (pressures[-1] - pressures[0]) / len(pressures) if pressures[0] != pressures[-1] else 0

                patterns.update({
                    'temperature_trend': temp_trend,
                    'pressure_trend': pressure_trend,
                    'environmental_volatility': abs(temp_trend) + abs(pressure_trend),
                    'stability_index': 1.0 / (1.0 + abs(temp_trend) + abs(pressure_trend))
                })

            # Vision pattern analysis
            vision_data = await self.hardware.capture_and_process_vision()
            self.vision_history.append(vision_data)
            if len(self.vision_history) > 5:
                self.vision_history.pop(0)

            if len(self.vision_history) >= 2:
                # Analyze vision trends
                brightness_trend = vision_data.get('brightness', 128) - self.vision_history[-2].get('brightness', 128)
                motion_level = sum(abs(v) for vec in vision_data.get('motion_vectors', [])
                                  for v in vec) / max(1, len(vision_data.get('motion_vectors', [])))

                patterns.update({
                    'brightness_trend': brightness_trend,
                    'motion_level': motion_level,
                    'vision_sharpness': vision_data.get('focus_sharpness', 0),
                    'scene_stability': 1.0 / (1.0 + motion_level)
                })

        except Exception as e:
            patterns['error'] = str(e)

        return patterns

    async def link_phase(self, action):
        """Link phase for hardware actuation based on decisions"""
        if not self.hardware:
            return

        try:
            # Start PID control if not active
            if hasattr(self.hardware, 'motors') and not self.hardware.motors.control_loop_active:
                await self.hardware.motors.start_control_loop()

            # Execute hardware actions based on CMFL decisions
            if action == "ENVIRONMENTAL_ADAPT":
                # Environmental adaptation behaviors
                env_patterns = await self._analyze_hardware_patterns()
                stability = env_patterns.get('stability_index', 1.0)

                if stability < 0.5:  # Very unstable environment
                    await self.hardware.motors.execute_behavior("obstacle_avoidance")
                    print("   🌪️  [LINK] Environmental adaptation: obstacle avoidance (unstable)")
                elif stability < 0.8:  # Moderately unstable
                    await self.hardware.motors.execute_behavior("rotate",
                        {"angle": 45.0, "speed": 0.2, "direction": 1})
                    print("   🌡️  [LINK] Environmental adaptation: exploratory rotation")
                else:  # Relatively stable
                    await self.hardware.motors.execute_behavior("forward",
                        {"distance": 1.0, "speed": 0.3})
                    print("   🌿 [LINK] Environmental adaptation: stable forward movement")

            elif action == "VISION_OPTIMIZE":
                # Vision optimization behaviors
                vision_patterns = await self._analyze_hardware_patterns()
                sharpness = vision_patterns.get('vision_sharpness', 0)
                motion = vision_patterns.get('motion_level', 0)

                if sharpness < 0.2:  # Very poor vision
                    # Adjust camera and move to improve visibility
                    await self.hardware.camera.adjust_exposure()
                    await self.hardware.motors.execute_behavior("rotate",
                        {"angle": 90.0, "speed": 0.1, "direction": -1})
                    print("   👁️  [LINK] Vision optimization: exposure adjustment + repositioning")
                elif motion > 50:  # High motion, unstable scene
                    await self.hardware.motors.differential_drive(0.0, 0.0)  # Stop and stabilize
                    print("   📹 [LINK] Vision optimization: stopping for stabilization")
                else:  # Moderate vision issues
                    await self.hardware.camera.adjust_focus()
                    print("   🔍 [LINK] Vision optimization: focus adjustment")

            elif action == "ADAPT":
                # General adaptation based on swarm variance
                patterns = await self._analyze_hardware_patterns()
                variance_level = patterns.get('variance_level', 0)

                if variance_level > 0.2:  # High variance = exploration
                    await self.hardware.motors.execute_behavior("figure_eight",
                        {"radius": 0.8, "speed": 0.4})
                    print("   🌀 [LINK] High variance adaptation: figure-eight exploration")
                elif variance_level > 0.1:  # Medium variance = investigation
                    await self.hardware.motors.execute_behavior("rotate",
                        {"angle": 180.0, "speed": 0.25, "direction": 1})
                    print("   🔍 [LINK] Medium variance adaptation: full rotation scan")
                else:  # Low variance = consolidation
                    await self.hardware.motors.execute_behavior("forward",
                        {"distance": 0.5, "speed": 0.2})
                    print("   📍 [LINK] Low variance adaptation: precise positioning")

            elif action == "MAINTAIN":
                # Maintenance behaviors for stable operation
                await self.hardware.motors.differential_drive(0.0, 0.0)  # Hold position
                print("   ⏸️  [LINK] Maintenance: holding position")

            elif action == "STAGNATION_WARNING":
                # Anti-stagnation behaviors
                await self.hardware.motors.execute_behavior("rotate",
                    {"angle": 30.0, "speed": 0.15, "direction": -1})
                print("   ⚠️  [LINK] Stagnation warning: small rotation to stimulate activity")

            # Update PID control after behavior execution
            if hasattr(self.hardware, 'motors'):
                await self.hardware.motors.update_pid_control()

        except Exception as e:
            print(f"   ⚠️  [LINK] Hardware actuation failed: {e}")
            # Fallback to basic motor control
            try:
                if hasattr(self.hardware, 'motors'):
                    await self.hardware.motors.differential_drive(0.0, 0.0)
            except Exception as e2:
                print(f"   ❌ [LINK] Fallback actuation also failed: {e2}")
