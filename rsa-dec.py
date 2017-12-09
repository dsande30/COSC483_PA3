#RSA Decrypt
import sys
import argparse
from Crypto.Util import number
import fractions

def getFlags():
    #parse command line args
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", dest = 'keyFile', help="Enter Key file", required = True)
    parser.add_argument("-i", dest = 'inputFile', help="Enter input file", required = True)
    args = parser.parse_args()

    return args

#Reads in key file
def readKey(keyFile):
    key = open(keyFile, 'rb')
    numBits = key.readline()
    numBits = numBits.strip()
    N = key.readline()
    N = N.strip()
    d = key.readline()
    d = d.strip()
    key.close()
    return numBits, N, d

#Reads in Input File
def readInput(inputFile):
    inp = open(inputFile, 'rb')
    c = inp.readline()
    c = c.strip()
    return c

#Decrypts the file
def Dec(key, c):
    c = int(c)
    d = int(key[2])
    N = int(key[1])
    #print "C: %d" % c
    #print("N: %d" % N)
    #print("d: %d" % d)
    m = pow(c, d, N)
    return m

#Writes the output to the designated output file
def writeOutput(outputFile, m):
    out = open(outputFile, 'wb')
    out.write("%d" %m)
    out.close()

#Removes the padding to reveal the original message
def unpad(m):
    #print m
    r, M = m.split("0", 1)
    M = M.strip()
    return M

def main():
    args = getFlags()
    key = readKey(args.keyFile)
    message = args.inputFile
    m = Dec(key, message)
    m = unpad(str(m))
    print(str(m))
    return

if __name__ == "__main__":
	main()
