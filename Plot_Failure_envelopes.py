# -*- coding: utf-8 -*-
"""
Plot failure envelopes and stress envelopes
"""

import numpy as np
from matplotlib.collections import PatchCollection
import math
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter

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
print(xslist,yslist,'\n', len(xslist), len(yslist))

print(xeslist,yeslist,'\n', len(xeslist), len(yeslist))
#print(len(xnlist),len(ynlist),len(xslist),len(yslist),len(xenlist),len(yenlist),len(xeslist),len(xeslist))
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


#plt.plot(maxStress_sig1,maxStress_sig2,tsaiWu_sig1,tsaiWu_sig2)


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
s1= float((max(max(xnlist), max(ynlist))))*5/4
s2= float((max(max(xslist), max(yslist))))*5/4

a1= float((max(max(xenlist),max(yenlist))))*5/4
a2= float((max(max(xeslist),max(yeslist))))*5/4


fig, ((sx1,sx2),(ax1,ax2)) = plt.subplots(nrows=2,ncols=2,figsize=(10,5))

sx1.set_title('Normal Spenning')
sx1.set_xlim(-s1,s1 )
sx1.set_ylim(-s1,s1 )
sx1.set_xticks(np.arange(-s1, s1, s1/5))
sx1.set_yticks(np.arange(-s1, s1, s1/5))
sx1.grid(True)
sx1.plot(0.0,0.0,'rx',xnlist,ynlist,'bo')

sx2.set_title('Shear Spenning')
sx2.set_xlim(-s2,s2 )
sx2.set_ylim(-s2,s2 )
sx2.set_xticks(np.arange(-s2, s2, s2/5))
sx2.set_yticks(np.arange(-s2, s2, s2/5))
sx2.grid(True)
sx2.plot(0.0,0.0,'rx',xslist,yslist,'go')

ax1.set_title('Normal Toying')
ax1.set_xlim(-a1,a1 )
ax1.set_ylim(-a1,a1 )
ax1.set_xticks(np.arange(-a1 , a1 , a1/4))
ax1.set_yticks(np.arange(-a1,  a1 , a1/4))
ax1.grid(True)
ax1.plot(0.0,0.0,'ro',xenlist,yenlist,'bx')

ax2.set_title('Shear Toying')
ax2.set_xlim(-a2,a2 )
ax2.set_ylim(-a2,a2 )
ax2.set_xticks(np.arange(-a2 , a2 , a2/4))
ax2.set_yticks(np.arange(-a2,  a2 , a2/4))
ax2.grid(True)
ax2.plot(0.0,0.0,'ro',xeslist,yeslist,'gx')
plt.gca().yaxis.set_minor_formatter(NullFormatter())
plt.tight_layout()
plt.show()



    



