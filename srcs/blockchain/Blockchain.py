import logging
from ..blocks import Block, Tx, Input, Output
from ..verifiers import TxVerifier, BlockVerifier
from ..verifiers.exceptions import BlockOutOfChain, BlockVerificationFailed

logger = logging.getLogger('Blockchain')

class Blockchain:
    __slots__= 'max_nonce', 'chain', 'unconfirmed_transactions', 'db', 'wallet', 'on_new_block', 'on_prev_block', 'current_block_transactions', 'fork_blocks'

    def __init__(self, db, wallet, on_new_block=None, on_prev_block=None):
        self.max_nonce = 2**32

        self.db = db
        self.wallet = wallet
        self.on_new_block = on_new_block
        self.on_prev_block = on_prev_block

        self.unconfirmed_transactions = set()
        self.current_block_transactions = set()
        self.chain = []
        self.fork_blocks = {}

    def create_first_block(self):
        tx = self.create_coinbase_tx()
        block = Block([tx], 0, 0x0)
        self.mine_block(block)

    def create_coinbase_tx(self, fee=0):
        inp = Input('COINBASE', 0, self.wallet.address, 0)
        inp.sign(self.wallet)
        out = Output(self.wallet.address, self.db.config['mining_reward'] + fee, 0)
        return Tx([inp], [out])

    def is_valid_block(self, block):
        bv = BlockVerifier(self.db)
        return bv.verify(self.head, block)

    def add_block(self, block):
        if self.head and block.hash() == self.head.hash():
            logger.error('Duplicate block')
            return False
        try:
            self.is_valid_block(block)
        except BlockOutOfChain:
            if block.prev_hash == self.head.prev_hash:
                logger.error('Split Brain Detected')
                self.fork_blocks[block.hash()] = block
                return False
            else:
                for b_hash, b in self.fork_block_items():
                    if block_prev_hash == b_hash:
                        logger.error('Split Brain fixed. Longer Chain choosen')
                        self.rollback_block()
                        self.chain.append(b)
                        self.chain.append(block)
                        self.fork_blocks = {}
                        return True
                    logger.error('Second Split Brain detected. Not programmed to fix this')
                    return False
        except BlockVerificationFailed as e:
            logger.error('Block verification failed: %s' % e)
            return False
        else:
            self.chain.append(block)
            self.fork_blocks = {}
            logger.info('   Block added')
            return True
        logger.error('Hard chain out of sync')

    def add_tx(self, tx):
        if self.db.transaction_by_hash.get(tx.hash):
            return False
        tv = TxVerifier(self.db)
        fee = tv.verify(tx.inputs, tx.outputs)
        self.db.transaction_by_hash[tx.hash] = tx.as_dict
        self.unconfirmed_transactions.add(fee, tx.hash)
        return True