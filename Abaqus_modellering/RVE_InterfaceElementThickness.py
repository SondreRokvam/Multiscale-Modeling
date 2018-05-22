def adjust():
    a = mod.rootAssembly
    nod = a.instances[instanceName].nodes
    count = 0
    for fiba in xydata:
        x = fiba[0]
        y = fiba[1]
        r = rmean
        if Fibervariation:
            r = fiba[2]
        Fod = nod.getByBoundingCylinder((x, y, -dL), (x, y, dL), r - tol)
        Fnod = nod.getByBoundingCylinder((x, y, -dL), (x, y, dL), r * (1 + rinterface) - tol)
        Inod = nod.getByBoundingCylinder((x, y, -dL), (x, y, dL), r * (1 + rinterface) + rinterface)
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
            FN = Fibnodes.getByBoundingCylinder((xns, yns, zns - tol), (xns, yns, zns + tol), 2 * r * rinterface)
            IN = Intnodes.getByBoundingCylinder((xns, yns, zns - tol), (xns, yns, zns + tol), 2 * r * rinterface)
            a.Set(nodes=IN, name='IN')
            a.Set(nodes=FN, name='FN')
            if len(FN) == 1 and len(IN) == 1:
                nyx = round(FN[0].coordinates[0], 7)
                nyy = round(FN[0].coordinates[1], 7)
                nyz = round(FN[0].coordinates[2], 7)

                RScaling = ElementInterfaceT / r

                if abs(nyy) > dL / 2 - tol and abs(yns) > dL / 2 - tol:
                    diff=(xns-nyx)/abs(xns-nyx)
                    Ix=round(nyx + diff * ElementInterfaceT, 7)
                    Iy = nyy
                elif abs(nyx) > dL / 2 - tol and abs(xns) > dL / 2 - tol:
                    diff=(yns-nyy)/abs(yns-nyy)
                    Iy=round(nyy + diff* ElementInterfaceT, 7)
                    Ix = nyx
                else:
                    Iy = round(nyy + (nyy - y) * RScaling, 7)
                    Ix = round(nyx + (nyx - x) * RScaling, 7)
                if abs(Iy) > dL / 2:
                    Iy = (Iy / abs(Iy)) * dL / 2
                if abs(Ix) > dL / 2:
                    Ix = (Ix / abs(Ix)) * dL / 2
                a.editNode(nodes=a.sets['IN'], coordinate1=Ix, coordinate2=Iy, coordinate3=nyz)
                a.editNode(nodes=a.sets['FN'], coordinate1=nyx, coordinate2=nyy, coordinate3=nyz)
                a.regenerate()
                a.deleteSets(setNames=('noFiber' + str(count) + 'nodes', 'IN', 'FN', 'Fiber' + str(count) + 'nodes',
                                       'FiberInterface' + str(count) + 'nodes', 'Fiberflate' + str(count) + 'nodes',
                                       'Interface' + str(count) + 'nodes',))
        count = count + 1
if not ElementInterfaceT == 0:
    adjust()
print 'Interface elements adjusted'