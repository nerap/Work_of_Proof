import os
import sys
import rsa


class Wallet:
    __slots__ = '_pub_key', '_priv_key', '_folder'

    def __init__(self, folder=None):
        if not folder:
            self._pub_key, self._priv_key = rsa.newkeys(512)
            print(self._pub_key.save_pkcs1())
            print(self._priv_key.save_pkcs1())
        else:
            self._folder = folder
            get_pair_keys()

    def save_in_folder(self):
        access_rights = 0o600
        
    def get_pair_keys(self):
        try:
            with open(self.folder + 'wallet_key', 'rb') as _priv_key_file:
                _priv_key_data = _priv_key_file.read()
            with open(self.folder + 'wallet_key.pub', 'rb') as _pub_key_file:
                _pub_key_data = _pub_key_file.read()
            
            self._priv_key = rsa.PrivateKey.load_pkcs1(_priv_key_data)
            self._pub_key = rsa.PublicKey.load_pkcs1(_pub_key_data)
        except OSError as err:
            print("Error: {0}".format(err))
            sys.exit()
        except rsa.pkcs1.CryptoError as err:
            print("Error: {0}".format(err))
            sys.exit()

    @classmethod
    def create(cls, folder=None):
        inst = cls(folder)
        return inst

    @property
    def address(self):
        return self._pub_key

    @property
    def priv(self):
        return self._priv_key




