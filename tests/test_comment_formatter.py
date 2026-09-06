from github.comment_formatter import format_review_comment
from schemas.review import ReviewFinding


def test_format_review_comment():

    findings = [
        ReviewFinding(
            severity="HIGH",
            category="security",
            file="demo/app.py",
            line=15,
            issue="SQL injection",
            explanation="User input is directly concatenated into SQL.",
            suggested_fix="Use parameterized queries.",
        )
    ]

    comment = format_review_comment(findings)

    assert "Agentic Code Review" in comment
    assert "HIGH" in comment
    assert "security" in comment
    assert "demo/app.py" in comment
    assert "15" in comment
    assert "SQL injection" in comment
    assert "Use parameterized queries." in comment


def test_format_empty_review_comment():

    comment = format_review_comment([])

    assert "Agentic Code Review" in comment
    assert "No security, error-handling, or testing issues found." in comment
