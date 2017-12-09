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

def encVerify(args):


def decDir(directory, key):
    currentdir = os.getcwd()
    newlist = []
    for letter in currentdir:
        newlist.append(letter)
    for i in range(0, len(newlist)):
        if newlist[i] == ' ':
            newlist[i] = "\ "
    current dir = ''.join(newlist)

    for root, dirs, files in os.walk(directory):
        os.chdir(directory)
        for file in files:
            decFile(file, key, currentdir)

def decFile(file, key, currentdir):
    command = "python 2.7 " + currentdir + "/cbc-dec.py -k " + str(key) + " -i " + file + " -o " + file
    subprocess.call([command], shell=True)

def decManifest(args, key):
    command = "python2.7 rsa-dec.py -k " + args.pubKeyFile + " -i " + str(key)
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
    else:
        print("Verified dat lock integrity")
    symIntegrity = symVerify(args)
    if symIntegrity != "True":
        print("Symmetric Key Manifest Was Unverified")
        exit()
    else:
        print("Verified sym key manifesto speghettio")
    key = readManifest()
    aesKey = decManifest(args, key)
    decDir(args.directory, aesKey)



if __name__ == "__main__":
    main()
