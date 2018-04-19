"""Filen er laget for aa bli kjort av microscale scriptet"""
#   I denne filen lages en sketch av en RVE. Modellen kan ha fiber, med eller uten interfaces.

def LageRVEflate(model):
    s = model.ConstrainedSketch(name='__profile__', sheetSize=3 * dL)
    p = mod.Part(name=partName, dimensionality=THREE_D,
                 type=DEFORMABLE_BODY)

    s.Line(point1=(-dL/2, -dL/2), point2=(dL/2, -dL/2))
    s.Line(point1=(dL/2, -dL/2), point2=(dL/2, dL/2))
    s.Line(point1=(dL/2, dL/2), point2=(-dL/2, dL/2))
    s.Line(point1=(-dL/2, dL/2), point2=(-dL/2, -dL/2))
    p = model.parts[partName]
    p.BaseShell(sketch=s)
def SketcheInnFiber_Interface(model):
    p = mod.parts[partName]
    f1, e = p.faces, p.edges
    t = p.MakeSketchTransform(sketchPlane=f1.findAt(coordinates=(0.0, 0.0, 0.0), normal=(0.0, 0.0, 1.0)),
                              sketchUpEdge=e.findAt(coordinates=(dL/2, 0.0, 0.0)), sketchPlaneSide=SIDE1,
                              origin=(0.0, 0.0, 0.0))
    s1 = model.ConstrainedSketch(name='__profile__', sheetSize=2 * dL, gridSpacing=dL / 25.0, transform=t)
    s1.setPrimaryObject(option=SUPERIMPOSE)
    p.projectReferencesOntoSketch(sketch=s1,filter=COPLANAR_EDGES)
    # Tegne inn Fiber
    for data in xydata:
        x = data[0]
        y = data[1]
        r = rmean
        if Fibervariation:
            r = data[2]
        rcos45 = r * cos(45.0 * pi / 180.0)
        done = 0
        if done == 0 and x >= dL/2:
            s1.CircleByCenterPerimeter(center=(x, y), point1=(x + r, y))
            done = 1
        if done == 0 and x <= -dL/2:
            s1.CircleByCenterPerimeter(center=(x, y), point1=(x - r, y))
            done = 1
        if done == 0 and y >= dL/2:
            s1.CircleByCenterPerimeter(center=(x, y), point1=(x, y + r))
            done = 1
        if done == 0 and y <= -dL/2:
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
    # Tegne inn Interfaces
    if Interface:
        for data in xydata:
            x = data[0]
            y = data[1]
            r = rmean
            if Fibervariation:
                r = data[2]
            r = r * (1 + rinterface)
            rcos45 = r * cos(45.0 * pi / 180.0)
            done = 0
            if done == 0 and x >= dL/2:
                s1.CircleByCenterPerimeter(center=(x, y), point1=(x + r, y))
                done = 1
            if done == 0 and x <= -dL/2:
                s1.CircleByCenterPerimeter(center=(x, y), point1=(x - r, y))
                done = 1
            if done == 0 and y >= dL/2:
                s1.CircleByCenterPerimeter(center=(x, y), point1=(x, y + r))
                done = 1
            if done == 0 and y <= -dL/2:
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
    # Selve partioneringen
    f = p.faces
    square = f.findAt(((0.0, 0.0, 0.0),))
    e1 = p.edges
    p.PartitionFaceBySketch(sketchUpEdge=e1.findAt(coordinates=(dL/2, 0.0, 0.0)), faces=square, sketch=s1)

model = mdb.Model(name=modelName, modelType=STANDARD_EXPLICIT)          #   Lage part
global  mod
mod = mdb.models[modelName]

LageRVEflate(model)                                                     # Tegne RVE - Firkant
if not nf == 0:
    SketcheInnFiber_Interface(model)                                    # Partionere RVE - Fiber med eller uten interface
