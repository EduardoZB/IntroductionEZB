# EUMETSAT ELT pipeline

The files with ".nat" extension are the native file format of the Meteosat Geostationary satellites. In order to obtain the newest Meteosat images, I found a script by Mr. [Darius A. Görgen](https://www.dariusgoergen.com/contents/blog/2020-06-14-nat2tif/index.html) and tweaked it to automate the process from extracion to transformation.

# Dependencies
This script requires **numpy, osgeo (GDAL), satpy and pyresample** libraries to function. When using Ubuntu 20.04LTS, the GDAL library can be tricky to install correctly, even when using virtual environment tools. Luckily, GitHub user [nvogtvincent](https://github.com/nvogtvincent) provided an [answer](https://github.com/ContinuumIO/anaconda-issues/issues/10351#issuecomment-976661610) that did it for me.

# Recipe format
The script will transform the data following the parameter specifications written in the eumetsat_recipe.txt file. The current version script will fail if the parameters do not follow some coherence guidelines:
* Color parameter will only accept **RGB** or **mono** as inputs. If **RGB** is specified, the script will ignore all pyresample and OpenCV parameters (calibration, dtype, radius, epsilon, nodata, out_type, brightness and contrast) and can take composite datasets, but will only show satpy resampled areas.
* Calibration admits **radiance** or **reflectance** options.
* Area definition uses satpy, and only works with composite processing at the moment. Available areas are found in satpy's 'areas.yaml' file.
* Dataset can be any of the available for the color chosen. For **mono** it takes the specific wavelenght name and for **RGB** it can take any of the composite options. Available options can be checked with satpy's Scene from a Python shell:
```
  from satpy import Scene
  file = 'path/to/your/file.nat'
  scn = Scene(filenames = {'seviri_l1b_native': [file]})
  scn.all_dataset_names(reader_name='seviri_l1b_native',composites=True)
```
* Reader chooses how to read the file. For all the MSG data, the **seviri_l1b_native** reader is the only one used in the tests.
* Label will only affect the output name but not the file.
* Dtype, Radius, Epsilon and Nodata are used in the pyresample resampling module. It works best fixing the values to 'float32', '16000', '.5' and '-3.4E+38' respectively. More info in Mr. Görgen's website.
* Out Type specifies the image processing library used in the image creation, as long as it is monochromatic. It can take **tif**, **cv2** or **plt** for 'GTiff', 'OpenCV' or 'matplotlib' respectively.
* Brightness and Contrast are used by OpenCV to modify said parameters during its processing.
* Start Time and End Time set the time range for extracting and processing data. If the Start Time is set to **Recent**, the script will automatically get the latest images in a 20-minute range.

# Output
Here I used ffmpeg to create a video for the images obtained on February 9th, from 10 to 16 UTC.

[Video](0902RGBvideo.mp4)
