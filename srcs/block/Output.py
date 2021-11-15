from hashlib import sha256
from ..wallet import Wallet

class Output:
    __slots__ = '_hash', 'address', 'index', 'amount', 'input_hash'

    def __init__(self, address, amount, index=0):
        self.address = address
        self.index = 0
        self.amount = int(amount)

        self.input_hash = None
        self._hash = None

    @property
    def hash(self):
        if self._hash:
            return self._hash
        hash_string = '{}{}{}{}'.format(self.amount, self.index, self.address, self.input_hash)
        self._hash = sha256(sha256(hash_string.encode()).hexdigest().encode('utf8')).hexdigest()
        return self._hash

    @property
    def as_dict(self):
        return {
            "amount" : int(self.amount),
            "address" : str(self.address),
            "index" : self.index,
            "input_hash" : self.input_hash,
            "hash" : self.hash
        }
    
    @classmethod
    def from_dict(cls, data):
        inst = cls(
            Address(data['address']),
            data['amount'],
            data['index'],
        )
        inst.input_hash = data['input_hash']
        inst._hash = None
        return inst