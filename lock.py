import os
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
        exit()

def randAESKey():
    val = random.getrandbits(128)
    val = str(val)
    val = val[0:16]
    return int(val)

def rsaEnc(args, key):
    command = "python2.7 rsa-enc.py -k " + args.pubKeyFile + " -i " + str(key)
    result = subprocess.check_output([command], shell=True)
    return result.strip()

def printManifest(encryptedKey):
    fd = open("symManifest", "w")
    fd.write(encryptedKey)
    fd.close()

def signManifest(lock_priv):
    command = "python2.7 rsa-sign.py -k " + lock_priv + " -m symManifest -s symManifest-casig"
    subprocess.call([command], shell=True)

def encryptDir(directory, key):
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
        for file in files:
            encryptFile(file, key, currentdir)
            tagFile(file, key, currentdir)

def encryptFile(file, key, currentdir):
    command = "python2.7 " + currentdir + "/cbc-enc.py -k " + str(key) + " -i " + file + " -o " + file
    subprocess.call([command], shell=True)

def tagFile(file, key, currentdir):
    command = "python2.7 " + currentdir + "/cbcmac-tag_2.py -k " + str(key) + " -m " + file + " -t " + file + "-tag"
    subprocess.call([command], shell=True)

def main():
    args = getFlags()
    check = verifyUnlocker(args)
    key = randAESKey()
    encryptedKey = rsaEnc(args, key)
    printManifest(encryptedKey)
    signManifest(args.privKeyFile)
    encryptDir(args.directory, key)

if __name__ == "__main__":
    main()
