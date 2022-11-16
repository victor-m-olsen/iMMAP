import geopandas as gpd
import numpy as np
import rasterio as rio
from rasterio import features
import matplotlib.pyplot as plt
import processing

iteration = '03'

os.chdir(r'D:\iMMAP\proj\ASDC\data\sett_workspace_v02')

# Load data
sett = gpd.read_file(r'input\afg_pplp_subset_proj.shp')
admin = gpd.read_file(r'input\afg_adm2_new_proj.shp')
pop = rio.open(r'input\pop_clipped_resamp.tif', masked=True)
bbox = gpd.read_file(r'input\bbox.shp')

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
admin_lines.to_file(r'process\admin_lines.shp')
admin_lines = gpd.read_file(r'process\admin_lines.shp').buffer(50)

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

    with rio.open(r'process\admin_lines_v{}.tif'.format(iteration), 'w', **profile) as dst:
        dst.write(rasterized, 1) #pop_clipped[0][0].astype(rasterio.float32), 1)



### Prepare and combine admin boundary and pop rasters

# Open raster as numpy array
adm = rio.open(r'process\admin_lines_v{}.tif'.format(iteration), masked=True)
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

    with rio.open(r'process\combined_cost.tif'.format(iteration), 'w', **profile) as dst:
        dst.write(cost_combined[0], 1) #pop_clipped[0][0].astype(rasterio.float32), 1)


print('done')
