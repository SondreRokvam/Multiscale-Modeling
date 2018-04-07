from math import *
from random import *
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
import numpy as np
import os


# Beskrivende variabler. Disse kan tweakes paa.
seed(1)
Vf = 0.6
nf = 50
r = 1.0
rtol = 0.025 * r
gtol = r * 0.1
dL = ((nf * pi * r ** 2) / (Vf)) ** 0.5


#Finne størrelse av utsnitt fra beskrivende variabler
dL = ((nf * pi * r ** 2) / (Vf)) ** 0.5

# Liste over fiberkoordinater
coord = list()
# Filplassering til progresjonsgrafer
path = 'C:/Users/Rockv/Desktop/pyBilder'

#Parametere for kantdodzone
ytrekantgrense = (dL / 2) - r + gtol
indrekantgrense = (dL / 2) - r - gtol
#Parametere for hjornedodzone
ytrehjornegrense = r+gtol
indrehjornegrense= r-gtol

#Random forflyttningvariabel
wiggle = 0.5*r

#Klarere filplassering for progresjonsgrafer
try:
    fileList = os.listdir(path)
except OSError:
    pass
try:
    for fileName in fileList:
        try:
            os.remove(path+"/"+fileName)
        except OSError:
            break
        fileList = os.listdir(path)
except OSError:
    pass
try:
    os.mkdir(path)
except OSError:
    pass


# liste for aa lagre fremgang paa iterasjonene i  prosessen
books = list()  # keeping records of progress
bildecount = list() # keeping records of  graphs
iterasjonsgrense = 7500  # maks antall omplasseringsforsok

# Hovedfunksjon, #utplasserer fibere
def modelleresnitt():
    flag = 0
    fVfforrige = 0
    nplassert = 0.0  # antall fiber plassert
    nkrasj = 0  # antall krasj
    sidepunkt = 0
    hjornepunkt = 0
    senterpunkt = 0
    dodpunkt = 0
    print("dL =", round(dL, 1), "x,y =", round(dL / 2, 1))  # print storrelse og max x,y
    while nplassert< nf:
        frem = countsjikt() / nf  # Forlopig fremdrift
        fvf = frem*Vf

        # Sjekke om loopen har stoppet nok ganger til at fibere skal shake up
        if nkrasj > iterasjonsgrense:
             # reset krasj for nytt forsok paa utplasseringen.
            saveplot()
            if fVfforrige == fvf:
                flag = flag + 1
            if flag>10:
                flag=0
                print( 'Punktene random forflyttes. npp:', nplassert, 'fnnp:', countsjikt(), 'Vf:', round(fvf,3), ' av tot Vf:', Vf, 'tries:', len( books), 'krasjes:', nkrasj)
                shakeitOOUP()
                shakeitOOUP()
            else:
                print('Punktene random forflyttes ned. npp:', nplassert, 'fnnp:', countsjikt(),'Vf:', round(fvf,3), ' av tot Vf:', Vf, 'tries:', len(books), 'krasjes:', nkrasj,'# fremdrift stanget:',flag)
                shakeitdown()# kjor shake it up
            fVfforrige = fvf
            saveplot()
            nkrasj = 0

        #genererer fiberkoordinater til ny fiber
        x = dL * random() - dL * 0.5
        y = dL * random() - dL * 0.5
        # sjekker krasj med andre fiber og hjorne dodzone
        if not krasj(x, y) and (sqrt((abs(x)-dL/2)**2 + (abs(x)-dL/2)**2)<ytrehjornegrense or sqrt((abs(x)-dL/2)**2 + (abs(x)-dL/2)**2)>indrehjornegrense):
            # Er koordinatet i hjornet? Krasjer det med punkt i et annet hjorne?
            if abs(x) > ytrekantgrense and abs(y) > ytrekantgrense:

                if cornerp(x, y):
                    print( "hjoernepunkt")
                    hjornepunkt = hjornepunkt + 1
                    nplassert = nplassert + 1
                    print( "fiber +1", "nnp:", nplassert, 'fnnf:', countsjikt(), round(fvf,3), ' av Vf:', Vf, 'tries:', len(books), 'krasjes:', nkrasj)
                    flag = 0
                else:
                    nkrasj = nkrasj + 1


            # Kan koordinatet vere et sidepunkt? Krasjer det med punkter paa motsatt side?
            elif abs(x) > ytrekantgrense or abs(y) > ytrekantgrense:

                if kantp(x, y):
                    print("sidepunkt")
                    nplassert = nplassert + 1
                    print ("fiber +1", "nfiber:", nplassert, 'faktisk:', countsjikt(), round(fvf,3), ' av Vf:', Vf, 'tries:', len(books), 'krasjes:', nkrasj)
                    flag = 0
                    sidepunkt = sidepunkt + 1
                else:
                    nkrasj = nkrasj + 1

            # Er koordinatet i "dodsonen" og derfor ubrukelig?
            elif indrekantgrense < abs(x) or indrekantgrense < abs(y):
                print ("dodzonepunkt")
                dodpunkt = dodpunkt + 1
                nkrasj = nkrasj + 1

                """senterpunkt"""  # Ellers er det i midten!
            else:
                print ("senterpunkt")
                coord.append([x, y])
                senterpunkt = senterpunkt + 1
                nplassert = nplassert + 1
                print("fiber +1", "nfiber:", nplassert, 'faktisk:', countsjikt(), round(fvf,3), ' av Vf:', Vf, 'tries:', len(books), 'krasjes:', nkrasj)
                flag=0
        else:
            nkrasj = nkrasj + 1
        books.append(nplassert)  # keeping record of amount of tries
    i_sjikt = countsjikt()
    print (i_sjikt, 'tot i crosssection Vf:', round(i_sjikt * Vf / nf, 3), 'av', Vf, senterpunkt, 'i senter', sidepunkt,
           'i sider', hjornepunkt, 'i hjorner og', dodpunkt, "dodsonepunkter", 'antall krasj:', nkrasj)
    g = open('D:/coordst.txt', "w")
    for l in range(0, len(coord)):
        g.write(str(coord[l][0]) + '\t' + str(coord[l][1]))
        if l < (len(coord)-1):
            g.write('\n')
    g.close()


