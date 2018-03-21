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
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(0.88575, 56.7192), point1=(0.88575, 65.7192))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(110.8858, 56.7192), point1=(110.8858, 65.7192))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(55.4862, 73.2832), point1=(55.4862, 82.2832))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(67.6288, 55.9875), point1=(67.6288, 64.9875))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(20.8229, 79.4986), point1=(20.8229, 88.4986))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(65.1995, 19.4421), point1=(65.1995, 28.4421))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(22.2796, 27.6113), point1=(22.2796, 36.6113))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(91.2408, 88.9805), point1=(91.2408, 97.9805))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(83.2979, 17.3969), point1=(83.2979, 26.3969))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(56.6299, 38.874), point1=(56.6299, 47.874))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(68.6856, 90.7266), point1=(68.6856, 99.7266))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(22.0923, 45.9051), point1=(22.0923, 54.9051))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(9.4494, 11.643), point1=(9.4494, 20.643))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(48.2282, 100.2813), point1=(48.2282, 109.2813))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(106.5169, 101.0397), point1=(106.5169, 110.0397))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(-3.4831, 101.0397), point1=(-3.4831, 110.0397))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(106.5169, -8.9603), point1=(106.5169, 0.039747))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(-3.4831, -8.9603), point1=(-3.4831, 0.039747))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(106.5071, 74.4424), point1=(106.5071, 83.4424))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(-3.4929, 74.4424), point1=(-3.4929, 83.4424))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(87.0544, 67.4104), point1=(87.0544, 76.4104))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(44.7373, 18.8157), point1=(44.7373, 27.8157))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(91.5732, 48.5992), point1=(91.5732, 57.5992))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(33.4495, 3.4002), point1=(33.4495, 12.4002))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(33.4495, 113.4002), point1=(33.4495, 122.4002))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(108.2615, 33.9996), point1=(108.2615, 42.9996))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(-1.7385, 33.9996), point1=(-1.7385, 42.9996))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(89.9275, 109.3353), point1=(89.9275, 118.3353))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(89.9275, -0.66468), point1=(89.9275, 8.3353))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(38.8249, 83.0693), point1=(38.8249, 92.0693))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(48.9903, 56.1637), point1=(48.9903, 65.1637))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(78.3387, 35.4021), point1=(78.3387, 44.4021))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(70.6959, 1.0786), point1=(70.6959, 10.0786))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(70.6959, 111.0786), point1=(70.6959, 120.0786))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(21.6824, 98.5186), point1=(21.6824, 107.5186))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(29.6903, 62.7771), point1=(29.6903, 71.7771))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(101.498, 15.0064), point1=(101.498, 24.0064))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(-8.502, 15.0064), point1=(-8.502, 24.0064))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(38.2542, 37.3238), point1=(38.2542, 46.3238))
# Interphase
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(0.88575, 56.7192), point1=(0.88575, 65.7292))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(110.8858, 56.7192), point1=(110.8858, 65.7292))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(55.4862, 73.2832), point1=(55.4862, 82.2932))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(67.6288, 55.9875), point1=(67.6288, 64.9975))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(20.8229, 79.4986), point1=(20.8229, 88.5086))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(65.1995, 19.4421), point1=(65.1995, 28.4521))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(22.2796, 27.6113), point1=(22.2796, 36.6213))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(91.2408, 88.9805), point1=(91.2408, 97.9905))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(83.2979, 17.3969), point1=(83.2979, 26.4069))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(56.6299, 38.874), point1=(56.6299, 47.884))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(68.6856, 90.7266), point1=(68.6856, 99.7366))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(22.0923, 45.9051), point1=(22.0923, 54.9151))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(9.4494, 11.643), point1=(9.4494, 20.653))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(48.2282, 100.2813), point1=(48.2282, 109.2913))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(106.5169, 101.0397), point1=(106.5169, 110.0497))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(-3.4831, 101.0397), point1=(-3.4831, 110.0497))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(106.5169, -8.9603), point1=(106.5169, 0.049747))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(-3.4831, -8.9603), point1=(-3.4831, 0.049747))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(106.5071, 74.4424), point1=(106.5071, 83.4524))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(-3.4929, 74.4424), point1=(-3.4929, 83.4524))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(87.0544, 67.4104), point1=(87.0544, 76.4204))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(44.7373, 18.8157), point1=(44.7373, 27.8257))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(91.5732, 48.5992), point1=(91.5732, 57.6092))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(33.4495, 3.4002), point1=(33.4495, 12.4102))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(33.4495, 113.4002), point1=(33.4495, 122.4102))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(108.2615, 33.9996), point1=(108.2615, 43.0096))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(-1.7385, 33.9996), point1=(-1.7385, 43.0096))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(89.9275, 109.3353), point1=(89.9275, 118.3453))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(89.9275, -0.66468), point1=(89.9275, 8.3453))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(38.8249, 83.0693), point1=(38.8249, 92.0793))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(48.9903, 56.1637), point1=(48.9903, 65.1737))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(78.3387, 35.4021), point1=(78.3387, 44.4121))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(70.6959, 1.0786), point1=(70.6959, 10.0886))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(70.6959, 111.0786), point1=(70.6959, 120.0886))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(21.6824, 98.5186), point1=(21.6824, 107.5286))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(29.6903, 62.7771), point1=(29.6903, 71.7871))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(101.498, 15.0064), point1=(101.498, 24.0164))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(-8.502, 15.0064), point1=(-8.502, 24.0164))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(38.2542, 37.3238), point1=(38.2542, 46.3338))
mdb.models['Model-1'].parts['RVE-3D'].PartitionFaceBySketch(faces=
    mdb.models['Model-1'].parts['RVE-3D'].faces.getSequenceFromMask(('[#10 ]',
    ), ), sketch=mdb.models['Model-1'].sketches['__profile__'], sketchUpEdge=
    mdb.models['Model-1'].parts['RVE-3D'].edges[7])
