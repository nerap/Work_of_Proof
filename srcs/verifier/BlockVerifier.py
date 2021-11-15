from .TxVerifier import TxVerifier
from .exception import BlockVerificationFailed
from .exception import BlockOutOfChain

class BlockVerifier:
    def __init__(self, db):
        self.db = db
        self.tv = TxVerifier(db)
    
    def verify(self, head, block):
        total_block_reward = int(self.db.config['mining_reward'])

        if int(block.hash(), 16) > (2 ** (256 - self.db.config['difficulty'])):
            raise BlockVerificationFailed('Block hash bigger than target difficulty')

        for tx in block.txs[1:]:
            fee = self.tv.verify(tx.inputs, tx.outputs)
            total_block_reward += fee

        total_reward_out = 0
        for out in block.txs[0].outputs:
            total_reward_out += out.amount

        if total_block_reward != total_reward_out:
            raise BlockVerificationFailed('Wrong reward sum')

        if head:
            if head.index >= block.index:
                raise BlockOutOfChain('Block wrong index number')
            if head.hash() != block.prev_hash:
                raise BlockOutOfChain('New block not pointed to the head')
            if head.timestamp > block.timestamp:
                raise BlockOutOfChain('Block is from the past')
        
        return True