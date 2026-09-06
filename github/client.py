import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.github.com"


def get_headers():
    github_token = os.getenv("GITHUB_TOKEN")

    if not github_token:
        raise RuntimeError(
            "GITHUB_TOKEN is required for GitHub API requests."
        )

    return {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github+json",
    }


def get_pull_request(owner, repo, pull_number):
    url = f"{BASE_URL}/repos/{owner}/{repo}/pulls/{pull_number}"

    response = requests.get(
        url,
        headers=get_headers(),
        timeout=30,
    )

    response.raise_for_status()
    return response.json()


def get_pull_request_diff(owner, repo, pull_number):
    url = f"{BASE_URL}/repos/{owner}/{repo}/pulls/{pull_number}"

    headers = get_headers()
    headers["Accept"] = "application/vnd.github.diff"

    response = requests.get(
        url,
        headers=headers,
        timeout=30,
    )

    response.raise_for_status()
    return response.text


def post_pull_request_comment(owner, repo, pull_number, body):
    url = (
        f"{BASE_URL}/repos/{owner}/{repo}"
        f"/issues/{pull_number}/comments"
    )

    response = requests.post(
        url,
        headers=get_headers(),
        json={"body": body},
        timeout=30,
    )

    response.raise_for_status()
    return response.json()


def find_existing_review_comment(owner, repo, pull_number):
    url = (
        f"{BASE_URL}/repos/{owner}/{repo}"
        f"/issues/{pull_number}/comments"
    )

    response = requests.get(
        url,
        headers=get_headers(),
        params={"per_page": 100},
        timeout=30,
    )

    response.raise_for_status()

    for comment in response.json():
        body = comment.get("body", "")

        if body.startswith("## Agentic Code Review"):
            return comment

    return None


def upsert_pull_request_comment(owner, repo, pull_number, body):
    existing_comment = find_existing_review_comment(
        owner,
        repo,
        pull_number,
    )

    if existing_comment:
        comment_id = existing_comment["id"]

        url = (
            f"{BASE_URL}/repos/{owner}/{repo}"
            f"/issues/comments/{comment_id}"
        )

        response = requests.patch(
            url,
            headers=get_headers(),
            json={"body": body},
            timeout=30,
        )

        response.raise_for_status()
        return response.json()

    return post_pull_request_comment(
        owner,
        repo,
        pull_number,
        body,
    )

