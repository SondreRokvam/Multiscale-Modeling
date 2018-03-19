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
    if not noFiber and Interface:
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
    print 'Imported to Assembly, Reference points created and constraint equ. applied'
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

# Linear
def create_Linearunitstrainslastcases():
    id = np.identity(6)  # Identity matrix for normalised load cases.'Exx','Eyy','Ezz','Exy','Exz','Eyz'
    a = mod.rootAssembly
    #Create step Linear step
    mod.StaticStep(name=stepName, previous='Initial')
    #Request outputs
    mod.fieldOutputRequests['F-Output-1'].setValues(variables=('S', 'EVOL','U'))
    #Run the simulations to create stiffnessmatrix
    print '\nComputing stresses for normalized strains'
    for i in range(0,6):#   arg:   +   ,len(id)+1

        #Laste inn toyningscase
        exx, eyy, ezz, exy, exz, eyz = id[i]
        mod.DisplacementBC(name='BCX', createStepName=stepName,
                           region=a.sets['RPX'], u1=exx, u2=exy, u3=exz, ur1=UNSET, ur2=UNSET, ur3=UNSET,
                           amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)

        mod.DisplacementBC(name='BCY', createStepName=stepName,
                           region=a.sets['RPY'], u1=exy, u2=eyy, u3=eyz, ur1=UNSET, ur2=UNSET, ur3=UNSET,
                           amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)

        mod.DisplacementBC(name='BCZ', createStepName=stepName,
                           region=a.sets['RPZ'], u1=exz, u2=eyz, u3=ezz, ur1=UNSET, ur2=UNSET, ur3=UNSET,
                           amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)
        print Enhetstoyinger[i]
        run_Job(Enhetstoyinger[i],modelName)
        del exx, eyy, ezz, exy, exz, eyz
def create_Linearsweepedlastcases(sweep):
    mod = mdb.models[modelName]
    a = mod.rootAssembly
    mod.fieldOutputRequests['F-Output-1'].setValues(variables=('S', 'MISES', 'E', 'U', 'ELEDEN'))
    mod.steps.changeKey(fromName=stepName, toName=difstpNm)
    print '\nComputing strains for normalized load sweep'
    #Lagring av output data base filer .odb
    for case in range(0,sweepcases):

        print '\nLoad at'+str(360*case/sweepcases)+'deg'
        exx, eyy, ezz, exy, exz, eyz = sweep[case]
        mod.boundaryConditions['BCX'].setValues(u1=exx, u2=exy, u3=exz)
        mod.boundaryConditions['BCY'].setValues(u1=exy, u2=eyy, u3=eyz)
        mod.boundaryConditions['BCZ'].setValues(u1=exz, u2=eyz, u3=ezz)
        Jobw = Sweeptoyinger[case]
        run_Job(Jobw, modelName)
    del a, Jobw, case
def get_stiffness():
    stiffmatrix = []
    for i in range(0,6):
        path = workpath + Enhetstoyinger[i]
        odb = session.openOdb(path+'.odb')
        instance = odb.rootAssembly.instances[instanceName]

        sag=[0.0] * 6
        for j in range(0,len(instance.elements)):
            v = odb.steps[stepName].frames[-1].fieldOutputs['S'].getSubset(position=CENTROID)
            elvol = odb.steps[stepName].frames[-1].fieldOutputs['EVOL']
            for p in range(0,6):
                sag[p] = sag[p]+v.values[j].data[p]*elvol.values[j].data
        odb.close()
        for k in range(0,6):
            sag[k]= sag[k]/(tykkelse*(dL)**2) #Volume
        stiffmatrix.append(sag)
    print '\n'
    g = open(lagrestiffpath, "w")
    print '\nStiffnessmatrix stored\n'
    for a in range(0, 6):
        g.write(str(float(stiffmatrix[0][a]))+'\t'+str(float(stiffmatrix[1][a]))+'\t'+str(float(stiffmatrix[2][a]))+'\t'+str(float(stiffmatrix[3][a]))+'\t'+str(float(stiffmatrix[4][a]))+'\t'+str(float(stiffmatrix[5][a])))
        if not a==5:
            g.write('\t\t')
        print '%7f \t %7f \t %7f \t %7f \t %7f \t %7f' % (stiffmatrix[0][a], stiffmatrix[1][a], stiffmatrix[2][a], stiffmatrix[3][a], stiffmatrix[4][a], stiffmatrix[5][a])
    g.write('\n')
    g.close()
    return stiffmatrix
def get_compliance(Stiffmatrix):
    print '\nCompliancematrix found'
    try:
        inverse = np.linalg.inv(Stiffmatrix)
    except np.linalg.LinAlgError:
        # Not invertible. Skip this one.
        print 'ERROR in inverting with numpy'
        pass    #intended break
    for a in range(0, 6):
        print inverse[0][a],'\t', inverse[1][a],'\t', inverse[2][a],'\t', inverse[3][a],'\t',inverse[4][a],'\t', inverse[5][a]
    inverse = inverse.tolist()
    return inverse
