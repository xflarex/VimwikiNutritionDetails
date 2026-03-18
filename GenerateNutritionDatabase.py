nutritionFile = open("opennutrition.tsv", "r+")
nutFile = nutritionFile.readlines()


def generate_nutrition_database():
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
            # Convert searchTerm to searchLine
            searchDict = dict.fromkeys(searchTerm,splitLine[2])
            servingTerm = ('serving',)
            tempDict = eval(splitLine[6])
            servingDict = dict.fromkeys(servingTerm,tempDict)
            nutrientTerm = ('nutrient',)
            nutrientDict = dict.fromkeys(nutrientTerm,splitLine[7])

            # Prep for use in dict.fromkeys
            termList = (splitLine[0],)
            keyDict = dict.fromkeys(termList)
            # Create dictionary object with nested dictionaries
            completeDict = dict.fromkeys(keyDict,nameDict)
            completeDict[splitLine[0]].update(searchDict)
            completeDict[splitLine[0]].update(servingDict)
            completeDict[splitLine[0]].update(nutrientDict)
            # Update completed dictionary
            finalDict.update(completeDict)
        else:
            # Skip the first line (could be repurposed to steal column names)
            ready = True
    return finalDict


def generate_recipe_database(recipe):
    recipeDict = {}

    for line in recipe:
        splitLine = line.split(",")
        servingSplit = splitLine[0].split(" ")

        if servingSplit[0] == "to" and servingSplit[1] == "taste":
            servingSplit[0] = 1
            servingSplit[1] = "to taste"

        nameTerm = "(\'" + splitLine[1].strip() + "\'),"
        nameTerm = eval(nameTerm)
        servingTerm = ('serving',)
        quantityTerm = ('quantity',)

        servingDict = dict.fromkeys(servingTerm,servingSplit[1].strip())
        quantityDict = dict.fromkeys(quantityTerm,int(servingSplit[0]))

        completeServingDict = dict.fromkeys(nameTerm,servingDict)
        completeQuantityDict = dict.fromkeys(nameTerm,quantityDict)
        
        combinedDict = {}
        combinedDict.update(servingDict)
        combinedDict.update(quantityDict)
        recipeDict.update(dict.fromkeys(nameTerm,combinedDict))
    return recipeDict



def show_potential():
    unitList = []
    for ingredient in database:
        #print(ingredient)
        for unit in database[ingredient]['serving']:
            tempUnit = database[ingredient]['serving']['metric']['unit']
            print("tempUnit:",tempUnit)
            if tempUnit not in unitList and len(tempUnit) < 5:
                unitList.append(tempUnit)
    for unit in unitList:
        print(unit)

database = generate_nutrition_database()
show_potential()
