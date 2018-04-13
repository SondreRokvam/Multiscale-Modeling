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
    del mod.parts[meshPartName].sets['Alle']


if not nf == 0:         # Om fiber i RVE
    RVEsets()
else:                   # Om ingen fiber, bare matrix set
    p = mod.parts[meshPartName]
    p.Set(name='Matrix', elements=p.elements)



if not noFiber and Interface:
    # Lage fiber datums for material orientering av Interface UNCLEAR IF NEEDED
    """for ie in range(0, len(xydata)):
        x = xydata[ie][0]
        y = xydata[ie][1]
        p.DatumCsysByThreePoints(name=('Fiber datum ' + str(ie)), coordSysType=CYLINDRICAL,
                                 origin=(x, y, 0.0), point1=(x + 1.0, y, 0.0), point2=(x + 1.0, y + 1.0, 0.0))
                                 """

    if nonLinearAnalysis: # Slette og lage nye element i interface for       # Set cohesive elementtype paa Interface
        p = mod.parts[meshPartName]
        for i in range(0, len(xydata)):
            intface = mod.parts[meshPartName].sets['FiberInt' + str(i)]
            x = xydata[i][0]
            y = xydata[i][1]
            r = xydata[i][2]
            relevantnods = intface.nodes
            FOnodes = relevantnods.getByBoundingCylinder((x, y, -10.0), (x, y, 10.0), r + tol)
            bothnodes = relevantnods.getByBoundingCylinder((x, y, -10.0), (x, y, 10.0), r * (1 + rinterface) + 2*tol)
            p.Set(name='OFnods', nodes=FOnodes)
            p.Set(name='BOnods', nodes=bothnodes)
            p.SetByBoolean(name='IFnods', sets=(p.sets['BOnods'], p.sets['OFnods'],), operation=DIFFERENCE)
            bNodOF= p.sets['OFnods'].nodes.getByBoundingBox(-dL/2 - tol, -dL/2 - tol, RVEt - tol, dL/2 + tol, dL/2 + tol, RVEt + tol)
            frNodOF= p.sets['OFnods'].nodes.getByBoundingBox(-dL/2 - tol, -dL/2 - tol, 2*RVEt - tol, dL/2 + tol, dL/2 + tol, 2*RVEt + tol)
            bNodIF= p.sets['IFnods'].nodes.getByBoundingBox(-dL/2 - tol, -dL/2 - tol, RVEt - tol, dL/2 + tol, dL/2 + tol, RVEt + tol)
            frNodIF= p.sets['OFnods'].nodes.getByBoundingBox(-dL/2 - tol, -dL/2 - tol, 2*RVEt - tol, dL/2 + tol, dL/2 + tol, 2*RVEt + tol)
            p.Set(name='FremreFibnods', nodes=frNodOF)
            p.Set(name='FremreIntnods', nodes=frNodIF)
            p.Set(name='BakreFibnods', nodes=bNodOF)
            p.Set(name='BakreIntnods', nodes=bNodOF)
            del p.sets['BOnods'],p.sets['OFnods'],p.sets['IFnods']
            n1=p.sets['FremreFibnods'].nodes[0]
            thet = 2 * pi / FiberSirkelResolution
            for elems in range(0,len(intface.elements)):
                refx,refy,refz = n1.coordinates
                n4 = p.sets['BakreFibnods'].nodes.getByBoundingCylinder((refx,refy,-10*RVEt),(refx,refy,+10*RVEt), rinterface+tol)[0]
                n5 = p.sets['FremreIntnods'].nodes.getByBoundingCylinder((refx,refy,-10*RVEt),(refx,refy,+10*RVEt), rinterface+tol)[0]
                n8 = p.sets['BakreIntnods'].nodes.getByBoundingCylinder((refx,refy,-10*RVEt),(refx,refy,+10*RVEt), rinterface+tol)[0]
                alph = atan((refy-y)/(refx-x))
                alph = alph-thet
                Nx, Ny = x+cos(alph)*r, y+sin(alph)*r
                n2 = p.sets['FremreFibnods'].nodes.getByBoundingCylinder((Nx,Ny,-10*RVEt ),(Nx,Ny,+10*RVEt ), rinterface+tol)[0]
                n3 = p.sets['BakreFibnods'].nodes.getByBoundingCylinder((Nx,Ny,-10*RVEt ),(Nx,Ny,+10*RVEt ), rinterface+tol)[0]
                n6 = p.sets['FremreIntnods'].nodes.getByBoundingCylinder((Nx,Ny,-10*RVEt ),(Nx,Ny,+10*RVEt ), rinterface+tol)[0]
                n7 = p.sets['BakreIntnods'].nodes.getByBoundingCylinder((Nx,Ny,-10*RVEt ),(Nx,Ny,+10*RVEt ), rinterface+tol)[0]
                print n1, n2, n3, n4, n5, n6, n7, n8
                p.Element(nodes=(n1, n2, n3, n4, n5, n6, n7, n8), elemShape=HEX8)
                n1=n2
                del sad
            p.deleteElement(elements=intface.elements)
        """p.setElementType(regions=p.sets['Interfaces'],elemTypes=(mesh.ElemType(elemCode=COH3D8, elemLibrary=STANDARD,
                                                                               elemDeletion=ON, viscosity=0.0001),))
        #stackdirection fixer
        for i in range(0, len(xydata)):
            pickedments = mod.parts[meshPartName].sets['FiberInt' + str(i)]
            elFa= pickedments.elements[0].label
            for elementface in p.elementFaces:
                if elementface.label == elFa:
                    if elementface.face == FACE2:
                        q = elementface
                        print elementface.label, elementface.face,q
                        leaf = dgm.LeafFromSets(sets=(pickedments, ))
                        session.viewports['Viewport: 1'].partDisplay.displayGroup.replace(leaf=leaf)
                        p.assignStackDirection(referenceRegion=q, pickedElements=pickedments.cells)
                        del skl
                        p.orientElements(referenceRegion=q, pickedElements=pickedments)
                        print 'did it'
        """
        print 'Element sets (and Fiber center datums) created'
