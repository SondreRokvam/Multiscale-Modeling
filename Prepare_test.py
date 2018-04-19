"""Test preperation for iteration"""
#Directories
GitHub, workpath = 'C:/Multiscale-Modeling/', 'C:/Temp/'
Tekstfiler, Modellering = GitHub+'textfiles/', GitHub+'Abaqus_modellering/'

#Nullsette iterasjoner
Itra = open(Tekstfiler+'Iterasjoner.txt', "w")
Itra.close()

#Nullsette jobber
JOBO = open(workpath + 'Abaqusjobs.bat', "w")
JOBO.close()

#Lese antall itersjoner
Itra = open(Tekstfiler+'Iterasjoner.txt', "r")
Content = Itra.read()
Content.split('\n')
number = len(Content)

#Lage pythonscript som setter iterasjonsparameter lik antall iterasjoner
InterestingParameter = 'ItraPara'
Itra = open(Modellering+'IterationParameters.py', "w")
Itra.write('global '+InterestingParameter+'\n' + InterestingParameter+' = '+str(int(number)))
Itra.close()