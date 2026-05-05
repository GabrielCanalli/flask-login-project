from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
# Chave necessária para que as mensagens (flash) e sessões funcionem
app.secret_key = "projeto_ads_sucesso"

def get_db():
    conn = sqlite3.connect('database.db')
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

init_db()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session["usuario_logado"] = username
            flash(f"Bem-vindo, {username}!", "success")
            return redirect(url_for('dashboard'))
        else:
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
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
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