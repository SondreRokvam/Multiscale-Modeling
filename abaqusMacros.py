# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import __main__


def Macro1():
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
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    Mdb()
    session.viewports['Viewport: 1'].setValues(displayedObject=None)
    session.viewports['Viewport: 1'].setValues(displayedObject=None)
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
        sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.rectangle(point1=(-5.0, 5.0), point2=(5.0, -5.0))


def Macro2():
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
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    session.viewports['Viewport: 1'].view.setValues(nearPlane=22.6393, 
        farPlane=42.3734, cameraPosition=(23.7562, -3.68744, 29.386), 
        cameraUpVector=(-0.505208, 0.835621, 0.215645), cameraTarget=(-1.57678, 
        0.801343, 6.18872))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=25.1803, 
        farPlane=40.2809, cameraPosition=(1.14536, 7.28254, 39.3933), 
        cameraUpVector=(-0.0245931, 0.852899, -0.521497), cameraTarget=(
        -0.0917015, 0.0808349, 5.53144))
    p = mdb.models['Model-1'].parts['Part-1-mesh-1']
    n = p.nodes
    print n[3].coordinates, n[2].coordinates, n[6].coordinates, n[7].coordinates, n[1].coordinates, n[0].coordinates, n[4].coordinates, n[5].coordinates



def Macro3():
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
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    session.viewports['Viewport: 1'].view.setValues(nearPlane=40.6722, 
        farPlane=56.1064, cameraPosition=(-8.88706, 1.66152, 51.6527), 
        cameraUpVector=(0.119407, 0.936289, -0.33031), cameraTarget=(1.19975, 
        0.879221, -4.07037))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=44.1958, 
        farPlane=52.5829, width=9.84506, height=4.5078, cameraPosition=(
        -15.1766, 1.90821, 50.5107), cameraTarget=(-5.08978, 1.12592, 
        -5.21234))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=44.3828, 
        farPlane=52.3959, cameraPosition=(-15.4085, 0.25817, 50.4919), 
        cameraTarget=(-5.32168, -0.524129, -5.23116))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=43.3023, 
        farPlane=66.2241, cameraPosition=(-48.3836, 6.76964, -20.7825), 
        cameraUpVector=(0.299528, 0.858761, 0.415706), cameraTarget=(0.296717, 
        -1.63357, 6.91279))
    cliCommand(
        """execfile('C:\\Multiscale-Modeling\\MicroscaleModelling_randomSweep.py')""")
    session.viewports['Viewport: 1'].setValues(displayedObject=None)
    p = mdb.models['Model-A'].parts['Part-1-mesh-1']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    p = mdb.models['Model-A'].parts['Part-1-mesh-1']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
def Macro4():
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
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    execfile('C:/Multiscale-Modeling/Abaqus_steg/nonLinearAnalysis.py', 
        __main__.__dict__)


def Macro5():
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
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    odb = session.odbs['C:/Temp/ShearExy.odb']
    xyList = xyPlot.xyDataListFromField(odb=odb, outputPosition=INTEGRATION_POINT, 
        variable=(('S', INTEGRATION_POINT, ((INVARIANT, 
        'Max. Principal (Abs)'), )), ), elementSets=(
        'PART-1-MESH-1-1.INTERFACES', 'PART-1-MESH-1-1.MATRIX', ))
    xyp = session.XYPlot('XYPlot-1')
    chartName = xyp.charts.keys()[0]
    chart = xyp.charts[chartName]
    curveList = session.curveSet(xyData=xyList)
    chart.setValues(curvesToPlot=curveList)
    session.viewports['Viewport: 1'].setValues(displayedObject=xyp)
    odb = session.odbs['C:/Temp/ShearExy.odb']
    xyList = xyPlot.xyDataListFromField(odb=odb, outputPosition=INTEGRATION_POINT,
        variable=(('S', INTEGRATION_POINT, ((INVARIANT, 'Max. Principal'), )),
        ), elementSets=('PART-1-MESH-1-1.INTERFACES', 'PART-1-MESH-1-1.MATRIX',
        ))
    print sum(xyList)
    xyp = session.xyPlots['XYPlot-1']
    chartName = xyp.charts.keys()[0]
    chart = xyp.charts[chartName]
    curveList = session.curveSet(xyData=xyList)
    chart.setValues(curvesToPlot=curveList)


def Macro6():
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
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    odb = session.odbs['C:/temp/TensionX_NothingElse.odb']
    session.xyDataListFromField(odb=odb, outputPosition=ELEMENT_CENTROID, 
        variable=(('S', INTEGRATION_POINT, ((COMPONENT, 'S11'), (COMPONENT, 
        'S22'), (COMPONENT, 'S33'), )), ), elementSets=(' ALL ELEMENTS', ))


