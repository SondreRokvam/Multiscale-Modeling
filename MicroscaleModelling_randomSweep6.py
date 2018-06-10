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
            path = workpath + Jobb
            odb = session.openOdb(path + '.odb')
            fras = odb.steps[stepName].frames[-1]
        except:
            error=1
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
    limit = 0.05
    print Sigmapaths
    StressSi = np.genfromtxt(Sigmapaths)
    StressSi = StressSi[1:, 1:]
    for a in range(0, 6):
        if not a == Ret:
            StressSi[1:, a] = np.multiply(StressSi[1:, a], 1 / StressSi[1:, Ret])
    Sing = [0]*6
    Dob = [0]*6
    Trecharm = [0]*6
    StressFlags = [0]*6
    for kj in range(0,len(StressSi)):
        for sa in range(0,len(StressSi[0])):
            if not sa==Ret:
                if not Trecharm[sa]:
                    if not Dob[sa]:
                        if not Sing[sa]:
                            if abs(StressSi[kj][sa]) > limit:
                                Sing[sa]=1
                        else:
                            if abs(StressSi[kj][sa]) > limit:     #   Feilmargin
                                Dob[sa] = 1
                            else:
                                Sing[sa]=0
                    else:
                        if abs(StressSi[kj][sa]) > limit:  # Feilmargin
                            Trecharm[sa] = 1
                        else:
                            Sing[sa] = 0
                            Dob[sa] = 0
                else:
                    StressFlags[sa] = 1
        for sa in range(0, len(StressSi[0])):
            if StressFlags[sa]:
                return kj - 3, StressFlags, StressSi[kj]

    for sa in range(0, len(StressSi[0])):
        if Dob[sa]:
            return len(StressSi) - 2, Dob, StressSi[kj]
        if Sing[sa]:
            return len(StressSi) - 1, Sing, StressSi[kj]
    #del Ididtifying_diverging_frame_did_notwork
    print 'No divergence found'
    return len(StressSi)-1, StressFlags, StressSi[len(StressSi)-1]

# Init : forste fix
execfile('C:/MultiScaleMethod/Github/Multiscale-Modeling/Abaqus_modellering/Init.py')

Yeah = np.genfromtxt(GitHub + 'Sweeps.txt')
ParameterSweep = Yeah[6]

nf = 25
Vf = 0.6
scsc = 9973  # A prime for good measure

# Hvilken parameter sweepes

#   Meshsize/ Fiberresolution
#   Interface element thickness
#   RVE size from nf
#   Critical RVE convergence test
#   Klareringsavstand

SkalereInterface = ParameterSweep
print'Iterasjon : ', ItraPara  # Antall itersjoner saa langt

# Loops
tests = 1  # Antall iterasjoner per startup
n = [int(ParameterSweep * scsc + ItraPara * 169)]
ItraPara = 0



# Intiering
execfile(Modellering + 'Initial.py')

  # Arbeids lokke

