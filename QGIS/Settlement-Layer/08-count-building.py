import processing

os.chdir(r'D:\iMMAP\proj\ASDC\data\sett_workspace_v02')

processing.run("native:countpointsinpolygon", {
'POLYGONS':'D:/iMMAP/proj/ASDC/data/sett_workspace_v02/output/sett-basin-lc-union-sample.shp',
'POINTS':'D:\\iMMAP\\proj\\ASDC\\data\\sett_workspace_v02\\input\\building-centroid-sample.shp',
'WEIGHT':'',
'CLASSFIELD':'',
'FIELD':'num-build',
'OUTPUT':'TEMPORARY_OUTPUT'
})

print('count stats - done')