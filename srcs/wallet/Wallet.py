import rsa
import binascii
from .Address import Address

class Wallet:
    __slots__ = '_pub', '_priv'

    def __init__(self, pub=None, priv=None):
        if pub:
            self._pub = Address(pub)
            self._priv = rsa.PrivateKey.load_pkcs1(priv)

    @classmethod
    def create(cls):
        inst = cls(b'', b'')
        _pub, _priv = rsa.newkeys(512)
        inst._pub = Address(_pub)
        inst._priv = _priv
        return inst

    @classmethod
    def verify(cls, data, signature, address):
        signature = binascii.unhexlify(signature.encode())
        if not isinstance(address, Address):
            address = Address(address)
        try:
            return rsa.verify(data, signature, address.key) == 'SHA-256'
        except:
            return False

    @property
    def address(self):
        return str(self._pub)

    @property
    def priv(self):
        return self._priv.save_pkcs1()   

    def sign(self, hash):
        return binascii.hexlify(rsa.sign(hash, self._priv, 'SHA-256')).decode()
