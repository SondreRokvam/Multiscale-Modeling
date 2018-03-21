from random import *
from math import *
import numpy as np
from multiprocessing import cpu_count
numCpus = cpu_count()/4
print ('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n'
       'Multiscale Modelling, Microscale  \n'
       'Allowed numCpus = ',numCpus)


"""         MODELLERINGS FUNKSJONER                """
#RVEmodell
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
def createPart_n_Ophanmesh():
    Mdb()  # reset Abaqus
    #Lag sketch
    execfile(GitHub+Abaqus+'RVEsketching.py')                                             # Lage 2D RVE fra fiberpopulasjon data
    del mdb.models['Model-1']                                             # Slett standard part
    execfile(GitHub+Abaqus+'RVEmeshpart.py')                                              # Meshe 2D RVE  til 3D part og lage orphanmesh
    print '\nRVEpart created, meshed and Orphanmesh created'
def createSets_n_Datums():
    p = mod.parts[meshPartName]
    execfile(GitHub+Abaqus+'RVEelementsets.py')
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
    print '\nElement sets and Fiber center datums  created' #Element sets for material properties and Fiber center datums for material orientation
def create_Properites():  # Angi materialegenskaper
    execfile(GitHub + Abaqus + 'RVEproperties.py')
    print '\nMaterial properties assigned to element sets in model'
def createCEq():
    execfile(GitHub + Abaqus + 'RVE_Assembly_RP_CE.py')
    print '\nReference points created and constraint equ. applied'
def collapsInterface():
    a = mod.rootAssembly
    nod = a.instances[instanceName].nodes
    count=0
    for fiba in xydata:
        x = fiba[0]
        y = fiba[1]
        r = rmean
        if Fibervariation:
            r = fiba[2]
        Fod = nod.getByBoundingCylinder((-10, y, -x), (10, y, -x), r  - tol)
        Fnod = nod.getByBoundingCylinder((-10, y, -x), (10, y, -x), r * (1 + rinterface)  - tol)
        Inod = nod.getByBoundingCylinder((-10, y, -x), (10, y, -x), r * (1 + rinterface) + tol)
        a.Set(nodes=Fod, name='noFiber'+str(count)+'nodes')
        a.Set(nodes=Fnod, name='Fiber'+str(count)+'nodes')
        a.Set(nodes=Inod, name='FiberInterface' + str(count) + 'nodes')
        a.SetByBoolean(name='Fiberflate'+ str(count) + 'nodes', sets=(a.sets['Fiber'+str(count)+'nodes'], a.sets['noFiber'+str(count)+'nodes'],), operation=DIFFERENCE)
        a.SetByBoolean(name='Interface'+ str(count) + 'nodes', sets=(a.sets['FiberInterface' + str(count) + 'nodes'], a.sets['Fiber'+str(count)+'nodes'],), operation=DIFFERENCE)
        Intnodes = a.sets['Interface'+ str(count) + 'nodes'].nodes
        Fibnodes = a.sets['Fiberflate'+ str(count) + 'nodes'].nodes
        for node in Intnodes:
            xns = node.coordinates[0]
            yns = node.coordinates[1]
            zns = node.coordinates[2]
            FN = Fibnodes.getByBoundingCylinder((xns - tol, yns, zns), (xns + tol, yns, zns), 2 * r * rinterface)
            IN = Intnodes.getByBoundingCylinder((xns - tol, yns, zns), (xns + tol, yns, zns), 2 * r * rinterface)
            a.Set(nodes=IN, name='IN')
            a.Set(nodes=FN, name='FN')
            nyx = round(FN[0].coordinates[0],5)
            nyy = round(FN[0].coordinates[1],5)
            nyz = round(FN[0].coordinates[2],5)
            a.editNode(nodes=a.sets['IN'], coordinate1=nyx, coordinate2=nyy, coordinate3=nyz)
            a.editNode(nodes=a.sets['FN'], coordinate1=nyx, coordinate2=nyy, coordinate3=nyz)
            a.regenerate()
            a.deleteSets(setNames=('noFiber'+str(count)+'nodes','IN','FN', 'Fiber'+str(count)+'nodes','FiberInterface' + str(count) + 'nodes','Fiberflate'+ str(count) + 'nodes','Interface'+ str(count) + 'nodes',))
        count = count + 1

"""         SIMULERINGS FUNKSJONER               """

