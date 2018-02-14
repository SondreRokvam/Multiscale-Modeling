from random import *
from math import *
import numpy as np
from multiprocessing import cpu_count

numCpus = cpu_count()/2

print '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\nMultiscale modelling on microscale  \nHalve numCpus = ',numCpus

#RVEmodell
def lagreparametere(Q):
    g = open(parameterpath, "w")
    print '\nQ\tr\tnf\tVf\twiggle\t\tcoordpath\t\t\t\tLoops\trtol\tgtoL\tdL'
    g.write('Q' + '\t' + 'r' + '\t' + 'nf' + '\t' + 'Vf' + '\t' + 'wiggle' + '\t' + 'coordpath' + '\t' + 'iterasjonsgrense' + '\t' + 'rtol' + '\t' + 'gtol' + '\t' + 'dL'+'\n'+
            str(Q) + '\t' + str(r) + '\t' + str(nf) + '\t' + str(Vf) + '\t' + str(wiggle) + '\t' + coordpath + '\t' + str(iterasjonsgrense) + '\t' + str(rtol) + '\t' +str(gtol)+ '\t' +str(dL)) # til fiber modellering
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
    print 'Antall fiber = ',int(nf),'\tAntall fiberkoordinater = '+str(len(xy))
    return xy

#Abaqus

def createModel(xydata):
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
    #

    model = mdb.Model(name=modelName, modelType=STANDARD_EXPLICIT)  # Lag model
    del mdb.models['Model-1']                                       # Slett standard model


    mod = mdb.models[modelName]

    dx=dL/2.0
    dy=dL/2.0
    #Lag sketch
    s1 = model.ConstrainedSketch(name='__profile__',sheetSize=2*dL)
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
    #del mod.sketches['__profile__']
    del bon
    if not nf == 0:
        f1, e, = p.faces, p.edges
        t = p.MakeSketchTransform(sketchPlane=f1.findAt(coordinates=(0.0,
                                                                     0.0, 0.0), normal=(0.0, 0.0, 1.0)),
                                  sketchUpEdge=e.findAt(
                                      coordinates=(dx, 0.0, 0.0)), sketchPlaneSide=SIDE1, origin=(0.0,
                                                                                                  0.0, 0.0))
        s1 = model.ConstrainedSketch(name='__profile__',
                                     sheetSize=2*dL, gridSpacing=dL / 25.0, transform=t)
        s1.setPrimaryObject(option=SUPERIMPOSE)
        p.projectReferencesOntoSketch(sketch=s1, filter=COPLANAR_EDGES)

        rcos45 = r * cos(45.0 * pi / 180.0)
        for data in xydata:
            x = data[0]
            y = data[1]
            done = 0
            if done == 0 and x >= dx:
                s1.CircleByCenterPerimeter(center=(x, y), point1=(x + r, y))
                done = 1
            if done == 0 and x <= -dx:
                s1.CircleByCenterPerimeter(center=(x, y), point1=(x - r, y))
                done = 1
            if done == 0 and y >= dx:
                s1.CircleByCenterPerimeter(center=(x, y), point1=(x, y + r))
                done = 1
            if done == 0 and y <= -dx:
                s1.CircleByCenterPerimeter(center=(x, y), point1=(x, y - r))
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
        #del model.sketches['__profile__'], f, pickedFaces, e1, d2, f1, e, t
        #del s1, model
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
        vector = ((0.0, 0.0, 0.0), (0.0, 0.0, 2*tykkelse))
        p.generateBottomUpExtrudedMesh(elemFacesSourceSide=pickedElemFacesSourceSide,
                                       extrudeVector=vector, numberOfLayers=2)
        p = mod.parts['Part-1']
        n = p.nodes
        nodes = n.getByBoundingBox(-dL, -dL, -0.01, dL, dL, 0.01)
        p.deleteNode(nodes=nodes)
        p.PartFromMesh(name='Part-1-mesh-1', copySets=True)
        # Created extruded mesh part

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
        vector = ((0.0, 0.0, 0.0), (0.0, 0.0, 2*tykkelse))
        p.generateBottomUpExtrudedMesh(elemFacesSourceSide=pickedElemFacesSourceSide,
                                       extrudeVector=vector, numberOfLayers=2)
        p = mod.parts['Part-1']
        n = p.nodes
        nodes = n.getByBoundingBox(-dL, -dL, -0.01, dL, dL, 0.01)
        p.deleteNode(nodes=nodes)
        # delete shell nodes
        p.PartFromMesh(name='Part-1-mesh-1', copySets=True)
        # extruded mesh and make orphan mesh

        p.Set(name='AllE', elements=p.elements)
        mod.Material(name='resin')
        mod.materials['resin'].Elastic(table=((3500.0, 0.33),))
        mod.HomogeneousSolidSection(name='Matrix', material='resin', thickness=None)
        region = p.sets['AllE']
        p.SectionAssignment(region=region, sectionName='Matrix', offset=0.0,
                            offsetType=MIDDLE_SURFACE, offsetField='',
                            thicknessAssignment=FROM_SECTION)
    #del mod.parts['Part-1'], p, n, mod, region
    print '\nModel created, meshed and assigned properties'

