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

def openFiles(args):
    #keyFile
    fd = open(args.keyFile, "r")
    numBits = fd.readline()
    numBits = int(numBits.strip())
    N = fd.readline()
    N = int(N.strip())
    pubKey = fd.readline()
    pubKey = int(pubKey.strip())
    keyTuple = (numBits, N, pubKey)
    fd.close()

    #msgFile
    msg = ""
    fd = open(args.msgFile, "rb")
    while True:
        string = fd.readline()
        if string == "":
                break
        msg += string
    fd.close()

    #sigFile
    fd = open(args.sigFile, "r")
    sig = ""
    while True:
        string = fd.readline()
        if string == "":
            break
        sig += string
    sig = int(sig)
    fd.close()

    return (keyTuple, msg, sig)

def hash(message):
    h = SHA256.new()
    h.update(message)
    return h

def verify(h, sig, N, e):
    result = pow(sig, e, N)
    if result == (int(h.hexdigest(), 16) % N):
        return 1
    else:
        return 0

def main():
    args = getFlags()
    results = openFiles(args)
    h = hash(results[1])
    value = verify(h, results[2], results[0][1], results[0][2])
    if value == 1:
        print("True")
    else:
        print("False")

if __name__ == "__main__":
    main()