def run_Job(Jobe, modelName):
    if Runjobs:
        mdb.Job(name=Jobe, model=modelName, description='', type=ANALYSIS,
        atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90,
        memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True,
        explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF,
        modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='',
        scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=numCpus,
        numDomains=numCpus, numGPUs=1)

        mdb.jobs[Jobe].submit(consistencyChecking=OFF)
        mdb.jobs[Jobe].waitForCompletion()
        """type=ANALYSIS,atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90,
                memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True,
                explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF,
                modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='',
                scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=numCpus,
                numDomains=numCpus, numGPUs=OFF)"""

# nonLinear
def create_nonLinearsweepedlastcases(Strain,bob):
    a = mod.rootAssembly
    mod.StaticStep(name=difstpNm, previous='Initial', nlgeom=ON)
    mod.steps['Lasttoyinger'].setValues(
        stabilizationMagnitude=0.0002, stabilizationMethod=DAMPING_FACTOR,
        continueDampingFactors=False, adaptiveDampingRatio=0.05,
        extrapolation=LINEAR, convertSDI=CONVERT_SDI_OFF)

    mod.fieldOutputRequests['F-Output-1'].setValues(variables=('DAMAGEC', 'DAMAGET', 'LE', 'MISES', 'PE', 'PEEQ', 'RT', 'S', 'SDEG','STATUS', 'STATUSXFEM', 'U'), timeInterval=0.01)
    mod.historyOutputRequests['H-Output-1'].setValues(variables=(
        'ALLDMD', 'ALLIE', 'ALLSD'))
    a.SetByBoolean(name='RPS', sets=(a.sets['RPX'], a.sets['RPY'],a.sets['RPZ'],))
    regDef=mdb.models['Model-A'].rootAssembly.sets['RPS']
    mod.HistoryOutputRequest(name='H-Output-2', 
        createStepName='Lasttoyinger', variables=('RT', 'UT'), 
        region=regDef, sectionPoints=DEFAULT, rebar=EXCLUDE)
    
    print '\nnon Linear load analysis'
    # Lagring av output data base filer .odb
    for case in range(0, 1):
        exx, eyy, ezz, exy, exz, eyz = Strain
        mod.DisplacementBC(name='BCX', createStepName=difstpNm,
                           region=a.sets['RPX'], u1=exx, u2=exy, u3=exz, ur1=UNSET, ur2=UNSET, ur3=UNSET,
                           amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)

        mod.DisplacementBC(name='BCY', createStepName=difstpNm,
                           region=a.sets['RPY'], u1=exy, u2=eyy, u3=eyz, ur1=UNSET, ur2=UNSET, ur3=UNSET,
                           amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)

        mod.DisplacementBC(name='BCZ', createStepName=difstpNm,
                           region=a.sets['RPZ'], u1=exz, u2=eyz, u3=ezz, ur1=UNSET, ur2=UNSET, ur3=UNSET,
                           amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)

        if Siglepin:
            region = a.sets['NL1']
            mod.PinnedBC(name='Laas-3', createStepName='Initial',
                        region=region, localCsys=None)
        if Trippelpin and Singlepin:
            region = a.sets['NL2']
            mod.DisplacementBC(name='Laas-2', createStepName='Initial',
                               region=region, u1=SET, u2=UNSET, u3=SET, ur1=UNSET, ur2=UNSET, ur3=UNSET,
                               amplitude=UNSET, distributionType=UNIFORM, fieldName='',
                               localCsys=None)
            region = a.sets['NL3']
            mod.DisplacementBC(name='Laas-1', createStepName='Initial',
                               region=region, u1=SET, u2=UNSET, u3=UNSET, ur1=UNSET, ur2=UNSET, ur3=UNSET,
                               amplitude=UNSET, distributionType=UNIFORM, fieldName='',
                               localCsys=None)



        run_Job(bob+'lol', modelName)

"""$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"""
"""            TEST VARIABLER               """
#Flag
Runjobs = 1                         # TRUE/FALSE Bestemmer om jobber skal kjores
nonLinearDeformation = 1              # TRUE/FALSE Linear eller nonlinear analyse?
Singlepin = 1
tripplepin = 1

noFiber = 0                               # TRUE/FALSE Overstyrer antall fiber til 0
Fibervariation = 1                          # TRUE/FALSE Skal fiber radius variere eller ikke?
Interface = 1                                  # TRUE/FALSE Interface paa fibere?
Interfacetykkelse = 1                            # TRUE/FALSE 0 volum Interfaceelement  paa fibere?

# Fibere
rmean = 8.7096  # Gjennomsnittradius. Om ikke fibervariasjon saa settes fibere til aa vaere uniform.
Rstdiv = 0.6374  # Standard avvik fra gjennomsnittsradius.

