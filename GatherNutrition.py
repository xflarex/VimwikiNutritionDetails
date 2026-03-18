from pathlib import Path
from GenerateDatabases import *
from MeasurementsConverter import *

database = generate_nutrition_database()

filename = "Roasted Broccoli & Cauliflower Rice Bowl.wiki"
inputFile = open(filename, "r+")
recipeFile = inputFile.readlines()
recipeDict = generate_recipe_database(recipeFile)

idDict = {}
calculatedNutrientDict = {}

# Recreate as nested list or other sensible type
recipeIngredientsList = []

def create_alias_file_if_it_does_not_exist():
    aliasPath = Path("aliases")
    if aliasPath.exists():
        print("aliases file exists")
    else:
        print("aliases does not exist")
        aliasFile = open("aliases", "a")  
        aliasFile.close()

def write_to_alias_file(ingredient, alias):
    aliasFile = open("aliases", "a")
    newAlias = ingredient + "," + alias + "\n"
    print("Added to aliases:", newAlias)
    aliasFile.write(newAlias)
    aliasFile.close()

def load_aliases_into_list():
    aliasFile = open("aliases", "r")  
    aliasList = aliasFile.readlines()
    aliasFile.close()
    return aliasList

def is_frozen(isItFrozen):
    if "(frozen)" in isItFrozen:
        print(isItFrozen, "identified as frozen")
        return True
    else:
        return False

def remove_frozen(frozen):
    removeFrozen = frozen.split("(")
    return removeFrozen[0]

def find_ingredient_by_alias(ingredient):
    print("Searching by alias")
    found = False
    ingredient = ingredient.lower().strip()

    aliasList = load_aliases_into_list()

    for alias in aliasList:
        splitAlias = alias.split(",")
        if ingredient == splitAlias[0]:
            found = True
            print("Found by alias")
            idDict.update(dict.fromkeys((splitAlias[1].strip(),),ingredient))
            print(idDict)

    if found == False:
        find_ingredient_by_name(ingredient)

def find_ingredient_by_name(ingredient):
    print("Searching by name")
    found = False

    if is_frozen(ingredient) == True:
        tempIngredient = remove_frozen(ingredient)
        tempIngredient = tempIngredient.strip()
    else:
        tempIngredient = ingredient

    for line in database:
        if found == False:
            name = database[line]['name']
            name = name.lower()
            if name == tempIngredient:
                found = True
                print("Found by name")
                idDict.update(dict.fromkeys((str(database[line]),),ingredient))
                write_to_alias_file(ingredient,line)
    if found == False:
        find_ingredient_by_search_term(ingredient)

def find_ingredient_by_search_term(ingredient):
    print("Searching by search term")
    found = False

    for line in database:
        searchList = database[line]['search']
        searchList = eval(searchList)

        for term in searchList:
            if term == ingredient:
                found = True
                print("Found by search")
                idDict.update(dict.fromkeys(str((database[line]),),ingredient))
                write_to_alias_file(ingredient,line)

    if found == False:
        if is_frozen(ingredient) == True:
            tempIngredient = remove_frozen(ingredient)
            tempIngredient = tempIngredient.strip()
            for line in database:
                searchList = database[line]['search']
                searchList = eval(searchList)

                for term in searchList:
                    if term == tempIngredient:
                        found = True
                        print("Found by search term")
                        idDict.update(dict.fromkeys((str(database[line]),),ingredient))
                        write_to_alias_file(ingredient,line)
        else:
            find_ingredient_by_name_search(ingredient)

    if found == False:
        find_ingredient_by_name_search(ingredient)

def find_ingredient_by_name_search(ingredient):
    print("Searching by name search")
    found = False
    ingredient = ingredient.strip()
    foundList = []
    foundIDList = []

    if is_frozen(ingredient) == True:
        tempIngredient = remove_frozen(ingredient)
        tempIngredient = tempIngredient.strip()
    else:
        tempIngredient = ingredient

    for line in database:
        name = database[line]['name']
        name = name.lower()

        if name.find(tempIngredient) != -1:
            found = True
            print("Found by name search")
            foundList.append(name)
            foundIDList.append(line)
    n = 0
    for potentialIngredient in foundList:
        print(n,potentialIngredient)
        n += 1

    x = input("Choose the correct ingredient:")
    x = int(x)
    idDict.update(dict.fromkeys((foundIDList[x],),ingredient))
    write_to_alias_file(ingredient,foundIDList[x])

def get_ids_of_all_ingredients():
    for ingredient in recipeDict:
        find_ingredient_by_alias(ingredient)

def convert_x_to_y(ingredient,x,y):
    recipeQuantity = recipeDict[idDict[ingredient]]['quantity']
    databaseQuantity = database[ingredient]['serving']['common']['quantity']
    joinedString = x + "_to_" + y + "(recipeQuantity)"
    ratio = databaseQuantity / eval(joinedString)
    return ratio

def is_it_metric(unit):
    if unit == ("g" or "ml" or "grm" or "mg" or "iu" or "IU"):
        print("It's metric")
        abbr = identify_abbreviation(unit)
        return abbr
    else:
        return None

