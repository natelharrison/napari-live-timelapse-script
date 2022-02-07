from napari.qt.threading import thread_worker
from glob import glob
import napari, tifffile, time

directory = 'MIPs'
channels = 'CamA_ch0,CamB_ch0'
colorMaps = 'blue,green'

colorList = colorMaps.split(',')
channelList = channels.split(',')

#Returns new files in a folder

oldFiles = []
def getFiles():
    newFiles = []
    for file in glob(directory+'/*tif'):
        if file not in oldFiles:
            newFiles.append(file)
            oldFiles.append(file)
    newFiles.sort(key=lambda fname: int(fname.split('_')[3]))
    return newFiles


def addImage(image):
    for channel in channelList:
        if channel in image:
            imName = lambda fname: int(fname.split('_')[2:3])
            im = tifffile.imread(image)
            viewer.add_image(im, name=imName)


#Returns list of all new files in tiff format
def tiffImage(): 
    newList = getFiles()
    im = []
    for tif in newList:
        print(tifffile.imread(tif))
        im.append(tifffile.imread(tif))
    return im

@thread_worker(connect={'yielded': addImage})
def runCycle():
    while True:
        for file in getFiles():
            yield file
        time.sleep(10)


viewer = napari.Viewer()

runCycle()

napari.run()

