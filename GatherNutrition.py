filename = "Roasted Broccoli & Cauliflower Rice Bowl.wiki"
inputFile = open(filename, "r+")
tempFile = inputFile.readlines()

nutritionFile = open("opennutrition.tsv", "r+")
nutFile = nutritionFile.readlines()

aliasFile = open("aliases", "a")  


nameList = []
searchList = []

recipeIngredientsList = []

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
            #if count > 2000:
                #break
        else:
            ready = True

def is_frozen(isItFrozen):
    if "(frozen)" in isItFrozen:
        removeFrozen = isItFrozen.split("(")
        return removeFrozen[0]
    else:
        removeNewLine = isItFrozen.split("\n")
        return removeNewLine[0]

def load_recipe_ingredients():
    for tempLine in tempFile:
        tempString = tempLine.split(", ")

        ingredient = is_frozen(tempString[1])
        ingredient = ingredient.strip()
        ingredient = ingredient.lower()
        recipeIngredientsList.append(ingredient)

def find_ingredient_by_alias():
    aliasFile.readlines()

def find_ingredient_by_name(ingredient):
    count = 0
    found = False
    ingredient = ingredient.strip()

    for name in nameList:
        if ingredient == name:
            print("Found", count)
            found = True
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
            count += 1

    if found == False:
        find_ingredient_by_name_subsearch(ingredient)


def find_ingredient_by_name_subsearch(ingredient):
    count = 0
    found = False
    ingredient = ingredient.strip()
    tempNameList = []
    tempNameCount = []

    for name in nameList:
        if name.find(ingredient) != -1:
            tempNameList.append(name)
            tempNameCount.append(count)
            found = True
        count += 1

    if found == True:
        n = 0
        while n < len(tempNameList):
            print(n, ": ", tempNameCount[n], ": ", tempNameList[n])
            n += 1

        x = input("Choose the correct ingredient:")
        aliasFile.write(ingredient)
        aliasFile.write(",")
        aliasFile.write(str(tempNameCount[int(x)]))
        aliasFile.write("\n")
    else:
        print("Error: No results found")

def find_all_ingredients_in_recipe(recipe):
    for ingredient in recipe:

        find_ingredient_by_name(ingredient)

loadNameList()
load_recipe_ingredients()

find_all_ingredients_in_recipe(recipeIngredientsList)
#for name in nameList:
    #print(name)
#print(searchList)

#print(searchList[35286])
