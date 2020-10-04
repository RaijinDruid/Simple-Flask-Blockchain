import hashlib
import json
import datetime
import time

class Block:
    """ 
    A class to represent a block

        Attributes
        ----------------------
            time_stamp: datetime
                time of instantiation
            transactions: 
                a list of transactions
            previous_hash: str
                hash key of the previous block
            index: int
                unique ID
            nonce: int
                incremented to change the hash until meeting conditions set by proof of work
        Methods
        --------------------
    """

    def __init__(self, transactions, index, previous_hash='', nonce=0,):
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.index = index
        self.nonce = nonce

    def calculate_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True) 
        return hashlib.sha256(block_string.encode()).hexdigest()
     
    def __repr__(self):
        return f"\n    index: {self.index}\n    timestamp: {str(self.timestamp)}\n    transactions: {self.transactions}\n    hash: {self.hash}\n previous_hash: {self.previous_hash}"
    def __str__(self):
        return f"\n    index: {self.index}\n    timestamp: {str(self.timestamp)}\n    transactions: {self.transactions}\n previous_hash: {self.previous_hash}"
    