import numpy as np

Yeah = np.genfromtxt('C:/MultiScaleMethod/Github/Multiscale-Modeling/Sweeps.txt')
count =0
scsc = 9973

for yih in Yeah:
    fifi = open('C:/MultiScaleMethod/Github/textfiles/Stiffness__InPST-' + str(int(yih*scsc)) + '.txt','r')
    tekst = fifi.read()
    fifi.close()
    lines = tekst.split('\n')
    print(yih)
    if (len(lines)-1)<25:
        print ('lines',len(lines)-1)
        parts = lines[-2].split('\t\t\t')
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


"""
    print('\n',num)
    fifi = open('C:/MultiScaleMethod/Github/textfiles/Stiffness__InY-' + str(int(ParameterSweep*scsc)) + '.txt','r')
    
a=np.arange[1,4,1]
print(a)
"""