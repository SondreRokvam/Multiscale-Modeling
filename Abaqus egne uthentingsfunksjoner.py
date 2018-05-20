xyPlot.xyDataListFromField(odb=od, outputPosition=ELEMENT_CENTROID,
                           variable=(('S',ELEMENT_CENTROID, ( (COMPONENT, 'S11' ),(COMPONENT, 'S22' ), (COMPONENT, 'S33' ),(COMPONENT, 'S12' ), (COMPONENT, 'S13' ),(COMPONENT, 'S23' ),   )), elementSets=('PART-1-MESH-1-1.MATRIX','PART-1-MESH-1-1.FIBERS',))

xyList = xyPlot.xyDataListFromField(odb=odb, outputPosition=ELEMENT_CENTROID,
        variable=(('S', INTEGRATION_POINT, ((COMPONENT, 'S33'), )), ),
        elementSets=('PART-1-MESH-1-1.INTERFACES', 'PART-1-MESH-1-1.MATRIX', ))

xyList = xyPlot.xyDataListFromField(odb=od, outputPosition=ELEMENT_CENTROID,
        variable=(('S', INTEGRATION_POINT, ((COMPONENT, 'S11'), (COMPONENT,
        'S22'), (COMPONENT, 'S33'), )), ), elementSets=('PART-1-MESH-1-1.FIBERS',
        'PART-1-MESH-1-1.INTERFACES', 'PART-1-MESH-1-1.MATRIX', ))


xyList = xyPlot.xyDataListFromField(odb=od, outputPosition=ELEMENT_CENTROID,
        variable=(('S', INTEGRATION_POINT, ((COMPONENT, 'S11'), (COMPONENT,
        'S22'), (COMPONENT, 'S33'), (COMPONENT, 'S12'), (COMPONENT, 'S13'), (
        COMPONENT, 'S23'), )), ), elementSets=('PART-1-MESH-1-1.FIBERS', 'PART-1-MESH-1-1.MATRIX', ))