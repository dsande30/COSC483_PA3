##CBC - DEC

import binascii
import getopt
import sys
import os
import argparse
from Crypto.Random import random
from Crypto.Cipher import AES

#XOR function
def xor(blocks, IV, key32):
    message = []
    cipher = AES.new(key32, AES.MODE_ECB)
    priorBlock = IV
    for currentBlock in blocks:
        ciphertext = cipher.encrypt(str(priorBlock))
        text = ""
        text += "".join(chr(ord(a)^ord(b)) for a,b in zip(currentBlock, ciphertext))
        priorBlock = currentBlock
        message += text
    return message

def main(argv):
    keyfile = ''
    inputfile = ''
    outputfile = ''
    ivfile = ''

    #Reads flags from command line
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", dest = 'keyfile', help="Enter key file", required = True)
    parser.add_argument("-i", dest = 'inputfile', help="Enter input file", required = True)
    parser.add_argument("-o", dest = 'outputfile', help= "Enter ouput file", required=True)
    args = parser.parse_args()

    #Opens Files
    i = open(args.inputfile, 'rb')


    s = []
    key = ""
    ciphertext = ""

    #Takes the IV from the Encryption Part
    key = args.keyfile
    IV = i.readline()
    print("Iv: %s DONE WITH IV" % IV)

    while True:
        string = i.readline()
        if string == "":
            break
        ciphertext += str(string)

    i.close()
    os.remove(args.inputfile)


    blocks = []

    #Splits up the ciphertext into blocks of 16 bytes
    x = 0
    check = ciphertext[:]
    while len(check) > 0:
        slicelen = min(len(ciphertext), 16)
        blocks.append(check[0:slicelen])
        check = check[slicelen:]
        x += 1

    #Gets correct key
    #key32 = "".join([ ' ' if x >= len(s) else s[x] for x in range(32)])
    key32 = key
    #print("Key %s" % key32)

    #Strips any newline characters from the IV so that it is the right size
    IV = IV.rstrip("\n\r")
    #print("IV %s" % IV)

    #Calls the XOR function to get the original plaintext
    plaintext = xor(blocks, IV, key32)

    o = open(args.outputfile, 'wb')
    o.write(repr("".join(plaintext)))
    o.close()

if __name__ == "__main__":
    main(sys.argv[1:])