def calculate_serving(ingredient):
    tempUnit = recipeDict[idDict[ingredient]]['unit']
    print("tempUnit::",tempUnit)
    dataUnit = database[ingredient]['serving']['common']['unit']
    if is_it_metric(tempUnit) != None:
        print(convert_x_to_y(ingredient,tempUnit,dataUnit))
    if recipeDict[idDict[ingredient]]['unit'] == database[ingredient]['serving']['common']['unit']:
        print("Correct serving type: Common")
        databaseQuantity = database[ingredient]['serving']['common']['quantity']
        recipeQuantity = recipeDict[idDict[ingredient]]['quantity']
        ratio = databaseQuantity / recipeQuantity
        print(databaseQuantity, "/", recipeQuantity, "=", ratio)
        return ratio

    elif recipeDict[idDict[ingredient]]['unit'] == database[ingredient]['serving']['metric']['unit']:
        print("Correct serving type: Metric")

    else:
        abbr = str(recipeDict[idDict[ingredient]]['unit'])
        print("Unknown serving type:", abbr, recipeDict[idDict[ingredient]]['quantity'])
        print(abbr, database[ingredient]['serving']['common']['unit'],database[ingredient]['serving']['metric']['unit'])
        commonUnit = str(database[ingredient]['serving']['common']['unit'])
        metricUnit = str(database[ingredient]['serving']['metric']['unit'])
        abbr = identify_abbreviation(abbr)
        commonUnit = identify_abbreviation(commonUnit)
        metricUnit = identify_abbreviation(metricUnit)
        print("acm",abbr,commonUnit,metricUnit)
        if abbr != "noMatch":
            print(convert_x_to_y(ingredient,abbr,commonUnit))
        match abbr:
            case "tablespoon":
                recipeQuantity = recipeDict[idDict[ingredient]]['quantity']
                if commonUnit == "milliliter":
                    print("Found ml")
                    databaseQuantity = database[ingredient]['serving']['common']['quantity']
                    tbs = "tablespoon"
                    mm = "milliliter"
                    ttm = tbs + "_to_" + mm + "(recipeQuantity)"
                    ratio = databaseQuantity / eval(ttm)
                    print("ratio:",ratio)
                    return(ratio)
                if metricUnit == "milliliter":
                    databaseQuantity = database[ingredient]['serving']['metric']['quantity']
                    ratio = databaseQuantity / tablespoon_to_milliliter(recipeQuantity)
                    return(ratio)
            case "teaspoon":
                if abbr == commonUnit or abbr == metricUnit:
                    print("Found", abbr)
                recipeQuantity = recipeDict[idDict[ingredient]]['quantity']
                if commonUnit == "milliliter":
                    print("Found ml")
                    databaseQuantity = database[ingredient]['serving']['common']['quantity']
                    ratio = databaseQuantity / tablespoon_to_milliliter(recipeQuantity)
                    return(ratio)
                if metricUnit == "milliliter":
                    databaseQuantity = database[ingredient]['serving']['metric']['quantity']
                    ratio = databaseQuantity / tablespoon_to_milliliter(recipeQuantity)
                    return(ratio)
            case "cup":
                if abbr == commonUnit or abbr == metricUnit:
                    print("Found", abbr)
            case "pint":
                if abbr == commonUnit or abbr == metricUnit:
                    print("Found", abbr)
            case "quart":
                if abbr == commonUnit or abbr == metricUnit:
                    print("Found", abbr)
            case "gallon":
                if abbr == commonUnit or abbr == metricUnit:
                    print("Found", abbr)
            case "ounce":
                if abbr == commonUnit or abbr == metricUnit:
                    print("Found", abbr)
            case "fluidOunce":
                if abbr == commonUnit or abbr == metricUnit:
                    print("Found", abbr)
            case "pound":
                if abbr == commonUnit or abbr == metricUnit:
                    print("Found", abbr)
            case "milliliter":
                if abbr == commonUnit:
                    print("Found", abbr)
            case "gram":
                if abbr == commonUnit or abbr == metricUnit:
                    print("Found", abbr)
            case "milligram":
                if abbr == commonUnit or abbr == metricUnit:
                    print("Found", abbr)
            case "liter":
                if abbr == commonUnit or abbr == metricUnit:
                    print("Found", abbr)
        print(commonUnit,metricUnit)
        print("End match case")

def calculate_totals():
    for ingredient in idDict:
        calculatedRatio = calculate_serving(ingredient)
        if calculatedRatio == None:
            calculatedRatio = 1
        for nutrient in database[ingredient]['nutrient']:
            tempValue = database[ingredient]['nutrient'][nutrient] * calculatedRatio
            if calculatedNutrientDict.get(nutrient) == None:
                calculatedNutrientDict.update(dict.fromkeys((nutrient,), tempValue))
            else:
                calculatedValue = tempValue + int(calculatedNutrientDict.get(nutrient))
                calculatedNutrientDict.update(dict.fromkeys((nutrient,), calculatedValue))

create_alias_file_if_it_does_not_exist()

get_ids_of_all_ingredients()

print(recipeDict)
calculate_totals()
print(calculatedNutrientDict)
