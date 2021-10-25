from hashlib import sha256
import random
import json
from flask import Flask, request
import heapq as hq

mod=5000

priority =[(random.randint(1,10),1)]
# ,(random.randint(1,10),2),(random.randint(1,10),3)

app = Flask(__name__)

@app.route("/")
def PoEt():
    
    hq.heapify(priority)
    while(1):
        hq.heapify(priority)
        tup=hq.heappop(priority)
        time_old,node= tup
        time=(time_old%mod+random.randint(1,10)%mod)%mod
        hq.heappush(priority,(time,node))
        return json.dumps({'node_priority' : time_old,'node_id' : node})

    return json.dumps({"length": "NULL" })