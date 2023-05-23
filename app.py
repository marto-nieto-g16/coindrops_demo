# app.py
from flask import Flask, render_template, request, jsonify
from coinbase.wallet.client import Client
import redis
import time

app = Flask(__name__)
redis_db = redis.Redis()

API_KEY = 'uBT2LzeEiRZ0iMn7'
API_SECRET = 'lUlwoziJzYqpSo9jS8tf5IStJpZ0Fdvq'
client = Client(API_KEY, API_SECRET)

FAUCET_AMOUNT = 0.011  # Cantidad de criptomonedas que se distribuirán en cada reclamo
CLAIM_INTERVAL = 42 * 60 * 60  # Intervalo de tiempo en segundos entre reclamos (42 horas)

# Configura la conexión a Redis
redis_host = 'redis://red-chlotgu7avj217fvm180'
redis_port = 6379
redis_db = 0
redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sponsorship')
def sponsorship():
    return render_template('sponsorship.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/claim', methods=['POST'])
def claim():
    user_address = request.form.get('address')
    last_claim_time = redis_db.get(user_address)

    if last_claim_time:
        time_since_last_claim = time.time() - float(last_claim_time)
        if time_since_last_claim < CLAIM_INTERVAL:
            return jsonify({'message': f'Puedes reclamar nuevamente en {CLAIM_INTERVAL - time_since_last_claim:.0f} segundos.'})

    try:
        # Enviamos la criptomoneda utilizando la API de Coinbase
        response = client.send_money(user_address, FAUCET_AMOUNT, 'SHIB', description='Reclamo de Faucet')

        # Verificamos si la transacción se realizó con éxito
        if response and response.status == 'completed':
            # Registramos el tiempo del último reclamo exitoso
            redis_db.set(user_address, time.time())
            return jsonify({'message': f'Reclamaste {FAUCET_AMOUNT} SHIB exitosamente.'})
        else:
            return jsonify({'message': 'Error al enviar la criptomoneda.'})
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)
