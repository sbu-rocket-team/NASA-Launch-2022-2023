from tools import instruction_functions as iF, radio_simulator as rs 


instruc = rs.genRandInstr(3,6,8)
ks = "KQ4CTL"

print(instruc)
print(iF.getInstructionList(instruc, ks))

