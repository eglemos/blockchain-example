import datetime
import hashlib
import json
from re import L
from flask import Flask, jsonify

class Blockchain:
    
    def __init__(self):
        self._chain = []
        
    def create_block(self, proof: int = 1, previous_hash : str = '0'):
        return 

    @property
    def chain(self):
        return self._chain