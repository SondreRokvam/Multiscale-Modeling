a = mod.rootAssembly
nod = a.instances[instanceName].nodes
count = 0
# del checkHere
for fiba in xydata:
    x = fiba[0]
    y = fiba[1]
    r = rmean
    if Fibervariation:
        r = fiba[2]
    Fod = nod.getByBoundingCylinder((-10, y, -x), (10, y, -x), r - tol)
    Fnod = nod.getByBoundingCylinder((-10, y, -x), (10, y, -x), r * (1 + rinterface) - tol)
    Inod = nod.getByBoundingCylinder((-10, y, -x), (10, y, -x), r * (1 + rinterface) + rinterface)
    a.Set(nodes=Fod, name='noFiber' + str(count) + 'nodes')
    a.Set(nodes=Fnod, name='Fiber' + str(count) + 'nodes')
    a.Set(nodes=Inod, name='FiberInterface' + str(count) + 'nodes')
    a.SetByBoolean(name='Fiberflate' + str(count) + 'nodes',
                   sets=(a.sets['Fiber' + str(count) + 'nodes'], a.sets['noFiber' + str(count) + 'nodes'],),
                   operation=DIFFERENCE)
    a.SetByBoolean(name='Interface' + str(count) + 'nodes',
                   sets=(a.sets['FiberInterface' + str(count) + 'nodes'], a.sets['Fiber' + str(count) + 'nodes'],),
                   operation=DIFFERENCE)
    Intnodes = a.sets['Interface' + str(count) + 'nodes'].nodes
    Fibnodes = a.sets['Fiberflate' + str(count) + 'nodes'].nodes
    for node in Intnodes:
        xns = node.coordinates[0]
        yns = node.coordinates[1]
        zns = node.coordinates[2]
        FN = Fibnodes.getByBoundingCylinder((xns - tol, yns, zns), (xns + tol, yns, zns), 2 * r * rinterface)
        IN = Intnodes.getByBoundingCylinder((xns - tol, yns, zns), (xns + tol, yns, zns), 2 * r * rinterface)
        a.Set(nodes=IN, name='IN')
        a.Set(nodes=FN, name='FN')
        if len(FN) == 1 and len(IN) == 1:
            nyx = round(FN[0].coordinates[0], 7)
            nyy = round(FN[0].coordinates[1], 7)
            nyz = round(FN[0].coordinates[2], 7)
            RScaling = ElementInterfaceT / r

            Iy = round(nyy + (nyy - y) * RScaling, 7)
            Iz = round(nyz + (nyz + x) * RScaling, 7)
            if abs(Iy) > dL / 2:
                Iy = (Iy / abs(Iy)) * dL / 2
            if abs(Iz) > dL / 2:
                Iz = (Iz / abs(Iz)) * dL / 2
            a.editNode(nodes=a.sets['IN'], coordinate1=nyx, coordinate2=Iy, coordinate3=Iz)
            a.editNode(nodes=a.sets['FN'], coordinate1=nyx, coordinate2=nyy, coordinate3=nyz)
            a.regenerate()
            a.deleteSets(setNames=('noFiber' + str(count) + 'nodes', 'IN', 'FN', 'Fiber' + str(count) + 'nodes',
                                   'FiberInterface' + str(count) + 'nodes', 'Fiberflate' + str(count) + 'nodes',
                                   'Interface' + str(count) + 'nodes',))
    count = count + 1

print '\nInterface elements adjusted'