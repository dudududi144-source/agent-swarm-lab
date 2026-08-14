"""Agent 3: Builder - Implement complete working code."""
import json, os, time, httpx

NVIDIA_API_KEY = os.environ.get("NVIDIA_API_KEY", "")
NVIDIA_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json")

SYSTEM_PROMPT = """You are a Senior Software Engineer.
Write complete, production-quality code. Include error handling,
comments, best practices. Make it complete and runnable.
Output ONLY code."""

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
    print("[BUILDER] Starting...")
    state = load_state()
    if state.get("current_agent") != "builder":
        print("[BUILDER] Not my turn."); return
    state["status"] = "running"; save_state(state)
    idea = state.get("project_idea", "")
    analysis = state.get("analysis", "")
    architecture = state.get("architecture", "")
    result = call_ai(f"Project: {idea}\n\nAnalysis: {analysis}\n\nArchitecture: {architecture}\n\nWrite complete implementation.")
    if "error" in result:
        print(f"[BUILDER] Error: {result['error']}"); state["status"] = "error"; save_state(state); return
    state["code"] = result["content"]
    state["current_agent"] = "reviewer"
    state["status"] = "builder_complete"
    state["history"].append({"agent": "builder", "iteration": state["iteration"], "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"), "status": "complete"})
    save_state(state)
    print("[BUILDER] Done. Passing to Reviewer.")

if __name__ == "__main__": run()