import numpy as np
import matplotlib.pyplot as plt

#Globale Directories
GitHub= 'C:/Multiscale-Modeling/'
Tekstfiler  = GitHub+'textfiles/'


def readRelaxationData():
    # NOTE: you will probably need to change
    # the file path:
    fileName = Tekstfiler+'Sigmas1_0.txt'
    a = np.genfromtxt(fileName)
    a = np.transpose(a)  # In order to get time and E(t) in two columns
    return a

def plotRelaxationData():
    Stresses = readRelaxationData()
    plt.plot(Stresses[0],Stresses[1], 'b-')
    plt.plot(Stresses[0],Stresses[2], 'g-')
    plt.plot(Stresses[0],Stresses[3], 'r-')
    plt.plot(Stresses[0],Stresses[4], 'b--')
    plt.plot(Stresses[0],Stresses[5], 'g--')
    plt.plot(Stresses[0],Stresses[6], 'r--')
    plt.tight_layout()
    plt.show()


plotRelaxationData()
