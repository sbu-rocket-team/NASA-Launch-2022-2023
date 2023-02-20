import os

def readFile(fileName):
    file_dir = os.path.dirname(os.path.abspath(__file__))
    fileLoc = os.path.join(file_dir, fileName)

    file = open(fileLoc, "r")
    fileData = file.read()
    fileData = ' '.join(fileData.splitlines())
    file.close()

    return fileData

def writeFile(fileName, *fileText):
    file_dir = os.path.dirname(os.path.abspath(__file__))
    fileLoc = os.path.join(file_dir, fileName)

    file = open(fileLoc, "w")

    for i in range(len(fileText)):
        file.write(fileText[i])
    
    file.close()