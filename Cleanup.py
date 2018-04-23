# Rydde for neste iterasjon
import os
RunningCleanup=1
workpath = 'C:/temp/'
if RunningCleanup:
    filelist = [f for f in os.listdir(workpath) if not f.endswith('.bat')]  # if not f.endswith('.inp')]
    for f in filelist:
        try:
            os.remove(os.path.join(workpath, f))
        except:
            pass