def createCEq():
    mod = mdb.models[modelName]
    a = mod.rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    p = mdb.models[modelName].parts['Part-1-mesh-1']
    a.Instance(name=instanceName, part=p, dependent=ON)

    # Flytte modellen til origo og sette x i fiberretning.
    a.translate(instanceList=(instanceName,), vector=(0.0, 0.0, -tykkelse))
    a.rotate(instanceList=(instanceName,), axisPoint=(0.0, 0.0, 0.0),
             axisDirection=(0.0, 1.0, 0.0), angle=90.0)
    tol = 0.01

    allNodes = a.instances[instanceName].nodes

    # Finding the dimensions
    xmax, ymax, zmax, xmin, ymin, zmin = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    for n in allNodes:
        x, y, z = n.coordinates[0], n.coordinates[1], n.coordinates[2]
        xmax = max(xmax, x)
        ymax = max(ymax, y)
        zmax = max(zmax, z)
        xmin = min(xmin, x)
        ymin = min(ymin, y)
        zmin = min(zmin, z)

    # Creating reference point

    a.ReferencePoint(point=(xmin - 0.2 * (xmax - xmin), 0.0, 0.0))
    refPoints = (a.referencePoints[a.features['RP-1'].id],)
    a.Set(referencePoints=refPoints, name='RPX')

    a.ReferencePoint(point=(0.0, ymin - 0.2 * (ymax - ymin), 0.0))
    refPoints = (a.referencePoints[a.features['RP-2'].id],)
    a.Set(referencePoints=refPoints, name='RPY')

    a.ReferencePoint(point=(0.0, 0.0, zmin - 0.2 * (zmax - zmin)))
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
    a=1
    #mdb.jobs[Jobe].submit(consistencyChecking=OFF)
    #mdb.jobs[Jobe].waitForCompletion()
    del a

def create_unitstrainslastcases():
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

def sweep_sig2_sig3(Compliancematrix,sweepresolution):
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
    print sweep
    return sweep

def create_sweepedlastcases(sweep):

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

    del a, mod, Jobw, case

def Extract_parameterdata():

    maxMisesStresses = list()
    minMisesStresses = list()

    maxnormstresses = list()
    minnormstresses = list()

    maxnormstrains = list()
    minnormstrains = list()

    maxsherstresses = list()
    maxsherstrains = list()

    print 'Computing stresses for ' + str(sweepcases) + ' sweep cases'
    for case in range(0,sweepcases):
        odb = session.openOdb(workpath + Sweeptoyinger[case] + '.odb')
        nodalStresses = odb.steps[difstpNm].frames[-1].fieldOutputs['S'].getSubset(position=ELEMENT_NODAL).values
        nodalStrains = odb.steps[difstpNm].frames[-1].fieldOutputs['E'].getSubset(position=ELEMENT_NODAL).values
        Mises = odb.steps[difstpNm].frames[-1].fieldOutputs['S'].getSubset(position=ELEMENT_NODAL).values
        if not nf==0:
            Matrix = odb.rootAssembly.instances[instanceName].elementSets['MATRIX']
            nodalStresses = odb.steps[difstpNm].frames[-1].fieldOutputs['S'].getSubset(position=ELEMENT_NODAL,
                                                                                       region=Matrix).values
            nodalStrains = odb.steps[difstpNm].frames[-1].fieldOutputs['E'].getSubset(position=ELEMENT_NODAL,
                                                                                      region=Matrix).values
            Mises = odb.steps[difstpNm].frames[-1].fieldOutputs['S'].getSubset(position=ELEMENT_NODAL,region=Matrix).values

        MisesStresses = list()
        normstresses = list()
        sherstresses = list()
        normstrains=list()
        sherstrains=list()

        for j in range(0,len(nodalStresses)):
            MisesStresses.append(float(Mises[j].mises))
            for p in range(0,3):
                normstresses.append(float(nodalStresses[j].data[p]))
                sherstresses.append(abs(float(nodalStresses[j].data[p+3])))
                normstrains.append(float(nodalStrains[j].data[p]))
                sherstrains.append(abs(float(nodalStrains[j].data[p+3])))
        odb.close()
        maxMisesStresses.append(float(max(MisesStresses)))
        minMisesStresses.append(float(min(MisesStresses)))

        maxnormstresses.append(float(max(normstresses)))
        minnormstresses.append(float(min(normstresses)))
        maxnormstrains.append(float(max(normstrains)))
        minnormstrains.append(float(min(normstrains)))

        maxsherstresses.append(max(sherstresses))
        maxsherstrains.append(max(sherstrains))
    g = open(Envelope, "w")
    for a in range(0, len(maxMisesStresses)):
        #                 1                              2                             3                             4                        5
        g.write(str(maxMisesStresses[a]) + '\t' + str(minMisesStresses[a]) + '\t' + str(maxnormstresses[a]) + '\t' + str(minnormstresses[a]) + '\t' + str(maxnormstrains[a])
                + '\t' + str(minnormstrains[a]) + '\t' + str(maxsherstresses[a]) + '\t' + str(maxsherstrains[a]))
        if not a ==len(maxMisesStresses)-1:
            g.write('\n')
    g.close()
    return


