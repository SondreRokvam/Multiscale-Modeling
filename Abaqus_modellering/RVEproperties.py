"""Filen er laget for aa bli kjort av microscale scriptet"""
# Lage materialer, material sections og assigne materialer til sections for Matrix, Fiber og Interface
"""Material Constants for Resin, Fiber and Interfaze/Bond/Sizing"""
ResCon2 = {'E,v':(3,0.35), 'Den':1.2e-06,
          'CDP':(0.1, 0.1, 1.16, 0.89, 0.0001),
          'cdpCCH':((0.102, 0.0), (0.104, 0.05), (0.106, 0.32), (0.00102, 0.55)),
          'cdpCTS':(0.6, 0.09),
          'cdpCTD':((0.0, 0.0), (0.9, 1.487)),
          'cdpCCD':((0.0, 0.0), (0.0, 0.32), (0.9, 0.55))}
ResCon = {'E,v':(3.0,0.35), 'Den':1.2e-06,
          'CDP':(0.1, 0.1, 1.16, 0.89, 0.0001),
          'cdpCCH':((0.102, 0.0), (0.104, 0.05), (0.106, 0.32), (0.00102, 0.55)),
          'cdpCTS':(0.6, 0.09),
          'cdpCTD':((0.0, 0.0), (0.9, 1.487)),
          'cdpCCD':((0.0, 0.0), (0.0, 0.32), (0.9, 0.55))}

FibCon = {'E,v':(90,0.22), 'Den':2.55e-06}

IntCon = {'Trac':(0.060, 0.060, 0.060), 'Den':1.2e-06,
          'QDI':(0.042, 0.063, 0.063),
          'qdiDEpower':1.2,   'qdiDE':(0.0028, 0.0078, 0.0078), }

def SetMaterialConstants(ResCon,FibCon,IntCon):                     #Assign Properties
    mod.Material(name='resin')
    res=mod.materials['resin']
    res.Elastic(table=(ResCon['E,v'],))
    if MaterialDens:
        res.Density(table=((ResCon['Den'],),))
    if nonLinearAnalysis:
        res.ConcreteDamagedPlasticity(table=(ResCon['CDP'],))
        RCDP = res.concreteDamagedPlasticity
        RCDP.ConcreteCompressionHardening(table=ResCon['cdpCCH'])
        RCDP.ConcreteCompressionDamage(table=ResCon['cdpCCD'])
        RCDP.ConcreteTensionStiffening(table=(ResCon['cdpCTS'],), type=GFI)
        RCDP.ConcreteTensionDamage(table=ResCon['cdpCTD'], type=DISPLACEMENT)

    if not nf == 0:
        mod.Material(name='glass')
        mod.materials['glass'].Elastic(table=(FibCon['E,v'],))
        if MaterialDens:
            mod.materials['glass'].Density(table=((FibCon['Den'],),))
        if Interface:
            mod.Material(name='interface')
            intF= mod.materials['interface']
            intF.Elastic(type=TRACTION, table=(IntCon['Trac'],))
            if MaterialDens:
                intF.Density(table=((IntCon['Den'],),))
            if nonLinearAnalysis:
                intF.QuadsDamageInitiation(table=(IntCon['QDI'],))
                intF.quadsDamageInitiation.DamageEvolution(type=ENERGY, mixedModeBehavior=BK,
                                                       power=IntCon['qdiDEpower'], table=(IntCon['qdiDE'],))
    if not ConDmPlast:
        del mdb.models['Model-A'].materials['interface'].quadsDamageInitiation
        mdb.models['Model-A'].materials['interface'].Plastic(table=((0.060, 0.0), (0.061,
        0.015)))
        del mdb.models['Model-A'].materials['resin'].concreteDamagedPlasticity
        mdb.models['Model-A'].materials['resin'].Plastic(table=((0.060, 0.0), (0.061,
        0.015)))

def SectionsAndOrientations():                                  # Create and assign sections to materials
    p = mdb.models['Model-A'].parts['Part-1-mesh-1']
    mod.HomogeneousSolidSection(name='SSmatrix', material='resin', thickness=None)          # Create Matrix sections
    region = p.sets['Matrix']
    p.MaterialOrientation(region=region,orientationType=GLOBAL, axis=AXIS_1,additionalRotationType=ROTATION_NONE,
                          localCsys=None, fieldName='',stackDirection=STACK_3)
    p.SectionAssignment(region=region, sectionName='SSmatrix', offset=0.0,                  # Assign Matrix sections
                        offsetType=MIDDLE_SURFACE, offsetField='',
                        thicknessAssignment=FROM_SECTION)

    if not nf == 0:
        mod.HomogeneousSolidSection(name='SSfibers', material='glass', thickness=None)         # Create Fibersections
        region = p.sets['Fibers']
        p.MaterialOrientation(region=region, orientationType=GLOBAL, axis=AXIS_1, additionalRotationType=ROTATION_NONE,
                              localCsys=None, fieldName='', stackDirection=STACK_3)
        p.SectionAssignment(region=region, sectionName='SSfibers', offset=0.0,
                            offsetType=MIDDLE_SURFACE, offsetField='',
                            thicknessAssignment=FROM_SECTION)
        if Interface:
            #if nonLinearAnalysis:
            """# Lage fiber datums for material orientering av Interface UNCLEAR IF NEEDED
                for ie in range(0, len(xydata)):
                    x = xydata[ie][0]
                    y = xydata[ie][1]
                    p.DatumCsysByThreePoints(name=('Fiber datum ' + str(ie)), coordSysType=CYLINDRICAL,
                                                 origin=(x, y, 0.0), point1=(x + 1.0, y, 0.0), point2=(x + 1.0, y + 1.0, 0.0))
                # Materialorientering paa coheesive materiale UNCLEAR IF NEEDED
                for Fdats in range(0, len(xydata)):
                    datId = p.features['Fiber datum ' + str(Fdats)].id
                    fibCsys = p.datums[datId]
                    region = p.sets['FiberInt' + str(Fdats)]
                    p.MaterialOrientation(region=region, orientationType=SYSTEM, axis=AXIS_3, localCsys=fibCsys,fieldName='',
                                          additionalRotationType=ROTATION_NONE, angle=0.0, additionalRotationField='',
                                          stackDirection=STACK_ORIENTATION)
                    
                                    # additionalRotationType = ROTATION_ANGLE, angle=-90.0, additionalRotationField='',
                                    # additionalRotationType = ROTATION_NONE,  angle = 0.0, additionalRotationField='',
            """
            mod.CohesiveSection(name='SSbond', material='interface', response=TRACTION_SEPARATION,
                                    initialThicknessType=GEOMETRY, outOfPlaneThickness=None)
                # initialThicknessType=SPECIFY, initialThickness = 0.01, outOfPlaneThickness = None)
                # initialThicknessType=GEOMETRY,outOfPlaneThickness=None)
            #else:
            #   mod.HomogeneousSolidSection(name='SSbond', material='interface', thickness=None)
            region = p.sets['Interfaces']
            p.SectionAssignment(region=region, sectionName='SSbond', offset=0.0,offsetType=MIDDLE_SURFACE,
                                offsetField='',thicknessAssignment=FROM_SECTION)

SetMaterialConstants(ResCon,FibCon,IntCon)
SectionsAndOrientations()

print 'Material properties assigned to element sets in model'