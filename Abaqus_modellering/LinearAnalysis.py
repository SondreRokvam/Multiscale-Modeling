# Linear
def create_Linearunitstrainslastcases():
    a = mod.rootAssembly
    p = mod.parts[meshPartName]
    if Interface and not noFibertest:
        if ConDmPlast:
            del mod.materials['interface'].quadsDamageInitiation
        else:
            del mdb.models['Model-A'].materials['interface'].plastic
        CohEelem = mesh.ElemType(elemCode=COH3D8, elemLibrary=STANDARD, elemDeletion=OFF, viscosity=0.0001)
        p.setElementType(regions=p.sets['Interfaces'], elemTypes=(CohEelem,))
    if ConDmPlast:
        del mod.materials['resin'].concreteDamagedPlasticity
    else:
        del mod.materials['resin'].plastic
    #Create step Linear step
    mod.StaticStep(name=stepName, previous='Initial')
    #Request outputs
    mod.fieldOutputRequests['F-Output-1'].setValues(variables=('S', 'EVOL','U'))
    #Run the simulations to create stiffnessmatrix
    print '\nComputing stresses for normalized unit strains'
    for i in range(0,6):#   arg:   +   ,len(id)+1
        if not error:
            #Laste inn toyningscase
            exx, eyy, ezz, exy, exz, eyz = id[i]*0.01
            #Strainsene var mulighens litt store.
            mod.DisplacementBC(name='BCX', createStepName=stepName,
                               region=a.sets['RPX'], u1=exx, u2=exy, u3=exz, ur1=UNSET, ur2=UNSET, ur3=UNSET,
                               amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)

            mod.DisplacementBC(name='BCY', createStepName=stepName,
                               region=a.sets['RPY'], u1=exy, u2=eyy, u3=eyz, ur1=UNSET, ur2=UNSET, ur3=UNSET,
                               amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)

            mod.DisplacementBC(name='BCZ', createStepName=stepName,
                               region=a.sets['RPZ'], u1=exz, u2=eyz, u3=ezz, ur1=UNSET, ur2=UNSET, ur3=UNSET,
                               amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)
            print Enhetstoyinger[i][0]
            run_Job(Enhetstoyinger[i][0],modelName)

            del exx, eyy, ezz, exy, exz, eyz

#  STIFFNESS  MATRIX
create_Linearunitstrainslastcases()     # Unit strain cases. Set boundary condition and create job.


