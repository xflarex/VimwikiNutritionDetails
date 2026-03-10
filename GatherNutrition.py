#filename = "Roasted Broccoli & Cauliflower Rice Bowl.wiki"
filename = "Rice Bowl.wiki"
inputFile = open(filename, "r+")
tempFile = inputFile.readlines()

nutritionFile = open("opennutrition.tsv", "r+")
nutFile = nutritionFile.readlines()

aliasFile = open("aliases", "a")  
aliasFile.close()

nameList = []
searchList = []

recipeIngredientsList = []

quantityLine = []
infoLine = []

searchAlias = "asdf"

# Load ingredient name list
def loadNameList():
    count = 0
    ready = False

    for tempLine in nutFile:
        if ready == True:
            splitLine = tempLine.split("\t")
            nameList.append(splitLine[1].lower())
            searchList.append(eval(splitLine[2]))

            count += 1
        else:
            ready = True

# ", frozen" needs added back to search
def is_frozen(isItFrozen):
    if "(frozen)" in isItFrozen:
        return True
    else:
        return False

def remove_frozen(frozen):
        removeFrozen = frozen.split("(")
        find_ingredient_by_alias(removeFrozen[0])

def load_recipe_ingredients():
    for tempLine in tempFile:
        tempString = tempLine.split(", ")

        #ingredient = is_frozen(tempString[1])
        ingredient = tempString[1]
        ingredient = ingredient.strip()
        ingredient = ingredient.lower()
        recipeIngredientsList.append(ingredient)

def find_ingredient_by_alias(ingredient):
    found = False
    aliasFile = open("aliases", "r")  
    aliasList = aliasFile.readlines()
    aliasFile.close()

    for alias in aliasList:
        splitAlias = alias.split(",")
        if ingredient == splitAlias[0]:
            found = True
            show_info(int(splitAlias[1]))
            show_quantity(int(splitAlias[1]))
    if found == False:
        find_ingredient_by_name(ingredient)
            

def find_ingredient_by_name(ingredient):
    count = 0
    found = False
    ingredient = ingredient.strip()

    for name in nameList:
        if ingredient == name:
            found = True

            show_info(int(count))
            show_quantity(int(count))
        count += 1

    if found == False:
        find_ingredient_by_search_term(ingredient)

def find_ingredient_by_search_term(ingredient):
    count = 0
    found = False
    ingredient = ingredient.lower()

    for searchTermList in searchList:
        for name in searchTermList:
            if ingredient == name:
                print("Found by search term", count)
                found = True

                show_info(int(count))
                show_quantity(int(count))
            count += 1

    if found == False:
        find_ingredient_by_name_subsearch(ingredient)


def find_ingredient_by_name_subsearch(ingredient):
    count = 0
    found = False
    ingredient = ingredient.strip()
    tempNameList = []
    tempNameCount = []

    aliasFile = open("aliases", "a")  

    for name in nameList:
        if name.find(ingredient) != -1:
            tempNameList.append(name)
            tempNameCount.append(count)
            found = True
        count += 1

    if found == True:
        n = 0
        while n < len(tempNameList):
            n += 1

        x = input("Choose the correct ingredient:")
        aliasFile.write(searchAlias)
        aliasFile.write(",")
        aliasFile.write(str(tempNameCount[int(x)]))
        aliasFile.write("\n")
        aliasFile.close()

        show_info(tempNameCount[int(x)])
        show_quantity(tempNameCount[int(x)])
    else:
        if is_frozen(ingredient) == True:
            remove_frozen(ingredient)
        else:
            print("Error: No results found")

def find_all_ingredients_in_recipe(recipe):
    for ingredient in recipe:
        print("\ningredient in recipe: ", ingredient)
        global searchAlias
        searchAlias = ingredient
        find_ingredient_by_alias(searchAlias)

def load_info_and_quantity():
    ready = False
    for tempLine in nutFile:
        if ready == True:
            splitLine = tempLine.split("\t")
            quantityLine.append(splitLine[6])
            infoLine.append(splitLine[7])
            #print(nameDict)
        else:
            ready = True

def show_info(n):
    print(infoLine[n])

def show_quantity(n):
    print(quantityLine[n])

loadNameList()
load_info_and_quantity()
load_recipe_ingredients()

find_all_ingredients_in_recipe(recipeIngredientsList)
