import argparse

def getFlags():
    #parse command line args
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", dest = 'keyFile', help="Enter key file", required = True)
    parser.add_argument("-m", dest = 'msgFile', help="Enter message file", required = True)
    parser.add_argument("-o", dest = 'sigFile', help= "Enter signature file", required=True)
    args = parser.parse_args()
    return args

def main():
    args = getFlags()

if __name__ == "__main__":
    main()
