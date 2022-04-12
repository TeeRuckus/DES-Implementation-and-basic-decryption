from DES import *
import unittest

class DESTest(unittest.TestCase):
    #going through and testing private functions to make sure they work as
    #expected in the algorithm

    originalData = "0001001100110100010101110111100110011011101111001101111111110001"
    desObj = DES()
    permutationKey = desObj._applyPermutation(originalData, desObj._PC_1)

    def testApplyPermutation(self):
        #test data are derived from the following textbook
        #https://page.math.tu-berlin.de/~kant/teaching/hess/krypto-ws2006/des.htm

        #TEST 1: Applying the initial permutation on a 64 bit key
        expected = "11110000110011001010101011110101010101100110011110001111"

        #desObj = DES()
        actual = self.desObj._applyPermutation(self.originalData, self.desObj._PC_1)
        self.permutationKey = actual
        self.assertEqual(expected, actual)

    def testSplitKeys(self):
        #Test 2: splitting the permutation keys into two halves, to ensure 
        #that we will have our right hand key and our left hand key

        ret = self.desObj._splitKeys(self.permutationKey)
        leftActual = ret[0]
        rightActual = ret[1] 
        leftExpected = "1111000011001100101010101111"
        rightExpected = "0101010101100110011110001111"

        self.assertEqual(leftExpected, leftActual)
        self.assertEqual(rightExpected, rightActual)

    def testRoundKeys(self):
        expectedKeys =[
                "11100001100110010101010111111010101011001100111100011110", 
                "11000011001100101010101111110101010110011001111000111101",
                "00001100110010101010111111110101011001100111100011110101",
                "00110011001010101011111111000101100110011110001111010101",
                "11001100101010101111111100000110011001111000111101010101",
                "00110010101010111111110000111001100111100011110101010101",
                "11001010101011111111000011000110011110001111010101010110",
                "00101010101111111100001100111001111000111101010101011001",
                "01010101011111111000011001100011110001111010101010110011",
                "01010101111111100001100110011111000111101010101011001100",
                "01010111111110000110011001011100011110101010101100110011",
                "01011111111000011001100101010001111010101010110011001111",
                "01111111100001100110010101010111101010101011001100111100",
                "11111110000110011001010101011110101010101100110011110001",
                "11111000011001100101010101111010101010110011001111000111",
                "11110000110011001010101011110101010101100110011110001111",
                ]

        #re-creating the left and right side of the key to be used
        keys = self.desObj._splitKeys(self.permutationKey)
        #running the actual test to create the required key
        actualKeys = self.desObj._createKeys(keys)

        for pos, expectedKey in enumerate(expectedKeys):
            self.assertEqual(expectedKey, actualKeys[pos])

    def applyPermutationSecondPermutation(self):
        expectedPerm = [
                "000110110000001011101111111111000111000001110010",
                "011110011010111011011001110110111100100111100101",
                "010101011111110010001010010000101100111110011001",
                "011100101010110111010110110110 110011 010100 011101",
                "011111 001110 110000 000111 111010 110101 001110 101000",
                "011000 111010 010100 111110 010100 000111 101100 101111",
                "111011 001000 010010 110111 111101 100001 100010 111100",
                "111101 111000 101000 111010 110000 010011 101111 111011",
                "111000 001101 101111 101011 111011 011110 011110 000001",
                "101100 011111 001101 000111 101110 100100 011001 001111",
                "001000 010101 111111 010011 110111 101101 001110 000110",
                "011101 010111 000111 110101 100101 000110 011111 101001",
                "100101 111100 010111 010001 111110 101011 101001 000001",
                " 010111 110100 001110 110111 111100 101110 011100 111010",
                "101111 111001 000110 001101 001111 010011 111100 001010",
                "110010 110011 110110 001011 000011 100001 011111 110101",


                ]

