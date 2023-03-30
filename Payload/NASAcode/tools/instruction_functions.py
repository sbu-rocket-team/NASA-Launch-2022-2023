"""
Property Of: SBU Rocket Team

Written By: Jewick Shi
"""

"""
need to add in 
gets 2 instructions out of the radio signal...
6 mins record to guarntee at least 2 readings... best case 3 full proper, avg case 2 full 1 partial
"""
def getInstructionList(inString, callSign):
    tempStr = inString[:]
    tempStr = tempStr.upper()
    
    tempList = tempStr.rsplit(" ")

    callSignList = [i for i in tempList if len(i) == 6] # originally len(i)> 2

    nextCall = callSignList[callSignList.index(callSign)+1]
    
    callIndex1 = tempList.index(callSign)

    nextCallIndex1 = tempList.index(nextCall)
    listEnd = False

    if ((nextCallIndex1 < callIndex1) | (nextCallIndex1 == callIndex1)):
        nextCallIndex1 = tempList.index(nextCall, nextCallIndex1+1)
        listEnd = True

    outList1 = tempList[callIndex1+1:nextCallIndex1]
    outList1.reverse()
    
    callIndex2 = tempList.index(callSign, callIndex1+1)

    if (listEnd):
        outList2 = tempList[callIndex2+1:-1]
    else:
        nextCallIndex2 = tempList.index(nextCall, nextCallIndex1+1)

        outList2 = tempList[callIndex2+1:nextCallIndex2]

    outList2.reverse()
    
    return outList1, outList2

"""
need to improve maybe do 3?
# outputs the command with the most similarity
# if first 2 are the same continue to perform task
# if not the same, get signal again and compare again
"""
def compareInstructions(inList1, inList2):
    commandList = ["A1", "B2", "C3", "D4", "E5", "F6", "G7", "H8"]
    matching = True
    differences = 0
    invalid1 = 0
    invalid2 = 0
    if (len(inList1) == len(inList2)) and (len(inList1) != 0):
        for i in range(len(inList1)):
            if (inList1[i].upper() != inList2[i].upper()):
                matching = False
                differences += 1

                if any(x != inList1[i] for x in commandList):
                    invalid1 += 1
                if any(x != inList2[i] for x in commandList):
                    invalid2 += 1

            
    else:
        matching = False
        differences = -1

    return matching, differences, invalid1, invalid2

def mergeInstructions(inList1, inList2, invalid1, invalid2):
    commandList = ["A1", "B2", "C3", "D4", "E5", "F6", "G7", "H8"]
    returnList = []

    for i in range(len(inList1)):
            if (inList1[i].upper() == inList2[i].upper()):
                returnList.append(inList1[i])
            elif any(x == inList1[i] for x in commandList):
                if ((invalid1 < invalid2) or any(x != inList2[i] for x in commandList)):
                    returnList.append(inList1[i])
            elif any(x == inList2[i] for x in commandList):
                if (invalid2 < invalid1 or any(x != inList1[i] for x in commandList)):
                    returnList.append(inList2[i])

    return returnList
