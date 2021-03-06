import numpy as np
import matplotlib.pyplot as plt
import os
#Globale Directories
Tekstfiler  = 'C:/MultiScaleMethod/Github/textfiles/Stresstests/'

#Type =  tens_      comp_        sher_
#['Exx', 'Eyy', 'Ezz', 'Exy', 'Exz', 'Eyz']

Type = 'comp_'

#Sigmascomp_comp_EyyEzz0_0.txt
filelist = [f for f in os.listdir(Tekstfiler) if f.startswith('Sigmas'+Type)]  # if not f.endswith('.inp')]
filelist = [f for f in os.listdir(Tekstfiler) if f.startswith('Sigmascomp_comp_Exx')]  # if not f.endswith('.inp')]
print(filelist)
def readSSData(fily):
    # NOTE: you will probably need to change
    # the file path:
    a = np.genfromtxt(Tekstfiler+fily)
    a = np.transpose(a)  # In order to get time and E(t) in two columns
    b = float(a[0][0])
    a = a[:,1:]
    return a,b

def plotStressStrainData():
    for fily in filelist:
        Stresses, stray = readSSData(fily)
        x =Stresses[0]*stray
        plt.ylabel('Stresses [GPa]')
        plt.xlabel('Strain')
        plt.plot(x,Stresses[1], 'b-')
        plt.plot(x,Stresses[2], 'y-')
        plt.plot(x,Stresses[3], 'r-')
        plt.plot(x,Stresses[4], 'g--')
        plt.plot(x,Stresses[5], 'c--')
        plt.plot(x,Stresses[6], 'm--')

        plt.title('Stress Strain curve'+fily[0:15])
        plt.ylabel('Stresses [GPa]')
        plt.xlabel('Strain')

        #ymin, ymax = plt.ylim()
        #xmin, xmax = plt.xlim()

        #print (ymin, ymax, xmin, xmax)

        #plt.xlim((xmin), (xmax))
        #plt.ylim((ymin / zoom), (ymax / zoom))

        #plt.xlim((0.94*xmax), (0.95*xmax))
        #plt.ylim((-0.007 / zoom), (0.007 / zoom))
        #ymin, ymax = plt.ylim()
        #xmin, xmax = plt.xlim()
        #print (ymin, ymax, xmin, xmax)
        plt.tight_layout()
        plt.show()

    for fily in filelist:
        Stresses, stray = readSSData(fily)
        x =Stresses[0]*stray
        plt.ylabel('Stresses [GPa]')
        plt.xlabel('Strain')
        plt.plot(x,Stresses[1], 'b-')
        plt.plot(x,Stresses[2], 'y-')
        plt.plot(x,Stresses[3], 'r-')
        plt.plot(x,Stresses[4], 'g--')
        plt.plot(x,Stresses[5], 'c--')
        plt.plot(x,Stresses[6], 'm--')

        plt.title('Stress Strain curve for RVE')
        plt.ylabel('Stresses [GPa]')
        plt.xlabel('Strain')

        ymin, ymax = plt.ylim()
        xmin, xmax = plt.xlim()

        #print (ymin, ymax, xmin, xmax)



        #plt.xlim((0.94*xmax), (0.95*xmax))
        #plt.ylim((-0.007 / zoom), (0.007 / zoom))
        #print (ymin, ymax, xmin, xmax)
    plt.tight_layout()
    plt.show()

    """
        plt.plot(x, Stresses[1], 'bo--')
        plt.plot(x, Stresses[2], 'yo--')
        plt.plot(x, Stresses[3], 'ro--')
        plt.plot(x, Stresses[4], 'bx--')
        plt.plot(x, Stresses[5], 'gx--')
        plt.plot(x, Stresses[6], 'rx--')
        #plt.xlim(xmin, (0.01))
        plt.ylim((-0.007 / zoom), (0.007 / zoom))
        plt.tight_layout()
        plt.show()
        """


plotStressStrainData()
