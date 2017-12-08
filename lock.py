import argparse
from Crypto.Random import random
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

def randAESKey():
    val = random.getrandbits(128)
    val = str(val)
    val = val[0:16]
    print("Key is %s" % val)
    return int(val)

def rsaEnc(args, key):
    command = "python2.7 rsa-enc.py -k " + args.pubKeyFile + " -i " + str(key)
    result = subprocess.check_output([command], shell=True)
    print("Result:", result.strip())


def main():
    args = getFlags()
    check = verifyUnlocker(args)
    key = randAESKey()
    encryptedKey = rsaEnc(args, key)

if __name__ == "__main__":
    main()
