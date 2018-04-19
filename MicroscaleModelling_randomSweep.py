from random import *
from math import *
import numpy as np
import os
from sets import Set
import multiprocessing
print'%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n', 'Multiscale Modelling, Microscale  \n',
def CreateNewRVEModel():
    # Creates RVE model and orphanmesh. Lage 2D RVE shell, meshe RVE, extrudere til 3D part, lage orphanmesh og sette cohesive elementtype paa Interface
    execfile(GitHub+Abaqus+'RVEsketching.py')           # Lage 2D RVE fra fiberpopulasjon data
    del mdb.models['Model-1']                           # Slett standard part model 1
    execfile(GitHub+Abaqus+'RVEmeshpart.py')            # Meshe 2D RVE  til 3D part, lage orphan mesh part
    p = mod.parts[meshPartName]
    execfile(GitHub+Abaqus+'RVEelementsets.py')         # Fiber, sizing og matrix elementer i set og Fiber center datums for material orientation
    execfile(GitHub + Abaqus + 'RVEproperties.py')                         # Sett materialegenskaper for elementset
    execfile(GitHub + Abaqus + 'RVE_Assembly_RP_CE.py')     # Assembly med RVE med x i fiber retning. Lage constrain equations til RVE modell og fixe boundary condition for rigid body movement
    if not noFiber and Interface:        # Rearrange fiber interface nodes for controlled elementthickness and stable simulations
        execfile(GitHub + Abaqus + 'RVE_InterfaceElementThickness.py')
    """ Boundaryconditions mot rigid body movement"""
    if True:
        if Singlepin:
            region = mod.rootAssembly.sets['NL1']
            mod.PinnedBC(name='Laas-3', createStepName='Initial',
                         region=region, localCsys=None)
        if tripplepin and Singlepin:
            region = mod.rootAssembly.sets['NL2']
            mod.DisplacementBC(name='Laas-2', createStepName='Initial',
                               region=region, u1=SET, u2=UNSET, u3=SET, ur1=UNSET, ur2=UNSET, ur3=UNSET,
                               amplitude=UNSET, distributionType=UNIFORM, fieldName='',
                               localCsys=None)
            region = mod.rootAssembly.sets['NL3']
            mod.DisplacementBC(name='Laas-1', createStepName='Initial',
                               region=region, u1=SET, u2=UNSET, u3=UNSET, ur1=UNSET, ur2=UNSET, ur3=UNSET,
                               amplitude=UNSET, distributionType=UNIFORM, fieldName='',
                               localCsys=None)
def run_Job(Jobb, modelName):
    mdb.Job(name=Jobb, model=modelName, description='', type=ANALYSIS,
            atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90,
            memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True,
            explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF,
            modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='',
            scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1,
            numDomains=1, numGPUs=1)
    if Runjobs:
        mdb.jobs[Jobb].submit(consistencyChecking=OFF)
        mdb.jobs[Jobb].waitForCompletion()
    else:
        mdb.jobs[Jobb].writeInput(consistencyChecking=OFF)
        qw = open(Jobsss, "a")
        qw.write('call "C:\SIMULIA\Abaqus\6.14-4\code\bin\abq6144.exe" job=' + Jobb + ' cpus=' + str(numCPU))
        qw.close()
numCPU = multiprocessing.cpu_count()


#Hent Test variabler
execfile('C:\Multiscale-Modeling\TestVariabler.py')


