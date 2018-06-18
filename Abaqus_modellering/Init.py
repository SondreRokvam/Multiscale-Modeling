Iterations = 0

# Globale Directories
GitHub, workpath = 'C:/MultiScaleMethod/Github/Multiscale-Modeling/', 'C:/Temp/'
Tekstfiler, Modellering, processering = 'C:/MultiScaleMethod/Github/textfiles/', GitHub + 'Abaqus_modellering/', GitHub + 'Abaqus_prosessering/'


Yeah = np.genfromtxt(GitHub + 'Sweeps.txt')

# Hvilken parameter sweepes

#   Meshsize/ Fiberresolution
#   Interface element thickness
#   RVE size from nf
#   Critical RVE convergence test
#   Klareringsavstand



nf = 10
Vf = 0.6
scsc = 9973  # A prime for good measure


# Open for big scale iterations
execfile(Modellering + 'IterationParameters.py')  # Sette iterasjonsnummer
if Iterations:
    Itra = open(Tekstfiler + 'Iterasjoner.txt', "a")
    Itra.write('\n')
    Itra.close()
    Iterasjonfiks()

print'Iterasjon : ', ItraPara  # Antall itersjoner saa langt
