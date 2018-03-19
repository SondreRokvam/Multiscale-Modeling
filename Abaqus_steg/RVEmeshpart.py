"""Filen er laget for aa bli kjort av microscale scriptet"""
# Definerer meshinstillinger og mesher. Lager Orphan mesh part

def LageFiberRegionSetsForMeshing():
    if not nf==0:
        p = mod.parts[partName]
        f = p.faces
        # Velge alle fiberregioner ved loope gjennom fiberdata.
        x = xydata[0][0]  # En iterasjon utfor loopen grunnet abaqus tull
        y = xydata[0][1]
        r = rmean
        if Fibervariation:
            r = xydata[0][2]
        Ffaces = f.getByBoundingCylinder((x, y, -10.0), (x, y, 10.0), r + tol)
        for i in range(1, len(xydata)):
            x = xydata[i][0]
            y = xydata[i][1]
            if Fibervariation:
                r = xydata[i][2]
            temp = f.getByBoundingCylinder((x, y, -10.0), (x, y, 10.0), r + tol)
            Ffaces = Ffaces + temp
        p.Set(name='Ffiber', faces=Ffaces)
        if Interface:  # Velge alle fiberregionerGenerate mesh med/uten interface set
            p = mod.parts[partName]
            f = p.faces
            p.Set(faces=f, name='Alt')  # Lag set for  Alt
            # Velge alle fiberregioner ved loope gjennom fiberdata.
            x = xydata[0][0]  # En iterasjon utfor loopen grunnet abaqus tull
            y = xydata[0][1]
            r = rmean
            if Fibervariation:
                r = xydata[0][2]
            IFfaces = f.getByBoundingCylinder((x, y, -10.0), (x, y, 10.0), r * (1 + rinterface) + tol)
            for i in range(1, len(xydata)):
                x = xydata[i][0]
                y = xydata[i][1]
                if Fibervariation:
                    r = xydata[i][2]
                temp = f.getByBoundingCylinder((x, y, -10.0), (x, y, 10.0), r * (1 + rinterface) + tol)
                IFfaces = IFfaces + temp
            p.Set(name='IFset', faces=IFfaces)
            p.SetByBoolean(name='Interface', sets=(p.sets['IFset'], p.sets['Ffiber'],), operation=DIFFERENCE)
            p.SetByBoolean(name='Matrix', sets=(p.sets['Alt'], p.sets['IFset'],), operation=DIFFERENCE)
            del mod.parts[partName].sets['IFset']
    else:   # Bare lage "Matrix" set.
        p = mod.parts[partName]
        p.SetByBoolean(name='Matrix', sets=(p.sets['Alt'], p.sets['Ffiber'],), operation=DIFFERENCE)
def meshOrphanRVEpart():
    p = mod.parts[partName]
    p.seedPart(size=meshsize, deviationFactor=0.1, minSizeFactor=0.1)
    if Interface:
        p = mod.parts[partName]
        for ma in p.sets['Interface'].faces:
            mosh = []
            mosh.append(ma)
            p.setMeshControls(regions=mosh, elemShape=QUAD, technique=SWEEP)
        del mod.parts[partName].sets['Interface']
    p = mod.parts[partName]
    p.setMeshControls(regions=p.sets['Ffiber'].faces, elemShape=TRI)
    p = mod.parts[partName]
    p.generateMesh()                                                                                     # Generate mesh

    elFace = mod.parts[partName].elementFaces                                                                   # Velge partens overflater for aa lage 3D
    v = ((0.0, 0.0, 0.0), (0.0, 0.0, 2 * tykkelse))
    p.generateBottomUpExtrudedMesh(elemFacesSourceSide=elFace, extrudeVector=v, numberOfLayers=2)
    p = mod.parts[partName]                                                                                 # Slette shell noder of part
    n = p.nodes
    nodes = n.getByBoundingBox(-dL, -dL, -0.01, dL, dL, 0.01)
    p.deleteNode(nodes=nodes)
    p.PartFromMesh(name=meshPartName, copySets=True)  # Make orphan mesh
    del mod.parts[partName].sets['Ffiber'], mod.parts[partName].sets['Matrix']
def meshOrphanSlabpart():
    p = mod.parts[partName]
    p.seedPart(size=meshsize, deviationFactor=0.1, minSizeFactor=0.1)
    p.generateMesh()                                                                                                # Generate mesh

def Extrude_and_create_orphanmesh():
    elFace = mod.parts[partName].elementFaces                                                                       # Velge partens overflater for aa extrude til 3D
    v = ((0.0, 0.0, 0.0), (0.0, 0.0, 2 * tykkelse))
    p = mod.parts[partName]
    p.generateBottomUpExtrudedMesh(elemFacesSourceSide=elFace, extrudeVector=v, numberOfLayers=2)
    n = p.nodes                                                                                                      # Slette shell noder of part
    nodes = n.getByBoundingBox(-dL, -dL, -0.01, dL, dL, 0.01)
    p.deleteNode(nodes=nodes)
    p.PartFromMesh(name=meshPartName, copySets=True)                                                                # Make orphan mesh

    # Lag set i Abaqus for "Alt"
p = mod.parts[partName]
f = p.faces
p.Set(faces=f, name='Alt')

if not nf == 0:
    LageFiberRegionSetsForMeshing()
    meshOrphanRVEpart()
else:
    meshOrphanSlabpart()
del mod.parts[partName].sets['Alt']
Extrude_and_create_orphanmesh()
