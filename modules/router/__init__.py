from __future__ import annotations
import sys
from pathlib import Path

# Allow import of state_reader from sibling module
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from modules.state_reader import read_state, StateReaderError

ROUTES = {
    "analyze":   {"module": "analyzer",   "description": "Analyze objective, gaps, conflicts"},
    "plan":      {"module": "planner",    "description": "Convert findings into ordered plan"},
    "evaluate":  {"module": "evaluator",  "description": "Validate output against requirements"},
    "research":  {"module": "researcher", "description": "Gather external information"},
    "execute":   {"module": "executor",   "description": "Perform authorized action"},
    "state":     {"module": "state_reader","description": "Read current canonical state"},
    "audit":     {"module": "audit",      "description": "Audit structural/persistence integrity"},
}

TASK_KEYWORDS: dict[str, list[str]] = {
    "analyze":  ["analyze", "analysis", "gap", "conflict", "review", "assess", "վերլուծ"],
    "plan":     ["plan", "planning", "schedule", "roadmap", "steps", "պլան"],
    "evaluate": ["evaluate", "validate", "verify", "check", "test", "ստուգ"],
    "research": ["research", "find", "search", "look up", "investigate", "ուսումնասիր"],
    "execute":  ["execute", "run", "do", "perform", "create", "build", "կատար", "կառուց"],
    "state":    ["state", "status", "current", "what is", "վիճակ", "կարգավիճ"],
    "audit":    ["audit", "integrity", "persist", "audit mode", "աուդիտ"],
}
