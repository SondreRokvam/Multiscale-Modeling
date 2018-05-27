from random import *
from math import *
import numpy as np
import os
from sets import Set
import multiprocessing
import time
start_time = time.time()
print'\n\n>>>\tMultiscale Modelling, Microscale\n',
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
        try:
            mdb.jobs[Jobb].submit(consistencyChecking=OFF)
            mdb.jobs[Jobb].waitForCompletion()
        except:
            pass
    else:
        mdb.jobs[Jobb].writeInput(consistencyChecking=OFF)
        qw = open(Jobsss, "a")
        qw.write('call "C:\SIMULIA\Abaqus\6.14-4\code\bin\abq6144.exe" job=' + Jobb + ' interactive cpus=' + str(numCPU))
        qw.close()
def Iterasjonfiks():
    global Jobsss
    Jobsss = workpath + 'Abaqusjobs.bat'
    Itra = open(Tekstfiler + 'Iterasjoner.txt', "r")
    Content = Itra.read()
    cals = Content.split('\n')
    number = len(cals) - 1
    Itra.close()
    InterestingParameter = 'ItraPara'
    Itra = open(Modellering + 'IterationParameters.py', "w")
    Itra.write('global ' + InterestingParameter + '\n' + InterestingParameter + ' = ' + str(int(number)))
    Itra.close()
def FrameFinder():
    StressSigs = np.genfromtxt(Sigmapaths)
    StressSigs = StressSigs[1:, 1:]
    for a in range(0, 6):
        if not a == Ret:
            StressSigs[1:, a] = np.multiply(StressSigs[1:, a], 1 / StressSigs[1:, Ret])
    Sing = [0]*6
    for kj in range(0,len(StressSigs)):
        for sa in range(0,len(StressSigs[0])):
            if not sa==Ret:
                if not Sing[sa]:
                    if abs(StressSigs[kj][sa]) > 10e-2:
                        Sing[sa]=1
                else:
                    if abs(StressSigs[kj][sa]) > 10e-2:
                        return kj-2,sa,StressSigs[kj-2]
                    else:
                        Sing[sa]=0
    return len(StressSigs)-1, False, StressSigs[len(StressSigs)-1]


"""Intierings"""
if True:
    #Globale Directories
    GitHub, workpath = 'C:/MultiScaleMethod/Github/', 'C:/Temp/'
    Tekstfiler, Modellering,processering = GitHub+'textfiles/', GitHub+'Abaqus_modellering/',GitHub+'Abaqus_prosessering/'


    """Start"""
    #Sette variabler
    execfile(Modellering+'TestVariabler.py')            # Sette Test variabler
    Iterasjonfiks()
    execfile(Modellering+'IterationParameters.py')      # Sette iterasjonsnummer


    print 'Iterasjon : ',ItraPara      #Antall itersjoner saa langt

    #INFO DUMP
    if Interface and Createmodel and not noFibertest:
        print('Aspect ratio for Interface elementsn= ' + str(round(meshsize / (rinterface * rmean), 2)) +
              '\t Interface element thickness = ' + str(float(ElementInterfaceT * rmean)))
    if not noFibertest and FiberSirkelResolution<20:
        print 'For grov opplosning, avslutter..'
        del error

"""Iterasjonsprameter"""
#Meshsize/ Fiberresolution, Sweepe fiberresolution
#Interface element thickness, Sweepe nedover til crash, analysere data
#RVE size from nf       # Trenger minimum RVE convergence test
#Klareringsavstand, sweepe nedover til crash, analysere data
#ParameterSweep=np.round(np.linspace(2 ,80,79)) # nf sweep

ParameterSweep=[5]

nf = 8
Vf = 0.6  #
nf= int(ParameterSweep[ItraPara])

