import datetime
import json

import requests
from flask import render_template, redirect, request
import random
from app import app
import time



#Requesting for the node chosen by PoEt
get_node = "http://127.0.0.1:8000"
response = requests.get(get_node)
rsp=(json.loads(response.content))['node_id']
CONNECTED_NODE_ADDRESS="http://127.0.0.1:500{}".format(rsp)
GLOBAL_ADD="http://127.0.0.1:5004"
transaction_array = []


def get_posts():
    
    get_chain_address = "{}/chain".format("http://127.0.0.1:5004")  #Database
    response = requests.get(get_chain_address)
    if response.status_code == 200:
        content = []
        chain = json.loads(response.content)
        for block in chain["chain"]:
            for transaction in block["transactions"]:
                transaction["index"] = block["index"]
                transaction["hash"] = block["previous_hash"]
                content.append(transaction)
        global transaction_array   #making the array global to use it in other functions as well
        transaction_array = sorted(content, key=lambda k: k['timestamp'],
                       reverse=True)


@app.route('/')
def index():
    response = requests.get(get_node)
    rsp=(json.loads(response.content))['node_id']
    CONNECTED_NODE_ADDRESS="http://127.0.0.1:500{}".format(rsp)
    get_posts()
    return render_template('index.html',title="Dexter's Blockchain",posts=transaction_array,node_address=CONNECTED_NODE_ADDRESS,readable_time=timestamp_to_string)

@app.route('/invalid')
def invalid():
   
    return "Enter an valid number for amount"

@app.route('/submit', methods=['POST'])
def submit_textarea():
    amount = request.form["amount"]
    c_name = request.form["c_name"]


    #Checking the format of amount entered is valid or not
    i=0
    n=len(amount)
    while i<n:
        if amount[i]=='.':
            i+=1
            continue
        if (amount[i]>'9' or amount[i]<'0'):
            #redirecting if the format of amount entered is incorrect.
            return redirect('/invalid')
        i+=1

    post_object = {
        'c_name': c_name,
        'amount': amount,
    }

    #retrieving the node given by PoEt
    response = requests.get(get_node)
    rsp=(json.loads(response.content))['node_id']
    CONNECTED_NODE_ADDRESS="http://127.0.0.1:500{}".format(rsp)

    new_tx_address = "{}/add_transaction".format(CONNECTED_NODE_ADDRESS)
    requests.post(new_tx_address,
                  json=post_object,
                  headers={'Content-type': 'application/json'})

    return redirect('/')


def timestamp_to_string(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time).strftime('%H:%M')
