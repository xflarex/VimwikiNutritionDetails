teaspoonAbbr = {"Teaspoon","teaspoon","t","tsp","Teaspoons","teaspoons","ts","tsps"}
tablespoonAbbr = {"Tablespoon","tablespoon","T","TB","tb","tbs","tbl","Tbl","tbls","Tbls","Tbsp","tbsp","Tablespoons","tablespoons","Ts","TBs","tbsps","Tbap","tbap","Tbaps","tbaps"}
cupAbbr = {"Cup","cup","C","c","Cups","cups","Cs","cs"}
pintAbbr = {"Pint","pint","pt","Pints","pints","pts"}
quartAbbr = {"Quart","quart","qt","Quarts","quarts","qts"}
gallonAbbr = {"Gallon","gallon","gal","Gallons","gallons","gals"}
ounceAbbr = {"O","o","Ounce","ounce","oz","Ounces","ounces","ozs","Onz","onz","Onza","onza"}
fluidOunceAbbr = {"Fluid Ounces","Fluid ounces","fluid ounces","fl ozs","flozs","Fluid Ounce","Fluid ounce","fluid ounce","fl oz","floz","onz","onza","oza","ozas"}
poundAbbr = {"Pound","pound","Pounds","pounds","lb","lbs"}
milliliterAbbr = {"Milliliter","milliliter","ml","mls","mlt","mlts"}
gramAbbr = {"Gram","gram","g","gs","Grm","grm"}
milligramAbbr = {"Milligram","milligram","mg"}
literAbbr = {"Liter","liter","l"}
poundAbbr = {"Pound","pound","lb","lbs"}

def identify_abbreviation(abbr):
    if abbr in teaspoonAbbr:
        print("teaspoon")
        return "teaspoon"

    elif abbr in tablespoonAbbr:
        print("tablespoon")
        return "tablespoon"

    elif abbr in cupAbbr:
        print("cup")
        return "cup"

    elif abbr in pintAbbr:
        print("pint")
        return "pint"

    elif abbr in quartAbbr:
        print("quart")
        return "quart"

    elif abbr in gallonAbbr:
        print("gallon")
        return "gallon"

    elif abbr in ounceAbbr:
        print("ounce")
        return "ounce"

    elif abbr in fluidOunceAbbr:
        print("fluidOunce")
        return "fluidOunce"

    elif abbr in poundAbbr:
        print("pound")
        return "pound"

    elif abbr in milliliterAbbr:
        print("milliliter")
        return "milliliter"

    elif abbr in gramAbbr:
        print("gram")
        return "gram"

    elif abbr in milligramAbbr:
        print("milligram")
        return "milligram"

    elif abbr in literAbbr:
        print("liter")
        return "liter"

    else:
        print("No match found")
        return "noMatch"

def if_half(quantity):
    if quantity == "half":
        return 0.5

def teaspoon_to_tablespoon(teaspoon):
    return teaspoon * 3
def teaspoon_to_milliliter(teaspoon):
    return 5
def teaspoon_to_cup(teaspoon):
    return ounce / 48

def tablespoon_to_teaspoon(tablespoon):
    return tablespoon / 3
def tablespoon_to_milliliter(tablespoon):
    return tablespoon * 15
def tablespoon_to_fluid_ounce(tablespoon):
    return tablespoon
def tablespoons_to_cup(tablespoon):
    return ounce / 16
def tablespoon_to_fluid_ounce(tablespoon):
    return tablespoon / 2

def milliliter_to_liter(milliliter):
    return milliliter * 1000
def milliliter_to_tablespoon(milliliters):
    return milliliters * 15
def milliliters_to_cup(milliliters):
    return ounce / 240
def milliliter_to_teaspoon(milliter):
    return milliliter * 5

def ounce_to_gram(ounce):
    return ounce * 29
def ounce_to_fluid_tablespoon(ounce):
    return tablespoon
def ounce_to_cup(ounce):
    return ounce / 8


def cup_to_ounce(cup):
    return cup * 8
def cup_to_milliliters(cup):
    return cup * 240
def cup_to_tablespoons(cup):
    return cup * 16
def cup_to_teaspoon(cup):
    return cup * 48
def cup_to_pint(pint):
    return pint / 2

def gram_to_ounce(gram):
    return gram / 29


def pint_to_cup(pint):
    return pint * 2
def pint_to_quart(pint):
    return pint / 2

def fluid_ounce_to_tablespoon(fluidOunce):
    return fluidOunce * 2

def quart_to_pint(quart):
    return quart * 2

def liter_to_milliliter(liter):
    return liter * 1000

