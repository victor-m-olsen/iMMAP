import processing

os.chdir(r'D:\iMMAP\proj\ASDC\data\sett_workspace_v02')

processing.run("native:zonalstatisticsfb", {
'INPUT':'D:/iMMAP/proj/ASDC/data/sett_workspace_v02/output/sett-basin-lc-union-sample.shp',
'INPUT_RASTER':'D:/iMMAP/proj/ASDC/data/sett_workspace_v02/input/pop.tif',
'RASTER_BAND':1,
'COLUMN_PREFIX':'Pop_',
'STATISTICS':[1],
'OUTPUT':'TEMPORARY_OUTPUT'
})

print('zonal stats - done')

