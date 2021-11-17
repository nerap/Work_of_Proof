from srcs.Wallet.Wallet import Wallet
from srcs.Transactions.Input import Input
from srcs.Transactions.Output import Output
from srcs.Transactions.Transactions import Transactions
from srcs.Blocks.Block import Block

if __name__ == "__main__":
    wall = Wallet.create()
    wall2 = Wallet.create('.wallet2/')
    wall3 = Wallet.create('.wallet3/')


    #print(wall.address)
    #print(wall2.address)
    #print(wall3.address)

    #print(wall.sign(b'hello'))

    out = Output(wall.address, '132')
    out1 = Output(wall2.address, '132')
    inp = Input(out.hash, out._index, wall.address)
    inp1 = Input('INIT', out._index, wall.address)
 
    inp.sign(wall)


    transac = Transactions([inp], [out, out1])

    #print(out.as_dict)
    #print(inp.as_dict)
    print(transac.as_dict)

    pass