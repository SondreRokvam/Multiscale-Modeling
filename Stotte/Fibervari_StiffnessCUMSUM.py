import matplotlib.pyplot as plt
import numpy as np


Yeah = np.genfromtxt('C:/MultiScaleMethod/Github/Multiscale-Modeling/Sweeps.txt')
count =0
scsc = 9973
Yeah= Yeah[0:2]
print(Yeah)

count =0
plotsss=[]
for num in Yeah:

    print('\n',num)
    fifi = open('C:/MultiScaleMethod/Github/textfiles/Stiffness__FibVari-'+str(int(num*scsc))+'.txt','r')
    tekst = fifi.read()
    fifi.close()
    lines = tekst.split('\n')
    lines = lines[:-1]
    # print (lines)
    if len(lines) >= 50:
        lines = lines[0:5]
    print('lines', len(lines))
    allparts = []
    for line in lines:
        parts = line.split('\t\t\t')
        part = parts[1]
        bits = part.split('\t\t')
        alldata = []
        for bit in bits:
            data = bit.split('\t')
            for dat in data:
                alldata.append(float(dat))
        allparts.append(alldata)

    Ploting = np.zeros([36, len(allparts)])
    Xaxis = []
    for par in range(0, len(allparts)):
        Xaxis.append(par + 1)
        for ci in range(0, 36):
            Ploting[ci][par] = allparts[par][ci]
    plotsss.append([Ploting, 'Stiffness__VF-' + str(int(num))])
    Cumavg = np.zeros([36, len(allparts)])
    for csi in range(0, 36):
        for x in range(0, len(Ploting[csi, :])):
            Cumavg[csi][x] = np.sum(Ploting[csi, :][0:(x + 1)]) / (x + 1)
    plt.title('Clearing distance effect on stiffness')
    plt.ylabel('Stiffness matrix constants [GPa]')
    plt.xlabel('Clearing distance')

for yeh in range(0, 36):
    test=[]
    for plot in plotsss:
        test.append(plot[0][yeh][:])
    plt.boxplot(test)
    #plt.ylim(50, 62.5)
    #plt.ylim(9, 18)
    #plt.ylim(2.5, 7.5)
    #plt.ylim(-1, 2)
plt.title('Effect of fiber variation')
plt.ylabel('Stiffness matrix constants [GPa]')
plt.xlabel('Fiber variation')
plt.tight_layout()
plt.show()




