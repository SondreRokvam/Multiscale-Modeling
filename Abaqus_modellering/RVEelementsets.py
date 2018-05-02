"""Filen er laget for aa bli kjort av microscale scriptet"""
# Lage Element set for baade Matrix, Fiber og Interface
def RVEsets():
    # Alle set
    p = mod.parts[meshPartName]
    e = p.elements
    p.Set(name='Alle', elements=e)
    # Fiber set
    x = xydata[0][0]
    y = xydata[0][1]
    r = xydata[0][2]
    Felements = e.getByBoundingCylinder((x, y, -10.0), (x, y, 10.0), r + tol)
    for i in range(1, len(xydata)):
        x = xydata[i][0]
        y = xydata[i][1]
        r = xydata[i][2]
        temp = e.getByBoundingCylinder((x, y, -10.0), (x, y, 10.0), r + tol)
        Felements = Felements + temp
    p.Set(name='Fibers', elements=Felements)
    #  Matrix set, Om Interface : Interfaces sets
    if Interface:  # Interfaces og matrix
        x = xydata[0][0]
        y = xydata[0][1]
        r = xydata[0][2]
        IFelements = e.getByBoundingCylinder((x, y, -10.0), (x, y, 10.0), r * (1 + rinterface) + tol)
        for i in range(1, len(xydata)):
            x = xydata[i][0]
            y = xydata[i][1]
            r = xydata[i][2]
            temp = e.getByBoundingCylinder((x, y, -10.0), (x, y, 10.0), r * (1 + rinterface) + tol)
            IFelements = IFelements + temp
        p.Set(name='IandF', elements=IFelements)  # Fiber+fiberinterface set made
        p.SetByBoolean(name='Interfaces', sets=(p.sets['IandF'], p.sets['Fibers'],), operation=DIFFERENCE)
        p.SetByBoolean(name='Matrix', sets=(p.sets['Alle'], p.sets['IandF'],),
                       operation=DIFFERENCE)  # Lag matrix og interface set

        # Lage Interface element set for hver fiber
        e = p.sets['Interfaces'].elements
        x = xydata[0][0]
        y = xydata[0][1]
        r = xydata[0][2]
        Felements = e.getByBoundingCylinder((x, y, -10.0), (x, y, 10.0), r * (1 + rinterface) + tol)
        p.Set(name='FiberInt0', elements=Felements)
        for i in range(1, len(xydata)):
            x = xydata[i][0]
            y = xydata[i][1]
            r = xydata[i][2]
            temp = e.getByBoundingCylinder((x, y, -10.0), (x, y, 10.0), r * (1 + rinterface) + tol)
            p.Set(name=('FiberInt' + str(i)), elements=temp)
        del mod.parts[meshPartName].sets['IandF']
    else:  # Bare matrix.
        p.SetByBoolean(name='Matrix', sets=(p.sets['Alle'], p.sets['Fibers'],), operation=DIFFERENCE)


