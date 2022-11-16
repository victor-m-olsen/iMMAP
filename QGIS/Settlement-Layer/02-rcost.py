import processing
os.chdir(r'D:\iMMAP\proj\ASDC\data\sett_workspace_v04')

processing.run("grass7:r.cost", {
'input':r'process\combined_cost.tif',
'start_coordinates':None,
'stop_coordinates':None,
'-k':False,
'-n':False,
'start_points':r'input\pplp-sample.shp',
'stop_points':None,
'start_raster':None,
'max_cost':0,
'null_cost':None,
'memory':3000,
'output':r'process/rcost_out.tif',
'nearest':r'process/rcost_map.tif',
'outdir':r'process/rcost_outdir.tif',
'GRASS_REGION_PARAMETER':None,
'GRASS_REGION_CELLSIZE_PARAMETER':0,
'GRASS_RASTER_FORMAT_OPT':'',
'GRASS_RASTER_FORMAT_META':'',
'GRASS_SNAP_TOLERANCE_PARAMETER':-1,
'GRASS_MIN_AREA_PARAMETER':0.0001
})

print('grass7:r.cost - done')