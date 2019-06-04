
# Globale Directories
multiMod, workpath = GitHub+'Multiscale-Modeling/', 'C:/Temp/'
Tekstfiler, Modellering, processering = GitHub+'textfiles/',multiMod+'Abaqus_modellering/', multiMod+'/Abaqus_prosessering/'

#RVE parametere
nf = 1
Vf = 0.2

#Iterasjon parametere
Iterations = 0
SweepParametere = np.genfromtxt(multiMod + 'Sweeps.txt')
SweepPrime = 9973  # A prime for good measure




# Hvilken parameter sweepes

#   Meshsize/ Fiberresolution
#   Interface element thickness
#   RVE size from nf
#   Critical RVE convergence test
#   Klareringsavstand


# Open for big scale iterations
execfile(Modellering + 'IterationParameters.py')  # Sette iterasjonsnummer
if Iterations:
    Itra = open(Tekstfiler + 'Iterasjoner.txt', "a")
    Itra.write('\n')
    Itra.close()
    Iterasjonfiks()

print 'Iterasjon : ', ItraPara  # Antall itersjoner saa langt
