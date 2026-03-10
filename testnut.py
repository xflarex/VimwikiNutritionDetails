nutritionFile = open("opennutrition.tsv", "r+")
nutFile = nutritionFile.readlines()


quantityDict = {}
infoDict = {}

nameList = []
searchList = []

count = 0
ready = False
for tempLine in nutFile:
    if ready == True:
        splitLine = tempLine.split("\t")
        quantityDict.update(eval(splitLine[6]))
        infoDict.update(eval(splitLine[7]))

        nameList.append(splitLine[1])

        count += 1
        if count > 9:
            break
    else:
        ready = True

print(nameList)
print("\n")
print(quantityDict)

ingredient = 'white rice'
ingredient = ingredient.title()

count = 0
for name in nameList:
    if ingredient == name:
        print("Found", count)
    count += 1
