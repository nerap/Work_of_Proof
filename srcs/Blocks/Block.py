import time
from hashlib import sha256
from merkletools import MerkleTools

from srcs.Transactions.Transactions import Transactions

class Block:

    __slots__ = '_prev_block_hash', '_timestamp', '_transactions', '_nonce', '_difficulty', '_merkle_tree_root', '_index', '_hash', '_confirmations', '_fee_reward'

    def __init__(self, prev_block_hash, transactions, difficulty, index, fee_reward, timestamp=None, nonce=None, merkle_tree_root=None, confirmations=0):
        self._prev_block_hash = prev_block_hash
        self._transactions = transactions
        self._timestamp = timestamp or int(time.time())
        self._nonce = nonce
        self._difficulty = difficulty
        self._index = index
        self._fee_reward = fee_reward
        self._merkle_tree_root = merkle_tree_root
        self._confirmations = confirmations

    def merkle_tree(self):
        if self._merkle_tree_root:
            return self._merkle_tree_root
        merkle_tools = MerkleTools(hash_type='SHA256')
        for transaction in self._transactions:
            merkle_tools.add_leaf(transaction.hash)
        merkle_tools.make_tree()
        self._merkle_tree_root = merkle_tools.get_merkle_root()
        return self._merkle_tree_root

    def hash(self, nonce=None):
        if nonce:
            self._nonce = nonce
        hash_string = '{}{}{}{}{}{}{}'.format(
            self._prev_block_hash, self._timestamp, self._nonce, self._difficulty, self._index, self._fee_reward, self.merkle_tree()
        )

    @property
    def as_dict(self) -> dict:
        return {
            "_prev_block_hash" : self._prev_block_hash,
            "_transactions" : [transaction.as_dict for transaction in self._transactions],
            "_timestamp" : self._timestamp,
            "_nonce" : self._nonce,
            "_difficulty" : self._difficulty,
            "_index" : self._index,
            "_fee_reward" : self._fee_reward,
            "_merkle_tree_root" : self._merkle_tree_root,
            "_confirmations" : self._confirmations
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            data['_prev_block_hash'],
            [Transactions.from_dict(transaction) for transaction in data['_transactions']],
            data['_difficulty'],
            data['_index'],
            data['_fee_reward'],
            data['_timestamp'],
            data['_nonce'],
            data['_merkle_tree_root'],
            data['_confirmations']
        )
