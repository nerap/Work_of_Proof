import rsa

class Address:
    def __init__(self, addr):
        if isinstance(addr, rsa.PublicKey):
            self.addr = addr
        else:
            if isinstance(addr, str):
                addr = addr.encode()
            self.addr = rsa.PublicKey.load_pkcs1(b'-----BEGIN RSA PUBLIC KEY-----\n%b\n-----END RSA PUBLIC KEY-----\n' % addr)

    def __str__(self):
        return b''.join(self.addr.save_pkcs1().split(b'\n')[1:-2]).decode()
    
    @property
    def key(self):
        return self.addr