def get_sweepstrains_sig2_sig3(Compliancematrix,sweepresolution):
    sweep=list()
    x= np.arange(0,2*pi,sweepresolution)
    x =x.tolist()
    print '\nStrains from stress sweep at angle \n',
    print  x,'\n'
    for d in range(0, len(x)):
        sig2 = cos(x[d])
        sig3 = sin(x[d])
        a=np.dot(Compliancematrix,[0,sig2,sig3,0,0,0])

        a = a.tolist()
        print a
        sweep.append(a)
    return sweep

# nonLinear
def create_nonLinearsweepedlastcases(Strain,bob):
    mod = mdb.models[modelName]
    mod.StaticStep(name=difstpNm, previous='Initial', nlgeom=ON)
    a = mod.rootAssembly
    mod.fieldOutputRequests['F-Output-1'].setValues(variables=('DAMAGEC', 'DAMAGET', 'LE', 'MISES', 'PE', 'PEEQ', 'RT', 'S', 'SDEG','STATUS', 'STATUSXFEM', 'U'), timeInterval=0.05)
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
        region = a.sets['Xb0']
        mod.DisplacementBC(name='BC-4', createStepName='Initial',
                                             region=region, u1=SET, u2=SET, u3=SET, ur1=UNSET, ur2=UNSET, ur3=UNSET,
                                             amplitude=UNSET, distributionType=UNIFORM, fieldName='',
                                             localCsys=None)
        """
        a = mod.rootAssembly
        n1 = a.instances[instanceName].nodes
        nodes1 = n1.getByBoundingCylinder((-dL, -dL, 0 - tol), (-dL, -dL, tol), tykkelse/2)
        navn = 'hjorne1'
        a.Set(nodes=nodes1, name=navn)
        mdb.models['Model-A'].DisplacementBC(name='BC-4', createStepName='Initial', 
            region=a.sets[navn], u1=SET, u2=SET, u3=SET, ur1=UNSET, ur2=UNSET, ur3=UNSET, 
            amplitude=UNSET, distributionType=UNIFORM, fieldName='', 
            localCsys=None)
        
    
        nodes1 = n1.getByBoundingCylinder((+dL, -dL, 0 - tol), (+dL, -dL, tol), tykkelse/2)
        navn = 'hjorne2'
        a.Set(nodes=nodes1, name=navn)
        mdb.models['Model-A'].DisplacementBC(name='BC-5', createStepName='Initial', 
            region=a.sets[navn], u1=UNSET, u2=UNSET, u3=SET, ur1=UNSET, ur2=UNSET, 
            ur3=UNSET, amplitude=UNSET, distributionType=UNIFORM, fieldName='', 
            localCsys=None)
    
        nodes1 = n1.getByBoundingCylinder((+dL, +dL, 0 - tol), (+dL, +dL, tol), tykkelse/2)
        navn = 'hjorne3'
        a.Set(nodes=nodes1, name=navn)
        mdb.models['Model-A'].DisplacementBC(name='BC-6', createStepName='Initial', 
            region=a.sets[navn], u1=SET, u2=SET, u3=UNSET, ur1=UNSET, ur2=UNSET, 
            ur3=UNSET, amplitude=UNSET, distributionType=UNIFORM, fieldName='', 
        localCsys=None)
        """

        run_Job(bob+'lol', modelName)



"""$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"""
"""              GLOBALE VARIABLER               """
#Flag
Runjobs = 1                         # TRUE/FALSE Bestemmer om jobber skal kjores


nonLinearDeformation = 1               # TRUE/FALSE Linear eller nonlinear analyse?

noFiber = 0                         # TRUE/FALSE Overstyrer antall fiber til 0

Fibervariation = 1                      # TRUE/FALSE Skal fiber radius variere eller ikke?

Interface = 1                               # TRUE/FALSE Interface paa fibere?
Interfacetykkelse = 1                           # TRUE/FALSE 0 volum Interfaceelement  paa fibere?

