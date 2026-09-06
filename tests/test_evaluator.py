from schemas.review import ReviewFinding

from evaluation.evaluator import evaluate_findings


def test_evaluator():

    cases = [
        {
            "id": "sql-001",
            "file": "demo/app.py",
            "line": 15,
            "expected_category": "security",
            "expected_issue_keywords": ["sql", "injection"],
        },
        {
            "id": "safe-001",
            "file": "demo/app.py",
            "line": 20,
            "expected_category": None,
            "expected_issue_keywords": [],
        },
    ]

    findings = [
        ReviewFinding(
            severity="CRITICAL",
            category="security",
            file="demo/app.py",
            line=15,
            issue="SQL Injection",
            explanation="Unsafe SQL construction.",
            suggested_fix="Use parameterized queries.",
        )
    ]

    result = evaluate_findings(cases, findings)

    assert result["true_positives"] == 1
    assert result["false_positives"] == 0
    assert result["false_negatives"] == 0
    assert result["true_negatives"] == 1
    assert result["precision"] == 1.0
    assert result["recall"] == 1.0
    assert result["f1"] == 1.0


def test_false_positive():

    cases = [
        {
            "id": "safe-001",
            "file": "demo/app.py",
            "line": 20,
            "expected_category": None,
            "expected_issue_keywords": [],
        }
    ]

    findings = [
        ReviewFinding(
            severity="LOW",
            category="security",
            file="demo/app.py",
            line=20,
            issue="Potential security issue",
            explanation="Test finding.",
            suggested_fix="Review the code.",
        )
    ]

    result = evaluate_findings(cases, findings)

    assert result["true_positives"] == 0
    assert result["false_positives"] == 1
    assert result["false_negatives"] == 0
