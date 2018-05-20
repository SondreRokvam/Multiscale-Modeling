def getHomogenizedSigmas():
    path = workpath + Jobbnavn
    print path
    global od
    od = session.openOdb(path + '.odb')
    antallElems = len(od.steps['Lasttoyinger'].frames[0].fieldOutputs['EVOL'].values)
    frj =len(od.steps['Lasttoyinger'].frames)
    print 'Elementer: ', antallElems
    print 'Frames: ', frj
    print 'Time completion: ', od.steps['Lasttoyinger'].frames[-1].frameValue
    print 'Strain completion: ', od.steps['Lasttoyinger'].frames[-1].frameValue*strains[Ret]
    Sigma_frame= np.zeros([frj, 6])
    Time_frame= np.zeros(frj)
    Volume_frame = np.zeros(frj)
    DVolume_frame = np.zeros(frj)

    for fra in range(0,frj):
        fras = od.steps['Lasttoyinger'].frames[fra]
        Time_frame[fra]=od.steps['Lasttoyinger'].frames[fra].frameValue
        vol = 0.0
        dodvolum=0.0
        for j in range(0, antallElems):
            eldat = float(fras.fieldOutputs['EVOL'].values[j].data)
            vol = vol + eldat
            datas = fras.fieldOutputs['S'].getSubset(position=CENTROID).values[j].data
            if datas[0] == 0:
                if datas[1] == 0:
                    if datas[3] == 0:
                        if not fra == 0:
                            if eldat > 0.0:
                                for p in [2,4,5]:   #Avhenging
                                    Sigma_frame[fra][p] = Sigma_frame[fra][p] + float(datas[p]) * eldat
                                dodvolum = dodvolum + eldat
            else:
                for p in range(0,len(datas)):
                    Sigma_frame[fra][p] = Sigma_frame[fra][p] + float(datas[p]) * eldat
        Volume_frame[fra]= vol
        DVolume_frame[fra]= dodvolum
    #od.close()
    print 'Ferdig med aa hente data'
    # Dele paa total volum her
    for Sigfra in range(0,len(Sigma_frame)):
        # print Sigma_frame[Sigfra],Volume_frame[Sigfra]
        for si in range(0,len(Sigma_frame[Sigfra])):
            Sigma_frame[Sigfra][si]=Sigma_frame[Sigfra][si]*(1/Volume_frame[Sigfra])#(tykkelse*dL*dL))#
        # print Sigma_frame[Sigfra],'\n\n'
    print 'Volumes = ',len(Volume_frame), 'initial count:',Volume_frame[0],' calc:', tykkelse*dL*dL,' dodvolum:', dodvolum
    print 'Sigmas = ',len(Sigma_frame)
    return Sigma_frame, Volume_frame,Time_frame


global HomoSigs
HomoSigs = getHomogenizedSigmas()
ss = open(Sigmapaths, "w")
ss.write('%7f\t%7f\t%7f\t%7f\t%7f\t%7f\t%7f\n' % (strains[Ret],0,0,0,0,0,0))
ss.write('%7f\t%7f\t%7f\t%7f\t%7f\t%7f\t%7f\n' % (strains[Ret],0,0,0,0,0,0))
print HomoSigs[0][-1]
count =0
for s in HomoSigs[0]:
    ss.write('%7f\t%7f\t%7f\t%7f\t%7f\t%7f\t%7f\n' % (HomoSigs[2][count],s[0], s[1], s[2], s[3], s[4], s[5]))
    count = count + 1
ss.close()
print 'saved to: ' ,Sigmapaths
