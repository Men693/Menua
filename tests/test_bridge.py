from modules.bridge import dispatch_task


def test_non_execute_route_returns_routing():
    result = dispatch_task("analyze the current objective")

    assert result["route"] == "analyze"
    assert result["module"] == "analyzer"


def test_execute_requires_action():
    result = dispatch_task(
        "execute this task",
        payload={},
    )

    assert result["route"] == "execute"
    assert result["status"] == "FAIL