from random import *
from math import *
import numpy as np
from multiprocessing import cpu_count

numCpus = cpu_count()

print '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\nMultiscale modelling on microscale  \nnumCpus = ',numCpus

#RVEmodell   SMA
def lagreparametere(Q):
    g = open(parameterpath, "w")
    g.write(str(Q) + '\t' + str(r) + '\t' + str(nf) + '\t' + str(Vf) + '\t' + str(wiggle) + '\t' + coordpath + '\t' + str(iterasjonsgrense) + '\t' + str(rtol) + '\t' +str(gtol)+ '\t' +str(dL)) # til fiber modellering
    g.close()

def hentePopulation(coordpath):
    #Les fiber matrix populasjon
    xy=list()
    f = open(coordpath,'r')
    tekst = f.read()
    f.close()
    lines = tekst.split('\n')
    #lagre koordinater til stottefil
    for line in lines:
        data = line.split('\t')
        a = float(data[0])
        b = float(data[1])
        xy.append([a,b])
    print 'Antall fiber = ',int(nf),'\tAntall fiberkoordinater = '+str(len(xy))+'\n'
    print '\n \n',xy,'\n \n'
    return xy
#Abaqus


def createModel(modelName,xydata,L,rf,nf, meshsize):
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
    Mdb()  #reset
    model = mdb.Model(name=modelName, modelType=STANDARD_EXPLICIT)  # Lag model
    del mdb.models['Model-1']  # Slett standard model
    mod = mdb.models[modelName]

    dx=L/2.0
    dy=L/2.0
    #Lag sketch
    s1 = model.ConstrainedSketch(name='__profile__',sheetSize=2*L)
    s1.setPrimaryObject(option=STANDALONE)

    #Tegne Firkant
    s1.Line(point1=(-dx, -dy), point2=(dx, -dy))
    s1.Line(point1=(dx, -dy), point2=(dx, dy))
    s1.Line(point1=(dx,dy), point2=(-dx,dy))
    s1.Line(point1=(-dx,dy), point2=(-dx,-dy))
    p = mod.Part(name='Part-1', dimensionality=THREE_D,
        type=DEFORMABLE_BODY)
    p = model.parts['Part-1']
    p.BaseShell(sketch=s1)

    s1.unsetPrimaryObject()
    del mod.sketches['__profile__']
    if not nf == 0:
        f1, e, = p.faces, p.edges
        t = p.MakeSketchTransform(sketchPlane=f1.findAt(coordinates=(0.0,
                                                                     0.0, 0.0), normal=(0.0, 0.0, 1.0)),
                                  sketchUpEdge=e.findAt(
                                      coordinates=(dx, 0.0, 0.0)), sketchPlaneSide=SIDE1, origin=(0.0,
                                                                                                  0.0, 0.0))
        s1 = model.ConstrainedSketch(name='__profile__',
                                     sheetSize=2*L, gridSpacing=L / 20.0, transform=t)
        s1.setPrimaryObject(option=SUPERIMPOSE)
        p.projectReferencesOntoSketch(sketch=s1, filter=COPLANAR_EDGES)

        rcos45 = rf * cos(45.0 * pi / 180.0)
        for data in xydata:
            x = data[0]
            y = data[1]
            done = 0
            if done == 0 and x >= dx:
                s1.CircleByCenterPerimeter(center=(x, y), point1=(x + rf, y))
                done = 1
            if done == 0 and x <= -dx:
                s1.CircleByCenterPerimeter(center=(x, y), point1=(x - rf, y))
                done = 1
            if done == 0 and y >= dx:
                s1.CircleByCenterPerimeter(center=(x, y), point1=(x, y + rf))
                done = 1
            if done == 0 and y <= -dx:
                s1.CircleByCenterPerimeter(center=(x, y), point1=(x, y - rf))
                done = 1

            if done == 0 and x >= 0 and y >= 0:
                s1.CircleByCenterPerimeter(center=(x, y), point1=(x - rcos45, y - rcos45))
                done = 1
            if done == 0 and x >= 0 and y <= 0:
                s1.CircleByCenterPerimeter(center=(x, y), point1=(x - rcos45, y + rcos45))
                done = 1
            if done == 0 and x <= 0 and y <= 0:
                s1.CircleByCenterPerimeter(center=(x, y), point1=(x + rcos45, y + rcos45))
                done = 1
            if done == 0 and x <= 0 and y >= 0:
                s1.CircleByCenterPerimeter(center=(x, y), point1=(x + rcos45, y - rcos45))
                done = 1

        # Create partioned planar shell from sketch
        f = p.faces
        pickedFaces = f.findAt(((0.0, 0.0, 0.0),))
        e1, d2 = p.edges, p.datums
        p.PartitionFaceBySketch(sketchUpEdge=e1.findAt(coordinates=(dx, 0.0,
                                                                    0.0)), faces=pickedFaces, sketch=s1)
        s1.unsetPrimaryObject()
        del model.sketches['__profile__'], f, pickedFaces, e1, d2, f1, e, t
        del s1, model
        #Partioned planar shell

        # mesh

        p = mod.parts['Part-1']
        p.seedPart(size=meshsize, deviationFactor=0.1, minSizeFactor=0.1)
        p = mod.parts['Part-1']
        p.generateMesh()
        p = mod.parts['Part-1']
        # meshed

        mdb.meshEditOptions.setValues(enableUndo=True, maxUndoCacheElements=0.5)
        pickedElemFacesSourceSide = mod.parts['Part-1'].elementFaces
        vector = ((0.0, 0.0, 0.0), (0.0, 0.0, 2.0))
        p.generateBottomUpExtrudedMesh(elemFacesSourceSide=pickedElemFacesSourceSide,
                                       extrudeVector=vector, numberOfLayers=2)
        p = mod.parts['Part-1']
        p.PartFromMesh(name='Part-1-mesh-1', copySets=True)
        p = mod.parts['Part-1-mesh-1']
        n = p.nodes
        nodes = n.getByBoundingBox(-dL, -dL, -0.01, dL, dL, 0.01)
        p.deleteNode(nodes=nodes)

        # print 'Created extruded mesh part'
        # Debugging abaqus tool :)#del mdb.models['Model-1']
        # This is where the fibers are chosen and put together in set
        p = mod.parts['Part-1-mesh-1']
        p.Set(name='AllE', elements=p.elements)
        x = xydata[0][0]
        y = xydata[0][1]
        fiber = p.elements.getByBoundingCylinder((x, y, -10.0), (x, y, 10.0), r + 0.01)
        for i in range(1, len(xydata)):
            x = xydata[i][0]
            y = xydata[i][1]
            temp = p.elements.getByBoundingCylinder((x, y, -10.0), (x, y, 10.0), r + 0.01)
            fiber = fiber + temp
        p.Set(name='Fibers', elements=fiber)
        p.SetByBoolean(name='Matrix', sets=(p.sets['AllE'], p.sets['Fibers'],), operation=DIFFERENCE)

        mod.Material(name='glass')
        mod.materials['glass'].Elastic(table=((70000.0, 0.22),))
        mod.Material(name='resin')
        mod.materials['resin'].Elastic(table=((3500.0, 0.33),))
        mod.HomogeneousSolidSection(name='Fibers', material='glass',
                                                      thickness=None)
        mod.HomogeneousSolidSection(name='matrix', material='resin',
                                                      thickness=None)

        p = mod.parts['Part-1-mesh-1']
        region = p.sets['Fibers']
        p.SectionAssignment(region=region, sectionName='Fibers', offset=0.0,
                            offsetType=MIDDLE_SURFACE, offsetField='',
                            thicknessAssignment=FROM_SECTION)
        region = p.sets['Matrix']
        p.SectionAssignment(region=region, sectionName='matrix', offset=0.0,
                            offsetType=MIDDLE_SURFACE, offsetField='',
                            thicknessAssignment=FROM_SECTION)
        del x, y
    else:
        p.seedPart(size=meshsize, deviationFactor=0.1, minSizeFactor=0.1)
        p.generateMesh()
        mdb.meshEditOptions.setValues(enableUndo=True, maxUndoCacheElements=0.5)
        pickedElemFacesSourceSide = mod.parts['Part-1'].elementFaces
        vector = ((0.0, 0.0, 0.0), (0.0, 0.0, 2.0))
        p.generateBottomUpExtrudedMesh(elemFacesSourceSide=pickedElemFacesSourceSide,
                                       extrudeVector=vector, numberOfLayers=2)
        p.PartFromMesh(name='Part-1-mesh-1', copySets=True)
        # extruded mesh and make orphan mesh
        p = mod.parts['Part-1-mesh-1']
        n = p.nodes
        nodes = n.getByBoundingBox(-dL, -dL, -0.01, dL, dL, 0.01)
        p.deleteNode(nodes=nodes)
        # delete shell nodes
        p.Set(name='AllE', elements=p.elements)
        mod.Material(name='resin')
        mod.materials['resin'].Elastic(table=((3500.0, 0.33),))
        mod.HomogeneousSolidSection(name='Matrix', material='resin', thickness=None)
        region = p.sets['AllE']
        p.SectionAssignment(region=region, sectionName='Matrix', offset=0.0,
                            offsetType=MIDDLE_SURFACE, offsetField='',
                            thicknessAssignment=FROM_SECTION)
    del mod.parts['Part-1'], p, n, mod, region
    print '\nModel created, meshed and assigned properties'

