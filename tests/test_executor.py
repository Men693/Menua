import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from modules.executor import (
    ActionContract,
    execute_action,
    REGISTERED_ACTIONS,
)


def test_unknown_action_rejected():
    result = execute_action(
        ActionContract(action="nonexistent_action")
    )
    assert result.status == "UNKNOWN_ACTION"
    assert "not registered" in result.error


def test_confirmation_guard():
    result = execute_action(
        ActionContract(
            action="write_file",
            payload={"path": "/tmp/test.txt", "content": "x"},
            requires_confirmation=True,
        )
    )
    assert result.status == "REQUIRES_CONFIRMATION"


def test_read_file_missing():
    result = execute_action(
        ActionContract(
            action="read_file",
            payload={"path": "/