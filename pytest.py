import requests
import time

from srcs.wallet.Wallet import Wallet
from srcs.blocks.Input import Input
from srcs.blocks.Output import Output
from srcs.blocks.Tx import Tx

while True:
    for port in [8001, 8002, 8000]:
        try:
            print(requests.get(f'http://127.0.0.1:{port}/chain/status').json()['block_hash'])
        except:
            pass
    print('================================================')
    
    time.sleep(2)