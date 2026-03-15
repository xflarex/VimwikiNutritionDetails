from pathlib import Path
from GenerateNutritionDatabase import generate_database

database = generate_database()

filename = "Roasted Broccoli & Cauliflower Rice Bowl.wiki"
inputFile = open(filename, "r+")
tempFile = inputFile.readlines()

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
            recipeIngredientsServingQuantity.append(1)
            tempQuantityValue = 1
            recipeIngredientsServingUnit.append("to taste")
            tempUnitValue = "to taste"
        else:
            recipeIngredientsServingQuantity.append(int(quantitySplit[0]))
            tempQuantityValue = quantitySplit[0]
            recipeIngredientsServingUnit.append(quantitySplit[1])
            tempUnitValue = quantitySplit[1]

        tList = ('quantity,')
        tempQuantity = dict.fromkeys(tList,tempQuantityValue)
        tempDict = dict.fromkeys(ingredient,tempQuantity)
        tempIDDict = {}
        tempIDDict.update(tempDict)

        tempUnit = dict.fromkeys(list('unit,'),tempUnitValue)
        tempDict = dict.fromkeys(ingredient,tempUnit)
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
            print(idList)

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
    write_to_alias_file(ingredient,foundIDList[x])

def get_ids_of_all_ingredients():
    for ingredient in recipeIngredientsList:
        find_ingredient_by_alias(ingredient)

def update_serving_unit_list():
    for ingredient in idList:
        asdf = 0


def calculate_serving(ingredient):
    if recipeIngredientsServingUnit == database[ingredient]['serving']['common']['unit']:
        print("Correct serving type")
    else:
        print(recipeIngredientsServingUnit[0], database[ingredient]['serving']['common']['unit'])

create_alias_file_if_it_does_not_exist()

load_recipe_ingredients()
get_ids_of_all_ingredients()

for ingredient in idList:
    calculate_serving(ingredient)
    print(database[ingredient]['name'])
    print(database[ingredient]['serving'])
    #print(type(database[ingredient]['serving']))
    print(database[ingredient]['serving']['common']['unit'])
    print(database[ingredient]['serving']['common']['quantity'])
    #print(database[ingredient]['nutrient'])
