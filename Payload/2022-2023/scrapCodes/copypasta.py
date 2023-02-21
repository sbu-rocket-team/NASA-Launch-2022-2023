# random execution generation
"""
instr1 = rS.genRandInstr(5, 20)

print("Random instruction strings")
print(instr1)
print()

eventList1_1, eventList1_2 = instF.getInstructionList(instr1, CALLSIGN)

print("Instruction Lists")
print(eventList1_1)
print()

tempCopy1 = eventList1_1[:]
tempCopy2 = eventList1_1[:]
rS.createError(tempCopy1)
rS.createError(tempCopy2)
    
print("Instruction Lists post chance")
print(tempCopy1)
print(tempCopy2)
print()

# note... does A1 == a1???
matchingInstr1, DiffInstr1 = instF.compareInstructions(eventList1_1, tempCopy1)
matchingInstr2, DiffInstr2 = instF.compareInstructions(eventList1_1, tempCopy2)
    
print("Matching? and # differences")
print(matchingInstr1, DiffInstr1)
print(matchingInstr2, DiffInstr2)

if (DiffInstr1 < DiffInstr2):
    print("first one less mistake")
    executeList = tempCopy1
else:
    print("second one less mistake")
    executeList = tempCopy2

print("\nExecuting Instructions... what, grey? custom? flipped?")
executeInstructions(executeList)
print("\nPassed Operation")
"""