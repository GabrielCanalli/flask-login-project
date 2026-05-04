from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
# Chave secreta necessária para usar sessões
app.secret_key = "chave_muito_segura_123"

def get_db():
    conn = sqlite3.connect("database.db")
    return conn

# Se você já criou o banco, essa parte pode ser mantida como está
def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)")
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

        # 🚨 PRESTE ATENÇÃO NOS ESPAÇOS ABAIXO 🚨
        if user:
            session["usuario_logado"] = username
            return redirect(url_for('dashboard'))
        else:
            return "<h1>Erro: Usuário ou senha incorretos!</h1>"

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "usuario_logado" not in session:
        return redirect(url_for('login'))
    
    return render_template("dashboard.html", nome_usuario=session["usuario_logado"])

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()

        return redirect(url_for('login'))

    return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop("usuario_logado", None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)