def createCEq(dL,modelName,instanceName):
    mod = mdb.models[modelName]
    a = mod.rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    p = mdb.models[modelName].parts['Part-1-mesh-1']
    a.Instance(name=instanceName, part=p, dependent=ON)

    a.translate(instanceList=(instanceName, ), vector=(0.0, 0.0, -1.0))

    a.rotate(instanceList=(instanceName, ), axisPoint=(0.0, 0.0, 0.0),
        axisDirection=(0.0, 1.0, 0.0), angle=90.0)
    tol = 0.01


    allNodes = a.instances[instanceName].nodes

    # Finding the dimensions
    xmax, ymax, zmax, xmin, ymin, zmin = 1.0, dL/2, dL/2, 0.0, -dL/2, -dL/2
    # Debugging abaqus tool :)
    #del mdb.models['Model-1']
    for n in allNodes:
        x, y, z = n.coordinates[0], n.coordinates[1], n.coordinates[2]
        xmax = max(xmax, x)
        ymax = max(ymax, y)
        zmax = max(zmax, z)
        xmin = min(xmin, x)
        ymin = min(ymin, y)
        zmin = min(zmin, z)
    #print xmax, ymax, zmax, xmin, ymin, zmin

    # Creating reference point

    a.ReferencePoint(point=( xmin - 0.2 * (zmax - zmin),0.0,  0.0))
    refPoints = (a.referencePoints[a.features['RP-1'].id],)
    a.Set(referencePoints=refPoints, name='RPX')

    a.ReferencePoint(point=(0.0, ymin - 0.2 * (ymax - ymin), 0.0))
    refPoints = (a.referencePoints[a.features['RP-2'].id],)
    a.Set(referencePoints=refPoints, name='RPY')

    a.ReferencePoint(point=(0.0, 0.0,zmin - 0.2 * (zmax - zmin)))
    refPoints = (a.referencePoints[a.features['RP-3'].id],)
    a.Set(referencePoints=refPoints, name='RPZ')

    # CE between x-normal surfaces:

    nodesXa = allNodes.getByBoundingBox(xmin - tol, ymin - tol, zmin - tol, xmin + tol, ymax + tol, zmax + tol)
    nodesXb = allNodes.getByBoundingBox(xmax - tol, ymin - tol, zmin - tol, xmax + tol, ymax + tol, zmax + tol)

    counter = 0

    for n in nodesXa:
        name1 = "Xa%i" % (counter)
        nodes1 = nodesXa[counter:counter + 1]
        a.Set(nodes=nodes1, name=name1)
        x, y, z = n.coordinates[0], n.coordinates[1], n.coordinates[2]
        name2 = "Xb%i" % (counter)
        nodes2 = nodesXb.getByBoundingBox(x + (xmax - xmin) - tol, y - tol, z - tol, x + (xmax - xmin) + tol, y + tol,
                                          z + tol)
        a.Set(nodes=nodes2, name=name2)

        mod.Equation(name="Cq11x%i" % (counter),
                     terms=((1.0, name2, 1), (-1.0, name1, 1), (-(xmax - xmin), 'RPX', 1),))  # 11
        mod.Equation(name="Cq21x%i" % (counter),
                     terms=((1.0, name2, 2), (-1.0, name1, 2), (-(xmax - xmin) / 2, 'RPX', 2),))  # 21
        mod.Equation(name="Cq31x%i" % (counter),
                     terms=((1.0, name2, 3), (-1.0, name1, 3), (-(xmax - xmin) / 2, 'RPX', 3),))  # 31

        counter = counter + 1

        # CE between y-normal surfaces
    # Note: excluding the nodes at xmax:

    nodesYa = allNodes.getByBoundingBox(xmin - tol, ymin - tol, zmin - tol, xmax - tol, ymin + tol, zmax + tol)
    nodesYb = allNodes.getByBoundingBox(xmin - tol, ymax - tol, zmin - tol, xmax - tol, ymax + tol, zmax + tol)

    counter = 0

    for n in nodesYa:
        name1 = "Ya%i" % (counter)
        nodes1 = nodesYa[counter:counter + 1]
        a.Set(nodes=nodes1, name=name1)
        x, y, z = n.coordinates[0], n.coordinates[1], n.coordinates[2]
        name2 = "Yb%i" % (counter)
        nodes2 = nodesYb.getByBoundingBox(x - tol, y + (ymax - ymin) - tol, z - tol, x + tol, y + (ymax - ymin) + tol,
                                          z + tol)
        a.Set(nodes=nodes2, name=name2)

        mod.Equation(name="Cq12y%i" % (counter),
                     terms=((1.0, name2, 1), (-1.0, name1, 1), (-(ymax - ymin) / 2, 'RPY', 1),))  # 12
        mod.Equation(name="Cq22y%i" % (counter),
                     terms=((1.0, name2, 2), (-1.0, name1, 2), (-(ymax - ymin), 'RPY', 2),))  # 22
        mod.Equation(name="Cq32y%i" % (counter),
                     terms=((1.0, name2, 3), (-1.0, name1, 3), (-(ymax - ymin) / 2, 'RPY', 3),))  # 32

        counter = counter + 1

        # CE between z-normal surfaces
    # Note: excluding the nodes at xmax and ymax :

    nodesZa = allNodes.getByBoundingBox(xmin - tol, ymin - tol, zmin - tol, xmax - tol, ymax - tol, zmin + tol)
    nodesZb = allNodes.getByBoundingBox(xmin - tol, ymin - tol, zmax - tol, xmax - tol, ymax - tol, zmax + tol)

    counter = 0

    for n in nodesZa:
        name1 = "Za%i" % (counter)
        nodes1 = nodesZa[counter:counter + 1]
        a.Set(nodes=nodes1, name=name1)
        x, y, z = n.coordinates[0], n.coordinates[1], n.coordinates[2]
        name2 = "Zb%i" % (counter)
        nodes2 = nodesZb.getByBoundingBox(x - tol, y - tol, z + (zmax - zmin) - tol, x + tol, y + tol,
                                          z + (zmax - zmin) + tol)
        a.Set(nodes=nodes2, name=name2)

        mod.Equation(name="Cq13z%i" % (counter),
                     terms=((1.0, name2, 1), (-1.0, name1, 1), (-(zmax - zmin) / 2, 'RPZ', 1),))  # 13
        mod.Equation(name="Cq23z%i" % (counter),
                     terms=((1.0, name2, 2), (-1.0, name1, 2), (-(zmax - zmin) / 2, 'RPZ', 2),))  # 23
        mod.Equation(name="Cq33z%i" % (counter),
                     terms=((1.0, name2, 3), (-1.0, name1, 3), (-(zmax - zmin), 'RPZ', 3),))  # 33

        counter = counter + 1
    print 'Constraint equ. applied'

