import pyaes

class CryptoUtils:

    def encrypt(self, plaintext, key):
        key = key.encode('utf-8')
        aes = pyaes.AESModeOfOperationCTR(key)    
        ciphertext = aes.encrypt(plaintext)
        return ciphertext

    def decrypt(self, ciphertext, key):
        key = key.encode('utf-8')
        aes = pyaes.AESModeOfOperationCTR(key)
        decrypted = aes.decrypt(ciphertext).decode('utf-8')
        return decrypted

if __name__ == "__main__":
    crypt = CryptoUtils()
    inp = 'I am a good boy.'
    key = 'puaay'
    if(len(key) < 32):
        while(len(key)<32):
            key = key + '!'
    text = crypt.encrypt(inp, key)
    print(text)
    de = crypt.decrypt(text, key)
    print(de)
