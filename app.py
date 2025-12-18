from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecreto123'

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

init_db()

def get_user(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()
    return user

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/servicios')
def servicios():
    return render_template('servicios.html')

@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

@app.route('/portafolio')
def portafolio():
    return render_template('portafolio.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        role = request.form['role']

        try:
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                      (username, password, role))
            conn.commit()
            conn.close()
            flash('Usuario registrado con éxito', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('El nombre de usuario ya existe', 'danger')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user(username)
        if user and check_password_hash(user[2], password):
            session['username'] = user[1]
            session['role'] = user[3]
            flash('Has iniciado sesión correctamente', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    return render_template('login.html')

@app.route('/reserva')
def reserva():
    if 'username' not in session:
        flash('Debes iniciar sesión para reservar', 'warning')
        return redirect(url_for('login'))
    return f"¡Bienvenido {session['username']}! Aquí puedes reservar recursos."

@app.route('/admin')
def admin():
    if 'role' in session and session['role'] == 'admin':
        return "Bienvenido administrador. Aquí puedes gestionar usuarios y reservas."
    else:
        flash('Acceso denegado: Solo administradores', 'danger')
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)