import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
import os
#filelist = [f for f in os.listdir('C:/MultiScaleMethod/Github/textfiles/') if f.startswith('Stiffness__NF-')]
nums=[5, 14, 23,32,41,50,59]
colos=['b','c','g','y','m','r','k']
scsc=9973
#print(filelist)
#nums= [0.4,0.45,0.5,0.55,0.6,0.65,0.7]

plotsss=[]
for nfs in range(0,len(nums)):
    print(nums[nfs])
    fifi = open('C:/MultiScaleMethod/Github/textfiles/Stiffness__NF-' + str(int(nums[nfs]*scsc)) + '.txt','r')
    tekst = fifi.read()
    fifi.close()
    lines = tekst.split('\n')
    lines = lines[:-1]
    #print (lines)
    print ('lines',len(lines))
    allparts=[]
    for line in lines:
        parts = line.split('\t\t\t')
        part = parts[1]
        bits = part.split('\t\t')
        alldata=[]
        for bit in bits:
            data = bit.split('\t')
            for dat in data:
                alldata.append(float(dat))
        allparts.append(alldata)

    Ploting = np.zeros([36,len(allparts)])
    Xaxis= []
    for par in range(0,len(allparts)):
        Xaxis.append(par+1)
        for ci in range(0,36):
            Ploting[ci][par]=allparts[par][ci]
    plotsss.append([Ploting,'Stiffness__NF-' + str(int(nums[nfs]))])
    Cumavg= np.zeros([36,len(allparts)])
    for csi in range(0, 36):
        for x in range(0,len(Ploting[csi,:])):
            Cumavg[csi][x]=np.sum(Ploting[csi, :][0:(x+1)])/(x+1)


    #plt.plot(Xaxis, Cumavg[0, :],colos[nfs]+'-')

    for csi in range(0,36):
        plt.plot(Xaxis,Cumavg[csi,:],c=colos[nfs],ls ='-', label='NF-' + str(int(nums[nfs])))
        #plt.plot(Xaxis,Ploting[csi,:],'x')
        #plt.gca().legend(('NF-' + str(int(nums[nfs]))))
#plt.legend()
#plt.legend(loc=2)
plt.ylim(50, 65)
plt.ylim(11, 20)
#plt.ylim(2.5, 10)
#plt.ylim(-2.5, 2.5)
plt.xlim(0, 100)
plt.title('Stiffness convergence for number of fibers in RVEs')
plt.ylabel('Stiffness matrix constants [GPa]')
plt.xlabel('Number of RVEs')
#plt.tight_layout()
plt.show()


#for plot in plotsss:
for yeh in range(0, 36):
    yeh=0
    test=[]
    for plot in plotsss:
        test.append(plot[0][yeh][:])
    plt.boxplot(test)
    #plt.ylim(45, 65)
    #plt.ylim(11, 20)
    #plt.ylim(2.5, 10)
    #plt.ylim(-2.5, 2.5)
plt.tight_layout()
#plt.show()



