from __future__ import annotations
from typing import Any

from modules.router import route_task
from modules.executor import ActionContract, ActionResult, execute_action

class BridgeError(Exception):
    pass

def dispatch_task(task: str, payload: dict[str, Any] | None = None) -> ActionResult | dict:
    routing = route_task(task)

    if routing["route"] != "execute":
        return routing

    p = payload or {}
    action = p.get("action", "")
    if not action:
        return ActionResult(
            action="",
            status="FAIL",
            error="route=='execute' but payload missing 'action' key.",
        )

    contract = ActionContract(
        action=action,
        payload=p.get("payload", {}),
        requires_confirmation=p.get("requires_confirmation", False),
        description=p.get("description", task),
    )
    return execute_action(contract)
