


def char_to_binary(inChar):
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









