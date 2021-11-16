from hashlib import sha256

class Output:

    __slots__ = '_hash', '_address', '_index', '_amount', '_input_hash'

    def __init__(self, address, amount, index=0) -> None:
        self._address = address
        self._amount = int(amount)
        self._index = index
        self._input_hash = None
        self._hash = None

    @property
    def hash(self):
        if self._hash:
            return self._hash
        hash_string = '{}{}{}{}'.format(self._amount, self._index, self._address, self._input_hash)
        self._hash = sha256(sha256(hash_string.encode()).hexdigest().encode('utf8')).hexdigest()
        return self._hash

    @property
    def as_dict(self):
        return {
            '_amount' : int(self._amount),
            '_address' : self._address,
            '_index' : self._index,
            '_input_hash' : self._input_hash,
            '_hash' : self.hash
        }

    @classmethod
    def from_dict(cls, data):
        inst = cls(
            data['_address'],
            data['_amount'],
            data['_index'],
        )
        inst._input_hash = data['_input_hash']
        inst._hash = None
        return inst