# -*- coding: utf-8 -*-
"""
Plot failure envelopes and stress envelopes
"""

import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter

def Get_sweeps():
    g = open(Envelope, "r")
    print(Envelope)
    tekst =g.read()
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

def inverted(thing):
    Yield =1
    for b in range(0,len(thing)):
        thing[b] =Yield/thing[b]
    return thing

"""%%%%%%%%%%%%%%%%%%%%%%%"""
"""      Funksjoner       """
GitHub = 'C:/Multiscale-Modeling/'
nf=1
all_plots=1
one_plots=0

#Lag plot for følgende:
Sample=[0,5, 10, 25,50]
for Samples in Sample:
    #Spenninger 12
    maxMisesStresses = list()       #0
    minMisesStresses = list()       #1
    maxPrinceStresses = list()      #2
    midPrinceStresses = list()      #3

    minPrinceStresses = list()      #4
    maxTresca = list()              #5
    minTresca = list()              #6
    maxPress = list()               #7

    minPress = list()               #8
    maxINV3 = list()                #9
    minINV3  = list()               #10
    maxSherstresses = list()        #11

    #Toyinger 4
    maxPrinceToyinger = list()      #0
    midPrinceToyinger = list()      #1
    minPrinceToyinger = list()      #2
    maxSherToyinger = list()        #3

    Spenninger=[maxMisesStresses,minMisesStresses, maxPrinceStresses,midPrinceStresses,
                minPrinceStresses,maxTresca,minTresca,maxPress,
                minPress,maxINV3,minINV3,maxSherstresses]
    Toyinger = [maxPrinceToyinger,midPrinceToyinger,minPrinceToyinger,maxSherToyinger]

    Envelope = GitHub + 'envelope'+str(int(nf*Samples))+'.txt'
    SweepCases = Get_sweeps()
    for line in SweepCases:
        data = line.split('\t')
        for f in range(0, len(Spenninger)):
            Spenninger[f].append(float(data[f]))
        for g in range(0,len(Toyinger)):
            Toyinger[g].append(float(data[len(Spenninger)+g]))


    plotinfo =     [['max Mises Stresses',          inverted(Spenninger[0])],
                    ['min Mises Stresses',          inverted(Spenninger[1])],
                    ['max Principal Stresses',      inverted(Spenninger[2])],
                    ['mid Principal Stresses',      inverted(Spenninger[3])],

                    ['min Principal Stresses',      inverted(Spenninger[4])],
                    ['max Tresca Stresses',         inverted(Spenninger[5])],
                    ['min Tresca Stresses',         inverted(Spenninger[6])],
                    ['max Press Stresses',          inverted(Spenninger[7])],

                    ['min Press Stresses',          inverted(Spenninger[8])],
                    ['max INV3 Stresses',           inverted(Spenninger[9])],
                    ['min INV3 Stresses',           inverted(Spenninger[10])],
                    ['max Shear Stresses',          inverted(Spenninger[11])],

                    ['max Principal Strains',      inverted(Toyinger[0])],
                    ['mid Principal Strains',      inverted(Toyinger[1])],
                    ['min Principal Strains',      inverted(Toyinger[2])],
                    ['max Shear Strains',          inverted(Toyinger[3])]]

    straight_plotaxe = ['R', 'Stress sweep angle']
    angular_plotaxe = ['σ2 (y)', 'σ3 (x)']

    Scale = 10 / 9                                          # Graf zoom out
    phi = (1 / (len(Spenninger[0])-1)) * 2 * math.pi             # Angular stepsize
    Steg = np.arange(0, 2 * math.pi+phi, phi)               # Antall datapunkter


    if all_plots:
        fig, axes = plt.subplots(nrows=4, ncols=8,figsize=(30,18))
        axes_list = [item for sublist in axes for item in sublist]

        for plot in plotinfo:
            name = plot[0]
            R = plot[1]
            x, y = to_xy(R)
            my1 = max(max(max(y), abs(min(y))),max(max(x), abs(min(x)))) * Scale
            mx1 = my1
            my2 = max(max(R), abs(min(R))) *Scale
            sx = axes_list.pop(0)
            lx = axes_list.pop(0)
            sx.set_title(name+' Angular')
            lx.set_title(name+' Linear')
            sx.set_xlim(-mx1, mx1)
            lx.set_xlim(0, 2 * math.pi)
            sx.set_ylim(-my1, my1)
            lx.set_ylim(-my2, my2)
            sx.set_xticks(np.arange(-mx1, mx1, mx1 / 5))
            lx.set_xticks(np.arange(0, 2 * math.pi, 2*math.pi/16))
            sx.set_yticks(np.arange(-my1, my1, my1 / 5))
            lx.set_yticks(np.arange(-my2, my2, my2 / 5))
            sx.set_xlabel(angular_plotaxe[0])
            lx.set_xlabel(straight_plotaxe[0])
            sx.set_ylabel(angular_plotaxe[1])
            lx.set_ylabel(straight_plotaxe[1])
            sx.grid(True)
            lx.grid(True)
            sx.plot(x, y, 'b--',0.0,0.0,'kx')
            lx.plot(Steg, plot[1], 'ro')

        for ax in axes_list:
            ax.remove()
        plt.subplots_adjust(hspace=0.5)
        plt.tight_layout()
        fig.savefig(GitHub+'graphs/'+'allgraphs'+str(int(Samples*nf))+'.png')

    if one_plots:
        for bob in range(0,len(plotinfo)):
            fig, (sx,lx) = plt.subplots(nrows=1, ncols=2,figsize=(21,14))
            plot=plotinfo[bob]
            name = plot[0]
            R = plot[1]
            x, y = to_xy(R)
            my1 = max(max(max(y), abs(min(y))),max(max(x), abs(min(x)))) * Scale
            mx1 = my1
            my2 = max(max(R), abs(min(R))) *Scale
            sx.set_title(name+' Angular')
            lx.set_title(name+' Linear')
            sx.set_xlim(-mx1, mx1)
            lx.set_xlim(0, 2 * math.pi)
            sx.set_ylim(-my1, my1)
            lx.set_ylim(-my2, my2)
            sx.set_xticks(np.arange(-mx1, mx1, mx1 / 5))
            lx.set_xticks(np.arange(0, 2 * math.pi, 2*math.pi/16))
            sx.set_yticks(np.arange(-my1, my1, my1 / 5))
            lx.set_yticks(np.arange(-my2, my2, my2 / 5))
            sx.set_xlabel(angular_plotaxe[0])
            lx.set_xlabel(straight_plotaxe[0])
            sx.set_ylabel(angular_plotaxe[1])
            lx.set_ylabel(straight_plotaxe[1])
            sx.grid(True)
            lx.grid(True)
            sx.plot(x, y, 'b--',0.0,0.0,'kx')
            lx.plot(Steg, plot[1], 'ro')

            plt.subplots_adjust(hspace=0.5)
            plt.tight_layout()
            fig.savefig(GitHub+'graphs/'+name+str(int(Samples*nf))+'.png')
            plt.close(fig)




    




