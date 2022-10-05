from blockchain import Blockchain
from flask import Flask, jsonify, request
from uuid import uuid4

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

node_address = str(uuid4()).replace('-', '')


blockchain = Blockchain()

@app.route('/mine', methods = ['GET'])
def mine_block():
    previous_block = blockchain.retrieve_previous_block()
    previous_proof = previous_block['proof']
    previous_hash = blockchain.hash_block(previous_block)
    proof = blockchain.proof_of_work(previous_proof)
    block = blockchain.create_block(proof, previous_hash)
    blockchain.add_transaction(sender = node_address, receiver = 'Eduardo', amount = 1)
    response = {'message': 'Block mined', 'block': block }
    return jsonify(response), 200

@app.route('/chain', methods = ['GET'])
def retrieve_chain():
    response = {'message': 'blockchain retrieved', 'chain': blockchain.chain, 'length': blockchain.chain_length}
    return jsonify(response), 200

@app.route('/validate-chain', methods = ['GET'])
def is_valid():
    response = {'message': 'blockchain validated', 'is_valid': blockchain.is_chain_valid(blockchain.chain)}
    return jsonify(response), 200

@app.route('/add-transaction', methods = ['POST'])
def add_transaction():
    body = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']
    missing_keys = []

    for key in transaction_keys:
        if key not in body:
            missing_keys.append(key)

    if len(missing_keys) != 0:
        return {'message': f'Missing {missing_keys} values.'}

    index = blockchain.add_transaction(body['sender'], body['receiver'], body['amount'])

    return jsonify({'message': f'This transaction will be added to block {index}.'}), 201

@app.route('/connect_node', methods = ['POST'])
def connect_node():
    body = request.get_json()
    nodes = body.get('nodes')
    
    if nodes is None:
        return {'message': 'Invalid node'}, 400
    
    for node in nodes:
        blockchain.add_node(node)

    return jsonify({
        'message': 'node added into the chain',
        'nodes_amount': len(blockchain.nodes),
        'nodes': list(blockchain.nodes)
        }), 201

@app.route('/replace-chain', methods = ['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    
    if is_chain_replaced:
        response = {'message': 'Chain was resplaced by the largest one', 'chain': blockchain.chain}
    else:
        response = {'message': 'Chain is already the largest one', 'chain': blockchain.chain}
    return jsonify(response), 200

app.run()