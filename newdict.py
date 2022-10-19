

f = open('wordlewords.txt')

f1 = open("bigramfrequncies.txt", "w")
characters = []
times = []
for eachLine in f:
    prevLetter = ""
    print(eachLine.split("\n")[0])
    # for eachChar in eachLine.split("\n")[0]:
    x = 0
    while x < len(eachLine.split("\n")[0]):
        if prevLetter != "":
            if characters.count(prevLetter+eachLine.split("\n")[0][x] + "-" + str(x-1)) == 0:
                characters.append(prevLetter+eachLine.split("\n")[0][x] + "-" + str(x-1))
                times.append(1)
            else:
                oldTime = times[characters.index(prevLetter+eachLine.split("\n")[0][x] + "-" + str(x-1))]
                times.pop(characters.index(prevLetter+eachLine.split("\n")[0][x] + "-" + str(x-1)))
                times.append(oldTime+1)

        prevLetter = eachLine.split("\n")[0][x]
        x+=1
print(characters)
print(times)
sumOfTimes = 0
for eachTime in times:
    sumOfTimes += eachTime

for char in characters:
    f1.write(char + ": " + str(times[characters.index(char)] / sumOfTimes * 100) + "\n")


f1.close()

