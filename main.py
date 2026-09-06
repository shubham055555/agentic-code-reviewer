from github.client import get_pull_request_diff
from github.diff_parser import parse_diff

from agents.security import review_security_changes
from agents.error_handling import review_error_handling_changes
from agents.test_reviewer import review_testing_changes
from agents.aggregator import aggregate_findings


OWNER = "shubham055555"
REPO = "agentic-code-reviewer"
PR_NUMBER = 1


def run_agent_safely(agent_name, agent_function, changes):

    try:
        return agent_function(changes)

    except Exception as exc:
        print(
            f"{agent_name} failed: "
            f"{type(exc).__name__}: {exc}"
        )
        print(
            f"{agent_name} failure isolated. "
            "Continuing with remaining agents."
        )
        return []


def main():
    print(f"Fetching PR #{PR_NUMBER}...")

    diff = get_pull_request_diff(
        OWNER,
        REPO,
        PR_NUMBER
    )

    changes = parse_diff(diff)

    changes = [
        change
        for change in changes
        if change["code"].strip()
    ]

    print(f"\nFound {len(changes)} changed lines.")

    if not changes:
        print("\nNo code changes found.")
        return

    print("\nRunning Security Agent...")
    security_findings = run_agent_safely(
        "Security Agent",
        review_security_changes,
        changes,
    )

    print("\nRunning Error Handling Agent...")
    error_findings = run_agent_safely(
        "Error Handling Agent",
        review_error_handling_changes,
        changes,
    )

    print("\nRunning Testing Agent...")
    testing_findings = run_agent_safely(
        "Testing Agent",
        review_testing_changes,
        changes,
    )

    all_findings = (
        security_findings
        + error_findings
        + testing_findings
    )

    final_findings = aggregate_findings(all_findings)

    print("\n" + "=" * 70)
    print("FINAL CODE REVIEW")
    print("=" * 70)

    if not final_findings:
        print("\nNo issues found.")
        return

    print(f"\nTotal findings: {len(final_findings)}")

    for index, finding in enumerate(final_findings, start=1):
        print(f"\n[{index}] {finding.severity} - {finding.category}")
        print(f"File: {finding.file}")
        print(f"Line: {finding.line}")
        print(f"Issue: {finding.issue}")
        print(f"Explanation: {finding.explanation}")
        print(f"Suggested fix: {finding.suggested_fix}")


if __name__ == "__main__":
    main()
