"""Filen er laget for aa bli kjort av microscale scriptet"""
# Importere til assembly, transformere til origo og rotere til fiberretning langs x akse, lage referanse punkter, Constraint equation
def Import_n_Transform(a,p):
    a.DatumCsysByDefault(CARTESIAN)
    a.Instance(name=instanceName, part=p, dependent=ON)  # Hente modell til assembly,
    a.translate(instanceList=(instanceName,), vector=(0.0, 0.0, -tykkelse))  # Flytte modellen til origo
    a.rotate(instanceList=(instanceName,), axisPoint=(0.0, 0.0, 0.0),  # Rotere rundt y akse saa x er i fiberretning
             axisDirection=(0.0, 1.0, 0.0), angle=90.0)

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
    counter = 0
    for n in nodesXa:
        name1 = "Xa%i" % (counter)
        nodes1 = nodesXa[counter:counter + 1]
        a.Set(nodes=nodes1, name=name1)
        x, y, z = n.coordinates[0], n.coordinates[1], n.coordinates[2]
        name2 = "Xb%i" % (counter)
        nodes2 = nodesXb.getByBoundingCylinder((-dL, y, z), (dL, y, z), tol)
        a.Set(nodes=nodes2, name=name2)
        if counter==0:
            mod.Equation(name="Cq11x%i" % (counter),
                         terms=((1.0, name2, 1), (-(xmax - xmin), 'RPX', 1),))  # 11
        else:
            mod.Equation(name="Cq11x%i" % (counter),
                         terms=((1.0, name2, 1), (-1.0, name1, 1), (-(xmax - xmin), 'RPX', 1),))  # 11
        mod.Equation(name="Cq21x%i" % (counter),
                     terms=((1.0, name2, 2), (-1.0, name1, 2), (-(xmax - xmin) / 2, 'RPX', 2),))  # 21
        mod.Equation(name="Cq31x%i" % (counter),
                     terms=((1.0, name2, 3), (-1.0, name1, 3), (-(xmax - xmin) / 2, 'RPX', 3),))  # 31

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
                     terms=((1.0, name2, 1), (-1.0, name1, 1), (-(ymax - ymin) / 2, 'RPY', 1),))  # 12
        mod.Equation(name="Cq22y%i" % (counter),
                     terms=((1.0, name2, 2), (-1.0, name1, 2), (-(ymax - ymin), 'RPY', 2),))  # 22
        mod.Equation(name="Cq32y%i" % (counter),
                     terms=((1.0, name2, 3), (-1.0, name1, 3), (-(ymax - ymin) / 2, 'RPY', 3),))  # 32

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
                     terms=((1.0, name2, 1), (-1.0, name1, 1), (-(zmax - zmin) / 2, 'RPZ', 1),))  # 13
        mod.Equation(name="Cq23z%i" % (counter),
                     terms=((1.0, name2, 2), (-1.0, name1, 2), (-(zmax - zmin) / 2, 'RPZ', 2),))  # 23
        mod.Equation(name="Cq33z%i" % (counter),
                     terms=((1.0, name2, 3), (-1.0, name1, 3), (-(zmax - zmin), 'RPZ', 3),))  # 33

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