Sample=[50]   #Forste sweepvariabel
#Sample=np.round(np.linspace(2 ,80,79))
for m in range(0,len(Sample)):
    """  RVE design parameters  """
    if True:
        nf   =      int(Sample[m])
        Vf   =      0.6                 #
        RVEt =      meshsize            #      RVE tykkelse i fiberretning

        Rclearing  = 0.01                    # Minimumsavstand mellom fiberkant og RVE kant. Verdi relativ til radius. Skal den settes lik meshsize?
        tol = rinterface*0.4                  # Modelleringstoleranse - Mindre en minste modelleringsvariabel (rInterface)
        """   Stess sweeps settings     """
        sweepcases = 1              # Stress sweeps cases. Decides sweep resolution
        id = np.identity(6)         # Identity matrix. Good for normalised load cases.'Exx','Eyy','Ezz','Exy','Exz','Eyz'
    #Generelle instilliger
    if True:                     # For aa kunne kollapse instillinger
        print Sample[m]
        if nf == 0 or Vf == 0 or noFibertest:
            nf = 0
            Vf = 0
            dL = rmean*5
            noFiber = 1
        if not nf == 0:                              # RVE dL er relativ av nf, rmean og V
            dL = ((nf * pi * rmean ** 2) / (Vf)) ** 0.5
            noFiber =0

            #RVE tykkelse
        tykkelse = RVEt

        """     Modelleringsvariabler   """
        r = rmean
        gtol = Rclearing * r  # Dodsone klaring toleranse
        ytredodgrense = r + gtol  # Dodzone avstand, lengst fra kantene
        indredodgrense = r - gtol  # Dodzone avstand, naermest kantene

        iterasjonsgrense = 10000   # iterasjonsgrense i Fiberutplassering loop

        sweepresolution = 2 * pi / sweepcases
        Retning = ['Exx', 'Eyy', 'Ezz', 'Exy', 'Exz', 'Eyz']
        """   Details  """
        if Interface and Createmodel:
            print('Aspect ratio for Interface elements ved modellering = ' + str(round(meshsize / (rinterface * rmean), 2)) +
                    '\t Interface element thickness = ' + str(float(ElementInterfaceT * rmean)))

            # Se tekstfiler for databehandling

        GitHub, workpath  = 'C:/Multiscale-Modeling/', 'C:/Temp/'           #Hovedmapper
        Tekstfiler, Abaqus = 'textfiles/', 'Abaqus_steg/'                   #Undermapper

        Jobsss = workpath + 'Abaqusjobs.bat'
        parameterpath = GitHub +Tekstfiler+'Parametere.txt'               # Skrives ned for chaining eller importering
        iterationsParaPath = GitHub + Tekstfiler+'IterationParameters.txt'


        """ ABAQUS modelleringsnavn    """

        modelName = 'Model-A'
        partName, meshPartName = 'Part-1', 'Part-1-mesh-1'
        instanceName = 'PART-1-MESH-1-1'
        stepName, difstpNm = 'Enhetstoyninger', 'Lasttoyinger'

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

        # Rydde for neste iterasjon
        if RunningCleanup:
            filelist = [f for f in os.listdir(workpath) if not f.endswith('.inp')]
            for f in filelist:
                try:
                    os.remove(os.path.join(workpath, f))
                except:
                    pass
        """Random variabler og iterasjonsnavn"""
        if True:                     # For aa kunne kollapse variabler
            seed(Q)                                                         # Q er randomfunksjonensnokkelen
            wiggle = random() * rmean                                       # Omplasseringsgrenser for fiberomplassering

            """ Navn for lineare tester """

            Enhetstoyinger =['']*6                                          # Enhetstoyinger for lineare retninger
            for g in range(0, 6):                                                   # 6 Enhetstoyinger - Exx, Eyy, Ezz, Exy, Exz, Eyz
                Enhetstoyinger[g] = [Retning[g] + str(int(Sample[m])) + '_' + str(Q)]
            Sweeptoyinger = [''] * sweepcases                               # Sweepcasesog n relative ABAQUS Jobb navn
            for g in range(0,sweepcases):
                Sweeptoyinger[g] = ('Sweep_strain'+ str(int(Sample[m])) + '_'+str(int(g*180*sweepresolution/pi))+'__'+str(int(Q)))

            """ Datalagring """
            lagrestiffpath = GitHub + Tekstfiler + 'Stiffness__NF-'+ str(int(nf))+'.txt'  # Skrives ned statistikk til ett annet script
            Envelope = GitHub + Tekstfiler + 'envelope'  # Parameteravhengig - Spesifikt navn legges til i funksjonen
            coordpath = GitHub + Tekstfiler + 'RVEcoordinatsandRadiuses'+ str(int(Sample[m])) + '_' + str(Q)+'.txt'  # Skrives ned i genererefiberPop for reference
        """ Get Abaqus RVE model """
        if 1:
            Mdb()  # reset Abaqus
            model = mdb.Model(name=modelName, modelType=STANDARD_EXPLICIT)  # Lage model
            mod = mdb.models[modelName]
            if Createmodel:
                xydata = None                       # Fiber kordinater og radiuser
                if not noFiber:
                    execfile(GitHub+'GenerereFiberPopTilFil.py')            # create a random population
                CreateNewRVEModel()
                if Savemodel:
                    if Interface:
                        ### DEBUGGING FOR INTERFACE PROBLEMS
                        mdb.saveAs(pathName=workpath+'RVE-'+str(Sample[m])+'-'+str(int(Q)))
                    else:
                        mdb.saveAs(pathName=workpath + 'RVE-' + str(Sample[m]) + '-0-int-' + str(int(Q)))
            else:
                try:
                    Q=0
                    Mdb()  # reset Abaqus
                    mod = mdb.models[modelName]
                    model = mdb.Model(name=modelName, modelType=STANDARD_EXPLICIT)  # Lage model
                    openMdb(pathName=workpath + 'RVE-' + str(Sample[m]) + '-' + str(int(Q)))
                except:
                    pass

        """ SIMULERINGER    """
        if linearAnalysis:                                  # LinearAnalysis for stiffness and small deformation
            try:
                execfile(GitHub + Abaqus + 'LinearAnalysis.py')
            except:
                pass
                n=n+1
        if nonLinearAnalysis:                            # nonLinearAnalysis for strength and large deformation

            strain = 0.05#       STRAINS:  exx, eyy, ezz, exy, exz, eyz
            #strains = {'ShearExy': [0, -strain/3, 0, strain, 0, 0], 'TensionEyy': [0, 0.1, 0, 0, 0, 0], 'TensionEzz': [0, 0, 0.1, 0, 0, 0]}
            #strains = {'CompressionYCompressionZ': [-strain/3, -strain/3, 0, 0, 0, 0], 'TensionEyy': [0, 0.1, 0, 0, 0, 0], 'TensionEzz': [0, 0, 0.1, 0, 0, 0]}
            #cases = [['ShearExy', strains['ShearExy']] , ['TensionEyy',strains['TensionEyy']], ['TensionEzz',strains['TensionEzz']]]       # Shear + Compression
            cases = [['TensionX_NothingElse', [strain, 0, 0, 0, 0, 0]]]
            #cases = [['CompressionYCompressionZ', [0, -strain, -strain, 0, 0, 0]]]
            #strains = {'ShearExy': [0, -strain/3, 0, strain, 0, 0], 'TensionEyy': [0, 0.1, 0, 0, 0, 0], 'TensionEzz': [0, 0, 0.1, 0, 0, 0]}
            cases = [['ShearCompression',(0, -strain, 0, 0,strain, 0)]]       # Shear + Compression

            for Case in cases:
                Jobbnavn, Strain = Case
                try:
                    execfile(GitHub + Abaqus + 'nonLinearAnalysis.py')
                except:
                    pass
                    try:
                        Increments['initial'] = Increments['initial']/10
                        execfile(GitHub + Abaqus + 'nonLinearAnalysis.py')
                    except:
                        pass
                        n = n + 1
        print 'Reached end of random key Iteration'
        Q = Q + 1
        del section, regionToolset, dgm, part, material, assembly, step, interaction
        del load, mesh, job, sketch, visualization, xyPlot, dgo, connectorBehavior


    print 'Reached end of primary Iteration'




