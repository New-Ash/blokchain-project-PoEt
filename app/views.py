import datetime
import json

import requests
from flask import render_template, redirect, request
import random
from app import app
import time


# CONNECTED_NODE_ADDRESS = "http://127.0.0.1:500{}".format(nodeno)
get_node = "http://127.0.0.1:8000"
response = requests.get(get_node)
rsp=(json.loads(response.content))['node_id']
CONNECTED_NODE_ADDRESS="http://127.0.0.1:500{}".format(rsp)
GLOBAL_ADD="http://127.0.0.1:5004"
posts = []


def fetch_posts():
    
    get_chain_address = "{}/chain".format("http://127.0.0.1:5004")
    response = requests.get(get_chain_address)
    if response.status_code == 200:
        content = []
        chain = json.loads(response.content)
        for block in chain["chain"]:
            for tx in block["transactions"]:
                tx["index"] = block["index"]
                tx["hash"] = block["previous_hash"]
                content.append(tx)

        global posts
        posts = sorted(content, key=lambda k: k['timestamp'],
                       reverse=True)


@app.route('/')
def index():
    response = requests.get(get_node)
    rsp=(json.loads(response.content))['node_id']
    CONNECTED_NODE_ADDRESS="http://127.0.0.1:500{}".format(rsp)
    fetch_posts()
    return render_template('index.html',title="Dexter's Blockchain",posts=posts,node_address=CONNECTED_NODE_ADDRESS,readable_time=timestamp_to_string)


@app.route('/submit', methods=['POST'])
def submit_textarea():
    amount = request.form["content"]
    author = request.form["author"]

    # i=0
    # n=len(amount)
    # while i<n:
    #     if amount[i]=='.':
    #         i+=1
    #         continue
    #     if (amount[i]>'9' or amount[i]<'0'):
    #         print("Enter an numerical value for amount :")
    #         amount=input().strip()
    #         i=0
    #         n=len(amount)
    #         continue
    #     i+=1

    post_object = {
        'author': author,
        'content': amount,
    }
    response = requests.get(get_node)
    rsp=(json.loads(response.content))['node_id']
    CONNECTED_NODE_ADDRESS="http://127.0.0.1:500{}".format(rsp)

    # time.sleep(1)
    # Submit a transaction
    new_tx_address = "{}/new_transaction".format(CONNECTED_NODE_ADDRESS)
    requests.post(new_tx_address,
                  json=post_object,
                  headers={'Content-type': 'application/json'})

    # requests.post("http://127.0.0.1:5001"+"/new_transaction",
    #             json=post_object,
    #             headers={'Content-type': 'application/json'})




    return redirect('/')


def timestamp_to_string(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time).strftime('%H:%M')
