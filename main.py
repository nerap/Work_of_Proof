from srcs.Wallet.Wallet import Wallet
from srcs.Transactions.Input import Input
from srcs.Transactions.Output import Output

if __name__ == "__main__":
    wall = Wallet.create()

    print(wall.address)

    out = Output(wall.address, '132')
    inp = Input(out.hash, out._index, wall.address)
 
    inp.sign(wall)
    print(out.as_dict)
    print(inp.as_dict)
   # print(wall.verify(b"Hello", wall.sign(b"Hello"), wall._pub_key))
    pass