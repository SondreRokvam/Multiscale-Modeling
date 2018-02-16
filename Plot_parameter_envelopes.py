# -*- coding: utf-8 -*-
"""
Plot failure envelopes and stress envelopes
"""

import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter

def Get_sweeps(Samples):
    g = open(Envelope+str(nf*Samples)+'.txt', "r")
    tekst =g.read()
    g.close()
    lines=tekst.split('\n')
    return lines

def to_xy(Values):
    x = list()
    y = list()
    for i in range(0,len(Values)):
        x.append(math.cos(phi*i))
        y.append(math.sin(phi*i))
    return x,y


def invert(thing):
    Yield =1
    for b in range(0,len(Steg)):
        thing[b] =Yield/thing[b]
    return thing

#                                           XT   XC   YT   YC   S12
materialA = ( (140000, 10000, 0.3, 5000), (1200, 800, 50, 150, 75) )

nf=1
GitHub = 'C:/Multiscale-Modeling/'
Envelope = GitHub + 'envelope'

""" Lage RVE modell"""
Sample=[0,4,25,50]
for Samples in Sample:
    maxMises = list()
    minMises = list()
    maxNormSpen = list()
    minNormSpen = list()
    maxNormToy = list()
    minNormToy = list()
    maxSherSpen = list()
    maxSherToy = list()
    maxPrince  =list()
    minPrince  =list()
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
        maxPrince.append(float(data[8]))
        minPrince.append(float(data[9]))

    Scale = 10 / 9                              #Graf zoom out

    phi = (1 / len(maxMises)) * 2 * math.pi  # Angular stepsize

    Steg = np.arange(0, 2 * math.pi, phi)

    plotinfo =    [['max Mises Stresses',                      invert(maxMises)],
                    ['min Mises Stresses',                      invert(minMises)],
                    ['max Principal Stresses',                  invert(maxPrince)],
                    ['min Principal Stresses',                  invert(minPrince)],
                    ['max Normal xyz orientated  Stresses',     invert(maxNormToy)],
                    ['min Normal xyz orientated  Stresses',     invert(minNormToy)],
                    ['max Normal xyz orientated  Toying',       invert(maxNormToy)],
                    ['min Normal xyz orientated  Toying',       invert(minNormToy)],
                    ['max Shear  xyz  orientated Stresses',     invert(maxSherSpen)],
                    ['max Shear  xyz  orientated Toying',       invert(maxSherToy)]]

    straight_plotaxe = ['R', 'Stress sweep angle']
    angular_plotaxe = ['σ2 (y)', 'σ3 (x)']

    rows =5
    col = 4
    fig, ((sx1, sx2,sx3,sx4),(ax1, ax2,ax3,ax4),(dx1, dx2,dx3,dx4),(px1, px2,px3,px4),(fx1, fx2,fx3,fx4)) = plt.subplots(nrows=rows, ncols=col, figsize=(15, 15))
    a = [[sx1, sx2,sx3,sx4],[ax1, ax2,ax3,ax4],[dx1, dx2,dx3,dx4],[px1, px2,px3,px4],[fx1, fx2,fx3,fx4]]


    for num in range(0,len(a)):
        for plot in range(0,int(col/2)):
            count = 2*num+plot
            #


            x,y = to_xy(plotinfo[count][1])
            my1 = max(max(y),abs(min(y)))*Scale
            my2 = max(max(plotinfo[count][1]),abs(min(plotinfo[count][1])))
            mx1 = max(max(x),abs(min(x)))*Scale
            job1 = a[num][2*plot]
            job2 = a[num][2*plot+1]
            job1.set_title(plotinfo[count][0])
            job2.set_title(plotinfo[count][0])
            job1.set_xlim(-mx1, mx1)
            job2.set_xlim(-phi, (len(minMises) + 1) * phi)
            job1.set_ylim(-my1, my1)
            job2.set_ylim(-my2, my2)
            job1.set_xticks(np.arange(-mx1, mx1, mx1 / 5))
            job2.set_xticks(np.arange(-phi, (len(minMises) + 1) * phi,phi))
            job1.set_yticks(np.arange(-my1, my1, my1 / 5))
            job2.set_yticks(np.arange(-my2, my2, my2 / 5))
            job1.set_xlabel(angular_plotaxe[0])
            job2.set_xlabel(straight_plotaxe[0])
            job1.set_ylabel(angular_plotaxe[1])
            job2.set_ylabel(straight_plotaxe[1])
            job1.grid(True)
            job2.grid(True)
            job1.plot(x,y,'k--')
            job2.plot(Steg,plotinfo[count][1],'k--')

    """%%%%%%%%%%%%%%%%%%%%%%%"""
    """Sirkelplot Spenninger
for plot in range(0,len(plotinfo)
    sub_id, Title, xlabel, ylabel, ):
    sub_id.set_title(Title)
    maP.set_xlim(-MAP,MAP )
    maP.set_ylim(-MAP,MAP )
    maP.set_xticks(np.arange(-MAP, MAP, MAP/5))
    maP.set_yticks(np.arange(-MAP, MAP, MAP/5))
    maP.set_xlabel('Sig2 (y)')
    maP.set_ylabel('Sig3 (z)')
    maP.grid(True)
    maP.plot(XmaxPR, YmaxPR,0.0,0.0,'kx')


    miP.set_title('min Prince Spenninger')
    miP.set_xlim(-MIP,MIP )
    miP.set_ylim(-MIP,MIP )
    miP.set_xticks(np.arange(-MIP, MIP, MIP/5))
    miP.set_yticks(np.arange(-MIP, MIP, MIP/5))
    miP.set_xlabel('Sig2 (y)')
    miP.set_ylabel('Sig3 (z)')
    miP.grid(True)
    miP.plot(XminPR, YminPR,0.0,0.0,'kx')

    sx1.set_title('max og min Mises Spenninger')
    sx1.set_xlim(-ms,ms )
    sx1.set_ylim(-ms,ms )
    sx1.set_xticks(np.arange(-ms, ms, ms/5))
    sx1.set_yticks(np.arange(-ms, ms, ms/5))
    sx1.set_xlabel('Sig2 (y)')
    sx1.set_ylabel('Sig3 (z)')
    sx1.grid(True)
    sx1.plot(XmaxM, YmaxM,'r--',XminM, YminM,'b--',0.0,0.0,'kx')

    sx2.set_title('max og min Normal Spenning')
    sx2.set_xlim(-ns,ns )
    sx2.set_ylim(-ns,ns )
    sx2.set_xticks(np.arange(-ns, ns, ns/5))
    sx2.set_yticks(np.arange(-ns, ns, ns/5))
    sx2.set_xlabel('Sig2 (y)')
    sx2.set_ylabel('Sig3 (z)')
    sx2.grid(True)
    sx2.plot(XmaxNS, YmaxNS,'r--',XminNS, YminNS,'b--',0.0,0.0,'kx')

    ax1.set_title('max og min Normal')
    ax1.set_xlim(-a1,a1 )
    ax1.set_ylim(-a1,a1 )
    ax1.set_xticks(np.arange(-a1, a1, a1 / 5))
    ax1.set_yticks(np.arange(-a1, a1, a1 / 5))
    ax1.set_xlabel('Epsi2 (y)')
    ax1.set_ylabel('Epsi3 (z)')
    ax1.grid(True)
    ax1.plot(XmaxNT, YmaxNT,'r--',XminNT, YminNT,'b--',0.0,0.0,'kx')

    ST1.set_title('skjer Toyinger')
    ST1.set_xlim(-a_s,a_s )
    ST1.set_ylim(-a_s,a_s )
    ST1.set_xticks(np.arange(-a_s, a_s, a_s / 5))
    ST1.set_yticks(np.arange(-a_s, a_s, a_s / 5))
    ST1.set_xlabel('Epsi2 (y)')
    ST1.set_ylabel('Epsi3 (z)')
    ST1.grid(True)
    ST1.plot(XmaxST,YmaxST,'g--',0.0,0.0,'kx')

    ax2.set_title('Shear Stresses')
    ax2.set_xlim(-a2,a2 )
    ax2.set_ylim(-a2,a2 )
    ax2.set_xticks(np.arange(-a2, a2, a2 / 5))
    ax2.set_yticks(np.arange(-a2, a2, a2 / 5))
    ax2.set_xlabel('Sig2 (y)')
    ax2.set_ylabel('Sig3 (z)')
    ax2.grid(True)
    ax2.plot(XmaxSS,YmaxSS,'g--',0.0,0.0,'kx')

    Steg=np.arange(0,2*math.pi,phi)

    #invert
    maxMises = invert(maxMises,Steg)
    minMises = invert(minMises,Steg)
    maxNormSpen = invert(maxNormSpen,Steg)
    minNormSpen = invert(minNormSpen,Steg)
    maxNormToy = invert(maxNormToy,Steg)
    minNormToy = invert(minNormToy,Steg)
    maxSherSpen = invert(maxSherSpen,Steg)
    maxSherToy = invert(maxSherToy,Steg)


    sx3.set_title('max og min Mises')
    sx3.set_xlim(-phi, (len(minMises)+1)*phi)
    sx3.set_ylim(-ms, ms)
    sx3.set_xticks(np.arange(-phi, (len(minMises)+1)*phi, phi))
    sx3.set_yticks(np.arange(-ms, ms, ms / 5))
    sx3.set_xlabel('Sweepcases')
    sx3.set_ylabel('Prop load stress')
    sx3.grid(True)
    sx3.plot(Steg,maxMises, 'bo',Steg,minMises,'ro')

    sx4.set_title('max og min Normal Spenning')
    sx4.set_xlim(-phi, (len(minMises)+1)*phi)
    sx4.set_ylim(-ns, ns)
    sx4.set_xticks(np.arange(-phi, (len(minMises)+1)*phi, phi))
    sx4.set_yticks(np.arange(-ns, ns, ns / 5))
    sx4.set_xlabel('Sweepcases')
    sx4.set_ylabel('Prop load stress')
    sx4.grid(True)
    sx4.plot(Steg,maxNormSpen, 'ro', Steg,minNormSpen, 'bo')

    ax3.set_title('max og min Normal og skjer Toyinger')
    ax3.set_xlim(-phi, (len(minMises)+1)*phi )
    ax3.set_ylim(-a1,a1 )
    ax3.set_xticks(np.arange(-phi, (len(minMises)+1)*phi, phi))
    ax3.set_yticks(np.arange(-a1, a1, a1 / 5))
    ax3.set_xlabel('Sweepcases')
    ax3.set_ylabel('Prop load Strains')
    ax3.grid(True)
    ax3.plot(Steg,maxNormToy,'ro',Steg,minNormToy,'bo')


    ST3.set_title('skjer Toyinger')
    ST3.set_xlim(-phi, (len(minMises)+1)*phi )
    ST3.set_ylim(-a_s,a_s )
    ST3.set_xticks(np.arange(-phi, (len(minMises)+1)*phi, phi))
    ST3.set_yticks(np.arange(-a_s, a_s, a_s / 5))
    ST3.set_xlabel('Epsi2 (y)')
    ST3.set_ylabel('Epsi3 (z)')
    ST3.grid(True)
    ST3.plot(Steg,maxSherToy,'gx')


    ax4.set_title('Shear Stresses')
    ax4.set_xlim(-phi, (len(minMises)+1)*phi)
    ax4.set_ylim(-a2,a2 )
    ax4.set_xticks(np.arange(-phi, (len(minMises)+1)*phi, phi))
    ax4.set_yticks(np.arange(-a2, a2, a2 / 5))
    ax4.set_xlabel('Sweepcases')
    ax4.set_ylabel('Prop load stress')
    ax4.grid(True)
    ax4.plot(Steg,maxSherSpen,'gx')

    """

    plt.tight_layout()
    fig.savefig('D:/graph'+str(int(Samples*nf))+'.png')
plt.show()



    




