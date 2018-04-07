def create_nonLinearstrainedlastcases(Strain, bob):
    a = mod.rootAssembly
    mod.StaticStep(name=difstpNm, previous='Initial', nlgeom=ON)
    mod.steps['Lasttoyinger'].setValues(maxNumInc=Increments['maxNum'], initialInc=Increments['initial'] ,minInc=Increments['min'],
        maxInc=Increments['max'])
    if Dampening:
        mod.steps['Lasttoyinger'].setValues(stabilizationMagnitude=0.0002,
                                                              stabilizationMethod=DAMPING_FACTOR,
                                                              continueDampingFactors=False, adaptiveDampingRatio=0.05)
    mdb.models['Model-A'].fieldOutputRequests['F-Output-1'].setValues(variables=(
        'DAMAGEC', 'DAMAGET', 'LE', 'MISES', 'PE', 'PEEQ', 'RT', 'S', 'SDEG',
        'STATUS', 'STATUSXFEM', 'U'),frequency=1)

    mod.historyOutputRequests['H-Output-1'].setValues(variables=(
        'ALLDMD', 'ALLIE', 'ALLSD'))
    a.SetByBoolean(name='RPS', sets=(a.sets['RPX'], a.sets['RPY'], a.sets['RPZ'],))
    regDef = mdb.models['Model-A'].rootAssembly.sets['RPS']
    mod.HistoryOutputRequest(name='H-Output-2',
                             createStepName='Lasttoyinger', variables=('RT', 'UT'),
                             region=regDef, sectionPoints=DEFAULT, rebar=EXCLUDE)
    print bob,': ', Strain,'       Increments : ',Increments
    print '\nnon Linear load analysis'
    # Lagring av output data base filer .odb
    for case in range(0, 1):
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


        run_Job(bob+'job'+str(case), modelName)
create_nonLinearstrainedlastcases(Strain, Jobbnavn)