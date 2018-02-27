import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import PatchCollection
"Funksjoner"
def henteParametere():
    f = open(parameterpath+'.txt', 'r')
    tekst = f.read()
    lines =tekst.split('\n')
    data = lines[1].split('\t')
    f.close()
    dL,r,nf,Vf = float(data[9]),float(data[1]),float(data[2]),float(data[3])
    a = 1
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
        c = float(data[2])
        xy.append([a,b,c])
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
            circle = plt.Circle((coord[i][0], coord[i][1]), coord[i][2])
            fiberlist.append(circle)
        p = PatchCollection(fiberlist, alpha=0.8)
        sx.add_collection(p)
    fig.savefig('D:/RVEmodel.png')
    plt.show()

"""Variabler"""
GitHub = 'C:/Multiscale-Modeling/'
parameterpath = GitHub+'Parametere'
coordpath = GitHub+'coordst.txt'
a,dL,r= henteParametere()
if a:
    coord =hentePopulation()
    print(coord)
saveplot()
