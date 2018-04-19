# Post processing of data
def Extract_parameterdata():
    #Spenninger 12
    maxMisesStresses = list()       #0
    minMisesStresses = list()       #1
    maxPrinceStresses = list()      #2
    midPrinceStresses = list()      #3

    minPrinceStresses = list()      #4
    maxTresca = list()              #5
    minTresca = list()              #6
    maxPress = list()               #7

    minPress = list()               #8
    maxINV3 = list()                #9
    minINV3  = list()               #10
    maxSherstresses = list()        #11

    #Toyinger 4
    maxPrinceToyinger = list()      #0
    midPrinceToyinger = list()      #1
    minPrinceToyinger = list()      #2
    maxSherToyinger = list()        #3

    Spenninger=[maxMisesStresses,minMisesStresses, maxPrinceStresses,midPrinceStresses,
                minPrinceStresses,maxTresca,minTresca,maxPress,
                minPress,maxINV3,minINV3,maxSherstresses]
    Toyinger = [maxPrinceToyinger,midPrinceToyinger,minPrinceToyinger,maxSherToyinger]

    print 'Computing stresses for ' + str(sweepcases) + ' sweep cases'
    for case in range(0,sweepcases):
        odb = session.openOdb(workpath + Sweeptoyinger[case] + '.odb')
        nodalStresses = odb.steps[difstpNm].frames[-1].fieldOutputs['S'].getSubset(position=Centroid).values
        for
        if not nf==0:
            Matrix = odb.rootAssembly.instances[instanceName].elementSets['MATRIX']
            nodalStresses = odb.steps[difstpNm].frames[-1].fieldOutputs['S'].getSubset(position=ELEMENT_NODAL,
                                                                                       region=Matrix).values
            nodalStrains = odb.steps[difstpNm].frames[-1].fieldOutputs['E'].getSubset(position=ELEMENT_NODAL,
                                                                                      region=Matrix).values

        MisesS = list()
        maxPrinceS =list()
        midPrinceS =list()
        minPrinceS =list()
        TrescaS =list()
        PressS =list()
        INV3S =list()
        sherS=list()

        maxPrinceT = list()
        midPrinceT = list()
        minPrinceT = list()
        sherT=list()

        for j in range(0,len(nodalStresses)):

            MisesS.append(float(nodalStresses[j].mises))
            maxPrinceS.append(float(nodalStresses[j].maxPrincipal))
            midPrinceS.append(float(nodalStresses[j].midPrincipal))
            minPrinceS.append(float(nodalStresses[j].minPrincipal))
            TrescaS.append(float(nodalStresses[j].tresca))
            PressS.append(float(nodalStresses[j].press))
            INV3S.append(float(nodalStresses[j].inv3))
            sherS.append(sqrt(float(nodalStresses[j].data[3]) ** 2 + float(nodalStresses[j].data[4]) ** 2 + float(nodalStresses[j].data[5]) ** 2))

            maxPrinceT.append(float(nodalStrains[j].maxPrincipal))
            midPrinceT.append(float(nodalStrains[j].midPrincipal))
            minPrinceT.append(float(nodalStrains[j].minPrincipal))
            sherT.append(sqrt(float(nodalStrains[j].data[3])**2+float(nodalStrains[j].data[4])**2+float(nodalStrains[j].data[5])**2))
        odb.close()

        Spenninger[0].append(float(max(MisesS)))
        Spenninger[1].append(float(min(MisesS)))
        Spenninger[2].append(float(max(maxPrinceS)))
        Spenninger[3].append(float(max(midPrinceS)))

        Spenninger[4].append(float(min(minPrinceS)))
        Spenninger[5].append(float(max(TrescaS)))
        Spenninger[6].append(float(min(TrescaS)))
        Spenninger[7].append(float(max(PressS)))

        Spenninger[8].append(float(min(PressS)))
        Spenninger[9].append(float(max(INV3S)))
        Spenninger[10].append(float(min(INV3S)))
        Spenninger[11].append(float(max(sherS)))

        Toyinger[0].append(float(max(maxPrinceT)))
        Toyinger[1].append(float(max(midPrinceT)))
        Toyinger[2].append(float(min(minPrinceT)))
        Toyinger[3].append(float(max(sherT)))



    g = open(Envelope+str(int(nf))+'_'+str(int(Q))+'.txt', "w")
    for a in range(0, len(maxMisesStresses)):
        #                 0                         1                         2                               3                                  4
        g.write(str(Spenninger[0][a]) + '\t' + str(Spenninger[1][a]) + '\t' + str(Spenninger[2][a]) + '\t' + str(Spenninger[3][a]) + '\t' + str(Spenninger[4][a])
            + '\t' + str(Spenninger[5][a]) + '\t' + str(Spenninger[6][a]) + '\t' + str(Spenninger[7][a]) + '\t' + str(Spenninger[8][a])
            + '\t' + str(Spenninger[9][a]) + '\t' + str(Spenninger[8][a]) + '\t' + str(Spenninger[9][a]) + '\t' + str(Spenninger[10][a]) + '\t' + str(Spenninger[11][a])
            + '\t' + str(Toyinger[0][a]) + '\t' + str(Toyinger[1][a]) + '\t' + str(Toyinger[2][a]) + '\t' + str(Toyinger[3][a])+'\n')

    a=0 # Complete the Sirkel
    g.write(str(Spenninger[0][a]) + '\t' + str(Spenninger[1][a]) + '\t' + str(Spenninger[2][a]) + '\t' + str(Spenninger[3][a]) + '\t' + str(Spenninger[4][a])
            + '\t' + str(Spenninger[5][a]) + '\t' + str(Spenninger[6][a]) + '\t' + str(Spenninger[7][a]) + '\t' + str(Spenninger[8][a])
            + '\t' + str(Spenninger[9][a]) + '\t' + str(Spenninger[8][a]) + '\t' + str(Spenninger[9][a]) + '\t' + str(Spenninger[10][a]) + '\t' + str(Spenninger[11][a])
            + '\t' + str(Toyinger[0][a]) + '\t' + str(Toyinger[1][a]) + '\t' + str(Toyinger[2][a]) + '\t' + str(Toyinger[3][a]))
    g.close()
    return

Extract_parameterdata()                                                            # Abaqus Save Odb data to textfile for envelopes
