from random import *
from math import *
import numpy as np
from multiprocessing import cpu_count
numCpus = cpu_count()/4
print ('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n'
       'Multiscale Modelling, Microscale  \n'
       'Allowed numCpus = ',numCpus)

"""         RVE MODELLERING                """
#RVEmodellfibercoordinaterdata
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

#Abaqus operations
def createPart_n_Ophanmesh():                                       # Creates an RVE model and a orphanmesh
    Mdb()  # reset Abaqus
    execfile(GitHub+Abaqus+'RVEsketching.py')                                             # Lage 2D RVE fra fiberpopulasjon data
    del mdb.models['Model-1']                                                             # Slett standard part model 1
    execfile(GitHub+Abaqus+'RVEmeshpart.py')                                              # Meshe 2D RVE  til 3D part og lage orphanmesh
    print '\nRVEpart created, meshed and Orphanmesh created'
def createSets_n_Datums():                                          # Element sets for materials properties. Fiber center datums for material orientation
    p = mod.parts[meshPartName]
    execfile(GitHub+Abaqus+'RVEelementsets.py')                                         # Sette i fiber, sizing og matrix elementer i set
                                                                                        # Lage cylindriske kordinatsystemer i fiber sentrum
    if not noFiber and Interface and nonLinearDeformation:
        # Lage fiber datums for material orientering av Interface
        for ie in range(0, len(xydata)):
            x = xydata[ie][0]
            y = xydata[ie][1]
            p.DatumCsysByThreePoints(name=('Fiber datum ' + str(ie)), coordSysType=CYLINDRICAL,
                                 origin=(x, y, 0.0), point1=(x + 1.0, y, 0.0), point2=(x + 1.0, y + 1.0, 0.0))
        # Set cohesive elementtype paa Interface
        p.setElementType(regions=p.sets['Interfaces'],
                         elemTypes=(mesh.ElemType(elemCode=COH3D8, elemLibrary=STANDARD),))
    print '\nElement sets (and Fiber center datums) created'
def create_Properites():                                    # Sett materialegenskaper for element settene i kompositten
    execfile(GitHub + Abaqus + 'RVEproperties.py')
    print '\nMaterial properties assigned to element sets in model'
def createCEq():                                        # Sett constraint equations for RVE model
    execfile(GitHub + Abaqus + 'RVE_Assembly_RP_CE.py')
    print '\nReference points created and constraint equ. applied'
def ReadajustInterface():                                    # Rearrange fiber interface nodes for different element thickness and stable simulations
    execfile(GitHub + Abaqus + 'RVE_InterfaceElementThickness.py')
    print '\nInterface elements adjusted'

"""         SIMULERING               """

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


"""$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        VARIABLER                                       """
#FLAGS
Runjobs = 0                             #   Bestemmer om jobber skal kjores
linearAnalysis = 0                      #   Linear analyse
nonLinearDeformation = 1                #   non-linear analyse

Singlepin = 1                               #   Laaser en hjorne node mot forskyvning i 3 retninger
tripplepin = 0                              #   Laaser to noder mot forskyvning. En langs kant i 2 retninger og en i midten i 1 retning

#Interface
Interface = 1                                   # Modellere Interface?
rinterface = 0.005                              # Interfacetykkelse ved modellering relativt til radius.    0.005 =0 .5%
ElementInterfaceT = 0.005                       # Sette/endre Interfacetykkelse relativt til radius.

# Fibere
noFibertest = 0                                     # Fjerner alle fiber fra modellen
Fibervariation = 1                                  # Legger til fiberradius variasjon fra standard avvik

rmean = 8.7096                      # Gjennomsnittradius. Om fibervariasjon er uniform.
Rstdiv = 0.6374                     # Om fibervariasjon saa brukes dette som Standard avvik fra gjennomsnittsradius.

# Meshsize
FiberSirkelResolution = 32                              # Standard meshsizer er 2*pi/FiberSirkelResolution
meshsize = rmean * 2 * pi / FiberSirkelResolution           # Meshsize fra interface resolution rundt fiber

#Material Density
MaterialDens  = 0
"""Process Start"""

