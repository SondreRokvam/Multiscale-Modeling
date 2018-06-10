Iterations = 1
# Globale Directories
GitHub, workpath = 'C:/MultiScaleMethod/Github/Multiscale-Modeling/', 'C:/Temp/Vf/'
Tekstfiler, Modellering, processering = 'C:/MultiScaleMethod/Github/textfiles/', GitHub + 'Abaqus_modellering/', GitHub + 'Abaqus_prosessering/'

# Open for big scale iterations
execfile(Modellering + 'IterationParameters.py')  # Sette iterasjonsnummer
if Iterations:
    Itra = open(Tekstfiler + 'Iterasjoner.txt', "a")
    Itra.write('\n')
    Itra.close()
    Iterasjonfiks()
