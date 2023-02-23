"""
Property Of: SBU Rocket Team

Written By: Jewick Shi
"""
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

    with open(fileLoc, "w") as file: 
        file.write("SBU Rocket Team records... \n")

def writeFile(fileName, fileText):
    file_dir = os.path.dirname(os.path.abspath(__file__))
    fileLoc = os.path.join(file_dir, fileName)

    text = "\n" + fileText

    with open(fileLoc, "a") as file: 
        file.write(text)