"""Orchestrator: Runs agents in sequence, infinite loop."""
import json, os, sys, time, subprocess

AGENTS_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(AGENTS_DIR, "state.json")

AGENT_SEQUENCE = [
    ("analyst", "agent_1_analyst.py"),
    ("architect", "agent_2_architect.py"),
    ("builder", "agent_3_builder.py"),
    ("reviewer", "agent_4_reviewer.py"),
    ("optimizer", "agent_5_optimizer.py"),
    ("deployer", "agent_6_deployer.py"),
]

CONFIG = {
    "delay_between_agents": 3,
    "delay_between_iterations": 10,
    "max_iterations": 100,
    "max_retries": 2,
    "timeout_per_agent": 180,
}

def load_state():
    try:
        with open(STATE_FILE, "r") as f: return json.load(f)
    except: return {"current_agent": "analyst", "iteration": 0, "status": "idle", "history": []}

def save_state(state):
    with open(STATE_FILE, "w") as f: json.dump(state, f, indent=2, ensure_ascii=False)

def run_agent(agent_name, script_name, retries=0):
    script_path = os.path.join(AGENTS_DIR, script_name)
    print(f"  Running {agent_name}...")
    try:
        result = subprocess.run([sys.executable, script_path], capture_output=True, text=True, timeout=CONFIG["timeout_per_agent"], env={**os.environ})
        if result.returncode == 0:
            print(f"  {agent_name} completed")
            return True
        else:
            print(f"  {agent_name} failed: {result.stderr[:200]}")
            if retries < CONFIG["max_retries"]:
                time.sleep(2)
                return run_agent(agent_name, script_name, retries + 1)
            return False
    except subprocess.TimeoutExpired:
        print(f"  {agent_name} timed out")
        return False
    except Exception as e:
        print(f"  {agent_name} error: {e}")
        return False

def run_pipeline():
    state = load_state()
    iteration = state.get("iteration", 0)
    print(f"\n  ITERATION {iteration + 1}")
    print("  " + "="*40)
    for agent_name, script_name in AGENT_SEQUENCE:
        state = load_state()
        if state.get("current_agent") != agent_name:
            continue
        success = run_agent(agent_name, script_name)
        if not success:
            print(f"  Pipeline halted at {agent_name}")
            state = load_state()
            state["status"] = "error"
            save_state(state)
            return False
        time.sleep(CONFIG["delay_between_agents"])
    print(f"\n  Iteration {iteration + 1} complete!")
    return True

def run_infinite_loop():
    print("\n  AGENT SWARM - INFINITE IMPROVEMENT LOOP")
    print("  " + "="*40)
    state = load_state()
    max_iterations = CONFIG["max_iterations"]
    while state.get("iteration", 0) < max_iterations:
        success = run_pipeline()
        if not success:
            print("  Pipeline error. Waiting 30s...")
            time.sleep(30)
            continue
        state = load_state()
        delay = CONFIG["delay_between_iterations"]
        print(f"  Waiting {delay}s before next iteration...")
        time.sleep(delay)
    print("\n  Max iterations reached.")

def set_project_idea(idea):
    state = load_state()
    state["project_idea"] = idea
    state["current_agent"] = "analyst"
    state["status"] = "ready"
    state["iteration"] = 0
    save_state(state)
    print(f"Project idea set: {idea[:100]}...")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        idea = " ".join(sys.argv[1:])
        set_project_idea(idea)
    run_infinite_loop()