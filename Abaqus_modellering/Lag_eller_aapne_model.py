""" Abaqus RVE model """
try:
    execfile(Modellering + 'Model.py')
    t = (time.time() - start_time)
    print    '\tModelleringstid=', np.round(t, 3)
except:
    print 'Feil i RVE modellering - Lag_or_Prep'
    error = 1
# Prep Stiffness tests
if not error:
    # Strain test
    Enhetstoyinger = [''] * 6  # 6 Enhetstoyinger - Exx, Eyy, Ezz, Exy, Exz, Eyz
    for g in range(0, 6):
        if not noFibertest:
            Enhetstoyinger[g] = [Retning[g] + str(int(ParameterSweep * SweepPrime)) + '_' + str(Q)]
        else:
            Enhetstoyinger[g] = [Retning[g] + 'noFiber']

    # Kjore Linear analyse
    if not Createmodel or openModel:
        try:
            openMdb(pathName=RVEmodellpath)
            mod = mdb.models[modelName]
        except:
            print 'Cae-fil ikke funnet'
            error = 1