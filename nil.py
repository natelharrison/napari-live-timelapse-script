from napari.qt.threading import thread_worker
from qtpy.QtWidgets import QPushButton
from glob import glob
import napari, tifffile, time
import numpy as np

directory = 'MIPs'
channels = 'CamA_ch0,CamB_ch0'
colorMaps = 'blue,green'

color_list = colorMaps.split(',')
channel_list = channels.split(',')

old_files = []
def get_files():
    new_files = []
    for file in glob(directory+'/*tif'):
        if file not in old_files:
            new_files.append(file)
            old_files.append(file)
    new_files.sort(key=lambda fname: int(fname.split('_')[3]))
    return new_files

im_array_list = []
def add_images(file_list):   
    if not file_list:
        return  
    channel = file_list[1].split('_')[4] + '_' + file_list[1].split('_')[5] 
    colormap = color_list[channel_list.index(channel)]
    tif_list = []
    for image in file_list:       
        tif_list.append(tifffile.imread(image, name=channel))
    print(channel)
    timelapse = np.asarray(tif_list)
    viewer.add_image(timelapse, name=channel, colormap=colormap)

@thread_worker(connect={'yielded': add_images})
def run_cycle():
    while True:
        new_files = get_files()
        for channel in channel_list:
            file_list = []
            for file in new_files:
                if channel in file:
                    file_list.append(file)
            yield file_list
        time.sleep(10)


viewer = napari.Viewer()


# add a button to the viewew that, when clicked, stops the worker
button = QPushButton("STOP!")
button.clicked.connect(run_cycle().quit)
run_cycle().finished.connect(button.clicked.disconnect)
viewer.window.add_dock_widget(button)

run_cycle()

napari.run()


