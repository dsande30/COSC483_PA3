import argparse
import subprocess

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
    command = "python2.7 rsa-validate.py -k " + args.valFile + " -m " + args.pubKeyFile + " -s " + args.pubKeyFile + "-casig"
    #print("Command: %s" % command)
    result = subprocess.check_output([command], shell=True)
    if(result.strip() == "True"):
        print("Verified")
        return
    else:
        print("Unverified unlocker")
        return

def main():
    args = getFlags()
    check = verifyUnlocker(args)

if __name__ == "__main__":
    main()
