import os

def readFile(fileName):
    file_dir = os.path.dirname(os.path.abspath(__file__))
    fileLoc = os.path.join(file_dir, fileName)

    file = open(fileLoc, "r")
    fileData = file.read()
    fileData = ' '.join(fileData.splitlines())
    file.close()

    return fileData

def createFile(fileName):
    file_dir = os.path.dirname(os.path.abspath(__file__))
    fileLoc = os.path.join(file_dir, fileName)

    file = open(fileLoc, "w")
    file.write("SBU Rocket Team records... \n")
    file.close()

def writeFile(fileName, fileText):
    file_dir = os.path.dirname(os.path.abspath(__file__))
    fileLoc = os.path.join(file_dir, fileName)

    file = open(fileLoc, "a")

    text = "\n" + fileText
    file.write(text)
    
    file.close()