import geopandas as gpd
import numpy as np
import rasterio as rio
from rasterio import features
import matplotlib.pyplot as plt
import processing


iteration = '21'

os.chdir(r'D:\iMMAP\proj\ASDC\data\sett_workspace')

# Load data
sett = gpd.read_file('afg_pplp_subset_proj.shp')
admin = gpd.read_file('afg_adm2_new_proj.shp')
pop = rio.open('pop_clipped_qgis_resamp.tif', masked=True)
bbox = gpd.read_file('bbox.shp')

# Clipping the data
admin_clipped = gpd.clip(admin, bbox)
# Ignore missing/empty geometries
admin_clipped = admin_clipped[~admin_clipped.is_empty]



### Adding hard boundaries to raster
# Turn rows in geodataframe into list of linestrings
lines = []
for x in range(len(admin_clipped.index)):

    geometry = admin_clipped.iloc[x].geometry    #gets a polygon from each row (i.e. object) in geodataframe
    boundary = geometry.boundary                 #turns polygon into linestring
    if boundary.type == 'MultiLineString':
        for line in boundary:
            lines.append(line)
    else:
        lines.append(boundary)

# Convert linestring to geoseries
admin_lines = gpd.GeoSeries(lines)

# Saving admin_lines to file
admin_lines.to_file("admin_lines.shp")
admin_lines = gpd.read_file("admin_lines.shp").buffer(100)

# Get list of geometries for all features in vector file
geom = [shapes for shapes in admin_lines.geometry]

# Rasterize vector using the shape and coordinate system of the raster
rasterized = features.rasterize(geom,
                                out_shape = pop.shape,
                                fill = 0,
                                out = None,
                                transform = pop.transform,
                                all_touched = False,
                                default_value = 99999999,
                                dtype = None)

# Save raster with admin lines
with rio.Env():

    profile = pop.profile

    # And then change the band count to 1, set the
    # dtype to uint8, and specify LZW compression.
    profile.update(
        dtype=rio.float32,
        count=1,
        compress='lzw')

    with rio.open('admin_lines_v{}.tif'.format(iteration), 'w', **profile) as dst:
        dst.write(rasterized, 1) #pop_clipped[0][0].astype(rasterio.float32), 1)




### Prepare and combine admin boundary and pop rasters

# Open raster as numpy array
adm = rio.open('admin_lines_v{}.tif'.format(iteration), masked=True)
adm_np = adm.read()

# Opening pop as numpy array
pop_np = pop.read()

# Removing nodata values from calculation
pop_np[(pop_np <= -99.0)] = np.nan

print(np.nanmax(pop_np))
print(np.nanmin(pop_np))

# Conduct calculation to reverse values (("Rasterlayer" - Max_value) * -1) + Min_value
cost = ((pop_np - np.nanmax(pop_np)) * -1) + np.nanmin(pop_np)


# Sdd admin boundaries to cost layer
cost_combined = cost + adm_np

# Optional - set boundary pixels to nan
#cost_combined[(cost_combined >= 1000.0)] = np.nan

# Save cost layer to file
with rio.Env():

    profile = pop.profile

    # And then change the band count to 1, set the
    # dtype to uint8, and specify LZW compression.
    profile.update(
        dtype=rio.float32,
        count=1,
        compress='lzw')

    with rio.open('combined_cost_v{}.tif'.format(iteration), 'w', **profile) as dst:
        dst.write(cost_combined[0], 1) #pop_clipped[0][0].astype(rasterio.float32), 1)

processing.run("grass7:r.cost", {
'input':'combined_cost_v{}.tif'.format(iteration),
'start_coordinates':None,
'stop_coordinates':None,
'-k':False,
'-n':False,
'start_points':'D:/iMMAP/proj/ASDC/data/geodb_backups/afg_pplp_SUBSET_proj.shp',
'stop_points':None,
'start_raster':None,
'max_cost':0,
'null_cost':None,
'memory':300,
'output':'D:/iMMAP/proj/ASDC/data/sett_workspace/qgis/out.tif',
'nearest':'D:/iMMAP/proj/ASDC/data/sett_workspace/qgis/cost_map.tif',
'outdir':'D:/iMMAP/proj/ASDC/data/sett_workspace/qgis/outdir.tif',
'GRASS_REGION_PARAMETER':None,
'GRASS_REGION_CELLSIZE_PARAMETER':0,
'GRASS_RASTER_FORMAT_OPT':'',
'GRASS_RASTER_FORMAT_META':'',
'GRASS_SNAP_TOLERANCE_PARAMETER':-1,
'GRASS_MIN_AREA_PARAMETER':0.0001
})

print('grass7:r.cost - done')

processing.run("gdal:polygonize",
{'INPUT':'D:/iMMAP/proj/ASDC/data/sett_workspace/qgis/cost_map.tif',
'BAND':1,
'FIELD':'DN',
'EIGHT_CONNECTEDNESS':False,
'EXTRA':'',
'OUTPUT':'D:/iMMAP/proj/ASDC/data/sett_workspace/qgis/cost_map.shp'})

print('gdal:polygonize - done')

processing.run("grass7:v.generalize",{
'input':'D:/iMMAP/proj/ASDC/data/sett_workspace/qgis/cost_map.shp',
'type':[2],
'cats':'',
'where':'',
'method':3,
'threshold':200,
'look_ahead':15,
'reduction':50,
'slide':0.5,
'angle_thresh':3,
'degree_thresh':0,
'closeness_thresh':0,
'betweeness_thresh':0,
'alpha':1,
'beta':1,
'iterations':1,
'-t':False,
'-l':True,
'output':'D:/iMMAP/proj/ASDC/data/sett_workspace/qgis/cost_map_gen.shp',
'error':'TEMPORARY_OUTPUT',
'GRASS_REGION_PARAMETER':None,
'GRASS_SNAP_TOLERANCE_PARAMETER':1,
'GRASS_MIN_AREA_PARAMETER':0.0001,
'GRASS_OUTPUT_TYPE_PARAMETER':3,
'GRASS_VECTOR_DSCO':'',
'GRASS_VECTOR_LCO':'',
'GRASS_VECTOR_EXPORT_NOCAT':False
})

print('grass7:v.generalize - done')

print('done')
