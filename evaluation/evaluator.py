import json

from evaluation.metrics import calculate_metrics


def load_dataset(path="evaluation/dataset.json"):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def finding_matches_case(finding, case):
    if case["expected_category"] is None:
        return False

    if finding.file != case["file"]:
        return False

    if finding.line != case["line"]:
        return False

    if finding.category != case["expected_category"]:
        return False

    issue_text = finding.issue.lower()

    return any(
        keyword.lower() in issue_text
        for keyword in case["expected_issue_keywords"]
    )


def evaluate_findings(cases, findings):

    positive_cases = [
        case
        for case in cases
        if case["expected_category"] is not None
    ]

    negative_cases = [
        case
        for case in cases
        if case["expected_category"] is None
    ]

    matched_case_ids = set()
    true_positives = 0
    false_positives = 0

    for finding in findings:

        matched_positive = False

        for case in positive_cases:

            if case["id"] in matched_case_ids:
                continue

            if finding_matches_case(finding, case):
                matched_case_ids.add(case["id"])
                true_positives += 1
                matched_positive = True
                break

        if matched_positive:
            continue

        false_positives += 1

    false_negatives = len(positive_cases) - true_positives

    negative_findings = {
        (finding.file, finding.line)
        for finding in findings
    }

    false_positive_negative_cases = sum(
        1
        for case in negative_cases
        if (case["file"], case["line"]) in negative_findings
    )

    true_negatives = (
        len(negative_cases) - false_positive_negative_cases
    )

    metrics = calculate_metrics(
        true_positives=true_positives,
        false_positives=false_positives,
        false_negatives=false_negatives,
    )

    metrics["true_negatives"] = true_negatives

    return metrics


def generate_failure_report(cases, findings):

    positive_cases = [
        case
        for case in cases
        if case["expected_category"] is not None
    ]

    negative_cases = [
        case
        for case in cases
        if case["expected_category"] is None
    ]

    matched_finding_indexes = set()
    report = []

    # Check expected positive cases
    for case in positive_cases:

        matched = False

        for index, finding in enumerate(findings):

            if index in matched_finding_indexes:
                continue

            if finding_matches_case(finding, case):
                matched_finding_indexes.add(index)

                report.append({
                    "status": "MATCHED",
                    "case_id": case["id"],
                    "file": case["file"],
                    "line": case["line"],
                    "expected": case["expected_category"],
                    "issue": finding.issue,
                })

                matched = True
                break

        if not matched:
            report.append({
                "status": "MISSED",
                "case_id": case["id"],
                "file": case["file"],
                "line": case["line"],
                "expected": case["expected_category"],
                "issue": "No matching finding produced",
            })

    # Remaining findings are unexpected
    for index, finding in enumerate(findings):

        if index in matched_finding_indexes:
            continue

        report.append({
            "status": "UNEXPECTED",
            "case_id": None,
            "file": finding.file,
            "line": finding.line,
            "expected": "SAFE or different issue",
            "issue": finding.issue,
        })

    # Explicitly show safe cases
    for case in negative_cases:

        has_finding = any(
            finding.file == case["file"]
            and finding.line == case["line"]
            for finding in findings
        )

        if not has_finding:
            report.append({
                "status": "SAFE",
                "case_id": case["id"],
                "file": case["file"],
                "line": case["line"],
                "expected": "SAFE",
                "issue": "No finding produced",
            })

    return report
