def create_nonLinearstrainedlastcases(Strain, bob):
    a = mod.rootAssembly
    mod.StaticStep(name=difstpNm, previous='Initial', nlgeom=ON)
    steg = mod.steps[difstpNm]
    steg.setValues(maxNumInc=Increments['maxNum'], initialInc=Increments['initial'] ,minInc=Increments['min'],
        maxInc=Increments['max'],convertSDI=CONVERT_SDI_OFF)
    if Dampening:
        steg.setValues(stabilizationMethod=DAMPING_FACTOR, stabilizationMagnitude=Stabl_Magn,
                                            adaptiveDampingRatio=Atapt_Damp_Ratio)
        # stabilizationMethod=DAMPING_FACTOR, stabilizationMagnitude=Stabl_Magn,
    steg.Restart(frequency=10,
        numberIntervals=0, overlay=OFF, timeMarks=OFF)
    mod.fieldOutputRequests['F-Output-1'].setValues(variables=('DAMAGEC', 'DAMAGET', 'LE','PE', 'PEEQ',
                                                               'RT', 'S', 'SDEG','STATUS', 'STATUSXFEM',
                                                               'U','EVOL'),frequency=1)

    mod.historyOutputRequests['H-Output-1'].setValues(variables=( 'ALLDMD', 'ALLIE', 'ALLSD'))

    #Tracke reaksjoner
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

def getSum22_33():
    path = workpath + Jobbnavn
    odb = session.openOdb(path + '.odb')
    instance = odb.rootAssembly.instances[instanceName]
    vol=0.0
    Sigs=[0.0]*6
    print len(instance.elements)
    for j in range(0, len(instance.elements)):
        elvol = odb.steps[difstpNm].frames[-1].fieldOutputs['EVOL']
        vol=vol + elvol.values[j].data
        S = odb.steps[difstpNm].frames[-1].fieldOutputs['S'].getSubset(position=CENTROID)
        for p in range(0, 6):
            Sigs[p] = Sigs[p] + S.values[j].data[p] * elvol.values[j].data
        print j, Sigs, vol
    odb.close()
    #print(tykkelse * (dL) ** 2), vol, Sigs
    Sag=[0.0]*6
    for k in range(0, 6):
        Sag[k] = Sigs[k] / (tykkelse * (dL) ** 2)  # Volume
        Sigs[k] = Sigs[k] / vol  # Volume
    print Sigs,Sag
    return
def getAverageStressStrain():
    """
    path = workpath + Jobbnavn
    odb = session.openOdb(name='C:/Temp/TensionX_NothingElse.odb')
    global s11xy, s22xy, s33xy, Evol
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
                                                                                            'EVOL', WHOLE_ELEMENT),),
                                       elementSets=(' ALL ELEMENTS',))
    VolumePerTime = []
    VolweightedS11 = []

    for frame in range(0,len(Evol[0])):
        elementVolumes = []
        for Element in Evol:
            elementVolumes.append(Element[frame][1])
        VolumePerTime.append(sum(elementVolumes))
    ggg = open('C:/Users/Rockv/Desktop/Nytt tekstdokument.txt', "w")
    ggg.write(VolumePerTime)
    ggg.close()
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
getSum22_33()
#getAverageStressStrain()