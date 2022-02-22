### Multichannel live timelapse Script
This script requires [Napari](https://napari.org/tutorials/fundamentals/installation:// "Napari") to be installed.

To launch the script open Napari conda enviroment and navigate to directory where the script is located.
The script can be called using `python nlts.py <directory location> <channel1,channel2,...> <optional arguments>`

#### Arguments:
There are several optional image setting that can be passed into the script before launch. When passing in an argument that requires multiple values seperate them by spaces (e.g `--contrast_limits 0.0 100.0 0.0 100.0`) in the case of numerical inputs, or commas (e.g `--colormaps blue,green`) in the case of strings.
- opacity: (0.0-1.0) The opacity of the image. One for each channel.
- contrast limits: (No limits) The upper and lower contrast limits of the image. Upper and lower bounds for each image.
- gamma: (0.0-2.0) The gamma correct of the image. One for each channel.
- colormaps: The desired colormap for each channel.
- blending: Blending option for each channel. Default is additive.
- interpolation: Interpolation option for each channel. Default is nearest
- fetch interval: Duration (seconds) to wait between searching directory for new images. Default is 2 minutes
- layer buffer: Can prevent the files from being loaded into Napari in the wrong order in some rare cases, so we leave out the last N layers to prevent this. (This is not working as intended currently.
