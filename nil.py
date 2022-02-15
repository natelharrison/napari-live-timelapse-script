from napari.qt.threading import thread_worker
from glob import glob
import napari, tifffile, time
import numpy as np

parser = argparse.ArgumentParser()

#Required args
parser.add_argument('directory', type=str, default='MIPs')
parser.add_argument('channels', type=str, default='CamA_ch0,CamB_ch0')

channel_list = args.channels.split(',')

#Optional args
parser.add_argument('--opacity', type=float, nargs='+', defualt=[1.0 for i in channel_list])            #1.0 1.0
parser.add_argument('--contrast_limits', type=float, nargs='+', default=[None for i in channel_list])   #0.0 100.0 0.0 100.0
parser.add_argument('--gammma', type=float, nargs='+', default=[1.0 for i in channel_list])             #1.0 1.0 
parser.add_argument('--colormaps', type=str, default='blue,green,red,magenta,yellow,orange,cyan')       #'blue,red,green'
parser.add_argument('--blending', type=str, default=''.join(['addative,' for i in channel_list]))       #'addative,addative'
parser.add_argument('--interpolation', type=str, default=''.join(['nearest,' for i in channel_list]))    #'nearest,nearest'

parser.add_argument('--auto_contrast', action='store_true')
parser.add_argument('--toggle_grid_mode', action='store_true')                                        

parser.add_argument('--fetch_interval', type=int, default=10)                                           #120
parser.add_argument('--layer_buffer', type=int, default=2)                                              #2

color_list = colormaps.split(',')

viewer = napari.Viewer()

def add_images(file_list):   
    if not file_list:
        return  

    channel = file_list[1].split('_')[4] + '_' + file_list[1].split('_')[5] 
    index = channel_list.index(channel)

    tif_list = []
    for image in file_list:       
        tif_list.append(tifffile.imread(image, name=channel))
    timelapse = np.asarray(tif_list)
    
    if len(viewer.layers) >= len(color_list):
        layer = viewer.layers[index]   
        layer.data = np.concatenate((layer.data, timelapse), axis=0)
    else:
        viewer.add_image(
            timelapse, name=channel, opacity=args.opacity[index], 
            contrast_limits=args.contrast_limits[index], gamma=args.gamma[index],
            colormap=args.colormaps.split(',')[index], blending=args.blending.split(',')[index],
            interpolation=args.interpolation.split(',')[index] )

@thread_worker(connect={'yielded': add_images})
def fetch_files():
    old_files = []
    while True:

        new_files = []
        for file in glob(directory+'/*tif')[: -args.layer_buffer or None]:
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
        time.sleep(args.fetch_interval)

fetch_files()

napari.run()

