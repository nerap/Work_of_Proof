from hashlib import sha256
from ..wallet import Wallet

class Input:
    __slots__ = 'prev_tx_hash', 'output_index', 'signature', '_hash', 'address', 'index', 'amount'

    def __init__(self, prev_tx_hash, output_index, address, index=0):
        self.prev_tx_hash = prev_tx_hash
        self.output_index = output_index
        self.address = address
        self.index = 0
        self._hash = None
        self.signature = None
        self.amount = None

    def sign(self, wallet):
        hash_string = '{}{}{}{}'.format(self.prev_tx_hash, self.output_index, self.address, self.index).encode()
        self.signature = wallet.sign(hash_string)

    @property
    def hash(self):
        if self._hash:
            return self._hash
        if not self.signature and self.prev_tx_hash != 'COINBASE':
            raise Exception('Sign the first input first')
        hash_string = '{}{}{}{}'.format(self.prev_tx_hash, self.output_index, self.address, self.signature, self.index)
        self._hash = sha256(sha256(hash_string.encode()).hexdigest().encode('utf8')).hexdigest()
        return self._hash

    @property
    def as_dict(self):
        return {
            "prev_tx_hash" : self.prev_tx_hash,
            "output_index" : self.output_index,
            "address" : str(self.address),
            "index" : self.index,
            "hash" : self.hash,
            "signature" : self.signature
        }

    @classmethod
    def from_dict(cls, data):
        inst = cls(
            data['prev_tx_hash'],
            data['output_index'],
            Address(data['address']),
            data['index'],
        )
        inst.signature = data['signature']
        inst._hash = None
        return inst