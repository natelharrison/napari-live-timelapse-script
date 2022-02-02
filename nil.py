from napari.qt.threading import thread_worker
import napari, tifffile, os, time

@thread_worker
def runCycle():

    #Returns new files in a folder
    newFiles = []
    oldFiles = []
    def getFiles():
        newFiles.clear
        for file in os.listdir('MIPs'):
            if file not in oldFiles:
                newFiles.append(file)
                oldFiles.append(file)
        return newFiles  
    
    #Returns list of all new files in tiff format
    def tiffImage(): 
        tifList = []
        im = []
        for file in getFiles():
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
