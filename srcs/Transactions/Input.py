from hashlib import sha256

class Input:

    __slots__ = '_prev_transaction_hash', '_output_index', '_signature', '_hash', '_address', '_index', '_amount'

    def __init__(self, prev_transaction_hash, output_index, address, index=0) -> None:
        self._prev_transaction_hash = prev_transaction_hash
        self._output_index = output_index
        self._address = address
        self._index = index
        self._hash = None
        self._signature = None
        self._amount = None

    def sign(self, wallet):
        hash_string = '{}{}{}{}'.format(self._prev_transaction_hash, self._output_index, self._address, self._index).encode()
        self._signature = wallet.sign(hash_string)

    @property
    def hash(self):
        if self._hash:
            return self._hash
        if not self._signature and self._prev_transaction_hash != 'COINBASE':
            raise Exception('Sign the first input')
        hash_string = '{}{}{}{}'.format(self._prev_transaction_hash, self._output_index, self._address, self._signature, self._index)
        self._hash = sha256(sha256(hash_string.encode()).hexdigest().encode('utf8')).hexdigest()
        return self._hash

    @property
    def as_dict(self):
        print("hello")
        print(self._signature)
        return {
            "_prev_transaction_hash" : self._prev_transaction_hash,
            "_output_index" : self._output_index,
            "_address" : self._address,
            "_index" : self._index,
            "_hash" : self.hash,
            "_signature" : self._signature
        }

    @classmethod
    def from_dict(cls, data):
        inst = cls(
            data['_prev_transaction_hash'],
            data['_output_index'],
            data['_address'],
            data['_index'],
        )
        inst._signature = data['_signature']
        inst._hash = None
        return inst