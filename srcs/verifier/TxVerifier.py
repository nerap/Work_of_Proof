import rsa
import binascii
from ..wallet import Address

class TxVerifier:
    def __init__(self, db):
        self.db = db
    
    def verify(self, inputs, outputs):
        total_amount_in = 0
        total_amount_out = 0
        for i, inp in enumerate(inputs):
            if inp.prev_tx_hash == 'COINBASE' and i == 0:
                total_amount_in = int(self.db.config['mining_reward'])
                continue

            try:
                out = self.db.transaction_by_hash[inp.prev_tx_hash]['outputs'][inp.output_index]
            except KeyError:
                raise Exception('Transaction output not found.')
            
            total_amount_in += int(out['amount'])

            if (inp.prev_tx_hash, out['hash']) not in self.db.unspent_txs_by_user_hash.get(out['address'], set()):
                raise Exception('Output of transaction already spent.')
            
            hash_string = '{}{}{}{}'.format(inp.prev_tx_hash, inp.output_index, inp.address, inp.index)

            try:
                rsa.verify(hash_string.encode(), binascii.unhexlify(inp.signature.encode()), Address(out['address']).key) == 'SHA-256'
            except:
                raise Exception('Signature verification failed: %s' % inp.as_dict)
        
        for out in outputs:
            total_amount_out += int(out.amount)
        
        if total_amount_in < total_amount_out:
            raise Exception('Insuficient funds.')
        
        return total_amount_in - total_amount_out 