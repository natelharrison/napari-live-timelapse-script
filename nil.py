from napari.qt.threading import thread_worker
import tifffile, os, time
import napari

@thread_worker
def runCycle():

    #Returns new and previous files
    def getNewFiles(newPrevFiles = ([], [])):
        newPrevFiles[1].clear()
        for file in os.listdir('MIPs'):
            if file not in newPrevFiles[0]:
                newPrevFiles[0].append(file)
                newPrevFiles[1].append(file)
        return newPrevFiles    
    
    #Returns list of all new files in tiff format
    def tiffImage(): 
        tifList = []
        im = []
        for file in getNewFiles()[1]:
            tifList.append('MIPs/'+file)

        for tif in tifList:
            im.append(tifffile.imread(tif))
        return im

    #Yields files for connecter and sleeps for duration 
    while True:
        for file in tiffImage():
            yield file
        time.sleep(10)


viewer = napari.Viewer()
worker = runCycle()
worker.yielded.connect(viewer.add_image)
worker.start()

napari.run()
