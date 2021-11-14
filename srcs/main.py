from wallet import Wallet 

if __name__ == "__main__":
	print("hello")
	wall = Wallet.Wallet.create()
	print(wall.address)
	print(wall.priv)
	pass
