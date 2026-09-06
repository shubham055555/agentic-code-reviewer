from unittest.mock import patch

from agents.test_reviewer import review_testing_changes
from schemas.review import ReviewFinding


def test_testing_review():

    mock_finding = ReviewFinding(
        severity="MEDIUM",
        category="testing",
        file="demo/app.py",
        line=13,
        issue="Missing regression test",
        explanation="A new function was added without a corresponding test.",
        suggested_fix="Add tests covering update_user behavior and edge cases.",
    )

    changes = [
        {
            "file": "demo/app.py",
            "line": 13,
            "code": "def update_user(username, email):"
        }
    ]

    with patch("agents.test_reviewer.get_client") as mock_client:

        mock_generate = mock_client.return_value.models.generate_content
        mock_generate.return_value.text = mock_finding.model_dump_json()
        mock_generate.return_value.parsed = [mock_finding.model_dump()]

        findings = review_testing_changes(changes)

    assert len(findings) == 1
    assert findings[0].category == "testing"
    assert findings[0].file == "demo/app.py"
    assert findings[0].line == 13
    assert findings[0].severity == "MEDIUM"
