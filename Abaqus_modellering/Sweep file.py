#Sweepcases kode
    #if False:
        #sweepcases = 1  # Stress sweeps cases. Decides sweep resolution
        #sweepresolution = 2 * pi / sweepcases
        #Sweeptoyinger = [''] * sweepcases  # Sweepcasesog n relative ABAQUS Jobb navn
        #for g in range(0, sweepcases):
        #    Sweeptoyinger[g] = ('Sweep_strain' + str(int(ParameterSweep[ItraPara])) + '_' + str(
        #        int(g * 180 * sweepresolution / pi)) + '__' + str(int(Q)))

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


"""     Compliance matrix and sweepes stress envelopes"""

#Compliancematrix = get_compliance(Stiffmatrix)  # Inverter til compliance materix
#sweepstrains = get_sweepstrains_sig2_sig3(Compliancematrix, sweepresolution)  # Finne strains for sweep stress case
#create_Linearsweepedlastcases(sweepstrains)