import json
from blockchain import Blockchain
from flask import Flask, request, abort, jsonify
import time
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

ezekial_blockchain = Blockchain()

def missing_fields(request_data, required_fields=[]):
    missing = []
    for key in required_fields:
        if key not in request_data:
            missing.append(key)
    if missing:
        abort(400,f"Missing fields: {missing}")
    return


@app.route('/transactions', methods=['POST'])

def new_transaction():
    transaction = request.get_json()
    print(f"Transaction data {transaction}")
    missing_fields(transaction, required_fields=["from_wallet", "to_wallet", "amount"])
    transaction["timestamp"] = time.time()
    ezekial_blockchain.add_new_transaction({"from_wallet": transaction['from_wallet'], "to_wallet":transaction['to_wallet'], "amount": transaction['amount'],"timestamp": transaction['timestamp']})
    return "Success", 201

@app.route('/transactions/pending', methods=['GET'])
def get_pending_transactions():
    return jsonify(ezekial_blockchain.pending_transcations), 200

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_json = []
    for block in ezekial_blockchain.chain:
        chain_json.append(block.__dict__)

    return json.dumps({"length": len(ezekial_blockchain.chain),
                       "chain": chain_json})

@app.route('/mine', methods=['POST'])
def mine_unconfirmed_transactions():
    if 'miner_id' not in request.get_json(): return "No miner id", 400
    
    miner_id = request.get_json()['miner_id']
    mined =  ezekial_blockchain.mine(miner_id) if miner_id else None
    if not mined:
        return "No transactions to mine"
    
    return f"Block #{ezekial_blockchain.last_block.index} is mined by miner {mined}"

@app.route('/miner/<id>', methods=['GET'])
def get_miner(id):
    miner = ezekial_blockchain.get_miner(id)
    if not miner:
        return f"No miner with id {id} found", 404
    return jsonify(miner.__dict__)