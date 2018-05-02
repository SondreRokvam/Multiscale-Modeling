from random import *
from math import *
import numpy as np
import os
from sets import Set
import multiprocessing
print'%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n', 'Multiscale Modelling, Microscale  \n',
def CreateNewRVEModel():
    # Creates RVE model and orphanmesh. Lage 2D RVE shell, meshe RVE, extrudere til 3D part, lage orphanmesh og sette cohesive elementtype paa Interface
    execfile(Modellering+'RVEsketching.py')             # Lage 2D RVE fra fiberpopulasjon data
    del mdb.models['Model-1']                           # Slett standard part model 1
    execfile(Modellering+'RVEmeshpart.py')              # Meshe 2D RVE  til 3D part, lage orphan mesh part
    p = mod.parts[meshPartName]
    execfile(Modellering+'RVEelementsets.py')           # Fiber, sizing og matrix elementer i set og Fiber center datums for material orientation
    execfile(Modellering + 'RVEproperties.py')          # Sett materialegenskaper for elementset
    execfile(Modellering + 'RVE_Assembly_RP_CE.py')     # Assembly med RVE med x i fiber retning. Lage constrain equations til RVE modell og fixe boundary condition for rigid body movement
    if not noFiber and Interface:                       # Rearrange fiber interface nodes for controlled elementthickness and stable simulations
        execfile(Modellering + 'RVE_InterfaceElementThickness.py')
    execfile(Modellering + 'RVE_Boundaryconditions.py') # Boundaryconditions mot rigid body movement

def run_Job(Jobb, modelName):
    mdb.Job(name=Jobb, model=modelName, description='', type=ANALYSIS,
            atTime=None, memory=90,
            memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True,
            explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF,
            modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='',
            scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=numCPU,
            numDomains=numCPU, numGPUs=1)
    if Runjobs:
        mdb.jobs[Jobb].submit(consistencyChecking=OFF)
        mdb.jobs[Jobb].waitForCompletion()
    else:
        mdb.jobs[Jobb].writeInput(consistencyChecking=OFF)
        qw = open(Jobsss, "a")
        qw.write('call "C:\SIMULIA\Abaqus\6.14-4\code\bin\abq6144.exe" job=' + Jobb + ' interactive cpus=' + str(numCPU))
        qw.close()

#Globale Directories
GitHub, workpath = 'C:/Multiscale-Modeling/', 'C:/Temp/'
Tekstfiler, Modellering,processering = GitHub+'textfiles/', GitHub+'Abaqus_modellering/',GitHub+'Abaqus_prosessering/'

#Globale Paths
Jobsss = workpath + 'Abaqusjobs.bat'

# Sette variabler
execfile(Modellering+'TestVariabler.py')            # Sette Test variabler
execfile(Modellering+'IterationParameters.py')      # Sette iterasjonsnummer

#INFO DUMP
if Interface and Createmodel and not noFibertest:
    print('Aspect ratio for Interface elementsn= ' + str(round(meshsize / (rinterface * rmean), 2)) +
          '\t Interface element thickness = ' + str(float(ElementInterfaceT * rmean)))
if not noFibertest and FiberSirkelResolution<20:
    print 'For grov opplosning, avslutter..'
    del error



        # Generelle instilliger

"""Iterasjonsprameter"""
#Meshsize/ Fiberresolution, Sweepe fiberresolution
#Interface element thickness, Sweepe nedover til crash, analysere data
#RVE size from nf       # Trenger minimum RVE convergence test
#Klareringsavstand, sweepe nedover til crash, analysere data
#ParameterSweep=np.round(np.linspace(2 ,80,79)) # nf sweep

ParameterSweep=[4]

nf = 50
Vf = 0.6  #
nf= int(ParameterSweep[ItraPara])

"""Sette Iterasjonsavhengige variabler"""

if nf == 0 or Vf == 0 or noFibertest:
    nf = 0
    Vf = 0
    dL = rmean * 5
    noFiber = 1
if not nf == 0:  # RVE dL er relativ av nf, rmean og V
    dL = ((nf * pi * rmean ** 2) / (Vf)) ** 0.5
    noFiber = 0

