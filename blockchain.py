from block import Block
from miner import Miner
import uuid
import datetime
import time

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.reward_amount = 5
        self.difficulty_level = 5
        self.pending_transcations = []
        self.transactions = []
        self.miners = {}


    def create_genesis_block(self):
        """ Creates the genesis block (first block) of the block chain

        Returns:
            Block: newly created genesis block with the hash value computer
        """
        gen_block = Block([],0, '')
        gen_block.hash = gen_block.calculate_hash()
        return gen_block

    def append_new_block(self, block, proof_hash):
        prev = self.last_block.hash
        if prev != block.previous_hash:
            return False
        if not self.proof_is_valid(block, proof_hash):
            return False
        
        block.hash = proof_hash
        self.chain.append(block)
        return True

    @property
    def last_block(self):
        return self.chain[-1]

    def get_miner(self,id):
        miner = None
        if id in self.miners:
            miner = self.miners[id]
        return miner

    def add_miner(self):
        miner_id = str(uuid.uuid4())

        # make sure miner_id is unique, keep generating new uuid until so
        while miner_id in self.miners:
            miner_id = str(uuid.uuid4())

        new_miner = Miner(id=miner_id)
        self.miners[miner_id] = new_miner
        return new_miner

    def mine(self, id):
        """
            Add the pending transactions to the blockchain by adding them to a 
            block once the proof of work has been completed.
        """
        if not self.pending_transcations:
            return False

        last_block = self.last_block

        new_block = Block(self.pending_transcations, last_block.index + 1, last_block.hash)
        proof_of_work = self.proof_of_work(new_block)
        added_block = self.append_new_block(new_block, proof_of_work)
        self.pending_transcations = []
        
        reward_miner = self.get_miner(id)
        if not reward_miner:
            reward_miner = self.add_miner()

        reward_miner.wallet['coins'] += self.reward_amount

        print(f"Congratulations you sucessfully mined {self.reward_amount} Ezekial Coins")
        return reward_miner

    def proof_of_work(self,block):
        """
        Function that tries different values of nonce to get a hash that meets our diffculty criteria.
        Difficulty criteria following hashcash is if a hash starts with N leading 0's, where N difficulty
        """
        print(block)
        block_hash = block.calculate_hash()

        while not block_hash.startswith('0' * self.difficulty_level):
            block.nonce += 1
            block_hash = block.calculate_hash()
        return block_hash

    def proof_is_valid(self, block, proof_hash):
        """ 
        Check that the hash produced by the proof is the same as the block computed hash
        and that the proof hash meets the confition of our difficulty requirement
        """
        return (proof_hash == block.calculate_hash() and proof_hash.startswith('0' * self.difficulty_level))

    def check_chain_validity(self):
        """
        Go through each block in the chain, recompute the hash and check it contains the valid proof of work. 
        Also comparing against original that they match. Also checking that
        """
        previous_hash = ""

        for block in self.chain:
            block_hash = block.hash
            del block.hash

            if not self.is_valid_proof(block, block_hash) or previous_hash != block.previous_hash:
                return False

            block.hash, previous_hash = block_hash, block_hash

        return True

    def add_new_transaction(self,transaction):
        self.pending_transcations.append(transaction)

    def __str__(self):
        return f"{self.chain}"
