"""Notification Module - Sends alerts on important events."""
import json, os, time

STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json")
NOTIFY_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "notifications.log")

def load_state():
    try:
        with open(STATE_FILE, "r") as f: return json.load(f)
    except: return {}

def log_notification(event_type, message):
    """Log a notification event."""
    entry = {
        "type": event_type,
        "message": message,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    try:
        with open(NOTIFY_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except:
        pass
    print(f"[NOTIFY] {event_type}: {message}")

def notify_agent_complete(agent_name, iteration):
    """Notify when an agent completes."""
    log_notification("agent_complete", f"{agent_name} completed iteration {iteration}")

def notify_iteration_complete(iteration):
    """Notify when a full iteration completes."""
    log_notification("iteration_complete", f"Iteration {iteration} complete")

def notify_error(agent_name, error):
    """Notify on error."""
    log_notification("error", f"{agent_name}: {error}")

def notify_halted(reason):
    """Notify when pipeline is halted."""
    log_notification("halted", f"Pipeline halted: {reason}")

def notify_quality_issue(agent_name, issue):
    """Notify on quality gate failure."""
    log_notification("quality_issue", f"{agent_name}: {issue}")

def get_recent_notifications(count=10):
    """Get recent notifications."""
    try:
        with open(NOTIFY_LOG, "r") as f:
            lines = f.readlines()
        return [json.loads(line) for line in lines[-count:]]
    except:
        return []