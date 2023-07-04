import redis

# Configurar la conexión a Redis
redis_client = redis.Redis(host='redis://red-cihqq559aq012evkgnkg', port=6379, db=0)

@app.route('/')
def index():
    # Obtener el valor actual del contador desde Redis
    contador = redis_client.get('contador')
    if contador is None:
        contador = 86400  # Valor predeterminado de 24 horas en segundos
    else:
        contador = int(contador)

    # Renderizar el template con el contador
    return render_template('index.html', contador=contador)

@app.route('/decrementar')
def decrementar():
    # Obtener el valor actual del contador desde Redis
    contador = redis_client.get('contador')
    if contador is None:
        contador = 86400  # Valor predeterminado de 24 horas en segundos
    else:
        contador = int(contador)

    # Decrementar el contador en 1
    contador -= 1

    # Actualizar el contador en Redis
    redis_client.set('contador', contador)

    # Renderizar el template con el contador actualizado
    return render_template('index.html', contador=contador)


