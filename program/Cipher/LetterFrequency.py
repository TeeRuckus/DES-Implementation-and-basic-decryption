import numpy as np
#from autocorrect import Speller

#Read files, and reads all the worlds as lists
def read_file(fileName):
    words = []
    with open(fileName, "r")  as  inStrm:
        for line in inStrm:
            words.extend(line.split(" "))

    return words


#Counts letters and puts them in the right place if they're going to between
#A - Z
def count_letters(words):
    #going to be analysing based on the ASCII code of the letters
    #all the alphabet letters
    alphabet = np.zeros(26)
    for word in words:
        word = word.upper()
        for letter in word:
            #since the ASCII code for the letters are going to be between
            #65 and 90. Subtracting 65 to make 'A' the 0th index of the array
            #till the 25th index of Z
            pos = ord(letter) - 65
            #we only care about alphabet letters for now
            if pos >= 0 and pos <= 25:
                alphabet[pos] += 1

    return alphabet

def decryptText(lookUpTable, fileName):
    decrypted = []
    with open(fileName, "r") as inStrm:
        for line in inStrm:
            decryptedLine = decryptLine(line, lookUpTable)
            decrypted.append(decryptedLine)

    #returning everything as a giant string
    return "".join(decrypted)

def decryptLine(inLine, lookUpTable):
    newLine = []
    for char in inLine:
        #all the keys are going to be in upper cases
        char = char.upper()
        #the values of the dictionary are going to be in upper case as well
        try:
            newLine.append(lookUpTable[char].lower())
        except KeyError:
            #ignoring any key errors, as this is going to be characters which
            #are not going to be included in the original key frequency analysis
            #attack, and just adding the character the way it is to the line
            newLine.append(char)

    #making the new line one big string
    return "".join(newLine)

"""
def correction(inPassage):
    words = inPassage.split(" ")
    correctedPassage = []
    spell = Speller(lang='en')

    for word in words:
        newWord = spell(word)
        correctedPassage.append(newWord)

    return " ".join(correctedPassage)
"""




