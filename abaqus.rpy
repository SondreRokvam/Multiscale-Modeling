# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 6.14-4 replay file
# Internal Version: 2015_06_11-22.41.13 135079
# Run by Blue on Sun Apr 15 04:20:44 2018
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(1.55729, 1.55556), width=229.233, 
    height=154.311)
session.viewports['Viewport: 1'].makeCurrent()
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
execfile('C:/Multiscale-Modeling/MicroscaleModelling_randomSweep.py', 
    __main__.__dict__)
#: %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#: Multiscale Modelling, Microscale  
#: 10
#: Model: C:/Temp/ShearExy.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     1
#: Number of Meshes:             2
#: Number of Element Sets:       22
#: Number of Node Sets:          2600
#: Number of Steps:              1
#* VisError: No xy data was extracted using the provided options.
#* File "C:/Multiscale-Modeling/MicroscaleModelling_randomSweep.py", line 240, 
#* in <module>
#*     execfile(GitHub + Abaqus + 'nonLinearAnalysis.py')
#* File "C:/Multiscale-Modeling/Abaqus_steg/nonLinearAnalysis.py", line 70, in 
#* <module>
#*     getAverageStressStrain()
#* File "C:/Multiscale-Modeling/Abaqus_steg/nonLinearAnalysis.py", line 43, in 
#* getAverageStressStrain
#*     elementSets=('PART-1-MESH-1-1.INTERFACES', 'PART-1-MESH-1-1.MATRIX',
