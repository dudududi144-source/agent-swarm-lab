"""Quality Gates - Validates output between agents."""
import json, os, re

MIN_CODE_LENGTH = 100
MAX_CODE_LENGTH = 50000
MIN_ANALYSIS_LENGTH = 50

def validate_analysis(analysis):
    """Validate analyst output."""
    if not analysis or len(analysis) < MIN_ANALYSIS_LENGTH:
        return False, "Analysis too short"
    return True, "OK"

def validate_architecture(architecture):
    """Validate architect output."""
    if not architecture or len(architecture) < MIN_ANALYSIS_LENGTH:
        return False, "Architecture too short"
    return True, "OK"

def validate_code(code):
    """Validate builder/optimizer output."""
    if not code:
        return False, "No code generated"
    if len(code) < MIN_CODE_LENGTH:
        return False, "Code too short"
    if len(code) > MAX_CODE_LENGTH:
        return False, "Code too long"
    # Check for common issues
    if code.count("TODO") > 5:
        return False, "Too many TODOs"
    return True, "OK"

def validate_review(review):
    """Validate reviewer output."""
    if not review or len(review) < 20:
        return False, "Review too short"
    return True, "OK"

def run_quality_gate(agent_name, output):
    """Run appropriate quality gate for agent output."""
    gates = {
        "analyst": validate_analysis,
        "architect": validate_architecture,
        "builder": validate_code,
        "reviewer": validate_review,
        "optimizer": validate_code,
        "deployer": lambda x: (True, "OK")
    }
    gate = gates.get(agent_name, lambda x: (True, "OK"))
    passed, reason = gate(output)
    if not passed:
        print(f"[QUALITY] {agent_name} failed: {reason}")
    return passed, reason