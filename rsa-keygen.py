#RSA Key Generation
import sys
import argparse
from Crypto.Util import number
import fractions
import subprocess

def getFlags():
    #parse command line args
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", dest = 'publicFile', help="Enter public key file", required = True)
    parser.add_argument("-s", dest = 'secretFile', help="Enter private key file", required = True)
    parser.add_argument("-n", dest = 'numBits', type=int, help= "Enter num of bits file", required=True)
    parser.add_argument("-c", dest = 'caFile', help="Enter CA private key")
    args = parser.parse_args()

    return args

def variableGenerator(numBits):
    #to make p and q
    p = 0
    q = 0
    l = (numBits / 2)
    while(p ==0 and q == 0):
        p = number.getPrime(l)
        q = number.getPrime(l)
        #confirm lengths are the same, not the values
        if p.bit_length() != q.bit_length() or p == q:
            p = 0
            q = 0

    p = int(p)
    q = int(q)

    N = p * q
    order = (p-1)*(q-1)

    #calculate e: coprime to order
    ePrimes = [3,5,7,17,257, 65537]
    booly = 0
    for x in ePrimes:
        if(fractions.gcd(order, x) == 1):
            booly = 1
            e = x
            break
    if booly == 0:
        sys.exit("No coprime")

    #d is inverse of e mod order
    #NOTE: if this is not allowed, let me know. I was unsure.
    d = number.inverse(e, order)

    #print "P: %d" % p
    #print "Q: %d" % q
    #print "N: %d" % N
    #print "Order: %d" % order

    return N, d, e

def writeFiles(args, keys):
    pub = open(args.publicFile, 'w')
    priv = open(args.secretFile, 'w')

    #Write public key
    pub.write("%d\n" % args.numBits)
    pub.write("%d\n" % keys[0])
    pub.write("%d\n" % keys[2])

    #Write private key
    priv.write("%d\n" % args.numBits)
    priv.write("%d\n" % keys[0])
    priv.write("%d\n" % keys[1])

    #close files
    pub.close()
    priv.close()

    #Read CA key
    if args.caFile is not None:
        CA = open(args.caFile, "r")
        caNumBits = CA.readline()
        caN = CA.readline()
        caD = CA.readline()
        CA.close()
    else:
        args.caFile = args.secretFile
        priv = open(args.secretFile, "r")
        caNumBits = priv.readline()
        caN = priv.readline()
        caD = priv.readline()
        priv.close()
    dest = args.publicFile + "-casig"

    command = "python2.7 rsa-sign.py -k " + args.caFile + " -m " + args.publicFile + " -s " + dest
    subprocess.call([command], shell=True)


def main():
    args = getFlags()
    keys = variableGenerator(args.numBits)
    writeFiles(args, keys)

if __name__ == "__main__":
	main()
