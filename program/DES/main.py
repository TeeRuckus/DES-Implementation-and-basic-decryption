from DES import *

def main():
    fileName = "DES-test.txt"
    des = DES()

    e = des.loadFile(fileName)
    des.key = "0001001100110100010101110111100110011011101111001101111111110001"
    des.encrypt()
    des.saveFile("out.txt")
    des.key = "0001001100110100010101110111100110011011101111001101111111110001"
    decryptedContents = des.decrypt()
    des.saveFile("retrieved.txt")

if __name__ == "__main__":
    main()
