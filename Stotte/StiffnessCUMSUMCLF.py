import matplotlib.pyplot as plt
import numpy as np

nums=[5, 10, 15,20,25,30,35,40,45,50,55]
nums= [5000,7500,10000,12500,15000,17500,20000,22500,25000,27500,30000]
nummy= [0.005,0.0075,0.01,0.012500,0.0150,0.0175,0.02,0.0225,0.0250,0.0275,0.03]
count =0
for num in nums:

    print('\n',num)
    fifi = open('C:/MultiScaleMethod/Github/textfiles/Stiffness__CLF-'+str(num)+'.txt','r')
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
    print(len(Ploting))
    Xaxis= []
    for par in range(0,len(allparts)):
        Xaxis.append(par+1)
        for ci in range(0,36):
            Ploting[ci][par]=allparts[par][ci]
    print(Ploting[0,:])

    #Cumsum
    Cumavg= np.zeros([36,len(allparts)])
    for csi in range(0, 36):
        for x in range(0,len(Ploting[csi,:])):
            Cumavg[csi][x]=np.sum(Ploting[csi, :][0:(x+1)])/(x+1)

    plt.title('Clearing distance effect on stiffness')
    plt.ylabel('Stiffness matrix constants [GPa]')
    plt.xlabel('Clearing distance')

    for asa in range(0,len(Ploting[csi, :])):
        plt.plot(nummy[count], Ploting[csi, asa], '+')

    for csi in range(0,36):
        plt.plot(nummy[count],Cumavg[csi,-1],'x')
        #plt.plot(Xaxis,Ploting[csi,:],'x')
    #plt.xlim(0, 25)
    #plt.ylim(55, 62)
    #plt.ylim(12.5, 20)
    #plt.ylim(2.5, 8)
    #plt.ylim(-1.5/2, 1.5/2)
    count = count + 1
plt.tight_layout()
plt.show()




