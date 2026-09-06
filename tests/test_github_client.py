from unittest.mock import Mock, patch

from github.client import upsert_pull_request_comment


def test_updates_existing_review_comment(monkeypatch):

    monkeypatch.setenv("GITHUB_TOKEN", "test-token")

    existing_comment = {
        "id": 12345,
        "body": "## Agentic Code Review\n\nOld review",
    }

    with patch(
        "github.client.find_existing_review_comment",
        return_value=existing_comment,
    ), patch(
        "github.client.requests.patch",
    ) as mock_patch, patch(
        "github.client.requests.post",
    ) as mock_post:

        mock_patch.return_value.raise_for_status = Mock()
        mock_patch.return_value.json.return_value = {
            "id": 12345,
            "body": "## Agentic Code Review\n\nUpdated review",
        }

        result = upsert_pull_request_comment(
            "shubham055555",
            "agentic-code-reviewer",
            1,
            "## Agentic Code Review\n\nUpdated review",
        )

    mock_patch.assert_called_once()
    mock_post.assert_not_called()

    assert result["id"] == 12345


def test_creates_comment_when_no_existing_review(monkeypatch):

    monkeypatch.setenv("GITHUB_TOKEN", "test-token")

    with patch(
        "github.client.find_existing_review_comment",
        return_value=None,
    ), patch(
        "github.client.post_pull_request_comment",
    ) as mock_post:

        mock_post.return_value = {
            "id": 67890,
            "body": "## Agentic Code Review\n\nNew review",
        }

        result = upsert_pull_request_comment(
            "shubham055555",
            "agentic-code-reviewer",
            1,
            "## Agentic Code Review\n\nNew review",
        )

    mock_post.assert_called_once()

    assert result["id"] == 67890
