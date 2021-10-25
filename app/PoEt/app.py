from hashlib import sha256
import random
import json
from flask import Flask, request
import heapq as hq

mod=5003

#Idea : Maintaining a priority queue parameterized on time. Alloting random waiting times for the nodes and selecting the node whose cooldown 
# (waiting time) is lowest for mining the node. Once the node mines the block , it is  again alloted some random waiting time and pushed back 
# into the priority

#considering  3 nodes in the system
priority =[(random.randint(1,10),1),(random.randint(1,10),2),(random.randint(1,10),3)]


app = Flask(__name__)

@app.route("/")
def PoEt():
    
    hq.heapify(priority)
    while(1):
        hq.heapify(priority)
        tup=hq.heappop(priority)  #retrieving the yop element in the priority queue
        time_old,node= tup
        time=(time_old%mod+random.randint(5,10)%mod)%mod    #avoiding overflow
        hq.heappush(priority,(time,node))  #pushing the node back with modified waiting time
        return json.dumps({'node_priority' : time_old,'node_id' : node})

    return json.dumps({"length": "NULL" })