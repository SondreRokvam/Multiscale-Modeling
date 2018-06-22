import numpy as np
import matplotlib.pyplot as plt
import os
#Globale Directories
Tekstfiler  = 'C:/MultiScaleMethod/Github/textfiles/Stresstests/'

#Type =  tens_      comp_        sher_
#['Exx', 'Eyy', 'Ezz', 'Exy', 'Exz', 'Eyz']

Type = 'comp_'

#Sigmascomp_comp_EyyEzz0_0.txt
#filelist = [f for f in os.listdir(Tekstfiler) if f.startswith('Sigmas'+Type)]  # if not f.endswith('.inp')]
filelist = [f for f in os.listdir(Tekstfiler) ]  # if not f.endswith('.inp')]
print(len(filelist),'\n',filelist)
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
        plt.plot(x,Stresses[3], 'ro-',label='\u03C31')
        plt.plot(x,Stresses[1], 'b-',label='\u03C32')
        plt.plot(x,Stresses[2], 'y-',label='\u03C33')
        plt.plot(x,Stresses[4], 'g--',label='\u03C423')
        plt.plot(x,Stresses[5], 'c--',label='\u03C412')
        plt.plot(x,Stresses[6], 'm--',label='\u03C413')
        fis=fily.split('__')
        Test= 'Plasticity, Matrix damage and delamination '
        Title =Test+'Stress Strain curve:\n'+fis[0]
        plt.title(Title)
        plt.ylabel('Stresses [GPa]')
        plt.xlabel('Strain')

        plt.legend(loc='best')

        #ymin, ymax = plt.ylim()
        #xmin, xmax = plt.xlim()

        #print (ymin, ymax, xmin, xmax)

        #plt.xlim((xmin), (xmax))
        #plt.ylim((ymin / zoom), (ymax / zoom))

        #plt.xlim((0.94*xmax), (0.95*xmax))
        #plt.ylim((-0.007 ), (0.007 ))
        #ymin, ymax = plt.ylim()
        #xmin, xmax = plt.xlim()
        #print (ymin, ymax, xmin, xmax)
        plt.tight_layout()
        plt.savefig('C:/MultiScaleMethod/Github/Plots/'+Test+fily+'.png')
        plt.show()


        #Small scale zoom
        """
        Stresses, stray = readSSData(fily)
        x = Stresses[0] * stray
        plt.ylabel('Stresses [GPa]')
        plt.xlabel('Strain')
        plt.plot(x, Stresses[3], 'r-', label='\u03C31')
        plt.plot(x, Stresses[1], 'b-', label='\u03C32')
        plt.plot(x, Stresses[2], 'y-', label='\u03C33')
        plt.plot(x, Stresses[4], 'g--', label='\u03C423')
        plt.plot(x, Stresses[5], 'c--', label='\u03C412')
        plt.plot(x, Stresses[6], 'm--', label='\u03C413')
        fis = fily.split('__')
        Test = 'Plasticity, Matrix damage and delamination '
        Title = Test + 'Stress Strain curve:\n' + fis[0]
        plt.title(Title)
        plt.ylabel('Stresses [GPa]')
        plt.xlabel('Strain')

        plt.legend(loc='best')

        # ymin, ymax = plt.ylim()
        # xmin, xmax = plt.xlim()

        # print (ymin, ymax, xmin, xmax)

        # plt.xlim((xmin), (xmax))
        # plt.ylim((ymin / zoom), (ymax / zoom))

        # plt.xlim((0.94*xmax), (0.95*xmax))
        plt.ylim((-0.007 ), (0.007 ))
        # ymin, ymax = plt.ylim()
        # xmin, xmax = plt.xlim()
        # print (ymin, ymax, xmin, xmax)
        plt.tight_layout()
        # plt.savefig('C:/MultiScaleMethod/Github/Plots/'+Test+fis[0]+'.png')
        plt.show()
        """


plotStressStrainData()
