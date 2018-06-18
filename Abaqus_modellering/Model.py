Mdb()  # reset Abaqus
model = mdb.Model(name=modelName, modelType=STANDARD_EXPLICIT)  # Lage model
mod = mdb.models[modelName]  # Lage snarvei
if Createmodel:
    xydata = None  # Fiber kordinater og radiuser
    if not noFiber:
        execfile(Modellering + 'GenerereFiberPopTilFil.py')  # create a random population
    CreateNewRVEModel()
    if Savemodel:
        mdb.saveAs(pathName=RVEmodellpath)
# Prov aa aapne tidligere modell
if openModel:
    Mdb()
    openMdb(pathName=RVEmodellpath)
    mod = mdb.models[modelName]

t = (time.time() - start_time)
print('t etter lagd modell=', t)