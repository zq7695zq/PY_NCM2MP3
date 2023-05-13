box = [i for i in range(256)]

# CR4-KSA秘钥调度算法  生成s-box
def KSA(key):
    bLen = len(key)
    for i in range(256):
        box[i] = i
    j = 0
    for i in range(256):
        j = (j + box[i] + key[i % bLen]) & 0xff
        box[i], box[j] = box[j], box[i]


# CR4-PRGA伪随机数生成算法 加密或解密
def PRGA(data, dLen):
    i, j = 0, 0
    data = bytearray(data)
    for k in range(dLen):
        i = (k + 1) & 0xff
        j = (box[i] + i) & 0xff
        data[k] ^= box[(box[i] + box[j]) & 0xff]
    return data
