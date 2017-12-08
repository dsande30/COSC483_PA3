import argparse
from Crypto.Cipher import AES

def getFlags():
    #parse command line args
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", dest = 'keyFile', help="Enter key file", required = True)
    parser.add_argument("-m", dest = 'msgFile', help="Enter message file", required = True)
    parser.add_argument("-t", dest = 'tagFile', help= "Enter tag file", required=True)
    args = parser.parse_args()
    return args

def getInfo(args):
    fd = open(args.keyFile)
    key = fd.readline().strip()
    fd.close()

    fd = open(args.msgFile)
    msg = ""
    while True:
        string = fd.readline()
        if string == "":
            break
        msg += string
    fd.close()
    msg = msg.strip()
    return (key, msg)

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
    priorBlock = cipher.encrypt(blocks[0])
    message = ""
    for currentBlock in blocks[0:]:
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

def writeFile(oFile, ciphertext):
    fd = open(oFile, "wb")
    fd.write(ciphertext)
    fd.close()

def main():
    args = getFlags()
    results = getInfo(args)
    paddedmsg = pad(results[1])
    blocks = blockify(paddedmsg)
    ciphertext = xor(blocks, results[0])
    writeFile(args.tagFile, ciphertext)

if __name__ == "__main__":
    main()
