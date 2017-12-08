import argparse

def getFlags():
    #parse command line args
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", dest = 'directory', help="Enter directory to lock", required = True)
    parser.add_argument("-p", dest = 'pubKeyFile', help="Enter action public key file", required = True)
    parser.add_argument("-r", dest = 'privKeyFile', help= "Enter action private key file", required=True)
    parser.add_argument("-vk", dest = 'valFile', help= "Enter validate pubkey file", required=True)
    args = parser.parse_args()
    return args

def verifyUnlocker(args):
    print("Pub: %s" % args.pubKeyFile)
    print("Priv: %s" % args.privKeyFile)

def main():
    args = getFlags()
    verifyUnlocker(args)

if __name__ == "__main__":
    main()
