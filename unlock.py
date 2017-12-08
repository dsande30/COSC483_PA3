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

def pubVerify(args):
    dest = args.pubKeyFile + "-casig"
    command = "python2.7 rsa-validate.py -k " + args.valFile + " -m " + args.pubKeyFile + " -s " + dest
    returnVal = subprocess.check_output([command], shell=True)
    return returnVal.strip()

def symVerify(args):
    command = "python2.7 rsa-validate.py -k " + args.pubKeyFile + " -m  symManifest -s symManifest-casig"
    returnVal = subprocess.check_output([command], shell=True)
    return returnVal.strip()

def main():
    args = getFlags()
    lockIntegrity = pubVerify(args)
    if lockIntegrity != "True":
        print("Locking Party's Public Key Was Unverified")
        exit()
    symIntegrity = symVerify(args)
    if symIntegrity != "True":
        print("Symmetric Key Manifest Was Unverified")
        exit()


if __name__ == "__main__":
    main()


command = "python2.7 rsa-sign.py -k " + args.caFile + " -m " + args.publicFile + " -s " + dest
subprocess.call([command], shell=True)
