from github.diff_parser import parse_diff


def test_parse_added_lines():
    diff = """diff --git a/demo/app.py b/demo/app.py
--- a/demo/app.py
+++ b/demo/app.py
@@ -6,0 +7,3 @@
+def delete_user(user_id):
+    conn = sqlite3.connect("users.db")
+    conn.commit()
"""

    result = parse_diff(diff)

    assert len(result) == 3
    assert result[0]["file"] == "demo/app.py"
    assert result[0]["line"] == 7
    assert result[0]["code"] == "def delete_user(user_id):"
    assert result[1]["line"] == 8
    assert result[2]["line"] == 9


def test_multiple_files():
    diff = """diff --git a/a.py b/a.py
--- a/a.py
+++ b/a.py
@@ -1,0 +2,1 @@
+print("hello")
diff --git a/b.py b/b.py
--- a/b.py
+++ b/b.py
@@ -1,0 +2,1 @@
+print("world")
"""

    result = parse_diff(diff)

    assert len(result) == 2
    assert result[0]["file"] == "a.py"
    assert result[1]["file"] == "b.py"
