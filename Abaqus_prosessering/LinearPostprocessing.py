"""Post processing"""

def get_stiffness():
    stiffmatrix = np.zeros([6,6])
    for i in range(0,6):
        path = workpath + Enhetstoyinger[i][0]
        odb = session.openOdb(path+'.odb')
        instance = odb.rootAssembly.instances[instanceName]
        for j in range(0,len(instance.elements)):
            v = odb.steps[stepName].frames[-1].fieldOutputs['S'].getSubset(position=CENTROID).values[j]
            elvol = odb.steps[stepName].frames[-1].fieldOutputs['EVOL'].values[j]
            for p in range(0,6):
                stiffmatrix[i][p] = stiffmatrix[i][p]+(v.data[p]*elvol.data)/(tykkelse*(dL)**2)
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

