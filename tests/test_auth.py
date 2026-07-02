import sqlite3

from werkzeug.security import check_password_hash

import app as app_module


def make_client(tmp_path):
    app_module.DATABASE_PATH = str(tmp_path / "database.db")
    app_module.app.config.update(TESTING=True, SECRET_KEY="test")
    app_module.init_db()
    return app_module.app.test_client()


def fetch_password(database_path, username):
    conn = sqlite3.connect(database_path)
    row = conn.execute(
        "SELECT password FROM users WHERE username = ?",
        (username,),
    ).fetchone()
    conn.close()
    return row[0]


def test_register_stores_password_hash(tmp_path):
    client = make_client(tmp_path)

    response = client.post(
        "/register",
        data={"username": "alice", "password": "known-pass"},
    )

    assert response.status_code == 302
    stored_password = fetch_password(app_module.DATABASE_PATH, "alice")
    assert stored_password != "known-pass"
    assert app_module.is_password_hash(stored_password)
    assert check_password_hash(stored_password, "known-pass")


def test_login_rehashes_legacy_plaintext_password(tmp_path):
    client = make_client(tmp_path)
    conn = sqlite3.connect(app_module.DATABASE_PATH)
    conn.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        ("legacy", "known-pass"),
    )
    conn.commit()
    conn.close()

    response = client.post(
        "/",
        data={"username": "legacy", "password": "known-pass"},
    )

    assert response.status_code == 302
    with client.session_transaction() as flask_session:
        assert flask_session["usuario_logado"] == "legacy"

    stored_password = fetch_password(app_module.DATABASE_PATH, "legacy")
    assert stored_password != "known-pass"
    assert app_module.is_password_hash(stored_password)
    assert check_password_hash(stored_password, "known-pass")
