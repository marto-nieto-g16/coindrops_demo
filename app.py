from flask import Flask, request
from web3 import Web3

app = Flask(__name__)
web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/a4693816802c4b01bedef15ad5a2fd92'))
private_key = 'a4693816802c4b01bedef15ad5a2fd92'
address = '0xdbD9cFe329Fcb90529579Fe25282089464616CD0'

def send_ether(to_address, amount):
    nonce = web3.eth.getTransactionCount(address)
    gas_price = web3.eth.gasPrice
    value = web3.toWei(amount, 'ether')

    transaction = {
        'nonce': nonce,
        'to': to_address,
        'value': value,
        'gas': 21000,
        'gasPrice': gas_price,
    }

    signed_txn = web3.eth.account.signTransaction(transaction, private_key)
    tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    return receipt

@app.route('/faucet', methods=['POST'])
def faucet():
    to_address = request.form.get('address')
    amount = request.form.get('amount')

    if to_address and amount:
        try:
            send_ether(to_address, float(amount))
            return 'Ether sent successfully!'
        except Exception as e:
            return str(e)
    else:
        return 'Invalid request'

if __name__ == '__main__':
    app.run()
