from collections import deque
import numpy as np

class DES(object):
    #this is going to represent the initial permutation of the algorithm
    #TODO: you will already have this, you should come back and delete this out
    #of your code
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
            # S1 - Checked
            [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
             0, 15, 7, 4, 14, 2, 13, 10, 3, 6, 12, 11, 9, 5, 3, 8,
             4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
             15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],

            # S2 - Checked
            [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
             3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
             0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
             13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],

            # S3 - Checked
            [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
             13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
             13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
             1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],

            # S4 - Checked
            [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
             13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
             10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
             3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],

            # S5 - Checked
            [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
             14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
             4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
             11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],

            # S6 - Checked
            [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
             10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
             9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
             4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 10, 0, 8, 13],

            # S7 - Checked
            [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
             13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
             1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
             6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],

            # S8 - Checked
            [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
             1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 10, 14, 9, 2,
             7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 10, 15, 3, 5, 8,
             2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 9, 3, 5, 6, 11],
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


    def __init__(self):
        #I am going to have it as nothing at the current moment, and build
        #it up as time goes
        pass

    #ACCESSOR METHODS:


    #MUTATOR METHODS:
    def encypt(self, passage):
        pass

    def decrypt(self, cipher):
        pass

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
    #TODO: you will need to apply header guards to be able to protect
    #this function from having the wrong inputted key size, and the wrong
    #inputted messages size as well
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

    #that it's going to work and to do what it's supposed to do
    def _char_to_binary(self, inChar):
        intChar = ord(inChar)
        binaryNum = ""

        while intChar > 0:
            remindar = intChar % 2
            intChar = intChar // 2

            if remindar == 0:
                binaryNum = "0" + binaryNum
            else:
                binaryNum = "1" + binaryNum

        return binaryNum

    def _xor(self, streamOne, streamTwo):

        result = ""
        for bitOne, bitTwo in zip(streamOne, streamTwo):
            result = result + str(int(bitOne) ^ int(bitTwo))

        return  result

