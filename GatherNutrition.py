filename = "Roasted Broccoli & Cauliflower Rice Bowl.wiki"
inputFile = open(filename, "r+")
tempFile = inputFile.readlines()

for tempLine in tempFile:
    tempString = tempLine.split(", ")

    for x in range(0,len(tempString)):
        if "(frozen)" in tempString[x]:
            print("frozen")
            removeFrozen = tempString[x].split("(")
            print(removeFrozen[0])
            print("x: ", x, "\n")
        else:
            print("tempString[x]: ", tempString[x])
