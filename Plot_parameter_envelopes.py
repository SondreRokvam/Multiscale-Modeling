# -*- coding: utf-8 -*-
"""
Plot failure envelopes and stress envelopes
"""

import numpy as np
from matplotlib.collections import PatchCollection
import math
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter

#                                           XT   XC   YT   YC   S12
materialA = ( (140000, 10000, 0.3, 5000), (1200, 800, 50, 150, 75) )

nf=0



def to_xy(Values):
    x = list()
    y = list()
    for i in range(0,len(Values)):
        x.append(math.cos(phi*i)*Values[i])
        y.append(math.sin(phi*i)*Values[i])
    return x,y

GitHub = 'C:/Multiscale-Modeling/'
Envelope = GitHub + 'envelope'

maxMises = list()
minMises = list()
maxNormSpen = list()
minNormSpen = list()
maxNormToy = list()
minNormToy = list()
maxSherSpen = list()
maxSherToy = list()

g = open(Envelope+str(nf)+'.txt', "r")
tekst =g.read()
print(tekst)
g.close()
lines=tekst.split('\n')
for line in lines:
    data = line.split('\t')
    maxMises.append(float(data[0]))
    minMises.append(float(data[1]))
    maxNormSpen.append(float(data[2]))
    minNormSpen.append(float(data[3]))
    maxNormToy.append(float(data[4]))
    minNormToy.append(float(data[5]))
    maxSherSpen.append(float(data[6]))
    maxSherToy.append(float(data[7]))

phi=(1/len(maxMises))*2*math.pi
print(phi,phi*360/(2*math.pi),len(maxMises),360/len(maxMises))



# s1 = maxMises og minMises
# s2 = max og min NormsSpen

# a1= Max og min Norm toy og sher toy
# a2 =Max sherspen

fig, ((sx1,sx2),(ax1,ax2)) = plt.subplots(nrows=2,ncols=2,figsize=(6,5))

XmaxM, YmaxM =to_xy(maxMises)
XminM, YminM =to_xy(minMises)

XmaxNS, YmaxNS =to_xy(maxNormSpen)
XminNS, YminNS =to_xy(minNormSpen)

XmaxNT, YmaxNT =to_xy(maxNormToy)
XminNT, YminNT =to_xy(minNormToy)
XmaxST, YmaxST =to_xy(maxSherToy)

XmaxSS, YmaxSS =to_xy(maxSherSpen)



s1= float((max(max(maxMises), abs(min(minMises)))))*5/4
s2= float((max(max(maxNormSpen), abs(min(minNormSpen)))))*5/4

a1= float((max(max(maxSherToy), max(maxNormToy), abs(min(minNormToy)))))*5/4
a2= float(max(maxSherSpen))*5/4




sx1.set_title('max og min Mises')
sx1.set_xlim(-s1,s1 )
sx1.set_ylim(-s1,s1 )
sx1.set_xticks(np.arange(-s1, s1, s1/5))
sx1.set_yticks(np.arange(-s1, s1, s1/5))
sx1.grid(True)
sx1.plot(0.0,0.0,'kx',XmaxM, YmaxM,'ro',XminM, YminM,'bo')

sx2.set_title('max og min Normal Spenning')
sx2.set_xlim(-s2,s2 )
sx2.set_ylim(-s2,s2 )
sx2.set_xticks(np.arange(-s2, s2, s2/5))
sx2.set_yticks(np.arange(-s2, s2, s2/5))
sx2.grid(True)
sx2.plot(0.0,0.0,'kx',XmaxNS, YmaxNS,'ro',XminNS, YminNS,'bo')

ax1.set_title('Toyinger')
ax1.set_xlim(-a1,a1 )
ax1.set_ylim(-a1,a1 )
ax1.set_xticks(np.arange(-a1 , a1 , a1/5))
ax1.set_yticks(np.arange(-a1,  a1 , a1/5))
ax1.grid(True)
ax1.plot(0.0,0.0,'kx',XmaxNT, YmaxNT,'ro',XminNT, YminNT,'bo',XmaxST, YmaxST,'gx')

ax2.set_title('Shear Stresses')
ax2.set_xlim(-a2,a2 )
ax2.set_ylim(-a2,a2 )
ax2.set_xticks(np.arange(-a2 , a2 , a2/5))
ax2.set_yticks(np.arange(-a2,  a2 , a2/5))
ax2.grid(True)
ax2.plot(0.0,0.0,'kx',XmaxSS, YmaxSS,'gx')
plt.gca().yaxis.set_minor_formatter(NullFormatter())
plt.tight_layout()
plt.show()



    



