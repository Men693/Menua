from __future__ import annotations

from typing import Any

from modules.executor import ActionContract, execute_action
from modules.router import route_task


def dispatch_task(
    task: str,
    payload: dict[str, Any] | None = None,
    *,
    confirmed: bool = False,
) -> dict[str, Any]:
    payload = payload or {}

    routing = route_task(task)

    if routing.get("route") != "execute":
        return routing

    action = payload.get("action")

    if not action:
        return {
            **routing,
            "status": "FAIL",
            "error": "Execute route requires an action",
        }

    contract = ActionContract(
        action=action,
        payload=payload.get("payload", {}),
        requires_confirmation=payload.get(
            "requires_confirmation",
            action == "update_state",
        ),
    )

    result = execute_action(contract)

    if confirmed and result.status == "REQUIRES_CONFIRMATION":
        confirmed_contract = ActionContract(
            action=contract.action,
            payload=contract.payload,
            requires