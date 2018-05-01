def getHomogenizedSigmas():
    path = workpath + Jobbnavn
    global odbsa,Sigma_frame,Volume_frame,Time_frame
    odbsa = session.openOdb(path + '.odb')
    instance = odbsa.rootAssembly.instances[instanceName]
    print 'Elementer: ',len(instance.elements)
    print 'Frames: ', len(odbsa.steps['Lasttoyinger'].frames)
    print 'Time completion: ', odbsa.steps['Lasttoyinger'].frames[-1].frameValue
    Sigma_frame= []
    Volume_frame = []
    Time_frame= []

    Volume_frame = []
    Time_frame.append(0.0)
    #for fra in range(0,len(odbsa.steps['Lasttoyinger'].frames)):
    fra=-1
    Time_frame.append(odbsa.steps['Lasttoyinger'].frames[fra].frameValue)
    vol = float(0.0)
    elvol = odbsa.steps[difstpNm].frames[fra].fieldOutputs['EVOL']
    for j in range(0, len(instance.elements)):
        vol = vol + float(elvol.values[j].data)
    Volume_frame.append(vol)
    Sigs = [0.0] * 6
    Sigma_frame.append(Sigs)
    for j in range(0, len(instance.elements)):
        datas= odbsa.steps['Lasttoyinger'].frames[fra].fieldOutputs['S'].values[j].data
        for p in range(0,len(datas)):
            print datas
            # Apenbart at vi ikke kan summere ikke eksisterende verdier.
            # Om element er cohesive saa unngaar vi aa legge de til
            #
            Sigs[p] = Sigs[p] + float(datas[p]) * float(elvol.values[j].data)
        print Sigs
    Sigma_frame.append(Sigs)
    odbsa.close()
    #Flytte dele paa total volum hit
    print 'Volumes = ',len(Volume_frame), 'initial count:',Volume_frame[0],' calc:', tykkelse*dL*dL
    print 'Sigmas = ',len(Sigma_frame)
    return Sigma_frame, Volume_frame,Time_frame
HomoSigs = getHomogenizedSigmas()
ss = open(Sigmapaths, "w")
count =0
for s in HomoSigs[0]:
    ss.write('%7f\t%7f\t%7f\t%7f\t%7f\t%7f\t%7f\n' % (Time_frame[count],s[0], s[1], s[2], s[3], s[4], s[5]))
    count = count + 1
ss.close()
