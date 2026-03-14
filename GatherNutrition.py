from pathlib import Path
from GenerateNutritionDatabase import generate_database

database = generate_database()

filename = "Roasted Broccoli & Cauliflower Rice Bowl.wiki"
inputFile = open(filename, "r+")
tempFile = inputFile.readlines()

idList = []

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
            recipeIngredientsServingUnit.append("to taste")
        else:
            recipeIngredientsServingQuantity.append(int(quantitySplit[0]))
            recipeIngredientsServingUnit.append(quantitySplit[1])

def find_ingredient_by_alias(ingredient):
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
    found = False

    for line in database:
        if found == False:
            name = database[line]['name']
            name = name.lower()
            if name == ingredient:
                found = True
                print("Found by name")
                idList.append(database[line])
                write_to_alias_file(ingredient,line)
    if found == False:
        find_ingredient_by_search_term(ingredient)

def find_ingredient_by_search_term(ingredient):
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
            remove_frozen(ingredient)
        else:
            find_ingredient_by_name_search(ingredient)

# Fix frozen alias handling
def is_frozen(isItFrozen):
    if "(frozen)" in isItFrozen:
        print("Identified as frozen")
        return True
    else:
        return False

def remove_frozen(frozen):
    removeFrozen = frozen.split("(")
    find_ingredient_by_alias(removeFrozen[0])

def find_ingredient_by_name_search(ingredient):
    found = False
    ingredient = ingredient.strip()
    print("ingredient:", ingredient)
    foundList = []
    foundIDList = []

    for line in database:
        name = database[line]['name']
        name = name.lower()

        if name.find(ingredient) != -1:
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

create_alias_file_if_it_does_not_exist()

#testIngredient = 'medium-grain white rice'
testIngredient = 'Black Rice'
#testIngredient = 'White Rice (frozen)'
#find_ingredient_by_alias(testIngredient)
load_recipe_ingredients()
get_ids_of_all_ingredients()

for ingredient in idList:
    print(ingredient)
    #print(database[ingredient])
