import argparse
from Crypto.Cipher import AES
import binascii
import difflib

def getFlags():
    #parse command line args
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", dest = 'keyFile', help="Enter key file", required = True)
    parser.add_argument("-m", dest = 'msgFile', help="Enter message file", required = True)
    parser.add_argument("-t", dest = 'tagFile', help= "Enter tag file", required=True)
    args = parser.parse_args()
    return args

def readTag(tagFile):
    t = open(tagFile, 'rb')
    tag = ""
    while True:
        string = t.readline()
        if string == "":
            break
        tag += string
    t.close()
    return tag

def readKey(keyFile):
    key = open(keyFile, 'rb')
    validKey = key.readline().strip()
    key.close()
    return validKey

def readInput(msgFile):
    i = open(msgFile, 'r')
    m = ""
    while True:
        string = i.readline()
        if string == "":
            break
        m += string
    m = m.strip()
    i.close()
    return m

#Pads the plaintext
def pad(message):
    if len(message) > 16:
        if len(message) % 16 != 0:
            message += "0" * (16 - (len(message) % 16))
    elif len(message) < 16:
        message += "0" * (16 - len(message))
    return message

#XOR function
def xor(blocks, key32):
    message = []
    cipher = AES.new(key32, AES.MODE_ECB)
    priorBlock = blocks[0]
    message = ""
    for currentBlock in blocks[1:]:
        ciphertext = cipher.encrypt(str(priorBlock))
        text = ""
        text += "".join(chr(ord(a)^ord(b)) for a,b in zip(currentBlock, ciphertext))
        priorBlock = text
        message += text
    return message

def blockify(plaintext):
    #Separates the plaintext into blocks of 16 bytes
    x = 0
    blocks = []
    length = len(plaintext)
    while(len(str(length)) < 16):
        length = "0" + str(length)
    blocks.append(length)
    check = plaintext[:]
    while len(check) > 0:
        slicelen = min(len(plaintext), 16)
        blocks.append(check[0:slicelen])
        check = check[slicelen:]
        x += 1
    return blocks

def verify(key, message, tag):
    message = pad(str(message))
    blocks = blockify(message)
    compMsg = xor(blocks, key)
    if tag == compMsg:
        return 1
    else:
        return 0

def main():
    args = getFlags()
    key = readKey(args.keyFile)
    tag = readTag(args.tagFile)
    message = readInput(args.msgFile)
    validity = verify(key, message, tag)
    if validity == 1:
        print("True")
    else:
        print("False")


if __name__ == "__main__":
    main()
