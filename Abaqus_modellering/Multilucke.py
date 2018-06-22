def FrameFinder():
    limit = 0.05
    print Sigmapaths
    if not Reset:
        StressSi = np.genfromtxt(Sigmapaths)
    else:
        StressSi = np.genfromtxt(ReSigmapaths)
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
                if not Reset:
                    StressSi = np.genfromtxt(Sigmapaths)
                else:
                    StressSi = np.genfromtxt(ReSigmapaths)
                StressSi = StressSi[1:, :]
                try:
                    StressSi = StressSi[kj - 4:kj , :]
                except:
                    StressSi = StressSi[kj - 4:kj, :]
                return kj - 4, StressFlags, (StressSi[2,1:]-StressSi[0,1:])/(StressSi[2,0]-StressSi[0,0])*(1.0-StressSi[0,0])

    for sa in range(0, len(StressSi[0])):
        if Dob[sa]:
            return len(StressSi) - 2, Dob, StressSi[kj]
        if Sing[sa]:
            return len(StressSi) - 1, Sing, StressSi[kj]
    #del Ididtifying_diverging_frame_did_notwork
    print 'No divergence found'
    return len(StressSi)-1, StressFlags, StressSi[-1]

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
if not ConDmPlast:
    Plastic=1
    Damage=0
    Interdamage=0
    if Plastic:
        mdb.models['Model-A'].materials['resin'].Plastic(table=((Yieldlim, 0.0), (Plastlim, PlasticStrain)))
        mdb.models['Model-A'].materials['resin'].Plastic(table=((Yieldlim, 0.0), (Plastlim, PlasticStrain)))
    if Damage:
        mdb.models['Model-A'].materials['resin'].DuctileDamageInitiation(table=((0.035,
                                                                                 0.0, 0.0),))
        mdb.models['Model-A'].materials['resin'].ductileDamageInitiation.DamageEvolution(
            type=DISPLACEMENT, table=((0.001, ), ))
    if Interdamage:
        IntCon = {'QDI': (0.061, 0.061, 0.061),
                  'qdiDEpower': 1.2, 'qdiDE': (0.0078, 0.0078, 0.0078), }
        intF = mdb.models['Model-A'].materials['interface']
        intF.QuadsDamageInitiation(table=(IntCon['QDI'],))
        intF.quadsDamageInitiation.DamageEvolution(type=ENERGY, table=(IntCon['qdiDE'],))


Size = 0.8e-1
Mult = [[Size, 4]]

Case1 = [[Size, 4],
        [Size, 1],
        [Size, 2]]
Case2 = [[Size,3],
        [Size, 4],
        [Size, 5]]
Case3 = [[-Size, 0],
        [-Size, 1],
        [-Size,2]]

