"""
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

p = mod.parts[partName]


p.seedEdgeBySize(edges=p.edges, size=meshsize/2, deviationFactor=0.1,
                 constraint=FINER)
for ma in p.sets['Interface'].faces:
    mesh = []
    mesh.append(ma)
    p.setMeshControls(regions=(mesh), elemShape=QUAD, algorithm=MEDIAL_AXIS, minTransition=OFF)
p.setMeshControls(regions=(p.sets['Matrix'].faces), elemShape=QUAD)
"""
for ma in p.sets['Interface'].faces:
    mesh = []
    mesh.append(ma)
    p.setMeshControls(regions=(mesh), elemShape=QUAD, algorithm=MEDIAL_AXIS, minTransition=OFF)
    p.generateMesh(regions=(mesh))
    """
    p.setMeshControls(regions=p.sets['Ffiber'].faces, elemShape=TRI)
    p.generateMesh()
    #p.deleteMesh(regions=p.sets['Interface'].faces)
    #p.generateMesh(regions=p.sets['Interface'].faces)
    del a, mod.parts[partName].sets['Alt'],mod.parts[partName].sets['Matrix'],mod.parts[partName].sets['Interface'],mod.parts[partName].sets['Ffiber'],mod.parts[partName].sets['IFfiber']
"""