# Meshsize fra Interface resolution paa fiberomkrets
FiberSirkelResolution = 36          # Standard meshsixer er 2*pi/FiberSirkelResolution
meshsize = rmean * 2 * pi / FiberSirkelResolution           # Meshresolution

"""Process Start"""

Sample=[25]          #Forste sweepvariabel
#Sample=[0, 5, 10, 25,50]
for m in range(0,len(Sample)):
                                    #  RVE Modelleringsvariabler
    nf   =      Sample[m]
    Vf   =      0.6
    RVEt =      meshsize            #      RVE modellens tykkelse.

    #Toleranser og klaringer
    Rclearing  = 0.025                   # Prosent avstand av r klaring mellom fibere og fra kanter og sider
    rinterface = 0.005                    # Prosent avstand av r paa interfacetykkelse ved modellering
    tol = rinterface*0.4                  # Toleranse som er godt mindre en minste modelleringsvariabel

    #Unit stess sweeps
    sweepcases = 1      # Opplosning paa stress sweeps vinkler

    #Se instilliger
    if True:                     # For aa kunne kollapse instillinger
            # RVE modellering:
        if nf == 0 or Vf == 0 or noFiber:
            nf = 0
            Vf = 0
            dL = rmean*2
            noFiber = 1
        if not nf == 0:                              # RVE dL er relativ av nf, rmean og V
            dL = ((nf * pi * rmean ** 2) / (Vf)) ** 0.5

            #RVE tykkelse
        tykkelse = RVEt

            # Fibervariabler
        r = rmean
        gtol = Rclearing * r  # Dodsone klaring toleranse
        ytredodgrense = r + gtol  # Dodzone avstand, lengst fra kantene
        indredodgrense = r - gtol  # Dodzone avstand, naermest kantene

            # iterasjonsgrense i Fiberutplassering
        iterasjonsgrense = 10000

            # stepsize paa Stress sweep
        sweepresolution = 2 * pi / sweepcases

        if Interfacetykkelse:
            print 'Aspect ratio for Interface elements = ' + str(round(meshsize / (rinterface * rmean), 2)) + '    Interface elements thickness = ' + str(float(rinterface * rmean))

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

            #Lineare RVE og n relative ABAQUS Jobb navn
            Enhetstoyinger = ['Exx' + str(m) + '_' + str(Q), 'Eyy' + str(m) + '_' + str(Q), 'Ezz' + str(m) + '_' + str(Q),
                              'Exy' + str(m) + '_' + str(Q), 'Exz' + str(m) + '_' + str(Q), 'Eyz' + str(m) + '_' + str(Q)]
                                                        # Enhetstoyingene fra 0 til 5. Alle 6
            Sweeptoyinger = [''] * sweepcases
            for g in range(0,sweepcases):
                Sweeptoyinger[g] = ('Sweep_strain'+ str(m) + '_'+str(int(g*180*sweepresolution/pi))+'__'+str(int(Q)))

        #RVE parametere
        xydata = None
        if not noFiber:
            execfile(GitHub+'GenerereFiberPopTilFil.py')            # create a random population
            xydata= hentePopulation()                               # hente fibercoordinater

        # Abaqus Operasjoner
        createPart_n_Ophanmesh()            # Lage 2D RVE shell fra fiberpopulasjon data, meshe RVE, extrudere til 3D part og lage orphanmesh
        createSets_n_Datums()               # Element sets for material properties and Fiber center datums for material orientation

        create_Properites()
        createCEq()                                                                    # Lag constrain equations
        if not Interfacetykkelse and (Interface and not noFiber):
            print 'Collaps Interface elements'
            collapsInterface()
        if nonLinearDeformation:
                    #exx, eyy, ezz, exy, exz, eyz
            Case=[(0,0.005,0,0,0,0),    (0,-0.001,0,0,0,0),    (0,0,0,0.005,0,0),    (0,-0.005,0,0.001,0,0)]
            create_nonLinearsweepedlastcases(Case[0],'caseEyyT'+str(Q))          #    Lag linear strain cases. Set boundary condition and create job.
            create_nonLinearsweepedlastcases(Case[1],'caseEyyC'+str(Q))          #    Lag linear strain cases. Set boundary condition and create job.
            create_nonLinearsweepedlastcases(Case[2],'caseExyS'+str(Q))          #    Lag linear strain cases. Set boundary condition and create job.
            create_nonLinearsweepedlastcases(Case[3],'caseExySC'+str(Q))          #    Lag linear strain cases. Set boundary condition and create job.

        else:
            execfile(GitHub + Abaqus + 'LinearAnalysis.py')
        print 'Reached end of Iteration'
        Mdb()


del NotDone