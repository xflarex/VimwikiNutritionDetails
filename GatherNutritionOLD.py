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
        find_ingredient_by_name_search(ingredient)

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
    ratio = eval(joinedString) / databaseQuantity 
    print("\n=========")
    print(ingredient + ":", recipeQuantity, "/", databaseQuantity, "=", ratio)
    return ratio

def is_it_metric(unit):
    if unit == ("g" or "ml" or "grm" or "mg" or "iu" or "IU"):
        print("It's metric")
        return True
    else:
        return False

def calculate_serving(ingredient):
    print("\ningredient:",database[ingredient])
    ingredientUnit = recipeDict[idDict[ingredient]]['unit']
    dataUnit = ""
    if is_it_metric(ingredientUnit) == True:
        dataUnit = database[ingredient]['serving']['metric']['unit']
    else:
        dataUnit = database[ingredient]['serving']['common']['unit']

    print(ingredientUnit,dataUnit)
    if ingredientUnit == dataUnit:
        print("Same serving type found")
        databaseQuantity = database[ingredient]['serving']['common']['quantity']
        recipeQuantity = recipeDict[idDict[ingredient]]['quantity']
        ratio = recipeQuantity / databaseQuantity 
        print("\n=========")
        print(ingredient + ":", recipeQuantity, "/", databaseQuantity, "=", ratio)
        return ratio

    # Convert ingredients to their proper name
    ingredientUnit = identify_abbreviation(ingredientUnit)
    if identify_abbreviation(dataUnit) != None:
        dataUnit = identify_abbreviation(dataUnit)
    else:
        print("dataUnit not matched")

    print(identify_abbreviation(ingredientUnit))
    print(identify_abbreviation(dataUnit))
    if identify_abbreviation(ingredientUnit) != None and identify_abbreviation(dataUnit != None):
        print("Converted:", convert_x_to_y(ingredient,ingredientUnit,dataUnit))
        return convert_x_to_y(ingredient,ingredientUnit,dataUnit)
    else:
        print("Incompatible serving types")
        return None

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
