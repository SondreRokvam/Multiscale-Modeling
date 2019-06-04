Q = int( n[-1] )
seed(Q)  # Q er randomfunksjonensnokkelen
error = 0
print 'Random key:  ',Q, '\nAv:',  n

# Datalagring
if not error:
    #Sett directories
    try:
        execfile(Modellering + 'Set_text_dirs.py')
    except:
        print 'Feil med directories'
        error=1
if not error:
    try:
        #Modellere RVE eller aapne eksisterende  -  Sette navn for toyningsretning
        execfile(Modellering + 'Lag_eller_aapne_model.py')
    except:
        error = 1
        print 'Feil  i initiering og modellering'
# Stivhets tester
if not error:
    if Stifftest:
        print 'Simulations for Stiffness Matrix'
        try:
            execfile(Modellering +'LinearAnalysis.py')
        except:
            print 'Problem med Stiffness test'
            error = 1
        if not error:
            if LinearpostPross:
                try:
                    execfile(processering + 'LinearPostprocessing.py')
                    t = (time.time() - start_time)
                    print 'Tid etter Stiffness test = ', np.round(t,2)
                except:
                    print
                    'Problem med Stiffness prosessering'
                    error = 1
    else:
        print 'No stiffness simulations, checking Stiffness Matrix'
        try:
            Stiffmatrix = np.load(lagrestiffpathmod)
            print
            '\nStiffnessmatrix:'
            for a in range(0, 6):
                print
                '%7f \t %7f \t %7f \t %7f \t %7f \t %7f' % (
                    Stiffmatrix[0][a], Stiffmatrix[1][a], Stiffmatrix[2][a], Stiffmatrix[3][a], Stiffmatrix[4][a],
                    Stiffmatrix[5][a])
        except:
            error = 1
            print "Error - Stiffness Matrix not available"

# Stress tester
if not error:
    if stresstest:
        """Inital Strength test"""
        if not error:
            #try:
            Magni = [-3e-2,-3e-2]    # Skalarverdi til toyning
            Ret = [0,1]         # Mulige lastretninger STRAINS:  exx, eyy, ezz,  exy,  exz,  eyz
            strain = 0* id[0]
            for roos in range(0,len(Ret)):
                strain = strain+ Magni[roos] * id[Ret[roos]]

            ### SETTE lagringsplass

            if True:
                print '\n\nReferanse Strain Vector ', strain
                stresses = np.round(np.dot(Stiffmatrix, strain),3)
                print '\nStresses from RefSTRAINS', stresses
                Stresses = 0 * id[0]
                for roos in range(0, len(Ret)):
                    Stresses = Stresses +  stresses[Ret[0]] * id[Ret[roos]]
                print '\nReferanse Stress Vector', Stresses
                #print Stresses, Stiffmatrix
                strains = np.dot(np.linalg.inv(Stiffmatrix), Stresses)
                print '\nInitial Strain Vector', strains
                Type=''
                Dirs =''
                for roos in Ret:
                    if roos == 3 or roos == 4 or roos == 5:
                        Type = Type+'sher_'
                    else:
                        if Stresses[roos] > 0:
                            Type = Type +'tens_'
                        else:
                            Type = Type +'comp_'
                    Dirs= Dirs+Retning[roos]



            cases = [[Dirs + Type + str(int(ParameterSweep*scsc)) + '__Rand-' + str(Q), strains]]
            Sigmapaths = Tekstfiler + '/Stresstests/Sigmas' + Type + Dirs + str( int(ParameterSweep * scsc)) + '_' + str(Q) + '.txt'

            for Case in cases:
                Jobbnavn, Strain = Case
                if not Createmodel or linearAnalysis:
                    try:
                        openMdb(pathName=RVEmodellpath)
                        mod = mdb.models['Model-A']
                    except:
                        print 'Cae not found'
                        pass
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
        if Savemodel:
            mdb.saveAs(pathName=RVEmodellpath)
        d=[0.8]*6
        """Adjusting strength test"""
        if not error:
            strains2 = strains.tolist()
            Reset=1
            Jobbnav = Jobbnavn
            prev=0      #for aa vite hvor langt bak vi hoppet forrige gang
            reps = 50
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
                    mod.StaticStep(name='rep' + str(adjusts), previous=prevname, nlgeom=ON, stabilizationMagnitude=0.0002,
                                   stabilizationMethod=DAMPING_FACTOR,
                                   continueDampingFactors=False, adaptiveDampingRatio=0.05)
                    #IniTid = (StressSigs[-1, 0] - StressSigs[-2, 0]) * 0.9

                    steg = mod.steps['rep' + str(adjusts)]

                    steg.setValues(maxNumInc=Increments['maxNum'], initialInc=Increments['min']*1.1,
                                   minInc=Increments['min'], maxInc=Increments['max'], convertSDI=CONVERT_SDI_OFF)

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
                        if d[ssss]>0.3:
                            d[ssss] = d[ssss] * 0.75
                        adjfactor = abs(strains2[ssss])*d[ssss]
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
                    print 'Error making job'
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
            Q = Q + 1000
            n.append(Q)
            del section, regionToolset, dgm, part, material, assembly, step, interaction
            del load, mesh, job, sketch, visualization, xyPlot, dgo, connectorBehavior


#Oppdatere for neste iterasjon
if error:
    Q = Q +1
    n[-1] = Q
    print 'Error - Somewhere'
    del NotLikeThis
else:
    Q = Q+1
    n.append(Q)