from DES import *
#TODO: you will need to delete this error from the error file
from Errors import DESError
import sys

def main():
    if len(sys.argv) != 5:
        print("""
                Insufficient arguments to the program. Please make sure that
                the program will be ran in the following manner

                python3 main.py <mode> <key> <input file name> <outputfile>

                <mode>: The following is case insensitive
                    (e)ncryption - for encryption mode of the program 
                    (d)ecryption - for decryption mode of the program

                <key>: any input which you want to use as a key to either 
                encrypt or decrypt your file

                <input file name>: any file which you want to encrypt or
                decrypt
                
                <output file>: the file name which you want to write the
                results of the encryption or decryption too

                """)

    else:
        des = DES()
        des.key = sys.argv[2]


        if  sys.argv[1][0].upper() == "E":
            try:
                #des.encryption = encryptionStatus.decrypted
                des.loadFile(sys.argv[3])
            except FileNotFoundError as err:
                print("""
                        Please make sure that you have typed out file name 
                        correctly, or file exists in the current directory

                        ERROR FOUND:
                        %s

                        """ % err)
            #you will need to have a try and catch statement in here
            encryptedtext = des.encrypt()
            des.saveFile(sys.argv[4])

        elif sys.argv[1][0].upper() == "D":
            try:
                des.encryption = encryptionStatus.encrypted
                des.loadFile(sys.argv[3])
            except FileNotFoundError as err:
                print("""
                        Please make sure that you have typed out file name 
                        correctly, or file exists in the current directory

                        ERROR FOUND:
                        %s

                        """ % err)
            #this is needed because of the manner the class has being written
            des.decrypt()
            des.saveFile(sys.argv[4])
        else: 
            print("""
                Please make sure you enter the modes as the following
                    (e)ncryption - for encryption mode of the program 
                    (d)ecryption - for decryption mode of the program
                """)

    """


    des.key = "Tawana"

    decryptedContents = des.decrypt()
    des.saveFile("retrieved.txt")
    """

if __name__ == "__main__":
    main()
