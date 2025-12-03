#!/usr/bin/env python3
"""
GhostLink AutoTrace & Map System
Automated tracing, mapping, and visualization of InterMesh protocol flows
"""

import json
import time
import threading
from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Tuple
from collections import defaultdict, deque
import networkx as nx
from pathlib import Path

# Core trace structures
@dataclass
class TraceEvent:
    """Single traced event in the system"""
    ts: float
    source: str
    target: str
    action: str
    args: Dict
    trace_id: str = ""
    parent_id: str = ""
    
    def __post_init__(self):
        if not self.trace_id:
            self.trace_id = f"{self.source}_{int(self.ts*1000)}"

@dataclass
class TraceSpan:
    """Execution span tracking"""
    span_id: str
    module: str
    operation: str
    start_ts: float
    end_ts: Optional[float] = None
    children: List[str] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)
    
    @property
    def duration_ms(self) -> float:
        if self.end_ts:
            return (self.end_ts - self.start_ts) * 1000
        return 0

class AutoTracer:
    """Automatic tracing of all InterMesh messages"""
    
    def __init__(self, trace_dir="./traces"):
        self.trace_dir = Path(trace_dir)
        self.trace_dir.mkdir(exist_ok=True)
        
        # Live trace buffer
        self.events: deque = deque(maxlen=10000)
        self.spans: Dict[str, TraceSpan] = {}
        self.active_spans: Set[str] = set()
        
        # Module interaction graph
        self.interaction_graph = nx.DiGraph()
        self.module_states: Dict[str, str] = {}
        
        # Metrics
        self.metrics = defaultdict(lambda: defaultdict(int))
        self.latencies = defaultdict(list)
        
        # Background trace writer
        self.running = True
        self.writer_thread = threading.Thread(target=self._trace_writer, daemon=True)
        self.writer_thread.start()
    
    def trace(self, message: Dict) -> str:
        """Trace an InterMesh message"""
        event = TraceEvent(
            ts=message.get("ts", time.time()),
            source=message.get("source", "unknown"),
            target=message.get("module", "unknown"),
            action=message.get("action", "unknown"),
            args=message.get("args", {})
        )
        
        self.events.append(event)
        self._update_graph(event)
        self._update_metrics(event)
        
        # Start/end spans based on action
        if event.action in ["spawn", "event"]:
            span_id = self._start_span(event)
            return span_id
        elif event.action in ["ack", "error"]:
            self._end_span(event)
        
        return event.trace_id
    
    def _start_span(self, event: TraceEvent) -> str:
        """Start a new trace span"""
        span = TraceSpan(
            span_id=event.trace_id,
            module=event.target,
            operation=event.action,
            start_ts=event.ts
        )
        self.spans[span.span_id] = span
        self.active_spans.add(span.span_id)
        return span.span_id
    
    def _end_span(self, event: TraceEvent):
        """End an active span"""
        # Find matching span
        for span_id in list(self.active_spans):
            span = self.spans[span_id]
            if span.module == event.source:
                span.end_ts = event.ts
                self.active_spans.discard(span_id)
                self.latencies[span.module].append(span.duration_ms)
                break
    
    def _update_graph(self, event: TraceEvent):
        """Update module interaction graph"""
        # Add nodes
        if event.source not in self.interaction_graph:
            self.interaction_graph.add_node(event.source)
        if event.target not in self.interaction_graph:
            self.interaction_graph.add_node(event.target)
        
        # Add/update edge
        if self.interaction_graph.has_edge(event.source, event.target):
            self.interaction_graph[event.source][event.target]["weight"] += 1
        else:
            self.interaction_graph.add_edge(event.source, event.target, weight=1)
        
        # Update module states
        if event.action == "spawn":
            self.module_states[event.target] = "running"
        elif event.action == "stop":
            self.module_states[event.target] = "stopped"
        elif event.action == "error":
            self.module_states[event.source] = "error"
    
    def _update_metrics(self, event: TraceEvent):
        """Update trace metrics"""
        self.metrics[event.source][event.action] += 1
        self.metrics["_total"][event.action] += 1
    
    def _trace_writer(self):
        """Background writer for trace persistence"""
        while self.running:
            time.sleep(5)
            if self.events:
                # Write recent events to file
                trace_file = self.trace_dir / f"trace_{int(time.time())}.jsonl"
                with open(trace_file, "w") as f:
                    for _ in range(min(100, len(self.events))):
                        event = self.events.popleft()
                        f.write(json.dumps({
                            "ts": event.ts,
                            "src": event.source,
                            "tgt": event.target,
                            "act": event.action,
                            "args": event.args,
                            "tid": event.trace_id
                        }) + "\n")

