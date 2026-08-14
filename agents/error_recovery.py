"""Error Recovery Module - Handles failures gracefully."""
import json, os, time

STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json")
MAX_CONSECUTIVE_ERRORS = 3
ERROR_COOLDOWN_SECONDS = 60

def load_state():
    try:
        with open(STATE_FILE, "r") as f: return json.load(f)
    except: return {}

def save_state(state):
    with open(STATE_FILE, "w") as f: json.dump(state, f, indent=2, ensure_ascii=False)

def record_error(agent_name, error_msg):
    """Record an error and check if we should halt."""
    state = load_state()
    if "error_log" not in state:
        state["error_log"] = []
    state["error_log"].append({
        "agent": agent_name,
        "error": str(error_msg)[:200],
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    })
    # Keep only last 20 errors
    state["error_log"] = state["error_log"][-20:]
    
    # Count consecutive errors for this agent
    consecutive = 0
    for err in reversed(state["error_log"]):
        if err["agent"] == agent_name:
            consecutive += 1
        else:
            break
    
    if consecutive >= MAX_CONSECUTIVE_ERRORS:
        state["status"] = "halted"
        state["halt_reason"] = f"{agent_name} failed {consecutive} times consecutively"
        print(f"[RECOVERY] HALTED: {agent_name} failed {consecutive} times")
    
    save_state(state)
    return consecutive < MAX_CONSECUTIVE_ERRORS

def clear_errors():
    """Clear error log and resume."""
    state = load_state()
    state["error_log"] = []
    state["status"] = "ready"
    if "halt_reason" in state:
        del state["halt_reason"]
    save_state(state)
    print("[RECOVERY] Errors cleared, pipeline resumed")

def is_halted():
    """Check if pipeline is halted."""
    state = load_state()
    return state.get("status") == "halted"

def get_error_summary():
    """Get summary of recent errors."""
    state = load_state()
    errors = state.get("error_log", [])
    return {
        "total_errors": len(errors),
        "recent": errors[-5:] if errors else [],
        "halted": state.get("status") == "halted",
        "halt_reason": state.get("halt_reason", "")
    }