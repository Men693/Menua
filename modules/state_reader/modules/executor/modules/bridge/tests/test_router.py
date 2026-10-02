import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from modules.router import route_task, classify_task, ROUTES, TASK_KEYWORDS


def test_classify_known_routes():
    assert classify_task("analyze the gaps") == "analyze"
    assert classify_task("plan next steps") == "plan"
    assert classify_task("evaluate the output") == "evaluate"
    assert classify_task("research the topic") == "research"
    assert classify_task("execute the action") == "execute"
    assert classify_task("what is the current state") == "state"
    assert classify_task("audit the system") == "audit"


def test_classify_unknown_returns_none():
    assert classify_task("hello world") is None
    assert classify_task("") is None


def test_route_analyze():
    result = route_task("analyze the gaps in the project")
    assert result["route"] == "analyze"
    assert result["module"] == "analyzer"
    assert "MENUA_CORE.md" in result["required_context"]
    assert isinstance(result["state_reference"], dict)
    assert result["verification_required"] is False


def test_route_execute():
    result = route_task("execute the task")
    assert result["route"] == "execute"
    assert result["module"] == "executor"
    assert result["verification_required"] is True


def test_route_audit():
    result = route_task("audit the system")
    assert result["route"] == "audit"
    assert result["verification_required"] is True


def test_route_state():
    result = route_task("what is the current state")
    assert result["route"] == "state"
    assert result["module"] == "state_reader"
    assert result["verification_required"] is False


def test_route_unknown_task():
    result = route_task("hello")
    assert result["route"] == "UNKNOWN"
    assert result["module"] is None
    assert "MENUA_CORE.md" in result["required_context"]
    assert isinstance(result["ambiguous_matches"], list)


def test_router_does_not_mutate_state():
    r1 = route_task("analyze the gaps")
    r2 = route_task("analyze the gaps")
    assert r1["route"] == r2["route"]
    assert r1["state_reference"] == r2["state_reference"]


def test_route_output_has_required_keys():
    result = route_task("plan the next steps")
    for key in (
        "route",
        "module",
        "reason",
        "required_context",
        "state_reference",
        "verification_required",
        "ambiguous_matches",
    ):
        assert key in result, f"Missing key: {key}"


if __name__ == "__main__":
    tests = [
        test_classify_known_routes,
        test_classify_unknown_returns_none,
        test_route_analyze,
        test_route_execute,
        test_route_audit,
        test_route_state,
        test_route_unknown_task,
        test_router_does_not_mutate_state,
        test_route_output_has_required_keys,
    ]

    passed = 0
    failed = 0

    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
            passed += 1
        except Exception as e:
            print(f"  FAIL  {t.__name__}: {e}")
            failed += 1

    print(f"\n{passed}/{passed+failed} tests passed")

    if failed:
        sys.exit(1)
