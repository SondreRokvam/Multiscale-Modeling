
from abaqus import *
from abaqusConstants import *
from random import *
from math import *
import numpy as np
import os
from odbAccess import *


#def lesePopulasjon():

def hentePopulation(coordpath):
        #Les fiber matrix populasjon
    xy=list()
    f = open(coordpath,'r')
    tekst = f.read()
    lines = tekst.split('\n')
        #lagre koordinater til stottefil
    for line in lines:
        data = line.split('\t')
        a = float(data[0])
        b = float(data[1])
        xy.append([a,b])

    return xy

#Lage fiber populasjon
def modelleresnitt(coordpath,iterasjonsgrense): #Lage fiber populasjon
    coord = list()
    books = list()  # liste for aa lagre frremgang paa iterasjonene i  prosessen

    flag = 0
    fVfforrige = 0
    nplassert = 0.0  # antall fiber plassert
    nkrasj = 0  # antall krasj
    sidepunkt = 0
    hjornepunkt = 0
    senterpunkt = 0
    dodpunkt = 0
    #print("dL =", round(dL, 1), "x,y =", round(dL / 2, 1))  # print storrelse og max x,y
    while nplassert< nf:
        frem = countsjikt(coord) / nf  # Forlopig fremdrift
        fvf = frem*Vf

        # se om systemet har mott krasj saa mange ganger at fibere skal shake up
        if nkrasj > iterasjonsgrense:
             # reset krasj for nytt forsok paa utplasseringen.
            if fVfforrige == fvf:
                flag = flag + 1
            if flag>10:
                flag=0
                #print 'Punktene random forflyttes. npp:', nplassert, 'fnnp:', countsjikt(), 'Vf:', round(fvf,3), ' av tot Vf:', Vf, 'tries:', len( books), 'krasjes:', nkrasj,
                coord = shakeitdown(coord)


            else:
                #print 'Punktene random forflyttes ned. npp:', nplassert, 'fnnp:', countsjikt(),'Vf:', round(fvf,3), ' av tot Vf:', Vf, 'tries:', len(books), 'krasjes:', nkrasj,'# fremdrift stanget:',flag,
                coord=shakeitdown(coord)
            fVfforrige = fvf
            nkrasj = 0

        #genererer nye fiberkoordinater"
        if nf<=1:
            x = 0.0
            y = 0.0
        else:
            x = dL * random() - dL * 0.5
            y = dL * random() - dL * 0.5
        # sjekke krasj
        if not krasj(x, y,coord):
            if iskantp(x, y): # Er koordinatet i hjornet?
                #Krasjer det med punkt i et annet hjorne?
                if x < 0 and y < 0 and not krasj(x,y, coord) and not krasj(x + dL, y, coord) and not krasj(x, y + dL,coord) and not krasj(x + dL,y + dL, coord):
                    coord.append([x, y])
                    coord.append([x + dL, y])
                    coord.append([x, y + dL])
                    coord.append([x + dL, y + dL])
                    # print ("ned, ven")
                    hjornepunkt = hjornepunkt + 1
                    nplassert = nplassert + 1
                    print "fiber +1", "nnp:", nplassert, 'fnnf:', countsjikt(coord), round(fvf, 3), ' av Vf:', Vf, 'tries:', len(books), 'krasjes:', nkrasj
                    flag = 0
                elif x >= 0 and y < 0 and not krasj(x,y, coord) and not krasj(x - dL, y, coord) and not krasj(x,y + dL,coord) and not krasj(x - dL, y + dL, coord):
                    coord.append([x, y])
                    coord.append([x - dL, y])
                    coord.append([x, y + dL])
                    coord.append([x - dL, y + dL])
                    # print ("ned, hoy")
                    hjornepunkt = hjornepunkt + 1
                    nplassert = nplassert + 1
                    print "fiber +1", "nnp:", nplassert, 'fnnf:', countsjikt(coord), round(fvf,3), ' av Vf:', Vf, 'tries:', len(books), 'krasjes:', nkrasj
                    flag = 0
                elif x < 0 and y >= 0 and not krasj(x,y, coord) and not krasj(x + dL, y, coord) and not krasj(x,y - dL, coord) and not krasj(x + dL,y - dL, coord):
                    coord.append((x, y))
                    coord.append((x + dL, y))
                    coord.append((x, y - dL))
                    coord.append((x + dL, y - dL))
                    # print ("opp, ven")
                    hjornepunkt = hjornepunkt + 1
                    nplassert = nplassert + 1
                    print "fiber +1", "nnp:", nplassert, 'fnnf:', countsjikt(coord), round(fvf,3), ' av Vf:', Vf, 'tries:', len(books), 'krasjes:', nkrasj
                    flag = 0
                elif x >= 0 and y >= 0 and not krasj(x,y, coord) and not krasj(x - dL, y, coord) and not krasj(x,y - dL,coord) and not krasj(x - dL,y - dL, coord):
                    coord.append([x, y])
                    coord.append([x - dL, y])
                    coord.append([x, y - dL])
                    coord.append([x - dL, y - dL])
                    # print ("opp, hoy")
                    hjornepunkt = hjornepunkt + 1
                    nplassert = nplassert + 1
                    print "fiber +1", "nnp:", nplassert, 'fnnf:', countsjikt(coord), round(fvf,3), ' av Vf:', Vf, 'tries:', len(books), 'krasjes:', nkrasj
                    flag = 0
                else:
                    nkrasj = nkrasj + 1


            # Kan koordinatet vere et sidepunkt? Krasjer det med punkter paa motsatt side?
            elif abs(x) > ytrekantgrense or abs(y) > ytrekantgrense:
                # print "sidepunkt"

                if x > ytrekantgrense and x >= 0 and not iskantp(x, y) and not krasj(x - dL, y, coord):
                    coord.append([x, y])
                    coord.append([x - dL, y])
                    nplassert = nplassert + 1
                    print "fiber +1", "nfiber:", nplassert, 'faktisk:', countsjikt(coord), round(fvf,3), ' av Vf:', Vf, 'tries:', len(books), 'krasjes:', nkrasj
                    flag = 0
                    sidepunkt = sidepunkt + 1
                    # print ("hoyreside punkt")

                elif x < -ytrekantgrense and x < 0 and not iskantp(x, y) and not krasj(x + dL, y, coord):
                    coord.append([x, y])
                    coord.append([x + dL, y])
                    nplassert = nplassert + 1
                    print "fiber +1", "nfiber:", nplassert, 'faktisk:', countsjikt(coord), round(fvf,3), ' av Vf:', Vf, 'tries:', len(books), 'krasjes:', nkrasj
                    flag = 0
                    sidepunkt = sidepunkt + 1
                    # print ("venstreside punkt")

                elif y > ytrekantgrense and y >= 0 and not iskantp(x, y) and not krasj(x, y - dL, coord):
                    coord.append([x, y])
                    coord.append([x, y - dL])
                    nplassert = nplassert + 1
                    print "fiber +1", "nfiber:", nplassert, 'faktisk:', countsjikt(coord), round(fvf,3), ' av Vf:', Vf, 'tries:', len(books), 'krasjes:', nkrasj
                    flag = 0
                    sidepunkt = sidepunkt + 1
                    # print ("topp punkt")

                elif y < -ytrekantgrense and y < 0 and not iskantp(x, y) and not krasj(x, y + dL, coord):
                    coord.append([x, y])
                    coord.append([x, y + dL])
                    nplassert = nplassert + 1
                    print "fiber +1", "nfiber:", nplassert, 'faktisk:', countsjikt(coord), round(fvf,3), ' av Vf:', Vf, 'tries:', len(books), 'krasjes:', nkrasj
                    flag = 0
                    sidepunkt = sidepunkt + 1
                    # print ("bunn punkt")
                else:
                    nkrasj = nkrasj + 1

            # Er koordinatet i "dodsonen" og derfor ubrukelig?
            elif indrekantgrense < abs(x) or indrekantgrense < abs(y):
                #print "dodzonepunkt"
                dodpunkt = dodpunkt + 1
                nkrasj = nkrasj + 1

                """senterpunkt"""  # Ellers er det i midten!
            else:
                #print "senterpunkt"
                coord.append([x, y])
                senterpunkt = senterpunkt + 1
                nplassert = nplassert + 1
                print "fiber +1", "nfiber:", nplassert, 'faktisk:', countsjikt(coord), round(fvf,3), ' av Vf:', Vf, 'tries:', len(books), 'krasjes:', nkrasj
                flag=0
        else:
            nkrasj = nkrasj + 1
        books.append(nplassert)  # keeping record of amount of tries
    g = open(coordpath, "w")
    for l in range(0, len(coord)):
        g.write(str(coord[l][0]) + '\t' + str(coord[l][1]))
        if l < (len(coord) - 1):
            g.write('\n')
    g.close()
    #print str(countsjikt(coord)), 'av nf '+str(nf)
    del flag
    del fVfforrige
    del nplassert  # antall fiber plassert
    del nkrasj  # antall krasj
    del sidepunkt
    del hjornepunkt
    del senterpunkt
    del dodpunkt
    del coord
    del books

