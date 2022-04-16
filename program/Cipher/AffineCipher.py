
def encryption(mssg, a, shift):
    return  "".join([encryptChar(x, a, shift) for x in mssg.upper() if  x.isalpha()])

    """
    #the equation which you will have for the shift cipher
    # c = (am + k) mod 26
    lettersNumbers = break_string(mssg)
    #shifting all the letters over by one
    lettersShifted = [(x + shift) % 26  for x in lettersNumbers]
    #converting the cipher back into a message
    lettersCharacaters = [chr(x + ord("a")) for x in lettersShifted]
    return "".join(lettersCharacaters)
"""

def encryptChar(inChar, a, shift):
    #E = (a*x + b) % 26
    return chr(((a * (ord(inChar) - ord('A')) + shift) %  26) + ord('A'))

def decryption(mssg, a, shift):
    return "".join([decyptChar(xx, a, shift) for xx in  mssg])

    """
    # the equation which you will have for the shift cipher
    # (c - k) mod 25
    lettersNumbers = break_string(mssg)
    lettersShifted = [(x - shift) % 26 for x in lettersNumbers]
    lettersCharacaters = [chr(x + ord("a")) for x in lettersShifted]
    return "".join(lettersCharacaters)
"""

def decyptChar(inChar, a, shift):
    #D = invMod * (c - b) mod 26
    #some numbers will not have an inverse modulo, so we will skip these
    ret = " "
    try:
        ret = chr((invMod(a, 26) * (ord(inChar) - ord('A')- shift) % 26) + ord('A'))
    except TypeError:
        #can't decrypt using this combination, so we should just skip
        pass

    return ret

def  gcdExt(a, b):
    # Base Case 
    if a == 0 :
        return b,0,1
    #recursive call to find the GCD
    gcd,x1,y1 = gcdExt(b%a, a)
    x = y1 - (b//a) * x1
    y = x1

    return gcd,x,y

def invMod(a, m):
    g, x, y = gcdExt(a, m)
    retVal = None

    if g == 1:
        retVal = x % m

    return retVal

def break_string(mssg):
    pass
    """
    letters = [x for x in mssg]
    #ret = [ord(x) - ord("a") for x in letters if x.isalpha()]
    ret = [ord(x) - ord("a") for x in mssg]
    return ret

    #return [ord(x) - ord("a") if x.isalpha else " " for x in letters]
    """




