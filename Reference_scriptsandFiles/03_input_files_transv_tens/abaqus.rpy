# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 6.14-4 replay file
# Internal Version: 2015_06_11-22.41.13 135079
# Run by Blue on Tue Apr 10 18:03:14 2018
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=103.95573425293, 
    height=99.0393447875977)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
openMdb('RVE1.cae')
#: The model database "C:\Multiscale-Modeling\03_input_files_transv_tens\RVE1.cae" has been opened.
session.viewports['Viewport: 1'].setValues(displayedObject=None)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
p = mdb.models['Model-1'].parts['Part-1']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
session.viewports['Viewport: 1'].view.setValues(nearPlane=215.187, 
    farPlane=423.628, width=383.522, height=157.765, viewOffsetX=13.1095, 
    viewOffsetY=2.67687)
session.viewports['Viewport: 1'].view.setValues(nearPlane=238.357, 
    farPlane=373.558, width=424.819, height=174.753, cameraPosition=(129.542, 
    91.8832, 294.537), cameraUpVector=(-0.137712, 0.895742, -0.422708), 
    cameraTarget=(51.3526, 53.6941, -12.7882), viewOffsetX=14.5211, 
    viewOffsetY=2.96511)
o1 = session.openOdb(
    name='C:/Multiscale-Modeling/03_input_files_transv_tens/Job-RVE1.odb')
session.viewports['Viewport: 1'].setValues(displayedObject=o1)
#: Model: C:/Multiscale-Modeling/03_input_files_transv_tens/Job-RVE1.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     1
#: Number of Meshes:             2
#: Number of Element Sets:       5
#: Number of Node Sets:          7119
#: Number of Steps:              1
odb = session.odbs['C:/Multiscale-Modeling/03_input_files_transv_tens/Job-RVE1.odb']
xyList = xyPlot.xyDataListFromField(odb=odb, outputPosition=ELEMENT_NODAL, 
    variable=(('S', INTEGRATION_POINT, ((INVARIANT, 'Max. Principal'), )), ), 
    elementSets=('PART-1-1.SET-3', ))
xyp = session.XYPlot('XYPlot-1')
chartName = xyp.charts.keys()[0]
chart = xyp.charts[chartName]
curveList = session.curveSet(xyData=xyList)
chart.setValues(curvesToPlot=curveList)
session.viewports['Viewport: 1'].setValues(displayedObject=xyp)
#: Warning: Requested operation will result in the creation of a very large number of xyDataObjects. Performance can be affected. Please reduce the number of specified entities using Display Group operations before re-performing this operation.
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
    predefinedFields=ON, connectors=ON)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Initial')
session.viewports['Viewport: 1'].view.setValues(nearPlane=276.23, 
    farPlane=470.458, width=237.004, height=97.4938, viewOffsetX=-87.3794, 
    viewOffsetY=-7.65024)
session.viewports['Viewport: 1'].view.setValues(nearPlane=271.16, 
    farPlane=475.528, width=232.654, height=95.7045, cameraPosition=(266.974, 
    255.865, 218.912), cameraUpVector=(-0.480742, 0.569847, -0.666455), 
    cameraTarget=(51.4242, 40.3144, 3.3614), viewOffsetX=-85.7757, 
    viewOffsetY=-7.50983)
session.viewports['Viewport: 1'].view.setValues(nearPlane=271.098, 
    farPlane=475.59, width=232.601, height=95.6827, cameraPosition=(242.086, 
    295.088, 204.576), cameraUpVector=(-0.742984, 0.548788, -0.383155), 
    cameraTarget=(26.5366, 79.5374, -10.9742), viewOffsetX=-85.7562, 
    viewOffsetY=-7.50812)
session.viewports['Viewport: 1'].view.setValues(nearPlane=271.097, 
    farPlane=475.59, width=232.6, height=95.6824, cameraPosition=(257.366, 
    273.818, 210.566), cameraUpVector=(-0.6077, 0.57653, -0.546181), 
    cameraTarget=(41.8168, 58.2677, -4.98465), viewOffsetX=-85.7559, 
    viewOffsetY=-7.50809)
session.viewports['Viewport: 1'].view.setValues(nearPlane=234.65, 
    farPlane=512.037, width=614.407, height=252.742, viewOffsetX=-228.071, 
    viewOffsetY=-13.3986)
session.viewports['Viewport: 1'].view.setValues(nearPlane=226.156, 
    farPlane=520.531, width=592.166, height=243.593, viewOffsetX=67.039, 
    viewOffsetY=-9.9186)