def krasj(x, y, coord):
    for c in coord:
        xp, yp = c[0], c[1]
        if sqrt((x - xp) ** 2 + (y - yp) ** 2) < 2 * (r + rtol):
            return True

    return False
def countsjikt(coord):
    i_sjikt = 0.0
    for i in range(len(coord)):
        if abs(coord[i][0]) <= dL / 2 and abs(coord[i][1]) <= dL / 2:
            i_sjikt = i_sjikt + 1.0
    return i_sjikt

def issidep(x, y):
    if abs(x)>ytrekantgrense and abs(y)<indrekantgrense:
        return True
    elif abs(x)<ytrekantgrense and abs(y)>indrekantgrense:
        return True
    else:
        return False
def iskantp(x, y):
    if abs(x)>ytrekantgrense and abs(y)>ytrekantgrense:
        return True
    else:
        return False


def shakeitdown(coord):
    for k in range(0,20):
        t = 0
        for c in coord:
            i = list()
            i.append([dL * 2, dL * 2])
            x, y = c[0], c[1]
            if indrekantgrense > abs(x) and indrekantgrense > abs(y):
                coord[t] = i[0]
                for j in range(0, 100):
                    xp, yp = [x + wiggle * random() - wiggle * 0.5, y + wiggle * random() - wiggle * 0.65]
                    if not krasj(xp,yp, coord) and indrekantgrense > abs(xp) and indrekantgrense > abs(yp):
                        coord[t] = [xp,yp]
                        break
                    coord[t] = [x,y]
            t = t +1
    return coord
