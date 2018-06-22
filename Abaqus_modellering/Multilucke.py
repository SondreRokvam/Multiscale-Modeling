def FrameFinder():
    limit = 0.05
    print Sigmapaths
    StressSi = np.genfromtxt(Sigmapaths)
    StressSi = StressSi[1:, 1:]
    for a in range(0, 6):
        if len(Ret)==2:
            if not a == Ret[0]:
                if not a == Ret[1]:
                    StressSi[1:, a] = np.multiply(StressSi[1:, a], 1 / StressSi[1:, Ret[0]])
        else:
            if not a == Ret[0]:
                StressSi[1:, a] = np.multiply(StressSi[1:, a], 1 / StressSi[1:, Ret[0]])
    Sing = [0]*6
    Dob = [0]*6
    Trecharm = [0]*6
    StressFlags = [0]*6
    for kj in range(0,len(StressSi)):
        for sa in range(0,len(StressSi[0])):
            if len(Ret) == 2:
                if not (sa == Ret[0] or sa == Ret[1]):
                    if not Trecharm[sa]:
                        if not Dob[sa]:
                            if not Sing[sa]:
                                if abs(StressSi[kj][sa]) > limit:
                                    Sing[sa]=1
                            else:
                                if abs(StressSi[kj][sa]) > limit:     #   Feilmargin
                                    Dob[sa] = 1
                                else:
                                    Sing[sa]=0
                        else:
                            if abs(StressSi[kj][sa]) > limit:  # Feilmargin
                                Trecharm[sa] = 1
                            else:
                                Sing[sa] = 0
                                Dob[sa] = 0
                    else:
                        StressFlags[sa] = 1
            else:
                if not sa==Ret[0]:
                    if not Trecharm[sa]:
                        if not Dob[sa]:
                            if not Sing[sa]:
                                if abs(StressSi[kj][sa]) > limit:
                                    Sing[sa]=1
                            else:
                                if abs(StressSi[kj][sa]) > limit:     #   Feilmargin
                                    Dob[sa] = 1
                                else:
                                    Sing[sa]=0
                        else:
                            if abs(StressSi[kj][sa]) > limit:  # Feilmargin
                                Trecharm[sa] = 1
                            else:
                                Sing[sa] = 0
                                Dob[sa] = 0
                    else:
                        StressFlags[sa] = 1
        for sa in range(0, len(StressSi[0])):
            if StressFlags[sa]:
                for sts in range(0,len(StressFlags)):
                    if StressFlags[sts] == 0:
                        StressFlags[sts] = StressFlags[sts]+Dob[sts]
                print StressFlags
                return kj - 3, StressFlags, StressSi[kj]

    for sa in range(0, len(StressSi[0])):
        if Dob[sa]:
            return len(StressSi) - 2, Dob, StressSi[kj]
        if Sing[sa]:
            return len(StressSi) - 1, Sing, StressSi[kj]
    #del Ididtifying_diverging_frame_did_notwork
    print 'No divergence found'
    return len(StressSi)-1, StressFlags, StressSi[len(StressSi)-1]

Q = int( n[-1] )
seed(Q)  # Q er randomfunksjonensnokkelen
error = 0
print Q
print n

    #Datalagring
execfile(Modellering + 'Set_text_dirs.py')
    #Modellere RVE eller aapne eksisterende  -  Sette navn for toyningsretning
execfile(Modellering + 'LagOROpen_preplin.py')

# Linear_Analyse
if FoundStiff:
    Stiffmatrix = np.load(lagrestiffpathmod)
    print
    '\nStiffnessmatrix:'
    for a in range(0, 6):
        print '%7f \t %7f \t %7f \t %7f \t %7f \t %7f' % (
            Stiffmatrix[0][a], Stiffmatrix[1][a], Stiffmatrix[2][a], Stiffmatrix[3][a], Stiffmatrix[4][a],
            Stiffmatrix[5][a])
else:
    if not error:
        #try:
        execfile(Modellering +'LinearAnalysis.py')
        #except:
        #    print 'Problem_With_Linear_Analysis'
        #    error = 1

        print('t etter lin analyser=', (time.time() - start_time))
    if not error:
        if LinearpostPross:
            execfile(processering + 'LinearPostprocessing.py')
            t = (time.time() - start_time)
            print('t etter lin pross=', t)
    del mdb.models['Model-A'].steps['Enhetstoyninger']
#SAve point
if Model:
    mdb.saveAs(pathName=RVEmodellpath)
    print 'saved'

    # Non linear tester
Plastic=1
if Plastic:
    mdb.models['Model-A'].materials['resin'].Plastic(table=((Yieldlim, 0.0), (Plastlim, PlasticStrain)))
    mdb.models['Model-A'].materials['resin'].Plastic(table=((Yieldlim, 0.0), (Plastlim, PlasticStrain)))
