from DES import *
import unittest

class DESTest(unittest.TestCase):
    #going through and testing private functions to make sure they work as
    #expected in the algorithm

    initialMessage = "0000000100100011010001010110011110001001101010111100110111101111" 
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
        self.assertEqual(expected, actual, "testing the first permutation "+
        "applied to keys")

    def testSplitKeys(self):
        #Test 2: splitting the permutation keys into two halves, to ensure 
        #that we will have our right hand key and our left hand key

        ret = self.desObj._splitKeys(self.permutationKey)
        leftActual = ret[0]
        rightActual = ret[1] 
        leftExpected = "1111000011001100101010101111"
        rightExpected = "0101010101100110011110001111"

        self.assertEqual(leftExpected, leftActual, "checking if the left side" +
                " left shift is equal" )
        self.assertEqual(rightExpected, rightActual, "checking if the right" +
                " side right shift is equal")

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

        actualPerm = []

        #re-creating the sixteen keys again

        #re-creating the left and right side of the key to be used
        keys = self.desObj._splitKeys(self.permutationKey)
        #running the actual test to create the required key
        actualKeys = self.desObj._createKeys(keys)

        #applying the permutation on each of the returned keys
        for key  in actualKeys:
            actualPerm.append(self.desObj._applyPermutation(key, self.desObj._PC_2))

        #going through and comparing each key returned with the ones which was
        #generated

        for pos, data in enumerate(zip (expectedPerm, actualPerm)):
            expected = data[0]
            actual = data[1]
            self.assertEqual(expected, actual, "applying second permutation" +
                    " to key number [%s]" % pos )


    def testPermutationOnMessage(self):
        
        #testing if I have implemented the initial permutation table correctly 
        #into the code
        expected = "1100110000000000110011001111111111110000101010101111000010101010"

        actual = self.desObj._applyPermutation(self.initialMessage, self.desObj._IP)   
        self.assertEqual(expected, actual, "testing if the initial permutation"+
                " table is coded correctly in the program")

    def testSplitKeyMessage(self):
        #re-generating the permutated messages to see if the split will occur
        #correctly
        message = self.desObj._applyPermutation(self.initialMessage, self.desObj._IP)   
        ret = self.desObj._splitKeys(message)
        leftActual = ret[0]
        rightActual = ret[1] 
        leftExpected = "11001100000000001100110011111111"
        rightExpected = "11110000101010101111000010101010"

        self.assertEqual(leftExpected, leftActual, "checking if the left side" +
                " left shift is equal for message" )
        self.assertEqual(rightExpected, rightActual, "checking if the right" +
                " side right shift is equal message")


    """
    testing if we will be getting the correct results for inputted streams
    of data into the program
    """
    def testXorStreamTest(self):

        streamOnes =  [
                "10101", "0", "1", "00010101010101100101010110101100", 
                "1111111111", "0000000", "111111"]

        streamTwos  = [
                "10000", "0", "1", "11110101010101010101011100011111",
                "1111111111", "0000000","000000"]

        expected = [
                "00101", "0", "0", "11100000000000110000001010110011",
                "0000000000", "0000000", "111111"
                ]

        for pos, data in enumerate(zip(streamOnes, streamTwos)):
            testStreamOne = data[0]
            testStreamTwo = data[1]
            actual = self.desObj._xor(testStreamOne, testStreamTwo)

            self.assertEqual(expected[pos], actual, "testing xor number %s" % pos) 


    def testExpansionBox(self):
        inputData = "11110000101010101111000010101010"
        expected  = "011110100001010101010101011110100001010101010101"
        actual = self.desObj._applyPermutation(inputData, self.desObj._EBox)
        self.assertEqual(actual, expected, "testing if correct values are inputted"+
                " into the expansion box protocol")

    def testGroup48Blocks(self):
        inBlock = "". join([str(1) for x in range(0,48)])
        expected = ['111111', '111111', '111111', '111111', '111111', '111111', '111111', '111111']
        actual = self.desObj._group48Block(inBlock)

        self.assertEqual(expected, actual, "testing if 48 blocks will be divided"+
                " equally into 8 groups of 6 bits" )

    def tesCalculateSBoxRow(self):
        testData =  ["000000", "000001", "100000", "100001"]
        expected = ["00", "01", "10", "11"]

        for test, currData in enumerate(testData):
            actual = self.desObj._calculateSBoxRow(currData)
            self.assertEqual(expected[test], actual, "calculating the SBox row"+
                    " test number %s"%test)

    def testCalculateSBoxCol(self):
        testData = [
                "000000", "000010", "000100", "000110", "001000",
                "001010", "001100", "001110", "010000", "010010",
                "010100", "010110", "011000", "011010", "011100",
                "011110"]
        expected = [
                "0000", "0001", "0010", "0011", "0100",
                "0101", "0110", "0111", "1000", "1001",
                "1010", "1011", "1100", "1101", "1110",
                "1111"]

        for test, currData in enumerate(testData):
            actual = self.desObj._calculateSBoxCol(currData)
            self.assertEqual(expected[test], actual, "calculating the SBox col"+
                    " test number %s" % test)


    def testrowNumberConversion(self):
        testData =  ["000000", "000001", "100000", "100001"]
        expected = [0, 1, 2, 3]
        for test, currData in enumerate(testData):
            actual = self.desObj._calculateSBoxRow(currData)
            actual = self.desObj._calcBinary2Int(actual)
            self.assertEqual(actual, expected[test], "checking if the right range"+
                    " of numbers are being produced test # %s" % (test+1))


    def testcolNumber(self):
        testData = [
                "000000", "000010", "000100", "000110", "001000",
                "001010", "001100", "001110", "010000", "010010",
                "010100", "010110", "011000", "011010", "011100",
                "011110"]
        expected = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]

        for test, currData in enumerate(testData):
            actual = self.desObj._calculateSBoxCol(currData)
            actual = self.desObj._calcBinary2Int(actual) 
            self.assertEqual(actual, expected[test], "checking if the right range"
                    + "the column numbers will be produced. Test # %s" % (test+1))

    def testFeistelNetworkFunction(self):
        righStreamData = "11110000101010101111000010101010"
        #the sixteen keys which were generated from previous example 
        key = "000110110000001011101111111111000111000001110010"
        expected = "00100011010010101010100110111011"
        actual= self.desObj._feistelNetworkFunction(righStreamData, key)


        self.assertEqual(expected, actual, "testing if the feistel network" +
                " block will produce and return the right products")


    def testBinaryToHexadecimal(self):
        testData = ["0000","0001","0010","0011","0100","0101","0110","0111",
                "1000","1001","1010","1011","1100","1101","1110", "1111"]

        expected = ["0", "1", "2", "3", "4","5","6","7", "8", "9", "a", "b", 
                    "c", "d", "e", "f"]

        for test, data in enumerate(testData):
            actual = self.desObj._binary2Hexadecimal(data)
            self.assertEqual(actual, expected[test], "testing if this can successfully"+
                    " convert binary numbers to hexadecimal test # %s" % (test+1))


    def testHexadecimalToBinary(self):
        expected = ["0","1","10","11","100","101","110","111",
                "1000","1001","1010","1011","1100","1101","1110", "1111"]

        testData = ["0", "1", "2", "3", "4","5","6","7", "8", "9", "A", "B", 
                    "C", "D", "E", "F"]

        for test, data in enumerate(testData):
            actual = self.desObj._hexadecimal2Binary(data)
            self.assertEqual(actual, expected[test], "testing for successful" +
                    " conversation from hexadecimal numbers to binary numbers" + 
                    " test # %s" % (test + 1))


    #TODO: you will need to  come back and test these properly
    def testKeyAccesorsMutators(self): 
        testKeys = ["0001001100110100010101110111100110011011101111001101111111110001"]


    #TODO: you will need to come back and test these properly
    def messageAccesorsMuators(self):
        pass


    #I don't really care about the other class field, they is not that much 
    #which will really need to be done with that class field 

    def testEncryptionDecryption(self):
        #this will be in hex representation, the data strucuure will allow the messages in binary

        initialMessage = "0123456789ABCDEF"
        initialMessage = self.desObj._hexadecimal2Binary(initialMessage)
        
        #TODO: I am just cheating here, you will need to come back here and remove this line once you have figured out what padding strategy youu're going to be using  
        initialMessage =  "0000000" + initialMessage

        expected = "85E813540F0AB405"
        expected = self.desObj._hexadecimal2Binary(expected)

        self.desObj.message = initialMessage
        self.desObj.key =  "0001001100110100010101110111100110011011101111001101111111110001"

        actual = self.desObj.encrypt()

        self.assertEqual(actual, expected, "testing the encryption of the DES"+
                " algorithm")

        #I will need to reset the key again as it has being deleted
        self.desObj.key =  "0001001100110100010101110111100110011011101111001101111111110001"
        actualDecrypt = self.desObj.decrypt()

        self.assertEqual(actualDecrypt, initialMessage, "testing of the"+
                " decryption function of DES")






