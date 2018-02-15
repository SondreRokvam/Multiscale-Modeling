# -*- coding: utf-8 -*-
"""
Plot failure envelopes and stress envelopes
"""

import numpy as np
from matplotlib.collections import PatchCollection
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

    Yield =1
    x = list()
    y = list()
    for i in range(0,len(Values)):
        x.append(math.cos(phi*i)*Yield/Values[i])
        y.append(math.sin(phi*i)*Yield/Values[i])
    return x,y

def return_data(plotnr):


    maxMises = invert(maxMises)
    minMises = invert(minMises)
    maxNormSpen = invert(maxNormSpen)
    minNormSpen = invert(minNormSpen)
    maxNormToy = invert(maxNormToy, Steg)
    minNormToy = invert(minNormToy, Steg)
    maxSherSpen = invert(maxSherSpen, Steg)
    maxSherToy = invert(maxSherToy, Steg)
    ((plot1, sx3), (maP, miP), (sx2, sx4), (ax2, ax4), (ax1, ax3), (ST1, ST3))
    plotinfo =      [['max,min Mises Stresses', 'sirkelplot',   sx1, MAP, 'σ2 (y)', 'σ3 (x)',               XmaxPR, YmaxPR
                    [[plotinfo[0][0],           'linearplot',   sx2, ms, 'R',       'Stress sweep angle',   max, YmaxPR
                    [['max Principal Stresses', plotinfo[1][0], sx3, MAP, 'σ2 (y)', 'σ3 (x)', XmaxPR, YmaxPR
                    [['min Principal Stresses', plotinfo[1][0], sx4, MAP, 'σ2 (y)', 'σ3 (x)', XmaxPR, YmaxPR
                    [['max Principal Stresses', plotinfo[1][0], sx5, MAP, 'σ2 (y)', 'σ3 (x)', XmaxPR, YmaxPR
                    [['max Principal Stresses', plotinfo[1][0], sx6, MAP, 'σ2 (y)', 'σ3 (x)', XmaxPR, YmaxPR
                    [['max Principal Stresses', plotinfo[1][0], sx7, MAP, 'σ2 (y)', 'σ3 (x)', XmaxPR, YmaxPR
                    [['max Principal Stresses', plotinfo[1][0], sx8, MAP, 'σ2 (y)', 'σ3 (x)', XmaxPR, YmaxPR
                    [['max Principal Stresses', plotinfo[1][0], sx9, MAP, 'σ2 (y)', 'σ3 (x)', XmaxPR, YmaxPR
    sx3.set_title('max og min Mises')
    sx3.set_xlim(-steplength, (len(minMises) + 1) * steplength)
    sx3.set_ylim(-ms, ms)
    sx3.set_xticks(np.arange(-steplength, (len(minMises) + 1) * steplength, steplength))
    sx3.set_yticks(np.arange(-ms, ms, ms / 5))
    sx3.set_xlabel('Sweepcases')
    sx3.set_ylabel('Prop load stress')
    sx3.grid(True)
    sx3.plot(Steg, maxMises, 'bo', Steg, minMises, 'ro')
                      maP.set_title('max Prince Spenninger')
                      maP.set_xlim(-MAP, MAP)
                      maP.set_ylim(-MAP, MAP)
                      maP.set_xticks(np.arange(-MAP, MAP, MAP / 5))
                      maP.set_yticks(np.arange(-MAP, MAP, MAP / 5))
                      maP.set_xlabel('Sig2 (y)')
                      maP.set_ylabel('Sig3 (z)')
                      maP.grid(True)
                      maP.plot(XmaxPR, YmaxPR, 0.0, 0.0, 'kx')


                      miP.set_title('min Prince Spenninger')
                      miP.set_xlim(-MIP, MIP)
                      miP.set_ylim(-MIP, MIP)
                      miP.set_xticks(np.arange(-MIP, MIP, MIP / 5))
                      miP.set_yticks(np.arange(-MIP, MIP, MIP / 5))
                      miP.set_xlabel('Sig2 (y)')
                      miP.set_ylabel('Sig3 (z)')
                      miP.grid(True)
                      miP.plot(XminPR, YminPR, 0.0, 0.0, 'kx')

                      sx1.set_title('max og min Mises Spenninger')
                      sx1.set_xlim(-ms, ms)
                      sx1.set_ylim(-ms, ms)
                      sx1.set_xticks(np.arange(-ms, ms, ms / 5))
                      sx1.set_yticks(np.arange(-ms, ms, ms / 5))
                      sx1.set_xlabel('Sig2 (y)')
                      sx1.set_ylabel('Sig3 (z)')
                      sx1.grid(True)
                      sx1.plot(XmaxM, YmaxM, 'r--', XminM, YminM, 'b--', 0.0, 0.0, 'kx')

                      sx2.set_title('max og min Normal Spenning')
                      sx2.set_xlim(-ns, ns)
                      sx2.set_ylim(-ns, ns)
                      sx2.set_xticks(np.arange(-ns, ns, ns / 5))
                      sx2.set_yticks(np.arange(-ns, ns, ns / 5))
                      sx2.set_xlabel('Sig2 (y)')
                      sx2.set_ylabel('Sig3 (z)')
                      sx2.grid(True)
                      sx2.plot(XmaxNS, YmaxNS, 'r--', XminNS, YminNS, 'b--', 0.0, 0.0, 'kx')

                      ax1.set_title('max og min Normal')
                      ax1.set_xlim(-a1, a1)
                      ax1.set_ylim(-a1, a1)
                      ax1.set_xticks(np.arange(-a1, a1, a1 / 5))
                      ax1.set_yticks(np.arange(-a1, a1, a1 / 5))
                      ax1.set_xlabel('Epsi2 (y)')
                      ax1.set_ylabel('Epsi3 (z)')
                      ax1.grid(True)
                      ax1.plot(XmaxNT, YmaxNT, 'r--', XminNT, YminNT, 'b--', 0.0, 0.0, 'kx')

                      ST1.set_title('skjer Toyinger')
                      ST1.set_xlim(-a_s, a_s)
                      ST1.set_ylim(-a_s, a_s)
                      ST1.set_xticks(np.arange(-a_s, a_s, a_s / 5))
                      ST1.set_yticks(np.arange(-a_s, a_s, a_s / 5))
                      ST1.set_xlabel('Epsi2 (y)')
                      ST1.set_ylabel('Epsi3 (z)')
                      ST1.grid(True)
                      ST1.plot(XmaxST, YmaxST, 'g--', 0.0, 0.0, 'kx')

                      ax2.set_title('Shear Stresses')
                      ax2.set_xlim(-a2, a2)
                      ax2.set_ylim(-a2, a2)
                      ax2.set_xticks(np.arange(-a2, a2, a2 / 5))
                      ax2.set_yticks(np.arange(-a2, a2, a2 / 5))
                      ax2.set_xlabel('Sig2 (y)')
                      ax2.set_ylabel('Sig3 (z)')
                      ax2.grid(True)
                      ax2.plot(XmaxSS, YmaxSS, 'g--', 0.0, 0.0, 'kx')


                      """%%%%%%%%%%%%%%%%%%%%%%%"""
                      """linear plots"""
                      Steg = np.arange(0, 2 * math.pi, steplength)

    # invert
    maxMises = invert(maxMises)
    minMises = invert(minMises, Steg)
    maxNormSpen = invert(maxNormSpen, Steg)
    minNormSpen = invert(minNormSpen, Steg)
    maxNormToy = invert(maxNormToy, Steg)
    minNormToy = invert(minNormToy, Steg)
    maxSherSpen = invert(maxSherSpen, Steg)
    maxSherToy = invert(maxSherToy, Steg)



    sx4.set_title('max og min Normal Spenning')
    sx4.set_xlim(-steplength, (len(minMises) + 1) * steplength)
    sx4.set_ylim(-ns, ns)
    sx4.set_xticks(np.arange(-steplength, (len(minMises) + 1) * steplength, steplength))
    sx4.set_yticks(np.arange(-ns, ns, ns / 5))
    sx4.set_xlabel('Sweepcases')
    sx4.set_ylabel('Prop load stress')
    sx4.grid(True)
    sx4.plot(Steg, maxNormSpen, 'ro', Steg, minNormSpen, 'bo')

    ax3.set_title('max og min Normal og skjer Toyinger')
    ax3.set_xlim(-steplength, (len(minMises) + 1) * steplength)
    ax3.set_ylim(-a1, a1)
    ax3.set_xticks(np.arange(-steplength, (len(minMises) + 1) * steplength, steplength))
    ax3.set_yticks(np.arange(-a1, a1, a1 / 5))
    ax3.set_xlabel('Sweepcases')
    ax3.set_ylabel('Prop load Strains')
    ax3.grid(True)
    ax3.plot(Steg, maxNormToy, 'ro', Steg, minNormToy, 'bo')

    ST3.set_title('skjer Toyinger')
    ST3.set_xlim(-steplength, (len(minMises) + 1) * steplength)
    ST3.set_ylim(-a_s, a_s)
    ST3.set_xticks(np.arange(-steplength, (len(minMises) + 1) * steplength, steplength))
    ST3.set_yticks(np.arange(-a_s, a_s, a_s / 5))
    ST3.set_xlabel('Epsi2 (y)')
    ST3.set_ylabel('Epsi3 (z)')
    ST3.grid(True)
    ST3.plot(Steg, maxSherToy, 'gx')

    ax4.set_title('Shear Stresses')
    ax4.set_xlim(-steplength, (len(minMises) + 1) * steplength)
    ax4.set_ylim(-a2, a2)
    ax4.set_xticks(np.arange(-steplength, (len(minMises) + 1) * steplength, steplength))
    ax4.set_yticks(np.arange(-a2, a2, a2 / 5))
    ax4.set_xlabel('Sweepcases')
    ax4.set_ylabel('Prop load stress')
    ax4.grid(True)
    ax4.plot(Steg, maxSherSpen, 'gx')

    return_data()
    ]]
    return
def inverted(thing):
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

    phi=(1/len(maxMises))*2*math.pi
    steplength =(1/len(maxMises))*2*math.pi
    #Lag plot
    fig, ((sx1, sx3),(maP,miP),(sx2, sx4), (ax2, ax4),(ax1, ax3),(ST1, ST3)) = plt.subplots(nrows=6, ncols=2, figsize=(15,15))

    """  s1 s3 = maxMises og minMises          a1 a3 = Max og min Norm toy og sher toy
         s2 s4= max og min NormsSpen           a2 a4 = Max sherspen
    """


    Scale = 10/9
    #Finne max x og y til plottene
    ms= float(max(max(max(XmaxM),max(YmaxM)), abs(min(min(XminM),min(YminM)))))*Scale
    ns= float((max(max(max(XmaxNS), max(YmaxNS)), abs(min(min(XminNS),min(YminM))))))*Scale

    MAP =float((max(max(XmaxPR),max(YmaxPR))))*Scale
    MIP = float((max(abs(min(XminPR)),abs(min(YminPR)))))*Scale

    a1= float((max(max(max(XmaxNT), max(YmaxNT)), abs(min((min(XminNT),min(YminNT)))))))*Scale
    a_s= float((max(max(XmaxST), max(YmaxST))))*Scale
    a2=  float((max(max(XmaxSS),max(YmaxSS))))*Scale


    """%%%%%%%%%%%%%%%%%%%%%%%"""
    """Sirkelplot Spenninger"""
for plot in plots(sub_id, Title, xlabel, ):
    maP.set_title('max Prince Spenninger')
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


    """%%%%%%%%%%%%%%%%%%%%%%%"""
    """linear plots"""
    Steg=np.arange(0,2*math.pi,steplength)

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
    sx3.set_xlim(-steplength, (len(minMises)+1)*steplength)
    sx3.set_ylim(-ms, ms)
    sx3.set_xticks(np.arange(-steplength, (len(minMises)+1)*steplength, steplength))
    sx3.set_yticks(np.arange(-ms, ms, ms / 5))
    sx3.set_xlabel('Sweepcases')
    sx3.set_ylabel('Prop load stress')
    sx3.grid(True)
    sx3.plot(Steg,maxMises, 'bo',Steg,minMises,'ro')

    sx4.set_title('max og min Normal Spenning')
    sx4.set_xlim(-steplength, (len(minMises)+1)*steplength)
    sx4.set_ylim(-ns, ns)
    sx4.set_xticks(np.arange(-steplength, (len(minMises)+1)*steplength, steplength))
    sx4.set_yticks(np.arange(-ns, ns, ns / 5))
    sx4.set_xlabel('Sweepcases')
    sx4.set_ylabel('Prop load stress')
    sx4.grid(True)
    sx4.plot(Steg,maxNormSpen, 'ro', Steg,minNormSpen, 'bo')

    ax3.set_title('max og min Normal og skjer Toyinger')
    ax3.set_xlim(-steplength, (len(minMises)+1)*steplength )
    ax3.set_ylim(-a1,a1 )
    ax3.set_xticks(np.arange(-steplength, (len(minMises)+1)*steplength, steplength))
    ax3.set_yticks(np.arange(-a1, a1, a1 / 5))
    ax3.set_xlabel('Sweepcases')
    ax3.set_ylabel('Prop load Strains')
    ax3.grid(True)
    ax3.plot(Steg,maxNormToy,'ro',Steg,minNormToy,'bo')


    ST3.set_title('skjer Toyinger')
    ST3.set_xlim(-steplength, (len(minMises)+1)*steplength )
    ST3.set_ylim(-a_s,a_s )
    ST3.set_xticks(np.arange(-steplength, (len(minMises)+1)*steplength, steplength))
    ST3.set_yticks(np.arange(-a_s, a_s, a_s / 5))
    ST3.set_xlabel('Epsi2 (y)')
    ST3.set_ylabel('Epsi3 (z)')
    ST3.grid(True)
    ST3.plot(Steg,maxSherToy,'gx')


    ax4.set_title('Shear Stresses')
    ax4.set_xlim(-steplength, (len(minMises)+1)*steplength)
    ax4.set_ylim(-a2,a2 )
    ax4.set_xticks(np.arange(-steplength, (len(minMises)+1)*steplength, steplength))
    ax4.set_yticks(np.arange(-a2, a2, a2 / 5))
    ax4.set_xlabel('Sweepcases')
    ax4.set_ylabel('Prop load stress')
    ax4.grid(True)
    ax4.plot(Steg,maxSherSpen,'gx')

    plt.tight_layout()
    fig.savefig('D:/graph'+str(int(Samples*nf))+'.png')
plt.show()



    