"""Sette Iterasjonsavhengige variabler"""
t=(time.time() - start_time)
print('t ved start=', t)

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
    #Datalagring
    seed(Q)  # Q er randomfunksjonensnokkelen
    execfile(Modellering + 'Set_text_dirs.py')

    if True:
        """ Abaqus RVE model """

        Mdb()  # reset Abaqus
        model = mdb.Model(name=modelName, modelType=STANDARD_EXPLICIT)  # Lage model
        mod = mdb.models[modelName]                                     # Lage snarvei
        if Createmodel :
            xydata = None                       # Fiber kordinater og radiuser
            if not noFiber:
                execfile(Modellering+'GenerereFiberPopTilFil.py')            # create a random population
            CreateNewRVEModel()
            if Savemodel:
                mdb.saveAs(pathName=RVEmodellpath)
        # Prov aa aapne tidligere modell
        if openModel:
            Mdb()
            openMdb(pathName=RVEmodellpath)
            mod = mdb.models[modelName]

        t = (time.time() - start_time)
        print('t etter lagd modell=', t)


        """Simuleringer"""

            # Lineare tester
        Enhetstoyinger = [''] * 6  # 6 Enhetstoyinger - Exx, Eyy, Ezz, Exy, Exz, Eyz
        for g in range(0, 6):
            if not noFibertest:
                Enhetstoyinger[g] = [Retning[g] + str(int(ParameterSweep[ItraPara])) + '_' + str(Q)]
            else:
                Enhetstoyinger[g] = [Retning[g] + 'noFiber']

            # Kjore Linear analyse
        if linearAnalysis:  # LinearAnalysis for stiffness and small deformation
            if not Createmodel:
                try:
                    openMdb(pathName=RVEmodellpath)
                    mod = mdb.models['Model-A']
                except:
                    print 'Cae not found'
                    pass
            try:
                execfile(Modellering +'LinearAnalysis.py')
            except:
                n=n+1
            t = (time.time() - start_time)
            print('t etter lin analyser=', t)
        if LinearpostPross:
            execfile(processering + 'LinearPostprocessing.py')
            t = (time.time() - start_time)
            print('t etter lin pross=', t)
        else:
            Stiffmatrix = np.load(lagrestiffpathmod)
            print '\nStiffnessmatrix:'
            for a in range(0, 6):
                print '%7f \t %7f \t %7f \t %7f \t %7f \t %7f' % (
                    Stiffmatrix[0][a], Stiffmatrix[1][a], Stiffmatrix[2][a], Stiffmatrix[3][a], Stiffmatrix[4][a],
                    Stiffmatrix[5][a])

            # Non linear tester
        Magni = 2e-2    # Skalarverdi til toyning
        Ret = 1         # Mulige lastretninger STRAINS:  exx, eyy, ezz,  exy,  exz,  eyz
        strain = Magni * id[Ret]

        print '\n\nReferanse Strain Vector ', strain
        stresses = np.dot(Stiffmatrix, strain)# :  ex,  ey,  ex,  Yzy, -Yzx, -Yyx
        print '\nStresses from RefSTRAINS', stresses
        Stresses = stresses[Ret] * id[Ret]
        print '\nReferanse Stress Vector', Stresses
        #print Stresses, Stiffmatrix
        strains = np.dot(np.linalg.inv(Stiffmatrix), Stresses)

        print '\nInitial Strain Vector', strains
        Type = 'comp_'
        if strains[Ret] > 0:
            Type = 'tens_'

        cases = [[Retning[Ret] + Type + str(ParameterSweep[ItraPara]) + '__Rand-' + str(Q), strains]]

        for Case in cases:
            Jobbnavn, Strain = Case
            if nonLinearAnalysis:
                if not Createmodel or linearAnalysis:
                    try:
                        openMdb(pathName=RVEmodellpath)
                        mod = mdb.models['Model-A']
                    except:
                        print 'Cae not found'
                        pass
                try:
                    execfile(Modellering +'nonLinearAnalysis.py')
                except:
                    print
                    n = n + 1
                t = (time.time() - start_time)
                print('t etter nonlin analyser=', t)
                if Savemodel:
                    mdb.saveAs(pathName=RVEmodellpath)

    Reset = 0       #For aa logge initielle strain stress
    stegy=difstpNm
    if nonLinearpostPross:
        print '\nPostProcess'
        execfile(processering + 'nonLinearPostprocessing.py')
        t = (time.time() - start_time)
        print('t ved ferdig postprosess=', t)



    strains2 = strains.tolist()
    Reset=1
    Jobbnav = Jobbnavn
    prev=0      #for aa vite hvor langt bak vi hoppet forrige gang
    Framecount =0
    reps = 6

    for asad in range(0,reps):
        print '\nfix:  ',asad
        Fram = FrameFinder()
        print Fram
        StressSigs = np.genfromtxt(Sigmapaths)
        StressSigs = StressSigs[1:, 1:]
        print StressSigs[Fram[0], :]
        print 'diff = ',(Fram[0] - prev)

        appe = 0
        if not (Fram[0] - prev)<=0:
            Framecount = Framecount+(Fram[0]- prev)
            if asad==0:
                prevname= difstpNm
            else:
                prevname = 'rep'+str(asad-1)
            ass = np.transpose(np.genfromtxt(Sigmapaths))
            ass = ass[:, 1:Framecount + 1]
            print 'plotpunkter   ', len(ass[0])
            print ass[0][-1]
            stegy ='rep'+str(asad)
            mod.StaticStep(name='rep'+str(asad), previous=prevname, nlgeom=ON, stabilizationMagnitude=0.0002, stabilizationMethod=DAMPING_FACTOR,
                           continueDampingFactors=False, adaptiveDampingRatio=0.05)
            steg = mod.steps['rep'+str(asad)]
            steg.setValues(maxNumInc=Increments['maxNum'], initialInc=ass[0][-1]-ass[0][-2],
                           minInc=Increments['min'],
                           maxInc=Increments['max'], convertSDI=CONVERT_SDI_OFF)
            steg.Restart(frequency=1, numberIntervals=0, overlay=OFF, timeMarks=OFF)
            mod.setValues(restartJob=Jobbnavn,
                          restartStep=prevname, restartIncrement=Fram[0])

            Jobbnavn = Jobbnav + str(asad)
            mdb.Job(name=Jobbnavn, model=modelName, description='', type=RESTART,
                    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90,
                    memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True,
                    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF,
                    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='',
                    scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1,
                    numGPUs=0)
            appe= 1
            prev = Fram[0]



        print '\n' + Jobbnavn

        print '\nPrevious Strain Vector', strains2
        if Fram[1]==False:
            if Fram[2][Fram[1]]>=0:
                strains2[Fram[1]]= strains2[Fram[1]] + strains[Fram[1]]/4
            else:
                strains2[Fram[1]] = strains2[Fram[1]] - strains[Fram[1]]/4
        print '\nUpdated Strain Vector', strains2
        a = mod.rootAssembly
        exx, eyy, ezz, exy, exz, eyz = strains2
        mod.DisplacementBC(name='BCX', createStepName=difstpNm,
                           region=a.sets['RPX'], u1=exx, u2=exy, u3=exz, ur1=UNSET, ur2=UNSET, ur3=UNSET,
                           amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)

        mod.DisplacementBC(name='BCY', createStepName=difstpNm,
                           region=a.sets['RPY'], u1=exy, u2=eyy, u3=eyz, ur1=UNSET, ur2=UNSET, ur3=UNSET,
                           amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)

        mod.DisplacementBC(name='BCZ', createStepName=difstpNm,
                           region=a.sets['RPZ'], u1=exz, u2=eyz, u3=ezz, ur1=UNSET, ur2=UNSET, ur3=UNSET,
                           amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)


        try:
            mdb.jobs[Jobbnavn].submit(consistencyChecking=OFF)
            mdb.jobs[Jobbnavn].waitForCompletion()
        except:
            pass

        print '\nPostProcess'
        execfile(processering + 'nonLinearPostprocessing.py')
        t = (time.time() - start_time)
        print('t for Restart iterasjon=', t)
    strains2 = strains.tolist()

    print 'Reached end of random key Iteration'
    t = (time.time() - start_time)
    print('t ved ferdig', t)
    #"""
    Q = Q + 1
    del section, regionToolset, dgm, part, material, assembly, step, interaction
    del load, mesh, job, sketch, visualization, xyPlot, dgo, connectorBehavior

#Open for big scale iterations

"""
Itra = open(Tekstfiler+'Iterasjoner.txt', "a")
Itra.write('\n')
Itra.close()
"""