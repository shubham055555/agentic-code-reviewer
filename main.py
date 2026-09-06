from schemas.review import ReviewFinding


finding = ReviewFinding(
    severity="HIGH",
    category="security",
    file="app/db.py",
    line=42,
    issue="Potential SQL injection",
    explanation="User input is directly used in a SQL query.",
    suggested_fix="Use parameterized queries."
)

print(finding.model_dump_json(indent=2))
