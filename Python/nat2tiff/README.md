# .nat To .tiff converter

The files with ".nat" extension are the native file format of the Meteosat Geostationary satellites. In order to obtain the newest Meteosat images, I found a script by Mr. [Darius A. Görgen](https://www.dariusgoergen.com/contents/blog/2020-06-14-nat2tif/index.html) and tweaked it to automate the process from selecting the .nat file to all the individual bandwidth outputs.

# Dependencies
This script requires **numpy, osgeo (GDAL), satpy and pyresample** libraries to function. When using Ubuntu 20.04LTS, the GDAL library can be tricky to install correctly, even when using virtual environment tools. Luckily, GitHub user [nvogtvincent](https://github.com/nvogtvincent) provided an [answer](https://github.com/ContinuumIO/anaconda-issues/issues/10351#issuecomment-976661610) that did it for me.

# Output
For monday February 5th at 12:41 UTC

High Resolution Visual
![12_41NA_HRV](12_41NA_HRV.png "HRV")

Infrared 8.7 nanometers
![12_41IR_087](12_41IR_087.png "IR")

Infrared 7.3 nanometers
![12_41WV_073](12_41WV_073.png "WV")
