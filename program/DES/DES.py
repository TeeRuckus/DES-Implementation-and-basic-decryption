from Errors import *
from collections import deque
from enum import Enum
import numpy as np

"""
This DES algorithm was built and tested given the examples found in 
"The DES algorithm Illustrated" by J. Orlin Grabbe 
url: https://page.math.tu-berlin.de/~kant/teaching/hess/krypto-ws2006/des.htm
access date: 15/04/2021
Title of web page: The DES algorithm Illustrated
Author: J. Orlin Grabbe
"""
#TODO: you will need come back and add a clear function in her, which will clear the state of the current object 

#an Enum class to represent if the current message has being encrypted or not
class encryptionStatus(Enum):
    encrypted = 1
    decrypted = 2


class DES(object):
    _IP = [58, 50, 42, 34, 26, 18, 10, 2,
            60, 52, 44, 36, 28, 20, 12, 4,
            62, 54, 46, 38, 30, 22, 14, 6,
            64, 56, 48, 40, 32, 24, 16, 8,
            57, 49, 41, 33, 25, 17, 9, 1,
            59, 51, 43, 35, 27, 19, 11, 3,
            61, 53, 45, 37, 29, 21, 13, 5,
            63, 55, 47, 39, 31, 23, 15, 7]

    #this is going to be the final permutation look up
    __FP = [40, 8, 48, 16, 56, 24, 64, 32,
            39, 7, 47, 15, 55, 23, 63, 31,
            38, 6, 46, 14, 54, 22, 62, 30,
            37, 5, 45, 13, 53, 21, 61, 29,
            36, 4, 44, 12, 52, 20, 60, 28,
            35, 3, 43, 11, 51, 19, 59, 27,
            34, 2, 42, 10, 50, 18, 58, 26,
            33, 1, 41, 9, 49, 17, 57, 25]


    #this is going to represent the expansion D-box table
    __Dbox = [32,1,2,3,4,5,
              4,5,6,7,8,9,
              8,9,10,11,12,13,
              12,13,14,15,16,17,
              16,17,18,19,20,21,
              20,21,22,23,24,25,
              24,25,26,27,28,29,
              28,29,30,31,32,1]

    #this is going to represent all the 8 S-boxes used by the algorithm
    #the s-boxes are going to be derived from the following textbook extract
    #https://academic.csuohio.edu/yuc/security/Chapter_06_Data_Encription_Standard.pdf
    __SBox =[
            # S1 
            [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
             [0, 15, 7, 4, 14, 2, 13, 1,10, 6, 12, 11, 9, 5, 3, 8],
             [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
             [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

            # S2
            [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
             [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
             [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
             [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

            # S3
            [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
             [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
             [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
             [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

            # S4
            [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
             [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
             [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
             [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

            # S5
            [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
             [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
             [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
             [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

            # S6
            [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
             [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
             [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
             [ 4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

            # S7
            [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
             [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
             [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
             [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

            # S8
            [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
             [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
             [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
             [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]],
        ]


    #this is going to represent the final permutation of the DES algorithm
    __FinPBox = [ 16, 7, 20, 21, 29, 12, 28, 17,
                  1, 15, 23, 26, 5, 18, 31, 10,
                  2, 8, 24, 14, 32, 27, 3, 9,
                  19, 13, 30, 6, 22, 11, 4, 25 ]

    __key_PBox = [  14,    17,   11,    24,     1,    5,
                    3,    28,   15,     6,    21,   10,
                    23,    19,   12,     4,    26,    8,
                    16,     7,   27,    20,    13,    2,
                    41,    52,   31,    37,    47,   55,
                    30,    40,   51,    45,    33,   48,
                    44,    49,   39,    56,    34,  53,
                    46,    42,   50,    36,    29,   32 ]


    #this is going to be the number of left shifts for PC-1
    _leftShifts = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1 ]

    #this is going to represented the first permuted choice 
    _PC_1 = [57, 49, 41, 33, 25, 17, 9,
            1, 58, 50, 42, 34, 26, 18,
            10, 2, 59, 51, 43, 35, 27,
            19, 11, 3, 60, 52, 44, 36,
            63, 55, 47, 39, 31, 23, 15,
            7, 62, 54, 46, 38, 30, 22,
            14, 6, 61, 53, 45, 37, 29,
            21, 13, 5, 28, 20, 12, 4 ]

    #this is going to represent the second permuted choice
    _PC_2 = [14,17,11,24,1, 5,
              3,28,15,6,21,10,
             23,19,12,4,26,8,
             16,7,27,20,13,2,
             41,52,31,37,47,55,
             30,40,51,45,33,48,
             44,49,39,56,34,53,
             46,42,50,36,29,32
            ]

    #this will represent the expansion selection box which will be used
    #to expand a message from 32 bits to 48bits 
    _EBox = [ 32,1,2,3,4,5,
              4,5,6,7,8,9,
              8,9,10,11,12,13,
             12,13,14,15,16,17,
             16,17,18,19,20,21,
             20,21,22,23,24,25,
             24,25,26,27,28,29,
             28,29,30,31,32,1
            ]

    _PBox = [16,   7,  20,  21,
             29,  12,  28,  17,
              1,  15,  23,  26,
              5,  18,  31,  10,
              2,   8,  24,  14,
             32,  27,   3,   9,
             19,  13,  30,   6,
             22,  11,   4,  25]

    _invPer = [ 40, 8, 48, 16, 56, 24, 64, 32,
                39, 7, 47, 15, 55, 23, 63, 31,
                38, 6, 46, 14, 54, 22, 62, 30,
                37, 5, 45, 13, 53, 21, 61, 29,
                36, 4, 44, 12, 52, 20, 60, 28,
                35, 3, 43, 11, 51, 19, 59, 27,
                34, 2, 42, 10, 50, 18, 58, 26,
                33, 1, 41, 9, 49, 17, 57, 25
            ]


    def __init__(self):
        #I am going to have it as nothing at the current moment, and build
        #it up as time goes
        self.__key = None 
        self.__message = None
        self.__encryption  = encryptionStatus.decrypted
        self.__paddedZeros = 0

    #ACCESSOR METHODS:
    @property
    def key(self): 
        return self.__key

    @property
    def message(self):
        return self.__message


    @property
    def encryption(self):
        return self.__encryption


    #MUTATOR METHODS:
    @key.setter
    #TODO: I am also going to be assuming that the user will be inputting a word as their key
    def key(self, newKey):
        #TODO: you will need to be able to do some padding or chopping depending on what the user has inputted into your program
        #TODO: you will need to do the same error checking for the other function to make sure that you're reading in a binary number, otherwise you will need to convert it to binary
        #trying to determine if binary number already 
        try: 
            binaryNum = int(newKey, 2)
        except ValueError:
            #not a binary number and must be converted to a binary number
            binaryNum = []
            for char in newKey:
                binaryNum.append(self._char2Binary(char))
            #making it to whole entire string 
            binaryNum = "".join(binaryNum)
            newKey = binaryNum

        keySize = len(newKey)
        #we will have to do some padding 
        if keySize <= 64:
            newKey = self._padBinaryNum(newKey, 64)
        else:
            newKey = newKey[:64]
            #we will have to do some chopping, just going to take first 64 bits


        #sanity check, to ensure that everything was done correctly
        self.__validateBlockLen(newKey, 64)
        self.__key = newKey

    @message.setter
    def message(self, newMessage):
        self.__message = newMessage

    #deleter methods, to clear the values which have being set already 
    @key.deleter
    def key(self):
        del self.__key

    @message.deleter
    def message(self):
        del self.__message

    @encryption.deleter
    def encyption(self):
        self.__encryption = encryptionStatus.decrypted



    def encrypt(self):
        #all the preprocessing of the message will occur here, hence dividing
        #the message into the appropriate 64 bit block sizes

        #checking on how much we will need to pad the message by for each block
        #to be represented by a 64 block stream

        #how many bits will need to be padded to make the message be a multiple of 64
        self.__paddedZeros = len(self.__message) % 64
        self.__message = self._padBinaryNum(self.__message, 64)

        #we know that all the values are going to be multiples of 64 hence,
        #making all the starting  values of the function
        startVal = [xx for xx in range(0, len(self.__message), 64)]

        #the blocks which will have to be created 
        blocks = self._createBlocks(self.__message, startVal)

        #encrypting each and every single block which was created, and joining
        #them back into one big string
        encryptedBlocks = []
        for block in blocks:
            encryptedBlocks.append(self.__encryptBlock(block))

        encryptedMssg = "".join(encryptedBlocks)
        self.__message = encryptedMssg
        self.__encryption = encryptionStatus.encrypted
        self.__key = None

        return encryptedMssg

    #Public methods
    def __encryptBlock(self, inMessage):
        #if all the appropriate information hasn't being loaded into the object
        #we can't start decrypting the message
        if inMessage == None:
            raise  EncryptionError("ERROR: message hasn't been set")

        if self.__key == None:
            raise EncryptionError("ERROR: key hasn't been set")

        if (self.__encryption == encryptionStatus.encrypted):
            raise  EncryptionError("ERROR: message has already been encrypted")

        #STEP 1: creating the 16 sub keys, each of which is 48 bits long
        permutatedKeys = self._keyschedule()
        
        #STEP 2: Encode each 64 bit block of data
        initalPermutationMessg = self._applyPermutation(inMessage, self._IP)
        leftMssg, rightMssg = self._splitKeys(initalPermutationMessg)

        #applying the sixteen rounds of feistel

        #for pos, key  in enumerate(permutatedKeys):
        for currPos in range(0,16):
            leftMssg, rightMssg = self._feistelNetwork(leftMssg, rightMssg, permutatedKeys[currPos])


        #swapping the left and the right messages
        encryptedMssg = rightMssg + leftMssg

        #applying the final inverse permutation on the given message
        inMessage = self._applyPermutation(encryptedMssg, self._invPer)


        return inMessage

    def _createBlocks(self,inBinary,startVal):
        blocks = []
        for pos, start in enumerate(startVal):
            #if they is going to be only one block, we just ant to return that
            if len(startVal) == 1:
                blocks.append(inBinary)
            elif pos < len(startVal) - 1:
                blocks.append(inBinary[start:startVal[pos+1]])

        return blocks

    def decrypt(self):
        #all the processing of splitting the cipher text into 64 blocks will
        #occur and happen here

        startVal = [xx for xx in range(0, len(self.__message) , 64)]

        #the blocks for the cipher text
        blocks = self._createBlocks(self.__message, startVal)

        #decrypting each and every single block which was created and  joining
        #them back into one big string
        decryptedBlocks = []
        for block in blocks:
            decryptedBlocks.append(self.__decryptBlock(block ))

        decryptedMssg = "".join(decryptedBlocks)
        self.__message = decryptedMssg[self.__paddedZeros:]
        self.__encryption = encryptionStatus.decrypted
        self.__key = None

        return decryptedMssg[self.__paddedZeros:]


    def __decryptBlock(self, inCipher):

        if inCipher == None:
            raise DecryptionError("ERROR: message hasn't being set")

        if self.__key == None:
            raise DecryptionError("ERROR: key hasn't being set")

        if (self.__encryption == encryptionStatus.decrypted):
            raise DecryptionError("ERROR: message hasn't been encrypted")


        #STEP 1: re-creating the 16 sub keys, each of which is 48 bits  long
        #generating the key sets which we produced in the encryption set
        permutatedKeys = self._keyschedule()
        #reversing the order of keys produced, so we can do the fesitel network
        #to decrypt the cipher produced by the encrypt function
        permutatedKeys.reverse()

        #STEP 2: Decoding each 65 bit block of data

        decryptedMssgPermutated  = self._applyPermutation(inCipher, self._IP)
        leftMssg, rightMssg = self._splitKeys(decryptedMssgPermutated)

        #applying the 16 round of message on the reversed keys
        for currPos in range(0,16):
            leftMssg, rightMssg = self._feistelNetwork(leftMssg, rightMssg,\
                    permutatedKeys[currPos])

        decryptedMssg = rightMssg + leftMssg
        inCipher = self._applyPermutation(decryptedMssg, self._invPer)

        return inCipher

    def loadFile(self, fileName):
        with open(fileName, "r") as inStrm:
            #read the file in as a gigantic string
            fileContents = inStrm.readlines()

        #I want the file contents as one giant string
        fileContents = "".join(fileContents)
        binaryFileContents = []
        for char in fileContents:
            binaryFileContents.append(self._char2Binary(char))

        #making this back into one giant string again
        binaryFileContents = "".join(binaryFileContents)
        self.__message = binaryFileContents

        return binaryFileContents

    def saveFile(self, fileName):
        binaryMessage = self._padBinaryNum(self.__message, 8)
        startVal =  [xx for xx in range(0, len(binaryMessage), 8)]
        hexGroups = self._createBlocks(binaryMessage, startVal)

        #saving the file as hexadecimal digits
        if (self.__encryption == encryptionStatus.encrypted):
            #grouping the binary into groups of 8 bits
            #grouping the current message with each group having 8 bits
            with open(fileName, "w" ) as outStrm:
                for binary in hexGroups:
                    outStrm.write(self._binary2Hexadecimal(binary))
        else:
            with open(fileName, "w") as outStrm:
                for binary in hexGroups:
                    outStrm.write(self._binary2Char(binary))


    #TODO: I think that he maths in here is going to be a little bit wrong
    def _padBinaryNum(self, inBinary, requiredLen):
        #I am just trying out this implementation as it gives you the actual required bits
        
        remainder = abs(len(inBinary) - requiredLen)
        #TODO: come back and delete this line of code as you don't need it anymore
        #remainder = len(inBinary) % requiredLen
        bits = "".join(["0" for xx in range(0,remainder)])
        #padding the front of the message with the required zeros
        inBinary = bits + inBinary
        return  inBinary

    def _keyschedule(self):
        permutatedKeys = []

        permutatedKey = self._applyPermutation(self.__key, self._PC_1)

        #splitting the keys to get the right and the left halves
        keys = self._splitKeys(permutatedKey)

        #applying and getting the sixteen rounds of keys
        sixteenRoundKeys  =  self._createKeys(keys) 

        #applying the second permutation on the keys
        for key in sixteenRoundKeys:
            permutatedKeys.append(self._applyPermutation(key, self._PC_2))

        return permutatedKeys



    def laodMessageAsFile(self, fileName): 
        pass


    def _binary2Hexadecimal(self, inBinary):
        decimalNum =  int(inBinary,2)
        hexNum = hex(decimalNum)

        return hexNum[2:]

    def _hexadecimal2Binary(self, inHex):
        decNum = int(inHex, 16)
        #I want these numbers in sets of 4
        binaryNum = format(decNum, "b")

        return binaryNum


    """
    INPUT: Data(String)
    Output: data left shifted given the shifting scheduling which was
    defined above

    PURPOSE:
    """
    def __apply_left_shifts(data):
        shiftedData = ""
        if len(data) != 16:
            raise DESBlockError("ERROR: the length of the data must be 16 bits")

        for pos, value in enumerate(__leftShifts):
            pass

        return shiftedData




    """
    INPUT: data (what you want to apply the permutation on)
           table (the table which you're applying the permutation based on
    OUTPUT: perTable: a new permutated data string which will be done given the i
    inputted table into the program

    PURPOSE:
    """
    def _applyPermutation(self, data, table):
        #making a string the same size of data with all 0's
        retPerm = []


        for pos, value in enumerate(table):
            retPerm.append(data[value -1 ])

        #making it a clean string so we pass it back to other functions
        retPerm = "".join(retPerm)

        return retPerm


    def _splitKeys(self, permutatedKey):
        midIndex = len(permutatedKey) // 2
        #the left key will be stored in first index and right key will be stored
        #in the second index of returned list
        return [permutatedKey[:midIndex] , permutatedKey[midIndex:]]

    def _createKeys(self,keySides):
        leftKey  = deque([ii for ii in keySides[0]])
        rightKey = deque([ii for ii in keySides[1]])
        #they're going to be a total of 16 keys returned from the concatenation 
        #of the right and left side of the shifted key, based on the previous 
        #key and left shifting schedule
        allKeys = []

        for shift in self._leftShifts:
            leftKey.rotate(shift*-1)
            rightKey.rotate(shift*-1)
            #making the rotated left and right side a single string
            leftStr = "".join([ii for ii in leftKey])
            rightStr = "".join([ii for ii in rightKey])
            allKeys.append(leftStr + rightStr)




        return allKeys

    def _char2Binary(self, inChar):
        intChar = ord(inChar)
        binaryNum = ""

        #we want this to be easily represented in hexadecimal, and
        #we don't want information to be lost in the process. Hence,
        #requiring that each character will be represented by 8 bits. As
        #that will encompass all characters on the ASCII table
        binaryNum = self._calcInt2Binary(intChar, 8)

        return binaryNum

    def  _binary2Char(self, inBinary):
        decNum = int(inBinary, 2)
        return chr(decNum)
    
    
    def _calcInt2Binary(self, intNum, requiredLen):
        return format(intNum, "0>"+str(requiredLen)+"b")

    #padding to the left of the binary number, as that will not increase the
    #number of  the binary number
    def _padBinary(self, inBinary, padNum):
        padDigits = [str(xx) for xx in range (0, padNum)]
        padDigits = "".join(padDigits)
        return padDigits + inBinary
    
    def _calcBinary2Int(self, inBinary):
        return int(inBinary, 2)
            

    def _xor(self, streamOne, streamTwo):

        if len(streamOne) != len(streamTwo):
            raise DESBlockError("ERROR: xor stream blocks must be the same length")

        result = ""
        for bitOne, bitTwo in zip(streamOne, streamTwo):
            result = result + str(int(bitOne) ^ int(bitTwo))

        return  result

    #applying the feistel network based on the illustration given on slide 15 
    #of the lecture slides
    def _feistelNetwork(self, leftStream, rightStream, key):
        rightStreamFunc = self._feistelNetworkFunction(rightStream, key)

        #Xoring the result from the function and the left stream of the data 
        newRight = self._xor(rightStreamFunc, leftStream)
        newleft = rightStream

        return newleft, newRight

    def _feistelNetworkFunction(self, rightStream, key):
        #expanding the right stream bits from 32 bits to 48 bits
        sBoxAppliedFuncList = []
        expandedStream = self._applyPermutation(rightStream, self._EBox)

        if len(expandedStream) != 48:
            raise DESBlockError("ERROR: Feistel network expansion failed"+
                    " keys must be 48 bits. %s bits has being found" % len(expandedStream))

        #xoring the expanded data with the current key, and calculating the
        #following formula K_n + E(R_(n-1)
        xorRes = self._xor(expandedStream, key)
        grouped8s = self._group48Block(xorRes)

        for sBoxNum, binary in enumerate(grouped8s):
            currSBox = self.__SBox[sBoxNum]
            rowNumBinary = self._calculateSBoxRow(binary)
            colNumBinary = self._calculateSBoxCol(binary)
            rowNumInt = self._calcBinary2Int(rowNumBinary)
            colNumInt = self._calcBinary2Int(colNumBinary)

            value = currSBox[rowNumInt][colNumInt]

            sBoxAppliedFuncList.append(self._calcInt2Binary(value,4))

        #the final step of the function, applying permutations of re-calculated
        #values

        sBoxAppliedFuncStr  = "".join(sBoxAppliedFuncList)

        #sanity check

        assert len(sBoxAppliedFuncStr) == 32, "the applied function bits must"+\
        " be 32 bits long but %s bits found" % len(sBoxAppliedFuncStr)
        
        return self._applyPermutation(sBoxAppliedFuncStr, self._PBox)

    def _calculateSBoxRow(self, inBlock):
        self.__validateBlockLen(inBlock, 6)
        return inBlock[0] + inBlock[-1]

    def _calculateSBoxCol(self, inBlock):
        self.__validateBlockLen(inBlock, 6)
        return inBlock[1:-1]

    def _group48Block(self, inBlock):

        if(len(inBlock) != 48):
            raise DESBlockError("ERROR: the bits count must be 48 so six groups"+
            " can be made from the current data")

        #we always know it's going to be 8 groups of six hence, we can hard
        #code the running of this functio
        startValues = [xx for xx in range(0, 49, 6)]

        #we always know that the end is going to be 8 elements away
        #return [inBlock[start: start + 6] for start in startValues]
        return [inBlock[start:startValues[pos+1]] for pos, start in \
                enumerate(startValues) if pos < len(startValues) -1]

    def _calculateAddressSBox(self, inAddress):
        if (len (inBlock) != 6):
            raise DESBlockError("ERROR: the address must be a total of 6 bits")

    def __validateBlockLen(self, inBlock, size):
        if (len (inBlock) != size):
            raise DESBlockError("ERROR:block must be %s bits long. %s length found" % (size, len(inBlock)))

