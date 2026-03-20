from pathlib import Path

def create_file_if_it_does_not_exist(file):
    filePath = Path(file)
    if filePath.exists():
        print(file,"file exists")
    else:
        print(file,"does not exist")
        tempFile = open(file, "a")  
        tempFile.close()

def load_file_into_list(file):
    tempFile = open(file, "r")  
    tempList = tempFile.readlines()
    tempFile.close()
    return tempList

def add_to_alias_file(ingredient, alias):
    aliasFile = open("aliases", "a")
    newAlias = ingredient + "," + alias + "\n"
    print("Added to aliases:", newAlias)
    aliasFile.write(newAlias)
    aliasFile.close()

