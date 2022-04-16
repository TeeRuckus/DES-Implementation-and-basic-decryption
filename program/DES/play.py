

with open("res.txt", "r") as inStrm:
    fileConents  = inStrm.readlines()

#fileConents = "".join(fileConents)
for pair in fileConents:
    if len(pair) != 3:
        print(pair)
    
