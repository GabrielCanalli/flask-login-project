import os
import sqlite3

from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
# Chave necessária para que as mensagens (flash) e sessões funcionem
app.secret_key = os.getenv("SECRET_KEY", "projeto_ads_sucesso")
DATABASE_PATH = os.getenv("DATABASE_PATH", "database.db")


def get_db():
    conn = sqlite3.connect(DATABASE_PATH)
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()
    # Criamos a tabela com UNIQUE no username para evitar duplicatas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            username TEXT UNIQUE, 
            password TEXT
        )
    """)
    conn.commit()
    conn.close()


def is_password_hash(password_value):
    return password_value.startswith(("pbkdf2:", "scrypt:"))


def password_matches(stored_password, submitted_password):
    if not stored_password or not submitted_password:
        return False
    if is_password_hash(stored_password):
        return check_password_hash(stored_password, submitted_password)
    return stored_password == submitted_password


init_db()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user and password_matches(user[2], password):
            if not is_password_hash(user[2]):
                cursor.execute(
                    "UPDATE users SET password = ? WHERE id = ?",
                    (generate_password_hash(password), user[0]),
                )
                conn.commit()
            conn.close()
            session["usuario_logado"] = username
            flash(f"Bem-vindo, {username}!", "success")
            return redirect(url_for('dashboard'))

        conn.close()
        flash("Usuário ou senha incorretos!", "error")
        return redirect(url_for('login'))

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "usuario_logado" not in session:
        flash("Acesso negado. Faça login primeiro.", "error")
        return redirect(url_for('login'))
    
    return render_template("dashboard.html", nome_usuario=session["usuario_logado"])

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, generate_password_hash(password)),
            )
            conn.commit()
            flash("Conta criada com sucesso! Faça login.", "success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Este nome de usuário já existe!", "error")
        finally:
            conn.close()

    return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop("usuario_logado", None)
    flash("Sessão encerrada com sucesso.", "success")
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
