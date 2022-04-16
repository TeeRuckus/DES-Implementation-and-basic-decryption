import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.ticker import PercentFormatter
from LetterFrequency import *
from AffineCipher import *


#TODO: you will need to  have a script which will install the required things 
#which you will need for this assignment

def main():
    #attackLetterFrequency()
    bruteForceAttack("cipher-test.txt")

    #content = read_file("cipher-test.txt")
    #print(content)
    """
    key = 3
    mssg = "attack at dawn"
    #mssg = mssg.lower()
    mssg = encryption(mssg, 3, key)
    print(mssg)

    print("de-decrypting message again")
    mssg = decryption(mssg,3, key)
    print(mssg.lower())
    """

def bruteForceAttack(fileName):
    allAttempts = bruteForceAttempts(fileName)
    dictonary = read_file("dictonary.txt")
    results = analyseAttempts(allAttempts, dictonary)
    
    #extracting all the scores
    scores = [int(xx.split(" ")[0]) for xx in results]
    indexMax = np.argmax(scores)

    print("Key combination", results[indexMax])
    print("Decrypting cipherText.....")
    keys = results[indexMax].split(" ")
    keys = keys[1:]
    print(keys)
    keyA = int(keys[0].split("=")[1])
    keyB = int(keys[1].split("=")[1])

    cipher = read_file(fileName)
    wordsCipher = []

    for word in cipher:
        if word.isalpha():
            wordsCipher.append(decryption(word, keyA, keyB).lower())
        else:
            wordsCipher.append(word)

    wordsCipher = " ".join(wordsCipher)
    print(wordsCipher)


def analyseAttempts(allAttempts, dictonary):
    resultsOfAttempts = []
    keyCombination = allAttempts[:2]

    for attempt in allAttempts:
        score = 0
        for word in dictonary:
            word = word.strip().upper()
            score += attempt.count(word)

        keyCombination = attempt.split(" ")[:2]
        keyCombination = " ".join(keyCombination)
        #packet = zip(str(score), keyCombination)
        packet = str(score) + " " + keyCombination
        resultsOfAttempts.append(packet)

    return resultsOfAttempts

def bruteForceAttempts(fileName):
    decryptedFiles = []
    decryptedAttempts = []

    words = read_file(fileName)

    for a in range(0,26):
        for shift in range(0,26):
            currAttempt = []
            for word in words:
                attempt = decryption(word, a, shift)
                currAttempt.append(attempt)

            #saving the current decryption attempt
            currAttempt.insert(0, "b=%s" % shift)
            currAttempt.insert(0, "a=%s" % a)
            #making it into one big string
            currAttempt = " ".join(currAttempt)
            decryptedAttempts.append(currAttempt)

    return decryptedAttempts



def attackLetterFrequency():
    labelsBase, frequencyBase = letterFrequencyAnlaysis("inputText.txt")
    labelsCipher, frequencyCipher = letterFrequencyAnlaysis("cipher-test.txt")

    plotLetterFrequencyAnlaysis(labelsBase, frequencyBase, "Base comparison text")
    plotLetterFrequencyAnlaysis(labelsCipher, frequencyCipher, "Cipher  plot")
    #plt.show()

    #sorting the letters from the base comparison and the cipher text
    pairsBase = sorted(zip(labelsBase, frequencyBase), key=lambda x: x[1], reverse=True)
    pairsCipher = sorted(zip(labelsCipher, frequencyCipher), key=lambda x: x[1], reverse=True)

    lettersBase  = [xx[0] for xx in pairsBase]
    lettersCipher = [xx[0] for xx in pairsCipher]
    #creating a look up table for the cipher text
    lookUpCipher = dict(zip(lettersCipher, lettersBase))
    decrypted = decryptText(lookUpCipher, "cipher-test.txt")
    decrypted = correction(decrypted)

    with open("out.txt", "w") as outStrm:
        outStrm.write(decrypted)

def letterFrequencyAnlaysis(fileName):
    words = read_file(fileName)
    frequency = count_letters(words)
    labels = [chr(x + 65) for x in range(0,26)]

    return labels, frequency






def plotLetterFrequencyAnlaysis(labels, frequency, titleName):
    plt.figure()
    plt.xlabel("Alphabets")
    plt.ylabel("Frequency")
    plt.title("Letter Frequency Analysis: " + titleName)
    plt.bar(labels, frequency)
    plt.savefig("letter frequency")




if __name__ == "__main__":
    main()
