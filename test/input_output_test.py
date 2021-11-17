import io
import os
import unittest
import subprocess
from srcs.Wallet.Wallet import Wallet
from srcs.Transactions.Input import Input
from srcs.Transactions.Output import Output

python_itpt = "./venv/bin/python3"
wallet_directory = 'test/wallet_test/'

class TestIntputOutput(unittest.TestCase):

    def test_input_00(self):
        dir_test = wallet_directory + '/test00/'
        wall_test = Wallet.create(folder=dir_test)
        out = Output(wall_test.address, '132')
        inp = Input(out.hash, out._index, wall_test.address)
        inp2 = Input(out.hash, out._index, wall_test.address)
        inp.sign(wall_test)
        inp2.sign(wall_test)
        self.assertEqual(inp.as_dict, inp2.as_dict)
        self.assertEqual(inp.hash, inp2.hash)

    def test_input_01(self):
        dir_test = wallet_directory + '/test01/'
        wall_test = Wallet.create(folder=dir_test)
        out = Output(wall_test.address, '132')
        inp = Input(out.hash, out._index, wall_test.address)
        inp2 = Input('INIT', out._index, wall_test.address)
        inp.sign(wall_test)
        inp2.sign(wall_test)
        self.assertNotEqual(inp.as_dict, inp2.as_dict)
        self.assertNotEqual(inp.hash, inp2.hash)

    def test_input_02(self):
        dir_test = wallet_directory + '/test02/'
        wall_test = Wallet.create(folder=dir_test)
        wall_test_2 = Wallet.create(folder=wallet_directory + '/test01/')
        out = Output(wall_test.address, '132')
        out1 = Output(wall_test_2.address, '132')
        inp = Input(out.hash, out._index, wall_test.address)
        inp1 = Input('INIT', out._index, wall_test_2.address)
        inp.sign(wall_test)
        self.assertNotEqual(inp.as_dict, inp1.as_dict)
        self.assertNotEqual(out.as_dict, out1.as_dict)

if __name__ == '__main__':
    unittest.main()