def shakeitrand(coord):
    for k in range(0,20):
        t = 0
        for c in coord:
            i = list()
            i.append([dL * 2, dL * 2])
            x, y = c[0], c[1]
            if indrekantgrense > abs(x) and indrekantgrense > abs(y):
                coord[t] = i[0]
                for j in range(0, 100):
                    xp, yp = [x + wiggle * random() - wiggle * 0.5, y + wiggle * random() - wiggle * 0.5]
                    if not krasj(xp,yp) and indrekantgrense > abs(xp) and indrekantgrense > abs(yp):
                        coord[t] = [xp,yp]
                        break
                    coord[t] = [x,y]
            t = t +1
    return coord

def fiberdistances(dL,xydata):
    fibers=list()
    dists=list()
    for data in xydata:
        x=data[0]
        y=data[1]
        if x<dL/2 and y<dL/2:
            fibers.append([x,y])
    rep=len(fibers)
    for i in range(0,rep) :
        for j in range(0,rep):
            if not i==j: # since that would just be self-intersection...
                dx = fibers[i][0]-fibers[j][0]
                dy = fibers[i][1]-fibers[j][1]
                d = sqrt(dx**2+dy**2)
                dists.append([d])
    avg = np.mean(dists)
    print avg/(dL)
    return dists, avg

