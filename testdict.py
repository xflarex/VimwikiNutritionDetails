nutritionFile = open("opennutrition.tsv", "r+")
nutFile = nutritionFile.readlines()

commonQuantity = 0.0
metricQuantity = 0

quantityDict = {}
infoDict = {}
nameDict = {}

nameList = []
searchList = []

count = 0
ready = False
for tempLine in nutFile:
    if ready == True:
        splitLine = tempLine.split("\t")
        quantityDict.update(eval(splitLine[6]))
        #infoDict.update(eval(splitLine[7]))
        #print("2")
        #print(splitLine[1])
        #print(splitLine[2])
        nameDict.update(eval("{\"" + splitLine[1] + "\":{'SearchTerms':" + splitLine[2] + "}}"))
        #print(nameDict)


        count += 1
        if count > 13000:
            break
    else:
        ready = True

print(nameDict["Garlic Oil by Scotts Food Products"]["SearchTerms"])

