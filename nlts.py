from napari.qt.threading import thread_worker
from glob import glob
import napari, tifffile, time, argparse, random
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('directory', type=str, default='MIPs')
parser.add_argument('channels', type=str, default='CamA_ch0,CamB_ch0')
parser.add_argument('--opacity', type=float, nargs='+', default=[1.0])          
parser.add_argument('--contrast_limits', type=float, nargs='+', default=[None])   
parser.add_argument('--gamma', type=float, nargs='+', default=[1.0])             
parser.add_argument('--colormaps', type=str, default='blue,green,red,magenta,yellow,orange,cyan')       
parser.add_argument('--blending', type=str, default='additive')       
parser.add_argument('--interpolation', type=str, default='nearest')   
parser.add_argument('--auto_contrast', action='store_true')
parser.add_argument('--toggle_grid_mode', action='store_true')                                        
parser.add_argument('--fetch_interval', type=int, default=10)                                           
parser.add_argument('--layer_buffer', type=int, default=2)        
args = parser.parse_args()                                    


viewer = napari.Viewer()
channel_list = args.channels.split(',')
def add_images(file_list):   
    if not file_list:
        return  

    channel = file_list[1].split('_')[4] + '_' + file_list[1].split('_')[5] 
    index = channel_list.index(channel)

    tif_list = []
    for image in file_list:       
        tif_list.append(tifffile.imread(image, name=channel))
    timelapse = np.asarray(tif_list)

    if len(viewer.layers) >= len(channel_list):
        layer = viewer.layers[index]   
        layer.data = np.concatenate((layer.data, timelapse), axis=0)
    else:
        contrast_limits = args.contrast_limits[2*index % len(args.contrast_limits):
                                               2*index % len(args.contrast_limits)+2]
        if contrast_limits[0] is None:
            contrast_limits = None
        viewer.add_image(
            timelapse, name=channel, opacity=args.opacity[index % len(args.opacity)], 
            contrast_limits=contrast_limits, gamma=args.gamma[index % len(args.gamma)], 
            colormap=args.colormaps.split(',')[index], blending=args.blending, 
            interpolation=args.interpolation)

@thread_worker(connect={'yielded': add_images})
def fetch_files():
    old_files = []
    while True:
        new_files = []
        for file in sorted(glob(args.directory+'/*tif'))[: -args.layer_buffer or None]:
            if file not in old_files:
                new_files.append(file)
                old_files.append(file)

        for channel in channel_list:
            file_list = []
            for file in new_files:
                if channel in file:
                    file_list.append(file)
            yield file_list
        time.sleep(args.fetch_interval)

fetch_files()
napari.run()
