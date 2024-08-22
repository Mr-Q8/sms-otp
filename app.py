from flask import Flask, request, render_template, redirect, url_for, session
from functools import wraps
from datetime import datetime
import threading

app = Flask(__name__)
app.secret_key = 'my_secret_key'

# Simulación de usuarios en lugar de base de datos
users = {
    'dmorales': 'dmorales1'  # Usuario: contraseña
}

# Ruta para la página de inicio
@app.route('/')
def index():
    return redirect(url_for('login'))

# Autenticación simple
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Verificar las credenciales en el diccionario de usuarios
        if username in users and users[username] == password:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Credenciales incorrectas')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        tiktok_username = request.form.get('tiktok_username')
        followers_option = int(request.form.get('followers_option'))

        username = session['username']
        today = datetime.today().date()

        if 'followers_sent_today' not in session:
            session['followers_sent_today'] = {}

        if username not in session['followers_sent_today']:
            session['followers_sent_today'][username] = {'date': today, 'followers': 0}

        if session['followers_sent_today'][username]['date'] != today:
            session['followers_sent_today'][username] = {'date': today, 'followers': 0}

        if session['followers_sent_today'][username]['followers'] + followers_option > 2000:
            return render_template('dashboard.html', error="Límite diario alcanzado. Máximo 2000 seguidores por día.")

        session['followers_sent_today'][username]['followers'] += followers_option

        thread = threading.Thread(target=send_followers, args=(tiktok_username, followers_option))
        thread.start()

        return render_template('dashboard.html', success=True, tiktok_username=tiktok_username, followers_option=followers_option)

    return render_template('dashboard.html')

def send_followers(tiktok_username, count):
    # Simulación de envío de seguidores
    import time
    time.sleep(2)
    print(f"Se han enviado {count} seguidores a {tiktok_username}")

if __name__ == '__main__':
    app.run(debug=True)
