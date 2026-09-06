from schemas.review import ReviewFinding


def aggregate_findings(
    findings: list[ReviewFinding | None]
) -> list[ReviewFinding]:

    valid_findings = [
        finding
        for finding in findings
        if finding is not None
    ]

    # Remove exact duplicate findings
    unique = {}

    for finding in valid_findings:
        key = (
            finding.file,
            finding.line,
            finding.category,
            finding.issue,
        )
        unique[key] = finding

    # Highest severity first
    severity_order = {
        "CRITICAL": 4,
        "HIGH": 3,
        "MEDIUM": 2,
        "LOW": 1,
    }

    return sorted(
        unique.values(),
        key=lambda finding: severity_order[finding.severity],
        reverse=True,
    )
