import json,time
from .block import Block
LEDGER="app/blockchain/ledger.json"
class Blockchain:
    def __init__(self):
        self.chain=[]
        self.load()
    def load(self):
        try:
            for b in json.load(open(LEDGER)):
                blk=Block(b["index"],b["timestamp"],b["data"],b["previous_hash"])
                blk.hash=b["hash"]; self.chain.append(blk)
        except:
            self.chain=[Block(0,time.time(),"Genesis","0")]
            self.save()
    def add_block(self,data):
        blk=Block(len(self.chain),time.time(),data,self.chain[-1].hash)
        self.chain.append(blk); self.save(); return blk
    def save(self):
        json.dump([b.__dict__ for b in self.chain],open(LEDGER,"w"),indent=2)