p = mod.parts[meshPartName]

mod.Material(name='resin')
mod.materials['resin'].Elastic(table=((3500.0, 0.33),))
mod.materials['resin'].Density(table=((1.2e-09,),))
mod.HomogeneousSolidSection(name='SSmatrix', material='resin', thickness=None)  # Assign Properties and sections
if not nf == 0:
    mod.Material(name='glass')
    mod.materials['glass'].Elastic(table=((90000.0, 0.22),))
    mod.materials['glass'].Density(table=((2.55e-09,),))
    if Interface:
        mod.Material(name='interface')
        mod.materials['interface'].Elastic(type=TRACTION, table=((100.0, 100.0, 100.0),))
        mod.materials['interface'].Density(table=((1.2e-09,),))
        p = mdb.models['Model-A'].parts['Part-1-mesh-1']
        for Fdats in range(0, len(xydata)):
            datId = p.features['Fiber datum ' + str(Fdats)].id
            fibCsys = p.datums[datId]
            region = p.sets['FiberInt' + str(Fdats)]
            mdb.models['Model-A'].parts['Part-1-mesh-1'].MaterialOrientation(region=region,
                                                                             orientationType=SYSTEM, axis=AXIS_3,
                                                                             localCsys=fibCsys,
                                                                             fieldName='',
                                                                             additionalRotationType=ROTATION_NONE,
                                                                             angle=0.0,
                                                                             additionalRotationField='',
                                                                             stackDirection=STACK_3)

        if nonLinearDeformation:
            mod.materials['interface'].QuadsDamageInitiation(table=((0.042, 0.063, 0.063),))
            mod.materials['interface'].quadsDamageInitiation.DamageEvolution(type=ENERGY, mixedModeBehavior=BK,
                                                                             power=1.2,
                                                                             table=((0.0028, 0.0078, 0.0078),))
        mdb.models['Model-A'].CohesiveSection(name='SSbond', material='interface', response=TRACTION_SEPARATION,
                                              initialThicknessType=SPECIFY, initialThickness=rinterface * rmean,
                                              outOfPlaneThickness=None)
        # initialThicknessType=GEOMETRY,outOfPlaneThickness=None)
        region = p.sets['Interfaces']
        p.SectionAssignment(region=region, sectionName='SSbond', offset=0.0,
                            offsetType=MIDDLE_SURFACE, offsetField='',
                            thicknessAssignment=FROM_SECTION)
    if nonLinearDeformation:
        mod.materials['resin'].ConcreteDamagedPlasticity(table=((0.1, 0.1, 1.16, 0.89, 0.0001),))
        mod.materials['resin'].concreteDamagedPlasticity.ConcreteCompressionHardening(
            table=((0.102, 0.0), (0.104, 0.05), (0.106, 0.32), (0.00102, 0.55)))
        mod.materials['resin'].concreteDamagedPlasticity.ConcreteTensionStiffening(table=((0.6, 0.09),), type=GFI)
        mod.materials['resin'].concreteDamagedPlasticity.ConcreteTensionDamage(table=((0.0, 0.0), (0.9, 1.487)),
                                                                               type=DISPLACEMENT)
        mod.materials['resin'].concreteDamagedPlasticity.ConcreteCompressionDamage(
            table=((0.0, 0.0), (0.0, 0.32), (0.9, 0.55)))
    mod.HomogeneousSolidSection(name='SSfibers', material='glass', thickness=None)
    region = p.sets['Fibers']
    p.SectionAssignment(region=region, sectionName='SSfibers', offset=0.0,
                        offsetType=MIDDLE_SURFACE, offsetField='',
                        thicknessAssignment=FROM_SECTION)
    region = p.sets['Matrix']
    p.SectionAssignment(region=region, sectionName='SSmatrix', offset=0.0,
                        offsetType=MIDDLE_SURFACE, offsetField='',
                        thicknessAssignment=FROM_SECTION)
else:
    if nonLinearDeformation:
        mod.materials['resin'].ConcreteDamagedPlasticity(table=((0.1, 0.1, 1.16, 0.89, 0.0001),))
        mod.materials['resin'].concreteDamagedPlasticity.ConcreteCompressionHardening(
            table=((0.102, 0.0), (0.104, 0.05), (0.106, 0.32), (0.00102, 0.55)))
        mod.materials['resin'].concreteDamagedPlasticity.ConcreteTensionStiffening(table=((0.6, 0.09),), type=GFI)
        mod.materials['resin'].concreteDamagedPlasticity.ConcreteTensionDamage(table=((0.0, 0.0), (0.9, 1.487)),
                                                                               type=DISPLACEMENT)
        mod.materials['resin'].concreteDamagedPlasticity.ConcreteCompressionDamage(
            table=((0.0, 0.0), (0.0, 0.32), (0.9, 0.55)))
    region = p.sets['Matrix']
    p.SectionAssignment(region=region, sectionName='SSmatrix', offset=0.0,
                        offsetType=MIDDLE_SURFACE, offsetField='',
                        thicknessAssignment=FROM_SECTION)
