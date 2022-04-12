from DES import *
import unittest

class DESTest(unittest.TestCase):
    #going through and testing private functions to make sure they work as
    #expected in the algorithm

    def testApplyPermutationPrivate(self):
        #test data are derived from the following textbook
        #https://page.math.tu-berlin.de/~kant/teaching/hess/krypto-ws2006/des.htm

        originalData = "0001001100110100010101110111100110011011101111001101111111110001"
        expected = "11110000110011001010101011110101010101100110011110001111"

        desObj = DES()
        actual = desObj._apply_permutation(originalData, desObj._PC_1)
        self.assertEqual(expected, actual)

