import subprocess
import re


def get_diff():
    result = subprocess.run(
        ["git", "diff", "--unified=0"],
        capture_output=True,
        text=True,
        check=True
    )

    return result.stdout


def parse_diff(diff):
    changes = []
    current_file = None
    current_line = None

    for line in diff.splitlines():

        if line.startswith("+++ b/"):
            current_file = line[6:]
            continue

        if line.startswith("@@"):
            match = re.search(r"\+(\d+)(?:,(\d+))?", line)

            if match:
                current_line = int(match.group(1))

            continue

        if line.startswith("+") and not line.startswith("+++"):
            if current_file and current_line is not None:

                changes.append({
                    "file": current_file,
                    "line": current_line,
                    "code": line[1:]
                })

                current_line += 1

    return changes


if __name__ == "__main__":
    diff = get_diff()

    print("=== RAW DIFF ===")
    print(diff)

    print("\n=== PARSED CHANGES ===")

    changes = parse_diff(diff)

    for change in changes:
        print(change)
