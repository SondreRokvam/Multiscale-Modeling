def create_nonLinearstrainedlastcases(Strain, bob):
    a = mod.rootAssembly
    mod.StaticStep(name=difstpNm, previous='Initial', nlgeom=ON)
    mod.steps['Lasttoyinger'].setValues(maxNumInc=Increments['maxNum'], initialInc=Increments['initial'] ,minInc=Increments['min'],
        maxInc=Increments['max'],convertSDI=CONVERT_SDI_OFF)
    if Dampening:
        mod.steps['Lasttoyinger'].setValues(stabilizationMethod=DAMPING_FACTOR, stabilizationMagnitude=Stabl_Magn,
                                            adaptiveDampingRatio=Atapt_Damp_Ratio)
        # stabilizationMethod=DAMPING_FACTOR, stabilizationMagnitude=Stabl_Magn,
    mod.fieldOutputRequests['F-Output-1'].setValues(variables=('DAMAGEC', 'DAMAGET', 'LE',
                                    'PE', 'PEEQ', 'RT', 'S', 'SDEG','STATUS', 'STATUSXFEM', 'U','EVOL'),frequency=1)

    mod.historyOutputRequests['H-Output-1'].setValues(variables=( 'ALLDMD', 'ALLIE', 'ALLSD'))
    a.SetByBoolean(name='RPS', sets=(a.sets['RPX'], a.sets['RPY'], a.sets['RPZ'],))
    regDef = mdb.models['Model-A'].rootAssembly.sets['RPS']
    mod.HistoryOutputRequest(name='H-Output-2',
                             createStepName='Lasttoyinger', variables=('RT', 'UT'),
                             region=regDef, sectionPoints=DEFAULT, rebar=EXCLUDE)
    print bob,': ', Strain,'       Increments : ',Increments
    print '\nnon Linear load analysis'
    # Lagring av output data base filer .odb
    exx, eyy, ezz, exy, exz, eyz = Strain
    mod.DisplacementBC(name='BCX', createStepName=difstpNm,
                       region=a.sets['RPX'], u1=exx, u2=exy, u3=exz, ur1=UNSET, ur2=UNSET, ur3=UNSET,
                       amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)

    mod.DisplacementBC(name='BCY', createStepName=difstpNm,
                       region=a.sets['RPY'], u1=exy, u2=eyy, u3=eyz, ur1=UNSET, ur2=UNSET, ur3=UNSET,
                       amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)

    mod.DisplacementBC(name='BCZ', createStepName=difstpNm,
                       region=a.sets['RPZ'], u1=exz, u2=eyz, u3=ezz, ur1=UNSET, ur2=UNSET, ur3=UNSET,
                       amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)


    run_Job(bob, modelName)
def getAverageStressStrain():
    path = workpath + Jobbnavn
    odb = session.openOdb(path+'.odb')
    """
    xyList = xyPlot.xyDataListFromField(odb=odb, outputPosition=INTEGRATION_POINT,
                                        variable=(('S', INTEGRATION_POINT, ((INVARIANT, 'Max. Principal'),)),
                                                  ),
                                        elementSets=('PART-1-MESH-1-1.INTERFACES', 'PART-1-MESH-1-1.MATRIX',
                                                     ))
    kjk =  [sum(abs(xyList[:][0])),xyList[:][1]]
    odb.close()
    """
    instance = odb.rootAssembly.instances['PART-1-MESH-1-1']
    Intface = instance.elements
    ggg = open('C:/Users/Rockv/Desktop/Nytt tekstdokument.txt', "w")
    ggg.close()
    ggg = open('C:/Users/Rockv/Desktop/Nytt tekstdokument.txt', "a")
    for frame in range(0, 100):
        Framy = odb.steps['Lasttoyinger'].frames[frame]
        Vol=0.0
        tt=0
        while tt <len(Intface):
            Vol = Vol + float(Framy.fieldOutputs['EVOL'].values[tt].data)
            tt= tt + 1
        tt = 0
        Fram=[]
        while tt < len(Intface):
            v = Framy.fieldOutputs['S'].getSubset(region=instance.elements[tt]).values[0]
            elvol = Framy.fieldOutputs['EVOL'].values[tt].data
            Fram.append((abs(float(v.maxPrincipal)/float(elvol))/Vol))
            tt = tt + 1
        ggg.write(str(float(sum(Fram))+'\t'+ str(float(frame.description.split("Step Time =")[1])))+'\n')
    #for lens in kjk:
    #   ggg.write(str(lens[0])+'\t' + str(lens[1])+'\n')
    ggg.close()
    odb.close()
create_nonLinearstrainedlastcases(Strain, Jobbnavn)
getAverageStressStrain()