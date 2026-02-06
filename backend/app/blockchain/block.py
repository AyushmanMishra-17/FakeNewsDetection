import hashlib, json
class Block:
    def __init__(self,i,t,d,p):
        self.index=i; self.timestamp=t; self.data=d; self.previous_hash=p
        self.hash=self.calculate_hash()
    def calculate_hash(self):
        return hashlib.sha256(json.dumps(self.__dict__,sort_keys=True).encode()).hexdigest()