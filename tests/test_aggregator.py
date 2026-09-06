from agents.aggregator import aggregate_findings
from schemas.review import ReviewFinding


def test_aggregate_findings():
    security = ReviewFinding(
        severity="HIGH",
        category="security",
        file="demo/app.py",
        line=15,
        issue="SQL injection",
        explanation="User input is concatenated into SQL.",
        suggested_fix="Use parameterized queries.",
    )

    testing = ReviewFinding(
        severity="MEDIUM",
        category="testing",
        file="demo/app.py",
        line=13,
        issue="Missing test",
        explanation="New function has no regression test.",
        suggested_fix="Add tests for update_user.",
    )

    result = aggregate_findings([testing, security, None])

    assert len(result) == 2
    assert result[0].severity == "HIGH"
    assert result[0].category == "security"
    assert result[1].severity == "MEDIUM"
    assert result[1].category == "testing"


def test_duplicate_findings_are_removed():
    finding = ReviewFinding(
        severity="HIGH",
        category="security",
        file="demo/app.py",
        line=15,
        issue="SQL injection",
        explanation="User input is concatenated into SQL.",
        suggested_fix="Use parameterized queries.",
    )

    result = aggregate_findings([finding, finding])

    assert len(result) == 1
