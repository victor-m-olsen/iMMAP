import processing

os.chdir(r'D:\iMMAP\proj\ASDC\data\sett_workspace_v04')

#processing.run("native:union", {
#    'INPUT': r'output\sett-basin-union-sample.shp',
#    'OVERLAY': 'land-cover-sample-bbox.shp',
#    'OVERLAY_FIELDS_PREFIX': '',
#    'OUTPUT': r'output\sett-basin-lc-union-sample.shp'
#})

processing.run("native:union", {
'INPUT':'D:/iMMAP/proj/ASDC/data/sett_workspace_v04/process/ppla.shp',
'OVERLAY':'D:/iMMAP/proj/ASDC/data/sett_workspace_v04/input/land-cover-dis-sample.shp',
'OVERLAY_FIELDS_PREFIX':'',
'OUTPUT':'postgres://dbname=\'updates\' host=localhost port=5432 user=\'postgres\' password=\'pewp7re\' sslmode=disable table="public"."lndcrva-sample " (geom)'
})

print('union - done')
