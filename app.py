from web3 import Web3, HTTPProvider
from flask import Flask, request

# Configurar la conexión a la red Goerli
w3 = Web3(HTTPProvider('https://goerli.infura.io/v3/a4693816802c4b01bedef15ad5a2fd92'))

# Dirección de la cuenta desde la que se enviarán los fondos
faucet_address = "0xdbD9cFe329Fcb90529579Fe25282089464616CD0"

# Contraseña de la cuenta desde la que se enviarán los fondos (si se requiere)
faucet_password = "Mgnieto26-"

# Crear la aplicación Flask
app = Flask(__name__)

# Ruta para solicitar fondos
@app.route('/', methods=['POST'])
def request_funds():
    # Obtener la dirección de la cuenta a la que se enviarán los fondos desde los datos de solicitud
    data = request.get_json()
    recipient_address = data.get('address')

    # Verificar si la dirección de destino es válida
    if not w3.isAddress(recipient_address):
        return "Dirección inválida", 400

    # Verificar si la dirección de destino ya ha recibido fondos en los últimos 24 horas
    last_received_block = w3.eth.getBlockNumber() - 5760  # 5760 bloques ~ 24 horas en Goerli
    transactions = w3.eth.getTransactionsByAddress(faucet_address, last_received_block)
    for tx in transactions:
        if tx.get('to') == recipient_address:
            return "Dirección ya recibió fondos recientemente", 400

    # Enviar fondos a la dirección de destino
    try:
        transaction = {
            'from': faucet_address,
            'to': recipient_address,
            'value': w3.toWei(0.1, 'ether'),  # Monto de envío (0.1 ETH en este ejemplo)
            'gas': 21000,  # Estimación básica de gas para una transferencia
            'gasPrice': w3.toWei('5', 'gwei'),  # Precio del gas (5 gwei en este ejemplo)
        }

        # Desbloquear la cuenta del faucet (si se requiere)
        if faucet_password:
            w3.personal.unlockAccount(faucet_address, faucet_password)

        # Firmar y enviar la transacción
        signed_txn = w3.eth.account.signTransaction(transaction, private_key="YourPrivateKey")
        tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

        return f"Transacción enviada: {tx_hash.hex()}", 200
    except Exception as e:
        return f"Error al enviar la transacción: {str(e)}", 500

if __name__ == '__main__':
    app.run()
