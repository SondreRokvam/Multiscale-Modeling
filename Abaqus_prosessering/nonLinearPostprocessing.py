def get_intElements():
    label = []
    for elem in odbsa.rootAssembly.instances['PART-1-MESH-1-1'].elementSets['INTERFACES'].elements:
        label.append(elem.label)
    return label

def is_interface_elem(IntEls,testlab):
    for lab in IntEls:
        if lab == testlab:
            return True
    return False
def getHomogenizedSigmas():
    path = workpath + Jobbnavn
    global odbsa,Sigma_frame,Volume_frame,Time_frame
    odbsa = session.openOdb(path + '.odb')
    hj = len(odbsa.steps['Lasttoyinger'].frames[0].fieldOutputs['EVOL'].values)
    print 'Elementer: ',hj
    print 'Frames: ', len(odbsa.steps['Lasttoyinger'].frames)
    print 'Time completion: ', odbsa.steps['Lasttoyinger'].frames[-1].frameValue
    Sigma_frame= []
    Time_frame= []
    Volume_frame = []
    IntElems = get_intElements()
    for fra in range(0,len(odbsa.steps['Lasttoyinger'].frames)):
        Time_frame.append(odbsa.steps['Lasttoyinger'].frames[fra].frameValue)
        vol = 0.0
        dodvolum=0.0
        Sigs = [0.0] * 6
        for j in range(0, hj):
            eldat=float(odbsa.steps['Lasttoyinger'].frames[fra].fieldOutputs['EVOL'].values[j].data)
            datas= odbsa.steps['Lasttoyinger'].frames[fra].fieldOutputs['S'].getSubset(position=CENTROID).values[j].data
            for p in range(0,len(datas)):
                #if is_interface_elem(IntElems,odbsa.steps['Lasttoyinger'].frames[fra].fieldOutputs['S'].getSubset(position=CENTROID).values[j].elementLabel):
                if datas[0] == 0 and datas[1] == 0 and datas[3] == 0 and not fra == 0:
                    if (p==2 or p==4 or p==5) and eldat>0.0:
                        Sigs[p] = Sigs[p] + float(datas[p]) * eldat
                    dodvolum = dodvolum + eldat
                else:
                    vol = vol + eldat
                    Sigs[p] = Sigs[p] + float(datas[p]) * eldat
        Sigma_frame.append(Sigs)
        Volume_frame.append((vol, dodvolum))
    odbsa.close()
    del IntElems

    #Dele paa total volum her
    for Sigfra in range(0,len(Sigma_frame)):
        #print Sigma_frame[Sigfra],Volume_frame[Sigfra]
        for si in range(0,len(Sigma_frame[Sigfra])):
            Sigma_frame[Sigfra][si]=Sigma_frame[Sigfra][si]*(1/Volume_frame[Sigfra][0])#(tykkelse*dL*dL))#
        #print Sigma_frame[Sigfra],'\n\n'
    print 'Volumes = ',len(Volume_frame), 'initial count:',Volume_frame[0],' calc:', tykkelse*dL*dL,' dodvolum:', dodvolum, 'Stopped at:', Time_frame*strains[Ret]
    print 'Sigmas = ',len(Sigma_frame)
    return Sigma_frame, Volume_frame,Time_frame

global HomoSigs
HomoSigs = getHomogenizedSigmas()
ss = open(Sigmapaths, "w")
ss.write('%7f\t%7f\t%7f\t%7f\t%7f\t%7f\t%7f\n' % (strains[Ret],0,0,0,0,0,0))
print HomoSigs[0][-1]
count =0
for s in HomoSigs[0]:
    ss.write('%7f\t%7f\t%7f\t%7f\t%7f\t%7f\t%7f\n' % (Time_frame[count],s[0], s[1], s[2], s[3], s[4], s[5]))
    count = count + 1
ss.close()
print 'saved to: ' ,Sigmapaths
