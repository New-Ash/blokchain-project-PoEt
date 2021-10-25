from hashlib import sha256
import json
import time

from flask import Flask, request
import requests


class Block:

    #Block constructor
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce


    #method to find the hash of the block
    def compute_hash(self):

        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()


class Blockchain:
    # difficulty of our PoW algorithm
    difficulty = 2

    def __init__(self):
        self.unconfirmed_transactions = []  #initially all the transactions get added into this array
        self.verified_transactions = []    #after a node verify, the transactions get added over here

    def create_genesis_block(self):
                                                            #function to create genesis block of the blockchain 
        genesis_block = Block(0, [], 0, "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.verified_transactions.append(genesis_block)   #adding it directly into the verified transactions

    @property
    def last_block(self):
        return self.verified_transactions[-1]

    def add_block(self, block, proof):

        previous_hash = self.last_block.hash             #rechecking with previous hash

        if previous_hash != block.previous_hash:
            return False

        if not Blockchain.is_valid(block, proof):
            return False

        block.hash = proof
        self.verified_transactions.append(block)
        return True

    @staticmethod
    def POW(block):                          #function from A1 to find the nonce value
        block.nonce = 0

        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)         #initially adding the transaction to the pool of unverifed transactions.

    @classmethod
    def is_valid(cls, block, block_hash):

        return (block_hash.startswith('0' * Blockchain.difficulty) and    #checking if the hash value is valid or not
                block_hash == block.compute_hash())



    def mine(self):
        if not self.unconfirmed_transactions:
            return False
        last_block = self.last_block
        new_block = Block(index=last_block.index + 1,transactions=self.unconfirmed_transactions,timestamp=time.time(),previous_hash=last_block.hash)
        proof = self.POW(new_block)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = []
        return True  


app = Flask(__name__)
    

blockchain = Blockchain()
blockchain.create_genesis_block()

@app.route("/")
def front():
    return "<p>Miner Front Page!</p>"

@app.route('/add_transaction', methods=['POST'])
def new_transaction():
    transaction_data = request.get_json()
    req = ["c_name", "amount"]

    for field in req:
        if not transaction_data.get(field):
            return "Invalid transaction data", 404

    transaction_data["timestamp"] = time.time()
    requests.post("http://127.0.0.1:5004/add_transaction",
                  json=transaction_data,
                  headers={'Content-type': 'application/json'})

    blockchain.add_new_transaction(transaction_data)

    return "Added", 201

#adding the block
@app.route('/add_block', methods=['POST'])
def add_block_sever():
    block_data = request.get_json()
    block = Block(block_data["index"],block_data["transactions"],block_data["timestamp"],block_data["previous_hash"],block_data["nonce"])
    proof = block_data['hash']
    added = blockchain.add_block(block, proof)
    if not added:
        return "The block was discarded by the node", 400

    return "Block added to the chain", 201


#displays the blockchain with all the details
@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.verified_transactions:
        chain_data.append(block.__dict__)
    return json.dumps({"length": len(chain_data),"chain": chain_data})

#mining the block
@app.route('/mine', methods=['GET'])
def mine_unconfirmed_transactions():
    result = blockchain.mine()
    return "Block has been mined"








