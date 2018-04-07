from random import *
from math import *
import numpy as np
from multiprocessing import cpu_count
numCpus = cpu_count()/4
print'%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n', 'Multiscale Modelling, Microscale  \n', 'Allowed numCpus = ',numCpus,'\n'
def hentePopulation():                 #Les fiber matrix populasjon
    xy=list()
    f = open(coordpath,'r')
    tekst = f.read()
    f.close()
    lines = tekst.split('\n')
    for line in lines:
        data = line.split('\t')
        a = float(data[0])  #   X
        b = float(data[1])  #   Y
        c = float(data[2])  #   R
        xy.append([a,b,c])  #   lagre til liste
    print 'Antall fiber = ',int(nf),'\tAntall fiberkoordinater = '+str(len(xy))
    return xy
def CreateNewRVEModel():
    # Creates RVE model and orphanmesh. Lage 2D RVE shell, meshe RVE, extrudere til 3D part, lage orphanmesh og sette cohesive elementtype paa Interface
    execfile(GitHub+Abaqus+'RVEsketching.py')                                             # Lage 2D RVE fra fiberpopulasjon data
    del mdb.models['Model-1']                                                             # Slett standard part model 1
    execfile(GitHub+Abaqus+'RVEmeshpart.py')                                              # Meshe 2D RVE  til 3D part, lage orphan mesh part
    p = mod.parts[meshPartName]                                   # Element sets for materials properties. Fiber center datums for material orientation
    execfile(GitHub+Abaqus+'RVEelementsets.py')                    # Sette i fiber, sizing og matrix elementer i set og Lage cylindriske kordinatsystemer i fiber sentrum
    execfile(GitHub + Abaqus + 'RVEproperties.py')                         # Sett materialegenskaper for elementset
    execfile(GitHub + Abaqus + 'RVE_Assembly_RP_CE.py')     # Assembly med RVE med x i fiber retning. Lage constrain equations til RVE modell og fixe boundary condition for rigid body movement
    if not noFiber and Interface and False:        # Rearrange fiber interface nodes for controlled elementthickness and stable simulations
        execfile(GitHub + Abaqus + 'RVE_InterfaceElementThickness.py')
Simuleringer=[]
def run_Job(Jobb, modelName):
    Simuleringer.append(Jobb)
    mdb.Job(name=Jobb, model=modelName, description='', type=ANALYSIS,
            atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90,
            memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True,
            explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF,
            modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='',
            scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=numCpus,
            numDomains=numCpus, numGPUs=1)
    if Runjobs:
        mdb.jobs[Jobb].submit(consistencyChecking=OFF)
        mdb.jobs[Jobb].waitForCompletion()

"""         PROCESS FLAGS                                       """
Createmodel = 1

Runjobs = 1                             #   ON/OFF Start analyser
linearAnalysis = 0                      #   ON/OFF Linear analyse for stiffness
nonLinearDeformation = 1                #   ON/OFF non-linear analyse for strength

Singlepin = 1                               #   Randbetingelse:    Laaser hjornenode mot forskyvning i 3 retninger
tripplepin = 0                              #   Randbetingelse:    Laaser to noder mot forskyvning. En sentrert kantnode i 2 retninger og midtnode i 1 retning

"""         RVE MODELLERING                """
if True:
    Interface = 1                                   # ON/OFF CohesiveInterface
    rinterface = 0.001                              # Interfacetykkelse ved modellering. Verdi er relativ til radius.    0.01 = 1%
    ElementInterfaceT = 0.001                       # Interfacetykkelse paa elementene.  Verdi er relativ til radius.

    noFibertest = 0                                     # Fjerner fiber fra modellen. Modeller resin blokk
    Fibervariation = 1                                  # ON/OFF variasjon fiberradius. Mean and standard div. Kan paavirke Vf i endelig model.

    rmean = 8.7096                              # Gjennomsnittradius pa fiber
    Rstdiv = 0.6374                             # OStandard avvik fra gjennomsnittsradius

    # Meshsize
    FiberSirkelResolution = 24                                  # Meshresolution pa Fiber omkrets. 2*pi/FiberSirkelResolution
    meshsize = rmean * 2 * pi / FiberSirkelResolution           # Meshsize fra resolution paa interface paa fiberomkrets

    #Material Density
    MaterialDens  = 0
    Dampening = 0

