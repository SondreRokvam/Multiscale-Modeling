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

nf=4
def Get_sweeps(Samples):
    g = open(Envelope+str(nf*Samples)+'.txt', "r")
    tekst =g.read()
    print(tekst)
    g.close()
    lines=tekst.split('\n')
    return lines


def to_xy(Values):
    x = list()
    y = list()
    for i in range(0,len(Values)):
        x.append(math.cos(phi*i)*Values[i])
        y.append(math.sin(phi*i)*Values[i])
    return x,y



for Samples in range(0,2):
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
    SweepCases = Get_sweeps(Samples)
    for line in SweepCases:
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

    #Lag plot
    fig, ((sx1, sx2),(sx3, sx4),(ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=4, ncols=2, figsize=(20,10))

    # s1 = maxMises og minMises
    # s2 = max og min NormsSpen

    # a1= Max og min Norm toy og sher toy
    # a2 =Max sherspen


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



                # Sirkelplot Spenninger

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
    ax1.set_xticks(np.arange(-a1, a1, a1 / 5))
    ax1.set_yticks(np.arange(-a1, a1, a1 / 5))
    print('subs')
    print('subs')
    ax1.grid(True)
    ax1.plot(0.0,0.0,'kx',XmaxNT, YmaxNT,'ro',XminNT, YminNT,'bo', XmaxST,YmaxST,'gx')

    ax2.set_title('Shear Stresses')
    ax2.set_xlim(-a2,a2 )
    ax2.set_ylim(-a2,a2 )
    ax2.set_xticks(np.arange(-a2, a2, a2 / 5))
    ax2.set_yticks(np.arange(-a2, a2, a2 / 5))
    ax2.grid(True)
    ax2.plot(XmaxSS,YmaxSS,'gx')

            #linear plot
    steplength =(1/len(maxMises))*2*math.pi
    Steg=np.arange(0,2*math.pi,steplength)

    print(len(minMises),len(Steg))


    sx3.set_title('max og min Mises')
    sx3.set_xlim(-steplength, (len(minMises)+1)*steplength)
    sx3.set_ylim(-s1, s1)
    sx3.set_xticks(np.arange(-steplength, (len(minMises)+1)*steplength, steplength))
    sx3.set_yticks(np.arange(-s1, s1, s1 / 5))
    sx3.grid(True)
    sx3.plot(Steg,maxMises, 'bo',Steg,minMises,'rx')

    sx4.set_title('max og min Normal Spenning')
    sx4.set_xlim(-steplength, (len(minMises)+1)*steplength)
    sx4.set_ylim(-s2, s2)
    sx4.set_xticks(np.arange(-steplength, (len(minMises)+1)*steplength, steplength))
    sx4.set_yticks(np.arange(-s2, s2, s2 / 5))
    sx4.grid(True)
    sx4.plot(Steg,maxNormSpen, 'ro', Steg,minNormSpen, 'bo')

    ax3.set_title('Toyinger')
    ax3.set_xlim(-steplength, (len(minMises)+1)*steplength )
    ax3.set_ylim(-a1,a1 )
    ax3.set_xticks(np.arange(-steplength, (len(minMises)+1)*steplength, steplength))
    ax3.set_yticks(np.arange(-a1, a1, a1 / 5))
    print('subs')
    print('subs')
    ax3.grid(True)

    ax3.plot(Steg,maxNormToy,'ro',Steg,minNormToy,'bo',Steg,maxSherToy,'gx')

    ax4.set_title('Shear Stresses')
    ax4.set_xlim(-steplength, (len(minMises)+1)*steplength)
    ax4.set_ylim(-a2,a2 )
    ax4.set_xticks(np.arange(-steplength, (len(minMises)+1)*steplength, steplength))
    ax4.set_yticks(np.arange(-a2, a2, a2 / 5))
    ax4.grid(True)
    ax4.plot(Steg,maxSherSpen,'gx')
    print('subs')

    plt.tight_layout()
    fig.savefig('D:/graph'+str(Samples)+'.png')



    



