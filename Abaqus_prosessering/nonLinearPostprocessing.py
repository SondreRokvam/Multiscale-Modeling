def getHomogenizedSigmas():
    path = workpath + Jobbnavn
    global odbsa,Sigma_frame,Volume_frame,Time_frame
    odbsa = session.openOdb(path + '.odb')
    instance = odbsa.rootAssembly.instances[instanceName]
    print 'Elementer: ',len(instance.elements)
    print 'Sig Elementer0: ',len(odbsa.steps['Lasttoyinger'].frames[0].fieldOutputs['S'].values)
    print 'Sig Elementer1: ',len(odbsa.steps['Lasttoyinger'].frames[-1].fieldOutputs['S'].values)
    print 'Evol Elementer0: ',len(odbsa.steps['Lasttoyinger'].frames[0].fieldOutputs['EVOL'].values)
    print 'Evol Elementer1: ',len(odbsa.steps['Lasttoyinger'].frames[-1].fieldOutputs['EVOL'].values)
    print 'Frames: ', len(odbsa.steps['Lasttoyinger'].frames)
    print 'Time completion: ', odbsa.steps['Lasttoyinger'].frames[-1].frameValue
    Sigma_frame= []
    Time_frame= []
    Volume_frame = []
    for fra in range(0,len(odbsa.steps['Lasttoyinger'].frames)):
        Time_frame.append(odbsa.steps['Lasttoyinger'].frames[fra].frameValue)
        vol = float(0.0)
        elvol = odbsa.steps['Lasttoyinger'].frames[-1].fieldOutputs['EVOL'].values
        for j in range(0, len(instance.elements)):
            vol = vol + float(elvol[j].data)
        Volume_frame.append(vol)
        Sigs = [0.0] * 6
        for j in range(0, len(instance.elements)):
            datas= odbsa.steps['Lasttoyinger'].frames[fra].fieldOutputs['S'].values[j].data
            for p in range(0,len(datas)):
                if str(odbsa.steps['Lasttoyinger'].frames[-1].fieldOutputs['S'].values[j].baseElementType)=='COH3D8':
                    print 'Data set',p,'  elem',j,'sig',p,' var',Sigs[p], 'sig',p,'er:', Sigs[p] + float(datas[p]) * float(elvol[j].data)
                    print '\n',datas,'\n\n',elvol[j].data

                # Apenbart at vi ikke kan summere ikke eksisterende verdier.
                # Om element er cohesive saa unngaar vi aa legge de til
                #
                Sigs[p] = Sigs[p] + float(datas[p]) * float(elvol[j].data)
            #print 'Sigma this Frame',Sigs
        Sigma_frame.append(Sigs)
    odbsa.close()
    #Dele paa total volum her
    for Sigfra in range(0,len(Sigma_frame)):
        #print Sigma_frame[Sigfra],Volume_frame[Sigfra]
        for si in range(0,len(Sigma_frame[Sigfra])):
            Sigma_frame[Sigfra][si]=Sigma_frame[Sigfra][si]*(1/Volume_frame[Sigfra])#(tykkelse*dL*dL))#
        #print Sigma_frame[Sigfra],'\n\n'
    print 'Volumes = ',len(Volume_frame), 'initial count:',Volume_frame[0],' calc:', tykkelse*dL*dL
    print 'Sigmas = ',len(Sigma_frame)
    return Sigma_frame, Volume_frame,Time_frame
HomoSigs = getHomogenizedSigmas()
ss = open(Sigmapaths, "w")
print HomoSigs[0][-1]
count =0
for s in HomoSigs[0]:
    ss.write('%7f\t%7f\t%7f\t%7f\t%7f\t%7f\t%7f\n' % (Time_frame[count],s[0], s[1], s[2], s[3], s[4], s[5]))
    count = count + 1
ss.close()
print 'saved to: ' ,Sigmapaths
