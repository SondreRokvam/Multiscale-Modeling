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
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(31.5442, 18.7203), point1=(31.5442, 27.7203))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(99.3309, 84.5628), point1=(99.3309, 93.5628))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(75.2118, 92.8836), point1=(75.2118, 101.8836))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(45.9577, 2.132), point1=(45.9577, 11.132))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(45.9577, 112.132), point1=(45.9577, 121.132))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(50.9448, 64.659), point1=(50.9448, 73.659))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(0.60554, 68.8464), point1=(0.60554, 77.8464))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(110.6055, 68.8464), point1=(110.6055, 77.8464))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(63.0014, 30.2152), point1=(63.0014, 39.2152))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(77.3328, 52.6117), point1=(77.3328, 61.6117))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(23.5969, 99.6014), point1=(23.5969, 108.6014))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(1.6853, 32.139), point1=(1.6853, 41.139))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(111.6853, 32.139), point1=(111.6853, 41.139))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(28.115, 56.5213), point1=(28.115, 65.5213))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(91.3322, 4.2587), point1=(91.3322, 13.2587))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(91.3322, 114.2587), point1=(91.3322, 123.2587))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(91.896, 28.5327), point1=(91.896, 37.5327))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(7.1508, 49.7891), point1=(7.1508, 58.7891))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(117.1508, 49.7891), point1=(117.1508, 58.7891))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(81.3997, 74.8627), point1=(81.3997, 83.8627))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(43.2519, 33.6828), point1=(43.2519, 42.6828))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(55.9087, 96.2642), point1=(55.9087, 105.2642))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(24.7426, 79.8593), point1=(24.7426, 88.8593))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(77.22, 15.9845), point1=(77.22, 24.9845))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(97.6173, 50.6091), point1=(97.6173, 59.6091))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(13.9673, 5.2334), point1=(13.9673, 14.2334))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(13.9673, 115.2334), point1=(13.9673, 124.2334))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(6.8663, 89.1364), point1=(6.8663, 98.1364))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(116.8663, 89.1364), point1=(116.8663, 98.1364))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(107.603, 14.4561), point1=(107.603, 23.4561))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(-2.397, 14.4561), point1=(-2.397, 23.4561))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(107.66, 105.6499), point1=(107.66, 114.6499))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(-2.34, 105.6499), point1=(-2.34, 114.6499))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(107.66, -4.3501), point1=(107.66, 4.6499))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(-2.34, -4.3501), point1=(-2.34, 4.6499))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(22.9533, 38.5381), point1=(22.9533, 47.5381))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(62.7183, 79.4369), point1=(62.7183, 88.4369))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(58.1393, 47.9558), point1=(58.1393, 56.9558))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(68.214, 109.8363), point1=(68.214, 118.8363))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(68.214, -0.16366), point1=(68.214, 8.8363))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(43.2602, 81.0666), point1=(43.2602, 90.0666))
# Interphase
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(31.5442, 18.7203), point1=(31.5442, 27.7303))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(99.3309, 84.5628), point1=(99.3309, 93.5728))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(75.2118, 92.8836), point1=(75.2118, 101.8936))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(45.9577, 2.132), point1=(45.9577, 11.142))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(45.9577, 112.132), point1=(45.9577, 121.142))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(50.9448, 64.659), point1=(50.9448, 73.669))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(0.60554, 68.8464), point1=(0.60554, 77.8564))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(110.6055, 68.8464), point1=(110.6055, 77.8564))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(63.0014, 30.2152), point1=(63.0014, 39.2252))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(77.3328, 52.6117), point1=(77.3328, 61.6217))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(23.5969, 99.6014), point1=(23.5969, 108.6114))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(1.6853, 32.139), point1=(1.6853, 41.149))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(111.6853, 32.139), point1=(111.6853, 41.149))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(28.115, 56.5213), point1=(28.115, 65.5313))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(91.3322, 4.2587), point1=(91.3322, 13.2687))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(91.3322, 114.2587), point1=(91.3322, 123.2687))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(91.896, 28.5327), point1=(91.896, 37.5427))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(7.1508, 49.7891), point1=(7.1508, 58.7991))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(117.1508, 49.7891), point1=(117.1508, 58.7991))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(81.3997, 74.8627), point1=(81.3997, 83.8727))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(43.2519, 33.6828), point1=(43.2519, 42.6928))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(55.9087, 96.2642), point1=(55.9087, 105.2742))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(24.7426, 79.8593), point1=(24.7426, 88.8693))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(77.22, 15.9845), point1=(77.22, 24.9945))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(97.6173, 50.6091), point1=(97.6173, 59.6191))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(13.9673, 5.2334), point1=(13.9673, 14.2434))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(13.9673, 115.2334), point1=(13.9673, 124.2434))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(6.8663, 89.1364), point1=(6.8663, 98.1464))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(116.8663, 89.1364), point1=(116.8663, 98.1464))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(107.603, 14.4561), point1=(107.603, 23.4661))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(-2.397, 14.4561), point1=(-2.397, 23.4661))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(107.66, 105.6499), point1=(107.66, 114.6599))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(-2.34, 105.6499), point1=(-2.34, 114.6599))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(107.66, -4.3501), point1=(107.66, 4.6599))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(-2.34, -4.3501), point1=(-2.34, 4.6599))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(22.9533, 38.5381), point1=(22.9533, 47.5481))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(62.7183, 79.4369), point1=(62.7183, 88.4469))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(58.1393, 47.9558), point1=(58.1393, 56.9658))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(68.214, 109.8363), point1=(68.214, 118.8463))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(68.214, -0.16366), point1=(68.214, 8.8463))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(43.2602, 81.0666), point1=(43.2602, 90.0766))
mdb.models['Model-1'].parts['RVE-3D'].PartitionFaceBySketch(faces=
    mdb.models['Model-1'].parts['RVE-3D'].faces.getSequenceFromMask(('[#10 ]',
    ), ), sketch=mdb.models['Model-1'].sketches['__profile__'], sketchUpEdge=
    mdb.models['Model-1'].parts['RVE-3D'].edges[7])