class SystemMapper:
    """Generate visual and structural maps of the system"""
    
    def __init__(self, tracer: AutoTracer):
        self.tracer = tracer
        self.snapshots: List[Dict] = []
    
    def generate_map(self) -> Dict:
        """Generate current system map"""
        return {
            "timestamp": time.time(),
            "modules": self._map_modules(),
            "flows": self._map_flows(),
            "dependencies": self._map_dependencies(),
            "hotspots": self._identify_hotspots(),
            "topology": self._extract_topology()
        }
    
    def _map_modules(self) -> Dict:
        """Map module states and capabilities"""
        modules = {}
        for node in self.tracer.interaction_graph.nodes():
            modules[node] = {
                "state": self.tracer.module_states.get(node, "unknown"),
                "in_degree": self.tracer.interaction_graph.in_degree(node),
                "out_degree": self.tracer.interaction_graph.out_degree(node),
                "metrics": dict(self.tracer.metrics.get(node, {})),
                "avg_latency_ms": (
                    sum(self.tracer.latencies[node]) / len(self.tracer.latencies[node])
                    if self.tracer.latencies[node] else 0
                )
            }
        return modules
    
    def _map_flows(self) -> List[Dict]:
        """Map data flows between modules"""
        flows = []
        for src, tgt, data in self.tracer.interaction_graph.edges(data=True):
            flows.append({
                "source": src,
                "target": tgt,
                "volume": data.get("weight", 0),
                "type": "intermesh"
            })
        return sorted(flows, key=lambda x: x["volume"], reverse=True)
    
    def _map_dependencies(self) -> Dict[str, List[str]]:
        """Extract module dependencies"""
        deps = {}
        for node in self.tracer.interaction_graph.nodes():
            deps[node] = list(self.tracer.interaction_graph.predecessors(node))
        return deps
    
    def _identify_hotspots(self) -> List[Tuple[str, int]]:
        """Identify high-traffic modules"""
        traffic = {}
        for node in self.tracer.interaction_graph.nodes():
            traffic[node] = (
                self.tracer.interaction_graph.in_degree(node, weight="weight") +
                self.tracer.interaction_graph.out_degree(node, weight="weight")
            )
        return sorted(traffic.items(), key=lambda x: x[1], reverse=True)[:5]
    
    def _extract_topology(self) -> str:
        """Determine system topology pattern"""
        g = self.tracer.interaction_graph
        
        if nx.is_directed_acyclic_graph(g):
            return "pipeline"
        elif len(list(nx.strongly_connected_components(g))) == 1:
            return "mesh"
        elif any(node for node in g.nodes() 
                if g.in_degree(node) > 3 and g.out_degree(node) > 3):
            return "hub-spoke"
        else:
            return "hybrid"
    
    def snapshot(self):
        """Take a snapshot of current map"""
        self.snapshots.append(self.generate_map())
        return len(self.snapshots) - 1
    
    def diff_maps(self, idx1: int, idx2: int) -> Dict:
        """Compare two map snapshots"""
        if idx1 >= len(self.snapshots) or idx2 >= len(self.snapshots):
            return {}
        
        map1, map2 = self.snapshots[idx1], self.snapshots[idx2]
        
        return {
            "modules_added": set(map2["modules"]) - set(map1["modules"]),
            "modules_removed": set(map1["modules"]) - set(map2["modules"]),
            "state_changes": {
                m: (map1["modules"][m]["state"], map2["modules"][m]["state"])
                for m in set(map1["modules"]) & set(map2["modules"])
                if map1["modules"][m]["state"] != map2["modules"][m]["state"]
            },
            "topology_change": map1["topology"] != map2["topology"],
            "flow_delta": len(map2["flows"]) - len(map1["flows"])
        }

