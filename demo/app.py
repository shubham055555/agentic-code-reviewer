import sqlite3

def get_user(username):
    conn = sqlite3.connect("users.db")
    query = "SELECT * FROM users WHERE name = '" + username + "'"
    return conn.execute(query).fetchall()


def delete_user(user_id):
    conn = sqlite3.connect("users.db")
    query = "DELETE FROM users WHERE id = " + str(user_id)
    conn.execute(query)
    conn.commit()


def update_user(username, email):
    conn = sqlite3.connect("users.db")
    query = "UPDATE users SET email = '" + email + "' WHERE name = '" + username + "'"
    conn.execute(query)
    conn.commit()
