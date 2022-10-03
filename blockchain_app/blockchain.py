import hashlib
import json
from datetime import datetime
from re import L

class Blockchain:
    
    def __init__(self):
        self._chain = []
        self.create_block(1, '0')

    def create_block(self, proof: int, previous_hash : str):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.utcnow()),
            'proof': proof,
            'previous_hash': previous_hash
        }
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


    @property
    def chain(self):
        return self._chain

    @property
    def chain_length(self):
        return len(self._chain)