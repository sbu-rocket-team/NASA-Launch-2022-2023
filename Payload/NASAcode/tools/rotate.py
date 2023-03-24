from NASAcode.tools import encoder_functions as encF
import time, sys

def rotate(degrees,dir):
    currentDegree = 0
    currentDegree = encF.rotateCam(dir, currentDegree, degrees)
    time.sleep(0.25)


if(__name__ == '__main__'):
    print(sys.argv[1],sys.argv[2])
    rotate(int(sys.argv[1]),str(sys.argv[2]))