from unittest.mock import patch

from agents.error_handling import review_error_handling_changes
from schemas.review import ReviewFinding


def test_error_handling_review():

    mock_finding = ReviewFinding(
        severity="MEDIUM",
        category="error_handling",
        file="demo/app.py",
        line=16,
        issue="Database operation lacks error handling",
        explanation="The database operation can fail without being handled.",
        suggested_fix="Handle the database exception appropriately.",
    )

    changes = [
        {
            "file": "demo/app.py",
            "line": 16,
            "code": "    conn.execute(query)"
        }
    ]

    with patch("agents.error_handling.get_client") as mock_client:

        mock_generate = mock_client.return_value.models.generate_content
        mock_generate.return_value.text = mock_finding.model_dump_json()
        mock_generate.return_value.parsed = [mock_finding.model_dump()]

        findings = review_error_handling_changes(changes)

    assert len(findings) == 1
    assert findings[0].category == "error_handling"
    assert findings[0].file == "demo/app.py"
    assert findings[0].line == 16
    assert findings[0].severity == "MEDIUM"
