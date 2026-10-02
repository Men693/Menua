import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from modules.executor import (
    ActionContract,
    execute_action,
    REGISTERED_ACTIONS,
)


def test_unknown_action_rejected():
    result = execute_action(ActionContract(action="nonexistent_action"))
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
            payload={"path": "/nonexistent/path/file.txt"},
        )
    )
    assert result.status == "FAIL"
    assert "not found" in result.error


def test_write_and_read_file(tmp_path):
    target = tmp_path / "executor_test.txt"

    write_result = execute_action(
        ActionContract(
            action="write_file",
            payload={
                "path": str(target),
                "content": "hello menua",
            },
        )
    )

    assert write_result.status == "PASS"
    assert str(target) in write_result.changed

    read_result = execute_action(
        ActionContract(
            action="read_file",
            payload={"path": str(target)},
        )
    )

    assert read_result.status == "PASS"


def test_record_evidence():
    result = execute_action(
        ActionContract(
            action="record_evidence",
            payload={"note": "test evidence"},
        )
    )
    assert result.status == "PASS"


def test_update_state_requires_confirmation():
    result = execute_action(
        ActionContract(action="update_state")
    )
    assert result.status == "REQUIRES_CONFIRMATION"


def test_all_registered_actions_have_handlers():
    from modules.executor import _HANDLERS

    for action in REGISTERED_ACTIONS:
        assert action in _HANDLERS, (
            f"No handler for registered action: {action}"
        )


if __name__ == "__main__":
    import tempfile

    tmp = Path(tempfile.mkdtemp())

    print("test_unknown_action_rejected...", end=" ")
    test_unknown_action_rejected()
    print("PASS")

    print("test_confirmation_guard...", end=" ")
    test_confirmation_guard()
    print("PASS")

    print("test_read_file_missing...", end=" ")
    test_read_file_missing()
    print("PASS")

    print("test_write_and_read_file...", end=" ")
    test_write_and_read_file(tmp)
    print("PASS")

    print("test_record_evidence...", end=" ")
    test_record_evidence()
    print("PASS")

    print("test_update_state_requires_confirmation...", end=" ")
    test_update_state_requires_confirmation()
    print("PASS")

    print("test_all_registered_actions_have_handlers...", end=" ")
    test_all_registered_actions_have_handlers()
    print("PASS")

    print("ALL PASS")
