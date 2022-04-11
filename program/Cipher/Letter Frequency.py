import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.ticker import PercentFormatter
from functions import *

def main():
    letter_frequency_anlaysis("inputText.txt")


def letter_frequency_anlaysis(fileName):
    words = read_file(fileName)
    frequency = count_letters(words)
    labels = [chr(x + 65) for x in range(0,26)]
    plt.xlabel("Alphabets")
    plt.ylabel("Frequency")
    plt.title("Letter Frequency Analysis")
    plt.bar(labels, frequency)
    plt.savefig("letter frequency")
    plt.show()




if __name__ == "__main__":
    main()
