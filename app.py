# main.py
from flask import Flask, render_template, redirect, request, session
from flask_login import LoginManager, login_required, login_user, logout_user, UserMixin
import redis
import schedule
import time

app = Flask(__name__)
app.secret_key = b'\xfc^\xa0\x97\xef\x91%\x96\xf4c!j\x15\x84Dh\x0f\xfee\xe0s()\x8a'

# Configuración de Redis
redis_db = redis.from_url("redis://red-cihqq559aq012evkgnkg:6379")

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Clase de Usuario
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Rutas
@app.route('/')
@login_required
def index():
    user_id = session['user_id']
    username = redis_db.hget(user_id, 'username')
    tokens = redis_db.hget(user_id, 'tokens')
    return render_template('index.html', username=username, tokens=tokens)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_id = redis_db.incr('user_count')
        redis_db.hset(user_id, 'username', username)
        redis_db.hset(user_id, 'password', password)
        redis_db.hset(user_id, 'tokens', 0)
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_id = get_user_id(username)
        if user_id is not None and redis_db.hget(user_id, 'password') == password:
            user = User(user_id)
            login_user(user)
            session['user_id'] = user_id
            return redirect('/')
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

# Funciones auxiliares
def get_user_id(username):
    user_count = int(redis_db.get('user_count') or 0)
    for user_id in range(1, user_count + 1):
        if redis_db.hget(user_id, 'username') == username:
            return user_id
    return None

def reward_tokens():
    user_count = int(redis_db.get('user_count') or 0)
    for user_id in range(1, user_count + 1):
        tokens = int(redis_db.hget(user_id, 'tokens') or 0)
        tokens += 20
        redis_db.hset(user_id, 'tokens', tokens)

# Programar la recompensa cada 24 horas
schedule.every(24).hours.do(reward_tokens)

# Ejecutar la tarea en segundo plano
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    # Iniciar la tarea en segundo plano
    import threading
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()
    
    app.run()
