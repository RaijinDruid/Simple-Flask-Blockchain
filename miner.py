class Miner:
    def __init__(self, id):
        self.id = id
        self.wallet = {"address": '', "coins": 0}
    
    def __repr__(self):
        return f"Miner Id: {self.id}, Wallet: {self.wallet}"
    