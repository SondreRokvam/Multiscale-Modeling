from random import *
from math import *
import numpy as np
from multiprocessing import cpu_count
numCpus = cpu_count()/4
print ('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n'
       'Multiscale Modelling, Microscale  \n'
       'Allowed numCpus = ',numCpus)

"""                 FUNKSJONER                """
#RVEmodell
def lagreparametere(Q):
    g = open(parameterpath, "w")

    parametere=[Q,r,nf,Vf,wiggle,coordpath,iterasjonsgrense,rtol,gtol,dL]
    print parametere,'\nQ\tr\tnf\tVf\twiggle\t\tcoordpath\t\t\t\titerasjonsgrense\trtol\tgtoL\tdL'
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

    for line in lines:
        data = line.split('\t')
        a = float(data[0])  #   X
        b = float(data[1])  #   Y
        c = float(data[2])  #   R
        xy.append([a,b,c])  #   lagre til liste
    print 'Antall fiber = ',int(nf),'\tAntall fiberkoordinater = '+str(len(xy))
    return xy

#Abaqus operations
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

    model = mdb.Model(name=modelName, modelType=STANDARD_EXPLICIT)  # Lag model
    del mdb.models['Model-1']                                       # Slett standard model


    mod = mdb.models[modelName]

    dx=dL/2.0
    dy=dL/2.0
    #Lag sketch
    s1 = model.ConstrainedSketch(name='__profile__',sheetSize=2*dL)
    s1.setPrimaryObject(option=STANDALONE)

    #Tegne RVE sketch -Firkant
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

    if not nf == 0:                                                                                                     # If: Om ingen fiber? Uten fiber ingen interface
        f1, e = p.faces, p.edges
        t = p.MakeSketchTransform(sketchPlane=f1.findAt(coordinates=(0.0,0.0, 0.0), normal=(0.0, 0.0, 1.0)),
                                  sketchUpEdge=e.findAt(coordinates=(dx, 0.0, 0.0)), sketchPlaneSide=SIDE1, origin=(0.0,0.0, 0.0))
        s1 = model.ConstrainedSketch(name='__profile__', sheetSize=2*dL, gridSpacing=dL / 25.0, transform=t)
        s1.setPrimaryObject(option=SUPERIMPOSE)
        p.projectReferencesOntoSketch(sketch=s1, filter=COPLANAR_EDGES)

                                                                                                                            # Partionere og meshe RVE fibere med eller uten interface
        for data in xydata:     #Tegne inn fiber aa partionere
            x = data[0]
            y = data[1]
            r=rmean
            if Fibervariation:
                r=data[2]
            rcos45 = r * cos(45.0 * pi / 180.0)
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
        if Interface:       #Tegne inn fiber interfaces aa partionere
            for data in xydata:
                x = data[0]
                y = data[1]
                r=rmean
                if Fibervariation:
                    r=data[2]
                r=r*(1+rinterface)
                rcos45 = r * cos(45.0 * pi / 180.0)
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
            f = p.faces                                                                                                     # Create partioned planar shell from sketch
            pF = f.findAt(((0.0, 0.0, 0.0),))
            e1= p.edges
            p.PartitionFaceBySketch(sketchUpEdge=e1.findAt(coordinates=(dx, 0.0,0.0)), faces=pF, sketch=s1)        # Selve partioneringen
            s1.unsetPrimaryObject()                                                                              # Lag set for fiber, interface, matrix og Alt
            f = p.faces
            p.Set(faces=f, name='Alt')                                             # Lag Alt set
            x = xydata[0][0]
            y = xydata[0][1]
            r = rmean
            if Fibervariation:
                r = xydata[0][2]
            Ffaces= f.getByBoundingCylinder((x, y, -10.0), (x, y, 10.0), r + 0.01)
            for i in range(1, len(xydata)):
                x = xydata[i][0]
                y = xydata[i][1]
                if Fibervariation:
                    r = xydata[i][2]
                temp = f.getByBoundingCylinder((x, y, -10.0), (x, y, 10.0), r + 0.01)
                Ffaces = Ffaces + temp
            p.Set(name='Ffiber', faces=Ffaces)                          # Lag fiber set

            x = xydata[0][0]
            y = xydata[0][1]
            r = rmean
            if Fibervariation:
                r = xydata[0][2]
            IFfaces= f.getByBoundingCylinder((x, y, -10.0), (x, y, 10.0), r*(1+rinterface) + 0.01)
            for i in range(1, len(xydata)):
                x = xydata[i][0]
                y = xydata[i][1]
                if Fibervariation:
                    r = xydata[i][2]
                temp = f.getByBoundingCylinder((x, y, -10.0), (x, y, 10.0), r*(1+rinterface) + 0.01)
                IFfaces = IFfaces + temp
            p.Set(name='IFfiber', faces=IFfaces)                                                # Lag interface og matrix set

            p.SetByBoolean(name='Interface', sets=(p.sets['IFfiber'], p.sets['Ffiber'],), operation=DIFFERENCE)
            p.SetByBoolean(name='Matrix', sets=(p.sets['Alt'], p.sets['IFfiber'],), operation=DIFFERENCE)
            p = mod.parts['Part-1']



            p.seedPart(size=meshsize, deviationFactor=0.1, minSizeFactor=0.1)
            p.seedEdgeBySize(edges=p.edges, size=meshsize, deviationFactor=0.1,
                             constraint=FINER)
            p.setMeshControls(regions=p.sets['Interface'].faces, elemShape=QUAD, algorithm=MEDIAL_AXIS, minTransition=OFF)
            """for ma in p.sets['Interface'].faces:
                mesh =[]
                mesh.append(ma)
                p.setMeshControls(regions=(mesh), elemShape=QUAD, algorithm=MEDIAL_AXIS, minTransition=OFF)
                p.generateMesh(regions=(mesh))"""
            p.generateMesh(regions = p.sets['Matrix'].faces)
            for ma in p.sets['Interface'].faces:
                mesh =[]
                mesh.append(ma)
                p.setMeshControls(regions=(mesh), elemShape=QUAD, algorithm=MEDIAL_AXIS, minTransition=OFF)
                p.generateMesh(regions=(mesh))
            p.setMeshControls(regions=p.sets['Ffiber'].faces, elemShape=TRI)
            p.generateMesh(regions = p.sets['Ffiber'].faces)
            p.deleteMesh(regions=p.sets['Interface'].faces)
            p.generateMesh(regions=p.sets['Interface'].faces)
            del mod.parts['Part-1'].sets['Alt'],mod.parts['Part-1'].sets['Matrix'],mod.parts['Part-1'].sets['Interface'],mod.parts['Part-1'].sets['Ffiber'],mod.parts['Part-1'].sets['IFfiber']
        else:
            f = p.faces
            pickedFaces = f.findAt(((0.0, 0.0, 0.0),))
            e1 = p.edges                                                                                                   # Create partioned planar shell from sketch
            p.PartitionFaceBySketch(sketchUpEdge=e1.findAt(coordinates=(dx, 0.0,
                                                                        0.0)), faces=pickedFaces, sketch=s1)
            s1.unsetPrimaryObject()
            p = mod.parts['Part-1']
            p.seedPart(size=meshsize, deviationFactor=0.1, minSizeFactor=0.1)                                                   # Generate mesh
            p.generateMesh()
        mdb.meshEditOptions.setValues(enableUndo=True, maxUndoCacheElements=0.5)
        elFace = mod.parts['Part-1'].elementFaces                                                                             # Extrude mesh
        v = ((0.0, 0.0, 0.0), (0.0, 0.0, 2*tykkelse))
        p.generateBottomUpExtrudedMesh(elemFacesSourceSide=elFace,extrudeVector=v, numberOfLayers=2)
        p = mod.parts['Part-1']                                                                                               # Delete shell nodes of part
        n = p.nodes
        nodes = n.getByBoundingBox(-dL, -dL, -0.01, dL, dL, 0.01)
        p.deleteNode(nodes=nodes)
        p.PartFromMesh(name='Part-1-mesh-1', copySets=True)                                                                    # Make orphan mesh

        p = mod.parts['Part-1-mesh-1']                                                                                    # Lage Set
        e = p.elements
        p.Set(name='Alle', elements=e)                                                                                  # Lage set, meshe og lage material set
        if Interface:                                                               #IF Interface -  Lag elementset for fiber, interface og matrix
            x = xydata[0][0]
            y = xydata[0][1]
            r = xydata[0][2]
            Felements = e.getByBoundingCylinder((x, y, -10.0), (x, y, 10.0), r + 0.01)
            for i in range(1, len(xydata)):
                x = xydata[i][0]
                y = xydata[i][1]
                r = xydata[i][2]
                temp = e.getByBoundingCylinder((x, y, -10.0), (x, y, 10.0), r + 0.01)
                Felements = Felements + temp
            p.Set(name='Fibers', elements=Felements)                                                                            # Fiber set made

            x = xydata[0][0]
            y = xydata[0][1]
            r = xydata[0][2]
            IFelements = e.getByBoundingCylinder((x, y, -10.0), (x, y, 10.0), r * (1 + rinterface) + 0.01)
            for i in range(1, len(xydata)):
                x = xydata[i][0]
                y = xydata[i][1]
                r = xydata[i][2]
                temp = e.getByBoundingCylinder((x, y, -10.0), (x, y, 10.0), r * (1 + rinterface) + 0.01)
                IFelements = IFelements + temp
            p.Set(name='IandF', elements=IFelements)                                                                             # Fiber+fiberinterface set made

            p.SetByBoolean(name='Interfaces', sets=(p.sets['IandF'], p.sets['Fibers'],), operation=DIFFERENCE)
            p.SetByBoolean(name='Matrix', sets=(p.sets['Alle'], p.sets['IandF'],), operation=DIFFERENCE)                      # Lag matrix og interface set
            del mod.parts['Part-1-mesh-1'].sets['IandF']
        else:                                               #IF no interface -  Lag elementset for fiber og matrix.
            x = xydata[0][0]
            y = xydata[0][1]
            r = xydata[0][2]
            Felements = e.getByBoundingCylinder((x, y, -10.0), (x, y, 10.0), r + 0.001)
            for i in range(1, len(xydata)):
                x = xydata[i][0]
                y = xydata[i][1]
                r = xydata[i][2]
                temp = e.getByBoundingCylinder((x, y, -10.0), (x, y, 10.0), r + 0.001)
                Felements = Felements + temp
            p.Set(name='Fibers', elements=Felements)                                                                                    # Fiber set made
            p.SetByBoolean(name='Matrix', sets=(p.sets['Alle'], p.sets['Fibers'],), operation=DIFFERENCE)                               # Lag matrix set
        del mdb.models['Model-A'].parts['Part-1-mesh-1'].sets['Alle']
    else:                                                     # If: Om ingen fiber i modell
        p.seedPart(size=meshsize, deviationFactor=0.1, minSizeFactor=0.1)                                           #Meshe
        p.generateMesh()
        mdb.meshEditOptions.setValues(enableUndo=True, maxUndoCacheElements=0.5)
        elFace = mod.parts['Part-1'].elementFaces                                                                     # Extrude mesh
        v = ((0.0, 0.0, 0.0), (0.0, 0.0, 2*tykkelse))
        p.generateBottomUpExtrudedMesh(elemFacesSourceSide=elFace,extrudeVector=v, numberOfLayers=2)
        p.PartFromMesh(name='Part-1-mesh-1', copySets=True)                                                         # Make orphan mesh
        p = mod.parts['Part-1-mesh-1']
        n = p.nodes
        nodes = n.getByBoundingBox(-dL, -dL, -0.01, dL, dL, 0.01)
        p.deleteNode(nodes=nodes)                                                                                   # Deleted shell nodes
        p.Set(name='Matrix', elements=p.elements)                                                                   # Lag set for Matrix
                                                                                                                    # Angi materialegenskaper
    mod.Material(name='resin')                                                                  #Assign Properties and sections
    mod.materials['resin'].Elastic(table=((3500.0, 0.33),))
    mod.materials['resin'].Density(table=((1.2e-09,),))
    mod.HomogeneousSolidSection(name='SSmatrix', material='resin', thickness=None)
    if not nf == 0:
        mod.Material(name='glass')
        mod.materials['glass'].Elastic(table=((90000.0, 0.22),))
        mod.materials['glass'].Density(table=((2.55e-09,),))
        if Interface:
            mod.Material(name='interface')
            mod.materials['interface'].Elastic(type=TRACTION, table=((100.0, 100.0, 100.0), ))
            mod.materials['interface'].Density(table=((1.2e-09,),))
            if nonLinearDeformation:
                mod.materials['interface'].QuadsDamageInitiation(table=((0.042, 0.063, 0.063),))
                mod.materials['interface'].quadsDamageInitiation.DamageEvolution(type=ENERGY, mixedModeBehavior=BK,
                                                                                 power=1.2,
                                                                                 table=((0.0028, 0.0078, 0.0078),))
            mdb.models['Model-A'].CohesiveSection(name='SSbond', material='interface',
                                                  response=TRACTION_SEPARATION, initialThicknessType=GEOMETRY,
                                                  outOfPlaneThickness=None)
            region = p.sets['Interfaces']
            p.SectionAssignment(region=region, sectionName='SSbond', offset=0.0,
                                offsetType=MIDDLE_SURFACE, offsetField='',
                                thicknessAssignment=FROM_SECTION)
        if nonLinearDeformation:
            mod.materials['interface'].QuadsDamageInitiation(table=((0.042, 0.063, 0.063),))
            mod.materials['interface'].quadsDamageInitiation.DamageEvolution(type=ENERGY, mixedModeBehavior=BK, power=1.2, table=((0.0028, 0.0078,0.0078),))
            mod.materials['resin'].ConcreteDamagedPlasticity(table=((0.1, 0.1, 1.16, 0.89, 0.0001), ))
            mod.materials['resin'].concreteDamagedPlasticity.ConcreteCompressionHardening(table=((0.102, 0.0), (0.104, 0.05), (0.106, 0.32), (0.00102, 0.55)))
            mod.materials['resin'].concreteDamagedPlasticity.ConcreteTensionStiffening(table=((0.6, 0.09), ), type=GFI)
            mod.materials['resin'].concreteDamagedPlasticity.ConcreteTensionDamage(table=((0.0, 0.0), (0.9, 1.487)), type=DISPLACEMENT)
            mod.materials['resin'].concreteDamagedPlasticity.ConcreteCompressionDamage(table=((0.0, 0.0), (0.0, 0.32), (0.9, 0.55)))
        mod.HomogeneousSolidSection(name='SSfibers', material='glass', thickness=None)
        region = p.sets['Fibers']
        p.SectionAssignment(region=region, sectionName='SSfibers', offset=0.0,
                            offsetType=MIDDLE_SURFACE, offsetField='',
                            thicknessAssignment=FROM_SECTION)
        region = p.sets['Matrix']
        p.SectionAssignment(region=region, sectionName='SSmatrix', offset=0.0,
                            offsetType=MIDDLE_SURFACE, offsetField='',
                            thicknessAssignment=FROM_SECTION)
    else:
        if nonLinearDeformation:
            mod.materials['resin'].ConcreteDamagedPlasticity(table=((0.1, 0.1, 1.16, 0.89, 0.0001), ))
            mod.materials['resin'].concreteDamagedPlasticity.ConcreteCompressionHardening(table=((0.102, 0.0), (0.104, 0.05), (0.106, 0.32), (0.00102, 0.55)))
            mod.materials['resin'].concreteDamagedPlasticity.ConcreteTensionStiffening(table=((0.6, 0.09), ), type=GFI)
            mod.materials['resin'].concreteDamagedPlasticity.ConcreteTensionDamage(table=((0.0, 0.0), (0.9, 1.487)), type=DISPLACEMENT)
            mod.materials['resin'].concreteDamagedPlasticity.ConcreteCompressionDamage(table=((0.0, 0.0), (0.0, 0.32), (0.9, 0.55)))
        region = p.sets['Matrix']
        p.SectionAssignment(region=region, sectionName='SSmatrix', offset=0.0,
                            offsetType=MIDDLE_SURFACE, offsetField='',
                            thicknessAssignment=FROM_SECTION)
    # del mod.parts['Part-1'], p, n, mod, region
    # del model.sketches['__profile__'], f, pickedFaces, e1, f1, e, t
    # del s1, model,x,y
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
"""%%%%%%%%%%%%%%%%%%%%%"""
"""     SIMULATIONS     """

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

    del a, mod, Jobw, case

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

