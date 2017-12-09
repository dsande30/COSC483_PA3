#CBC - ENC

import binascii
import getopt
import sys
import os
from Crypto.Random import random
from Crypto.Cipher import AES
import argparse

#Pads the plaintext
def pad(message):
    if len(message) > 16:
        if len(message) % 16 != 0:
            message += "0" * (16 - (len(message) % 16))
    elif len(message) < 16:
        message += "0" * (16 - len(message))
    return message

#XOR function
def xor(blocks, IV, key32):
    message = []
    cipher = AES.new(key32, AES.MODE_ECB)
    priorBlock = IV
    for currentBlock in blocks:
        ciphertext = cipher.encrypt(str(priorBlock))
        text = ""
        text += "".join(chr(ord(a)^ord(b)) for a,b in zip(currentBlock, ciphertext))
        priorBlock = text
        message += text
    return message

def main(argv):
    keyfile = ''
    inputfile = ''
    outputfile = ''
    ivfile = ''

    parser = argparse.ArgumentParser()
    parser.add_argument("-k", dest = 'keyfile', help="Enter key file", required = True)
    parser.add_argument("-i", dest = 'inputfile', help="Enter input file", required = True)
    parser.add_argument("-o", dest = 'outputfile', help= "Enter ouput file", required=True)
    args = parser.parse_args()

    #Opens Files
    #k = open(args.keyfile, 'rb')
    i = open(args.inputfile, 'rb')
    if ivfile != "":
        v = open(ivfile, 'rb')

    s = []
    key = ""
    plaintext = ""
    IV = ""

    #reads in key
    key += keyfile
    print("Key: %s" % key)

    #read in input
    while True:
        string = i.readline()
        if string == "":
            break
        plaintext += string
    print("Plaintext: %s" % plaintext)

    i.close()
    os.remove(args.inputfile)

    #Reads in from the input file, key file, and optional IV file
    try:
        if ivfile != "":
            byte3 = v.read(1)
        if ivfile != "":
            while byte3 != "":
                IV += byte3
                byte3 = v.read(1)
    finally:
        if ivfile != "":
            v.close()

    #Pads the plaintext if needed
    plaintext = pad(plaintext)

    blocks = []


    #Separates the plaintext into blocks of 16 bytes
    x = 0
    check = plaintext[:]
    while len(check) > 0:
        slicelen = min(len(plaintext), 16)
        blocks.append(check[0:slicelen])
        check = check[slicelen:]
        x += 1

    #Generates IV if no file specified
    if ivfile == "":
        test = 0
        while test == 0:
            IV = str(random.getrandbits(64))
            if len(IV.encode('utf-8')) == 16:
                test = 1

    #Gets correct key and Then XORs text
    key32 = "".join([ ' ' if x >= len(s) else s[x] for x in range(32)])

    #Gets rid of any newline chars in the IV and unhexlifies it if
    #read in from a file
    IV = IV.rstrip("\n\r")
    if ivfile != "":
        IV = binascii.unhexlify(IV)

    #Calls the XOR function for the ciphertext
    ciphertext = xor(blocks, IV, key32)

    #Only the ciphertext appears in the output file
    o = open(args.outputfile, 'wb')
    o.write(str(IV))
    o.write("\n")
    o.write("".join(ciphertext))
    o.close()

if __name__ == "__main__":
    main(sys.argv[1:])
