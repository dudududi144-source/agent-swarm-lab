"""Agent 4: Reviewer - Review code quality, find issues."""
import json, os, time, httpx

NVIDIA_API_KEY = os.environ.get("NVIDIA_API_KEY", "")
NVIDIA_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json")

SYSTEM_PROMPT = """You are a Senior Code Reviewer.
Review code for: bugs, security, performance, style, error handling, edge cases.
Rate quality 1-10. List all issues. Be strict and thorough.
Output JSON: quality_score, issues, suggestions, approved"""

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
            json={"model": "meta/llama-3.3-70b-instruct", "messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}], "max_tokens": max_tokens, "temperature": 0.2}, timeout=90)
        if r.status_code == 200: return {"content": r.json()["choices"][0]["message"]["content"]}
        return {"error": f"API: {r.status_code}"}
    except Exception as e: return {"error": str(e)}

def run():
    print("[REVIEWER] Starting...")
    state = load_state()
    if state.get("current_agent") != "reviewer":
        print("[REVIEWER] Not my turn."); return
    state["status"] = "running"; save_state(state)
    code = state.get("code", "")
    result = call_ai(f"Review this code thoroughly:\n\n{code[:8000]}")
    if "error" in result:
        print(f"[REVIEWER] Error: {result['error']}"); state["status"] = "error"; save_state(state); return
    state["review"] = result["content"]
    state["current_agent"] = "optimizer"
    state["status"] = "reviewer_complete"
    state["history"].append({"agent": "reviewer", "iteration": state["iteration"], "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"), "status": "complete"})
    save_state(state)
    print("[REVIEWER] Done. Passing to Optimizer.")

if __name__ == "__main__": run()