"""Start"""
#Forste sweepvariabel
Sample=[25]
#Sample=[0, 5, 10, 25,50]
for m in range(0,len(Sample)):
    # Se variabler
    if True:                     # For aa kunne kollapse variabler
        # Sweep variabler: itererer random seeds fra 0 til n
        n = 1
        sweepcases = 1      # Opplosning paa stress sweeps vinkler

        #  RVE Modelleringsvariabler
        nf=Sample[m]
        Vf = 0.6
        RVEt =   0.01         # Proporsjonal forskjell mellom bredde/hoyde og RVE tykkelse

        # Fibere
        rmean = 8.7096                # Gjennomsnittradius. Om ikke fibervariasjon saa settes fibere til aa vaere uniform.
        Rstdiv = 0.6374                 # Standard avvik fra gjennomsnittsradius.

        #Toleranser og klaringer
        Rclearing  = 0.025                   # Prosent avstand av r klaring mellom fibere og fra kanter og sider
        rinterface = 0.005                    # Prosent avstand av r paa interfacetykkelse ved modellering
        tol = rinterface*0.4                  # Toleranse som er godt mindre en minste modelleringsvariabel

        # Meshsize fra Interface resolution paa fiberomkrets
        FiberSirkelResolution = 50                              #Standard meshsixer er 2*pi/FiberSirkelResolution

        #Se instilliger
        if True:                     # For aa kunne kollapse variabler
            # Fiberfri RVE
            if nf == 0 or Vf == 0 or noFiber:
                nf = 0
                Vf = 0
                dL = rmean*2
                noFiber = 1
            if not nf == 0:                              # RVE dL er relativ av nf, rmean og V
                dL = ((nf * pi * rmean ** 2) / (Vf)) ** 0.5
            #RVE tykkelse
            tykkelse = float(RVEt * dL)
            # Meshresolution
            meshsize = rmean * 2 * pi / FiberSirkelResolution
            # iterasjonsgrense i Fiberutplassering
            iterasjonsgrense = 10000
            # stepsize paa Stress sweep
            sweepresolution = 2 * pi / sweepcases
            # Fiber detaljier
            r = rmean
            gtol = Rclearing * r  # Dodsone klaring toleranse
            ytredodgrense = r + gtol  # Dodzone avstand, lengst fra kantene
            indredodgrense = r - gtol  # Dodzone avstand, naermest kantene

            if Interfacetykkelse:
                print 'Aspect ratio for Interface elements = ' + str(round(meshsize / (rinterface * rmean), 2)) + '    Interface elements thickness = ' + str(float(rinterface * rmean))
        # Se tekstfiler for databehandling
        if True:                     # For aa kunne kollapse variabler
            GitHub  = 'C:/Multiscale-Modeling/'
            workpath =  'C:/Temp/'

            Tekstfiler, Abaqus = 'textfiles/', 'Abaqus_steg/'

            parameterpath = GitHub + 'Parametere.txt'  # Skrives ned for chaining  til ett annet script
            coordpath = GitHub + 'coordst.txt'  # Hentes fra genererefiberPop chaining  til ett annet script

            lagrestiffpath = GitHub + 'Stiffness.txt'  # Skrives ned statistikk til ett annet script
            Envelope = GitHub + Tekstfiler + 'envelope'  # Parameteravhengig - Spesifikt navn legges til i funksjonen
        # Se ABAQUS navn
        if True:                     # For aa kunne kollapse variabler
            modelName = 'Model-A'
            partName, meshPartName = 'Part-1', 'Part-1-mesh-1'

            instanceName = 'PART-1-MESH-1-1'
            stepName, difstpNm = 'Enhetstoyninger', 'Lasttoyinger'

    """RVE MODELLERINGS LOOP"""
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

            #RVE og n relative ABAQUS Jobb navn
            Enhetstoyinger = ['Exx' + str(nf) + '_' + str(Q), 'Eyy' + str(nf) + '_' + str(Q), 'Ezz' + str(nf) + '_' + str(Q),
                              'Exy' + str(nf) + '_' + str(Q), 'Exz' + str(nf) + '_' + str(Q), 'Eyz' + str(nf) + '_' + str(Q)]
                                                        # Enhetstoyingene fra 0 til 5. Alle 6
            Sweeptoyinger = [''] * sweepcases
            for g in range(0,sweepcases):
                Sweeptoyinger[g] = ('Sweep_strain'+ str(nf) + '_'+str(int(g*180*sweepresolution/pi))+'__'+str(int(Q)))

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
            Case=[(0,0.001,0,0,0,0),    (0,-0.001,0,0,0,0),    (0,0,0,0.001,0,0),    (0,-0.001,0,0.001,0,0)]
            create_nonLinearsweepedlastcases(Case[0],'caseEyyT')          #    Lag linear strain cases. Set boundary condition and create job.
            create_nonLinearsweepedlastcases(Case[1],'caseEyyC')          #    Lag linear strain cases. Set boundary condition and create job.
            create_nonLinearsweepedlastcases(Case[2],'caseExyS')          #    Lag linear strain cases. Set boundary condition and create job.
            create_nonLinearsweepedlastcases(Case[3],'caseExySC')          #    Lag linear strain cases. Set boundary condition and create job.

        else:
            del noDoLinearWork
            create_Linearunitstrainslastcases()                                             # Lag linear strain cases. Set boundary condition and create job.
            Stiffmatrix = get_stiffness()                                                   # Faa ut stiffnessmatrix

            Compliancematrix = get_compliance(Stiffmatrix)                                  # Inverter til compliance materix
            sweepstrains = get_sweepstrains_sig2_sig3(Compliancematrix, sweepresolution)    # Finne strains for sweep stress case
            create_Linearsweepedlastcases(sweepstrains)                                     # Lag linear sweep strain cases. Set boundary condition and create job.

        print 'Reached end of Iteration'
        del NotDone

