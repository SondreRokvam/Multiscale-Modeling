import numpy as np

#nums=[5, 10, 15,20,25,30,35,40,45,50,55]
#nums=[40,50,55]
nums= [400,450,500,550,600,650,700]
for num in nums:
    fifi = open('C:/MultiScaleMethod/Github/textfiles/Stiffness__VF-'+str(num)+'.txt','r')
    tekst = fifi.read()
    fifi.close()
    lines = tekst.split('\n')
    print(num)
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

a=np.arange[1,4,1]
print(a)
"""