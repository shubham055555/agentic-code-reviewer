from agents.security import review_security_changes
from agents.error_handling import review_error_handling_changes
from agents.test_reviewer import review_testing_changes

from evaluation.evaluator import (
    load_dataset,
    evaluate_findings,
    generate_failure_report,
)


def main():

    cases = load_dataset()

    changes = [
        {
            "file": case["file"],
            "line": case["line"],
            "code": case["code"],
        }
        for case in cases
    ]

    print(f"Loaded {len(cases)} evaluation cases.")

    print("\nRunning Security Agent...")
    security_findings = review_security_changes(changes)

    print("Running Error Handling Agent...")
    error_findings = review_error_handling_changes(changes)

    print("Running Testing Agent...")
    testing_findings = review_testing_changes(changes)

    findings = (
        security_findings
        + error_findings
        + testing_findings
    )

    print(f"\nTotal findings produced: {len(findings)}")

    print("\n" + "=" * 70)
    print("PRODUCED FINDINGS")
    print("=" * 70)

    for index, finding in enumerate(findings, start=1):
        print(
            f"\n[{index}] {finding.severity} - {finding.category}"
        )
        print(f"File: {finding.file}")
        print(f"Line: {finding.line}")
        print(f"Issue: {finding.issue}")

    metrics = evaluate_findings(cases, findings)

    failure_report = generate_failure_report(cases, findings)

    print("\n" + "=" * 70)
    print("FAILURE ANALYSIS")
    print("=" * 70)

    for item in failure_report:
        print(
            f"{item['status']:10} | "
            f"{item['case_id'] or '-':25} | "
            f"{item['file']}:{item['line']} | "
            f"{item['issue']}"
        )

    print("\n" + "=" * 70)
    print("EVALUATION RESULTS")
    print("=" * 70)

    print(f"True Positives:   {metrics['true_positives']}")
    print(f"False Positives:  {metrics['false_positives']}")
    print(f"False Negatives:  {metrics['false_negatives']}")
    print(f"True Negatives:   {metrics['true_negatives']}")
    print(f"Precision:        {metrics['precision']:.2%}")
    print(f"Recall:           {metrics['recall']:.2%}")
    print(f"F1 Score:         {metrics['f1']:.2%}")


if __name__ == "__main__":
    main()
