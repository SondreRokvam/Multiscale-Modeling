from random import *
from math import *
import numpy as np
from multiprocessing import cpu_count
numCpus = cpu_count()/4
print'%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n', 'Multiscale Modelling, Microscale  \n', 'Allowed numCpus = ',numCpus,'\n'
"""         PROCESS FLAGS                                       """
Createmodel = 0

Runjobs = 1                             #   Bestemmer om jobber skal kjores
linearAnalysis = 0                      #   Linear analyse for aa finne stivhets matrix
nonLinearDeformation = 1                #   non-linear analyse

Singlepin = 1                               #   Laaser en hjorne node mot forskyvning i 3 retninger
tripplepin = 1                                #   Laaser to noder mot forskyvning. En langs kant i 2 retninger og en i midten i 1 retning

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
    if not noFiber and Interface and True:        # Rearrange fiber interface nodes for controlled elementthickness and stable simulations
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

"""         RVE MODELLERING                """
#Interface
Interface = 1                                   # Modellere Interface?
rinterface = 0.005                              # Interfacetykkelse ved modellering relativt til radius.    0.005 =0 .5%
ElementInterfaceT = 0.001                       # Sette/endre Interfacetykkelse relativt til radius.

# Fibere
noFibertest = 0                                     # Fjerner alle fiber fra modellen
Fibervariation = 1                                  # Legger til fiberradius variasjon fra standard avvik

rmean = 8.7096                      # Gjennomsnittradius. Om fibervariasjon er uniform.
Rstdiv = 0.6374                     # Om fibervariasjon saa brukes dette som Standard avvik fra gjennomsnittsradius.

# Meshsize
FiberSirkelResolution = 16                              # Standard meshsizer er 2*pi/FiberSirkelResolution
meshsize = rmean * 2 * pi / FiberSirkelResolution           # Meshsize fra interface resolution rundt fiber

#Material Density
MaterialDens  = 1
Dampening = 0

Sample=[50]   #Forste sweepvariabel
for m in range(0,len(Sample)):
    #  RVE Modelleringsvariabler
    nf   =      int(Sample[m])
    Vf   =      0.6
    RVEt =      meshsize            #      RVE modellens tykkelse.

    #Modellerings toleranser og klaringer
    Rclearing  = 0.025                    # Minimumsavstand mellom fibere og fra kantene rel til radius. Kan kanskje settes lik meshsize?
    tol = rinterface*0.4                  # Modellerings toleranse er mindre en minste modelleringsvariabel

    #Unit stess sweeps
    sweepcases = 1      # Opplosning paa stress sweeps vinkler
    id = np.identity(6)  # Identity matrix for normalised load cases.'Exx','Eyy','Ezz','Exy','Exz','Eyz'

    #Se Generelle instilliger
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

            # Fibervariabler
        r = rmean
        gtol = Rclearing * r  # Dodsone klaring toleranse
        ytredodgrense = r + gtol  # Dodzone avstand, lengst fra kantene
        indredodgrense = r - gtol  # Dodzone avstand, naermest kantene

            # iterasjonsgrense i Fiberutplassering og stepsize paa Stress sweep
        iterasjonsgrense = 10000

        sweepresolution = 2 * pi / sweepcases

        if Interface and Createmodel:
            print('Aspect ratio for Interface elements ved modellering = ' + str(round(meshsize / (rinterface * rmean), 2)) +
                    '\t Interface element thickness = ' + str(float(ElementInterfaceT * rmean)))

            # Se tekstfiler for databehandling
        #Hovedmapper
        GitHub  = 'C:/Multiscale-Modeling/'
        workpath =  'C:/Temp/'
        #Undermapper
        Tekstfiler, Abaqus = 'textfiles/', 'Abaqus_steg/'
        #Stottefiler
        parameterpath = GitHub + 'Parametere.txt'  # Skrives ned for chaining  til ett annet script
        coordpath = GitHub +  'RVEcoordinater.txt'  # Hentes fra genererefiberPop chaining  til ett annet script
            # ABAQUS modelleringsnavn
        modelName = 'Model-A'
        partName, meshPartName = 'Part-1', 'Part-1-mesh-1'
        instanceName = 'PART-1-MESH-1-1'
        stepName, difstpNm = 'Enhetstoyninger', 'Lasttoyinger'

    #RVE random modellering sweep
    n = 1           # Andre Sweep lokke. Itererer med random nokkeler fra 0 til n
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

        # Se randomseed spesifikke variabler og navn
        if True:                     # For aa kunne kollapse variabler
            seed(Q)                                     # Q er randomfunksjonensnokkelen
            wiggle = random() * rmean                     # Omplasseringsgrenser for fiberomplassering
            Retning =['Exx', 'Eyy' , 'Ezz' ,'Exy' , 'Exz' , 'Eyz']
            #Lineare RVE og n relative ABAQUS Jobb navn
            Enhetstoyinger =['']*6
            for g in range(0, 6):                                           # Enhetstoyingene fra 0 til 5. Alle 6
                Enhetstoyinger[g] = [Retning[g] + str(Sample[m]) + '_' + str(Q)]
            Sweeptoyinger = [''] * sweepcases                               # Sweepcases
            for g in range(0,sweepcases):
                Sweeptoyinger[g] = ('Sweep_strain'+ str(Sample[m]) + '_'+str(int(g*180*sweepresolution/pi))+'__'+str(int(Q)))

            lagrestiffpath = GitHub + Tekstfiler + 'Stiffness__NF-'+ str(int(nf))+'.txt'  # Skrives ned statistikk til ett annet script
            Envelope = GitHub + Tekstfiler + 'envelope'  # Parameteravhengig - Spesifikt navn legges til i funksjonen

        # RVE model in Abaqus
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

        # Boundary mot rigid body movement i simulering
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
        Increments = {'maxNum':1000,'initial': 1e-06,'min':1e-20,'max':1e-2}
        if linearAnalysis:          # LinearAnalysis for stiffness and small deformation
            execfile(GitHub + Abaqus + 'LinearAnalysis.py')
        if nonLinearDeformation:    # nonLinearAnalysis for strength and large deformation

            strains = {'ShearExy':[0,0,-0.0063,0.0182,0,0],'TensionEyy':[0,0.1,0,0,0,0], 'TensionEzz':[0,0,0.1,0,0,0]}
                    #                   exx,    eyy,    ezz,    exy,    exz,    eyz
            cases=[['ShearExy',strains['ShearExy']]]#, ['TensionEyy',strains['TensionEyy']], ['TensionEzz',strains['TensionEzz']]]       # Shear + Compression



            for Case in cases:
                if nonLinearDeformation:
                    Jobbnavn, Strain = Case
                            #exx, eyy, ezz, exy, exz, eyz
                    execfile(GitHub + Abaqus + 'nonLinearAnalysis.py')


        print 'Reached end of random key Iteration'
    print 'Reached end of primary Iteration'