def run_Job(Jobe, modelName):
    mdb.Job(name=Jobe, model=modelName, description='', type=ANALYSIS,
            atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90,
            memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True,
            explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF,
            modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='',
            scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=numCpus,
            numDomains=numCpus, numGPUs=1000)
"""
    mdb.jobs[Job].submit(consistencyChecking=OFF)
    mdb.jobs[Job].waitForCompletion()
    """

def create_unitstrainslastcases(stepName):
    id = np.identity(6)  # Identity matrix for normalised load cases.'Exx','Eyy','Ezz','Exy','Exz','Eyz'
    mod = mdb.models[modelName]
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

        run_Job(Enhetstoyinger[i],modelName)
        del exx, eyy, ezz, exy, exz, eyz

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
            sag[k]= sag[k]/(1*(dL)**2) #Volume
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
    return inverse

def sweep_sig2_sig3(Compliancematrix,sweepresolution):
    sweep=list()
    x= np.arange(0,2*pi,sweepresolution)

    print '\nStrains from stress sweep \n',
    print  x,'\n'
    for d in range(0, len(x)):
        sig2 = cos(x[d])
        sig3 = sin(x[d])
        a=np.dot([0,sig2,sig3,0,0,0],Compliancematrix)
        a = a.tolist()
        print a, '\n'
        sweep.append(a)

    return sweep

