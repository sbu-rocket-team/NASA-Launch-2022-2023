import os

import matplotlib.pyplot as plt
import numpy as np

import txt_functions as txtF

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR) # Up one directory

OUTPUTFILE = os.path.join(PARENT_DIR, "MPUOutputData.txt")

def plotData(txtFile):
    dataStr = txtF.readFile(txtFile)
    tdArray = dataStr.rsplit("...")[1].lstrip().rsplit(";")
    timeArray = []
    AxArray = []
    AyArray = []
    AzArray = []
    GxArray = []
    GyArray = []
    GzArray = []

    for i in tdArray:
        if  (len(i) > 0):
            tempArray = i.rsplit(":")

            timeArray.append(tempArray[0])
            
            dataArray = tempArray[1].rsplit(",")
            AxArray.append(dataArray[0])
            AyArray.append(dataArray[1])
            AzArray.append(dataArray[2])
            GxArray.append(dataArray[3])
            GyArray.append(dataArray[4])
            GzArray.append(dataArray[5])

    timeArray = [float(i) for i in timeArray]
    AxArray = [float(i) for i in AxArray]
    AyArray = [float(i) for i in AyArray]
    AzArray = [float(i) for i in AzArray]
    GxArray = [float(i) for i in GxArray]
    GyArray = [float(i) for i in GyArray]
    GzArray = [float(i) for i in GzArray]

    #AArray = np.linalg.norm(np.array([AxArray, AyArray, AzArray]), axis=0)
    #GArray = np.linalg.norm(np.array([GxArray, GyArray, GzArray]), axis=0)

    VxArray = np.zeros_like(AxArray)
    VyArray = np.zeros_like(AyArray)
    VzArray = np.zeros_like(AzArray)
    for i in range(1, len(VxArray)):
        VxArray[i] = np.trapz(AxArray[:i+1], timeArray[:i+1])
        VyArray[i] = np.trapz(AyArray[:i+1], timeArray[:i+1])
        VzArray[i] = np.trapz(AzArray[:i+1], timeArray[:i+1])

    PxArray = np.zeros_like(VxArray)
    PyArray = np.zeros_like(VyArray)
    PzArray = np.zeros_like(VzArray)
    for i in range(1, len(PxArray)):
        PxArray[i] = np.trapz(VxArray[:i+1], timeArray[:i+1])
        PyArray[i] = np.trapz(VyArray[:i+1], timeArray[:i+1])
        PzArray[i] = np.trapz(VzArray[:i+1], timeArray[:i+1])

    r = 1
    c = 3

    plt.figure("Kine")
    plt.subplot(r, c, 1)
    plt.plot(timeArray, AxArray, '-ob', label="Ax")
    plt.plot(timeArray, AyArray, '-og', label="Ay")
    plt.plot(timeArray, AzArray, '-or', label="Az")
    plt.xscale("linear")
    plt.yscale("linear")
    plt.title('Acceleration')
    plt.xlabel('Time, s')
    plt.ylabel('Acceleration, g')
    plt.grid('on')
    plt.legend()

    plt.subplot(r, c, 2)
    plt.plot(timeArray, VxArray, '-ob', label="Vx")
    plt.plot(timeArray, VyArray, '-og', label="Vy")
    plt.plot(timeArray, VzArray, '-or', label="Vz")
    plt.xscale("linear")
    plt.yscale("linear")
    plt.title('Velocity')
    plt.xlabel('Time, s')
    plt.ylabel('Velocity, m/s')
    plt.grid('on')
    plt.legend()

    plt.subplot(r, c, 3)
    plt.plot(timeArray, PxArray, '-ob', label="Px")
    plt.plot(timeArray, PyArray, '-og', label="Py")
    plt.plot(timeArray, PzArray, '-or', label="Pz")
    plt.xscale("linear")
    plt.yscale("linear")
    plt.title('Position')
    plt.xlabel('Time, s')
    plt.ylabel('Altitude, m')
    plt.grid('on')
    plt.legend()

    plt.figure("Gryo X")
    plt.plot(timeArray, GxArray, '-ob', label="Gx")
    plt.plot(timeArray, GyArray, '-og', label="Gy")
    plt.plot(timeArray, GzArray, '-or', label="Gz")
    plt.xscale("linear")
    plt.yscale("linear")
    plt.title('Gyro')
    plt.xlabel('Time, s')
    plt.ylabel('Angular change, */s')
    plt.grid('on')
    plt.legend()

    plt.show()

plotData(OUTPUTFILE)