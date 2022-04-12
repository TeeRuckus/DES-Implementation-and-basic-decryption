from DES import *

def main():
    #originalData = "0001001100110100010101110111100110011011101111001101111111110001"
    #expected = "11110000110011001010101011110101010101100110011110001111"
    originalData = "1111111111111111111111111111111111111111111111111111111111111111"
    expected = "11111111111111111111111111111111111111111111111111111111"
    desObj = DES()
    actual = desObj._apply_permutation(originalData, desObj._PC_1)

    assert actual == expected, "error in permutation function"


if __name__ == "__main__":
    main()
