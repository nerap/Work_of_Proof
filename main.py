from srcs.wallet import Wallet
from srcs.blocks import Input, Output
#from srcs.blocks import Output


if __name__ == "__main__":
	wall = Wallet.Wallet.create()
	inp = Input.Input('COINBASE', 0, wall.address, 0)
	inp.sign(wall)
	print(inp.as_dict)
	out = Output.Output(wall.address, 2, 0)
	print(out.as_dict)
