"""Filen er laget for aa bli kjort av microscale scriptet"""
# Importere til assembly, transformere til origo og rotere til fiberretning langs x akse, lage referanse punkter, Constraint equation
def Import_n_Transform(a,p):
    a.DatumCsysByDefault(CARTESIAN)
    a.Instance(name=instanceName, part=p, dependent=ON)  # Hente modell til assembly,
    a.translate(instanceList=(instanceName,), vector=(0.0, 0.0, -tykkelse))  # Flytte modellen til origo
    a.rotate(instanceList=(instanceName,), axisPoint=(0.0, 0.0, 0.0),  # Rotere rundt y akse saa x er i fiberretning
             axisDirection=(0.0, 1.0, 0.0), angle=90.0)
    print '\nImported to Assembly, Translated to origo with fibers longitudinal to x'
def ReferencePoints(a,xmax, ymax, zmax, xmin, ymin, zmin):        # Create X,Y,Z reference points

    a.ReferencePoint(point=(xmin - 0.2 * (xmax - xmin), 0.0, 0.0))
    refPoints = (a.referencePoints[a.features['RP-1'].id],)
    a.Set(referencePoints=refPoints, name='RPX')

    a.ReferencePoint(point=(0.0, ymin - 0.2 * (ymax - ymin), 0.0))
    refPoints = (a.referencePoints[a.features['RP-2'].id],)
    a.Set(referencePoints=refPoints, name='RPY')

    a.ReferencePoint(point=(0.0, 0.0, zmin - 0.2 * (zmax - zmin)))
    refPoints = (a.referencePoints[a.features['RP-3'].id],)
    a.Set(referencePoints=refPoints, name='RPZ')