Damage=1
if Damage:
    mdb.models['Model-A'].materials['resin'].DuctileDamageInitiation(table=((0.035,
                                                                             0.0, 0.0),))
    mdb.models['Model-A'].materials['resin'].ductileDamageInitiation.DamageEvolution(
        type=DISPLACEMENT, table=((0.001, ), ))
Interdamage=0
if Interdamage:
    IntCon = {'QDI': (0.061, 0.061, 0.061),
              'qdiDEpower': 1.2, 'qdiDE': (0.0078, 0.0078, 0.0078), }
    intF = mdb.models['Model-A'].materials['interface']
    intF.QuadsDamageInitiation(table=(IntCon['QDI'],))
    intF.quadsDamageInitiation.DamageEvolution(type=ENERGY, mixedModeBehavior=BK,
                                               power=IntCon['qdiDEpower'], table=(IntCon['qdiDE'],))
Size = 1.6e-1
Case1= [[Size, 1],
        [Size, 0],
        [Size, 2]]

Case2= [[Size,3],
        [Size, 4]]

Case3 = [-[Size,2],
        [-Size, 1],
        [-Size, 0]]
#for sisss in normal:
for sisss in Case1:
    if stresstest:
        """Inital Strength test"""
        if not error:
            #try:
            Magni = [sisss[0]]    # Skalarverdi til toyning
            Ret = [sisss[1]]         # Mulige lastretninger STRAINS:  exx, eyy, ezz,  exy,  exz,  eyz
            DIRSS=  ['2', '3', '1', '23', '12', '13']
            strain = 0.0 * id[0]
            for roos in range(0,len(Ret)):
                strain = strain+ Magni[roos] * id[Ret[roos]]

            Increments = {'maxNum': 300, 'initial': 1e-2, 'min': 1e-8, 'max': 0.1}
            ### SETTE lagringsplass

            if True:
                print '\n\nReferanse Strain Vector ', strain
                stresses = np.round(np.dot(Stiffmatrix, strain),3)
                print '\nStresses from RefSTRAINS', stresses
                Stresses = 0 * id[0]
                for roos in range(0, len(Ret)):
                    Stresses = Stresses +  stresses[Ret[0]] * id[Ret[roos]]
                print '\nReferanse Stress Vector', np.round(Stresses,3)
                #print Stresses, Stiffmatrix
                strains = np.dot(np.linalg.inv(Stiffmatrix), Stresses)
                print '\nInitial Strain Vector', np.round(strains,3)
                Type=''
            for roos in [Ret[0]]:
                if roos == 3 or roos == 4 or roos == 5:
                    Type = Type + 'Shear_'
                else:
                    if strains[roos] > 0:
                        Type = Type + 'Tension_'
                    else:
                        Type = Type + 'Compression_'
                Type = Type + DIRSS[roos]
            if len(Ret)==2:
                    for roos in Ret:
                        if roos == 3 or roos == 4 or roos == 5:
                            Type = Type + '_Shear_'
                        else:
                            if strains[roos] > 0:
                                Type = Type + '_Tension_'
                            else:
                                Type = Type + '_Compression_'
                        Type = Type + DIRSS[roos]



            cases = [[Type + '__Rand-' +str(key) +  str(Q), strains]]
            Sigmapaths = Tekstfiler + '/Stresstests/'+ Type+ '__Rand-' +  str(Q) + '.txt'

            for Case in cases:
                Jobbnavn, Strain = Case

                #try:
                execfile(Modellering +'nonLinearAnalysis.py')
                #except:
                #    del Problem_With_nonLinear_Analysis
                t = (time.time() - start_time)
                print('t etter nonlin analyser=', t)


                Reset = 0       #For aa logge initielle strain stress
                stegy=difstpNm
                print '\nPostProcess'
                execfile(processering + 'nonLinearPostprocessing.py')
                t = (time.time() - start_time)
                print('t ved ferdig postprosess=', t)
            """except:
                pass
                Q = Q + 1000
                n.append(Q)
                print 'Error in Stress tests'
                error=1"""

        d=[0.8]*6
        """Adjusting strength test"""
        if not error and False:
            strains2 = strains.tolist()
            Reset=1
            Jobbnav = Jobbnavn
            prev=0      #for aa vite hvor langt bak vi hoppet forrige gang
            reps = 12
            adjusts=0
            Frames = np.zeros(reps+1)
            while adjusts<reps:
                Fram = FrameFinder()  # Returns frame before divergion
                if not adjusts==0:
                    if Fram[0]<prevfram[0]:
                        Fram= prevfram
                print '\nfix:  ',adjusts

                print Fram
                StressSigs = np.genfromtxt(Sigmapaths)
                StressSigs = StressSigs[:Fram[0]]

                #print StressSigs[-1, :]
                print 'plotpunkter   ', len(StressSigs)-1

                appe = 0
                diff = Fram[0] - prev

                if not diff<=1:
                    Frames[adjusts + 1] = Fram[0]
                    appe = 1

                    prev = Fram[0]

                    if adjusts == 0:
                        prevname = difstpNm
                    else:
                        prevname = 'rep' + str(adjusts - 1)
                    re =3
                    if diff == 3:
                        re=2
                    if diff==2 or strains[Ret].any() < 0:
                        re=1
                    if diff<=0 :
                        re=0

                    print Frames[adjusts + 1], Frames[adjusts],re
                    addedF = int(Frames[adjusts + 1]) - int(Frames[adjusts]) - re  # minus ## for prevantiv

                    stegy = 'rep' + str(adjusts)

                    print 'diff', diff,  'addF', addedF
                    print prevname
                    lolo=1.0- StressSigs[-1][0]
                    mod.StaticStep(name='rep' + str(adjusts), previous=prevname, nlgeom=ON, stabilizationMagnitude=0.0002,
                                   stabilizationMethod=DAMPING_FACTOR,
                                   continueDampingFactors=False, adaptiveDampingRatio=0.05, timePeriod= lolo)
                    #IniTid = (StressSigs[-1, 0] - StressSigs[-2, 0]) * 0.9

                    steg = mod.steps['rep' + str(adjusts)]

                    steg.setValues(maxNumInc=Increments['maxNum'], initialInc=Increments['min']*1.1*lolo,
                                   minInc=Increments['min']*lolo, maxInc=Increments['max']*lolo, convertSDI=CONVERT_SDI_OFF)

                    steg.Restart(frequency=1, numberIntervals=0, overlay=OFF, timeMarks=OFF)

                    mod.setValues(restartJob=Jobbnavn,
                                  restartStep=prevname, restartIncrement=addedF)

                    Jobbnavn = Jobbnav + str(adjusts)
                    mdb.Job(name=Jobbnavn, model=modelName, description='', type=RESTART,
                            atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90,
                            memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True,
                            explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF,
                            modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='',
                            scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1,
                            numGPUs=0)


                print '\nPrevious Strain Vector', strains2
                print 'Change : ', Fram[1]



                for ssss in range(0,len(strains)):
                    if Fram[1][ssss]:
                        if d[ssss]>0.4:
                            d[ssss] = d[ssss] * 0.75
                        adjfactor = abs(strains[ssss])*d[ssss]
                        print 'Adjust by : ', adjfactor

                        if StressSigs[-1][ssss+1]>=0:
                            strains2[ssss] = strains2[ssss] - adjfactor
                        else:
                            strains2[ssss] = strains2[ssss] + adjfactor
                print 'Updated Strain Vector', strains2, '\n\n' + Jobbnavn

                a = mod.rootAssembly
                exx, eyy, ezz, exy, exz, eyz = strains2
                mod.DisplacementBC(name='BCX', createStepName=difstpNm,
                                   region=a.sets['RPX'], u1=exx, u2=exy, u3=exz, ur1=UNSET, ur2=UNSET, ur3=UNSET,
                                   amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)

                mod.DisplacementBC(name='BCY', createStepName=difstpNm,
                                   region=a.sets['RPY'], u1=exy, u2=eyy, u3=eyz, ur1=UNSET, ur2=UNSET, ur3=UNSET,
                                   amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)

                mod.DisplacementBC(name='BCZ', createStepName=difstpNm,
                                   region=a.sets['RPZ'], u1=exz, u2=eyz, u3=ezz, ur1=UNSET, ur2=UNSET, ur3=UNSET,
                                   amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)

                try:
                    mdb.jobs[Jobbnavn].submit(consistencyChecking=OFF)
                    mdb.jobs[Jobbnavn].waitForCompletion()
                except:
                    pass

                print '\nPostProcess'
                execfile(processering + 'nonLinearPostprocessing.py')
                t = (time.time() - start_time)
                print('t for Restart iterasjon=', t)

                if appe:
                    adjusts =adjusts+1
                    print 'count: ', adjusts
                    prevfram = Fram


            t = (time.time() - start_time)
            print('Reached end of random key Iteration\tt ved ferdig', t)
            ss = open('C:/Users/Sondre/Desktop/Ferdig'+str(ParameterSweep[ItraPara])+'.txt', "w")
            ss.close()
            Q = Q + 21
            n.append(Q)
            del section, regionToolset, dgm, part, material, assembly, step, interaction
            del load, mesh, job, sketch, visualization, xyPlot, dgo, connectorBehavior


    if error:
        Q = Q +1
        n[-1] = Q
        print 'Error'
    else:
        Q = Q+1
        n.append(Q)