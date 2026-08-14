#!/usr/bin/env python3
"""PSY4NEW Agent Swarm - Entry Point"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "agents"))
from orchestrator import run_infinite_loop, set_project_idea, load_state, save_state

def show_status():
    state = load_state()
    print("\n  PIPELINE STATUS")
    print("  " + "="*40)
    print(f"  Iteration: {state.get('iteration', 0)}")
    print(f"  Current Agent: {state.get('current_agent', 'none')}")
    print(f"  Status: {state.get('status', 'idle')}")
    print(f"  History: {len(state.get('history', []))} entries")
    idea = state.get("project_idea", "")
    if idea: print(f"  Idea: {idea[:80]}...")

def reset_pipeline():
    state = {"version": "1.0", "current_agent": "analyst", "iteration": 0, "status": "idle",
             "project_idea": "", "analysis": "", "architecture": "", "code": "",
             "review": "", "optimizations": "", "deployment": "", "history": [],
             "config": {"max_iterations": 100, "delay_between_agents": 3, "max_api_calls_per_agent": 10, "quality_threshold": 8}}
    save_state(state)
    print("Pipeline reset.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print('  python run.py "Your project idea"')
        print("  python run.py --status")
        print("  python run.py --reset")
        sys.exit(1)
    if sys.argv[1] == "--status": show_status()
    elif sys.argv[1] == "--reset": reset_pipeline()
    else:
        idea = " ".join(sys.argv[1:])
        set_project_idea(idea)
        run_infinite_loop()