from pathlib import Path
from GenerateDatabases import *

database = generate_nutrition_database()

filename = "Roasted Broccoli & Cauliflower Rice Bowl.wiki"
inputFile = open(filename, "r+")
tempFile = inputFile.readlines()
recipeDict = generate_recipe_database(tempFile)

idList = []
idDict = {}

# Recreate as nested list or other sensible type
recipeIngredientsList = []
recipeIngredientsServingQuantity = []
recipeIngredientsServingUnit = []

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

# Fix frozen alias handling
def is_frozen(isItFrozen):
    if "(frozen)" in isItFrozen:
        print(isItFrozen, "identified as frozen")
        return True
    else:
        return False

def remove_frozen(frozen):
    removeFrozen = frozen.split("(")
    return removeFrozen[0]

def load_recipe_ingredients():
    for line in tempFile:
        tempString = line.split(", ")

        print("tempString:", tempString)
        ingredient = tempString[1]
        ingredient = ingredient.strip()
        ingredient = ingredient.lower()
        recipeIngredientsList.append(ingredient)

        quantity = tempString[0]
        quantity = quantity.strip()
        quantity = quantity.lower()
        quantitySplit = quantity.split(" ")

        if tempString[0].lower() == "to taste":
            tempQuantityValue = 1
            tempUnitValue = "to taste"
        else:
            tempQuantityValue = quantitySplit[0]
            tempUnitValue = quantitySplit[1]

        tempQuantity = dict.fromkeys(('quantity,'),tempQuantityValue)
        tempDict = dict.fromkeys(ingredient,tempQuantity)
        tempIDDict = {}
        tempIDDict.update(tempDict)
        tempUnit = dict.fromkeys(('unit',),tempUnitValue)

        ingredientList = []
        ingredientList.append(ingredient)
        tempDict = dict.fromkeys((ingredient,),tempUnit)
        tempIDDict.update(tempDict)
    print(tempIDDict)

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
            idList.append(splitAlias[1].strip())
            idDict.update(dict.fromkeys((splitAlias[1].strip(),),ingredient))
            print(idList)
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
                idList.append(database[line])
                idDict.update(dict.fromkeys((database[line],),ingredient))
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
                idList.append(database[line])
                idDict.update(dict.fromkeys((database[line],),ingredient))
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
                        idList.append(database[line])
                        idDict.update(dict.fromkeys((database[line],),ingredient))
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
    idList.append(foundIDList[x])
    idDict.update(dict.fromkeys((foundIDList[x],),ingredient))
    write_to_alias_file(ingredient,foundIDList[x])

def get_ids_of_all_ingredients():
    for ingredient in recipeIngredientsList:
        find_ingredient_by_alias(ingredient)

def calculate_serving(ingredient):
    if recipeDict[idDict[ingredient]]['unit'] == database[ingredient]['serving']['common']['unit']:
        #print("Correct serving type: Common")
        databaseQuantity = database[ingredient]['serving']['common']['quantity']
        recipeQuantity = recipeDict[idDict[ingredient]]['quantity']
        ratio = databaseQuantity / recipeQuantity
        #print(databaseQuantity, "/", recipeQuantity, "=", ratio)
        return ratio

    elif recipeDict[idDict[ingredient]]['unit'] == database[ingredient]['serving']['metric']['unit']:
        print("Correct serving type: Metric")

    else:
        #print("Unknown serving type:", recipeDict[idDict[ingredient]]['unit'], recipeDict[idDict[ingredient]]['quantity'])
        #print(recipeDict[idDict[ingredient]]['unit'], database[ingredient]['serving']['common']['unit'],database[ingredient]['serving']['metric']['unit'])
        asdf = 0

create_alias_file_if_it_does_not_exist()

load_recipe_ingredients()
get_ids_of_all_ingredients()

print(recipeDict)

calculatedNutrientDict = {}
for ingredient in idDict:
    calculatedRatio = calculate_serving(ingredient)
    if calculatedRatio == None:
        calculatedRatio = 1
    print(idDict[ingredient],calculatedRatio)
    for nutrient in database[ingredient]['nutrient']:
        tempValue = database[ingredient]['nutrient'][nutrient] * calculatedRatio
        print("tempValue:",tempValue)
        print(nutrient)
        calculatedNutrientDict.update(dict.fromkeys((nutrient,), tempValue))
        # dictionary.get(keyname, value)

print(calculatedNutrientDict)

