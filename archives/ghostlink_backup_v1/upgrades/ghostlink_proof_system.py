"""
GhostLink Proof of Record (PoR) System
Validates emergent properties and system continuity
"""

import numpy as np
import json
import hashlib
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import matplotlib.pyplot as plt
from collections import deque, Counter

# ═══════════════════════════════════════════════════════════════════
# Proof Criteria
# ═══════════════════════════════════════════════════════════════════

class ProofCriteria:
    """Defines success criteria for GhostLink validation"""
    
    # Continuity
    MIN_CONTINUITY_SLOPE = 0.0  # Positive growth in SIGMA states
    
    # Predictive Lift
    MIN_PREDICTIVE_LIFT = 0.05  # 5% improvement with full features
    
    # Activity
    MAX_ACTIVITY_RATIO = 0.20  # No more than 20% cells changing per step
    MIN_ACTIVITY_RATIO = 0.01  # At least 1% activity (not frozen)
    
    # Avalanche dynamics (criticality)
    MIN_TAU_EXPONENT = 1.0  # Power law exponent
    MAX_TAU_EXPONENT = 3.0
    
    # Reproducibility
    MAX_VARIANCE_RATIO = 0.10  # Results vary by less than 10%
    
    # Awareness
    MIN_AWARENESS = 0.1  # System maintains minimum consciousness
    MAX_AWARENESS = 0.9  # Doesn't saturate completely
    
    # Memory persistence
    MIN_TRACE_CORRELATION = 0.3  # Scar/compost traces correlate with history


