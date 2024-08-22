from flask import Flask, request, render_template, redirect, url_for, session, g
from functools import wraps
from dotenv import load_dotenv
import os
import mysql.connector
import threading
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')  # Usa la clave del archivo .env

# Configuración de la base de datos MySQL para SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@"
    f"{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DATABASE')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar SQLAlchemy y Flask-Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Configuración de la base de datos MySQL para conexiones manuales
DB_CONFIG = {
    'host': os.getenv('MYSQL_HOST'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DATABASE')
}

# Función para obtener la conexión a la base de datos manual
def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(**DB_CONFIG)
    return g.db

# Función para cerrar la conexión a la base de datos
@app.teardown_appcontext
def close_connection(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

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

        db = get_db()
        cur = db.cursor(dictionary=True)
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()

        if user:  # Credenciales correctas
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
    # Aquí iría la lógica para enviar seguidores
    import time
    time.sleep(2)  # Simulación de envío
    print(f"Se han enviado {count} seguidores a {tiktok_username}")

if __name__ == '__main__':
    app.run(debug=True)
