import argparse
from Crypto.Hash import SHA256

def getFlags():
    #parse command line args
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", dest = 'keyFile', help="Enter key file", required = True)
    parser.add_argument("-m", dest = 'msgFile', help="Enter message file", required = True)
    parser.add_argument("-s", dest = 'sigFile', help= "Enter signature file", required=True)
    args = parser.parse_args()
    return args

def readKey(keyFile):
    key = open(keyFile, 'rb')
    numBits = key.readline()
    N = key.readline()
    d = key.readline()
    key.close()
    numBits = numBits.strip()
    N = N.strip()
    d = d.strip()
    return int(numBits), int(N), int(d)

def readInput(inputFile):
    i = open(inputFile, 'r')
    m = ""
    while True:
        string = i.readline()
        if string == "":
            break
        m += string
    i.close()
    return m

def writeOutput(outputFile, signature):
    o = open(outputFile, 'wb')
    #o.write("".join(paddedM))
    o.write(str(signature))
    o.close()

def doHash(message):
    h = SHA256.new()
    h.update(message)
    return h

def sign(h, N, d):
    signature = pow(int(h.hexdigest(), 16), d, N)
    return signature

def main():
    args = getFlags()
    contents = readKey(args.keyFile)
    message = readInput(args.msgFile)
    h = doHash(message)
    signature = sign(h, contents[1], contents[2])
    writeOutput(args.sigFile, signature)


if __name__ == "__main__":
    main()