def create_sweepedlastcases(stepName,difstpNm,sweep, cases, modelName,workpath):

    mod = mdb.models[modelName]
    a = mod.rootAssembly
    mod.fieldOutputRequests['F-Output-1'].setValues(variables=('S', 'MISES', 'E', 'U', 'ELEDEN'))
    mod.steps.changeKey(fromName=stepName, toName=difstpNm)
    print '\nComputing strains for normalized load sweep'
    #Lagring av output data base filer .odb
    for lol in range(0,cases):
        Jobw =Sweeptoyinger[lol]
        print '\nLoad at'+str(360*lol/cases)+'deg'
        exx, eyy, ezz, exy, exz, eyz = sweep[lol]
        mod.boundaryConditions['BCX'].setValues(u1=exx, u2=exy, u3=exz)
        mod.boundaryConditions['BCZ'].setValues(u1=exy, u2=eyy, u3=eyz)
        mod.boundaryConditions['BCY'].setValues(u1=exz, u2=eyz, u3=ezz)
        run_Job(Jobw, modelName)
    print 'Calculated '+str(cases)+' cases'
    del a,a

def Extract_parameterenvelopes():
    odb = session.openOdb(workpath + Job + '.odb')
    # instance = odb.rootAssembly.instances[
    elset = odb.rootAssembly.instances[instanceName].elementSets['MATRIX']
    elset_nodes = set()

    for element in elset.elements:
        elset_nodes.update(element.connectivity)
    odb.close()

