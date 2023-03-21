"""
Property Of: SBU Rocket Team

Written By: Jewick Shi
"""

import random
import string

"""
Random team and instruction generator

Parameters:
- teams [int]: Number of teams, default of 1
- length [int]: Number of instructions, default of 1
- limit [int]: Types of instructions, default of 8

Return:
- Instr [String]: A string of commands with randomized teams and instructions
"""
def genRandInstr(teams = 1, length = 1, limit = 8):
    reqTeam = "KQ4CTL"
    reqUsed = False
    Instr = ""
    
    if limit > 8:
        limit = 8
    
    for i in range(teams):
        if (i != 0):
                Instr += " "

        if ((random.randint(0,teams) < int(teams/2)) or i == teams-1) and (not reqUsed):
            Instr += reqTeam
            reqUsed = True
        else:
            tempRandStr1 = ''.join(random.choices(string.ascii_uppercase, k=2))
            tempRandStr2 = ''.join(random.choices(string.ascii_uppercase, k=3))
            Instr += tempRandStr1 + "4" + tempRandStr2
        
        for j in range(length):
            tempRand = random.randint(1,limit)
            Instr += " "
            
            
            if(tempRand==1):
                Instr += "A1"
            elif(tempRand==2):
                Instr += "B2"
            elif(tempRand==3):
                Instr += "C3"
            elif(tempRand==4):
                Instr += "D4"
            elif(tempRand==5):
                Instr += "E5"
            elif(tempRand==6):
                Instr += "F6"
            elif(tempRand==7):
                Instr += "G7"
            elif(tempRand==8):
                Instr += "H8"
    
    Instr = Instr #+ " " + Instr
    
    return Instr

"""
Creates random differences within the sequence

Parameters:
- inList [String List]: list of instructions
- chance [int]: chance (1 to 100) of change to occure per instruction, default of 10
"""
def createError(inList, chance = 10):
    for i in range(len(inList)):
        if (random.randint(1,100) <= chance):
            tempRand = random.randint(1,8)

            if(tempRand==1):
                inList[i] = "A1"
            elif(tempRand==2):
                inList[i] = "B2"
            elif(tempRand==3):
                inList[i] = "C3"
            elif(tempRand==4):
                inList[i] = "D4"
            elif(tempRand==5):
                inList[i] = "E5"
            elif(tempRand==6):
                inList[i] = "F6"
            elif(tempRand==7):
                inList[i] = "G7"
            elif(tempRand==8):
                inList[i] = "H8"
            
            if (random.randint(1,100) <= 50):
                inList[i] = inList[i].lower()


<<<<<<< HEAD
print(genRandInstr(10, 16))
=======
print(genRandInstr(teams = 1, length = 25, limit = 8))
>>>>>>> 513f14afa1fcedf99e21e081d3aa88b8883f1e9e
