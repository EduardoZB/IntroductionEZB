
import numpy as np
from osgeo import gdal
from osgeo import osr
import os
import pyresample as pr
from satpy import Scene
import matplotlib.pyplot as plt
import tkinter.filedialog
import time

# open file dialog asking what .nat file to work with
file = tkinter.filedialog.askopenfilename()
# define reader
reader = "seviri_l1b_native"
# read the file
scn = Scene(filenames = {reader:[file]})
# extract data set names
dataset_names = scn.all_dataset_names()
# print available datasets
print('\n'.join(map(str, dataset_names)))
# extract file creation time
filetime = scn.end_time
# take the day 
nowday = filetime.strftime('%d%m')
### Select a specific area to display

# create some information on the reference system
area_id = "Spain"
description = "Geographical Coordinate System clipped on Spain"
proj_id = "Spain"
# specifing some parameters of the projection
proj_dict = {"proj": "longlat", "ellps": "WGS84", "datum": "WGS84"}
# calculate the width and height of the aoi in pixels
llx = -10 # lower left x coordinate in degrees
lly = 35 # lower left y coordinate in degrees
urx = 4 # upper right x coordinate in degrees
ury = 45 # upper right y coordinate in degrees
resolution = 0.005 # target resolution in degrees
# calculating the number of pixels
width = int((urx - llx) / resolution)
height = int((ury - lly) / resolution)
area_extent = (llx,lly,urx,ury)
# defining the area
area_def = pr.geometry.AreaDefinition(area_id, proj_id, description, proj_dict, width, height, area_extent)
print(area_def)



### Define the function that converts the .nat file to a series of .tif files containing the different dataset images

def nat2tif(file, calibration, area_def, dataset, reader, outdir, label, dtype, radius,
            epsilon, nodata, out_type):
    # open the file
    scn = Scene(filenames = {reader: [file]})
    # let us check that the specified data set is actually available
    scn_names = scn.all_dataset_names()
    # raise exception if dataset is not present in available names
    if dataset not in scn_names:
        raise Exception("Specified dataset is not available.")
    # we need to load the data, different calibration can be chosen
    scn.load([dataset], calibration=calibration)
    # let us extract the longitude and latitude data
    lons, lats = scn[dataset].area.get_lonlats()
    # now we can apply a swath definition for our output raster
    swath_def = pr.geometry.SwathDefinition(lons=lons, lats=lats)
    # and finally we also extract the data
    values = scn[dataset].values
    # we will now change the datatype of the arrays
    # depending on the present data this can be changed
    lons = lons.astype(dtype)
    lats = lats.astype(dtype)
    values = values.astype(dtype)
    # now we can already resample our data to the area of interest
    values = pr.kd_tree.resample_nearest(swath_def, values,
                                         area_def,
                                         radius_of_influence=radius, # in meters
                                         epsilon=epsilon,
                                         fill_value=False)
    # we are going to check if the outdir exists and create it if it doesnt
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    # let us join our filename based on the input file's basename           
    outname = os.path.join(outdir, os.path.basename(file)[:-4] + "_" + str(label) + ".tif")
    # now we define some metadata for our raster file
    cols = values.shape[1]
    rows = values.shape[0]
    pixelWidth = (area_def.area_extent[2] - area_def.area_extent[0])/ cols
    pixelHeight = (area_def.area_extent[1] - area_def.area_extent[3])/ rows
    originX = area_def.area_extent[0]
    originY = area_def.area_extent[3] 
    
    if out_type == 'tif':
        
        # here we actually create the file
        driver = gdal.GetDriverByName("GTiff")
        outRaster = driver.Create(outname, cols, rows, 1)
        # writing the metadata
        outRaster.SetGeoTransform((originX, pixelWidth, 0, originY, 0, pixelHeight))
        # creating a new band and writting the data
        outband = outRaster.GetRasterBand(1)
        outband.SetNoDataValue(nodata) #specified no data value by user
        outband.WriteArray(np.array(values)) # writting the values
        outRasterSRS = osr.SpatialReference() # create CRS instance
        outRasterSRS.ImportFromEPSG(4326) # get info for EPSG 4326
        outRaster.SetProjection(outRasterSRS.ExportToWkt()) # set CRS as WKT
    
        # clean up
        outband.FlushCache()
        outband = None
        outRaster = None
    
    elif out_type == 'png':
        
        # This is experimental
        filetime = scn.end_time
        nowutc = filetime.strftime('%H%M')
        outnamev = nowutc+label+'.png'
        data = np.array(values)
        plt.imshow(data)
        plt.gca().set(title=label, xlabel='Longitude', ylabel='Latitude')
        plt.xticks([0, cols], [area_def.area_extent[0], area_def.area_extent[2]])
        plt.yticks([0, rows], [area_def.area_extent[3], area_def.area_extent[1]])
        plt.savefig(outdir+'/'+outnamev)
    
    else:
        print('Not a valid output type')
    
### Call the above function and specify the folder and file names of the output, including the date and time for sorting purposes


outdirv = './output'+nowday

nat2tif(file = file, 
    calibration = "radiance",  
    area_def = area_def,  
    dataset = 'HRV', 
    reader = reader, 
    outdir = outdirv,  
    label = 'HRV', 
    dtype = "float32", 
    radius = 16000, 
    epsilon = .5, 
    nodata = -3.4E+38,
    out_type = 'png')