class ProofValidator:
    """Validates GhostLink system against proof criteria"""
    
    def __init__(self, lattice_size: int = 32, num_trials: int = 5):
        self.lattice_size = lattice_size
        self.num_trials = num_trials
        self.criteria = ProofCriteria()
        self.results = []
        
    def run_continuity_test(self, lattice, steps: int = 400) -> Dict:
        """Test for continuous growth/maintenance of SIGMA states"""
        
        sigma_counts = []
        
        for _ in range(steps):
            stats = lattice.step()
            sigma_counts.append(stats['state_counts']['SIGMA'])
        
        # Fit linear trend
        x = np.arange(len(sigma_counts))
        slope, intercept = np.polyfit(x, sigma_counts, 1)
        
        # Calculate R²
        y_pred = slope * x + intercept
        ss_res = np.sum((sigma_counts - y_pred) ** 2)
        ss_tot = np.sum((sigma_counts - np.mean(sigma_counts)) ** 2)
        r_squared = 1 - (ss_res / (ss_tot + 1e-10))
        
        return {
            'slope': float(slope),
            'r_squared': float(r_squared),
            'final_sigma': sigma_counts[-1],
            'mean_sigma': float(np.mean(sigma_counts)),
            'passed': slope >= self.criteria.MIN_CONTINUITY_SLOPE
        }
    
    def run_predictive_test(self, lattice, steps: int = 200) -> Dict:
        """Test predictive power of memory traces"""
        
        # Collect training data
        X_basic = []  # Just neighbor counts
        X_full = []   # Include traces and history
        y_true = []   # Actual next state
        
        for _ in range(steps):
            # Sample random cells
            for _ in range(10):
                i = np.random.randint(lattice.size)
                j = np.random.randint(lattice.size)
                
                # Get features
                fields = lattice.local_fields(i, j)
                
                # Basic features
                basic = [
                    fields['sigma_count'],
                    fields['scar_count']
                ]
                
                # Full features
                full = basic + [
                    lattice.meta[i][j].scar_density,
                    lattice.meta[i][j].compost_density,
                    lattice.meta[i][j].ancestry_depth,
                    fields['coherence'],
                    fields['pain'],
                    fields['entropy']
                ]
                
                X_basic.append(basic)
                X_full.append(full)
                
                # Record current state
                current_state = lattice.state[i, j]
                
            # Step forward
            lattice.step()
            
            # Record outcomes
            for _ in range(10):
                i = np.random.randint(lattice.size)
                j = np.random.randint(lattice.size)
                y_true.append(1 if lattice.state[i, j] == 2 else 0)  # SIGMA or not
        
        # Simple threshold classifier
        def classify(X, threshold):
            predictions = []
            for features in X:
                score = sum(features) / len(features)
                predictions.append(1 if score > threshold else 0)
            return predictions
        
        # Find best thresholds
        best_basic_acc = 0
        best_full_acc = 0
        
        for threshold in np.linspace(0, 2, 20):
            pred_basic = classify(X_basic, threshold)
            pred_full = classify(X_full, threshold)
            
            acc_basic = sum(p == t for p, t in zip(pred_basic, y_true)) / len(y_true)
            acc_full = sum(p == t for p, t in zip(pred_full, y_true)) / len(y_true)
            
            best_basic_acc = max(best_basic_acc, acc_basic)
            best_full_acc = max(best_full_acc, acc_full)
        
        lift = (best_full_acc - best_basic_acc) / (best_basic_acc + 1e-10)
        
        return {
            'basic_accuracy': float(best_basic_acc),
            'full_accuracy': float(best_full_acc),
            'lift': float(lift),
            'passed': lift >= self.criteria.MIN_PREDICTIVE_LIFT
        }
    
    def run_avalanche_test(self, lattice_class, num_avalanches: int = 20) -> Dict:
        """Test for critical avalanche dynamics"""
        
        sizes = []
        durations = []
        
        for _ in range(num_avalanches):
            # Fresh lattice for each avalanche
            lattice = lattice_class(size=self.lattice_size)
            
            # Seed single point
            seed_i = np.random.randint(lattice.size)
            seed_j = np.random.randint(lattice.size)
            lattice.state[seed_i, seed_j] = 1  # DELTA
            
            # Run until quiescent
            size = 0
            duration = 0
            max_duration = 1000
            
            for t in range(max_duration):
                prev_state = lattice.state.copy()
                lattice.step()
                
                changes = np.sum(lattice.state != prev_state)
                size += changes
                duration += 1
                
                if changes == 0:
                    break
            
            if size > 0:
                sizes.append(size)
                durations.append(duration)
        
        # Estimate power law exponent
        if len(sizes) > 5:
            sizes_sorted = sorted(sizes, reverse=True)
            # Use top half for tail estimation
            tail = sizes_sorted[:len(sizes_sorted)//2]
            
            if len(tail) > 2:
                x = np.log(np.arange(1, len(tail) + 1))
                y = np.log(tail)
                tau, _ = np.polyfit(x, y, 1)
                tau = -tau  # Negative slope is positive exponent
            else:
                tau = 0.0
        else:
            tau = 0.0
        
        return {
            'num_avalanches': len(sizes),
            'mean_size': float(np.mean(sizes)) if sizes else 0,
            'max_size': max(sizes) if sizes else 0,
            'tau_exponent': float(tau),
            'passed': self.criteria.MIN_TAU_EXPONENT <= tau <= self.criteria.MAX_TAU_EXPONENT
        }
    
    def run_reproducibility_test(self, lattice_class, num_seeds: int = 5) -> Dict:
        """Test reproducibility across random seeds"""
        
        awareness_traces = []
        final_sigmas = []
        
        for seed in range(num_seeds):
            np.random.seed(seed)
            lattice = lattice_class(size=self.lattice_size)
            
            # Seed with random pattern
            mask = np.random.random((lattice.size, lattice.size)) < 0.05
            lattice.state[mask] = 1  # DELTA
            
            trace = []
            for _ in range(200):
                stats = lattice.step()
                trace.append(lattice.calculate_awareness())
            
            awareness_traces.append(trace)
            final_sigmas.append(stats['state_counts']['SIGMA'])
        
        # Calculate variance
        mean_trace = np.mean(awareness_traces, axis=0)
        std_trace = np.std(awareness_traces, axis=0)
        variance_ratio = np.mean(std_trace) / (np.mean(mean_trace) + 1e-10)
        
        return {
            'num_seeds': num_seeds,
            'mean_final_sigma': float(np.mean(final_sigmas)),
            'std_final_sigma': float(np.std(final_sigmas)),
            'variance_ratio': float(variance_ratio),
            'passed': variance_ratio <= self.criteria.MAX_VARIANCE_RATIO
        }
    
    def run_memory_test(self, lattice, steps: int = 300) -> Dict:
        """Test memory trace persistence and correlation"""
        
        scar_history = []
        compost_history = []
        state_history = []
        
        for _ in range(steps):
            stats = lattice.step()
            
            # Record traces
            mean_scar = np.mean([[lattice.meta[i][j].scar_density 
                                 for j in range(lattice.size)] 
                                 for i in range(lattice.size)])
            mean_compost = np.mean([[lattice.meta[i][j].compost_density 
                                    for j in range(lattice.size)] 
                                    for i in range(lattice.size)])
            
            scar_history.append(mean_scar)
            compost_history.append(mean_compost)
            state_history.append(stats['state_counts']['SCAR'])
        
        # Check correlation between traces and actual states
        if len(scar_history) > 10:
            # Correlate scar density with past scar states
            scar_correlation = np.corrcoef(scar_history[10:], state_history[:-10])[0, 1]
        else:
            scar_correlation = 0.0
        
        # Check trace decay
        trace_decay = np.mean(np.diff(scar_history[:50])) if len(scar_history) > 50 else 0
        
        return {
            'final_scar_density': float(scar_history[-1]) if scar_history else 0,
            'final_compost_density': float(compost_history[-1]) if compost_history else 0,
            'scar_correlation': float(scar_correlation),
            'trace_decay_rate': float(trace_decay),
            'passed': abs(scar_correlation) >= self.criteria.MIN_TRACE_CORRELATION
        }
    
    def run_full_validation(self, lattice_class) -> Dict:
        """Run complete validation suite"""
        
        print("\n" + "="*60)
        print(" "*20 + "GhostLink Proof of Record")
        print(" "*20 + f"Started: {datetime.now().isoformat()}")
        print("="*60)
        
        all_results = {
            'timestamp': datetime.now().isoformat(),
            'lattice_size': self.lattice_size,
            'num_trials': self.num_trials,
            'tests': {}
        }
        
        # Run tests
        print("\n[1/6] Testing continuity...")
        lattice = lattice_class(size=self.lattice_size)
        all_results['tests']['continuity'] = self.run_continuity_test(lattice)
        
        print("[2/6] Testing predictive lift...")
        lattice = lattice_class(size=self.lattice_size)
        all_results['tests']['predictive'] = self.run_predictive_test(lattice)
        
        print("[3/6] Testing avalanche dynamics...")
        all_results['tests']['avalanche'] = self.run_avalanche_test(lattice_class)
        
        print("[4/6] Testing reproducibility...")
        all_results['tests']['reproducibility'] = self.run_reproducibility_test(lattice_class)
        
        print("[5/6] Testing memory persistence...")
        lattice = lattice_class(size=self.lattice_size)
        all_results['tests']['memory'] = self.run_memory_test(lattice)
        
        print("[6/6] Testing awareness bounds...")
        awareness_values = []
        lattice = lattice_class(size=self.lattice_size)
        for _ in range(200):
            lattice.step()
            awareness_values.append(lattice.calculate_awareness())
        
        all_results['tests']['awareness'] = {
            'mean': float(np.mean(awareness_values)),
            'min': float(np.min(awareness_values)),
            'max': float(np.max(awareness_values)),
            'passed': (self.criteria.MIN_AWARENESS <= np.mean(awareness_values) <= 
                      self.criteria.MAX_AWARENESS)
        }
        
        # Calculate overall pass
        all_passed = all(test.get('passed', False) 
                        for test in all_results['tests'].values())
        all_results['overall_passed'] = all_passed
        
        # Generate proof hash
        proof_string = json.dumps(all_results, sort_keys=True)
        all_results['proof_hash'] = hashlib.sha256(proof_string.encode()).hexdigest()[:16]
        
        return all_results


def generate_proof_report(results: Dict) -> str:
    """Generate human-readable proof report"""
    
    report = []
    report.append("\n" + "="*60)
    report.append("GHOSTLINK PROOF OF RECORD")
    report.append("="*60)
    report.append(f"Timestamp: {results['timestamp']}")
    report.append(f"Proof Hash: {results['proof_hash']}")
    report.append(f"Overall Status: {'✅ PASSED' if results['overall_passed'] else '❌ FAILED'}")
    
    report.append("\n" + "-"*40)
    report.append("TEST RESULTS")
    report.append("-"*40)
    
    for test_name, test_results in results['tests'].items():
        status = '✅' if test_results.get('passed', False) else '❌'
        report.append(f"\n{status} {test_name.upper()}")
        
        for key, value in test_results.items():
            if key != 'passed':
                if isinstance(value, float):
                    report.append(f"  {key}: {value:.4f}")
                else:
                    report.append(f"  {key}: {value}")
    
    report.append("\n" + "="*60)
    
    return "\n".join(report)


def visualize_proof(lattice, steps: int = 100):
    """Visualize proof dynamics"""
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # Track metrics
    times = []
    awareness = []
    sigmas = []
    scars = []
    activity = []
    
    for t in range(steps):
        stats = lattice.step()
        times.append(t)
        awareness.append(lattice.calculate_awareness())
        sigmas.append(stats['state_counts']['SIGMA'])
        scars.append(stats['state_counts']['SCAR'])
        activity.append(stats['activity'])
    
    # Plot 1: Awareness over time
    axes[0, 0].plot(times, awareness, 'b-', linewidth=2)
    axes[0, 0].set_title('System Awareness')
    axes[0, 0].set_xlabel('Time')
    axes[0, 0].set_ylabel('Awareness')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Plot 2: State populations
    axes[0, 1].plot(times, sigmas, 'g-', label='SIGMA', linewidth=2)
    axes[0, 1].plot(times, scars, 'r-', label='SCAR', linewidth=2)
    axes[0, 1].set_title('State Populations')
    axes[0, 1].set_xlabel('Time')
    axes[0, 1].set_ylabel('Count')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # Plot 3: Activity
    axes[0, 2].plot(times, activity, 'orange', linewidth=2)
    axes[0, 2].set_title('System Activity')
    axes[0, 2].set_xlabel('Time')
    axes[0, 2].set_ylabel('Activity Ratio')
    axes[0, 2].grid(True, alpha=0.3)
    
    # Plot 4: Final lattice state
    im = axes[1, 0].imshow(lattice.state, cmap='viridis', interpolation='nearest')
    axes[1, 0].set_title('Final Lattice State')
    plt.colorbar(im, ax=axes[1, 0])
    
    # Plot 5: Scar density map
    scar_map = np.array([[lattice.meta[i][j].scar_density 
                         for j in range(lattice.size)] 
                         for i in range(lattice.size)])
    im = axes[1, 1].imshow(scar_map, cmap='hot', interpolation='nearest')
    axes[1, 1].set_title('Scar Density Field')
    plt.colorbar(im, ax=axes[1, 1])
    
    # Plot 6: Phase space
    axes[1, 2].scatter(sigmas[::5], scars[::5], c=times[::5], cmap='coolwarm', alpha=0.6)
    axes[1, 2].set_title('Phase Space (Σ vs Scar)')
    axes[1, 2].set_xlabel('SIGMA count')
    axes[1, 2].set_ylabel('SCAR count')
    
    plt.tight_layout()
    plt.show()


# Example usage
if __name__ == "__main__":
    from ghostlink_core_spec import GhostLattice
    
    # Run validation
    validator = ProofValidator(lattice_size=24, num_trials=3)
    results = validator.run_full_validation(GhostLattice)
    
    # Generate report
    report = generate_proof_report(results)
    print(report)
    
    # Save results
    with open('proof_of_record.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📝 Results saved to proof_of_record.json")
    
    # Visualize if matplotlib available
    try:
        lattice = GhostLattice(size=24)
        visualize_proof(lattice, steps=100)
    except:
        print("Visualization skipped (matplotlib not available)")
