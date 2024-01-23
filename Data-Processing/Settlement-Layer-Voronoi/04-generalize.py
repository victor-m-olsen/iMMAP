import processing

os.chdir(r'D:\iMMAP\proj\ASDC\data\sett_workspace_v04')

# Arabic attributes ('name-local') will be lost. Need to rejoin afterwards
processing.run("grass7:v.generalize",{
'input':r'process\rcost_map_poly_admAtt.shp',
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
'output':r'process\ppla.shp', 
'error':'TEMPORARY_OUTPUT',
'GRASS_REGION_PARAMETER':None,
'GRASS_SNAP_TOLERANCE_PARAMETER':1,
'GRASS_MIN_AREA_PARAMETER':0.0001,
'GRASS_OUTPUT_TYPE_PARAMETER':3,
'GRASS_VECTOR_DSCO':'',
'GRASS_VECTOR_LCO':'',
'GRASS_VECTOR_EXPORT_NOCAT':False
})

print('gdal:generalize - done')



