from napari.qt.threading import thread_worker
from glob import glob
import napari, tifffile, time
import numpy as np

directory = 'MIPs'
channels = 'CamA_ch0,CamB_ch0'
colormaps = 'blue,green'

color_list = colormaps.split(',')
channel_list = channels.split(',')

viewer = napari.Viewer()

def add_images(file_list):   
    if not file_list:
        return  

    channel = file_list[1].split('_')[4] + '_' + file_list[1].split('_')[5] 
    index = channel_list.index(channel)
    colormap = color_list[index]
    
    tif_list = []
    for image in file_list:       
        tif_list.append(tifffile.imread(image, name=channel))
    timelapse = np.asarray(tif_list)
    
    if len(viewer.layers) >= len(color_list):
        layer = viewer.layers[index]   
        layer.data = np.concatenate((layer.data, timelapse), axis=0)
    else:
        viewer.add_image(timelapse, name=channel, colormap=colormap)

@thread_worker(connect={'yielded': add_images})
def run_cycle():
    old_files = []
    while True:

        new_files = []
        for file in glob(directory+'/*tif'):
            if file not in old_files:
                new_files.append(file)
                old_files.append(file)
        new_files.sort(key=lambda fname: int(fname.split('_')[3]))

        for channel in channel_list:
            file_list = []
            for file in new_files:
                if channel in file:
                    file_list.append(file)
            yield file_list
        time.sleep(10)

run_cycle()

napari.run()

