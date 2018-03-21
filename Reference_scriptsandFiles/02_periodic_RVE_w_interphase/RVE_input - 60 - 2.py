# Input file - random periodic RVE 
# Abedin Gagani 2017 (c) 
from part import * 
from material import * 
from section import * 
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=220.0)
mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(0.0, 0.0),
    point2=(110.0, 110.0))
mdb.models['Model-1'].Part(dimensionality=THREE_D, name='RVE-3D', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].parts['RVE-3D'].BaseSolidExtrude(depth=0.2, sketch=
    mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']
mdb.models['Model-1'].ConstrainedSketch(gridSpacing=10.71, name='__profile__',
    sheetSize=428.48, transform=
    mdb.models['Model-1'].parts['RVE-3D'].MakeSketchTransform(
    sketchPlane=mdb.models['Model-1'].parts['RVE-3D'].faces[4],
    sketchPlaneSide=SIDE1,
    sketchUpEdge=mdb.models['Model-1'].parts['RVE-3D'].edges[7],
    sketchOrientation=RIGHT, origin=(0.0, 0.0, 0.2)))
mdb.models['Model-1'].parts['RVE-3D'].projectReferencesOntoSketch(filter=
    COPLANAR_EDGES, sketch=mdb.models['Model-1'].sketches['__profile__'])
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(10.9894, 105.2019), point1=(10.9894, 114.2019))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(10.9894, -4.7981), point1=(10.9894, 4.2019))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(68.4664, 9.5733), point1=(68.4664, 18.5733))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(91.7293, 15.5976), point1=(91.7293, 24.5976))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(4.0033, 56.9734), point1=(4.0033, 65.9734))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(114.0033, 56.9734), point1=(114.0033, 65.9734))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(74.9072, 39.2591), point1=(74.9072, 48.2591))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(92.9155, 62.3777), point1=(92.9155, 71.3777))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(38.5855, 59.1699), point1=(38.5855, 68.1699))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(18.8151, 23.4852), point1=(18.8151, 32.4852))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(80.9922, 102.7308), point1=(80.9922, 111.7308))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(80.9922, -7.2692), point1=(80.9922, 1.7308))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(2.0137, 86.1565), point1=(2.0137, 95.1565))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(112.0137, 86.1565), point1=(112.0137, 95.1565))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(22.238, 91.0628), point1=(22.238, 100.0628))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(63.3499, 90.8828), point1=(63.3499, 99.8828))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(22.3161, 46.1143), point1=(22.3161, 55.1143))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(68.3773, 57.0992), point1=(68.3773, 66.0992))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(39.4294, 13.4106), point1=(39.4294, 22.4106))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(53.8812, 29.9185), point1=(53.8812, 38.9185))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(43.4167, 94.4189), point1=(43.4167, 103.4189))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(18.1109, 69.7447), point1=(18.1109, 78.7447))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(2.6988, 36.2799), point1=(2.6988, 45.2799))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(112.6988, 36.2799), point1=(112.6988, 45.2799))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(89.5431, 86.4973), point1=(89.5431, 95.4973))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(54.335, 71.2102), point1=(54.335, 80.2102))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(0.5354, 16.8647), point1=(0.5354, 25.8647))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(110.5354, 16.8647), point1=(110.5354, 25.8647))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(93.4817, 38.9277), point1=(93.4817, 47.9277))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(102.0318, 104.4767), point1=(102.0318, 113.4767))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(-7.9682, 104.4767), point1=(-7.9682, 113.4767))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(102.0318, -5.5233), point1=(102.0318, 3.4767))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(-7.9682, -5.5233), point1=(-7.9682, 3.4767))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(29.3634, 108.0404), point1=(29.3634, 117.0404))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(29.3634, -1.9596), point1=(29.3634, 7.0404))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(74.6574, 75.912), point1=(74.6574, 84.912))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(34.6101, 32.3255), point1=(34.6101, 41.3255))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(53.0055, 109.7633), point1=(53.0055, 118.7633))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(53.0055, -0.23667), point1=(53.0055, 8.7633))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(35.9074, 77.5778), point1=(35.9074, 86.5778))
# Interphase
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(10.9894, 105.2019), point1=(10.9894, 114.2119))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(10.9894, -4.7981), point1=(10.9894, 4.2119))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(68.4664, 9.5733), point1=(68.4664, 18.5833))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(91.7293, 15.5976), point1=(91.7293, 24.6076))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(4.0033, 56.9734), point1=(4.0033, 65.9834))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(114.0033, 56.9734), point1=(114.0033, 65.9834))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(74.9072, 39.2591), point1=(74.9072, 48.2691))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(92.9155, 62.3777), point1=(92.9155, 71.3877))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(38.5855, 59.1699), point1=(38.5855, 68.1799))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(18.8151, 23.4852), point1=(18.8151, 32.4952))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(80.9922, 102.7308), point1=(80.9922, 111.7408))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(80.9922, -7.2692), point1=(80.9922, 1.7408))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(2.0137, 86.1565), point1=(2.0137, 95.1665))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(112.0137, 86.1565), point1=(112.0137, 95.1665))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(22.238, 91.0628), point1=(22.238, 100.0728))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(63.3499, 90.8828), point1=(63.3499, 99.8928))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(22.3161, 46.1143), point1=(22.3161, 55.1243))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(68.3773, 57.0992), point1=(68.3773, 66.1092))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(39.4294, 13.4106), point1=(39.4294, 22.4206))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(53.8812, 29.9185), point1=(53.8812, 38.9285))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(43.4167, 94.4189), point1=(43.4167, 103.4289))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(18.1109, 69.7447), point1=(18.1109, 78.7547))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(2.6988, 36.2799), point1=(2.6988, 45.2899))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(112.6988, 36.2799), point1=(112.6988, 45.2899))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(89.5431, 86.4973), point1=(89.5431, 95.5073))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(54.335, 71.2102), point1=(54.335, 80.2202))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(0.5354, 16.8647), point1=(0.5354, 25.8747))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(110.5354, 16.8647), point1=(110.5354, 25.8747))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(93.4817, 38.9277), point1=(93.4817, 47.9377))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(102.0318, 104.4767), point1=(102.0318, 113.4867))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(-7.9682, 104.4767), point1=(-7.9682, 113.4867))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(102.0318, -5.5233), point1=(102.0318, 3.4867))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(-7.9682, -5.5233), point1=(-7.9682, 3.4867))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(29.3634, 108.0404), point1=(29.3634, 117.0504))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(29.3634, -1.9596), point1=(29.3634, 7.0504))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(74.6574, 75.912), point1=(74.6574, 84.922))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(34.6101, 32.3255), point1=(34.6101, 41.3355))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(53.0055, 109.7633), point1=(53.0055, 118.7733))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(53.0055, -0.23667), point1=(53.0055, 8.7733))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(35.9074, 77.5778), point1=(35.9074, 86.5878))
mdb.models['Model-1'].parts['RVE-3D'].PartitionFaceBySketch(faces=
    mdb.models['Model-1'].parts['RVE-3D'].faces.getSequenceFromMask(('[#10 ]',
    ), ), sketch=mdb.models['Model-1'].sketches['__profile__'], sketchUpEdge=
    mdb.models['Model-1'].parts['RVE-3D'].edges[7])
