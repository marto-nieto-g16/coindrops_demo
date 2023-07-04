from flask import Flask, render_template
import sqlite3
import threading

app = Flask(__name__)
contador = 86400  # 24 horas en segundos
contador_activo = False  # Indica si la cuenta regresiva está activa
lock = threading.Lock()  # Bloqueo para asegurar operaciones atómicas

def decrementar_contador():
    global contador, contador_activo

    while contador > 0:
        with lock:
            if not contador_activo:
                break

            contador -= 1

        # Esperar 1 segundo
        threading.Event().wait(1)

    contador_activo = False

@app.route('/')
def index():
    # Conectar a la base de datos
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Obtener el valor actual del contador
    cursor.execute('SELECT valor FROM contador WHERE id = 1')
    contador = cursor.fetchone()[0]

    # Cerrar la conexión
    conn.close()

    # Renderizar el template con el contador
    return render_template('index.html', contador=contador)

@app.route('/decrementar')
def decrementar():
    global contador, contador_activo

    # Iniciar la cuenta regresiva si no está activa
    if not contador_activo:
        contador_activo = True
        threading.Thread(target=decrementar_contador).start()

    # Renderizar el template con el contador actualizado
    return render_template('index.html', contador=contador)

if __name__ == '__main__':
    app.run()
