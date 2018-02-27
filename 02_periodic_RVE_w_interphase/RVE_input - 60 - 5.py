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
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(42.2303, 58.1324), point1=(42.2303, 67.1324))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(75.7413, 66.5938), point1=(75.7413, 75.5938))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(45.5674, 13.4016), point1=(45.5674, 22.4016))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(107.2342, 19.4625), point1=(107.2342, 28.4625))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(-2.7658, 19.4625), point1=(-2.7658, 28.4625))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(31.6852, 93.4043), point1=(31.6852, 102.4043))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(66.0007, 33.9207), point1=(66.0007, 42.9207))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(64.0706, 94.4007), point1=(64.0706, 103.4007))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(6.8177, 37.678), point1=(6.8177, 46.678))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(116.8177, 37.678), point1=(116.8177, 46.678))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(94.4, 99.9204), point1=(94.4, 108.9204))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(100.2952, 69.2367), point1=(100.2952, 78.2367))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(15.1726, 78.9687), point1=(15.1726, 87.9687))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(81.3621, 43.808), point1=(81.3621, 52.808))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(28.744, 3.9945), point1=(28.744, 12.9945))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(28.744, 113.9945), point1=(28.744, 122.9945))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(11.4624, 99.6273), point1=(11.4624, 108.6273))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(27.9306, 33.5221), point1=(27.9306, 42.5221))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(75.9172, 17.6436), point1=(75.9172, 26.6436))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(56.3966, 69.8636), point1=(56.3966, 78.8636))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(15.7398, 57.7749), point1=(15.7398, 66.7749))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(100.6964, 49.1408), point1=(100.6964, 58.1408))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(48.2013, 37.7452), point1=(48.2013, 46.7452))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(79.5051, 84.9376), point1=(79.5051, 93.9376))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(15.3366, 16.5785), point1=(15.3366, 25.5785))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(63.1931, 51.9889), point1=(63.1931, 60.9889))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(32.6856, 73.7881), point1=(32.6856, 82.7881))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(77.4038, 106.7731), point1=(77.4038, 115.7731))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(77.4038, -3.2269), point1=(77.4038, 5.7731))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(48.512, 104.6379), point1=(48.512, 113.6379))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(48.512, -5.3621), point1=(48.512, 3.6379))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(92.4406, 8.2988), point1=(92.4406, 17.2988))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(92.4406, 118.2988), point1=(92.4406, 127.2988))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(108.3384, 86.5254), point1=(108.3384, 95.5254))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(-1.6616, 86.5254), point1=(-1.6616, 95.5254))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(91.5871, 28.92), point1=(91.5871, 37.92))
# Interphase
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(42.2303, 58.1324), point1=(42.2303, 67.1424))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(75.7413, 66.5938), point1=(75.7413, 75.6038))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(45.5674, 13.4016), point1=(45.5674, 22.4116))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(107.2342, 19.4625), point1=(107.2342, 28.4725))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(-2.7658, 19.4625), point1=(-2.7658, 28.4725))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(31.6852, 93.4043), point1=(31.6852, 102.4143))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(66.0007, 33.9207), point1=(66.0007, 42.9307))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(64.0706, 94.4007), point1=(64.0706, 103.4107))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(6.8177, 37.678), point1=(6.8177, 46.688))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(116.8177, 37.678), point1=(116.8177, 46.688))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(94.4, 99.9204), point1=(94.4, 108.9304))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(100.2952, 69.2367), point1=(100.2952, 78.2467))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(15.1726, 78.9687), point1=(15.1726, 87.9787))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(81.3621, 43.808), point1=(81.3621, 52.818))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(28.744, 3.9945), point1=(28.744, 13.0045))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(28.744, 113.9945), point1=(28.744, 123.0045))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(11.4624, 99.6273), point1=(11.4624, 108.6373))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(27.9306, 33.5221), point1=(27.9306, 42.5321))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(75.9172, 17.6436), point1=(75.9172, 26.6536))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(56.3966, 69.8636), point1=(56.3966, 78.8736))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(15.7398, 57.7749), point1=(15.7398, 66.7849))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(100.6964, 49.1408), point1=(100.6964, 58.1508))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(48.2013, 37.7452), point1=(48.2013, 46.7552))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(79.5051, 84.9376), point1=(79.5051, 93.9476))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(15.3366, 16.5785), point1=(15.3366, 25.5885))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(63.1931, 51.9889), point1=(63.1931, 60.9989))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(32.6856, 73.7881), point1=(32.6856, 82.7981))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(77.4038, 106.7731), point1=(77.4038, 115.7831))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(77.4038, -3.2269), point1=(77.4038, 5.7831))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(48.512, 104.6379), point1=(48.512, 113.6479))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(48.512, -5.3621), point1=(48.512, 3.6479))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(92.4406, 8.2988), point1=(92.4406, 17.3088))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(92.4406, 118.2988), point1=(92.4406, 127.3088))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(108.3384, 86.5254), point1=(108.3384, 95.5354))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(-1.6616, 86.5254), point1=(-1.6616, 95.5354))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(91.5871, 28.92), point1=(91.5871, 37.93))
mdb.models['Model-1'].parts['RVE-3D'].PartitionFaceBySketch(faces=
    mdb.models['Model-1'].parts['RVE-3D'].faces.getSequenceFromMask(('[#10 ]',
    ), ), sketch=mdb.models['Model-1'].sketches['__profile__'], sketchUpEdge=
    mdb.models['Model-1'].parts['RVE-3D'].edges[7])
