from flask import Flask, jsonify
from blockchain import Blockchain

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

blockchain = Blockchain()

@app.route('/mine', methods = ['GET'])
def mine_block():
    previous_block = blockchain.retrieve_previous_block()
    previous_proof = previous_block['proof']
    previous_hash = blockchain.hash_block(previous_block)
    proof = blockchain.proof_of_work(previous_proof)
    block = blockchain.create_block(proof, previous_hash)
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


app.run()