"""$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"""
"""              ALT OVER ER FUNKSJONER           """



#Variabler

Vf = 0
nf = 1
r = 1.0  # radiusene paa fiberne er naa satt til aa vaere uniforme, kan endres til liste med faktisk variasjon i diameter
n = 1  # sweep variabel 1 naa = antall random seed(n)
meshsize = r * 0.3
sweepcases = 16

tykkelse =0.1

#Andre variabler
if 1:
    #Er RVE tomt?
    if nf ==0 or Vf==0: # Fiberfri RVE
        nf=0
        Vf=0
        dL = 6

    else:
        dL = ((nf * pi * r ** 2) / (Vf)) ** 0.5 # RVE storrelsen er satt til aa vaere relativ av nf og V


    #RVE_Modelleringsparametere
    rtol = 0.025 * r        #Mellomfiber toleranse
    gtol = 0.025 * r        #Dodsone klaring toleranse

    ytredodgrense = r+gtol  #Dodzone avstand, lengst fra kantene
    indredodgrense= r-gtol  #Dodzone avstand, naermest kantene

    iterasjonsgrense =10000

    # Tekstfiler
    GitHub ='C:/Multiscale-Modeling/'
    Envelope = GitHub+'envelope.txt'
    parameterpath = GitHub+'Parametere.txt'
    coordpath = GitHub+'coordst.txt'
    lagrestiffpath = GitHub+'Stiffness.txt'
    workpath = 'C:/Users/Rockv/Desktop/Temp/'


    """   ABAQUS   """
    modelName = 'Model-A'
    instanceName = 'PART-1-MESH-1-1'
    stepName = 'Enhetstoyninger'
    difstpNm = 'Lasttoyinger'

    #Composite sweep stresses
    sweepresolution = 2*pi / sweepcases #stepsize


#
"""$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"""
"""              Micromodelleringsfunksjon av (n) kompositt           """
#execfile('C:\Multiscale-Modeling\Multiscalemethod_np.py')

for Q in range(0,n):
    from abaqus import *
    from abaqusConstants import *
    from odbAccess import *

    seed(Q)                                 # Q er randomfunksjonensnokkelen
    wiggle = random()*r                    # Omplasseringsgrenser for fiberomplassering
    
    #Abaqus navn
    Enhetstoyinger = ['Exx' + str(nf) + '_' + str(Q), 'Eyy' + str(nf) + '_' + str(Q), 'Ezz' + str(nf) + '_' + str(Q),
                      'Exy' + str(nf) + '_' + str(Q), 'Exz' + str(nf) + '_' + str(Q), 'Eyz' + str(nf) + '_' + str(Q)]
                        # Enhetstoyingene fra 0 til 5. Alle 6


    Sweeptoyinger = [''] * sweepcases
    for g in range(0,sweepcases):
        Sweeptoyinger[g] = ('Sweep_strain'+ str(nf) + '_'+str(int(g*180*sweepresolution/pi))+'__'+str(int(Q)))


    #Lagre parametere til stottefiler

    lagreparametere(Q)

    """Prosess"""

    xydata = None

    # Maa vi ha fiber populasjon?
    if not (nf==0):
        # create a random population
        execfile(GitHub+'GenerereFiberPopTilFil.py')                                        #modellereRVEsnitt()
        # hente fibercoordinater
        xydata= hentePopulation(coordpath)
    print '\n', xydata ,'\n\n'
    # Lage Abaqus strain-cases
    createModel( xydata)
    createCEq()
    create_unitstrainslastcases()

    #Faa ut stiffnessmatrix

    Stiffmatrix=get_stiffness()

    #Finne strains for sweep stress caser

    Compliancematrix = get_compliance(Stiffmatrix)
    sweepstrains = sweep_sig2_sig3(Compliancematrix,sweepresolution)

    # Abaqus Sweep Cases
    create_sweepedlastcases(sweepstrains)
    Extract_parameterdata()      #norm [0]       sher [1]


    print 'torke'

