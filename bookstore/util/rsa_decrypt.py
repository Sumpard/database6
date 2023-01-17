from pathlib import Path
import rsa

_pem_file = Path("auth.pem")
if not _pem_file.exists():
    _pub_key, _priv_key = rsa.newkeys(1024)
    _pem_file.write_bytes(_priv_key.save_pkcs1())
    print("Generate RSA public key:")
    print(_pub_key.save_pkcs1().decode())
else:
    _priv_key = rsa.PrivateKey.load_pkcs1(_pem_file.read_bytes())


def rsa_decrypt(data: bytes):
    return rsa.decrypt(data, _priv_key)