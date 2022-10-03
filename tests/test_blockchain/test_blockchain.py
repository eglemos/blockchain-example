import pytest
from blockchain_app.blockchain import Blockchain

# Arrange
@pytest.fixture
def blockchain():
    return Blockchain()

def test_create_block(blockchain):
    assert blockchain is not None
    assert isinstance(blockchain, Blockchain)
    assert isinstance(blockchain.chain, list)
    block = blockchain.create_block(2, '1')
    assert block is not None
    assert len(blockchain.chain) > 1
    assert block['proof'] == 2
    assert block['previous_hash'] == '1'

def test_retrieve_previous_block(blockchain):
    assert blockchain is not None
    block = blockchain.retrieve_previous_block()
    assert block is not None
    assert isinstance(block, dict)
    assert block['previous_hash'] == '0'

def test_proof_of_work(blockchain):
    assert blockchain is not None
    proof_of_work = blockchain.proof_of_work(0)
    assert proof_of_work is not None
    assert proof_of_work == 115558

def test_hash_block(blockchain):
    assert blockchain is not None
    hashed_block = blockchain.hash_block(blockchain.retrieve_previous_block())
    assert hashed_block is not None
    print(hashed_block)