def Field():
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
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    odb = session.openOdb(name='C:/Temp/TensionX_NothingElse.odb')
    global s11xy, s22xy,s33xy,Evol
    s11xy = session.xyDataListFromField(odb=odb, outputPosition=ELEMENT_CENTROID,
                                variable=(('S', INTEGRATION_POINT, ((COMPONENT, 'S11'),)),),
                                elementSets=(' ALL ELEMENTS',))
    s22xy = session.xyDataListFromField(odb=odb, outputPosition=ELEMENT_CENTROID,
                                variable=(('S', INTEGRATION_POINT, ((COMPONENT, 'S22'),)),),
                                elementSets=(' ALL ELEMENTS',))
    s33xy = session.xyDataListFromField(odb=odb, outputPosition=ELEMENT_CENTROID,
                                variable=(('S', INTEGRATION_POINT, ((COMPONENT, 'S33'),)),),
                                elementSets=(' ALL ELEMENTS',))
    Evol = session.xyDataListFromField(odb=odb, outputPosition=WHOLE_ELEMENT, variable=((
        'EVOL', WHOLE_ELEMENT), ), elementSets=(' ALL ELEMENTS', ))
    #EVOL per Frame
    """
    VolumePerTime=[] 
    for elements in Evol:
        elementVolumes=0
        for vol in elements:
            elementVolumes =elementVolumes+vol[0]
        VolumePerTime.append(elementVolumes)
       
       
       """
def Evol():
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
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
        variableLabel='EVOL', outputPosition=WHOLE_ELEMENT, )
    session.viewports['Viewport: 1'].odbDisplay.display.setValues(
        plotState=CONTOURS_ON_DEF)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=360.022, 
        farPlane=617.827, width=451.093, height=207.909, cameraPosition=(
        420.925, 134.069, 187.724), cameraUpVector=(-0.610593, 0.785026, 
        -0.104459), cameraTarget=(-3.15505, -13.6518, -12.3204))
    odb = session.odbs['C:/temp/TensionX_NothingElse.odb']
    session.xyDataListFromField(odb=odb, outputPosition=WHOLE_ELEMENT, variable=((
        'EVOL', WHOLE_ELEMENT), ), elementSets=(' ALL ELEMENTS', ))
    Mdb()
    session.viewports['Viewport: 1'].setValues(displayedObject=None)


def Macro7():
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
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    o1 = session.openOdb(name='C:/Temp/TensionX_NothingElse.odb')
    session.viewports['Viewport: 1'].setValues(displayedObject=o1)



def dasd():
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
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    session.xyPlots[session.viewports['Viewport: 1'].displayedObject.name].setValues(
        transform=(0.833333, 0, 0, -0.043067, 0, 0.833333, 0, -0.0104748, 0, 0, 
        0.833333, 0, 0, 0, 0, 1))
    odb = session.odbs['C:/Temp/TensionX_NothingElse.odb']
    session.xyDataListFromField(odb=odb, outputPosition=ELEMENT_CENTROID, 
        variable=(('S', INTEGRATION_POINT, ((COMPONENT, 'S11'), )), ), 
        elementSets=(' ALL ELEMENTS', ))
    odb = session.odbs['C:/Temp/TensionX_NothingElse.odb']
    session.xyDataListFromField(odb=odb, outputPosition=INTEGRATION_POINT, 
        variable=(('S', INTEGRATION_POINT, ((COMPONENT, 'S11'), )), ), 
        elementSets=(' ALL ELEMENTS', ))
    cliCommand(
        """s11xy = ssession.xyDataListFromField(odb=odb, outputPosition=INTEGRATION_POINT, 
    variable=(('S', INTEGRATION_POINT, ((COMPONENT, 'S11'), )), ), 
    elementSets=(' ALL ELEMENTS', ))""")
    cliCommand(
        """s11xy = session.xyDataListFromField(odb=odb, outputPosition=INTEGRATION_POINT, 
    elementSets=(' ALL ELEMENTS', ))""")
    cliCommand(
        """s11xy = session.xyDataListFromField(odb=odb, outputPosition=INTEGRATION_POINT, 
    variable=(('S', INTEGRATION_POINT, ((COMPONENT, 'S11'), )), ), 
    elementSets=(' ALL ELEMENTS', ))""")
    cliCommand("""len(s11xy)""")
    cliCommand(
        """ggg = open('C:/Users/Rockv/Desktop/Nytt tekstdokument.txt', "w")""")
    cliCommand("""ggg.write(VolumePerTime)""")
    cliCommand("""ggg.write(str(VolumePerTime))""")
    cliCommand("""ggg.close""")
    cliCommand(
        """ggg = open('C:/Users/Rockv/Desktop/Nytt tekstdokument.txt', "w")""")
    cliCommand("""for val in VolumePerTime:
    ggg.write(str(val)+'\\n')""")
    cliCommand("""for val in VolumePerTime:
    ggg.write(str(val)+'\\n')
    """)
    cliCommand("""ggg.close""")
    cliCommand("""for val in VolumePerTime:
    ggg.write(str(val)+'\\n')
    ggg.close""")
    odb = session.mdbData['Model-1']
    session.viewports['Viewport: 1'].setValues(displayedObject=odb)
    session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
        CONTOURS_ON_DEF, ))
    o7 = session.odbs['C:/Temp/TensionX_NothingElse.odb']
    session.viewports['Viewport: 1'].setValues(displayedObject=o7)
    cliCommand(
        """s11xy = session.xyDataListFromField(odb=odb, outputPosition=ELEMENT_CENTROID, 
    variable=(('S', ELEMENT_CENTROID, ((COMPONENT, 'S11'), )), ), 
    elementSets=(' ALL ELEMENTS', ))""")
    cliCommand(
        """s11xy = session.xyDataListFromField(odb=odb, outputPosition=ELEMENT_CENTROID, 
    variable=(('S', INTEGRATION_POINT, ((COMPONENT, 'S11'), )), ), 
    elementSets=(' ALL ELEMENTS', ))""")
    cliCommand("""len(s11xy)""")
    cliCommand("""len(Evol)""")
    cliCommand("""s11xy""")


