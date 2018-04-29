def getHomogenizedSigmas():
    path = workpath + Jobbnavn
    global odbsa,Sigma_frame,Volume_frame,Time_frame
    odbsa = session.openOdb(path + '.odb')
    instance = odbsa.rootAssembly.instances[instanceName]
    print 'Elementer: ',len(instance.elements)
    print 'Frames: ', len(odbsa.steps['Lasttoyinger'].frames)
    Sigma_frame= []
    Volume_frame = []
    Time_frame=[]
    for fra in range(0,len(odbsa.steps['Lasttoyinger'].frames)):
        Time_frame.append(odbsa.steps['Lasttoyinger'].frames[fra].frameValue)
        vol = float(0.0)
        for j in range(0, len(instance.elements)):
            elvol = odbsa.steps[difstpNm].frames[fra].fieldOutputs['EVOL']
            vol = vol + float(elvol.values[j].data)
        Volume_frame.append(vol)
        Sigs = [0.0] * 6
        for j in range(0, len(instance.elements)):
            elvol = odbsa.steps[difstpNm].frames[fra].fieldOutputs['EVOL']
            datas= odbsa.steps['Lasttoyinger'].frames[fra].fieldOutputs['S'].values[j].data
            for p in range(0,len(datas)):
                Sigs[p] = Sigs[p] + float(datas[p]) * float(elvol.values[j].data)/float(vol)
        Sigma_frame.append(Sigs)
    odbsa.close()
    print 'Volumes = ',len(Volume_frame), 'initial count:',Volume_frame[0],' calc:', tykkelse*dL*dL
    print 'Sigmas = ',len(Sigma_frame)
    return Sigma_frame, Volume_frame,Time_frame
HomoSigs = getHomogenizedSigmas()
print HomoSigs