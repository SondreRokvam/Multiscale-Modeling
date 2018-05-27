"""Test preperation for iteration"""

#Siden scriptet maa restarte abaqus saa mellomlagres informasjon om iterasjoner i en ekstern fil
#Denne filen resetter iterasjonstelleren og skriver et nullstilt iterasjonsscript.

#Globale Directories
GitHub = 'C:/MultiScaleMethod/Github/Multiscale-Modeling/'
workpath = 'C:/Temp/'

Tekstfiler = 'C:/MultiScaleMethod/Github/textfiles/'
Modellering = GitHub+'Abaqus_modellering/'


#Nullsette iterasjoner marker
Itra = open(Tekstfiler+'Iterasjoner.txt', "w")
Itra.close()


#Nullsette jobber
JOBO = open(workpath + 'Abaqusjobs.bat', "w")
JOBO.close()


#Lese antall itersjoner
Itra = open(Tekstfiler+'Iterasjoner.txt', "r")
Content = Itra.read()
colsa =Content.split('\n')
number = len(colsa)-1


print(number)
#Lage pythonscript som setter iterasjonsparameter lik antall iterasjoner == 0
InterestingParameter = 'ItraPara'
Itra = open(Modellering+'IterationParameters.py', "w")
Itra.write('global '+InterestingParameter+'\n' + InterestingParameter+' = '+str(int(number)))
Itra.close()