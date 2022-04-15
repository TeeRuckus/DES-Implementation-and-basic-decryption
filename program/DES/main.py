from DES import *

def main():
    fileName = "DES-test.txt"
    des = DES()

    contents = des.loadFile(fileName)
    des.encrypt()
    des.saveFile("out.txt")



    #TODO: figure out what to do with this testing code for the function: "chart_to_binary"
    """charOne = "A"
    charTwo = "B"
    charthree = "C"
    charFour = "a"
    charFive = "b"
    charSix = "c"

    print("test one: ", char_to_binary(charOne))
    print("test two: ", char_to_binary(charTwo))
    print("test three: ", char_to_binary(charthree))
    print("test four: ", char_to_binary(charOne))
    print("test five: ", char_to_binary(charOne))
    print("test six: ", char_to_binary(charOne))"""


if __name__ == "__main__":
    main()
