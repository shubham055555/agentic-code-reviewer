from unittest.mock import patch

from agents.security import review_security_changes
from schemas.review import ReviewFinding


def test_security_review_returns_finding():

    mock_finding = ReviewFinding(
        severity="HIGH",
        category="security",
        file="demo/app.py",
        line=15,
        issue="SQL injection",
        explanation="User input is directly concatenated into a SQL query.",
        suggested_fix="Use parameterized SQL queries.",
    )

    changes = [
        {
            "file": "demo/app.py",
            "line": 15,
            "code": 'query = "UPDATE users SET email = \'" + email + "\' WHERE name = \'" + username + "\'"'
        }
    ]

    with patch("agents.security.get_client") as mock_client:

        mock_generate = mock_client.return_value.models.generate_content
        mock_generate.return_value.text = mock_finding.model_dump_json()
        mock_generate.return_value.parsed = [mock_finding.model_dump()]

        findings = review_security_changes(changes)

    assert len(findings) == 1
    assert findings[0].category == "security"
    assert findings[0].file == "demo/app.py"
    assert findings[0].line == 15
    assert findings[0].severity == "HIGH"
