filename = "Roasted Broccoli & Cauliflower Rice Bowl.wiki"
#filename = "Rice Bowl.wiki"
inputFile = open(filename, "r+")
tempFile = inputFile.readlines()

nutritionFile = open("opennutrition.tsv", "r+")
nutFile = nutritionFile.readlines()

aliasFile = open("aliases", "a")  
aliasFile.close()

nameList = []
searchList = []

recipeIngredientsList = []
recipeIngredientsQuantity = []
recipeIngredientsQuantityType = []

quantityLine = []
infoLine = []
idList = []

nutrientDict = {}

searchAlias = "asdf"

# Load ingredient name list
def load_name_list():
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

        ingredient = tempString[1]
        ingredient = ingredient.strip()
        ingredient = ingredient.lower()
        recipeIngredientsList.append(ingredient)

        quantity = tempString[0]
        quantity = quantity.strip()
        quantity = quantity.lower()
        quantitySplit = quantity.split(" ")

        if tempString[0].lower() == "to taste":
            recipeIngredientsQuantity.append(1)
            recipeIngredientsQuantityType.append("to taste")
        else:
            recipeIngredientsQuantity.append(int(quantitySplit[0]))
            recipeIngredientsQuantityType.append(quantitySplit[1])

def find_ingredient_by_alias(ingredient):
    found = False
    aliasFile = open("aliases", "r")  
    aliasList = aliasFile.readlines()
    aliasFile.close()

    for alias in aliasList:
        splitAlias = alias.split(",")
        if ingredient == splitAlias[0]:
            idList.append(int(splitAlias[1]))
            found = True
            print("Found by alias")

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
            idList.append(int(count))
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
                idList.append(int(count))
                print("Found", ingredient, "by search term", count)
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
            print(n,tempNameList[n])
            n += 1

        x = input("Choose the correct ingredient:")
        idList.append(x)
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
        global searchAlias # Remove global
        searchAlias = ingredient
        find_ingredient_by_alias(searchAlias)

def load_info_and_quantity():
    ready = False
    for tempLine in nutFile:
        if ready == True:
            splitLine = tempLine.split("\t")
            quantityLine.append(splitLine[6])
            infoLine.append(splitLine[7])
        else:
            ready = True

def show_info(n):
    print("infoLine:", infoLine[n])
    #update_nutrients(eval(infoLine[n]), eval(quantityLine[n]))

def show_quantity(n):
    print("quantityLine[n]")
    print(quantityLine[n])

# Needs rebuilt run at the end
def update_nutrients(nutrients, quantity):
    print("\n\t\tquantity:", quantity)
    for nutrient in nutrients:
        if nutrient not in nutrientDict.keys():
            tempNutrient = "{'" + nutrient + "':" + str(nutrients[nutrient]) + "}"
            nutrientDict.update(eval(tempNutrient))

            #if quantity["common"]["unit"] == 
        else:
            nutrientDict[nutrient] = nutrientDict[nutrient] + nutrients[nutrient]

def update_nutrients_new():
    for id in idList:
        tempID = int(id)
        print(nameList[tempID])
        show_quantity(tempID)
    print("\n\n")

def list_nutrients(nutrients):
    for nutrient in nutrients:
        print(nutrient + ":", nutrients.get(nutrient))

def list_all_quantities():
    tempQuantity = []
    for quantity in quantityLine:
        tempDict = eval(quantity)
        if tempDict['metric']['unit'] not in tempQuantity:
            tempQuantity.append(tempDict['metric']['unit'])
    for temp in tempQuantity:
        print(temp)

load_name_list()
load_info_and_quantity()
load_recipe_ingredients()

find_all_ingredients_in_recipe(recipeIngredientsList)

print("\n\n")
#list_nutrients(nutrientDict)
#list_all_quantities()

print(recipeIngredientsList)
print(recipeIngredientsQuantity)
print(recipeIngredientsQuantityType)
print(idList)

update_nutrients_new()
