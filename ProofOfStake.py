#UAT Coding Blockchain MS582
#Matt Lindborg
#Proof of Stake (PoS), Digital Signatures,
#and Introduction to Transactions
#Assignment Week 2
#ProofOfStake.py

import hashlib
import time
import random

#Transaction Class
class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.signature = self.sign_transaction()

    #Format transaction data into a single string representation
    def to_string(self):
        return f"{self.sender} -> {self.receiver} : {self.amount}"

    # Simulated digital signature using hashing (In real world we use asymmetric crytography)
    def sign_transaction(self):
        return hashlib.sha256((self.sender + self.receiver + str(self.amount)).encode()).hexdigest()

#Block Class
class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, nonce = 0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.nonce = nonce
        self.hash = self.calculate_hash()

    #Generates hash based on block data including all transactions
    def calculate_hash(self):
        block_string = f"{self.index} {self.previous_hash} {self.timestamp} {self.transactions_string()} {self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def transactions_string(self):
        return "".join([t.to_string() for t in self.transactions])

    #proof of work mining: finding a hash that starts with "0" difficulty
    def mine_block(self, difficulty):
        while not self.hash.startswith("0" * difficulty):
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block mined: {self.hash}")

#Blockchain Class with proof of stake simulation
class Blockchain:
    def __init__(self, difficulty = 2, validators = ["Matt", "Bernard", "Michael"]):
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty
        self.validators = validators #list of validators for proof of stake

    #Create the first block in the blockchain
    def create_genesis_block(self):
        genesis_transaction = Transaction("Genesis", "Network", 0)
        return Block(0, "0", time.time(), [genesis_transaction])

    def get_latest_block(self):
        return self.chain[-1]

    #Proof of Stake: select a random validator to mine the next block
    def proof_of_stake_validator(self):
        return random.choice(self.validators)

    def add_block(self, new_block):
        validator = self.proof_of_stake_validator()
        print(f"Validator for this block: {validator}")
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            #Check if the current block's hash is valid
            if current_block.hash != current_block.calculate_hash():
                print(f"Invalid hash at block {i}")
                return False
            #Check if the current block's hash matches the previous block's hash
            if current_block.previous_hash != previous_block.hash:
                print(f"Invalid previous hash at block {i}")
                return False
        return True

#Node Class to simulate decentralization
class Node:
    def __init__(self, name):
        self.name = name
        self.blockchain = Blockchain()

    #Node receives and adds a new block to its own Blockchain
    def receive_block(self, block):
        self.blockchain.add_block(block)
        print(f"Node {self.name} received a new block with hash: {block.hash}")

#Example Usage

#Create Blockchain
node1 = Node("Node1")
node2 = Node("Node2")

#Create Transactions
transaction1 = Transaction("Rawad", "Bernard", 50)
transaction2 = Transaction("Bernard", "Matt", 10)

#Mine first block with transactions
block1 = Block(1, node1.blockchain.get_latest_block().hash, time.time(), [transaction1, transaction2])
node1.blockchain.add_block(block1)

#Simulate sending block to another node
node2.receive_block(block1)

#Check validity of the Blockchain
print("\nBlockchain validity:", node1.blockchain.is_chain_valid())

#Output Blockchain data for both nodes
for i, node in enumerate([node1, node2], start = 1):
    print(f"\nBlockchain in {node.name}:")
    for block in node.blockchain.chain:
        print(f"\nBlock {block.index}")
        print(f"Previous Hash: {block.previous_hash}")
        print(f"Hash: {block.hash}")
        print(f"Transactions: {block.transactions_string()}")
        print(f"Nonce: {block.nonce}")