class TraceReplay:
    """Replay traced execution for debugging"""
    
    def __init__(self, trace_dir="./traces"):
        self.trace_dir = Path(trace_dir)
        self.events: List[TraceEvent] = []
    
    def load_traces(self, start_ts: float = 0, end_ts: float = float('inf')):
        """Load traces from files"""
        self.events.clear()
        
        for trace_file in sorted(self.trace_dir.glob("trace_*.jsonl")):
            with open(trace_file) as f:
                for line in f:
                    data = json.loads(line)
                    if start_ts <= data["ts"] <= end_ts:
                        self.events.append(TraceEvent(
                            ts=data["ts"],
                            source=data["src"],
                            target=data["tgt"],
                            action=data["act"],
                            args=data.get("args", {}),
                            trace_id=data.get("tid", "")
                        ))
        
        self.events.sort(key=lambda e: e.ts)
        return len(self.events)
    
    def replay(self, speed: float = 1.0, callback=None):
        """Replay trace events"""
        if not self.events:
            return
        
        base_ts = self.events[0].ts
        start_time = time.time()
        
        for event in self.events:
            # Calculate when this event should fire
            event_offset = (event.ts - base_ts) / speed
            current_offset = time.time() - start_time
            
            if event_offset > current_offset:
                time.sleep(event_offset - current_offset)
            
            if callback:
                callback(event)
            else:
                print(f"[{event.source}→{event.target}] {event.action}")
    
    def find_anomalies(self) -> List[Dict]:
        """Detect anomalies in trace patterns"""
        anomalies = []
        
        # Check for missing ACKs
        spawns = {}
        for event in self.events:
            if event.action == "spawn":
                spawns[event.target] = event.ts
            elif event.action == "ack":
                spawns.pop(event.source, None)
        
        for module, ts in spawns.items():
            anomalies.append({
                "type": "missing_ack",
                "module": module,
                "timestamp": ts
            })
        
        # Check for rapid errors
        error_times = defaultdict(list)
        for event in self.events:
            if event.action == "error":
                error_times[event.source].append(event.ts)
        
        for module, times in error_times.items():
            if len(times) > 3:
                # Check if errors are clustered
                for i in range(len(times) - 3):
                    if times[i+3] - times[i] < 60:  # 4 errors in 60s
                        anomalies.append({
                            "type": "error_storm",
                            "module": module,
                            "count": 4,
                            "window_start": times[i],
                            "window_end": times[i+3]
                        })
                        break
        
        return anomalies

# Integration with GhostLink Manager
class TracedManager:
    """Enhanced manager with automatic tracing"""
    
    def __init__(self):
        self.tracer = AutoTracer()
        self.mapper = SystemMapper(self.tracer)
        self.replay = TraceReplay()
    
    def handle_message(self, msg: Dict):
        """Process message with automatic tracing"""
        # Trace the message
        trace_id = self.tracer.trace(msg)
        msg["_trace_id"] = trace_id
        
        # Regular processing...
        # (existing manager logic here)
        
        # Periodic mapping
        if msg["action"] in ["spawn", "stop", "error"]:
            self.mapper.snapshot()
    
    def get_system_map(self) -> Dict:
        """Get current system map"""
        return self.mapper.generate_map()
    
    def analyze_traces(self) -> Dict:
        """Analyze recent traces"""
        self.replay.load_traces(time.time() - 3600)  # Last hour
        
        return {
            "event_count": len(self.replay.events),
            "anomalies": self.replay.find_anomalies(),
            "hotspots": self.mapper._identify_hotspots(),
            "topology": self.mapper._extract_topology(),
            "metrics": dict(self.tracer.metrics["_total"])
        }

if __name__ == "__main__":
    # Demo trace & map
    manager = TracedManager()
    
    # Simulate some events
    test_events = [
        {"action": "spawn", "module": "ColdStack", "source": "Manager", "ts": time.time()},
        {"action": "ack", "module": "Manager", "source": "ColdStack", "ts": time.time() + 0.1},
        {"action": "spawn", "module": "HardwareDaemon", "source": "ColdStack", "ts": time.time() + 0.2},
        {"action": "heartbeat", "module": "ColdStack", "source": "ColdStack", "ts": time.time() + 1},
        {"action": "event", "module": "DriftGuard", "source": "ColdStack", "args": {"type": "drift_detected"}},
    ]
    
    for event in test_events:
        manager.handle_message(event)
        time.sleep(0.1)
    
    # Generate report
    print(json.dumps(manager.get_system_map(), indent=2))
    print("\nAnalysis:", json.dumps(manager.analyze_traces(), indent=2))