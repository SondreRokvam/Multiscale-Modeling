import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import PatchCollection


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
        r = float(data[2])
        xy.append([a,b,r])
    return xy

def saveplot():
    fig, sx = plt.subplots(figsize=(5,5))
    plt.axis([-dL / 2, dL / 2, -dL / 2, dL / 2])  # faa en kvadratisk plot
    sx.set_title('Fiberpopulasjon')
    sx.set_xticks(np.arange(-dL / 2, dL / 2, dL/10))
    sx.set_yticks(np.arange(-dL / 2, dL / 2, dL/10))
    #sx.grid(True)
    plt.tight_layout()
    fiberlist = list()
    for i in range(0, len(coord)):
        # plt.scatter(coord[i][0],coord[i][1], s=pi*(r*10)**2)
        circle = plt.Circle((coord[i][0], coord[i][1]), coord[i][2])
        fiberlist.append(circle)
        p = PatchCollection(fiberlist, alpha=0.8)
        sx.add_collection(p)

    fig.savefig('D:/graph.png')
    plt.show()

coordpath = 'C:/MultiScaleMethod/Github/textfiles/RVEcoordinatsandRadiuses70_0.txt'
coord =hentePopulation()
dL = ((70 * 3.14 * 8.3 ** 2) / (0.6)) ** 0.5
saveplot()
