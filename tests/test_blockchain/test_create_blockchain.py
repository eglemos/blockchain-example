import pytest
from blockchain_app.blockchain import Blockchain

# Arrange
@pytest.fixture
def blockchain():
    return Blockchain()

def test_create_blockchain(blockchain):
    assert blockchain != None 
    assert isinstance(blockchain, Blockchain)
    assert isinstance(blockchain.chain, list)
    assert blockchain.create_block() != None