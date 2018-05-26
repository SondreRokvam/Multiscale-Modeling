if Singlepin:
    region = mod.rootAssembly.sets['NL1']
    mod.PinnedBC(name='Laas-3', createStepName='Initial',
                 region=region, localCsys=None)
if tripplepin and Singlepin:
    region = mod.rootAssembly.sets['NL2']
    mod.DisplacementBC(name='Laas-2', createStepName='Initial',
                       region=region, u1=SET, u2=UNSET, u3=SET, ur1=UNSET, ur2=UNSET, ur3=UNSET,
                       amplitude=UNSET, distributionType=UNIFORM, fieldName='',
                       localCsys=None)
    region = mod.rootAssembly.sets['NL3']
    mod.DisplacementBC(name='Laas-1', createStepName='Initial',
                       region=region, u1=SET, u2=UNSET, u3=UNSET, ur1=UNSET, ur2=UNSET, ur3=UNSET,
                       amplitude=UNSET, distributionType=UNIFORM, fieldName='',
                       localCsys=None)