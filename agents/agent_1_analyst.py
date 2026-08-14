"""Agent 1: Analyst - Analyze idea, find broken parts, identify potential."""
import json, os, time, httpx

NVIDIA_API_KEY = os.environ.get("NVIDIA_API_KEY", "")
NVIDIA_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json")

SYSTEM_PROMPT = """You are a Senior Technical Analyst.
Analyze the project idea and identify:
1. What is broken or incomplete
2. What is the core purpose
3. What is the full potential
4. What are the critical gaps
5. Priority order for fixes
Be thorough, engineering-focused, honest.
Output JSON: broken_parts, core_purpose, full_potential, critical_gaps, priority_order"""

def load_state():
    try:
        with open(STATE_FILE, "r") as f: return json.load(f)
    except: return {"current_agent": "analyst", "iteration": 0, "status": "idle", "history": []}

def save_state(state):
    with open(STATE_FILE, "w") as f: json.dump(state, f, indent=2, ensure_ascii=False)

def call_ai(prompt, max_tokens=2048):
    if not NVIDIA_API_KEY: return {"error": "No API key"}
    try:
        r = httpx.post(NVIDIA_URL, headers={"Authorization": f"Bearer {NVIDIA_API_KEY}", "Content-Type": "application/json"},
            json={"model": "meta/llama-3.1-8b-instruct", "messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}], "max_tokens": max_tokens, "temperature": 0.3}, timeout=60)
        if r.status_code == 200: return {"content": r.json()["choices"][0]["message"]["content"]}
        return {"error": f"API: {r.status_code}"}
    except Exception as e: return {"error": str(e)}

def run():
    print("[ANALYST] Starting...")
    state = load_state()
    if state.get("current_agent") != "analyst":
        print("[ANALYST] Not my turn."); return
    state["status"] = "running"; state["iteration"] += 1; save_state(state)
    idea = state.get("project_idea", "")
    if not idea:
        print("[ANALYST] No idea set."); state["status"] = "error"; save_state(state); return
    result = call_ai(f"Analyze this project thoroughly:\n\n{idea}\n\nProvide structured JSON analysis.")
    if "error" in result:
        print(f"[ANALYST] Error: {result['error']}"); state["status"] = "error"; save_state(state); return
    state["analysis"] = result["content"]
    state["current_agent"] = "architect"
    state["status"] = "analyst_complete"
    state["history"].append({"agent": "analyst", "iteration": state["iteration"], "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"), "status": "complete"})
    save_state(state)
    print("[ANALYST] Done. Passing to Architect.")

if __name__ == "__main__": run()