# Post processing of data
def Extract_parameterdata():
    #Spenninger 12
    maxMisesStresses = list()       #0
    minMisesStresses = list()       #1
    maxPrinceStresses = list()      #2
    midPrinceStresses = list()      #3

    minPrinceStresses = list()      #4
    maxTresca = list()              #5
    minTresca = list()              #6
    maxPress = list()               #7

    minPress = list()               #8
    maxINV3 = list()                #9
    minINV3  = list()               #10
    maxSherstresses = list()        #11

    #Toyinger 4
    maxPrinceToyinger = list()      #0
    midPrinceToyinger = list()      #1
    minPrinceToyinger = list()      #2
    maxSherToyinger = list()        #3

    Spenninger=[maxMisesStresses,minMisesStresses, maxPrinceStresses,midPrinceStresses,
                minPrinceStresses,maxTresca,minTresca,maxPress,
                minPress,maxINV3,minINV3,maxSherstresses]
    Toyinger = [maxPrinceToyinger,midPrinceToyinger,minPrinceToyinger,maxSherToyinger]

    print 'Computing stresses for ' + str(sweepcases) + ' sweep cases'
    for case in range(0,sweepcases):
        odb = session.openOdb(workpath + Sweeptoyinger[case] + '.odb')
        nodalStresses = odb.steps[difstpNm].frames[-1].fieldOutputs['S'].getSubset(position=ELEMENT_NODAL).values
        nodalStrains = odb.steps[difstpNm].frames[-1].fieldOutputs['E'].getSubset(position=ELEMENT_NODAL).values
        if not nf==0:
            Matrix = odb.rootAssembly.instances[instanceName].elementSets['MATRIX']
            nodalStresses = odb.steps[difstpNm].frames[-1].fieldOutputs['S'].getSubset(position=ELEMENT_NODAL,
                                                                                       region=Matrix).values
            nodalStrains = odb.steps[difstpNm].frames[-1].fieldOutputs['E'].getSubset(position=ELEMENT_NODAL,
                                                                                      region=Matrix).values

        MisesS = list()
        maxPrinceS =list()
        midPrinceS =list()
        minPrinceS =list()
        TrescaS =list()
        PressS =list()
        INV3S =list()
        sherS=list()

        maxPrinceT = list()
        midPrinceT = list()
        minPrinceT = list()
        sherT=list()

        for j in range(0,len(nodalStresses)):

            MisesS.append(float(nodalStresses[j].mises))
            maxPrinceS.append(float(nodalStresses[j].maxPrincipal))
            midPrinceS.append(float(nodalStresses[j].midPrincipal))
            minPrinceS.append(float(nodalStresses[j].minPrincipal))
            TrescaS.append(float(nodalStresses[j].tresca))
            PressS.append(float(nodalStresses[j].press))
            INV3S.append(float(nodalStresses[j].inv3))
            sherS.append(sqrt(float(nodalStresses[j].data[3]) ** 2 + float(nodalStresses[j].data[4]) ** 2 + float(nodalStresses[j].data[5]) ** 2))

            maxPrinceT.append(float(nodalStrains[j].maxPrincipal))
            midPrinceT.append(float(nodalStrains[j].midPrincipal))
            minPrinceT.append(float(nodalStrains[j].minPrincipal))
            sherT.append(sqrt(float(nodalStrains[j].data[3])**2+float(nodalStrains[j].data[4])**2+float(nodalStrains[j].data[5])**2))
        odb.close()

        Spenninger[0].append(float(max(MisesS)))
        Spenninger[1].append(float(min(MisesS)))
        Spenninger[2].append(float(max(maxPrinceS)))
        Spenninger[3].append(float(max(midPrinceS)))

        Spenninger[4].append(float(min(minPrinceS)))
        Spenninger[5].append(float(max(TrescaS)))
        Spenninger[6].append(float(min(TrescaS)))
        Spenninger[7].append(float(max(PressS)))

        Spenninger[8].append(float(min(PressS)))
        Spenninger[9].append(float(max(INV3S)))
        Spenninger[10].append(float(min(INV3S)))
        Spenninger[11].append(float(max(sherS)))

        Toyinger[0].append(float(max(maxPrinceT)))
        Toyinger[1].append(float(max(midPrinceT)))
        Toyinger[2].append(float(min(minPrinceT)))
        Toyinger[3].append(float(max(sherT)))



    g = open(Envelope+str(int(nf))+'_'+str(int(Q))+'.txt', "w")
    for a in range(0, len(maxMisesStresses)):
        #                 0                         1                         2                               3                                  4
        g.write(str(Spenninger[0][a]) + '\t' + str(Spenninger[1][a]) + '\t' + str(Spenninger[2][a]) + '\t' + str(Spenninger[3][a]) + '\t' + str(Spenninger[4][a])
            + '\t' + str(Spenninger[5][a]) + '\t' + str(Spenninger[6][a]) + '\t' + str(Spenninger[7][a]) + '\t' + str(Spenninger[8][a])
            + '\t' + str(Spenninger[9][a]) + '\t' + str(Spenninger[8][a]) + '\t' + str(Spenninger[9][a]) + '\t' + str(Spenninger[10][a]) + '\t' + str(Spenninger[11][a])
            + '\t' + str(Toyinger[0][a]) + '\t' + str(Toyinger[1][a]) + '\t' + str(Toyinger[2][a]) + '\t' + str(Toyinger[3][a])+'\n')

    a=0 # Complete the Sirkel
    g.write(str(Spenninger[0][a]) + '\t' + str(Spenninger[1][a]) + '\t' + str(Spenninger[2][a]) + '\t' + str(Spenninger[3][a]) + '\t' + str(Spenninger[4][a])
            + '\t' + str(Spenninger[5][a]) + '\t' + str(Spenninger[6][a]) + '\t' + str(Spenninger[7][a]) + '\t' + str(Spenninger[8][a])
            + '\t' + str(Spenninger[9][a]) + '\t' + str(Spenninger[8][a]) + '\t' + str(Spenninger[9][a]) + '\t' + str(Spenninger[10][a]) + '\t' + str(Spenninger[11][a])
            + '\t' + str(Toyinger[0][a]) + '\t' + str(Toyinger[1][a]) + '\t' + str(Toyinger[2][a]) + '\t' + str(Toyinger[3][a]))
    g.close()
    return