def createModel(newModelName,xydata,LX,LY,rf,nf, meshsize):
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    #Reset session

    Mdb()
    model =mdb.Model(name=newModelName, modelType=STANDARD_EXPLICIT)
    del mdb.models['Model-1']

    s1 = model.ConstrainedSketch(name='__profile__', 
        sheetSize=LX)
    s1.setPrimaryObject(option=STANDALONE)



    dx=LX/2.0
    dy=LY/2.0

    #Tegne Firkant
    s1.Line(point1=(-dx, -dy), point2=(dx, -dy))
    s1.Line(point1=(dx, -dy), point2=(dx, dy))
    s1.Line(point1=(dx,dy), point2=(-dx,dy))
    s1.Line(point1=(-dx,dy), point2=(-dx,-dy))
    p = model.Part(name='Part-1', dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
    p = model.parts['Part-1']
    p.BaseShell(sketch=s1)
    s1.unsetPrimaryObject()
    del model.sketches['__profile__']


    if not nf == 0:
        f1, e, d1 = p.faces, p.edges, p.datums
        t = p.MakeSketchTransform(sketchPlane=f1.findAt(coordinates=(0.0,
            0.0, 0.0), normal=(0.0, 0.0, 1.0)), sketchUpEdge=e.findAt(
            coordinates=(dx, 0.0, 0.0)), sketchPlaneSide=SIDE1, origin=(0.0,
            0.0, 0.0))
        s1 = model.ConstrainedSketch(name='__profile__',
            sheetSize=LX, gridSpacing=LX/20.0, transform=t)
        s1.setPrimaryObject(option=SUPERIMPOSE)
        p.projectReferencesOntoSketch(sketch=s1, filter=COPLANAR_EDGES)

        rcos45=rf*cos(45.0*pi/180.0)
        for data in xydata:
           x=data[0]
           y=data[1]
           done=0
           if done==0 and x>=dx:
              s1.CircleByCenterPerimeter(center=(x,y), point1=(x+rf,y))
              done=1
           if done==0 and x<=-dx:
              s1.CircleByCenterPerimeter(center=(x,y), point1=(x-rf,y))
              done=1
           if done==0 and y>=dx:
              s1.CircleByCenterPerimeter(center=(x,y), point1=(x,y+rf))
              done=1
           if done==0 and y<=-dx:
              s1.CircleByCenterPerimeter(center=(x,y), point1=(x,y-rf))
              done=1

           if done==0 and x>=0 and y>=0:
              s1.CircleByCenterPerimeter(center=(x,y), point1=(x-rcos45,y-rcos45))
              done=1
           if done==0 and x>=0 and y<=0:
              s1.CircleByCenterPerimeter(center=(x,y), point1=(x-rcos45,y+rcos45))
              done=1
           if done==0 and x<=0 and y<=0:
              s1.CircleByCenterPerimeter(center=(x,y), point1=(x+rcos45,y+rcos45))
              done=1
           if done==0 and x<=0 and y>=0:
              s1.CircleByCenterPerimeter(center=(x,y), point1=(x+rcos45,y-rcos45))
              done=1

        #Create partioned planar shell from sketch
        f = p.faces
        pickedFaces = f.findAt(((0.0, 0.0, 0.0), ))
        e1, d2 = p.edges, p.datums
        p.PartitionFaceBySketch(sketchUpEdge=e1.findAt(coordinates=(dx, 0.0,
            0.0)), faces=pickedFaces, sketch=s1)
        s1.unsetPrimaryObject()
        del model.sketches['__profile__'], f,pickedFaces,e1,d2,f1, e, d1,t
    del s1,p, model

    #print 'Created Partioned planar shell'

    #del mdb.models['Model-1']
    #meshe

    p = mdb.models['Model-A'].parts['Part-1']
    p.seedPart(size=meshsize, deviationFactor=0.1, minSizeFactor=0.1)
    p = mdb.models['Model-A'].parts['Part-1']
    p.generateMesh()
    p = mdb.models['Model-A'].parts['Part-1']
    #print 'meshed'
    #if nf==30:


    mdb.meshEditOptions.setValues(enableUndo=True, maxUndoCacheElements=0.5)
    pickedElemFacesSourceSide = mdb.models['Model-A'].parts['Part-1'].elementFaces
    vector =((0.0, 0.0, 0.0), (0.0, 0.0, 2.0))
    p.generateBottomUpExtrudedMesh(elemFacesSourceSide=pickedElemFacesSourceSide,
        extrudeVector=vector, numberOfLayers=2)
    p = mdb.models['Model-A'].parts['Part-1']
    p.PartFromMesh(name='Part-1-mesh-1', copySets=True)
    del mdb.models['Model-A'].parts['Part-1']
    p = mdb.models['Model-A'].parts['Part-1-mesh-1']
    n = p.nodes
    nodes = n.getByBoundingBox(-dL, -dL, -0.01, dL , dL, 0.01)
    p.deleteNode(nodes=nodes)

    #print 'Created extruded mesh part'

    #Debugging abaqus tool :)#del mdb.models['Model-1']

    if not nf == 0:
        #This is where the fibers are chosen and put together in set
        p = mdb.models['Model-A'].parts['Part-1-mesh-1']
        p.Set(name='AllE', elements=p.elements)
        x=xydata[0][0]
        y=xydata[0][1]
        fiber = p.elements.getByBoundingCylinder((x,y,-10.0),(x,y,10.0),r+0.01)
        for i in range(1,len(xydata)):
            x=xydata[i][0]
            y=xydata[i][1]
            temp = p.elements.getByBoundingCylinder((x,y,-10.0),(x,y,10.0),r+0.01)
            fiber=fiber+temp
        p.Set(name='Fibers',elements=fiber)
        p.SetByBoolean(name='Matrix', sets=(p.sets['AllE'], p.sets['Fibers'],), operation=DIFFERENCE)

        mdb.models['Model-A'].Material(name='glass')
        mdb.models['Model-A'].materials['glass'].Elastic(table=((70000.0, 0.22), ))
        mdb.models['Model-A'].Material(name='resin')
        mdb.models['Model-A'].materials['resin'].Elastic(table=((3500.0, 0.33), ))
        mdb.models['Model-A'].HomogeneousSolidSection(name='Fibers', material='glass',
            thickness=None)
        mdb.models['Model-A'].HomogeneousSolidSection(name='matrix', material='resin',
            thickness=None)

        p = mdb.models['Model-A'].parts['Part-1-mesh-1']
        region = p.sets['Fibers']
        p = mdb.models['Model-A'].parts['Part-1-mesh-1']
        p.SectionAssignment(region=region, sectionName='Fibers', offset=0.0,
            offsetType=MIDDLE_SURFACE, offsetField='',
            thicknessAssignment=FROM_SECTION)
        p = mdb.models['Model-A'].parts['Part-1-mesh-1']
        region = p.sets['Matrix']
        p = mdb.models['Model-A'].parts['Part-1-mesh-1']
        p.SectionAssignment(region=region, sectionName='matrix', offset=0.0,
            offsetType=MIDDLE_SURFACE, offsetField='',
            thicknessAssignment=FROM_SECTION)
    else:
        # This is where the fibers are chosen and put together in set
        p = mdb.models['Model-A'].parts['Part-1-mesh-1']
        p.Set(name='Matrix', elements=p.elements)

        mdb.models['Model-A'].Material(name='resin')
        mdb.models['Model-A'].materials['resin'].Elastic(table=((3500.0, 0.33),))
        mdb.models['Model-A'].HomogeneousSolidSection(name='matrix', material='resin',
                                                      thickness=None)

        p = mdb.models['Model-A'].parts['Part-1-mesh-1']
        region = p.sets['Matrix']
        p = mdb.models['Model-A'].parts['Part-1-mesh-1']
        p.SectionAssignment(region=region, sectionName='matrix', offset=0.0,
                            offsetType=MIDDLE_SURFACE, offsetField='',
                            thicknessAssignment=FROM_SECTION)

def createCEq(dL,modelName,instanceName):

    a = mdb.models[modelName].rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    p = mdb.models[modelName].parts['Part-1-mesh-1']
    a.Instance(name=instanceName, part=p, dependent=ON)

    a = mdb.models['Model-A'].rootAssembly
    a.translate(instanceList=(instanceName, ), vector=(0.0, 0.0, -1.0))

    a = mdb.models['Model-A'].rootAssembly
    a.rotate(instanceList=(instanceName, ), axisPoint=(0.0, 0.0, 0.0),
        axisDirection=(0.0, 1.0, 0.0), angle=90.0)
    tol = 0.01

    mod = mdb.models[modelName]
    a = mod.rootAssembly
    allNodes = a.instances[instanceName].nodes



    # Finding the dimensions
    xmax, ymax, zmax, xmin, ymin, zmin = 1.0, dL/2, dL/2, 0.0, -dL/2, -dL/2
    # Debugging abaqus tool :)
    #del mdb.models['Model-1']
    for n in allNodes:
        x, y, z = n.coordinates[0], n.coordinates[1], n.coordinates[2]
        xmax = max(xmax, x)
        ymax = max(ymax, y)
        zmax = max(zmax, z)
        xmin = min(xmin, x)
        ymin = min(ymin, y)
        zmin = min(zmin, z)
    #print xmax, ymax, zmax, xmin, ymin, zmin

    # Creating reference point

    a.ReferencePoint(point=( xmin - 0.2 * (zmax - zmin),0.0,  0.0))
    refPoints = (a.referencePoints[a.features['RP-1'].id],)
    a.Set(referencePoints=refPoints, name='RPX')

    a.ReferencePoint(point=(0.0, ymin - 0.2 * (ymax - ymin), 0.0))
    refPoints = (a.referencePoints[a.features['RP-2'].id],)
    a.Set(referencePoints=refPoints, name='RPY')

    a.ReferencePoint(point=(0.0, 0.0,zmin - 0.2 * (zmax - zmin)))
    refPoints = (a.referencePoints[a.features['RP-3'].id],)
    a.Set(referencePoints=refPoints, name='RPZ')

    # CE between x-normal surfaces:

    nodesXa = allNodes.getByBoundingBox(xmin - tol, ymin - tol, zmin - tol, xmin + tol, ymax + tol, zmax + tol)
    nodesXb = allNodes.getByBoundingBox(xmax - tol, ymin - tol, zmin - tol, xmax + tol, ymax + tol, zmax + tol)

    counter = 0

    for n in nodesXa:
        name1 = "Xa%i" % (counter)
        nodes1 = nodesXa[counter:counter + 1]
        a.Set(nodes=nodes1, name=name1)
        x, y, z = n.coordinates[0], n.coordinates[1], n.coordinates[2]
        name2 = "Xb%i" % (counter)
        nodes2 = nodesXb.getByBoundingBox(x + (xmax - xmin) - tol, y - tol, z - tol, x + (xmax - xmin) + tol, y + tol,
                                          z + tol)
        a.Set(nodes=nodes2, name=name2)

        mod.Equation(name="Cq11x%i" % (counter),
                     terms=((1.0, name2, 1), (-1.0, name1, 1), (-(xmax - xmin), 'RPX', 1),))  # 11
        mod.Equation(name="Cq21x%i" % (counter),
                     terms=((1.0, name2, 2), (-1.0, name1, 2), (-(xmax - xmin) / 2, 'RPX', 2),))  # 21
        mod.Equation(name="Cq31x%i" % (counter),
                     terms=((1.0, name2, 3), (-1.0, name1, 3), (-(xmax - xmin) / 2, 'RPX', 3),))  # 31

        counter = counter + 1

        # CE between y-normal surfaces
    # Note: excluding the nodes at xmax:

    nodesYa = allNodes.getByBoundingBox(xmin - tol, ymin - tol, zmin - tol, xmax - tol, ymin + tol, zmax + tol)
    nodesYb = allNodes.getByBoundingBox(xmin - tol, ymax - tol, zmin - tol, xmax - tol, ymax + tol, zmax + tol)

    counter = 0

    for n in nodesYa:
        name1 = "Ya%i" % (counter)
        nodes1 = nodesYa[counter:counter + 1]
        a.Set(nodes=nodes1, name=name1)
        x, y, z = n.coordinates[0], n.coordinates[1], n.coordinates[2]
        name2 = "Yb%i" % (counter)
        nodes2 = nodesYb.getByBoundingBox(x - tol, y + (ymax - ymin) - tol, z - tol, x + tol, y + (ymax - ymin) + tol,
                                          z + tol)
        a.Set(nodes=nodes2, name=name2)

        mod.Equation(name="Cq12y%i" % (counter),
                     terms=((1.0, name2, 1), (-1.0, name1, 1), (-(ymax - ymin) / 2, 'RPY', 1),))  # 12
        mod.Equation(name="Cq22y%i" % (counter),
                     terms=((1.0, name2, 2), (-1.0, name1, 2), (-(ymax - ymin), 'RPY', 2),))  # 22
        mod.Equation(name="Cq32y%i" % (counter),
                     terms=((1.0, name2, 3), (-1.0, name1, 3), (-(ymax - ymin) / 2, 'RPY', 3),))  # 32

        counter = counter + 1

        # CE between z-normal surfaces
    # Note: excluding the nodes at xmax and ymax :

    nodesZa = allNodes.getByBoundingBox(xmin - tol, ymin - tol, zmin - tol, xmax - tol, ymax - tol, zmin + tol)
    nodesZb = allNodes.getByBoundingBox(xmin - tol, ymin - tol, zmax - tol, xmax - tol, ymax - tol, zmax + tol)

    counter = 0

    for n in nodesZa:
        name1 = "Za%i" % (counter)
        nodes1 = nodesZa[counter:counter + 1]
        a.Set(nodes=nodes1, name=name1)
        x, y, z = n.coordinates[0], n.coordinates[1], n.coordinates[2]
        name2 = "Zb%i" % (counter)
        nodes2 = nodesZb.getByBoundingBox(x - tol, y - tol, z + (zmax - zmin) - tol, x + tol, y + tol,
                                          z + (zmax - zmin) + tol)
        a.Set(nodes=nodes2, name=name2)

        mod.Equation(name="Cq13z%i" % (counter),
                     terms=((1.0, name2, 1), (-1.0, name1, 1), (-(zmax - zmin) / 2, 'RPZ', 1),))  # 13
        mod.Equation(name="Cq23z%i" % (counter),
                     terms=((1.0, name2, 2), (-1.0, name1, 2), (-(zmax - zmin) / 2, 'RPZ', 2),))  # 23
        mod.Equation(name="Cq33z%i" % (counter),
                     terms=((1.0, name2, 3), (-1.0, name1, 3), (-(zmax - zmin), 'RPZ', 3),))  # 33

        counter = counter + 1


def get_stiffness(dL,id,stepName,jobName,instanceName,lagrestiffma):
    mod = mdb.models[modelName]
    a = mod.rootAssembly


    #Create step
    #mdb.models[modelName].StaticStep(name=stepName, previous='Initial', nlgeom=ON)
    mdb.models[modelName].StaticStep(name=stepName, previous='Initial')

    #request Filed outputs
    mdb.models[modelName].fieldOutputRequests['F-Output-1'].setValues(variables=(
        'S', 'EVOL','U'))

    #Create stiffnessmatrix
    stiffmatix = list()
    for i in range(0,6):#   arg:   +   ,len(id)+1
        path = 'C:/Temp/'+jobName[i]
        #print 'Job '+jobName[i], path+'.odb'

        exx, eyy, ezz, exy, exz, eyz = id[i]

        mod.DisplacementBC(name='BCX', createStepName=stepName,
                           region=a.sets['RPX'], u1=exx, u2=exy, u3=exz, ur1=UNSET, ur2=UNSET, ur3=UNSET,
                           amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)
        mod.DisplacementBC(name='BCY', createStepName=stepName,
                           region=a.sets['RPY'], u1=exy, u2=eyy, u3=eyz, ur1=UNSET, ur2=UNSET, ur3=UNSET,
                           amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)
        mod.DisplacementBC(name='BCZ', createStepName=stepName,
                           region=a.sets['RPZ'], u1=exz, u2=eyz, u3=ezz, ur1=UNSET, ur2=UNSET, ur3=UNSET,
                           amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)
        mdb.Job(name=jobName[i], model=modelName, description='', type=ANALYSIS,
            atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90,
            memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True,
            explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF,
            modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='',
            scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1,
            numGPUs=0)

        try:
            os.chmod(path+'.lck', 0o755)
        except OSError:
            pass
        try:
            os.chmod(path+'.odb', 0o755)
        except OSError:
            pass
        try:
            os.remove(path+'.lck')
        except OSError:
            pass
        try:
            os.remove(path+'.odb')
        except OSError:
            pass

        mdb.jobs[jobName[i]].submit(consistencyChecking=OFF)
        mdb.jobs[jobName[i]].waitForCompletion()
        odb = session.openOdb(path+'.odb')
        instance = odb.rootAssembly.instances[instanceName]

        sag=[0.0] * 6
        #volume = 0
        #elemlist = []
        for j in range(0,len(instance.elements)):
            v = odb.steps[stepName].frames[-1].fieldOutputs['S'].getSubset(position=CENTROID)
            elvol = odb.steps[stepName].frames[-1].fieldOutputs['EVOL']
            #volume = volume + elvol.values[j].data
            #elem = instance.elements[j].label
            #sig1 = v.values[0].data[0]
            #sig2 = v.values[0].data[1]
            #sig3 = v.values[0].data[2]
            #tau12 = v.values[0].data[3]
            #tau13 = v.values[0].data[4]
            #tau23 = v.values[0].data[5]
            #elemlist.append(elem)
            for p in range(0,6):
                sag[p] = sag[p]+v.values[j].data[p]*elvol.values[j].data
        odb.close()
        for k in range(0,6):
            sag[k]= sag[k]/(1*(dL)**2) #Volume
        stiffmatix.append(sag)

    g = open(lagrestiffma, "w")
    for a in range(0, 6):
        g.write(str(stiffmatix[0][a]) + '\t'+ '\t' + str(stiffmatix[1][a]) + '\t'+ '\t' + str(stiffmatix[2][a]) + '\t'+ '\t' + str(stiffmatix[3][a]) + '\t'+ '\t' + str(stiffmatix[4][a]) + '\t'+ '\t' + str(stiffmatix[5][a])+'\n')
        print '%7f \t %7f \t %7f \t %7f \t %7f \t %7f' % (stiffmatix[0][a], stiffmatix[1][a], stiffmatix[2][a], stiffmatix[3][a], stiffmatix[4][a], stiffmatix[5][a])
    g.close()


"""ALT OVER ER FUNKSJONER"""




"""PARAMETERE"""
#seed(21) #random funksjon nokkel
Vf = 0.65
nf = 2.0
r = 1.0
rtol = 0.025 * r
gtol = r * 0.1
dL = ((nf * pi * r ** 2) / (Vf)) ** 0.5
if nf==0:
    dL=10
ytrekantgrense = (dL / 2) - r + gtol
indrekantgrense = (dL / 2) - r - gtol
wiggle = random()*r

iterasjonsgrense = 10000  # max antall plasseringsforsok per fiber


"""Stottefiler"""
coordpath = 'C:\Users\Sondre\Desktop\coordst.txt'
lagrestiffma = 'C:\Users\Sondre\Desktop\Stiffness.txt'


"""Prosess"""



modelleresnitt(coordpath,iterasjonsgrense)
 #create a random population
if not nf==0:
    xydata=hentePopulation(coordpath)
else:
    xydata= [None] *2
modelName = 'Model-A'
instanceName = 'PART-1-MESH-1-1'
stepName = 'Enhetstoyninger'
meshsize= r*0.2
id = np.identity(6) #Identity matrix for normalised load cases.'Exx','Eyy','Ezz','Exy','Exz','Eyz'
Toying = ['Exx','Eyy','Ezz','Exy','Exz','Eyz'] #Enhetstoyingene fra 0 til 5. Altsaa alle 6
#print 'fiber coordinates found' ,nf, len(xydata)
# In abaqus
createModel(modelName,xydata,dL,dL,r,nf, meshsize)
createCEq(dL,modelName,instanceName)

get_stiffness(dL, id,stepName,Toying,instanceName,lagrestiffma)

#stats
if not nf<=1:
    fiberdist, avgfdist = fiberdistances(dL,xydata)
analyticalfiberdist = 0.521

session.mdbData.summary()
o1 = session.openOdbs(names=('C:/Temp/Exx.odb', 'C:/Temp/Exy.odb',
                             'C:/Temp/Exz.odb', 'C:/Temp/Eyy.odb', 'C:/Temp/Eyz.odb',
                             'C:/Temp/Ezz.odb'))
session.viewports['Viewport: 1'].setValues(displayedObject=o1)