def countsjikt():
    i_sjikt = 0.0
    for i in range(len(coord)):
        if abs(coord[i][0]) <= dL / 2 and abs(coord[i][1]) <= dL / 2:
            i_sjikt = i_sjikt + 1.0
    return i_sjikt


# funksjon for aa speile over hjoerner
def cornerp(x, y):
    if x < 0 and y < 0 and not krasj(x, y) and not krasj(x + dL, y) and not krasj(x, y + dL) and not krasj(x + dL,
                                                                                                           y + dL):
        coord.append([x, y])
        coord.append([x + dL, y])
        coord.append([x, y + dL])
        coord.append([x + dL, y + dL])
        print ("ned, ven")
        return True
    elif x >= 0 and y < 0 and not krasj(x, y) and not krasj(x - dL, y) and not krasj(x, y + dL) and not krasj(x - dL,
                                                                                                              y + dL):
        coord.append([x, y])
        coord.append([x - dL, y])
        coord.append([x, y + dL])
        coord.append([x - dL, y + dL])
        print ("ned, hoy")
        return True
    elif x < 0 and y >= 0 and not krasj(x, y) and not krasj(x + dL, y) and not krasj(x, y - dL) and not krasj(x + dL,
                                                                                                              y - dL):
        coord.append((x, y))
        coord.append((x + dL, y))
        coord.append((x, y - dL))
        coord.append((x + dL, y - dL))
        print ("opp, ven")
        return True
    elif x >= 0 and y >= 0 and not krasj(x, y) and not krasj(x - dL, y) and not krasj(x, y - dL) and not krasj(x - dL,
                                                                                                               y - dL):
        coord.append([x, y])
        coord.append([x - dL, y])
        coord.append([x, y - dL])
        coord.append([x - dL, y - dL])
        print ("opp, hoy")
        return True
    else:
        return False