Sample=[5]          #Forste sweepvariabel for parameter tester
#Sample=[0, 5, 10, 25, 50]
for m in range(0,len(Sample)):
    #  RVE Modelleringsvariabler
    nf   =      Sample[m]
    Vf   =      0.6
    RVEt =      meshsize            #      RVE modellens tykkelse.

    #Toleranser og klaringer
    Rclearing  = 0.025                    # Minimumsavstand mellom fibere og fra kantene. Kan kanskje settes lik meshsize?
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

        if Interface:
            print('Aspect ratio for Interface elements ved modellering = ' + str(round(meshsize / (rinterface * rmean), 2)) +
                    '\t Interface element thickness = ' + str(float(ElementInterfaceT * rmean)))

            # Se tekstfiler for databehandling
        GitHub  = 'C:/Multiscale-Modeling/'
        workpath =  'C:/Temp/'

        Tekstfiler, Abaqus = 'textfiles/', 'Abaqus_steg/'

        parameterpath = GitHub + 'Parametere.txt'  # Skrives ned for chaining  til ett annet script
        coordpath = GitHub + 'coordst.txt'  # Hentes fra genererefiberPop chaining  til ett annet script

        lagrestiffpath = GitHub + 'Stiffness.txt'  # Skrives ned statistikk til ett annet script
        Envelope = GitHub + Tekstfiler + 'envelope'  # Parameteravhengig - Spesifikt navn legges til i funksjonen

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
                Enhetstoyinger[g] = [Retning[g] + str(m) + '_' + str(Q)]

            Sweeptoyinger = [''] * sweepcases                               # Sweepcases
            for g in range(0,sweepcases):
                Sweeptoyinger[g] = ('Sweep_strain'+ str(m) + '_'+str(int(g*180*sweepresolution/pi))+'__'+str(int(Q)))

        # RVE model creation in Abaqus
        xydata = None                       # Fiber kordinater og radiuser
        if not noFiber:
            execfile(GitHub+'GenerereFiberPopTilFil.py')            # create a random population
            xydata= hentePopulation()                               # hente fibercoordinater
        createPart_n_Ophanmesh()            # Lage 2D RVE shell fra fiberpopulasjon data, meshe RVE, extrudere til 3D part, lage orphanmesh og sette cohesive elementtype paa Interface
        createSets_n_Datums()               # Element sets for material properties and Fiber center datums for material orientation
        create_Properites()                 # Sette egenskaper paa fiber og matrix materialene
        createCEq()                         # Sette rVE med x i fiber retning. Lage constrain equations til RVE stykket og fixe boundary condition
        if not noFiber and True:
            ReadajustInterface()            # Justere pa elementtykkelsen pa interface elements

        print 'RVEmodel made from given parameters and random key'

        """Simuleringer sweeps lokke"""


        strains = {'TensionEyy' :, 'TensionEzz':[0,0,-1e-3,0,0,0],'ShearExy':[0,0,0,1e-3,0,0]} \
                #                   exx,    eyy,    ezz,    exy,    exz,    eyz
        cases=[('TensionEyy',       [  0,   1e-3,   0,      0,      0,     0]),        # Tension
               ('CompressionEyy',   [  0,  -1e-3,   0,      0,       0,   0]),           # Compression
               ('TensionEzz',       [ 0,    0,      1e-3,   0,      0, 0]),              # Tension
               ('CompressionEzz',   [ 0,    0,      -1e-3,  0,      0, 0]),                # Compression
               ('ShearExy',         [0,     0,      0,      1e-3,   0,0]),                  # Shear
               ('ShearExy+Eyy',     [0,     1e-3,      0,      1e-3,   0,0]),       # Shear + Tension
               ('ShearExy-Eyy',     strains['ShearExy'] - strains['TensionEyy']),         # Shear + Compression
               ('ShearExy+Ezz',     strains['ShearExy'] + strains['TensionEzz']),       # Shear + Tension
               ('ShearExy-Ezz',     strains['ShearExy'] - strains['TensionEzz'])]       # Shear + Compression



        for Case in cases:
            if linearAnalysis:
                execfile(GitHub + Abaqus + 'LinearAnalysis.py')
            if nonLinearDeformation:
                Jobbnavn, Strain = Case
                        #exx, eyy, ezz, exy, exz, eyz
                execfile(GitHub + Abaqus + 'nonLinearAnalysis.py')


            print 'Reached end of 2 Iteration'

    print 'Reached end of Iteration'
del IfWork_NowDone