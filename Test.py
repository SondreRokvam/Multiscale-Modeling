xy = list()
name = 'c:/Multiscale-Modeling/textfiles/Stiffness__NF-2.txt'
f = open(name,'r')
tekst = f.read()
f.close()
lines = tekst.split('\n')
"""for line in lines:
    data = line.split('\t')
    a = float(data[0])  # X
    b = float(data[1])  # Y
    c = float(data[2])  # R
    xy.append([a, b, c])  # lagre til liste"""
print(len(lines))#'Antall fiber = ', int(nf), '\tAntall fiberkoordinater = ' + str(len(xy))