"""$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"""
"""          GLOBALE VARIABLER                                                   """

#Flag

Runjobs = 0                         # Bestemmer om jobber skal kjores
nonLinearDeformation = 1            # Linear eller nonlinear analyse?

noFiber = 0                         # Overstyrer antall fiber til 0
Fibervariation = 1                  # Skal fiber radius variere eller ikke?
Interface = 1                       # Interface paa fibere?


"""Start"""
#Sample=[0, 5, 10, 25,50]

Sample=[20]
for m in range(0,len(Sample)):
    n = 1                                                                # Sweep variabel: fra 0 til n antall random seeds
    nf=Sample[m]                                                         # Modelleringsvariabler
    Vf = 0.6

    rmean = 8.7096                                                       # Gjennomsnittradius. Om ikke fibervariasjon saa settes fibere til aa vaere uniform.
    Rstdiv = 0.6374                                                      # Standard avvik fra gjennomsnittsradius.
    Rclearing = 0.025                                                    # Prosent avstand mellom fibere og fra kanter og sider

    FiberSirkelResolution = 32                                           # 2*pi/FiberSirkelResolution
    meshsize = rmean * 2*pi/FiberSirkelResolution                        # Meshresolution, mindre koeffisient er mindre og flere elementer
    sweepcases = 2

    #Andre variabler
    if True:            # For aa kunne kollapse variabler
                                                                    # Er RVE tomt? RVE_Modelleringsparametere
        if nf == 0 or Vf == 0 or noFiber:                   # Fiberfri RVE
            nf = 0
            Vf = 0
            dL = rmean*3
        if not nf == 0:
            dL = ((nf * pi * rmean ** 2) / (Vf)) ** 0.5                 # RVE storrelsen er satt til aa vaere relativ av nf og V

        tykkelse = 0.01 * dL                                                       # RVE tykkelse

        r = rmean                                                                  # Tykkelse paa RVE
        rtol = Rclearing * r                                                       # Mellomfiber toleranse
        rinterface = 0.01/2                                                       # Interface tykkelse    1% av diameteren    0.5%av radius

        gtol = Rclearing * r                                                       # Dodsone toleranse
        ytredodgrense = r + gtol                                                   # Dodzone avstand, lengst fra kantene
        indredodgrense = r - gtol                                                  # Dodzone avstand, naermest kantene

        iterasjonsgrense = 10000                                                   # iterasjonsgrense

        sweepresolution = 2 * pi / sweepcases  # stepsize

        # Tekstfiler

        GitHub ='C:/Multiscale-Modeling/'
        Tekstfiler = 'textfiles/'

        Envelope = GitHub + Tekstfiler + 'envelope'         #   Parameteravhengig - Spesifikt navn legges til i funksjonen
        parameterpath = GitHub + 'Parametere.txt'         #   Skrives ned for chaining  til ett annet script
        coordpath = GitHub + 'coordst.txt'                #   Hentes fra genererefiberPop chaining  til ett annet script
        lagrestiffpath = GitHub + 'Stiffness.txt'         #   Skrives ned statistikk til ett annet script
        workpath = 'C:/Temp/'                           #   Abaqus arbeidsmappe


        """   ABAQUS   """
        modelName = 'Model-A'
        instanceName = 'PART-1-MESH-1-1'
        stepName = 'Enhetstoyninger'
        difstpNm = 'Lasttoyinger'

    """RVE_MODELLERING"""
    for Q in range(0,n):
        from abaqus import *
        from abaqusConstants import *
        from odbAccess import *

        seed(Q)                                     # Q er randomfunksjonensnokkelen
        wiggle = random() * rmean                     # Omplasseringsgrenser for fiberomplassering

        #Abaqus
        Enhetstoyinger = ['Exx' + str(nf) + '_' + str(Q), 'Eyy' + str(nf) + '_' + str(Q), 'Ezz' + str(nf) + '_' + str(Q),
                          'Exy' + str(nf) + '_' + str(Q), 'Exz' + str(nf) + '_' + str(Q), 'Eyz' + str(nf) + '_' + str(Q)]
                                                    # Enhetstoyingene fra 0 til 5. Alle 6
        Sweeptoyinger = [''] * sweepcases
        for g in range(0,sweepcases):
            Sweeptoyinger[g] = ('Sweep_strain'+ str(nf) + '_'+str(int(g*180*sweepresolution/pi))+'__'+str(int(Q)))

        #Lagre parametere til stottefiler

        lagreparametere(Q)

        """Prosess"""


        xydata = None                                                       #Fiber populasjon?
        if not (nf==0):
            execfile(GitHub+'GenerereFiberPopTilFil.py')            # create a random population
            xydata= hentePopulation(coordpath)                      # hente fibercoordinater

        # Lag Abaqus Model
        createModel(xydata)                                                    # Lag model for testing med onsket fiber og interface.
        createCEq()                                                            # Lag constrain equations

        if nonLinearDeformation:
            print 'yeah'
            del noWORK

        else:
            create_Linearunitstrainslastcases()                                             # Lag linear strain cases. Set boundary condition and create job.
            Stiffmatrix = get_stiffness()                                                   # Faa ut stiffnessmatrix

            Compliancematrix = get_compliance(Stiffmatrix)                                  # Inverter til compliance materix
            sweepstrains = get_sweepstrains_sig2_sig3(Compliancematrix, sweepresolution)    # Finne strains for sweep stress case
            create_Linearsweepedlastcases(sweepstrains)                                     # Lag linear sweep strain cases. Set boundary condition and create job.

        #Extract_parameterdata()                                                            # Abaqus Save Odb data to textfile for envelopes

        print 'bob'

