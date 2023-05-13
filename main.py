# 这是一个示例 Python 脚本。
import base64
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB
import json

from aes import AES_ENCRYPT
import cr4

cr4_aes_key = bytearray(
    [0x68, 0x7A, 0x48, 0x52, 0x41, 0x6D, 0x73, 0x6F, 0x35, 0x6B, 0x49, 0x6E, 0x62, 0x61, 0x78, 0x57])
mata_aes_key = bytearray(
    [0x23, 0x31, 0x34, 0x6C, 0x6A, 0x6B, 0x5F, 0x21, 0x5C, 0x5D, 0x26, 0x30, 0x55, 0x3C, 0x27, 0x28])


def magicHeader(file):
    file.read(10)


def getLength(bytes):
    len = 0
    len |= bytes[0] & 0xff
    len |= (bytes[1] & 0xff) << 8
    len |= (bytes[2] & 0xff) << 16
    len |= (bytes[3] & 0xff) << 24
    return len


def cr4Key(file):
    len = getLength(file.read(4))
    bytes = bytearray(file.read(len))
    for i in range(len):
        bytes[i] ^= 0x64
    aes = AES_ENCRYPT(cr4_aes_key)  # 创建一个aes对象
    bytes = aes.decrypt(bytes)
    return bytes[17:]


def mataData(file):
    len = getLength(file.read(4))
    bytes = bytearray(file.read(len))
    file.read(9)  # skip
    for i in range(len):
        bytes[i] ^= 0x63
    bytes = bytes[22:]
    temp = base64.b64decode(bytes)
    aes = AES_ENCRYPT(mata_aes_key)  # 创建一个aes对象
    bytes = aes.decrypt(temp)
    return bytes[6:]


def albumImage(file):
    len = getLength(file.read(4))
    return bytearray(file.read(len))


def musicData(in_file, out_file, cr4key):
    cr4.KSA(cr4key)
    while True:
        buffer = in_file.read(0x8000)
        bLen = len(buffer)
        if bLen == 0:
            break
        buffer = cr4.PRGA(buffer, bLen)
        out_file.write(buffer)


def combineFile(mata, mp3_file_path, image):
    # 加载MP3文件
    audio = MP3(mp3_file_path)
    print(mata)
    # 修改标题
    audio.tags.add(TIT2(encoding=3, text=mata['musicName']))

    # 修改专辑
    audio.tags.add(TALB(encoding=3, text=mata['album']))

    # 修改艺术家
    audio.tags.add(TPE1(encoding=3, text=mata['artist'][0]))

    # 修改封面
    # audio.tags.add(APIC(encoding=3, mime='image/png', type=3, desc='Cover', data=image))

    # 保存更改
    audio.save()


def num2mp3(ncm_file_path, mp3_file_path):
    with open(ncm_file_path, 'rb') as ncm_file:
        magicHeader(ncm_file)
        key = cr4Key(ncm_file)
        mata = json.loads(mataData(ncm_file))
        image = albumImage(ncm_file)
        with open(mp3_file_path, 'wb') as mp3_file:
            musicData(ncm_file, mp3_file, key)
        combineFile(mata, mp3_file_path, image)


if __name__ == '__main__':
    num2mp3("test1.ncm", "test2.mp3")
