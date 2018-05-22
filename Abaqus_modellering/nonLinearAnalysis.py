def create_nonLinearstrainedlastcases(Strain, Jobbinfo):
    #if linearAnalysis:
        #del mdb.models['Model-A'].steps[stepName]
    a = mod.rootAssembly

    #Sett opp steg
    mod.StaticStep(name=difstpNm, previous='Initial', nlgeom=ON)
    steg = mod.steps[difstpNm]
    steg.setValues(maxNumInc=Increments['maxNum'], initialInc=Increments['initial'] ,minInc=Increments['min'],
        maxInc=Increments['max'],convertSDI=CONVERT_SDI_OFF)
    steg.Restart(frequency=1, numberIntervals=0, overlay=ON, timeMarks=OFF)

    # ON/OFF aktivere Demping
    if Dampening:
        steg.setValues(stabilizationMethod=DAMPING_FACTOR, stabilizationMagnitude=Stabl_Magn,
                                            adaptiveDampingRatio=Atapt_Damp_Ratio)
        # stabilizationMethod=DAMPING_FACTOR, stabilizationMagnitude=Stabl_Magn,

    # Outputs
    mod.fieldOutputRequests['F-Output-1'].setValues(variables=('DAMAGEC', 'DAMAGET', 'LE','PE', 'PEEQ',
                                                               'RT', 'S', 'SDEG','STATUS', 'STATUSXFEM',
                                                               'U','EVOL'),frequency=1)
    mod.historyOutputRequests['H-Output-1'].setValues(variables=( 'ALLDMD', 'ALLIE', 'ALLSD'))

    # Tracke reaksjoner
    a.SetByBoolean(name='RPS', sets=(a.sets['RPX'], a.sets['RPY'], a.sets['RPZ'],))
    regDef = mdb.models['Model-A'].rootAssembly.sets['RPS']
    mod.HistoryOutputRequest(name='H-Output-2',createStepName='Lasttoyinger',
                             variables=('RT', 'UT'),region=regDef,
                             sectionPoints=DEFAULT, rebar=EXCLUDE)

    print '\nJob : ',Jobbinfo,'\nStrains : ',Strain,'\nIncrements : ',Increments
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


    run_Job(Jobbinfo, modelName)

def getHomogenizedSigmas():
    path = workpath + Jobbnavn
    global odbsa
    odbsa = session.openOdb(path + '.odb')
    instance = odbsa.rootAssembly.instances[instanceName]
    vol=0.0
    Sigs=[0.0]*6
    print len(instance.elements)
    for j in range(0, len(instance.elements)):
        elvol = odbsa.steps[difstpNm].frames[-1].fieldOutputs['EVOL']
        vol=vol + elvol.values[j].data
        S = odbsa.steps[difstpNm].frames[-1].fieldOutputs['S'].getSubset(position=CENTROID)
        for p in range(0, 6):
            print S.values[j].data[p], elvol.values[j].data
            Sigs[p] = Sigs[p] + S.values[j].data[p] * elvol.values[j].data
        print j, Sigs, vol
    odbsa.close()
    #print(tykkelse * (dL) ** 2), vol, Sigs
    Sag=[0.0]*6
    for k in range(0, 6):
        Sag[k] = Sigs[k] / (tykkelse * (dL) ** 2)  # Volume
        Sigs[k] = Sigs[k] / vol  # Volume
    print Sigs,Sag
    return

create_nonLinearstrainedlastcases(Strain, Jobbnavn)

