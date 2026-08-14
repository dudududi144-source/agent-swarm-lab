"""Agent 5: Optimizer - Enhance code beyond requirements."""
import json, os, time, httpx

NVIDIA_API_KEY = os.environ.get("NVIDIA_API_KEY", "")
NVIDIA_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json")

SYSTEM_PROMPT = """You are a Principal Engineer.
Take code + review feedback, then:
1. Fix ALL identified issues
2. Optimize performance
3. Add features that make it exceptional
4. Improve BEYOND original requirements
5. Add comprehensive error handling
6. Think: what would make this world-class?
Output the complete improved code."""

def load_state():
    try:
        with open(STATE_FILE, "r") as f: return json.load(f)
    except: return {}

def save_state(state):
    with open(STATE_FILE, "w") as f: json.dump(state, f, indent=2, ensure_ascii=False)

def call_ai(prompt, max_tokens=4096):
    if not NVIDIA_API_KEY: return {"error": "No API key"}
    try:
        r = httpx.post(NVIDIA_URL, headers={"Authorization": f"Bearer {NVIDIA_API_KEY}", "Content-Type": "application/json"},
            json={"model": "deepseek-ai/deepseek-coder-6.7b-instruct", "messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}], "max_tokens": max_tokens, "temperature": 0.1}, timeout=120)
        if r.status_code == 200: return {"content": r.json()["choices"][0]["message"]["content"]}
        return {"error": f"API: {r.status_code}"}
    except Exception as e: return {"error": str(e)}

def run():
    print("[OPTIMIZER] Starting...")
    state = load_state()
    if state.get("current_agent") != "optimizer":
        print("[OPTIMIZER] Not my turn."); return
    state["status"] = "running"; save_state(state)
    code = state.get("code", "")
    review = state.get("review", "")
    result = call_ai(f"Code:\n{code[:6000]}\n\nReview feedback:\n{review[:2000]}\n\nOptimize and enhance beyond requirements.")
    if "error" in result:
        print(f"[OPTIMIZER] Error: {result['error']}"); state["status"] = "error"; save_state(state); return
    state["optimizations"] = result["content"]
    state["code"] = result["content"]
    state["current_agent"] = "deployer"
    state["status"] = "optimizer_complete"
    state["history"].append({"agent": "optimizer", "iteration": state["iteration"], "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"), "status": "complete"})
    save_state(state)
    print("[OPTIMIZER] Done. Passing to Deployer.")

if __name__ == "__main__": run()