# funksjon for speile over sider
def kantp(x, y):
    if x > ytrekantgrense and x >= 0 and not krasj(x, y) and not krasj(x - dL, y):
        coord.append([x, y])
        coord.append([x - dL, y])
        print ("hoyreside punkt")
        return True

    elif x < -ytrekantgrense and x < 0 and not krasj(x, y) and not krasj(x + dL, y):
        coord.append([x, y])
        coord.append([x + dL, y])
        print ("venstreside punkt")
        return True

    elif y > ytrekantgrense and y >= 0 and not krasj(x, y) and not krasj(x, y - dL):
        coord.append([x, y])
        coord.append([x, y - dL])
        print ("topp punkt")
        return True

    elif y < -ytrekantgrense and y < 0 and not krasj(x, y) and not krasj(x, y + dL):
        coord.append([x, y])
        coord.append([x, y + dL])
        print ("bunn punkt")
        return True
    else:
        return False


# Funksjon som sjekker krasj
def krasj(x, y):
    for c in coord:
        xp, yp = c[0], c[1]
        if sqrt((x - xp) ** 2 + (y - yp) ** 2) < 2 * (r + rtol):
            return True

    return False


def lagplot():

    fig, ax = plt.subplots()
    plt.axis([-dL / 2, dL / 2, -dL / 2, dL / 2])  # faa en kvadratisk plot
    fiberlist = list()
    for i in range(0, len(coord)):
        # plt.scatter(coord[i][0],coord[i][1], s=pi*(r*10)**2)
        circle = plt.Circle((coord[i][0], coord[i][1]), r)
        fiberlist.append(circle)

    p = PatchCollection(fiberlist, alpha=0.8)
    ax.add_collection(p)

    return plt.show()


def saveplot():
    bildecount.append(1)
    fig, sx = plt.subplots()
    plt.axis([-dL / 2, dL / 2, -dL / 2, dL / 2])  # faa en kvadratisk plot
    fiberlist = list()
    for i in range(0, len(coord)):
        # plt.scatter(coord[i][0],coord[i][1], s=pi*(r*10)**2)
        circle = plt.Circle((coord[i][0], coord[i][1]), r)
        fiberlist.append(circle)
    p = PatchCollection(fiberlist, alpha=0.8)
    sx.add_collection(p)
    print( 'graph added', str(len(bildecount)))
    fig.savefig(path+'/graph'+str(len(bildecount))+'.png')
    plt.close('all')




def shakeitdown():
    for k in range(0,20):
        t = 0
        for c in coord:
            i = list()
            i.append([dL * 2, dL * 2])
            x, y = c[0], c[1]
            if indrekantgrense > abs(x) and indrekantgrense > abs(y):
                coord[t] = i[0]
                for j in range(0, 100):
                    xp, yp = [x + wiggle * random() - wiggle * 0.5, y + wiggle * random() - wiggle * 0.65]
                    if not krasj(xp,yp) and indrekantgrense > abs(xp) and indrekantgrense > abs(yp):
                        coord[t] = [xp,yp]
                        break
                    coord[t] = [x,y]
            t = t +1

def shakeitOOUP():
    for k in range(0,len(coord)):
        t = 0
        for c in coord:
            i = list()
            i.append([dL * 2, dL * 2])
            x, y = c[0], c[1]
            if indrekantgrense > abs(x) and indrekantgrense > abs(y):
                coord[t] = i[0]
                for j in range(0, 100):
                    xp, yp = [x + wiggle * random() - wiggle * 0.5, y  + wiggle * random()- wiggle *0.5]
                    if not krasj(xp,yp) and indrekantgrense > abs(xp) and indrekantgrense > abs(yp):
                        coord[t] = [xp,yp]
                        break
                    coord[t] = [x,y]
            t = t +1





"""HOVEDKODE"""

modelleresnitt()
print('lag plot')
lagplot()
saveplot()
# Lage plot
