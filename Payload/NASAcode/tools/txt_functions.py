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

def writeFile(fileName, fileText, list=False):
    file_dir = os.path.dirname(os.path.abspath(__file__))
    fileLoc = os.path.join(file_dir, fileName)

    with open(fileLoc, "a") as file: 
        if (list):
            file.write("\n ")
            for i in range(len(fileText)):
                file.write(fileText[i] + " ")
        else:
            text = "\n" + fileText
            file.write(text)