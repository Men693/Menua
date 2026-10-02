from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable


class ExecutorError(Exception):
    pass


class ConfirmationRequired(ExecutorError):
    pass


@dataclass
class ActionContract:
    action: str
    payload: dict[str, Any] = field(default_factory=dict)
    requires_confirmation: bool = False


@dataclass
class ActionResult:
    status: str
    action: str
    result: Any = None
    error: str | None = None
    changed: list[str] = field(default_factory=list)
    evidence: dict[str, Any] | None = None


def _require_confirmation(contract: ActionContract) -> None:
    if contract.requires_confirmation:
        raise ConfirmationRequired(
            f"Confirmation required for action: {contract.action}"
        )


def _write_file(payload: dict[str, Any]) -> dict[str, Any]:
    path = Path(payload["path"])
    content = payload.get("content", "")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

    return {
        "path": str(path),
        "bytes_written": len(content.encode("utf-8")),
    }


def _read_file(payload: dict[str, Any]) -> dict[str, Any]:
    path = Path(payload["path"])

    if not path.exists():
        raise ExecutorError(f"File not found: {path}")

    return {
        "path": str(path),
        "content": path.read_text(encoding="utf-8"),
    }