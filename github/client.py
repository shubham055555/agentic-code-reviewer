import os
import requests
from dotenv import load_dotenv


load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

BASE_URL = "https://api.github.com"


def get_pull_request(owner, repo, pull_number):
    url = f"{BASE_URL}/repos/{owner}/{repo}/pulls/{pull_number}"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    response = requests.get(url, headers=headers, timeout=30)

    response.raise_for_status()

    return response.json()


def get_pull_request_diff(owner, repo, pull_number):
    url = f"{BASE_URL}/repos/{owner}/{repo}/pulls/{pull_number}"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.diff"
    }

    response = requests.get(url, headers=headers, timeout=30)

    response.raise_for_status()

    return response.text
