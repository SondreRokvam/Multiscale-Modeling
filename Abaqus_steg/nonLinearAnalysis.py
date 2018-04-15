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
    instance = odb.rootAssembly.instances['PART-1-MESH-1-1']
    All=[]
    for frame in odb.steps['Lasttoyinger'].frames:
        Vol=0.0
        Frame =[]
        for tt in range(0, len(instance.elements)):
            Vol = Vol + float(frame.fieldOutputs['EVOL'].values[tt].data)
        for j in range(0, len(instance.elements)):
            v = frame.fieldOutputs['S'].getSubset(region=instance.elements[j]).values[0]
            elvol = frame.fieldOutputs['EVOL'].values[j].data
            Frame.append((float(v.maxPrincipal)/float(elvol))/Vol)
        All.append((float(sum(Frame)), float(frame.description.split("Step Time =")[1])))
    odb.close()
    ggg = open('C:/Users/Rockv/Desktop/Nytt tekstdokument.txt', "a")
    ggg.write(All)
    g.close()
#create_nonLinearstrainedlastcases(Strain, Jobbnavn)
getAverageStressStrain()