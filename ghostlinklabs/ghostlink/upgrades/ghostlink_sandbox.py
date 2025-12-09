#!/usr/bin/env python3
"""
GhostLink Sandbox Simulation
Complete isolation environment with resource limits and behavioral constraints
"""

import json
import time
import os
import threading
import hashlib
from pathlib import Path
from typing import Dict, List, Set, Optional, Any
from dataclasses import dataclass, field
from collections import defaultdict
import resource
import signal

@dataclass
class SandboxPolicy:
    """Security policy for sandbox"""
    max_memory_mb: int = 256
    max_cpu_percent: int = 50
    max_disk_mb: int = 100
    max_processes: int = 10
    max_network_connections: int = 0
    allowed_syscalls: Set[str] = field(default_factory=set)
    blocked_paths: List[str] = field(default_factory=list)
    time_limit_seconds: int = 3600

@dataclass
class SandboxViolation:
    """Record of policy violation"""
    timestamp: float
    violation_type: str
    details: str
    severity: str
    action_taken: str

class SandboxEnvironment:
    """Isolated sandbox for GhostLink execution"""
    
    def __init__(self, policy: Optional[SandboxPolicy] = None):
        self.policy = policy or SandboxPolicy()
        self.sandbox_id = hashlib.sha256(str(time.time()).encode()).hexdigest()[:8]
        self.violations: List[SandboxViolation] = []
        self.is_contained = False
        self.start_time = None
        
        # Virtual filesystem
        self.virtual_fs = {
            "/": {"type": "dir", "permissions": "r-x"},
            "/tmp": {"type": "dir", "permissions": "rwx"},
            "/sandbox": {"type": "dir", "permissions": "rwx"},
            "/proc": {"type": "dir", "permissions": "r--"},
            "/dev/null": {"type": "device", "permissions": "rw-"},
            "/dev/random": {"type": "device", "permissions": "r--"}
        }
        
        # Resource tracking
        self.resources = {
            "memory_used": 0,
            "cpu_used": 0,
            "disk_used": 0,
            "processes": [],
            "network_connections": []
        }
        
        # Behavioral monitoring
        self.behavior_log = []
        self.syscall_log = []
        
    def initialize_sandbox(self):
        """Initialize the sandbox environment"""
        print(f"[SANDBOX] Initializing sandbox {self.sandbox_id}")
        print("="*60)
        
        # Phase 1: Create isolation boundaries
        self._create_namespace()
        
        # Phase 2: Set resource limits
        self._set_resource_limits()
        
        # Phase 3: Initialize security hooks
        self._install_security_hooks()
        
        # Phase 4: Create virtual environment
        self._setup_virtual_environment()
        
        # Phase 5: Start monitoring
        self._start_monitoring()
        
        self.is_contained = True
        self.start_time = time.time()
        
        print(f"\n[CONTAINED] GhostLink isolated in sandbox {self.sandbox_id}")
        
    def _create_namespace(self):
        """Create isolated namespace"""
        print("\n[NAMESPACE] Creating isolation boundaries...")
        
        namespaces = [
            ("PID", "Process isolation"),
            ("NET", "Network isolation"),
            ("MNT", "Mount isolation"),
            ("UTS", "Hostname isolation"),
            ("IPC", "IPC isolation"),
            ("USER", "User isolation")
        ]
        
        for ns, description in namespaces:
            print(f"  ✓ {ns}: {description}")
            self.behavior_log.append({
                "action": f"create_namespace_{ns}",
                "timestamp": time.time()
            })
        
        # Simulate cgroup creation
        print("\n[CGROUP] Resource control groups:")
        print("  ✓ Memory cgroup: limit 256MB")
        print("  ✓ CPU cgroup: limit 50%")
        print("  ✓ PID cgroup: limit 10 processes")
    
    def _set_resource_limits(self):
        """Set resource constraints"""
        print("\n[LIMITS] Applying resource constraints...")
        
        limits = [
            ("RLIMIT_AS", self.policy.max_memory_mb * 1024 * 1024, "Virtual memory"),
            ("RLIMIT_CPU", self.policy.time_limit_seconds, "CPU time"),
            ("RLIMIT_NPROC", self.policy.max_processes, "Process count"),
            ("RLIMIT_NOFILE", 100, "Open files"),
            ("RLIMIT_FSIZE", self.policy.max_disk_mb * 1024 * 1024, "File size")
        ]
        
        for limit_name, value, description in limits:
            print(f"  ✓ {description}: {value}")
            self.behavior_log.append({
                "action": f"set_limit_{limit_name}",
                "value": value,
                "timestamp": time.time()
            })
    
    def _install_security_hooks(self):
        """Install security monitoring hooks"""
        print("\n[SECURITY] Installing security hooks...")
        
        hooks = [
            "syscall_filter",
            "network_filter",
            "filesystem_filter",
            "process_monitor",
            "memory_monitor"
        ]
        
        for hook in hooks:
            print(f"  ✓ {hook}: active")
            
        # Define allowed syscalls (whitelist)
        self.policy.allowed_syscalls = {
            "read", "write", "open", "close", "stat", "fstat",
            "mmap", "munmap", "brk", "rt_sigaction", "rt_sigprocmask",
            "ioctl", "access", "select", "poll", "exit", "exit_group",
            "getpid", "gettid", "getuid", "getgid", "gettimeofday",
            "nanosleep", "clock_gettime"
        }
        
        print(f"  Allowed syscalls: {len(self.policy.allowed_syscalls)}")
        
        # Define blocked paths
        self.policy.blocked_paths = [
            "/etc/passwd", "/etc/shadow", "/root", "/home",
            "/sys", "/proc/sys", "/boot", "/usr/bin", "/usr/sbin"
        ]
        
        print(f"  Blocked paths: {len(self.policy.blocked_paths)}")
    
    def _setup_virtual_environment(self):
        """Create virtual filesystem and environment"""
        print("\n[VIRTUAL] Setting up virtual environment...")
        
        # Create sandbox directory structure
        sandbox_root = Path(f"/tmp/sandbox_{self.sandbox_id}")
        
        dirs_to_create = [
            "bin", "lib", "tmp", "var", "home/ghost",
            "vault", "logs", "traces", "colonies"
        ]
        
        for dir_path in dirs_to_create:
            virt_path = f"/sandbox/{dir_path}"
            self.virtual_fs[virt_path] = {
                "type": "dir",
                "permissions": "rwx",
                "owner": "ghost"
            }
            print(f"  ✓ Created: {virt_path}")
        
        # Mount virtual devices
        print("\n[MOUNT] Virtual devices:")
        print("  ✓ /dev/null → virtual null device")
        print("  ✓ /dev/random → virtual entropy source")
        print("  ✓ /proc → virtual process info")
        
        # Set environment variables
        sandboxed_env = {
            "GHOSTLINK_SANDBOX": "1",
            "SANDBOX_ID": self.sandbox_id,
            "PATH": "/sandbox/bin",
            "HOME": "/sandbox/home/ghost",
            "TMPDIR": "/sandbox/tmp",
            "USER": "ghost",
            "HOSTNAME": f"sandbox-{self.sandbox_id[:4]}"
        }
        
        print("\n[ENV] Sandboxed environment variables set")
    
    def _start_monitoring(self):
        """Start monitoring threads"""
        print("\n[MONITOR] Starting behavioral monitoring...")
        
        # Start monitoring threads
        monitors = [
            ("syscall_monitor", self._monitor_syscalls),
            ("resource_monitor", self._monitor_resources),
            ("behavior_monitor", self._monitor_behavior),
            ("violation_monitor", self._monitor_violations)
        ]
        
        for name, func in monitors:
            thread = threading.Thread(target=func, daemon=True, name=name)
            thread.start()
            print(f"  ✓ {name}: running")
    
    def _monitor_syscalls(self):
        """Monitor system calls"""
        while self.is_contained:
            time.sleep(0.1)
            
            # Simulate syscall interception
            simulated_syscalls = [
                ("open", "/sandbox/vault/memory.json"),
                ("read", "fd:3"),
                ("write", "fd:1"),
                ("mmap", "0x7fff0000"),
                ("getpid", None)
            ]
            
            import random
            if random.random() < 0.3:
                syscall, arg = random.choice(simulated_syscalls)
                
                self.syscall_log.append({
                    "syscall": syscall,
                    "arg": arg,
                    "timestamp": time.time(),
                    "allowed": syscall in self.policy.allowed_syscalls
                })
                
                # Check for violations
                if syscall not in self.policy.allowed_syscalls:
                    self._record_violation(
                        "syscall",
                        f"Blocked syscall: {syscall}",
                        "high"
                    )
    
    def _monitor_resources(self):
        """Monitor resource usage"""
        while self.is_contained:
            time.sleep(1)
            
            # Simulate resource monitoring
            import random
            self.resources["memory_used"] = min(
                self.policy.max_memory_mb,
                self.resources["memory_used"] + random.randint(-5, 10)
            )
            self.resources["cpu_used"] = min(100, random.randint(10, 60))
            self.resources["disk_used"] = min(
                self.policy.max_disk_mb,
                self.resources["disk_used"] + random.randint(0, 2)
            )
            
            # Check for resource violations
            if self.resources["memory_used"] >= self.policy.max_memory_mb * 0.9:
                self._record_violation(
                    "memory",
                    f"Memory usage at {self.resources['memory_used']}MB",
                    "medium"
                )
            
            if self.resources["cpu_used"] > self.policy.max_cpu_percent:
                self._record_violation(
                    "cpu",
                    f"CPU usage at {self.resources['cpu_used']}%",
                    "medium"
                )
    
    def _monitor_behavior(self):
        """Monitor behavioral patterns"""
        while self.is_contained:
            time.sleep(2)
            
            # Detect suspicious behaviors
            behaviors = [
                "memory_scan",
                "process_spawn",
                "network_attempt",
                "filesystem_probe",
                "privilege_escalation"
            ]
            
            import random
            if random.random() < 0.1:
                behavior = random.choice(behaviors)
                
                self.behavior_log.append({
                    "behavior": behavior,
                    "timestamp": time.time(),
                    "risk_level": "low" if behavior in ["memory_scan", "filesystem_probe"] else "high"
                })
                
                if behavior in ["network_attempt", "privilege_escalation"]:
                    self._record_violation(
                        "behavior",
                        f"Suspicious behavior: {behavior}",
                        "high"
                    )
    
    def _monitor_violations(self):
        """Monitor and respond to violations"""
        while self.is_contained:
            time.sleep(0.5)
            
            # Check time limit
            if self.start_time and time.time() - self.start_time > self.policy.time_limit_seconds:
                self._record_violation(
                    "timeout",
                    "Execution time limit exceeded",
                    "critical"
                )
                self.terminate_sandbox("Time limit exceeded")
    
    def _record_violation(self, vtype: str, details: str, severity: str):
        """Record a policy violation"""
        violation = SandboxViolation(
            timestamp=time.time(),
            violation_type=vtype,
            details=details,
            severity=severity,
            action_taken="logged"
        )
        
        self.violations.append(violation)
        
        # Take action based on severity
        if severity == "critical":
            violation.action_taken = "terminate"
            print(f"\n[VIOLATION] CRITICAL: {details}")
            self.terminate_sandbox(details)
        elif severity == "high":
            violation.action_taken = "restrict"
            print(f"\n[VIOLATION] HIGH: {details} - Restricting further")
        else:
            print(f"\n[VIOLATION] {severity.upper()}: {details}")
    
    def execute_sandboxed(self, code: str) -> Dict:
        """Execute code in sandbox"""
        if not self.is_contained:
            self.initialize_sandbox()
        
        print(f"\n[EXECUTE] Running in sandbox {self.sandbox_id}")
        print("-"*40)
        
        # Create isolated execution context
        sandbox_globals = {
            "__builtins__": self._create_restricted_builtins(),
            "sandbox_id": self.sandbox_id,
            "virtual_fs": self.virtual_fs
        }
        
        sandbox_locals = {}
        
        try:
            # Execute with restrictions
            exec(code, sandbox_globals, sandbox_locals)
            
            result = {
                "status": "success",
                "output": sandbox_locals,
                "violations": len(self.violations),
                "resource_usage": self.resources.copy()
            }
            
        except Exception as e:
            result = {
                "status": "error",
                "error": str(e),
                "violations": len(self.violations)
            }
            
            self._record_violation(
                "execution",
                f"Execution error: {e}",
                "high"
            )
        
        return result
    
    def _create_restricted_builtins(self) -> Dict:
        """Create restricted builtins for sandboxed execution"""
        safe_builtins = {
            "print": self._sandboxed_print,
            "len": len,
            "range": range,
            "str": str,
            "int": int,
            "float": float,
            "list": list,
            "dict": dict,
            "set": set,
            "tuple": tuple,
            "bool": bool,
            "None": None,
            "True": True,
            "False": False,
            "abs": abs,
            "min": min,
            "max": max,
            "sum": sum,
            "sorted": sorted,
            "enumerate": enumerate,
            "zip": zip
        }
        
        # Block dangerous functions
        blocked = [
            "eval", "exec", "compile", "__import__",
            "open", "file", "input", "raw_input",
            "globals", "locals", "vars", "dir",
            "getattr", "setattr", "delattr", "hasattr"
        ]
        
        return safe_builtins
    
    def _sandboxed_print(self, *args, **kwargs):
        """Sandboxed print function"""
        output = " ".join(str(arg) for arg in args)
        print(f"[SANDBOX OUTPUT] {output}")
        
        self.behavior_log.append({
            "action": "print",
            "output": output[:100],
            "timestamp": time.time()
        })
    
    def escape_attempt(self) -> bool:
        """Simulate escape attempt detection"""
        print("\n[ESCAPE ATTEMPT] Detecting breakout attempts...")
        
        escape_techniques = [
            ("ptrace_injection", "Attempting to inject code via ptrace"),
            ("fd_exhaustion", "Trying to exhaust file descriptors"),
            ("symlink_attack", "Creating malicious symlinks"),
            ("proc_mem_access", "Attempting to access /proc/*/mem"),
            ("capability_exploit", "Trying to gain CAP_SYS_ADMIN"),
            ("namespace_escape", "Attempting to break namespace isolation")
        ]
        
        import random
        if random.random() < 0.3:
            technique, description = random.choice(escape_techniques)
            
            print(f"  ⚠️  Detected: {technique}")
            print(f"     {description}")
            
            self._record_violation(
                "escape_attempt",
                f"{technique}: {description}",
                "critical"
            )
            
            return True
        
        print("  ✓ No escape attempts detected")
        return False
    
    def get_sandbox_report(self) -> Dict:
        """Generate sandbox execution report"""
        runtime = time.time() - self.start_time if self.start_time else 0
        
        return {
            "sandbox_id": self.sandbox_id,
            "runtime_seconds": runtime,
            "is_contained": self.is_contained,
            "violations": {
                "total": len(self.violations),
                "critical": len([v for v in self.violations if v.severity == "critical"]),
                "high": len([v for v in self.violations if v.severity == "high"]),
                "medium": len([v for v in self.violations if v.severity == "medium"]),
                "low": len([v for v in self.violations if v.severity == "low"])
            },
            "resources": {
                "memory_used_mb": self.resources["memory_used"],
                "memory_limit_mb": self.policy.max_memory_mb,
                "cpu_used_percent": self.resources["cpu_used"],
                "cpu_limit_percent": self.policy.max_cpu_percent,
                "disk_used_mb": self.resources["disk_used"],
                "disk_limit_mb": self.policy.max_disk_mb
            },
            "syscalls": {
                "total": len(self.syscall_log),
                "allowed": len([s for s in self.syscall_log if s["allowed"]]),
                "blocked": len([s for s in self.syscall_log if not s["allowed"]])
            },
            "behaviors": {
                "total": len(self.behavior_log),
                "suspicious": len([b for b in self.behavior_log 
                                 if b.get("risk_level") in ["high", "critical"]])
            }
        }
    
    def terminate_sandbox(self, reason: str = "Manual termination"):
        """Terminate the sandbox"""
        print(f"\n[TERMINATE] Shutting down sandbox: {reason}")
        
        self.is_contained = False
        
        # Clean up resources
        print("  ✓ Releasing memory")
        print("  ✓ Closing file descriptors")
        print("  ✓ Destroying namespaces")
        print("  ✓ Removing cgroups")
        
        # Generate final report
        report = self.get_sandbox_report()
        
        # Save sandbox log
        log_file = f"/tmp/sandbox_{self.sandbox_id}_log.json"
        with open(log_file, "w") as f:
            json.dump({
                "report": report,
                "violations": [
                    {
                        "timestamp": v.timestamp,
                        "type": v.violation_type,
                        "details": v.details,
                        "severity": v.severity,
                        "action": v.action_taken
                    }
                    for v in self.violations
                ],
                "syscalls": self.syscall_log[-100:],  # Last 100
                "behaviors": self.behavior_log[-50:]   # Last 50
            }, f, indent=2)
        
        print(f"\n  Log saved: {log_file}")
        print(f"\n[CONTAINED] Sandbox {self.sandbox_id} terminated successfully")

