import numpy as np

Yeah = np.genfromtxt('C:/MultiScaleMethod/Github/Multiscale-Modeling/Sweeps.txt')
count =0
scsc = 9973
Yeah= Yeah[0:2]
print(Yeah)
nums=[5, 14, 23,32,41,50,59]


for yih in Yeah:
    print(yih)
    try:
        fifi = open('C:/MultiScaleMethod/Github/textfiles/Stiffness__Clear-' + str(int(yih*scsc)) + '.txt','r')
        tekst = fifi.read()
        fifi.close()
        lines = tekst.split('\n')
        lines = lines[0:-1]
        print('lines', len(lines))
        keys=[]
        for line in lines:
            part =line.split('\t\t\t')
            keys.append(part[0])
        #print ('key',keys)
        for i in range(0,len(keys)):
            for j in range(0, len(keys)):
                if i!=j:
                    if keys[i]==keys[j]:
                        print('dobbel')
    except:
        pass
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
