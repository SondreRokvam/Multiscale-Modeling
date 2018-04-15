# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 6.14-4 replay file
# Internal Version: 2015_06_11-22.41.13 135079
# Run by Blue on Sun Apr 15 04:41:27 2018
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
#: 50
#: Aspect ratio for Interface elements ved modellering = 261.8	 Interface element thickness = 0.7585713216
#: A new model database has been created.
#: The model "Model-1" has been created.
session.viewports['Viewport: 1'].setValues(displayedObject=None)
#: The model "Model-A" has been created.
#: Fiber added! Fiber = 1.0 av nf =  50 Koordinater =  1  Vf =  0.0  av  0.6  Krasjes: 0 Tries: 0
#: Fiber added! Fiber = 2.0 av nf =  50 Koordinater =  2  Vf =  0.012  av  0.6  Krasjes: 0 Tries: 1
#: Fiber added! Fiber = 3.0 av nf =  50 Koordinater =  3  Vf =  0.024  av  0.6  Krasjes: 0 Tries: 2
#: Fiber added! Fiber = 4.0 av nf =  50 Koordinater =  4  Vf =  0.036  av  0.6  Krasjes: 0 Tries: 3
#: Fiber added! Fiber = 5.0 av nf =  50 Koordinater =  6  Vf =  0.048  av  0.6  Krasjes: 1 Tries: 5
#: Fiber added! Fiber = 6.0 av nf =  50 Koordinater =  7  Vf =  0.06  av  0.6  Krasjes: 2 Tries: 7
#: Fiber added! Fiber = 7.0 av nf =  50 Koordinater =  8  Vf =  0.072  av  0.6  Krasjes: 3 Tries: 9
#: Fiber added! Fiber = 8.0 av nf =  50 Koordinater =  9  Vf =  0.084  av  0.6  Krasjes: 3 Tries: 10
#: Fiber added! Fiber = 9.0 av nf =  50 Koordinater =  10  Vf =  0.096  av  0.6  Krasjes: 3 Tries: 11
#: Fiber added! Fiber = 10.0 av nf =  50 Koordinater =  11  Vf =  0.108  av  0.6  Krasjes: 3 Tries: 12
#: Fiber added! Fiber = 11.0 av nf =  50 Koordinater =  12  Vf =  0.12  av  0.6  Krasjes: 3 Tries: 13
#: Fiber added! Fiber = 12.0 av nf =  50 Koordinater =  13  Vf =  0.132  av  0.6  Krasjes: 4 Tries: 15
#: Fiber added! Fiber = 13.0 av nf =  50 Koordinater =  14  Vf =  0.144  av  0.6  Krasjes: 5 Tries: 17
#: Fiber added! Fiber = 14.0 av nf =  50 Koordinater =  16  Vf =  0.156  av  0.6  Krasjes: 8 Tries: 21
#: Fiber added! Fiber = 15.0 av nf =  50 Koordinater =  17  Vf =  0.168  av  0.6  Krasjes: 8 Tries: 22
#: Fiber added! Fiber = 16.0 av nf =  50 Koordinater =  18  Vf =  0.18  av  0.6  Krasjes: 10 Tries: 25
#: Fiber added! Fiber = 17.0 av nf =  50 Koordinater =  19  Vf =  0.192  av  0.6  Krasjes: 10 Tries: 26
#: Fiber added! Fiber = 18.0 av nf =  50 Koordinater =  20  Vf =  0.204  av  0.6  Krasjes: 12 Tries: 29
#: Fiber added! Fiber = 19.0 av nf =  50 Koordinater =  22  Vf =  0.216  av  0.6  Krasjes: 15 Tries: 33
#: Fiber added! Fiber = 20.0 av nf =  50 Koordinater =  23  Vf =  0.228  av  0.6  Krasjes: 16 Tries: 35
#: Fiber added! Fiber = 21.0 av nf =  50 Koordinater =  27  Vf =  0.24  av  0.6  Krasjes: 17 Tries: 37
#: Fiber added! Fiber = 22.0 av nf =  50 Koordinater =  28  Vf =  0.252  av  0.6  Krasjes: 22 Tries: 43
#: Fiber added! Fiber = 23.0 av nf =  50 Koordinater =  29  Vf =  0.264  av  0.6  Krasjes: 29 Tries: 51
#: Fiber added! Fiber = 24.0 av nf =  50 Koordinater =  30  Vf =  0.276  av  0.6  Krasjes: 31 Tries: 54
#: Fiber added! Fiber = 25.0 av nf =  50 Koordinater =  31  Vf =  0.288  av  0.6  Krasjes: 32 Tries: 56
#: Fiber added! Fiber = 26.0 av nf =  50 Koordinater =  33  Vf =  0.3  av  0.6  Krasjes: 37 Tries: 62
#: Fiber added! Fiber = 27.0 av nf =  50 Koordinater =  34  Vf =  0.312  av  0.6  Krasjes: 42 Tries: 68
#: Fiber added! Fiber = 28.0 av nf =  50 Koordinater =  35  Vf =  0.324  av  0.6  Krasjes: 43 Tries: 70
#: Fiber added! Fiber = 29.0 av nf =  50 Koordinater =  36  Vf =  0.336  av  0.6  Krasjes: 48 Tries: 76
#: Fiber added! Fiber = 30.0 av nf =  50 Koordinater =  37  Vf =  0.348  av  0.6  Krasjes: 64 Tries: 93
#: Fiber added! Fiber = 31.0 av nf =  50 Koordinater =  39  Vf =  0.36  av  0.6  Krasjes: 68 Tries: 98
#: Fiber added! Fiber = 32.0 av nf =  50 Koordinater =  40  Vf =  0.372  av  0.6  Krasjes: 72 Tries: 103
#: Fiber added! Fiber = 33.0 av nf =  50 Koordinater =  41  Vf =  0.384  av  0.6  Krasjes: 103 Tries: 135
#: Fiber added! Fiber = 34.0 av nf =  50 Koordinater =  43  Vf =  0.396  av  0.6  Krasjes: 156 Tries: 189
#: Fiber added! Fiber = 35.0 av nf =  50 Koordinater =  44  Vf =  0.408  av  0.6  Krasjes: 207 Tries: 241
#: Fiber added! Fiber = 36.0 av nf =  50 Koordinater =  45  Vf =  0.42  av  0.6  Krasjes: 219 Tries: 254
#: Fiber added! Fiber = 37.0 av nf =  50 Koordinater =  46  Vf =  0.432  av  0.6  Krasjes: 310 Tries: 346
#: Fiber added! Fiber = 38.0 av nf =  50 Koordinater =  47  Vf =  0.444  av  0.6  Krasjes: 1564 Tries: 1601
#: Fiber added! Fiber = 39.0 av nf =  50 Koordinater =  48  Vf =  0.456  av  0.6  Krasjes: 1788 Tries: 1826
#: Fiber added! Fiber = 40.0 av nf =  50 Koordinater =  49  Vf =  0.468  av  0.6  Krasjes: 3824 Tries: 3863
#: Fiber added! Fiber = 41.0 av nf =  50 Koordinater =  51  Vf =  0.48  av  0.6  Krasjes: 3838 Tries: 3878
#: Fiber added! Fiber = 42.0 av nf =  50 Koordinater =  52  Vf =  0.492  av  0.6  Krasjes: 3922 Tries: 3963
#: Fiber added! Fiber = 43.0 av nf =  50 Koordinater =  53  Vf =  0.504  av  0.6  Krasjes: 4266 Tries: 4308
#: Fiber added! Fiber = 44.0 av nf =  50 Koordinater =  55  Vf =  0.516  av  0.6  Krasjes: 1609 Tries: 21654
#: Fiber added! Fiber = 45.0 av nf =  50 Koordinater =  57  Vf =  0.528  av  0.6  Krasjes: 2077 Tries: 22123
#: Fiber added! Fiber = 46.0 av nf =  50 Koordinater =  58  Vf =  0.54  av  0.6  Krasjes: 2278 Tries: 22325
#: Fiber added! Fiber = 47.0 av nf =  50 Koordinater =  59  Vf =  0.552  av  0.6  Krasjes: 3173 Tries: 23221
#: Fiber added! Fiber = 48.0 av nf =  50 Koordinater =  60  Vf =  0.564  av  0.6  Krasjes: 496 Tries: 30546
#: Fiber added! Fiber = 49.0 av nf =  50 Koordinater =  61  Vf =  0.576  av  0.6  Krasjes: 3731 Tries: 93789
#: Fiber added! Fiber = 50.0 av nf =  50 Koordinater =  62  Vf =  0.588  av  0.6  Krasjes: 3856 Tries: 93915
#: Modelled Vf = 0.5937
#: The model "Model-A" has been created.
#: RVEpart created, meshed and Orphanmesh created
#: Element sets and stack direction completed
#: Material properties assigned to element sets in model
#: Imported to Assembly, Translated to origo with fibers longitudinal to x
