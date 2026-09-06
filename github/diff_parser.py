import subprocess
from pathlib import Path


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

    for line in diff.splitlines():

        if line.startswith("+++ b/"):
            current_file = line[6:]
            continue

        if line.startswith("@@"):
            parts = line.split(" ")

            new_location = next(
                part for part in parts if part.startswith("+")
            )

            line_number = int(
                new_location.split(",")[0].replace("+", "")
            )

            changes.append({
                "file": current_file,
                "line": line_number
            })

            continue

        if line.startswith("+") and not line.startswith("+++"):
            if current_file:
                changes[-1]["code"] = line[1:]

    return changes


if __name__ == "__main__":
    diff = get_diff()

    print("=== RAW DIFF ===")
    print(diff)

    print("\n=== PARSED CHANGES ===")
    print(parse_diff(diff))
