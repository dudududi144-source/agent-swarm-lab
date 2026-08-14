"""Monitoring Module - Tracks pipeline health and performance."""
import json, os, time

STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json")
METRICS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "metrics.json")

def load_state():
    try:
        with open(STATE_FILE, "r") as f: return json.load(f)
    except: return {}

def load_metrics():
    try:
        with open(METRICS_FILE, "r") as f: return json.load(f)
    except: return {"iterations": 0, "total_time": 0, "agent_times": {}, "errors": 0, "quality_passes": 0, "quality_fails": 0}

def save_metrics(metrics):
    with open(METRICS_FILE, "w") as f: json.dump(metrics, f, indent=2)

def record_agent_time(agent_name, seconds):
    """Record how long an agent took."""
    metrics = load_metrics()
    if agent_name not in metrics["agent_times"]:
        metrics["agent_times"][agent_name] = []
    metrics["agent_times"][agent_name].append(seconds)
    metrics["total_time"] += seconds
    save_metrics(metrics)

def record_iteration():
    """Record a completed iteration."""
    metrics = load_metrics()
    metrics["iterations"] += 1
    save_metrics(metrics)

def record_error():
    """Record an error."""
    metrics = load_metrics()
    metrics["errors"] += 1
    save_metrics(metrics)

def record_quality(passed):
    """Record quality gate result."""
    metrics = load_metrics()
    if passed:
        metrics["quality_passes"] += 1
    else:
        metrics["quality_fails"] += 1
    save_metrics(metrics)

def get_health_report():
    """Generate a health report."""
    state = load_state()
    metrics = load_metrics()
    
    avg_times = {}
    for agent, times in metrics.get("agent_times", {}).items():
        if times:
            avg_times[agent] = sum(times) / len(times)
    
    total_quality = metrics.get("quality_passes", 0) + metrics.get("quality_fails", 0)
    quality_rate = (metrics.get("quality_passes", 0) / total_quality * 100) if total_quality > 0 else 100
    
    return {
        "status": state.get("status", "unknown"),
        "current_agent": state.get("current_agent", "none"),
        "iteration": state.get("iteration", 0),
        "total_iterations": metrics.get("iterations", 0),
        "total_errors": metrics.get("errors", 0),
        "quality_rate": round(quality_rate, 1),
        "avg_agent_times": avg_times,
        "total_runtime_seconds": metrics.get("total_time", 0)
    }