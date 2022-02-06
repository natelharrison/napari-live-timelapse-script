from napari.qt.threading import thread_worker
from glob import glob
import napari, tifffile, time

directory = 'MIPs'
channel = 'CamA_ch0,CamB_ch0,CamC_ch0'

#Returns new files in a folder
newFiles = []
oldFiles = []
def getFiles():
    newFiles.clear()
    for file in glob(directory+'/*tif'):
        if file not in oldFiles:
            newFiles.append(file)
            oldFiles.append(file)
    newFiles.sort(key=lambda fname: int(fname.split('_')[3]))
    return newFiles

#Returns list of all new files in tiff format
def tiffImage(): 
    newList = getFiles()
    im = []
    for tif in newList:
        print(tifffile.imread(tif))
        im.append(tifffile.imread(tif))
    return im

@thread_worker
def runCycle():
    while True:
        for file in tiffImage():
            yield file 
        time.sleep(10)


viewer = napari.Viewer()
worker = runCycle()
worker.yielded.connect(viewer.add_image)

worker.start()

napari.run()


