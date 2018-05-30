"""         Script variabler                                      """

global Createmodel,Savemodel,numCPU,Runjobs,linearAnalysis,nonLinearAnalysis,Increments
#numCPU = multiprocessing.cpu_count()
numCPU = 1

analyse =0
FoundStiff = 1
if analyse:
    Createmodel = 1
    Savemodel = 1
    Runjobs = 1
    if not FoundStiff:
        linearAnalysis = 1
        LinearpostPross = 1
    else:
        linearAnalysis = 0
        LinearpostPross = 0
    nonLinearAnalysis = 1
    nonLinearpostPross =1
    openModel = 0
else:
    Createmodel = 0
    Savemodel = 1
    Runjobs = 1
    linearAnalysis = 0
    LinearpostPross = 0
    nonLinearpostPross = 1
    openModel = 1

    nonLinearAnalysis = 1 # Finne standard

Increments = {'maxNum': 60, 'initial': 1e-2, 'min': 1e-4, 'max': 0.05}

Iterations = 0


"""Simuleringsvariabler """
global Atapt_Damp_Ratio,Dampening,Stabl_Magn,Singlepin,tripplepin

Dampening = 1
Stabl_Magn =2e-4
Atapt_Damp_Ratio = 0.05

Singlepin = 0                               #   Randbetingelse:    Laaser hjornenode mot forskyvning i 3 retninger
tripplepin = 0                              #   Randbetingelse:    Laaser to noder mot forskyvning. En sentrert kantnode i 2 retninger og midtnode i 1 retning

global MaterialDens, ConDmPlast
ConDmPlast = 0
MaterialDens  = 0                           #   Material Density






"""    RVEmodel variabler                                      """
global noFibertest,Fibervariation,rmean,Rstdiv,Interface,rinterface,ElementInterfaceT,id, Retning

noFibertest = 0                                     # ON/OFF Fiber i modellen.
Fibervariation = 1                                  # ON/OFF variasjon fiberradius. Mean and standard div. Kan paavirke Vf i endelig model.

rmean = 8.7096                              # Gjennomsnittradius pa fiber
Rstdiv = 0.6374                             # OStandard avvik fra gjennomsnittsradius

Interface = 1                                   # ON/OFF CohesiveInterface
rinterface = 0.001                              # Interfacetykkelse ved modellering. Verdi er relativ til radius.    0.01 = 1%
ElementInterfaceT = 0                  # Interfacetykkelse paa elementene.  Verdi er relativ til radius.

id   =   np.identity(6)          # Identity matrix. Good for normalised load cases.'Exx','Eyy','Ezz','Exy','Exz','Eyz'
Retning =    ['Exx', 'Eyy', 'Ezz', 'Exy', 'Exz', 'Eyz']





"""Meshsize"""
global FiberSirkelResolution,meshsize,tykkelse,tol

FiberSirkelResolution =  20                               # Meshresolution pa Fiber omkrets. 2*pi/FiberSirkelResolution
meshsize = rmean * 2 * pi / FiberSirkelResolution           # Meshsize fra resolution paa interface paa fiberomkrets

tykkelse = meshsize    # RVE tykkelse
tol = rinterface * 0.4  # Modelleringstoleranse - Mindre en minste modelleringsvariabel (rInterface)





"""RVE populasjon"""
global r,gtol,ytredodgrense,indredodgrense,iterasjonsgrense,Rclearing

Rclearing = 0.02  # Minimumsavstand mellom fiberkant og RVE kant. Verdi relativ til radius. Skal den settes lik meshsize?

r = rmean       #Fordi jeg skrev koden med r som radius foer radius variasjon ble introdusert
gtol = Rclearing * r  # Fibers relative dodsone klarering for toleranse
ytredodgrense = r + gtol  # Dodzone avstand, ytre grense fra kanter/hjorner
indredodgrense = r - gtol  # Dodzone avstand, indre grense fra kanter/hjorner

iterasjonsgrense = 10000  # iterasjonsgrense i Fiberutplassering loop





""" ABAQUS modelleringsnavn    """

global modelName,partName, meshPartName, instanceName,stepName, difstpNm
modelName = 'Model-A'
partName, meshPartName = 'Part-1', 'Part-1-mesh-1'
instanceName = 'PART-1-MESH-1-1'
stepName, difstpNm = 'Enhetstoyninger', 'Lasttoyinger'