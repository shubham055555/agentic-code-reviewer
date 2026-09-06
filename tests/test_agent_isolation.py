from main import run_agent_safely


def test_agent_failure_is_isolated():

    def failing_agent(changes):
        raise RuntimeError("simulated agent failure")

    result = run_agent_safely(
        "Test Agent",
        failing_agent,
        [],
    )

    assert result == []


def test_successful_agent_returns_findings():

    expected = ["finding-1", "finding-2"]

    def successful_agent(changes):
        return expected

    result = run_agent_safely(
        "Test Agent",
        successful_agent,
        [],
    )

    assert result == expected
