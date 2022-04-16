from DES import *
#TODO: you will need to come back and make sure that the decrypted function, is not returning the message in binary but in human readable text

def main():
    fileName = "DES-test.txt"
    des = DES()

    e = des.loadFile(fileName)

    #des.message = "fuck"
    des.key = "Tawana"
    #des.key =  "0001001100110100010101110111100110011011101111001101111111110001"
    encryptedText = des.encrypt()
    des.saveFile("out.txt")


    des.key = "Tawana"

    #des.key =  "0001001100110100010101110111100110011011101111001101111111110001"
    decryptedContents = des.decrypt()
    des.saveFile("retrieved.txt")

if __name__ == "__main__":
    main()
