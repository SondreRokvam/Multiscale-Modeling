# -*- coding: utf-8 -*-
"""
Plot failure envelopes and stress envelopes
"""

import numpy as np
from matplotlib.collections import PatchCollection
import math
import matplotlib.pyplot as plt

GitHub = 'C:/Multiscale-Modeling/'
Envelope = GitHub + 'envelope.txt'

g = open(Envelope, "r")
tekst =g.read()
g.close()
lines=tekst.split('\n')
xnlist = list()
ynlist = list()
xslist = list()
yslist = list()
xenlist = list()
yenlist = list()
xeslist = list()
yeslist = list()
for line in lines:
    data = line.split('\t')
    xn = float(data[0])
    yn = float(data[1])
    xs = float(data[2])
    ys = float(data[3])
    xen = float(data[4])
    yen = float(data[5])
    xes = float(data[6])
    yes = float(data[7])

    xnlist.append(xn)
    ynlist.append(yn)
    xslist.append(xs)
    yslist.append(ys)
    xenlist.append(xen)
    yenlist.append(yen)
    xeslist.append(xes)
    yeslist.append(yes)
print(len(xnlist),len(ynlist),len(xslist),len(yslist),len(xenlist),len(yenlist),len(xeslist),len(xeslist))
"""
def maxStress(stresses,material):
    XT = material[1][0]
    XC = material[1][1]
    YT = material[1][2]
    YC = material[1][3]
    S12 = material[1][4]
    sig1=stresses[0]
    sig2=stresses[1]
    tau12=stresses[2]
    return max(sig1/XT, -sig1/XC, sig2/YT, -sig2/YC, abs(tau12/S12))

def tsaiWu(stresses,material):
    XT = material[1][0]
    XC = material[1][1]
    YT = material[1][2]
    YC = material[1][3]
    S12 = material[1][4]
    sig1=stresses[0]
    sig2=stresses[1]
    tau12=stresses[2]
    F1=(1/XT)-(1/XC)
    F2=(1/YT)-(1/YC)
    F11 = 1/(XT*XC)
    F22 = 1/(YT*YC)
    F66=1/(S12**2)
    f12=-0.5
    F12=f12*(F11*F22)**0.5
    a=F11*sig1**2 + F22*sig2**2 + 2*F12*sig1*sig2 + F66*tau12**2
    b=F1*sig1 + F2*sig2
    c=-1
    R=(-b+(b**2-4*a*c)**0.5)/(2*a)
    return 1/R
   """

### APPLICATIONS ###
      #                                    XT   XC   YT   YC   S12
materialA = ( (140000, 10000, 0.3, 5000), (1200, 800, 50, 150, 75) )
"""
maxStress_sig1=list()    # a list where values can be appended
maxStress_sig2=list()

tsaiWu_sig1=list()
tsaiWu_sig2=list()

for i in range(0,3600):
    sig1=math.cos(math.radians(i/10))
    sig2=math.sin(math.radians(i/10))
    stresses=(sig1,sig2,0)
    fE_maxStress=maxStress(stresses,materialA)
    fE_tsaiWu=tsaiWu(stresses,materialA)
    maxStress_sig1.append(sig1/fE_maxStress)
    maxStress_sig2.append(sig2/fE_maxStress)
    tsaiWu_sig1.append(sig1/fE_tsaiWu)
    tsaiWu_sig2.append(sig2/fE_tsaiWu)
    
    
    max(max(xslist),
    max(max(xeslist),
    
    """
s= float((max(xnlist)))*5/4
a= float((max(xenlist)))*5/4
print(s,a)
#plt.plot(maxStress_sig1,maxStress_sig2,tsaiWu_sig1,tsaiWu_sig2)
fig, (sx,ax) = plt.subplots(nrows=1, ncols=2,figsize=(10,5))


sx.set_title('Spenning')
sx.set_xlim(-s,s )
sx.set_ylim(-s,s )
sx.set_xticks(np.arange(-s, s, s/5))
sx.set_yticks(np.arange(-s, s, s/5))
sx.grid(True)

sx.plot(0.0,0.0,'x',xnlist,ynlist,'bo')

#,xslist,yslist,


ax.set_title('Toying')
ax.set_xlim(-a,a )
ax.set_ylim(-a,a )
ax.set_xticks(np.arange(-a , a , a/4))
ax.set_yticks(np.arange(-a,  a , a/4))
ax.grid(True)
ax.plot(0.0,0.0,'x',xenlist,yenlist,'rx')
#,xeslist,yeslist,'go')
plt.tight_layout()
plt.show()



    



