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
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(2.1905, 80.266), point1=(2.1905, 89.266))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(112.1905, 80.266), point1=(112.1905, 89.266))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(35.804, 6.6565), point1=(35.804, 15.6565))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(35.804, 116.6565), point1=(35.804, 125.6565))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(79.4105, 6.7097), point1=(79.4105, 15.7097))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(79.4105, 116.7097), point1=(79.4105, 125.7097))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(106.6857, 19.4019), point1=(106.6857, 28.4019))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(-3.3143, 19.4019), point1=(-3.3143, 28.4019))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(20.2549, 49.4006), point1=(20.2549, 58.4006))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(25.8955, 28.3693), point1=(25.8955, 37.3693))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(56.7783, 11.3049), point1=(56.7783, 20.3049))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(97.2776, 42.979), point1=(97.2776, 51.979))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(76.8181, 92.0767), point1=(76.8181, 101.0767))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(1.2857, 55.5801), point1=(1.2857, 64.5801))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(111.2857, 55.5801), point1=(111.2857, 64.5801))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(21.4856, 82.8729), point1=(21.4856, 91.8729))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(74.1112, 73.8321), point1=(74.1112, 82.8321))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(17.6847, 8.9468), point1=(17.6847, 17.9468))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(17.6847, 118.9468), point1=(17.6847, 127.9468))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(57.1491, 85.6411), point1=(57.1491, 94.6411))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(37.6101, 54.4833), point1=(37.6101, 63.4833))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(91.6449, 67.4065), point1=(91.6449, 76.4065))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(98.3292, 0.27816), point1=(98.3292, 9.2782))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(98.3292, 110.2782), point1=(98.3292, 119.2782))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(60.5003, 41.7656), point1=(60.5003, 50.7656))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(58.4263, 64.424), point1=(58.4263, 73.424))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(48.2917, 101.9059), point1=(48.2917, 110.9059))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(48.2917, -8.0941), point1=(48.2917, 0.90586))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(96.317, 90.9672), point1=(96.317, 99.9672))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(87.7254, 25.4292), point1=(87.7254, 34.4292))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(80.1711, 52.5781), point1=(80.1711, 61.5781))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(44.3591, 25.0286), point1=(44.3591, 34.0286))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(7.3728, 36.2823), point1=(7.3728, 45.2823))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(117.3728, 36.2823), point1=(117.3728, 45.2823))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(9.9664, 100.958), point1=(9.9664, 109.958))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(68.3246, 25.4774), point1=(68.3246, 34.4774))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(40.2635, 77.5997), point1=(40.2635, 86.5997))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(30.4528, 98.9898), point1=(30.4528, 107.9898))
# Interphase
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(2.1905, 80.266), point1=(2.1905, 89.276))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(112.1905, 80.266), point1=(112.1905, 89.276))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(35.804, 6.6565), point1=(35.804, 15.6665))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(35.804, 116.6565), point1=(35.804, 125.6665))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(79.4105, 6.7097), point1=(79.4105, 15.7197))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(79.4105, 116.7097), point1=(79.4105, 125.7197))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(106.6857, 19.4019), point1=(106.6857, 28.4119))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(-3.3143, 19.4019), point1=(-3.3143, 28.4119))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(20.2549, 49.4006), point1=(20.2549, 58.4106))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(25.8955, 28.3693), point1=(25.8955, 37.3793))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(56.7783, 11.3049), point1=(56.7783, 20.3149))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(97.2776, 42.979), point1=(97.2776, 51.989))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(76.8181, 92.0767), point1=(76.8181, 101.0867))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(1.2857, 55.5801), point1=(1.2857, 64.5901))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(111.2857, 55.5801), point1=(111.2857, 64.5901))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(21.4856, 82.8729), point1=(21.4856, 91.8829))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(74.1112, 73.8321), point1=(74.1112, 82.8421))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(17.6847, 8.9468), point1=(17.6847, 17.9568))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(17.6847, 118.9468), point1=(17.6847, 127.9568))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(57.1491, 85.6411), point1=(57.1491, 94.6511))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(37.6101, 54.4833), point1=(37.6101, 63.4933))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(91.6449, 67.4065), point1=(91.6449, 76.4165))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(98.3292, 0.27816), point1=(98.3292, 9.2882))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(98.3292, 110.2782), point1=(98.3292, 119.2882))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(60.5003, 41.7656), point1=(60.5003, 50.7756))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(58.4263, 64.424), point1=(58.4263, 73.434))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(48.2917, 101.9059), point1=(48.2917, 110.9159))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(48.2917, -8.0941), point1=(48.2917, 0.91586))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(96.317, 90.9672), point1=(96.317, 99.9772))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(87.7254, 25.4292), point1=(87.7254, 34.4392))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(80.1711, 52.5781), point1=(80.1711, 61.5881))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(44.3591, 25.0286), point1=(44.3591, 34.0386))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(7.3728, 36.2823), point1=(7.3728, 45.2923))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(117.3728, 36.2823), point1=(117.3728, 45.2923))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(9.9664, 100.958), point1=(9.9664, 109.968))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(68.3246, 25.4774), point1=(68.3246, 34.4874))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(40.2635, 77.5997), point1=(40.2635, 86.6097))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(30.4528, 98.9898), point1=(30.4528, 107.9998))
mdb.models['Model-1'].parts['RVE-3D'].PartitionFaceBySketch(faces=
    mdb.models['Model-1'].parts['RVE-3D'].faces.getSequenceFromMask(('[#10 ]',
    ), ), sketch=mdb.models['Model-1'].sketches['__profile__'], sketchUpEdge=
    mdb.models['Model-1'].parts['RVE-3D'].edges[7])
