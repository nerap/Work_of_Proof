import time
from hashlib import sha256
from merkletools import MerkleTools

class Block:
    __slots__ = 'nonce', 'prev_hash', 'index', 'txs', 'timestamp', 'merkel_root'

    def __init__(self, txs, index, prev_hash, timestamp=None, nonce=0):
        self.txs = txs or []
        self.prev_hash = prev_hash
        self.index = index
        self.nonce = nonce
        self.timestamp = timestamp or int(time.time())
        self.merkel_root = None
    
    def build_merkel_tree(self):
        if self.merkel_root:
            return self.merkel_root
        mt = MerkleTools(hash_type='SHA256')
        for el in self.txs:
            mt.add_leaf(el.hash)
        mt.make_tree()
        self.merkel_root = mt.get_merkle_root()
        return self.merkel_root

    def hash(self, nonce=None):
        if nonce:
            self.nonce = nonce
        block_string = '{}{}{}{}{}'.format(self.build_merkel_tree(), self.prev_hash, self.index, self.nonce, self.timestamp)
        return sha256(sha256(block_string.encode()).hexdigest().encode('utf8')).hexdigest()

    @property
    def as_dict(self):
        return {
            "index" : self.index,
            "timestamp" : self.timestamp,
            "prev_hash" : self.prev_hash,
            "hash" : self.hash(),
            "txs" : [el.as_dict for el in self.txs],
            "nonce" : self.nonce,
            "merkel_root" : self.merkel_root
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            [Tx.from_dict(el) for el in data['txs']],
            data['index'],
            data['prev_hash'],
            data['timestamp'],
            data['nonce']
        )