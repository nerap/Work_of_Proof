import os
import sys
import rsa

'''
    Wallet has a dedicated folder to hold both public and private key.
    Using rsa python package, encrypted with SHA-256 with 512 bits key length.
    Signing and verifying transaction. 
'''

class Wallet:
    __slots__ = '_pub_key', '_priv_key', '_folder', '_encrypt'

    def __init__(self, folder, _pub_key='', _priv_key='', _encrypt='SHA-256'):
        self._folder = folder
        self._pub_key = _pub_key
        self._priv_key = _priv_key
        self._encrypt = _encrypt

    @property
    def address(self):
        return self._pub_key

    @property
    def priv(self):
        return self._priv_key

    @classmethod
    def create(cls, folder='.wallet/'):
        inst = cls(folder)
        inst._pub_key, inst._priv_key = rsa.newkeys(512)
        inst.save_in_folder()
        return inst

    @classmethod
    def get(cls, folder='.wallet/'):
        inst = cls(folder)
        inst.read_pair_keys()
        return inst

    def save_in_folder(self):
        access_rights = 0o700
        try:
            if not os.path.exists(self._folder):
                os.mkdir(self._folder, access_rights)
            self.write_pair_keys()
        except OSError as err:
            print("Error: {0}".format(err))
            sys.exit(1)

    def write_pair_keys(self):
        try:
            with open(self._folder + 'wallet_key', 'wb') as _priv_key_file:
                _priv_key_file.write(self._priv_key.save_pkcs1())
            with open(self._folder + 'wallet_key.pub', 'wb') as _pub_key_file:
                _pub_key_file.write(self._pub_key.save_pkcs1())
        except OSError as err:
            print("Error: {0}".format(err))
            sys.exit(1)
        except rsa.pkcs1.CryptoError as err:
            print("Error: {0}".format(err))
            sys.exit(1)
 
    def read_pair_keys(self):
        try:
            with open(self._folder + 'wallet_key', 'rb') as _priv_key_file:
                _priv_key_data = _priv_key_file.read()
            with open(self._folder + 'wallet_key.pub', 'rb') as _pub_key_file:
                _pub_key_data = _pub_key_file.read()
            self._priv_key = rsa.PrivateKey.load_pkcs1(_priv_key_data)
            self._pub_key = rsa.PublicKey.load_pkcs1(_pub_key_data)
        except OSError as err:
            print("Error: {0}".format(err))
            sys.exit(1)
        except rsa.pkcs1.CryptoError as err:
            print("Error: {0}".format(err))
            sys.exit(1)

    def sign(self, message):
        try:
            return rsa.sign(message, self._priv_key, self._encrypt)
        except rsa.pkcs1.CryptoError as err:
            print("Error: {0}".format(err))
            sys.exit(1)

    def verify(self, message, signature, address):
        try:
            return rsa.verify(message, signature, address) == self._encrypt
        except rsa.pkcs1.VerificationError as err:
            return False
