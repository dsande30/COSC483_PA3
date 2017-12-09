import argparse
import subprocess
import os
import sys
from Crypto.Random import random

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

def encVerify(key, file, currentdir):
    file = file[:-4]
    command = "python2.7 " + currentdir + "/cbcmac-validate-2.py -k " + str(key) + " -m " + file + " -t " + file + "-tag"
    result = subprocess.check_output([command], shell=True)
    return result.strip()

def decDir(directory, key):
    currentdir = os.getcwd()
    newlist = []
    for letter in currentdir:
        newlist.append(letter)
    for i in range(0, len(newlist)):
        if newlist[i] == ' ':
            newlist[i] = "\ "
    currentdir = ''.join(newlist)

    for root, dirs, files in os.walk(directory):
        os.chdir(directory)
        #tags
        for file in files:
            if file[-4:] == "-tag":
                encIntegrity = encVerify(key, file, currentdir)
                if encIntegrity != "True":
                    sys.exit("Bad file detected: %s" % file)
                os.remove(file)

    os.chdir("..")
    for root, dirs, files in os.walk(directory):
        #for files
        os.chdir(directory)
        for file in files:
            decFile(file.strip(), key, currentdir)

def decFile(file, key, currentdir):
    command = "python2.7 " + currentdir + "/cbc-dec.py -k " + str(key) + " -i " + file + " -o " + file
    subprocess.call([command], shell=True)

def decManifest(args, key):
    command = "python2.7 rsa-dec.py -k " + args.privKeyFile + " -i " + str(key)
    result = subprocess.check_output([command], shell=True)
    return result.strip()

def readManifest():
    fd = open("symManifest", "rb")
    key = fd.readline()
    fd.close()
    return key.strip()

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

    key = readManifest()
    aesKey = decManifest(args, key)
    decDir(args.directory, aesKey)



if __name__ == "__main__":
    main()
