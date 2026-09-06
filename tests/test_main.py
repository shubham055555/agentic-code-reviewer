from unittest.mock import patch

import main


def test_main_posts_review_comment():

    fake_diff = """diff --git a/demo/app.py b/demo/app.py
--- a/demo/app.py
+++ b/demo/app.py
@@ -15,0 +16,1 @@
+query = "SELECT * FROM users WHERE name = '" + username + "'"
"""

    with patch(
        "main.get_pull_request_diff",
        return_value=fake_diff,
    ), patch(
        "main.review_security_changes",
        return_value=[],
    ), patch(
        "main.review_error_handling_changes",
        return_value=[],
    ), patch(
        "main.review_testing_changes",
        return_value=[],
    ), patch(
        "main.upsert_pull_request_comment",
    ) as mock_upsert:

        main.main()

    mock_upsert.assert_called_once()

    args = mock_upsert.call_args.args

    assert args[0] == "shubham055555"
    assert args[1] == "agentic-code-reviewer"
    assert args[2] == 1
    assert "Agentic Code Review" in args[3]
    assert "No security, error-handling, or testing issues found." in args[3]


def test_main_uses_environment_configuration(monkeypatch):

    monkeypatch.setenv("GITHUB_OWNER", "test-owner")
    monkeypatch.setenv("GITHUB_REPO", "test-repo")
    monkeypatch.setenv("GITHUB_PR_NUMBER", "42")

    import importlib

    importlib.reload(main)

    assert main.OWNER == "test-owner"
    assert main.REPO == "test-repo"
    assert main.PR_NUMBER == 42
