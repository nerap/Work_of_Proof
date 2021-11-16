import io
import os
import unittest
import subprocess
from srcs.Wallet.Wallet import Wallet

python_itpt = "./venv/bin/python3"
wallet_directory = 'test/wallet_test/'

class TestWallet(unittest.TestCase):

    def test_wallet_00(self):
        dir_test = wallet_directory + '/test00/'
        wall_test = Wallet.create(folder=dir_test)
        wall_read_test = Wallet.get(folder=dir_test)
        self.assertEqual(wall_test._pub_key, wall_read_test._pub_key)
        self.assertEqual(wall_test.priv, wall_read_test.priv)

    def test_wallet_01(self):
        dir_test = wallet_directory + '/test01/'
        message = b'hello'
        wall_test = Wallet.create(folder=dir_test)
        wall_read_test = Wallet.get(folder=dir_test)
        self.assertEqual(wall_test.sign(message), wall_read_test.sign(message))

    def test_wallet_02(self):
        dir_test = wallet_directory + '/test02/'
        message = b'hello'
        wall_test = Wallet.create(folder=dir_test)
        wall_read_test = Wallet.get(folder=dir_test)
        sign_one = wall_test.sign(message)
        sign_two = wall_read_test.sign(message)
        self.assertEqual(wall_test.verify(message, sign_one, wall_test._pub_key), wall_read_test.verify(message, sign_two, wall_read_test._pub_key))

if __name__ == '__main__':
    unittest.main()