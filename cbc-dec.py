##CBC - DEC

import binascii
import getopt
import sys
import os
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
    try:
        opts, args = getopt.getopt(argv, "k:i:o:v:", ["kfile=", "ifile=", "ofile=", "vfile="])
    except getopt.GetoptError:
        print('cbc-dec.py -k <keyfile> -i <inputfile> -o <outputfile> -v <ivfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("test.py -i <inputfile> -o <outputfile>")
            sys.exit()
        elif opt in ("-k", "--kfile"):
            keyfile = arg
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-v", "--vfile"):
            ivfile = arg

    #Opens Files
    k = open(keyfile, 'rb')
    i = open(inputfile, 'rb')
    o = open(outputfile, 'wb')


    s = []  
    key = ""
    ciphertext = ""

    #Takes the IV from the Encryption Part
    IV = i.readline()

    #Reads in from the input file, key file, and IV file
    try:
        byte = k.read(1)
        byte2 = i.read(1)
        if ivfile != "":
            byte3 = v.read(1)
        while byte != "":
            key += str(byte)
            s += str(byte)
            byte = k.read(1)
        while byte2 != "":
            ciphertext += str(byte2)
            byte2 = i.read(1)
    
    finally:
        k.close()
        i.close()


    blocks = []

    #Splits up the ciphertext into blocks of 16 bytes
    x = 0
    check = ciphertext[:]
    while len(check) >= 16:
        blocks.append(check[0:16])
        check = check[16:]
        x += 1

    #Gets correct key
    key32 = "".join([ ' ' if x >= len(s) else s[x] for x in range(32)])

    #Strips any newline characters from the IV so that it is the right size
    IV = IV.rstrip("\n\r")

    #Calls the XOR function to get the original plaintext
    plaintext = xor(blocks, IV, key32)

    o.write(repr("".join(plaintext)))
    o.close()

if __name__ == "__main__":
    main(sys.argv[1:])