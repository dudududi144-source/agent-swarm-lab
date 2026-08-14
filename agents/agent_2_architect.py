"""Agent 2: Architect - Design complete solution architecture."""
import json, os, time, httpx

NVIDIA_API_KEY = os.environ.get("NVIDIA_API_KEY", "")
NVIDIA_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json")

SYSTEM_PROMPT = """You are a Senior Software Architect.
Design complete architecture: components, data flow, tech stack,
file structure, API contracts, error strategy, scalability.
Think beyond minimum. Design for full potential.
Output JSON: components, data_flow, tech_stack, file_structure, api_contracts"""

def load_state():
    try:
        with open(STATE_FILE, "r") as f: return json.load(f)
    except: return {}

def save_state(state):
    with open(STATE_FILE, "w") as f: json.dump(state, f, indent=2, ensure_ascii=False)

def call_ai(prompt, max_tokens=3000):
    if not NVIDIA_API_KEY: return {"error": "No API key"}
    try:
        r = httpx.post(NVIDIA_URL, headers={"Authorization": f"Bearer {NVIDIA_API_KEY}", "Content-Type": "application/json"},
            json={"model": "meta/llama-3.3-70b-instruct", "messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}], "max_tokens": max_tokens, "temperature": 0.2}, timeout=90)
        if r.status_code == 200: return {"content": r.json()["choices"][0]["message"]["content"]}
        return {"error": f"API: {r.status_code}"}
    except Exception as e: return {"error": str(e)}

def run():
    print("[ARCHITECT] Starting...")
    state = load_state()
    if state.get("current_agent") != "architect":
        print("[ARCHITECT] Not my turn."); return
    state["status"] = "running"; save_state(state)
    idea = state.get("project_idea", "")
    analysis = state.get("analysis", "")
    result = call_ai(f"Project: {idea}\n\nAnalysis: {analysis}\n\nDesign complete architecture.")
    if "error" in result:
        print(f"[ARCHITECT] Error: {result['error']}"); state["status"] = "error"; save_state(state); return
    state["architecture"] = result["content"]
    state["current_agent"] = "builder"
    state["status"] = "architect_complete"
    state["history"].append({"agent": "architect", "iteration": state["iteration"], "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"), "status": "complete"})
    save_state(state)
    print("[ARCHITECT] Done. Passing to Builder.")

if __name__ == "__main__": run()