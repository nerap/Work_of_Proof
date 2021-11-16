from srcs.Wallet.Wallet import Wallet

if __name__ == "__main__":
    wall = Wallet.create()

    print(wall._pub_key)
    print(wall._priv_key)

    print(wall.verify(b"Hello", wall.sign(b"Hello"), wall._pub_key))
    pass