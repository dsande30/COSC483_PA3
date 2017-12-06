import argparse

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
    print("Key file: %s" % args.keyFile)
    fd = open(args.keyFile, "r")
    for line in fd:
        print("%s" % line.strip())
    print("\n")
    fd.close()

    #msgFile
    print("Message File: %s" % args.msgFile)
    fd = open(args.msgFile, "r")
    for line in fd:
        print("%s" % line.strip())
    print("\n")
    fd.close()

    #sigFile
    print("Signature File: %s" % args.sigFile)
    fd = open(args.sigFile, "r")
    for line in fd:
        print("%s" % line.strip())
    print("\n")
    fd.close()


def main():
    args = getFlags()
    openFiles(args)

if __name__ == "__main__":
    main()
