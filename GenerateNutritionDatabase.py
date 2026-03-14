nutritionFile = open("opennutrition.tsv", "r+")
nutFile = nutritionFile.readlines()


def generate_database():
    finalDict = {}
    ready = False

    for nut in nutFile:
        if ready == True:
            # Split by "tab"
            splitLine = nut.split("\t")
            # Create nested dictionaries
            nameTerm = ('name',)
            nameDict = dict.fromkeys(nameTerm,splitLine[1])
            searchTerm = ('search',)
            searchDict = dict.fromkeys(searchTerm,splitLine[2])
            servingTerm = ('serving',)
            servingDict = dict.fromkeys(servingTerm,splitLine[6])
            nutrientTerm = ('nutrient',)
            nutrientDict = dict.fromkeys(nutrientTerm,splitLine[7])
            labelTerm = ('label',)
            labelDict = dict.fromkeys(labelTerm,splitLine[8])

            # Prep for use in dict.fromkeys
            termList = (splitLine[0],)
            keyDict = dict.fromkeys(termList)
            # Create dictionary object with nested dictionaries
            completeDict = dict.fromkeys(keyDict,nameDict)
            completeDict[splitLine[0]].update(searchDict)
            completeDict[splitLine[0]].update(servingDict)
            completeDict[splitLine[0]].update(nutrientDict)
            completeDict[splitLine[0]].update(labelDict)
            # Update completed dictionary
            finalDict.update(completeDict)
        else:
            # Skip the first line (could be repurposed to steal column names)
            ready = True
    return finalDict

#returnDict = generate_database()
#print(returnDict['fd_zZmQBPvS5qfL']['name'])
#print(returnDict['fd_zZmQBPvS5qfL']['nutrient'])
