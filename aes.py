import base64
from Crypto.Cipher import AES


class AES_ENCRYPT(object):
    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_ECB

    def pading(self, text):
        """对加密字符的处理"""
        return text + (len(self.key) - len(text) % len(self.key)) * chr(len(self.key) - len(text) % len(self.key))

    def unpading(self, text):
        """对解密字符的处理"""
        return text[0:-ord(text[-1:])]

    def getKey(self, key):
        """对key的处理,key 的长度 16，24，32"""
        key_len = len(key)
        if key_len <= 16:
            key += "0" * (16 - key_len)
        elif 16 < key_len <= 24:
            key += "0" * (24 - key_len)
        elif key_len <= 32:
            key += "0" * (32 - key_len)
        else:
            key = key[:32]
        return key

    # 加密函数
    def encrypt(self, bytes):
        cryptor = AES.new(self.key, self.mode)  # ECB 模式
        return cryptor.encrypt(bytes)

    # 解密函数
    def decrypt(self, bytes):
        cryptor = AES.new(self.key, self.mode)  # ECB 模式
        plain_text = cryptor.decrypt(bytes)
        return self.unpading(plain_text)
