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
            keyString = ('name',)
            nameDict = dict.fromkeys(keyString,splitLine[1])
            searchTerm = ('searchTerm',)
            searchDict = dict.fromkeys(searchTerm,splitLine[2])
            print(nameDict)
            print(searchDict)
            #serving, nutrient, label
            #uniqueIDList.append(splitLine[0])
            #nameList.append(splitLine[1].lower())
            #searchList.append(eval(splitLine[2]))
            for line in splitLine:
                print("\n", line)

            count += 1
            if count >= 10:
                break
        else:
            ready = True

load_name_list()

#nestedKeys = ('uniqueID', 'name', 'searchTerm', 'quantity', 'ingredients', 'label')
#nestedDict = dict.fromkeys(nestedKeys)
#completeDict = dict.fromkeys(uniqueIDList, nestedDict)
#print(completeDict)
#print(uniqueIDList)
#print(nameList)

#completeDict['fd_XSd7Te973XKX']['name'] = "broccoli"
#print(completeDict['fd_XSd7Te973XKX']['name'])
#print(completeDict)

# Dict of unique ids and all others as single value
# name : broccoli 
# searchTerm : list of terms
