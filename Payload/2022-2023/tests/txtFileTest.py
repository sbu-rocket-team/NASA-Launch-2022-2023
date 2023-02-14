import os

readName = "radioCom.txt"
wrtieName = "writing.txt"

txt1 = "duishalisdufhaldsf\ndsalhfudasfdbavjbd\nasliudhfdsuail\n"
txtnum1, txtnum2, txtnum3 = "1\n", "2\n", "3\n"


def readFile(fileName):
    file_dir = os.path.dirname(os.path.abspath(__file__))
    fileLoc = os.path.join(file_dir, fileName)

    file = open(fileLoc, "r")
    fileData = file.read()
    file.close()

    return fileData

def writeFile(fileName, *fileText):
    file_dir = os.path.dirname(os.path.abspath(__file__))
    fileLoc = os.path.join(file_dir, fileName)

    file = open(fileLoc, "w")

    for i in range(len(fileText)):
        file.write(fileText[i])
    
    file.close()


readeded = readFile(readName)
print(readeded)
writeFile(wrtieName, txt1, txtnum1, txtnum2, txtnum3)