import math
import hashlib
import bitarray

def loadRock():
    loadedArr = []
    with open("rockyou.ISO-8859-1.txt", "r", encoding="ISO-8859-1") as file:
        for line in file:
            word = line.strip()
            loadedArr.append(word)
    print(loadedArr[:10], "\n")
    return loadedArr

def loadDict():
    dictArr = []
    with open("dictionary.txt", "r", encoding="ISO-8859-1") as file:
        for line in file:
            word = line.strip()
            dictArr.append(word)
    print(dictArr[:10])
    return dictArr

loadRock()

loadDict()