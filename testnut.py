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
        #nameDict = eval("{\"" + splitLine[1] + "\":{'SearchTerms':" + splitLine[2] + "}}")
        #print(nameDict)
        
        nameList.append(splitLine[1])
        searchList.append(eval(splitLine[2]))

        count += 1
        if count > 9:
            break
    else:
        ready = True



#print(nameDict["Oatmeal"]["SearchTerms"])
print(nameList)

line = 0
while line < len(nameList):
    print(nameList[line])
    print(searchList[line])
    line += 1

