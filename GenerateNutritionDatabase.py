nutritionFile = open("opennutrition.tsv", "r+")
nutFile = nutritionFile.readlines()

uniqueIDList = []
nameList = []
searchList = []

completeDict = {}

def load_name_list():
    count = 0
    ready = False

    for nut in nutFile:
        if ready == True:
            splitLine = nut.split("\t")
            nameTerm = ('name',)
            nameDict = dict.fromkeys(nameTerm,splitLine[1])
            print(nameDict)
            searchTerm = ('searchTerm',)
            searchDict = dict.fromkeys(searchTerm,splitLine[2])
            servingTerm = ('servingTerm',)
            servingDict = dict.fromkeys(servingTerm,splitLine[6])
            nutrientTerm = ('nutrientTerm',)
            nutrientDict = dict.fromkeys(nutrientTerm,splitLine[7])
            labelTerm = ('labelTerm',)
            labelDict = dict.fromkeys(labelTerm,splitLine[8])

            completeTerm = "('" + splitLine[0] + "',)"
            completeTerm = eval(completeTerm)
            #print(completeDict)
            dictList = (nameDict, searchDict, servingDict, nutrientDict, labelDict)
            completeDict.update(dict.fromkeys(completeTerm, dictList))
            #print(completeDict)
            for item in completeDict:
                print("\n")
                print(item)

            count += 1
            if count >= 10:
                break
        else:
            ready = True

load_name_list()
print(completeDict['fd_2dObzdqa6o2J'])
#print(completeDict)
