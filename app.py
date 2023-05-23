from flask import Flask, jsonify, request
from binance.client import Client

app = Flask(__name__)
client = Client('VWwBmJjSl4Rs13CchMBk14BqvDe48DaEdEbOyP4lPqlxWURPQGtWhR8WKmwZNCIq', 'eUVBEI3rutdAn3uCwffvKG83jNrET5ldQLCao244EsE2J3U9tOgfokFgTvkxpzZM')

@app.route('/faucet', methods=['POST'])
def faucet():
    address = request.form['address']
    amount = request.form['amount']
    asset = request.form['asset']

    response = client.withdraw(
        asset=asset,
        address=address,
        amount=amount
    )

    return jsonify(response)

if __name__ == '__main__':
    app.run()
