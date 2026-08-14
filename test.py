#!/usr/bin/env python3
"""Test script for Agent Swarm Lab."""
import json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "agents"))

def test_state_file():
    """Test that state.json exists and is valid."""
    state_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agents", "state.json")
    assert os.path.exists(state_file), "state.json not found"
    with open(state_file) as f:
        state = json.load(f)
    assert "current_agent" in state, "Missing current_agent"
    assert "iteration" in state, "Missing iteration"
    print("  [PASS] state.json valid")

def test_agents_exist():
    """Test that all agent files exist."""
    agents_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agents")
    expected = ["agent_1_analyst.py", "agent_2_architect.py", "agent_3_builder.py",
                "agent_4_reviewer.py", "agent_5_optimizer.py", "agent_6_deployer.py",
                "orchestrator.py", "config.json", "state.json"]
    for f in expected:
        path = os.path.join(agents_dir, f)
        assert os.path.exists(path), f"Missing: {f}"
    print("  [PASS] All agent files exist")

def test_config():
    """Test that config.json is valid."""
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agents", "config.json")
    with open(config_file) as f:
        config = json.load(f)
    assert "models" in config, "Missing models"
    assert "timing" in config, "Missing timing"
    assert "limits" in config, "Missing limits"
    print("  [PASS] config.json valid")

def test_quality_gates():
    """Test quality gates module."""
    from quality_gates import validate_code, validate_analysis
    passed, _ = validate_code("x" * 200)
    assert passed, "Valid code should pass"
    passed, _ = validate_code("")
    assert not passed, "Empty code should fail"
    passed, _ = validate_analysis("This is a valid analysis")
    assert passed, "Valid analysis should pass"
    print("  [PASS] Quality gates working")

if __name__ == "__main__":
    print("\n  AGENT SWARM LAB - TESTS")
    print("  " + "="*40)
    try:
        test_state_file()
        test_agents_exist()
        test_config()
        test_quality_gates()
        print("\n  ALL TESTS PASSED!")
    except AssertionError as e:
        print(f"\n  TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n  ERROR: {e}")
        sys.exit(1)