import time
from hashlib import sha256

class Tx:
    __slots__ = 'inputs', 'outputs', 'timestamp', '_hash'

    def __init__(self, inputs, outputs, timestamp=None):
        self.inputs = inputs
        self.outputs = outputs
        self.timestamp = timestamp or int(time.time())
        self._hash = None

    @property
    def hash(self):
        if self._hash:
            return self._hash
        inp_hash = sha256((str([el.as_dict for el in self.inputs]) + str(self.timestamp)).encode()).hexdigest()
        for el in self.outputs:
            el.inp_hash = inp_hash
        
        hash_string = '{}{}{}'.format([el.as_dict for el in self.inputs], [el.as_dict for el in self.outputs], self.timestamp)
        self._hash = sha256(sha256(hash_string.encode()).hexdigest().encode('utf8')).hexdigest()
        return self._hash

    @property
    def as_dict(self):
        inp_hash = sha256((str([el.as_dict for el in self.inputs]) + str(self.timestamp)).encode()).hexdigest()
        for el in self.outputs:
            el.input_hash = inp_hash
        return {
            "inputs" : [el.as_dict for el in self.inputs],
            "outputs" : [el.as_dict for el in self.outputs],
            "timestamp" : self.timestamp,
            "hash" : self.hash
        }

    @classmethod
    def from_dict(cls, data):
        inps = [Inputs.from_dict(el) for el in data['inputs']]
        outs = [Output.from_dict(el) for el in data['outputs']]
        inp_hash = sha256((str([el.as_dict for el in inps]) + str(data['timestamp'])).encode()).hexdigest()
        for el in outs:
            el.inp_hash = inp_hash
        inst = cls(
            inps,
            outs,
            data['timestamp'],
        )
        inst._hash = None
        return inst