"""$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"""
"""              ALT OVER ER FUNKSJONER           """

"""Utgangspunkt variabler"""

Vf = 0.6
nf = 4
r = 1.0  # radiusen paa fiberne er satt til aa vaere uniforme, dette kan endres med en liste og random funksjon med data om faktisk variasjon i fibertype. Kommer det til aa gjore noe forskjell?
n = 1  # sweep variabel 1 naa = antall random seed(n)
meshsize = r * 0.3
sweepcases = 4

"""Andre variabler"""
if 1:
    #Er RVE tomt?
    if nf ==0 or Vf==0: # Fiberfri RVE
        nf=0
        Vf=0
        dL = 10
    else:
        dL = ((nf * pi * r ** 2) / (Vf)) ** 0.5 # RVE storrelsen er satt til aa vaere relativ av nf og V

    """  RVE_Modelleringsparametere  """
    wiggle = random()*r       # Omplasseringsgrenser for fiberomplassering
    iterasjonsgrense = 10000  # max antall plasseringsforsok per fiber

    #Toleranser
    rtol = 0.025  * r    #mellomfiber
    gtol = r * 0.025    #dodsone klaring

    #Parametere for dodzonegrense
    ytredodgrense = r+gtol
    indredodgrense= r-gtol

    """Tekstfiler"""
    parameterpath = 'C:/Multiscale-Modeling/Parametere.txt'
    coordpath = 'C:/Multiscale-Modeling/coordst.txt'
    lagrestiffpath = 'C:/Multiscale-Modeling/Stiffness.txt'
    workpath = 'C:/Users/Rockv/Desktop/Temp/'


    """   ABAQUS   """
    modelName = 'Model-A'
    instanceName = 'PART-1-MESH-1-1'
    stepName = 'Enhetstoyninger'
    difstpNm = 'Lasttoyinger'

    #Composite unit stresses

    sweepresolution = 2*pi / sweepcases #stepsize

    print '\nQ\tr\tnf\tVf\twiggle\t\tcoordpath\tLoops\trtol\tgtoL\tdL'


