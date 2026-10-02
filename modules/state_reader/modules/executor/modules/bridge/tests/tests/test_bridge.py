"""
Focused bridge tests.
Run: pytest tests/test_bridge.py -v
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import modules.state_reader as _sr

_FAKE_STATE = {
    "status": "ACTIVE",
    "verified_capabilities": ["Router", "Executor"],
}

_sr.read_state = lambda: _FAKE_STATE

from modules.bridge import dispatch_task
from modules.executor import ActionResult


def test_non_execute_returns_routing_dict():
    result = dispatch_task("analyze the gaps and conflicts")
    assert isinstance(result, dict)
    assert result["route"] == "analyze"
    assert "module" in result


def test_execute_read_file_pass(tmp_path):
    f = tmp_path / "hello.txt"
    f.write_text("hello")

    result = dispatch_task(
        "perform the action",
        payload={
            "action": "read_file",
            "payload": {"path": str(f)},
            "requires_confirmation": False,
        },
    )

    assert isinstance(result, ActionResult)
    assert result.status == "PASS"
    assert result.action == "read_file"


def test_execute_confirmation_guard():
    result = dispatch_task(
        "perform the action",
        payload={
            "action": "update_state",
            "payload": {},
            "requires_confirmation": True,
        },
    )

    assert isinstance(result, ActionResult)
    assert result.status == "REQUIRES_CONFIRMATION"


def test_execute_unknown_action():
    result = dispatch_task(
        "do the action",
        payload={
            "action": "delete_everything",
            "payload": {},
        },
    )

    assert isinstance(result, ActionResult)
    assert result.status == "UNKNOWN_ACTION"


def test_execute_missing_action_key():
    result = dispatch_task("perform the action", payload={})

    assert isinstance(result, ActionResult)
    assert result.status == "FAIL"
    assert "action" in result.error


def test_execute_write_file(tmp_path):
    out = tmp_path / "out.txt"

    result = dispatch_task(
        "do the action",
        payload={
            "action": "write_file",
            "payload": {
                "path": str(out),
                "content": "test data",
            },
            "requires_confirmation": False,
        },
    )

    assert result.status == "PASS"
    assert out.read_text() == "test data"
    assert str(out) in result.changed
