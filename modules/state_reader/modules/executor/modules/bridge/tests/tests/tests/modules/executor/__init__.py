from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


class ExecutorError(Exception):
    pass


class ConfirmationRequired(ExecutorError):
    pass


@dataclass
class ActionContract:
    action: str
    payload: dict[str, Any]
    requires_confirmation: bool = False


@dataclass
class ActionResult:
    success: bool
    action: str
    result: Any = None
    error: str | None = None
    evidence: dict[str, Any] | None = None


def _require_confirmation(contract: ActionContract, confirmed: bool) -> None:
    if contract.requires_confirmation and not confirmed:
        raise ConfirmationRequired(
            f"Confirmation required for action: {contract.action}"
        )


def write_file(payload: dict[str, Any]) -> dict[str, Any]:
    path = Path(payload["path"])
    content = payload.get("content", "")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

    return {
        "path": str(path),
        "bytes_written": len(content.encode("utf-8")),
    }


def read_file(payload: dict[str, Any]) -> dict[str, Any]:
    path = Path(payload["path"])

    if not path.exists():
        raise ExecutorError(f"File not found: {path}")

    return {
        "path": str(path),
        "content": path.read_text(encoding="utf-8"),
    }


def update_state(payload: dict[str, Any]) -> dict[str, Any]:
    path = Path(payload["path"])
    content = payload["content"]

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

    return {
        "path": str(path),
        "updated": True,
    }


def run_test(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "BLOCKED",
        "reason": "Test execution is not enabled by the current executor policy.",
        "requested_test": payload.get("test"),
    }


def record_evidence(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "recorded": True,
        "evidence": payload,
    }


HANDLERS: dict[str, Callable[[dict[str, Any]], dict[str, Any]]] = {
    "write_file": write_file,
    "read_file": read_file,
    "update_state": update_state,
    "run_test": run_test,
    "record_evidence": record_evidence,
}


def execute(
    contract: ActionContract,
    *,
    confirmed: bool = False,
) -> ActionResult:
    try:
        _require_confirmation(contract, confirmed)

        handler = HANDLERS.get(contract.action)
        if handler is None:
            raise ExecutorError(
                f"Unknown action: {contract.action}"
            )

        result = handler(contract.payload)

        return ActionResult(
            success=True,
            action=contract.action,
            result=result,
            evidence={
                "action": contract.action,
                "payload": contract.payload,
            },
        )

    except Exception as exc:
        return ActionResult(
            success=False,
            action=contract.action,
            error=str(exc),
            evidence={
                "action": contract.action,
                "payload": contract.payload,
            },
        )


def execute_action(
    action: str,
    payload: dict[str, Any] | None = None,
    *,
    confirmed: bool = False,
) -> ActionResult:
    payload = payload or {}

    contract = ActionContract(
        action=action,
        payload=payload,
        requires_confirmation=action == "update_state",
    )

    return execute(contract, confirmed=confirmed)
