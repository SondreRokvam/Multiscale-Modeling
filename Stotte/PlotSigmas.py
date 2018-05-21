import numpy as np
import matplotlib.pyplot as plt

#Globale Directories
GitHub= 'C:/Multiscale-Modeling/'
Tekstfiler  = GitHub+'textfiles/'


def readRelaxationData():
    # NOTE: you will probably need to change
    # the file path:
    fileName = Tekstfiler+'Sigmas4_0.txt'
    a = np.genfromtxt(fileName)
    a = np.transpose(a)  # In order to get time and E(t) in two columns
    b = float(a[0][0])
    a = a[:,1:]
    print(float(b*a[0][-1]))
    return a,b

def plotRelaxationData():
    Stresses, stray = readRelaxationData()
    x =Stresses[0]*stray
    plt.plot(x,Stresses[1], 'b-')
    plt.plot(x,Stresses[2], 'g-')
    plt.plot(x,Stresses[3], 'r-')
    plt.plot(x,Stresses[4], 'b--')
    plt.plot(x,Stresses[5], 'g--')
    plt.plot(x,Stresses[6], 'r--')
    change =100.0
    ymin, ymax = plt.ylim()
    xmin, xmax = plt.xlim()
    print (ymin, ymax, xmin, xmax)
    plt.ylim((ymin/change), (ymax/change))
    ymin, ymax = plt.ylim()
    xmin, xmax = plt.xlim()
    print (ymin, ymax, xmin, xmax)
    plt.tight_layout()
    ymin, ymax = plt.ylim()
    xmin, xmax = plt.xlim()
    print (ymin, ymax, xmin, xmax)
    plt.show()


plotRelaxationData()
