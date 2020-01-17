import pyaes
import random
import secrets

# This script is currently inactive i.e. it returns the data as it is.

class CryptoUtils:
    def gen_key(self):
        # key_list = ['efe449cb62fc12d14438e359dba9e2e7', 'c6e94274b6c9db1cbd35f94bede7de6b', '652c958432855a74d13b4ba8158dd66d', 'f4634a875fc01c194f0bb80f0bf040c3', 'aad17c52d7a104c9ba9945f3b32c45e5', '7d53f1f2e5d1325400ffe3103ba13284', '6730215463aa590060522256cb37c63a', 'c13f3f231486182a3113c3e11fb0eca2', 'b3b78539c0138126165f1f98bb472026', '69dcabfe990a819d40fd94e19f72245e', 'd657323adcb19e40d9087f1a715fb1eb', '40983838be261e9193b8daced6b87570', 'b74565536a37a4ca1445e905e2955bb2', 'a9a272d19107a7b2eb20b970789c26da', '0e9f55d642a97ff425e6378fb382cb02']
        # key = random.choice(key_list)
        key = secrets.token_hex(16)
        return key

    def encrypt(self, plaintext, key):
        newkey = key.encode('utf-8')
        aes = pyaes.AESModeOfOperationCTR(newkey)    
        ciphertext = aes.encrypt(plaintext)
        return ciphertext

    def decrypt(self, ciphertext, key):
        newkey = key.encode('utf-8')
        aes = pyaes.AESModeOfOperationCTR(newkey)
        decrypted = aes.decrypt(ciphertext).decode('utf-8')
        return decrypted

if __name__ == "__main__":
    crypt = CryptoUtils()
