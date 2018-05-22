"""Post processing"""

def get_stiffness():
    stiffmatrix = np.zeros([6,6])
    for i in range(0,6):
        path = workpath + Enhetstoyinger[i][0]
        odb = session.openOdb(path+'.odb')

        fras = odb.steps[stepName].frames[-1]
        inst = odb.rootAssembly.instances['PART-1-MESH-1-1']
        antallElems = len(odb.rootAssembly.instances['PART-1-MESH-1-1'].elements)

        vol = np.zeros(antallElems)
        dodvolum = np.zeros(antallElems)
        SS = np.zeros([antallElems, 6])

        dataa = fras.fieldOutputs['S'].getSubset(position=CENTROID, region=inst.elementSets[
                                                     'M_AND_F'])

        dat1 = len(inst.elementSets['M_AND_F'].elements)
        for j in range(0, dat1):
            eldat = float(fras.fieldOutputs['EVOL'].getSubset(
                region=inst.elementSets['M_AND_F']).values[j].data)
            datas = dataa.values[j].data
            # Utelukker cohesive volumes ugyldige verdier, OBS! Avhenging av orientation
            if eldat > 0.0:
                SS[j] = datas
                vol[j] = float(eldat)
        dataa = fras.fieldOutputs['S'].getSubset(position=CENTROID,
                                                 region=inst.elementSets[
                                                     'INTERFACES'])
        dat2 = len(inst.elementSets['INTERFACES'].elements)
        for j in range(dat1, dat1 + dat2):
            eldat = float(fras.fieldOutputs['EVOL'].getSubset(
                region=inst.elementSets['INTERFACES']).values[
                              j - dat1].data)
            datas = dataa.values[j - dat1].data
            # Utelukker cohesive volumes ugyldige verdier, OBS! Avhenging av orientation
            if eldat > 0.0:
                SS[j][2] = float(datas[2])  # Avhenging av orientation
                SS[j][4] = float(datas[4])
                SS[j][5] = float(datas[5])
                dodvolum[j] = float(eldat)
                vol[j] = float(eldat)

            for p in range(0,6):
                stiffmatrix[i][p] = (float(np.sum(vol * SS[:, p]))/(tykkelse*(dL)**2))
        odb.close()

    np.save(lagrestiffpathmod, stiffmatrix)
    print '\nStiffnessmatrix found\n'
    g = open(Lagrestiffpathprop, "a")
    g.write(str(int(Q)) + '\t')
    for a in range(0, 6):
        print '%7f \t %7f \t %7f \t %7f \t %7f \t %7f' % (
        stiffmatrix[0][a], stiffmatrix[1][a], stiffmatrix[2][a], stiffmatrix[3][a], stiffmatrix[4][a],
        stiffmatrix[5][a])
        g.write(str(float(stiffmatrix[0][a]))+'\t'+str(float(stiffmatrix[1][a]))+'\t'+str(float(stiffmatrix[2][a]))+'\t'+str(float(stiffmatrix[3][a]))+'\t'+str(float(stiffmatrix[4][a]))+'\t'+str(float(stiffmatrix[5][a])))
        if not a==5:
            g.write('\t\t')
        g.write('\n')
    g.close()
    return stiffmatrix

global Stiffmatrix
Stiffmatrix = get_stiffness()           # Faa stiffnessmatrix

