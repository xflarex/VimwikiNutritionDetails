nutritionFile = open("opennutrition.tsv", "r+")
nutFile = nutritionFile.readlines()

commonQuantity = 0.0
metricQuantity = 0

for tempLine in nutFile:
    #tempString = tempLine.split(" ", 1)

    if "Broccoli, Frozen" in tempLine:
        #print(tempLine)
        #foundLine = tempLine.split(",")
        foundLine = tempLine.split("\t")
        #for a in foundLine:
        #    print(a)

        print(foundLine[6])
        print(foundLine[7])
        #unitLine = dict(foundLine[7])
        testDict = {"common":{"unit":"cup","quantity":0.5},"metric":{"unit":"g","quantity":85}}

        print("=========")
        #print(unitLine[0]) # Needs to be ' not " ??
        #for a in foundLine[6]:
        #    print(a)

        # Split line 6
        tempQuantity = foundLine[6].split(":")
        # Get unit from line 6
        commonUnitDirty = tempQuantity[2].split("\"")
        commonUnit = commonUnitDirty[1]

        # Get common quantity from line 6
        commonQuantityDirty = tempQuantity[3].split("}")
        commonQuantity = commonQuantityDirty[0]
        {"common":{"unit":"cup","quantity":0.5},"metric":{"unit":"g","quantity":85}}

        print(commonUnit)
        print(commonQuantity)

        # Get metric unit
        metricUnitDirty = tempQuantity[5].split("\"")
        metricUnit = metricUnitDirty[1]
        metricQuantityDirty = tempQuantity[6].split("}")
        metricQuantity = metricQuantityDirty[0]
        print(metricUnit)
        print(metricQuantity)
        



