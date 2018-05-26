import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import PatchCollection

def henteParametere():
    a=1
    f = open(parameterpath, 'r')
    tekst = f.read()
    data = tekst.split('\t')
    f.close()
    dL,r,nf,Vf,wiggle,sweepcases = float(data[0]),float(data[1]),float(data[2]),float(data[3]),float(data[4]),float(data[5])
    if nf == 0 or Vf == 0:
        a=0
    return a,dL,r

def hentePopulation():
    #Les fiber matrix populasjon
    xy=list()
    f = open(coordpath,'r')
    tekst = f.read()
    f.close()
    lines = tekst.split('\n')
        #lagre koordinater til stottefil
    for line in lines:
        data = line.split('\t')
        a = float(data[0])
        b = float(data[1])
        xy.append([a,b])
    return xy

def saveplot():
    fig, sx = plt.subplots(figsize=(5,5))
    plt.axis([-dL / 2, dL / 2, -dL / 2, dL / 2])  # faa en kvadratisk plot
    sx.set_title('Fiberpopulasjon')
    sx.set_xticks(np.arange(-dL / 2, dL / 2, dL/10))
    sx.set_yticks(np.arange(-dL / 2, dL / 2, dL/10))
    sx.grid(True)
    plt.tight_layout()
    if a:
        fiberlist = list()
        for i in range(0, len(coord)):
            # plt.scatter(coord[i][0],coord[i][1], s=pi*(r*10)**2)
            circle = plt.Circle((coord[i][0], coord[i][1]), r)
            fiberlist.append(circle)
        p = PatchCollection(fiberlist, alpha=0.8)
        sx.add_collection(p)

    fig.savefig('D:/graph.png')
    plt.show()

parameterpath = '‪C:/Multiscale-Modeling/Parametere.txt'
coordpath = 'C:/Multiscale-Modeling/coordst.txt'
a,dL,r= henteParametere()
if a:
    coord =hentePopulation()
saveplot()
