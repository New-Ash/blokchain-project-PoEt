from hashlib import sha256
import json
import time

from flask import Flask, request
import requests

#This is similar to the app.py in server folder, comments are in that file
class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce

    def compute_hash(self):

        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()


class Blockchain:
    # difficulty of our PoW algorithm
    difficulty = 2

    def __init__(self):
        self.unconfirmed_transactions = []
        self.verified_transactions = []

    def create_genesis_block(self):

        genesis_block = Block(0, [], 0, "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.verified_transactions.append(genesis_block)

    @property
    def last_block(self):
        return self.verified_transactions[-1]

    def add_block(self, block):
        self.verified_transactions.append(block)
        return True

    def find_hash(self,block):
        block.nonce = 0

        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash

    @staticmethod
    def POW(block):

        block.nonce = 0

        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)


    def mine(self):
        if not self.unconfirmed_transactions:
            return False

        last_block = self.last_block

        new_block = Block(index=last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=self.find_hash(last_block))

        proof = self.POW(new_block)
        self.add_block(new_block)

        self.unconfirmed_transactions = []

        return True


app = Flask(__name__)
    

blockchain = Blockchain()
blockchain.create_genesis_block()
@app.route("/")
def front():
    return "<p>DB Front Page!</p>"

@app.route('/mine', methods=['GET'])
def mine_unconfirmed_transactions():
    return "All transactions"

@app.route('/add_transaction', methods=['POST'])
def new_transaction():
    transaction_data = request.get_json()
    req = ["c_name", "amount"]

    for field in req:
        if not transaction_data.get(field):
            return "Invalid transaction data", 404

    transaction_data["timestamp"] = time.time()

    blockchain.add_new_transaction(transaction_data)
    time.sleep(2)
    blockchain.mine()
    return "Transaction has been added", 201

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.verified_transactions:
        chain_data.append(block.__dict__)
    return json.dumps({"length": len(chain_data),
                       "chain": chain_data})







