#UAT Coding Blockchain MS582
#Matt Lindborg
#Blockchain Structure & Genesis Block
#Hashing & Consensus Protocol
#Assignment Week 2
#Blockchain.py

import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, data, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{self.data}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        while not self.hash.startswith("0" * difficulty):
            self.nonce += 1
            self.hash = self.calculate_hash()
            print(f"Block mined: {self.hash}")

class Blockchain:
    def __init__(self, difficulty = 2):
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty

    def create_genesis_block(self):
        return Block(0, "0", time.time(), "Genesis Block")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            if current_block.hash != current_block.calculate_hash():
                print(f"Invalid hash at block {i}")
                return False
            if current_block.previous_hash != previous_block.hash:
                print(f"Invalid previous hash at block {i}")
                return False
        return True

my_blockchain = Blockchain()
print("Mining block 1")
my_blockchain.add_block(Block(1, "", time.time(), "Block 1 Data"))
print("Mining block 2")
my_blockchain.add_block(Block(2, "", time.time(), "Block 2 Data"))
print("Mining block 3")
my_blockchain.add_block(Block(3, "", time.time(), "Block 3 Data"))
print("\nBlockchain Validity: ", my_blockchain.is_chain_valid())

for block in my_blockchain.chain:
    print(f"\nBlock {block.index}")
    print(f"Previous_Hash: {block.previous_hash}")
    print(f"Hash: {block.hash}")
    print(f"Data: {block.data}")
    print(f"Nonce: {block.nonce}")
    print(f"Timestamp: {block.timestamp}")
