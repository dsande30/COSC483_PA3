#RSA Encrypt
import sys
import argparse
from Crypto.Util import number
from Crypto.Random import random
import fractions
import binascii

def getFlags():
    #parse command line args
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", dest = 'keyFile', help="Enter Key file", required = True)
    parser.add_argument("-i", dest = 'inputFile', help="Enter input file", required = True)
    args = parser.parse_args()
    return args

#Encrypts the messag eafter padding
def Encrypt(m, contents):
    #print "M: %d" % m
    #rint "N: %d" % contents[1]
    #rint "e: %d" % contents[2]
    return pow(m, contents[2], contents[1])
    #return ((m**contents[2]) % contents[1])

#NOTE: This will change with proper message
def writeOutput(outputFile, paddedM):
    o = open(outputFile, 'wb')
    o.write(str(paddedM))
    o.close()

#Reads in the key file
def readKey(keyFile):
    key = open(keyFile, 'rb')
    numBits = key.readline()
    N = key.readline()
    e = key.readline()
    key.close()
    numBits = numBits.strip()
    N = N.strip()
    e = e.strip()
    return int(numBits), int(N), int(e)

#in this instance we don't need input file
'''
#Reads in the input file
def readInput(inputFile):
    i = open(inputFile, 'rb')
    m = i.readline()
    i.close()
    m = str(m)
    return m
'''

#Function pads the message and prepares for encryption
def pad(message, r):
    M = ""
    M += str(ord(b'\x00')) + str(ord(b'\x02'))
    test = 0


    #Gets r random bits for padding
    while test == 0:
        test = 1
        rand = random.getrandbits(r)
        rand = str(rand)
        length = len(rand)
        randlength = 0
        list = []
        for x in rand:
            list.append(x)
        for i in range(0, len(list)):
            if list[i] == "0":
                string = str(random.getrandbits(30))
                if string[0:1] != 0:
                    list[i] = string[0:1]
                    #print("Replacing with %s" % list[i])
            #randlength += int(x).bit_length()
        rand = int(''.join(list))
        randlength = rand.bit_length()
        if randlength != r:
            test = 0

    M += str(rand) + str(ord(b'\x00'))
    message = message.strip()
    messageLen = 0

    M += message

    bitLength = 0
    for i in range(0, len(M)):
        bitLength += int(M[i]).bit_length()
        if M[i] == "0":
            bitLength += 1

    #DEBUGGING
    #print "Rand: %s" % rand
    #print randlength
    #print "r - 24 = %d" % (r - 24)
    #print "Message after pad: %s" % message
    #print "messageLen: %d" % messageLen
    #print "What's M: %s" % M
    #print "bitLength: %d" % bitLength

    return int(M)



def main():
    args = getFlags()
    contents = readKey(args.keyFile)
    message = args.inputFile
    paddedM = pad(message, int(contents[0]) / 2)
    c = Encrypt(paddedM, contents)
    print(c)
    return
    #writeOutput(args.outputFile, c)

if __name__ == "__main__":
	main()
