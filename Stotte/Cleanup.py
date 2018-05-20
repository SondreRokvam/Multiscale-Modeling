# Rydde en mappe
import os
workpath = 'C:/temp/'
filelist = [f for f in os.listdir(workpath) if not f.endswith('.bat')]  # if not f.endswith('.inp')]
for f in filelist:
    try:
        os.remove(os.path.join(workpath, f))
    except:
        pass