import json

from PyDictionary import PyDictionary

f = open('fiveletters.txt')
data = f.readlines()
newData = []
for eachLine in data:
    newData.append(eachLine.split("\n")[0])
data = newData
newData = None
dictionary = PyDictionary()
greyLetters = []
f.close()
alphabet = "abcdefghijklmnopqrstuvwxyz"
numOfLetters = 5
print("First Word to Type: SALET")
curWord = "salet"
knownWord = []
yellowLetters = []
bannedWords = set()
main_list = set(data)
x = 0
possibleWords = [[]]
commonLetters = []

while x < int(numOfLetters):
    knownWord.append("-")
    x += 1

def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]


def returnValues(e):
    return e[1]

def isEqualIndex(str, letter):

    if letter in knownWord:
        if str[knownWord.index(letter)] == letter:
            newString = str[:knownWord.index(letter)] + str[knownWord.index(letter)+1:]
            print(newString)
            if letter not in newString:
                return True
            else:
                return False
        else:
            if letter not in str:
                return True
    else:
        if letter not in str:
            return True

def removeGreyWords(listOfWords, letter):
    global main_list
    global knownWord
    newList = []
    knownString = ""
    # print("Removing " + letter)
    for eachLetter in knownWord:
        knownString += eachLetter

    newList = [x for x in listOfWords if isEqualIndex(x, letter)]

    main_list = newList


def removeNonYellowWords(listOfWords, letter):
    global main_list
    newList = [x for x in listOfWords if letter[0] in x]
    newerList = [i for i in newList if letter[1] not in find(i, letter[0])]
    main_list = newerList


def findCommonLetters():
    f2 = open('spaceheater.json')
    letterData = json.load(f2)
    for eachData in letterData:
        commonLetters.append(eachData["Ltr"])


global findCount
findCount = 0


def FindWords():
    global findCount
    global main_list
    global knownWord
    global greyLetters

    print("Counter: " + str(findCount))
    if findCount == len(knownWord):
        # print(listOfWords)
        return main_list
    elif knownWord[findCount] == "-":
        findCount += 1
        FindWords()
    else:
        print("Retrieving " + knownWord[findCount] + " from list")
        newList = [i for i in main_list if knownWord[findCount].lower() == i[findCount]]
        findCount += 1
        print(findCount)
        x = 0
        main_list = newList
        FindWords()
        x += 1


def calculateValue(word):
    f2 = open('spaceheater.json')
    f5 = open("bigramfrequncies.txt", "r")
    bigramFreq = f5.readlines()
    values = []
    prevLetter = ""
    letterData = json.load(f2)
    x = 0
    while x < len(word):
        gramFloat = [gram.split(": ")[1].split("\n")[0] for gram in bigramFreq if
                     prevLetter + word[x] + "-" + str(x - 1) in gram]
        if gramFloat == []:
            gramFloat = [0]
        if word[x] == prevLetter:
            values.append(0)
        else:
            for eachData in letterData:
                if word[x] in eachData["Ltr"]:
                    if x == 0:

                        values.append(eachData["1st"] * (1+float(gramFloat[0]) * 10))
                    if x == 1:
                        values.append(eachData["2nd"] * (1+float(gramFloat[0]) * 10))
                    if x == 2:
                        values.append(eachData["3rd"] * (1+float(gramFloat[0]) * 10))
                    if x == 3:
                        values.append(eachData["4th"] * (1+float(gramFloat[0]) * 10))
                    if x == 4:
                        values.append(eachData["5th"] * (1+float(gramFloat[0]) * 10))

        prevLetter = word[x]

        x += 1

    average = sum(values) / len(values)

    f3 = open('wordlewords.txt')

    for eachLine in f3.readlines():
        if word in eachLine:
            average = average + 0.5

    f2.close()
    f3.close()
    f5.close()
    return average

def reCalculateValues(word):
    f3 = open('wordfreq.txt')
    for eachLine in f3.readlines():
        if word in eachLine:
            return 1

findCommonLetters()

j = 0
while j < len(knownWord):
    knownWord[j] = "-"
    j += 1

while True:
    possibleWords = []
    userInput = input("Give positions (2y, 3g): ").split(", ")
    cycle = 0
    i = 0
    print(userInput)
    if userInput != [""]:

        while i < len(userInput):
            eachPoint = i
            if userInput[i][1] == "g":
                knownWord[int(userInput[i][0])] = (curWord[int(userInput[i][0])])
                for eachYellow in yellowLetters:
                    if curWord[int(userInput[i][0])] in yellowLetters:
                        yellowLetters.remove(eachYellow)
            if userInput[i][1] == "y":
                yellowLetters.append([curWord[int(userInput[i][0])], int(userInput[i][0])])

            i += 1

    print(knownWord)
    p = 0
    while p < len(curWord):
        if curWord[p] not in knownWord[p]:
            greyLetters.append(curWord[p])
        p+=1
    print(greyLetters)

    for eachYellow in yellowLetters:
        if eachYellow[0] in greyLetters:
            greyLetters.remove(eachYellow[0])

            print(greyLetters)

    possibleWords = []
    x = 0

    y = 0
    goodWords = []

    findCount = 0
    FindWords()

    numOfUnknowns = 0

    for eachLetter in knownWord:
        if eachLetter == "-":
            numOfUnknowns += 1

    if numOfUnknowns == numOfLetters:
        main_list = data

    for eachLetter in greyLetters:
        removeGreyWords(main_list, eachLetter)
    for eachYellow in yellowLetters:
        removeNonYellowWords(main_list, eachYellow)

    for eachWord in main_list:
        if eachWord not in bannedWords:
            possibleWords.append([eachWord, calculateValue(eachWord)])

    # print(possibleWords)

    if len(possibleWords) < numOfLetters:
        x = 0
        while x<len(possibleWords):
            if reCalculateValues(possibleWords[x][0]) == 1:
                possibleWords[x][1] + 0.5
            x+=1

    x = 0
    topValue = [0, 0]
    while x < len(possibleWords):

        if possibleWords[x][1] > topValue[1]:
            topValue[0] = x
            topValue[1] = possibleWords[x][1]
        x += 1

    possibleWords.sort(reverse=False, key=returnValues)
    print("Possible words: ")
    for eachWord in possibleWords:
        print(eachWord)
    inputOver = input("Is this right? (Y or N) ")
    inputOver2 = ""
    while True:
        inputOver2 = input("What word did you use? ")
        if inputOver2 in main_list:
            break

    if inputOver == "N":
        bannedWords.add(inputOver2)
    if inputOver == "Y":
        break

    curWord = inputOver2