#Micromodellering av (n) kompositt

for Q in range(0,n):
    from abaqus import *
    from abaqusConstants import *
    from odbAccess import *

    # Q er randomfunksjonensnokkelen
    seed(Q)

    #Abaqus navn
    Enhetstoyinger = ['Exx' + str(nf) + '_' + str(Q), 'Eyy' + str(nf) + '_' + str(Q), 'Ezz' + str(nf) + '_' + str(Q),
              'Exy' + str(nf) + '_' + str(Q), 'Exz' + str(nf) + '_' + str(Q),
              'Eyz' + str(nf) + '_' + str(Q)]  # Enhetstoyingene fra 0 til 5. Alle 6

    Sweeptoyinger = [''] * sweepcases
    for g in range(0,sweepcases):
        Sweeptoyinger[g] = 'Sweep_strain_at'+str(int(g*180*sweepresolution/pi))+'__'+str(int(Q))


    #Lagre parametere til stottefiler

    lagreparametere(Q)


    """Prosess"""

    #Maa vi ha fiber populasjon?
    if not (nf==0):
        # create a random population
        execfile('D:/GenerereFiberPopTilFil.py')                                        #modellereRVEsnitt()
        # hente fibercoordinater
        xydata= hentePopulation(coordpath)
    else:
        xydata = None
    
    # Lage Abaqus strain-cases
    # Build_Enviroment()
    createModel(modelName, xydata, dL, r, nf, meshsize)
    createCEq(dL, modelName, instanceName)
    create_unitstrainslastcases(stepName)

    #Faa ut stiffnessmatrix

    Stiffmatrix=get_stiffness()

    #Calculations
    Compliancematrix = get_compliance(Stiffmatrix)
    sweepstrains = sweep_sig2_sig3(Compliancematrix,sweepresolution)

    # Abaqus Sweep Cases
    create_sweepedlastcases(stepName,difstpNm,sweepstrains, sweepcases, modelName,workpath)
    #collect parameters()
    # Extract_parameterenvelopes()
    print 'torke'
    #Mdb()
    # stats
    #if not nf <= 1:
    #    fiberdist, avgfdist = fiberdistances(dL, xydata)
    #analyticalfiberdist = 0.521


    #session.mdbData.summary()
    #
    #o1 = session.openOdbs(names=(workpath+Toying[0]+'.odb', workpath+Toying[1]+'.odb',
    #                             workpath+Toying[2]+'.odb', workpath+Toying[3]+'.odb', workpath+Toying[4]+'.odb',
    #                             workpath+Toying[5]+'.odb'))
    #session.viewports['Viewport: 1'].setValues(displayedObject=o1)
    #Preform konvergence tests