def Macro8():
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
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    mdb.models['Model-A'].steps['Lasttoyinger'].Restart(frequency=0, 
        numberIntervals=100, overlay=OFF, timeMarks=OFF)


def Macro9():
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
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    mdb.jobs['TensionX_NothingElse'].setValues(type=RESTART)
    mdb.models['Model-A'].setValues(restartJob='TensionX_NothingElse', 
        restartStep='Lasttoyinger')

    a = mdb.models['Model-A'].rootAssembly
    e1 = a.instances['PART-1-MESH-1-1'].elements
    elements1 = e1.getSequenceFromMask(mask=('[#ffffffff:16 #7f ]', ), )
    region = regionToolset.Region(elements=elements1)
    mdb.models['Model-A'].Stress(name='Predefined Field-1', 
        distributionType=FROM_FILE, 
        fileName='C:/Temp/TensionX_NothingElse.odb', step=-1, increment=1)


def Macro10():
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
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    mdb.Job(name='jojo', model='Model-A', description='', type=RESTART, 
        atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
        memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
        explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
        modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
        scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1, 
        numGPUs=0)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
        predefinedFields=ON, connectors=ON)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Lasttoyinger')
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Initial')
    a = mdb.models['Model-A'].rootAssembly
    e1 = a.instances['PART-1-MESH-1-1'].elements
    elements1 = e1.getSequenceFromMask(mask=('[#ffffffff:22 #3 ]', ), )
    region = regionToolset.Region(elements=elements1)
    mdb.models['Model-A'].Stress(name='Predefined Field-1', 
        distributionType=FROM_FILE, 
        fileName='C:/Temp/TensionX_NothingElse.odb', step=-1, increment=-1)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=OFF, bcs=OFF, 
        predefinedFields=OFF, connectors=OFF)
    cliCommand("""execfile(Modellering +'LinearAnalysis.py')""")


def Macro11():
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
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    a = mdb.models['Model-A'].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
        predefinedFields=ON, connectors=ON)
    a = mdb.models['Model-A'].rootAssembly
    e1 = a.instances['PART-1-MESH-1-1'].elements
    elements1 = e1.getSequenceFromMask(mask=('[#ffffffff:22 #3 ]', ), )
    region = regionToolset.Region(elements=elements1)
    mdb.models['Model-A'].Stress(name='FraNonLinear', distributionType=FROM_FILE, 
        fileName='C:/Temp/TensionX_NothingElse.odb', step=-1, increment=-1)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=OFF, bcs=OFF, 
        predefinedFields=OFF, connectors=OFF)
    mdb.jobs['Exx4_0'].submit(consistencyChecking=OFF)
    session.mdbData.summary()
    o3 = session.openOdb(name='C:/Temp/Exx4_0.odb')
    session.viewports['Viewport: 1'].setValues(displayedObject=o3)
    session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
        CONTOURS_ON_DEF, ))
    session.viewports[session.currentViewportName].odbDisplay.setFrame(
        step='Enhetstoyninger', frame=0)
    session.viewports[session.currentViewportName].odbDisplay.setFrame(
        step='Enhetstoyninger', frame=1)


