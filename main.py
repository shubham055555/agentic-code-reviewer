from github.client import get_pull_request_diff


OWNER = "octocat"
REPO = "Hello-World"
PR_NUMBER = 1


diff = get_pull_request_diff(
    OWNER,
    REPO,
    PR_NUMBER
)

print(diff)
