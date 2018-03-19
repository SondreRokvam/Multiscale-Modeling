"""Filen er laget for aa bli kjort av microscale scriptet"""
# Lage Element set for baade Matrix, Fiber og Interface
if not nf == 0:
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
else:  # Om ingen fiber, bare matrix set
    p = mod.parts[meshPartName]
    p.Set(name='Matrix', elements=p.elements)