#for sisss in normal:
for sisss in Mult:
    if stresstest:
        """Inital Strength test"""
        if not error:
            #try:
            Magni = [sisss[0],Size]    # Skalarverdi til toyning
            Ret = [sisss[1], 5]         # Mulige lastretninger STRAINS:  exx, eyy, ezz,  exy,  exz,  eyz
            DIRSS=  ['2', '3', '1', '23', '12', '13']
            strain = 0.0 * id[0]
            for roos in range(0,len(Ret)):
                strain = strain+ Magni[roos] * id[Ret[roos]]

            Increments = {'maxNum': 300, 'initial': 1e-2, 'min': 1e-8, 'max': 0.1}


            ### SETTE lagringsplass

            if True:
                print '\nReferanse Strain Vector ', strain
                stresses = np.round(np.dot(Stiffmatrix, strain),3)
                print 'Stresses from RefSTRAINS', stresses
                Stresses = 0 * id[0]
                for roos in range(0, len(Ret)):
                    Stresses = Stresses +  abs(stresses[Ret[0]])*stresses[Ret[roos]]/abs(stresses[Ret[roos]]) * id[Ret[roos]]
                print 'Referanse Stress Vector', np.round(Stresses,3)
                #print Stresses, Stiffmatrix
                strains = np.dot(np.linalg.inv(Stiffmatrix), Stresses)
                print 'Initial Strain Vector', np.round(strains,3)
                Type=''
                for roos in [Ret[0]]:
                    if roos == 3 or roos == 4 or roos == 5:
                        Type = Type + 'Shear_'
                    else:
                        if Stresses[roos] > 0:
                            Type = Type + 'Tension_'
                        else:
                            Type = Type + 'Compression_'
                    Type = Type + DIRSS[roos]
                if len(Ret)==2:
                    for roos in [Ret[1]]:
                        if roos == 3 or roos == 4 or roos == 5:
                            Type = Type + '_Shear_'
                        else:
                            if Stresses[roos] > 0:
                                Type = Type + '_Tension_'
                            else:
                                Type = Type + '_Compression_'
                        Type = Type + DIRSS[roos]

            cases = [[Type + '__Rand-' +str(key) +  str(Q), strains]]
            Sigmapaths = Tekstfiler + 'Stresstests/'+ Type+ '__Rand-' +  str(Q)+ '.txt'


            for Case in cases:
                Jobbnavn, Strain = Case

                execfile(Modellering +'nonLinearAnalysis.py')
                print('t etter nonlin analyser=', (time.time() - start_time))

                Reset = 0       #For aa logge initielle strain stress
                stegy=difstpNm
                print '\nPostProcess'
                if analyse:
                    execfile(processering + 'nonLinearPostprocessing.py')
                print('t ved ferdig postprosess=', (time.time() - start_time))


        d=[0.8]*6
        """Adjusting strength test"""
        if not error and Rerun:
            strains2 = strains.tolist()

            Jobbnav = Jobbnavn
            prev=0      #for aa vite hvor langt bak vi hoppet forrige gang
            reps = 5
            adjusts=0
            Frames = np.zeros(reps+1)
            lolo=1.0
            attempts= 0
            while adjusts<reps:
                Fram = FrameFinder()  # Returns frame before divergion
                if attempts==0:
                    Loao=Fram[2]
                if not adjusts==0:
                    if Fram[0]<prevfram[0]:
                        Fram= prevfram
                print '\nfix:  ',adjusts

                print Fram
                if Reset:
                    StressSigs = np.genfromtxt(ReSigmapaths)
                else:
                    StressSigs = np.genfromtxt(Sigmapaths)
                StressSigs = StressSigs[:Fram[0]]

                #print StressSigs[-1, :]
                print 'plotpunkter   ', len(StressSigs)-1

                appe = 0
                diff = Fram[0] - prev
                ReSigmapaths = Tekstfiler + 'Stresstests/' + Type + '__Rand-' + str(Q) + str(attempts) + 'RE.txt'
                if not diff<=1:
                    Reset = 1

                    Frames[adjusts + 1] = Fram[0]
                    appe = 1

                    prev = Fram[0]

                    if adjusts == 0:
                        prevname = difstpNm
                    else:
                        prevname = 'rep' + str(adjusts - 1)


                    print Frames[adjusts + 1], Frames[adjusts]
                    addedF = int(Frames[adjusts + 1]) - int(Frames[adjusts])  # minus ## for prevantiv

                    stegy = 'rep' + str(adjusts)

                    print 'diff', diff,  'addF', addedF
                    print prevname
                    lolo=lolo- StressSigs[-1][0]
                    mod.StaticStep(name='rep' + str(adjusts), previous=prevname, nlgeom=ON, stabilizationMagnitude=0.0002,
                                   stabilizationMethod=DAMPING_FACTOR,
                                   continueDampingFactors=False, adaptiveDampingRatio=0.05, timePeriod= lolo)
                    #IniTid = (StressSigs[-1, 0] - StressSigs[-2, 0]) * 0.9

                    steg = mod.steps['rep' + str(adjusts)]

                    steg.setValues(maxNumInc=Increments['maxNum'], initialInc=lolo*(StressSigs[-1][0]-StressSigs[-2][0]),
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


                print '\nPrevious Strain Vector', np.round(strains2,4)
                print 'Change : ', Fram[1]
                FEEDbakc=1
                if FEEDbakc:
                    loas=[]
                    for asa in range(0,6):
                        if asa != Ret[0]:
                            if len(Ret)==2:
                                if asa != Ret[1]:
                                    loas.append(1)
                                else:
                                    loas.append(0)
                            else:
                                if asa==2:
                                    loas.append(1)
                                else:
                                    loas.append(1)
                        else:
                            loas.append(0)
                    adjfac = np.dot(np.linalg.inv(Stiffmatrix), np.multiply(Fram[2], loas))

                    print np.round(adjfac), loas

                    strains2 = strains2 - adjfac

                print 'Updated Strain Vector', np.round(strains2,2), '\n\n' + Jobbnavn

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
                if Reset:
                    execfile(processering + 'nonLinearPostprocessing.py')
                    t = (time.time() - start_time)
                    print('t for Restart iterasjon=', t)

                if appe:
                    adjusts =adjusts+1
                    print 'count: ', adjusts
                    prevfram = Fram
                attempts= attempts+1


            t = (time.time() - start_time)
            print('Reached end of random key Iteration\tt ved ferdig', t)
            ss = open('C:/Users/Sondre/Desktop/Ferdig'+str(key)+'.txt', "w")
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