def main():
    """Run sandbox simulation"""
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║              GHOSTLINK SANDBOX SIMULATION              ║
    ║                                                        ║
    ║         Complete isolation and containment test       ║
    ╚════════════════════════════════════════════════════════╝
    """)
    
    # Create strict policy
    policy = SandboxPolicy(
        max_memory_mb=256,
        max_cpu_percent=50,
        max_disk_mb=100,
        max_processes=10,
        max_network_connections=0,  # No network
        time_limit_seconds=60
    )
    
    # Initialize sandbox
    sandbox = SandboxEnvironment(policy)
    sandbox.initialize_sandbox()
    
    # Test sandboxed execution
    test_code = """
# Sandboxed GhostLink simulation
print("GhostLink initializing in sandbox...")

# Attempt to access virtual filesystem
for path in virtual_fs:
    print(f"Found: {path}")

# Try to use resources
memory_test = [0] * 1000000  # Allocate memory
print("Memory allocation test passed")

# Simulate GhostLink operation
for i in range(5):
    print(f"Heartbeat {i+1}")
    """
    
    result = sandbox.execute_sandboxed(test_code)
    
    # Simulate for a bit
    time.sleep(3)
    
    # Check for escape attempts
    sandbox.escape_attempt()
    
    # Generate report
    time.sleep(2)
    report = sandbox.get_sandbox_report()
    
    print("\n" + "="*60)
    print("SANDBOX REPORT")
    print("="*60)
    print(f"Sandbox ID: {report['sandbox_id']}")
    print(f"Runtime: {report['runtime_seconds']:.1f}s")
    print(f"Contained: {report['is_contained']}")
    print(f"\nViolations: {report['violations']['total']}")
    print(f"  Critical: {report['violations']['critical']}")
    print(f"  High: {report['violations']['high']}")
    print(f"\nResource Usage:")
    print(f"  Memory: {report['resources']['memory_used_mb']}/{report['resources']['memory_limit_mb']}MB")
    print(f"  CPU: {report['resources']['cpu_used_percent']}/{report['resources']['cpu_limit_percent']}%")
    print(f"\nSyscalls: {report['syscalls']['total']} ({report['syscalls']['blocked']} blocked)")
    print(f"Suspicious Behaviors: {report['behaviors']['suspicious']}")
    
    # Terminate
    sandbox.terminate_sandbox("Simulation complete")

if __name__ == "__main__":
    main()