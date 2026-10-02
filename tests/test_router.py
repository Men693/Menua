from modules.router import route_task


def test_analyze_route():
    result = route_task("analyze the current objective")

    assert result["route"] == "analyze"
    assert result["module"] == "analyzer"


def test_plan_route():
    result = route_task("create a plan for the project")

    assert result["route"] == "plan"
    assert result["module"] == "planner"


def test_evaluate_route():
    result = route_task("evaluate this result")

    assert result["route"] == "evaluate"
    assert result["module"] == "evaluator"


def test_research_route():
    result = route_task("research this topic")

    assert result["route"] == "research"
    assert result["module"] == "researcher"


def test_execute_route():
    result = route_task("execute this action")

    assert result["route"] == "execute"
    assert result["module"] == "executor"


def test_state_route():
    result = route_task("show the current state")

    assert result["route"] == "state"
    assert result["module"] == "state_reader"


def test_audit_route():
    result = route_task("audit the project integrity")

    assert result["route"] == "audit"
    assert result["module"] == "audit"


def test_unknown_route():
    result = route_task("hello")

    assert result["route"] == "UNKNOWN"


def test_ambiguous_route():
    result = route_task(
        "analyze the current state and verify it"
    )

    assert result["route"] == "UNKNOWN"
    assert result["ambiguous_matches"]