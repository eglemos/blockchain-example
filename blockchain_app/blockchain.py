import hashlib
import json
import requests
from datetime import datetime
from urllib.parse import urlparse

from blockchain_app.app import is_valid

class Blockchain:
    
    def __init__(self):
        self._chain = []
        self.transactions = []
        self.create_block(1, '0')
        self.nodes = set()

    def create_block(self, proof: int, previous_hash : str):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.utcnow()),
            'proof': proof,
            'previous_hash': previous_hash,
            'transactions': self.transactions
        }
        self.transactions = []
        self.chain.append(block)
        return block

    def retrieve_previous_block(self):
        return self.chain[-1]

    def hash_operation(self, new_proof, previous_proof):
        return hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        
        while check_proof is False:
            hash_operation = self.hash_operation(new_proof, previous_proof)
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1

        return new_proof

    def hash_block(self, block):
        hashed_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(hashed_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            
            if block['previous_hash'] != self.hash_block(previous_block):
                return False
            
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_result = self.hash_operation(proof, previous_proof)

            if hash_result[:4] != '0000':
                return False

            previous_block = block
            block_index += 1
            
        return True

    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        })
        previous_block = self.retrieve_previous_block()
        return previous_block['index'] + 1

    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)


    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/chain')
            response_body = response.json()
            if response.status_code == 200:
                length = response_body['length']
                chain = response_body['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length  = length
                    longest_chain = chain
        
        if longest_chain:
            self.chain = longest_chain
            return True
        return False



    @property
    def chain(self):
        return self._chain

    @property
    def chain_length(self):
        return len(self._chain)