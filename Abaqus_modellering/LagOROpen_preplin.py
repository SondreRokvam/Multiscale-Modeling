
execfile(Modellering + 'Model.py')

# Prep Stiffness tests
if not error:
    # Strain test
    Enhetstoyinger = [''] * 6  # 6 Enhetstoyinger - Exx, Eyy, Ezz, Exy, Exz, Eyz
    for g in range(0, 6):
        if not noFibertest:
            Enhetstoyinger[g] = [Retning[g] + str(int(ParameterSweep * scsc)) + '_' + str(Q)]
        else:
            Enhetstoyinger[g] = [Retning[g] + 'noFiber']

    # Kjore Linear analyse
    if not FoundStiff:
        if not Createmodel:
            try:
                openMdb(pathName=RVEmodellpath)
                mod = mdb.models['Model-A']
            except:
                print
                'Cae not found'
                error = 1
                pass