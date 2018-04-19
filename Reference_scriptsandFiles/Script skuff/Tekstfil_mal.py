def lese(FilePath):
    data = list()   #Same hvilken

    g = open(FilePath, "r") #r for read, w for write og a for append

    tekst = g.read()
    g.close()

    lines = tekst.split('\n')
    for line in lines:
        dataer = float[line[0]]
        dataer = float[line[0]]     #for hvert ledd du har med.

        data.append(dataer)         #legger dataene inn i liste
    return data

info =lese(FilePath)