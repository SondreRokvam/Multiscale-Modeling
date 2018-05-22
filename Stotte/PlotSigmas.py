import numpy as np
import matplotlib.pyplot as plt

#Globale Directories
GitHub= 'C:/Multiscale-Modeling/'
Tekstfiler  = GitHub+'textfiles/'
change =100.0

def readSSData():
    # NOTE: you will probably need to change
    # the file path:
    fileName = Tekstfiler+'Sigmas7_0.txt'
    a = np.genfromtxt(fileName)
    a = np.transpose(a)  # In order to get time and E(t) in two columns
    b = float(a[0][0])
    a = a[:,1:]
    return a,b

def plotStressStrainData():
    Stresses, stray = readSSData()
    x =Stresses[0]*stray
    plt.ylabel('Stresses [GPa]')
    plt.xlabel('Strain')
    plt.plot(x,Stresses[1], 'bo--')
    plt.plot(x,Stresses[2], 'yo--')
    plt.plot(x,Stresses[3], 'ro--')
    plt.plot(x,Stresses[4], 'bx--')
    plt.plot(x,Stresses[5], 'gx--')
    plt.plot(x,Stresses[6], 'rx--')

    ymin, ymax = plt.ylim()
    xmin, xmax = plt.xlim()

    print (ymin, ymax, xmin, xmax)

    plt.xlim((xmin), (xmax))
    plt.ylim((ymin/(100)), (ymax / change))

    ymin, ymax = plt.ylim()
    xmin, xmax = plt.xlim()
    print (ymin, ymax, xmin, xmax)
    plt.tight_layout()
    plt.show()


plotStressStrainData()