def COHstackDir():  # Slette og lage nye element i interface for cohesive elementstack direction i Interface
    p = mod.parts[meshPartName]
    for i in range(0, len(xydata)):
        x = xydata[i][0]
        y = xydata[i][1]
        r = xydata[i][2]
        intface = mod.parts[meshPartName].sets['FiberInt' + str(i)]
        for element in intface.elements:
            p.SetFromElementLabels(name='elementi', elementLabels=(element.label,))
            elemNOdes = p.sets['elementi'].nodes
            min, max = -dL / 2 - tol, dL / 2 + tol
            nodesZa = elemNOdes.getByBoundingBox(min, min, tykkelse - tol, max, max,
                                                 tykkelse + tol)  # Velge noder front og bak av fiber i Z
            nodesZb = elemNOdes.getByBoundingBox(min, min, 2 * tykkelse - tol, max, max, 2 * tykkelse + tol)
            del min, max
            ZaFibnodes = nodesZa.getByBoundingCylinder((x, y, -10.0), (x, y, 10.0), r * (
                        rinterface + 1) - tol)  # Velge fiber og interface noder i front og bak av fiber
            ZbFibnodes = nodesZb.getByBoundingCylinder((x, y, -10.0), (x, y, 10.0), r * (rinterface + 1) - tol)
            p.Set(name='ZaBoth', nodes=nodesZa)
            p.Set(name='ZbBoth', nodes=nodesZb)
            p.Set(name='ZaFib', nodes=ZaFibnodes)
            p.Set(name='ZbFib', nodes=ZbFibnodes)
            p.SetByBoolean(name='ZaInt', sets=(p.sets['ZaBoth'], p.sets['ZaFib'],), operation=DIFFERENCE)
            p.SetByBoolean(name='ZbInt', sets=(p.sets['ZbBoth'], p.sets['ZbFib'],), operation=DIFFERENCE)
            del p.sets['ZaBoth'], p.sets['ZbBoth']

            # Orientere element
            x0, y0 = p.sets['ZaFib'].nodes[0].coordinates[0], p.sets['ZaFib'].nodes[0].coordinates[1]
            x1, y1 = p.sets['ZaFib'].nodes[1].coordinates[0], p.sets['ZaFib'].nodes[1].coordinates[1]
            dx1, dx2 = x0 - x, x1 - x
            dy1, dy2 = y0 - y, y1 - y
            th1 = np.arctan2(dy1, dx1) - pi
            th2 = np.arctan2(dy2, dx2) - pi

            XX, YY = x0, y0
            if th2 > th1:
                XX, YY = x1, y1

            if dy1 / abs(dy1) != dy2 / abs(
                    dy2) and dx1 < 0:  # Kontroller funksjon mot elementfeil element mellom som gaar fra 2pi>  til <0. I forrige funksjon blir dette vrengt
                XX, YY = x0, y0
                if th2 < th1:
                    XX, YY = x1, y1

            p.Set(name='N1',
                  nodes=p.sets['ZbFib'].nodes.getByBoundingCylinder((XX, YY, 0), (XX, YY, 3 * tykkelse), meshsize / 4))
            p.SetByBoolean(name='N2', sets=(p.sets['ZbFib'], p.sets['N1'],), operation=DIFFERENCE)
            p.Set(name='N4',
                  nodes=p.sets['ZaFib'].nodes.getByBoundingCylinder((XX, YY, 0), (XX, YY, 3 * tykkelse), meshsize / 4))
            p.SetByBoolean(name='N3', sets=(p.sets['ZaFib'], p.sets['N4'],), operation=DIFFERENCE)
            p.Set(name='N5',
                  nodes=p.sets['ZbInt'].nodes.getByBoundingCylinder((XX, YY, 0), (XX, YY, 3 * tykkelse), meshsize / 4))
            p.SetByBoolean(name='N6', sets=(p.sets['ZbInt'], p.sets['N5'],), operation=DIFFERENCE)
            p.Set(name='N8',
                  nodes=p.sets['ZaInt'].nodes.getByBoundingCylinder((XX, YY, 0), (XX, YY, 3 * tykkelse), meshsize / 4))
            p.SetByBoolean(name='N7', sets=(p.sets['ZaInt'], p.sets['N8'],), operation=DIFFERENCE)
            n1 = p.sets['N1'].nodes[0]
            n2 = p.sets['N2'].nodes[0]
            n3 = p.sets['N3'].nodes[0]
            n4 = p.sets['N4'].nodes[0]
            n5 = p.sets['N5'].nodes[0]
            n6 = p.sets['N6'].nodes[0]
            n7 = p.sets['N7'].nodes[0]
            n8 = p.sets['N8'].nodes[0]

            p.Element(nodes=(n1, n2, n3, n4, n5, n6, n7, n8), elemShape=HEX8)
            del p.sets['ZaFib'], p.sets['ZaInt'], p.sets['ZbFib'], p.sets['ZbInt'], p.sets['elementi']
            del p.sets['N1'], p.sets['N2'], p.sets['N3'], p.sets['N4'], p.sets['N5'], p.sets['N6'], p.sets['N7'], \
            p.sets['N8']
        p.deleteElement(elements=intface.elements)
        del mod.parts[meshPartName].sets['FiberInt' + str(i)]
    del p.sets['Matrix'], p.sets['Fibers'], p.sets['Interfaces'], p.sets['Ffiber'], p.sets['Alt'], p.sets[
        'Interface']

if not nf == 0:
    RVEsets()
    if Interface:
        COHstackDir()  # Endrer stackdirection paa elementer i Interface
        RVEsets()
        CohEelem = mesh.ElemType(elemCode=COH3D8, elemLibrary=STANDARD, elemDeletion=ON, viscosity=0.0001)
        p.setElementType(regions=p.sets['Interfaces'], elemTypes=(CohEelem,))
else:                   # Om ingen fiber, bare matrix set
    p = mod.parts[meshPartName]
    p.Set(name='Matrix', elements=p.elements)
print 'Element sets and stack direction completed'


