def getHomogenizedSigmas():
    path = workpath + Jobbnavn
    print path
    odb = session.openOdb(path + '.odb')
    inst = odb.rootAssembly.instances['PART-1-MESH-1-1']
    if 0 == len(odb.steps[stegy].frames):
        del IncrementError
    antallElems = len(inst.elements)
    frj =len(odb.steps[stegy].frames)
    print 'Elementer: ', antallElems,'\tFrames: ', frj
    print 'Time completion: ', odb.steps[stegy].frames[-1].frameValue,'\tStrain completion: ', odb.steps[stegy].frames[-1].frameValue*strains[Ret]

    Sigma_frame= np.zeros([frj, 6])
    Time_frame= np.zeros(frj)
    Volume_frame = np.zeros(frj)
    DVolume_frame = np.zeros(frj)

    ###TIMEMARKER
    t = (time.time() - start_time)
    print('t ved start post pross=', t)

    for fra in range(0,frj):
        fras = odb.steps[stegy].frames[fra]
        Time_frame[fra]=fras.frameValue
        vol = np.zeros(antallElems)
        dodvolum = np.zeros(antallElems)
        SS = np.zeros([antallElems, 6])

        ###Matrix og Fibers
        dataa = fras.fieldOutputs['S'].getSubset(position=CENTROID, region=inst.elementSets['M_AND_F'])
        dat1  = len(inst.elementSets['M_AND_F'].elements)
        for j in range(0, dat1):
            eldat = float(fras.fieldOutputs['EVOL'].getSubset(region=inst.elementSets['M_AND_F']).values[j].data)
            datas = dataa.values[j].data
            # Utelukker cohesive volumes ugyldige verdier, OBS! Avhenging av orientation
            if eldat > 0.0:
                SS[j] = datas
                #print SS[j], datas
                #print 'foooer', vol[j]
                vol[j] = float(eldat)
                #print vol[j]

        #Deale med cohesives
        dataa = fras.fieldOutputs['S'].getSubset(position=CENTROID, region=inst.elementSets['INTERFACES'])
        dat2  = len(inst.elementSets['INTERFACES'].elements)
        for j in range(dat1, dat1+dat2):
            eldat = float(fras.fieldOutputs['EVOL'].getSubset(region=inst.elementSets['INTERFACES']).values[j-dat1].data)
            datas = dataa.values[j-dat1].data
            # Utelukker cohesive volumes ugyldige verdier, OBS! Avhenging av orientation
            if eldat > 0.0:
                SS[j][2]= float(datas[2])         #Avhenging av orientation
                SS[j][4]= float(datas[4])
                SS[j][5]= float(datas[5])
                dodvolum[j] = float(eldat)

        #print '\n\n########################\n Sigmas\n', Sigmas#,'\n\nvols\n',vol,'\n\n', dodvolum
        for sig in range(0,6):
            Sigma_frame[fra][sig] = np.sum(vol * SS[:,sig])
        #print 'siigis', Sigma_frame [fra]
        Volume_frame[fra]= float(np.sum(vol))
        DVolume_frame[fra]= float(np.sum(dodvolum))


    odb.close()

    #print '\n\n',tykkelse*dL*dL,Volume_frame
    #print '\n\n',Sigma_frame

    t = (time.time() - start_time)
    print 'Ferdig med aa hente data',t
    # Dele paa total volum her
    for Sigfra in range(0,frj):
        for si in range(0, 6):
            Sigma_frame[Sigfra][si] = np.multiply(Sigma_frame[Sigfra][si],1/Volume_frame[Sigfra])#(tykkelse*dL*dL)

    #t = (time.time() - start_time)
    #print('t ferdig aa dele paa volum=', t)
    ## print 'Sigmas = ',len(Sigma_frame)
    return Sigma_frame, Volume_frame,Time_frame

HomoSigs = getHomogenizedSigmas()
np.save(Tekstfiler+'Sisss', HomoSigs[0])

if not Reset:
    ss = open(Sigmapaths, "w")
    ss.write('%f\t%f\t%f\t%f\t%f\t%f\t%f\n' % (abs(strains[Ret]),0,0,0,0,0,0))
    #print HomoSigs[0][-1]
    count =0
    for s in HomoSigs[0]:
        ss.write('%f\t%f\t%f\t%f\t%f\t%f\t%f\n' % (HomoSigs[2][count],s[0], s[1], s[2], s[3], s[4], s[5]))
        count = count + 1
    ss.close()
    print 'saved to: ' ,Sigmapaths
else:
    ss = open(Sigmapaths, "w")
    for sds in StressSigs:
        ss.write('%f\t%f\t%f\t%f\t%f\t%f\t%f\n' % (sds[0], sds[1], sds[2], sds[3],
                                                   sds[4], sds[5], sds[6]))
    ss.close()

    count = 0
    if not adjusts == (reps - 1):
        ss = open(Sigmapaths, "a")
        count = 0
        for s in HomoSigs[0]:
            if not HomoSigs[2][count]==0:
                ss.write('%f\t%f\t%f\t%f\t%f\t%f\t%f\n' % (HomoSigs[2][count]+StressSigs[-1][0],s[0], s[1], s[2], s[3], s[4], s[5]))
            count = count + 1
        ss.close()
    print 'saved to: ', Sigmapaths

