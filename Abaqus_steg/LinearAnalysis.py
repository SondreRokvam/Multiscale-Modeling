# Linear
def create_Linearunitstrainslastcases():

    a = mod.rootAssembly
    #Create step Linear step
    mod.StaticStep(name=stepName, previous='Initial')
    #Request outputs
    mod.fieldOutputRequests['F-Output-1'].setValues(variables=('S', 'EVOL','U'))
    #Run the simulations to create stiffnessmatrix
    print '\nComputing stresses for normalized unit strains'
    for i in range(0,6):#   arg:   +   ,len(id)+1

        #Laste inn toyningscase
        exx, eyy, ezz, exy, exz, eyz = id[i]
        mod.DisplacementBC(name='BCX', createStepName=stepName,
                           region=a.sets['RPX'], u1=exx, u2=exy, u3=exz, ur1=UNSET, ur2=UNSET, ur3=UNSET,
                           amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)

        mod.DisplacementBC(name='BCY', createStepName=stepName,
                           region=a.sets['RPY'], u1=exy, u2=eyy, u3=eyz, ur1=UNSET, ur2=UNSET, ur3=UNSET,
                           amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)

        mod.DisplacementBC(name='BCZ', createStepName=stepName,
                           region=a.sets['RPZ'], u1=exz, u2=eyz, u3=ezz, ur1=UNSET, ur2=UNSET, ur3=UNSET,
                           amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)
        run_Job(Enhetstoyinger[i][0],modelName)
        del exx, eyy, ezz, exy, exz, eyz
def create_Linearsweepedlastcases(sweep):
    mod = mdb.models[modelName]
    a = mod.rootAssembly
    mod.fieldOutputRequests['F-Output-1'].setValues(variables=('S', 'MISES', 'E', 'U', 'ELEDEN'))
    mod.steps.changeKey(fromName=stepName, toName=difstpNm)
    print '\nComputing strains for normalized load sweep'
    #Lagring av output data base filer .odb
    for case in range(0,sweepcases):

        print '\nLoad at'+str(360*case/sweepcases)+'deg'
        exx, eyy, ezz, exy, exz, eyz = sweep[case]
        mod.boundaryConditions['BCX'].setValues(u1=exx, u2=exy, u3=exz)
        mod.boundaryConditions['BCY'].setValues(u1=exy, u2=eyy, u3=eyz)
        mod.boundaryConditions['BCZ'].setValues(u1=exz, u2=eyz, u3=ezz)
        Jobw = Sweeptoyinger[case]
        run_Job(Jobw, modelName)
    del a, Jobw, case
def get_stiffness():
    stiffmatrix = []
    for i in range(0,6):
        path = workpath + Enhetstoyinger[i][0]
        odb = session.openOdb(path+'.odb')
        instance = odb.rootAssembly.instances[instanceName]

        sag=[0.0] * 6
        for j in range(0,len(instance.elements)):
            v = odb.steps[stepName].frames[-1].fieldOutputs['S'].getSubset(position=CENTROID)
            elvol = odb.steps[stepName].frames[-1].fieldOutputs['EVOL']
            for p in range(0,6):
                sag[p] = sag[p]+v.values[j].data[p]*elvol.values[j].data
        odb.close()
        for k in range(0,6):
            sag[k]= sag[k]/(tykkelse*(dL)**2) #Volume
        stiffmatrix.append(sag)
    print '\n'
    g = open(lagrestiffpath, "a")
    #g = open(lagrestiffpath, "a")
    print '\nStiffnessmatrix found\n'
    g.write(str(FaktiskVf) + '\t'+ str(int(Q)) + '\t')
    for a in range(0, 6):
        g.write(str(float(stiffmatrix[0][a]))+'\t'+str(float(stiffmatrix[1][a]))+'\t'+str(float(stiffmatrix[2][a]))+'\t'+str(float(stiffmatrix[3][a]))+'\t'+str(float(stiffmatrix[4][a]))+'\t'+str(float(stiffmatrix[5][a])))
        if not a==5:
            g.write('\t\t')
        print '%7f \t %7f \t %7f \t %7f \t %7f \t %7f' % (stiffmatrix[0][a], stiffmatrix[1][a], stiffmatrix[2][a], stiffmatrix[3][a], stiffmatrix[4][a], stiffmatrix[5][a])
    g.write('\n')
    g.close()
    return stiffmatrix
def get_compliance(Stiffmatrix):
    print '\nCompliancematrix found'
    try:
        inverse = np.linalg.inv(Stiffmatrix)
    except np.linalg.LinAlgError:
        # Not invertible. Skip this one.
        print 'ERROR in inverting with numpy'
        pass    #intended break
    for a in range(0, 6):
        print inverse[0][a],'\t', inverse[1][a],'\t', inverse[2][a],'\t', inverse[3][a],'\t',inverse[4][a],'\t', inverse[5][a]
    inverse = inverse.tolist()
    return inverse
def get_sweepstrains_sig2_sig3(Compliancematrix,sweepresolution):
    sweep=list()
    x= np.arange(0,2*pi,sweepresolution)
    x =x.tolist()
    print '\nStrains from stress sweep at angle \n',
    print  x,'\n'
    for d in range(0, len(x)):
        sig2 = cos(x[d])
        sig3 = sin(x[d])
        a=np.dot(Compliancematrix,[0,sig2,sig3,0,0,0])

        a = a.tolist()
        print a
        sweep.append(a)
    return sweep


"""     STIFFNESS  MATRIX       """
create_Linearunitstrainslastcases()     # Unit strain cases. Set boundary condition and create job.
Stiffmatrix = get_stiffness()           # Faa stiffnessmatrix


"""     Compliance matrix and sweepes stress envelopes"""

#Compliancematrix = get_compliance(Stiffmatrix)  # Inverter til compliance materix
#sweepstrains = get_sweepstrains_sig2_sig3(Compliancematrix, sweepresolution)  # Finne strains for sweep stress case
#create_Linearsweepedlastcases(sweepstrains)