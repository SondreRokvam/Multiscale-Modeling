Mdb()  # reset Abaqus
mod = mdb.models[modelName]  # Lage snarvei
if Createmodel:
    xydata = None  # Fiber kordinater og radiuser
    try:
        if not noFiber:
            execfile(Modellering + 'GenerereFiberPopTilFil.py')  # create a random population
    except:
        print 'Feil i generering av fiberpopulasjon - Model'
        error = 1
    if not error:
        try:
            CreateNewRVEModel()
        except:
            print 'Feil i RVEmodellering - Model'
            error=1
    if not error:
        if Savemodel:
            try:
                mdb.saveAs(pathName=RVEmodellpath)
            except:
                print 'Feil i lagring av RVEmodell - Model'
                error = 1
# Prov aa aapne tidligere modell
if openModel:
    Mdb()
    openMdb(pathName=RVEmodellpath)
    mod = mdb.models[modelName]
