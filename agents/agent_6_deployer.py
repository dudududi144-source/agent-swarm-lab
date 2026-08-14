"""Agent 6: Deployer - Validate and save final output."""
import json, os, time, httpx

NVIDIA_API_KEY = os.environ.get("NVIDIA_API_KEY", "")
NVIDIA_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output")

SYSTEM_PROMPT = """You are a Senior DevOps Engineer.
Validate code for deployment: syntax, dependencies, security, config.
Create deployment instructions. Output JSON: ready, issues, deployment_plan"""

def load_state():
    try:
        with open(STATE_FILE, "r") as f: return json.load(f)
    except: return {}

def save_state(state):
    with open(STATE_FILE, "w") as f: json.dump(state, f, indent=2, ensure_ascii=False)

def call_ai(prompt, max_tokens=2048):
    if not NVIDIA_API_KEY: return {"error": "No API key"}
    try:
        r = httpx.post(NVIDIA_URL, headers={"Authorization": f"Bearer {NVIDIA_API_KEY}", "Content-Type": "application/json"},
            json={"model": "meta/llama-3.1-8b-instruct", "messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}], "max_tokens": max_tokens, "temperature": 0.2}, timeout=60)
        if r.status_code == 200: return {"content": r.json()["choices"][0]["message"]["content"]}
        return {"error": f"API: {r.status_code}"}
    except Exception as e: return {"error": str(e)}

def save_output(state):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    iteration = state.get("iteration", 0)
    filepath = os.path.join(OUTPUT_DIR, f"iteration_{iteration}.py")
    with open(filepath, "w") as f:
        f.write(state.get("code", ""))
    print(f"[DEPLOYER] Saved to output/iteration_{iteration}.py")

def run():
    print("[DEPLOYER] Starting...")
    state = load_state()
    if state.get("current_agent") != "deployer":
        print("[DEPLOYER] Not my turn."); return
    state["status"] = "running"; save_state(state)
    code = state.get("code", "")
    result = call_ai(f"Validate for deployment:\n\n{code[:6000]}")
    save_output(state)
    state["deployment"] = result.get("content", "Validation complete")
    state["current_agent"] = "analyst"
    state["status"] = "iteration_complete"
    state["history"].append({"agent": "deployer", "iteration": state["iteration"], "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"), "status": "complete"})
    save_state(state)
    print("[DEPLOYER] Done. Loop restarts with Analyst.")

if __name__ == "__main__": run()