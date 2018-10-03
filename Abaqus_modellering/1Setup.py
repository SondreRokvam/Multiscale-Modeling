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


"""    RVEmodel variabler                                      """
global noFibertest,Fibervariation,rmean,Rstdiv,Interface,rinterface,ElementInterfaceT,id, Retning

noFibertest = 0                                     # ON/OFF Fiber i modellen.
Fibervariation = 1                                  # ON/OFF variasjon fiberradius. Mean and standard div. Kan paavirke Vf i endelig model.

rmean = 8.7096                              # Gjennomsnittradius pa fiber
Rstdiv = 0.6374                             # OStandard avvik fra gjennomsnittsradius

Interface = 1                                   # ON/OFF CohesiveInterface
rinterface = 0.001                              # Interfacetykkelse ved modellering. Verdi er relativ til radius.    0.01 = 1%
ElementInterfaceT = 0                  # Interfacetykkelse paa elementene.  Verdi er relativ til radius.

id   =   np.identity(6)          # Identity matrix. Good for normalised load cases.'Exx','Eyy','Ezz','Exy','Exz','Eyz'
Retning =    ['Exx', 'Eyy', 'Ezz', 'Exy', 'Exz', 'Eyz']


def Iterasjonfiks():
    Itrasjoner = open(Tekstfiler + 'Iterasjoner.txt', "r")
    Content = Itrasjoner.read()
    Itrasjoner.close()
    rows = Content.split('\n')
    number = len(rows) - 1      # 0 is read as 1
    InterestingParameter = 'ItraPara'
    Itra_fil = open(Modellering + 'IterationParameters.py', "w")
    Itra_fil.write('global ' + InterestingParameter + '\n' + InterestingParameter + ' = ' + str(int(number)))
    Itra_fil.close()

# Open for big scale iterations
Iterations = 0

execfile(Modellering + 'IterationParameters.py')    # Sette iterasjonsnummer
if Iterations:
    Itra = open(Tekstfiler + 'Iterasjoner.txt', "a")
    Itra.write('\n')
    Itra.close()
    Iterasjonfiks()
    print 'Iterasjon : ', ItraPara                      # Antall itersjoner saa langt

