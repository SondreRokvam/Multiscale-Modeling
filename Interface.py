for ie in range(0, len(xydata)):  # Tegne inn fiber aa partionere
    x = xydata[ie][0]
    y = xydata[ie][1]
    rcos45 = r * cos(45.0 * pi / 180.0)
    p.DatumCsysByThreePoints(name=('Fiber datum ' + str(ie)), coordSysType=CYLINDRICAL,
                             origin=(x, y, 0.0), point1=(x + 1.0, y, 0.0), point2=(x + 1.0, y + 1.0, 0.0))