def getHomogenizedSigmas():
    path = workpath + Jobbnavn
    global od
    od = session.openOdb(path + '.odb')


    antallElems = len(od.rootAssembly.instances['PART-1-MESH-1-1'].elements)
    print     antallElems
    frj =len(od.steps['Lasttoyinger'].frames)
    print 'Elementer: ', antallElems,'\nFrames: ', frj
    print 'Time completion: ', od.steps['Lasttoyinger'].frames[-1].frameValue,'\nStrain completion: ', od.steps['Lasttoyinger'].frames[-1].frameValue*strains[Ret]

    Sigma_frame= np.zeros([frj, 6])
    Time_frame= np.zeros(frj)
    Volume_frame = np.zeros(frj)
    DVolume_frame = np.zeros(frj)

    ###TIMEMARKER
    t = (time.time() - start_time)
    print('t ved start post pross=', t)

    for fra in range(0,frj):
        fras = od.steps['Lasttoyinger'].frames[fra]
        Time_frame[fra]=fras.frameValue
        vol = np.zeros(antallElems)
        dodvolum = np.zeros(antallElems)
        SS = np.zeros([antallElems, 6])

        ###Matrix og Fibers
        dataa = fras.fieldOutputs['S'].getSubset(position=CENTROID, region=od.rootAssembly.instances['PART-1-MESH-1-1'].elementSets['M_AND_F'])
        dat1  = len(od.rootAssembly.instances['PART-1-MESH-1-1'].elementSets['M_AND_F'].elements)
        for j in range(0, dat1):
            eldat = float(fras.fieldOutputs['EVOL'].getSubset(region=od.rootAssembly.instances['PART-1-MESH-1-1'].elementSets['M_AND_F']).values[j].data)
            datas = dataa.values[j].data
            # Utelukker cohesive volumes ugyldige verdier, OBS! Avhenging av orientation
            if eldat > 0.0:
                SS[j] = datas
                print SS[j], datas
                print 'foooer', vol[j]
                vol[j] = float(eldat)
                print vol[j]

        #Deale med cohesives
        dataa = fras.fieldOutputs['S'].getSubset(position=CENTROID, region=od.rootAssembly.instances['PART-1-MESH-1-1'].elementSets['INTERFACES'])
        dat2  = len(od.rootAssembly.instances['PART-1-MESH-1-1'].elementSets['INTERFACES'].elements)
        for j in range(dat1, dat1+dat2):
            eldat = float(fras.fieldOutputs['EVOL'].getSubset(region=od.rootAssembly.instances['PART-1-MESH-1-1'].elementSets['INTERFACES']).values[j-dat1].data)
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
        print 'siigis', Sigma_frame [fra]
        Volume_frame[fra]= float(np.sum(vol))
        DVolume_frame[fra]= float(np.sum(dodvolum))


    #od.close()
    print 'Ferdig med aa hente data'
    t = (time.time() - start_time)
    print '\n\n',tykkelse*dL*dL,Volume_frame

    print '\n\n',Sigma_frame
    print 'Ferdig med aa printe data'
    t = (time.time() - start_time)
    # Dele paa total volum her
    for Sigfra in range(0,frj):
        for si in range(0, 6):
            Sigma_frame[Sigfra][si] = np.multiply(Sigma_frame[Sigfra][si],1/Volume_frame[Sigfra])#(tykkelse*dL*dL)

    t = (time.time() - start_time)
    print('t ferdig aa dele paa volum=', t)
    ## print 'Sigmas = ',len(Sigma_frame)
    return Sigma_frame, Volume_frame,Time_frame


global HomoSigs
HomoSigs = getHomogenizedSigmas()
ss = open(Sigmapaths, "w")
ss.write('%7f\t%7f\t%7f\t%7f\t%7f\t%7f\t%7f\n' % (strains[Ret],0,0,0,0,0,0))
ss.write('%7f\t%7f\t%7f\t%7f\t%7f\t%7f\t%7f\n' % (strains[Ret],0,0,0,0,0,0))
#print HomoSigs[0][-1]
count =0
for s in HomoSigs[0]:
    ss.write('%7f\t%7f\t%7f\t%7f\t%7f\t%7f\t%7f\n' % (HomoSigs[2][count],s[0], s[1], s[2], s[3], s[4], s[5]))
    count = count + 1
ss.close()
print 'saved to: ' ,Sigmapaths
t = (time.time() - start_time)
print('t =', t)
