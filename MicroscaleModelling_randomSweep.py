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
    if numCPU==1:
        mdb.Job(name=Jobb, model=modelName, description='', type=ANALYSIS,
            atTime=None, memory=90,
            memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True,
            explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF,
            modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='',
            scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1,
            numDomains=1, numGPUs=1)
    else:
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
        qw.write('call "C:\SIMULIA\Abaqus\6.14-4\code\bin\abq6144.exe" job=' + Jobb + ' cpus=' + str(numCPU))
        qw.close()

#Directories
GitHub, workpath = 'C:/Multiscale-Modeling/', 'C:/Temp/'
Tekstfiler, Modellering = GitHub+'textfiles/', GitHub+'Abaqus_modellering/'

execfile(Modellering+'TestVariabler.py')        # Sette Test variabler
execfile(Modellering+'IterationParameters.py')  # Sette iterasjonsnummer

"""   Details  """
if Interface and Createmodel:
    print('Aspect ratio for Interface elements ved modellering = ' + str(round(meshsize / (rinterface * rmean), 2)) +
          '\t Interface element thickness = ' + str(float(ElementInterfaceT * rmean)))



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
n = 1           #  Itererer med random nokkeler fra 0 til n
Q = 0
while Q<n:
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

    """Random variabler og iterasjonsnavn"""
    if True:                     # For aa kunne kollapse variabler
        seed(Q)                                                         # Q er randomfunksjonensnokkelen
        wiggle = random() * rmean                                       # Omplasseringsgrenser for fiberomplassering

    """ Get Abaqus RVE model """
    if 1:
        Mdb()  # reset Abaqus
        model = mdb.Model(name=modelName, modelType=STANDARD_EXPLICIT)  # Lage model
        mod = mdb.models[modelName]
        if Createmodel:
            xydata = None                       # Fiber kordinater og radiuser
            if not noFiber:
                execfile(Modellering+'GenerereFiberPopTilFil.py')            # create a random population
            CreateNewRVEModel()
            if Savemodel:
                if Interface:
                    ### DEBUGGING FOR INTERFACE PROBLEMS
                    mdb.saveAs(pathName=workpath+'RVE-'+str(ParameterSweep[ItraPara])+'-'+str(int(Q)))
                else:
                    mdb.saveAs(pathName=workpath + 'RVE-' + str(ParameterSweep[ItraPara]) + '-0-int-' + str(int(Q)))
        else:
            try:
                Q=0
                Mdb()  # reset Abaqus
                mod = mdb.models[modelName]
                model = mdb.Model(name=modelName, modelType=STANDARD_EXPLICIT)  # Lage model
                openMdb(pathName=workpath + 'RVE-' + str(ParameterSweep[ItraPara]) + '-' + str(int(Q)))
            except:
                pass

    """ SIMULERINGER    """
    Jobsss = workpath + 'Abaqusjobs.bat'

    """   Stess sweeps settings     """
    sweepcases = 1              # Stress sweeps cases. Decides sweep resolution
    id   =   np.identity(6)          # Identity matrix. Good for normalised load cases.'Exx','Eyy','Ezz','Exy','Exz','Eyz'
    sweepresolution =    2 * pi / sweepcases
    Retning =    ['Exx', 'Eyy', 'Ezz', 'Exy', 'Exz', 'Eyz']

    """ Datalagring """
    Lagrestiffpath = Tekstfiler + 'Stiffness__NF-' + str(int(nf)) + '.txt'  # Skrives ned statistikk til ett annet script
    lagrestiffpath = Tekstfiler + 'StiffnessM.txt'  # Skrives ned statistikk til ett annet script
    Envelope = Tekstfiler + 'envelope'  # Parameteravhengig - Spesifikt navn legges til i funksjonen

    if linearAnalysis:                                  # LinearAnalysis for stiffness and small deformation
        """ Navn for lineare tester """
        Enhetstoyinger = [''] * 6  # Enhetstoyinger for lineare retninger
        for g in range(0, 6):  # 6 Enhetstoyinger - Exx, Eyy, Ezz, Exy, Exz, Eyz
            Enhetstoyinger[g] = [Retning[g] + str(int(ParameterSweep[ItraPara])) + '_' + str(Q)]

        Sweeptoyinger = [''] * sweepcases  # Sweepcasesog n relative ABAQUS Jobb navn
        for g in range(0, sweepcases):
            Sweeptoyinger[g] = ('Sweep_strain' + str(int(ParameterSweep[ItraPara])) + '_' + str(
                int(g * 180 * sweepresolution / pi)) + '__' + str(int(Q)))

        try:
            execfile(Modellering +'LinearAnalysis.py')
        except:
            pass
            n=n+1
    if nonLinearAnalysis:                            # nonLinearAnalysis for strength and large deformation

        strain = 1e-4#       STRAINS:  exx, eyy, ezz, exy, exz, eyz
        #strains = {'ShearExy': [0, -strain/3, 0, strain, 0, 0], 'TensionEyy': [0, 0.1, 0, 0, 0, 0], 'TensionEzz': [0, 0, 0.1, 0, 0, 0]}
        #strains = {'CompressionYCompressionZ': [-strain/3, -strain/3, 0, 0, 0, 0], 'TensionEyy': [0, 0.1, 0, 0, 0, 0], 'TensionEzz': [0, 0, 0.1, 0, 0, 0]}
        #cases = [['ShearExy', strains['ShearExy']] , ['TensionEyy',strains['TensionEyy']], ['TensionEzz',strains['TensionEzz']]]       # Shear + Compression
        cases = [['TensionX_NothingElse', [strain, 0, 0, 0, 0, 0]]]
        #cases = [['CompressionYCompressionZ', [0, -strain, -strain, 0, 0, 0]]]
        #strains = {'ShearExy': [0, -strain/3, 0, strain, 0, 0], 'TensionEyy': [0, 0.1, 0, 0, 0, 0], 'TensionEzz': [0, 0, 0.1, 0, 0, 0]}
        #cases = [['ShearCompression',(0, -strain, 0, 0,strain, 0)]]       # Shear + Compression

        for Case in cases:
            Jobbnavn, Strain = Case
            try:
                execfile(Modellering +'nonLinearAnalysis.py')
            except:
                pass
                try:
                    Increments['initial'] = Increments['initial']/10
                    execfile(Modellering + 'nonLinearAnalysis.py')
                except:
                    pass
                    n = n + 1
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