session.viewports['Viewport: 1'].view.setValues(nearPlane=271.728, 
    farPlane=474.96, width=186.513, height=76.7239, viewOffsetX=33.0034, 
    viewOffsetY=-10.5897)
session.viewports['Viewport: 1'].view.setValues(nearPlane=290.243, 
    farPlane=514.573, width=199.222, height=81.9519, cameraPosition=(388.683, 
    254.234, 26.8354), cameraUpVector=(-0.677929, 0.601483, -0.422647), 
    cameraTarget=(61.8137, 75.5119, 2.34188), viewOffsetX=35.2523, 
    viewOffsetY=-11.3112)
session.viewports['Viewport: 1'].view.setValues(nearPlane=305.965, 
    farPlane=498.85, width=55.0539, height=22.6469, viewOffsetX=14.8682, 
    viewOffsetY=-1.08218)
session.viewports['Viewport: 1'].view.setValues(nearPlane=346.878, 
    farPlane=429.729, width=62.4155, height=25.6752, cameraPosition=(36.6263, 
    283.271, 314.421), cameraUpVector=(-0.795728, 0.217902, -0.565099), 
    cameraTarget=(30.5846, 58.8073, 16.1516), viewOffsetX=16.8563, 
    viewOffsetY=-1.22688)
session.viewports['Viewport: 1'].view.setValues(nearPlane=330.294, 
    farPlane=446.313, width=226.713, height=93.2606, viewOffsetX=22.2279, 
    viewOffsetY=-7.48501)
session.viewports['Viewport: 1'].view.setValues(nearPlane=329.995, 
    farPlane=443.71, width=226.508, height=93.1761, cameraPosition=(148.292, 
    97.8063, 369.22), cameraUpVector=(-0.700557, 0.683314, -0.205673), 
    cameraTarget=(32.5011, 55.159, 16.8587), viewOffsetX=22.2078, 
    viewOffsetY=-7.47824)
session.viewports['Viewport: 1'].view.setValues(nearPlane=329.572, 
    farPlane=444.132, width=226.218, height=93.0568, cameraPosition=(146.719, 
    114.078, 367.768), cameraUpVector=(-0.212877, 0.895183, -0.391575), 
    cameraTarget=(30.9278, 71.4309, 15.4063), viewOffsetX=22.1793, 
    viewOffsetY=-7.46866)
session.viewports['Viewport: 1'].view.setValues(nearPlane=337.261, 
    farPlane=427.045, width=231.496, height=95.2279, cameraPosition=(-9.97381, 
    132.809, 371.48), cameraUpVector=(-0.0914745, 0.864045, -0.495034), 
    cameraTarget=(24.2436, 70.4789, 4.97066), viewOffsetX=22.6967, 
    viewOffsetY=-7.6429)
session.viewports['Viewport: 1'].view.setValues(nearPlane=336.64, 
    farPlane=427.666, width=231.069, height=95.0526, cameraPosition=(-8.70501, 
    137.203, 370.851), cameraUpVector=(0.0680773, 0.873649, -0.481771), 
    cameraTarget=(25.5124, 74.8728, 4.34186), viewOffsetX=22.6549, 
    viewOffsetY=-7.62882)
session.viewports['Viewport: 1'].view.setValues(nearPlane=341.492, 
    farPlane=418.907, width=234.4, height=96.4226, cameraPosition=(-1.26151, 
    47.6559, 378.7), cameraUpVector=(0.0520448, 0.962816, -0.265096), 
    cameraTarget=(25.5498, 73.1732, 7.19608), viewOffsetX=22.9814, 
    viewOffsetY=-7.73877)
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
    engineeringFeatures=ON)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=OFF)
p1 = mdb.models['Model-1'].parts['Part-1']
session.viewports['Viewport: 1'].setValues(displayedObject=p1)
o7 = session.odbs['C:/Multiscale-Modeling/03_input_files_transv_tens/Job-RVE1.odb']
session.viewports['Viewport: 1'].setValues(displayedObject=o7)
session.viewports['Viewport: 1'].view.setValues(nearPlane=302.774, 
    farPlane=439.613, width=287.908, height=125.229, cameraPosition=(144.97, 
    144.983, 344.623), cameraUpVector=(-0.324548, 0.816238, -0.477937), 
    cameraTarget=(44.4632, 53.8277, -3.19085))
session.viewports['Viewport: 1'].view.setValues(nearPlane=331.964, 
    farPlane=410.422, width=66.1996, height=28.7943, viewOffsetX=13.8832, 
    viewOffsetY=23.4077)
session.viewports['Viewport: 1'].odbDisplay.setFrame(step='Step-1', frame=0)