def ConstraintEquations(a,allNodes,xmax, ymax, zmax, xmin, ymin, zmin):
    # Constraint Equations between x-normal surfaces: Note: excluding a node for fixing
    nodesXa = allNodes.getByBoundingBox(xmin-tol,ymin-tol,zmin-tol,xmin+tol, ymax+tol,zmax+tol)    
    nodesXb = allNodes.getByBoundingBox(xmax-tol,ymin-tol,zmin-tol,xmax+tol, ymax+tol,zmax+tol)  
    
    NL1=nodesXa.getByBoundingCylinder((-tol,-dL/2,-dL/2), (tol,-dL/2,-dL/2), tol)
    if len(NL1)==1:
        a.Set(nodes=NL1, name='NL1')
    else:
        del FinnerIkkeHjornenode
    NL2=nodesXa.getByBoundingBox(xmin-tol,-dL/10,zmin-tol,xmin+tol,dL/10,zmin+tol)
    NL2 = NL2[int(len(NL2)/2):int(len(NL2)/2) + 1 ]
    if len(NL2)==1:
        a.Set(nodes=NL2, name='NL2')
    else:          
        del FinnerIkkeKantenode
    if not nf==0:
        NL3=nodesXa.getByBoundingCylinder((-tol,0,0), (tol,0,0), dL/10)
        NL3 = NL3[int(len(NL2)/2):int(len(NL2)/2) + 1 ]
    else:
        NL3 = nodesXa.getByBoundingCylinder((-tol, 0, 0), (tol, 0, 0), dL / 3)
        NL3 = NL3[int(len(NL2) / 2):int(len(NL2) / 2) + 1]
    if len(NL3)==1:
        a.Set(nodes=NL3, name='NL3')
    else:
        del FinnerIkkeMidtnode
    counter = 0
    for n in nodesXa:
        name1 = "Xa%i" % (counter)
        nodes1 = nodesXa[counter:counter + 1]
        a.Set(nodes=nodes1, name=name1)
        x, y, z = n.coordinates[0], n.coordinates[1], n.coordinates[2]
        name2 = "Xb%i" % (counter)
        nodes2 = nodesXb.getByBoundingCylinder((-dL, y, z), (dL, y, z), tol)
        a.Set(nodes=nodes2, name=name2)
        mod.Equation(name="Cq11x%i" % (counter),
                         terms=((1.0, name2, 1), (-1.0, name1, 1), (-(xmax - xmin), 'RPX', 1),(0, 'RPX', 2),(0, 'RPX', 3),))  # 11
        mod.Equation(name="Cq21x%i" % (counter),
                     terms=((1.0, name2, 2), (-1.0, name1, 2), (-(xmax - xmin) / 2, 'RPX', 2),(0, 'RPX', 1),(0, 'RPX', 3),))  # 21
        mod.Equation(name="Cq31x%i" % (counter),
                     terms=((1.0, name2, 3), (-1.0, name1, 3), (-(xmax - xmin) / 2, 'RPX', 3),(0, 'RPX', 1),(0, 'RPX', 2),))  # 31

        counter = counter + 1

    # Constraint Equations between y-normal surfaces. Note: excluding the nodes at xmax:
    nodesYa = allNodes.getByBoundingBox(xmin-tol,ymin-tol,zmin-tol,xmax-tol, ymin+tol,zmax+tol)    
    nodesYb = allNodes.getByBoundingBox(xmin-tol,ymax-tol,zmin-tol,xmax-tol, ymax+tol,zmax+tol)       
    counter = 0
    for n in nodesYa:
        name1 = "Ya%i" % (counter)
        nodes1 = nodesYa[counter:counter + 1]
        a.Set(nodes=nodes1, name=name1)
        x, y, z = n.coordinates[0], n.coordinates[1], n.coordinates[2]
        name2 = "Yb%i" % (counter)
        nodes2 = nodesYb.getByBoundingCylinder((x, -dL, z), (x, dL, z), tol)
        a.Set(nodes=nodes2, name=name2)

        mod.Equation(name="Cq12y%i" % (counter),
                     terms=((1.0, name2, 1), (-1.0, name1, 1), (-(ymax - ymin) / 2, 'RPY', 1),(0, 'RPY', 2),(0, 'RPY', 3),))  # 12
        mod.Equation(name="Cq22y%i" % (counter),
                     terms=((1.0, name2, 2), (-1.0, name1, 2), (-(ymax - ymin), 'RPY', 2),(0, 'RPY', 1),(0, 'RPY', 3),))  # 22
        mod.Equation(name="Cq32y%i" % (counter),
                     terms=((1.0, name2, 3), (-1.0, name1, 3), (-(ymax - ymin) / 2, 'RPY', 3),(0, 'RPY', 1),(0, 'RPY', 2)))  # 32

        counter = counter + 1

    # Constraint Equations between z-normal surfaces. Note: excluding the nodes at xmax and ymax :
    nodesZa = allNodes.getByBoundingBox(xmin-tol,ymin-tol,zmin-tol,xmax-tol, ymax-tol,zmin+tol)    
    nodesZb = allNodes.getByBoundingBox(xmin-tol,ymin-tol,zmax-tol,xmax-tol, ymax-tol,zmax+tol)       
    counter = 0
    for n in nodesZa:
        name1 = "Za%i" % (counter)
        nodes1 = nodesZa[counter:counter + 1]
        a.Set(nodes=nodes1, name=name1)
        x, y, z = n.coordinates[0], n.coordinates[1], n.coordinates[2]
        name2 = "Zb%i" % (counter)
        nodes2 = nodesZb.getByBoundingCylinder((x, y, -dL), (x, y, dL), tol)
        a.Set(nodes=nodes2, name=name2)

        mod.Equation(name="Cq13z%i" % (counter),
                     terms=((1.0, name2, 1), (-1.0, name1, 1), (-(zmax - zmin) / 2, 'RPZ', 1),(0, 'RPZ', 2),(0, 'RPZ', 3),))  # 13
        mod.Equation(name="Cq23z%i" % (counter),
                     terms=((1.0, name2, 2), (-1.0, name1, 2), (-(zmax - zmin) / 2, 'RPZ', 2),(0, 'RPZ', 1),(0, 'RPZ', 3),))  # 23
        mod.Equation(name="Cq33z%i" % (counter),
                     terms=((1.0, name2, 3), (-1.0, name1, 3), (-(zmax - zmin), 'RPZ', 3),(0, 'RPZ', 1),(0, 'RPZ', 2),))  # 33

        counter = counter + 1

a = mod.rootAssembly
p = mdb.models[modelName].parts[meshPartName]
Import_n_Transform(a,p)
allNodes = a.instances[instanceName].nodes
# Finding the RVE dimensions
xmax, ymax, zmax, xmin, ymin, zmin = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
for n in allNodes:
    x, y, z = n.coordinates[0], n.coordinates[1], n.coordinates[2]
    xmax, ymax, zmax, xmin, ymin, zmin = max(xmax, x), max(ymax, y), max(zmax, z), min(xmin, x), min(ymin, y), min(zmin, z)

ReferencePoints(a,xmax, ymax, zmax, xmin, ymin, zmin)
ConstraintEquations(a,allNodes,xmax, ymax, zmax, xmin, ymin, zmin)

# Feste for simulering
if Singlepin:
    region = a.sets['NL1']
    mod.PinnedBC(name='Laas-3', createStepName='Initial',
                 region=region, localCsys=None)
if tripplepin and Singlepin:
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