Sample=[50]   #Forste sweepvariabel
for m in range(0,len(Sample)):
    """  RVE design parameters  """
    nf   =      int(Sample[m])
    Vf   =      0.6                 #
    RVEt =      meshsize            #      RVE tykkelse i fiberretning

    Rclearing  = 0.025                    # Minimumsavstand mellom fiberkant og RVE kant. Verdi relativ til radius. Skal den settes lik meshsize?
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
            dL = rmean*2
            noFiber = 1
        if not nf == 0:                              # RVE dL er relativ av nf, rmean og V
            dL = ((nf * pi * rmean ** 2) / (Vf)) ** 0.5
            noFiber =0

            #RVE tykkelse
        tykkelse = RVEt

        """     Utregning av modelleringsvariabler   """
        r = rmean
        gtol = Rclearing * r  # Dodsone klaring toleranse
        ytredodgrense = r + gtol  # Dodzone avstand, lengst fra kantene
        indredodgrense = r - gtol  # Dodzone avstand, naermest kantene

        iterasjonsgrense = 10000   # iterasjonsgrense i Fiberutplassering loop

        sweepresolution = 2 * pi / sweepcases

        """   Details  """
        if Interface and Createmodel:
            print('Aspect ratio for Interface elements ved modellering = ' + str(round(meshsize / (rinterface * rmean), 2)) +
                    '\t Interface element thickness = ' + str(float(ElementInterfaceT * rmean)))

            # Se tekstfiler for databehandling

        GitHub, workpath  = 'C:/Multiscale-Modeling/', 'C:/Temp/'           #Hovedmapper
        Tekstfiler, Abaqus = 'textfiles/', 'Abaqus_steg/'                   #Undermapper

        parameterpath = GitHub + 'Parametere.txt'               # Skrives ned for chaining eller importering
        coordpath = GitHub +  'RVEcoordinater.txt'              # Skrives ned i genererefiberPop for chaining til main script

        """ ABAQUS modelleringsnavn    """

        modelName = 'Model-A'
        partName, meshPartName = 'Part-1', 'Part-1-mesh-1'
        instanceName = 'PART-1-MESH-1-1'
        stepName, difstpNm = 'Enhetstoyninger', 'Lasttoyinger'

    #Random modellering lokke
    n = 1           #  Itererer med random nokkeler fra 0 til n
    for Q in range(0,n):
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

            """ Navn for lineare tester """
            Retning =['Exx', 'Eyy' , 'Ezz' ,'Exy' , 'Exz' , 'Eyz']
            Enhetstoyinger =['']*6
            for g in range(0, 6):                                            # Enhetstoyinger for lineare retninger
                Enhetstoyinger[g] = [Retning[g] + str(int(Sample[m])) + '_' + str(Q)]       # 6 Enhetstoyinger - Exx, Eyy, Ezz, Exy, Exz, Eyz
            Sweeptoyinger = [''] * sweepcases                               # Sweepcases
            for g in range(0,sweepcases):
                Sweeptoyinger[g] = ('Sweep_strain'+ str(int(Sample[m])) + '_'+str(int(g*180*sweepresolution/pi))+'__'+str(int(Q)))

            """ Datalagring """
            lagrestiffpath = GitHub + Tekstfiler + 'Stiffness__NF-'+ str(int(nf))+'.txt'  # Skrives ned statistikk til ett annet script
            Envelope = GitHub + Tekstfiler + 'envelope'  # Parameteravhengig - Spesifikt navn legges til i funksjonen

        """ Get Abaqus RVE model """
        if True:
            Mdb()  # reset Abaqus
            model = mdb.Model(name=modelName, modelType=STANDARD_EXPLICIT)  # Lage model
            mod = mdb.models[modelName]
            if Createmodel:
                xydata = None                       # Fiber kordinater og radiuser
                if not noFiber:
                    execfile(GitHub+'GenerereFiberPopTilFil.py')            # create a random population
                    xydata= hentePopulation()                               # hente fibercoordinater
                CreateNewRVEModel()
                mdb.saveAs(pathName=workpath+'RVE-'+str(Sample[m])+'-'+str(int(Q)))
            else:
                openMdb(pathName=workpath+'RVE-'+str(Sample[m])+'-'+str(int(Q)))
                mod = mdb.models[modelName]

        # Boundaryconditions mot rigid body movement
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


        """ SIMULERINGER    """
        #try:
        if linearAnalysis:                                  # LinearAnalysis for stiffness and small deformation
            execfile(GitHub + Abaqus + 'LinearAnalysis.py')

        Increments = {'maxNum': 1000, 'initial': 1e-10, 'min': 1e-20, 'max': 1e-2}
        if nonLinearDeformation:                            # nonLinearAnalysis for strength and large deformation
            #Unitstrain to fracture.

            #Sweepstrain to fracture
            #       STRAINS:  exx, eyy, ezz, exy, exz, eyz
            #strains = {'ShearExy':[0,0,-0.0063,0.0182,0,0],'TensionEyy':[0,0.1,0,0,0,0], 'TensionEzz':[0,0,0.1,0,0,0]}
            strains = {'ShearExy':[0,0,0.063,0.182,0,0],'TensionEyy':[0,0.1,0,0,0,0], 'TensionEzz':[0,0,0.1,0,0,0]}

            #       CASES: Name, Strains
            cases=[['ShearExy',strains['ShearExy']]]#, ['TensionEyy',strains['TensionEyy']], ['TensionEzz',strains['TensionEzz']]]       # Shear + Compression

            for Case in cases:
                if nonLinearDeformation:
                    Jobbnavn, Strain = Case
                    execfile(GitHub + Abaqus + 'nonLinearAnalysis.py')
        #except:


        print 'Reached end of random key Iteration'
    print 'Reached end of primary Iteration'
