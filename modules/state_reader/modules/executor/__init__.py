from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

REGISTERED_ACTIONS: set[str] = {
    "write_file",
    "read_file",
    "update_state",
    "run_test",
    "record_evidence",
}

@dataclass
class ActionContract:
    action: str
    payload: dict[str, Any] = field(default_factory=dict)
    requires_confirmation: bool = False
    description: str = ""

@dataclass
class ActionResult:
    action: str
    status: str
    evidence: str = ""
    changed: list[str] = field(default_factory=list)
    error: str = ""

class ExecutorError(Exception):
    pass

def execute_action(contract: ActionContract) -> ActionResult:
    action = contract.action

    if action not in REGISTERED_ACTIONS:
        return ActionResult(
            action=action,
            status="UNKNOWN_ACTION",
            error=f"Action '{action}' is not registered. Registered: {sorted(REGISTERED_ACTIONS)}",
        )

    if contract.requires_confirmation:
        return ActionResult(
            action=action,
            status="REQUIRES_CONFIRMATION",
            evidence=f"Action '{action}' requires explicit human confirmation before execution.",
        )

    try:
        handler = _HANDLERS.get(action)
        if handler is None:
            return ActionResult(
                action=action,
                status="BLOCKED",
                error=f"Handler for '{action}' is registered but not yet implemented.",
            )
        return handler(contract)
    except Exception as exc:
        return ActionResult(
            action=action,
            status="FAIL",
            error=str(exc),
        )

def _handle_read_file(contract: ActionContract) -> ActionResult:
    from pathlib import Path
    path = Path(contract.payload.get("path", ""))
    if not path.exists():
        return ActionResult(
            action=contract.action,
            status="FAIL",
            error=f"File not found: {path}",
        )
    content = path.read_text(encoding="utf-8")
    return ActionResult(
        action=contract.action,
        status="PASS",
        evidence=f"Read {len(content)} bytes from {path}",
    )

def _handle_write_file(contract: ActionContract) -> ActionResult:
    from pathlib import Path
    path = Path(contract.payload.get("path", ""))
    content = contract.payload.get("content", "")
    if not path:
        return ActionResult(
            action=contract.action,
            status="FAIL",
            error="No path in payload.",
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return ActionResult(
        action=contract.action,
        status="PASS",
        evidence=f"Wrote {len(content)} bytes to {path}",
        changed=[str(path)],
    )

def _handle_record_evidence(contract: ActionContract) -> ActionResult:
    note = contract.payload.get("note", "")
    return ActionResult(
        action=contract.action,
        status="PASS",
        evidence=f"Evidence recorded (stub): {note}",
    )

def _handle_run_test(contract: ActionContract) -> ActionResult:
    return ActionResult(
        action=contract.action,
        status="BLOCKED",
        error="run_test handler not yet implemented in this environment.",
    )

def _handle_update_state(contract: ActionContract) -> ActionResult:
    return ActionResult(
        action=contract.action,
        status="REQUIRES_CONFIRMATION",
        evidence="update_state modifies canonical state — requires explicit confirmation.",
    )

_HANDLERS = {
    "read_file": _handle_read_file,
    "write_file": _handle_write_file,
    "record_evidence": _handle_record_evidence,
    "run_test": _handle_run_test,
    "update_state": _handle_update_state,
}
