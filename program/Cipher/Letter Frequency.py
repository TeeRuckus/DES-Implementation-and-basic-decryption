import numpy as np

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




