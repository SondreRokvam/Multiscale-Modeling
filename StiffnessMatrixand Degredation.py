e1 = a.instances['PART-1-MESH-1-1'].elements
region = regionToolset.Region(elements=e1)
mdb.models['Model-A'].Stress(name='FraNonLinear', distributionType=FROM_FILE,
    fileName='C:/Temp/TensionX_NothingElse.odb', step=-1, increment=-1)