#Random modellering lokke
n = int(1)           #  Itererer med random nokkeler fra 0 til n
Q = int(0)
while Q<n:
    #IMPORTERER ALT FRA ABAQUS
    from abaqus import *
    from abaqusConstants import *
    from odbAccess import *
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior

    """ Datalagring """
    coordpath = Tekstfiler + 'RVEcoordinatsandRadiuses' +str(
        int(ParameterSweep[ItraPara])) + '_' + str( Q) + '.txt'        # Skriver ned generert fiberPop for reference.
    Lagrestiffpathprop = Tekstfiler + 'Stiffness__NF-' + str(
        int(nf)) + '.txt'                               # Skrives ned statistikk til ett annet script
    lagrestiffpathmod = Tekstfiler + 'StiffnessM.txt'      # Lagrer ned Stiffnessmatrix
    Envelope = Tekstfiler + 'envelope'                  # Parameteravhengig - Spesifikt navn i funksjonen
    Sigmapaths = Tekstfiler +'Sigmas'+str(
        int(ParameterSweep[ItraPara])) + '_' + str( Q) + '.txt'

    """Random variabler og iterasjonsnavn"""
    seed(Q)                                                         # Q er randomfunksjonensnokkelen
    wiggle = random() * rmean                                       # Omplasseringsgrenser for fiberomplassering
    RVEmodellpath = workpath + 'RVEmodel__Parameter-' + str(ParameterSweep[ItraPara]) + '__RandKey-' + str(Q)


    """ Abaqus RVE model """
    Mdb()  # reset Abaqus
    model = mdb.Model(name=modelName, modelType=STANDARD_EXPLICIT)  # Lage model
    mod = mdb.models[modelName]                                     # Lage snarvei
    if Createmodel:
        xydata = None                       # Fiber kordinater og radiuser
        if not noFiber:
            execfile(Modellering+'GenerereFiberPopTilFil.py')            # create a random population
        CreateNewRVEModel()
        if Savemodel:
            mdb.saveAs(pathName=RVEmodellpath)
    # Prov aa aapne tidligere modell
    if not Createmodel:
        try:
            openMdb(pathName=RVEmodellpath)
            mod = mdb.models['Model-A']
        except:
            print 'Cae not found'
            pass

    """Simulering, linear stivhetsmatrise og nonlinear unidirectional strain and stress cases"""
    # Navn til lineare tester
    Enhetstoyinger = [''] * 6  # Enhetstoyinger for lineare retninger
    for g in range(0, 6):  # 6 Enhetstoyinger - Exx, Eyy, Ezz, Exy, Exz, Eyz
        if not noFibertest:
            Enhetstoyinger[g] = [Retning[g] + str(int(ParameterSweep[ItraPara])) + '_' + str(Q)]
        else:
            Enhetstoyinger[g] = [Retning[g] + 'noFiber']
    #Kjore Linear analyse
    if linearAnalysis:  # LinearAnalysis for stiffness and small deformation
        try:
            execfile(Modellering +'LinearAnalysis.py')
        except:
            n=n+1
            nonLinearAnalysis=0
        try:
            Mdb()
            openMdb(pathName=RVEmodellpath)
            mod = mdb.models['Model-A']
        except:
                print 'Cae cannot be opened'
                del errors
                # pass
        execfile(processering + 'LinearPostprocessing.py')
    else:
        f = open(lagrestiffpathmod, 'r')
        SM = f.read()
        rows = SM.split('\t\t')
        Stiffmatrix = []
        count = 0
        for row in rows:
            Col = []
            Colll = row.split('\t')
            for dip in range(0, len(Colll)):
                if not (dip==0 and count==0):
                    Col.append(float(Colll[dip]))
            count =  1
            Stiffmatrix.append(Col)
        for a in range(0, 6):
            print '%7f \t %7f \t %7f \t %7f \t %7f \t %7f' % (
            Stiffmatrix[0][a], Stiffmatrix[1][a], Stiffmatrix[2][a], Stiffmatrix[3][a], Stiffmatrix[4][a],
            Stiffmatrix[5][a])

    if nonLinearAnalysis:                            # nonLinearAnalysis for strength and large deformation
        #Storrelses ordenen paa strains
        Magni = 2e-1
        #Mulige lastretninger STRAINS:  exx, eyy, ezz,  exy,  exz,  eyz
        Ret = 1
        strain = Magni*id[Ret]
        print '\n\nRef Strain ',strain
        # Faktisk STRAINS:  ex,  ey,  ex,   Yzy, -Yzx, -Yyx
        stresses = np.dot(Stiffmatrix, strain)
        print 'Ref Stresses ', stresses
        if strain[Ret]>0:
            Type='tension'
        else:
            Type='compression'
        Stresses = stresses[Ret]*id[Ret]
        print 'Applied Stresses ', Stresses
        #ez,ey,ex,Yzy,-Yzx,-Yyx                              sz,sy,sx,Tzy,Tzx,Tyx
        strains = np.dot(np.linalg.inv(Stiffmatrix),Stresses)

        cases = [[Retning[Ret]+Type+ str(ParameterSweep[ItraPara]) + '__Rand-' + str(Q), strains]]

        for Case in cases:
            Jobbnavn, Strain = Case
            execfile(Modellering + 'nonLinearAnalysis.py')

            """
            try:
                execfile(Modellering +'nonLinearAnalysis.py')
            except:
                pass
                n = n + 1
                    """

        execfile(processering + 'nonLinearPostprocessing.py')
    print 'Reached end of random key Iteration'
    Q = Q + 1
    del section, regionToolset, dgm, part, material, assembly, step, interaction
    del load, mesh, job, sketch, visualization, xyPlot, dgo, connectorBehavior

#Open for big scale iterations

"""
Itra = open(Tekstfiler+'Iterasjoner.txt', "a")
Itra.write('\n')
Itra.close()
"""