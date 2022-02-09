from napari.qt.threading import thread_worker
from qtpy.QtWidgets import QPushButton
from glob import glob
import napari, tifffile, time
import numpy as np

directory = 'MIPs'
channels = 'CamA_ch0,CamB_ch0'
colorMaps = 'blue,green'

colorList = colorMaps.split(',')
channelList = channels.split(',')

oldFiles = []
def getFiles():
    newFiles = []
    for file in glob(directory+'/*tif'):
        if file not in oldFiles:
            newFiles.append(file)
            oldFiles.append(file)
    newFiles.sort(key=lambda fname: int(fname.split('_')[3]))
    return newFiles

imArrayList = []
def addImages(fileList):   
    if not fileList:
        return  
    channel = fileList[1].split('_')[4] + '_' + fileList[1].split('_')[5] 
    colormap = colorList[channelList.index(channel)]
    tifList = []
    for image in fileList:       
        tifList.append(tifffile.imread(image))
    print(channel)
    timelapse = np.asarray(tifList)
    viewer.add_image(timelapse, name=channel, colormap=colormap)

@thread_worker(connect={'yielded': addImages})
def runCycle():
    while True:
        newFiles = getFiles()
        for channel in channelList:
            fileList = []
            for file in newFiles:
                if channel in file:
                    fileList.append(file)
            yield fileList
        time.sleep(10)


viewer = napari.Viewer()

# add a button to the viewew that, when clicked, stops the worker
button = QPushButton("STOP!")
button.clicked.connect(runCycle().quit)
runCycle().finished.connect(button.clicked.disconnect)
viewer.window.add_dock_widget(button)

runCycle()

napari.run()



