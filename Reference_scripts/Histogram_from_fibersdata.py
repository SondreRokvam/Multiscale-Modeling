import matplotlib.pyplot as plt
import numpy as np

def lese(FilePath):
    data = list()   #Same hvilken

    g = open(FilePath, "r") #r for read, w for write og a for append

    tekst = g.read()
    g.close()

    lines = tekst.split('\n')
    for line in lines:
        print(line)
        dataer = line     #for hvert ledd du har med.

        data.append(dataer)         #legger dataene inn i liste
    print(len(data))
    return data
FilePath =r"C:/Multiscale-Modeling/FiberRadiuser.txt"

rads =lese(FilePath)
plt.hist(rads, bins=np.arange(21), density=True)  # arguments are passed to np.histogram
plt.title("Histogram with 100 bins")
plt.show()