while len(n)<=tests:
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

    Q = int( n[-1] )
    seed(Q)  # Q er randomfunksjonensnokkelen
    error = 0
    print Q
    print n
    """Datalagring"""

    execfile(Modellering + 'Set_text_dirs.py')

    """Modellering"""
    try:
        """ Abaqus RVE model """
        execfile(Modellering + 'Model.py')
    except:
        print 'Error in modellering'
        error = 1

    #Prep Stiffness tests
    if not error:
        # Strain test
        Enhetstoyinger = [''] * 6  # 6 Enhetstoyinger - Exx, Eyy, Ezz, Exy, Exz, Eyz
        for g in range(0, 6):
            if not noFibertest:
                Enhetstoyinger[g] = [Retning[g] + str(int(ParameterSweep[-1]*scsc)) + '_' + str(Q)]
            else:
                Enhetstoyinger[g] = [Retning[g] + 'noFiber']

        # Kjore Linear analyse
        if not FoundStiff:
            if not Createmodel:
                try:
                    openMdb(pathName=RVEmodellpath)
                    mod = mdb.models['Model-A']
                except:
                    print 'Cae not found'
                    error = 1
                    pass

    if not error:
        #try:
        execfile(Modellering +'LinearAnalysis.py')
        #except:
        #    print 'Problem_With_Linear_Analysis'
        #    error = 1

        print('t etter lin analyser=', (time.time() - start_time))
    if not error:
        if LinearpostPross:
            execfile(processering + 'LinearPostprocessing.py')
            t = (time.time() - start_time)
            print('t etter lin pross=', t)

    if FoundStiff:
        Stiffmatrix = np.load(lagrestiffpathmod)
        print
        '\nStiffnessmatrix:'
        for a in range(0, 6):
            print '%7f \t %7f \t %7f \t %7f \t %7f \t %7f' % (
                Stiffmatrix[0][a], Stiffmatrix[1][a], Stiffmatrix[2][a], Stiffmatrix[3][a], Stiffmatrix[4][a],
                Stiffmatrix[5][a])

        # Non linear tester


    if nonLinearAnalysis:
        """Inital Strength test"""
        if not error:
            # Stress test
            try:
                Magni = 3e-2    # Skalarverdi til toyning
                Ret = 1        # Mulige lastretninger STRAINS:  exx, eyy, ezz,  exy,  exz,  eyz
                strain = Magni * id[Ret]

                if True:
                    print '\n\nReferanse Strain Vector ', strain
                    stresses = np.round(np.dot(Stiffmatrix, strain),3)
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
                            del Problem_With_nonLinear_Analysis
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
            except:
                pass
                Q = Q + 1000
                n.append(Q)
                print 'Error in Stress tests'
                error=1

        #Adjustment of strain vector
        if not error and stresstest:
            strains2 = strains.tolist()
            Reset=1
            Jobbnav = Jobbnavn
            prev=0      #for aa vite hvor langt bak vi hoppet forrige gang
            reps = 50
            adjusts=0
            Frames = np.zeros(reps+1)
            while adjusts<reps:
                Fram = FrameFinder()  # Returns frame before divergion
                if not adjusts==0:
                    if Fram[0]<prevfram[0]:
                        Fram= prevfram
                print '\nfix:  ',adjusts

                print Fram
                StressSigs = np.genfromtxt(Sigmapaths)
                StressSigs = StressSigs[:Fram[0]]

                print StressSigs[-1, :]
                print 'plotpunkter   ', len(StressSigs)-1

                appe = 0
                diff = Fram[0] - prev

                if not diff<=0:
                    Frames[adjusts + 1] = Fram[0]
                    appe = 1

                    prev = Fram[0]

                    if adjusts == 0:
                        prevname = difstpNm
                    else:
                        prevname = 'rep' + str(adjusts - 1)
                    re =3
                    if diff == 3:
                        re=2
                    if diff==2 or strains[Ret] < 0:
                        re=1
                    if diff<=0 :
                        re=0

                    print Frames[adjusts + 1], Frames[adjusts],re
                    addedF = int(Frames[adjusts + 1]) - int(Frames[adjusts]) - re  # minus ## for prevantiv

                    stegy = 'rep' + str(adjusts)

                    print 'diff', diff,  'addF', addedF
                    print prevname
                    mod.StaticStep(name='rep' + str(adjusts), previous=prevname, nlgeom=ON, stabilizationMagnitude=0.0002,
                                   stabilizationMethod=DAMPING_FACTOR,
                                   continueDampingFactors=False, adaptiveDampingRatio=0.05)
                    IniTid = (StressSigs[-1, 0] - StressSigs[-2, 0]) * 0.9

                    steg = mod.steps['rep' + str(adjusts)]

                    steg.setValues(maxNumInc=Increments['maxNum'], initialInc=IniTid,
                                   minInc=Increments['min'], maxInc=Increments['max'], convertSDI=CONVERT_SDI_OFF)

                    steg.Restart(frequency=1, numberIntervals=0, overlay=OFF, timeMarks=OFF)

                    mod.setValues(restartJob=Jobbnavn,
                                  restartStep=prevname, restartIncrement=addedF)

                    Jobbnavn = Jobbnav + str(adjusts)
                    mdb.Job(name=Jobbnavn, model=modelName, description='', type=RESTART,
                            atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90,
                            memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True,
                            explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF,
                            modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='',
                            scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1,
                            numGPUs=0)


                print '\nPrevious Strain Vector', strains2
                print 'Change : ', Fram[1]

                d = 2
                #if strains[Ret] < 0:
                #    d = 10
                for ssss in range(0,len(strains)):
                    if Fram[1][ssss]:
                        adjfactor = abs(strains[ssss])/d
                        print 'Adjust by : ', adjfactor

                        if StressSigs[-1][ssss+1]>=0:
                            strains2[ssss] = strains2[ssss] + adjfactor
                        else:
                            strains2[ssss] = strains2[ssss] - adjfactor
                print 'Updated Strain Vector', strains2, '\n\n' + Jobbnavn

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

                if appe:
                    adjusts =adjusts+1
                    print 'count: ', adjusts
                    prevfram = Fram


            t = (time.time() - start_time)
            print('Reached end of random key Iteration\tt ved ferdig', t)
            ss = open('C:/Users/Sondre/Desktop/Ferdig'+str(ParameterSweep[ItraPara])+'.txt', "w")
            ss.close()
            Q = Q + 1000
            n.append(Q)
            del section, regionToolset, dgm, part, material, assembly, step, interaction
            del load, mesh, job, sketch, visualization, xyPlot, dgo, connectorBehavior


    if error:
        Q = Q +1
        n[-1] = Q
        print 'Error'
    else:
        Q = Q+1
        n.append(Q)