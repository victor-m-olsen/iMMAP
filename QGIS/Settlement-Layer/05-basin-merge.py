import processing

os.chdir(r'D:\iMMAP\proj\ASDC\data\sett_workspace_v04')

#db_path = 'postgres://dbname=\'updates\' host=localhost port=5432 sslmode=disable authcfg=w3a657y key=\'id\' srid=32642 type=MultiPolygon checkPrimaryKeyUnicity=\'1\' table="public"."{}" (geom)'

processing.run("native:union", {
    'INPUT': r'process\ppla.shp',
    'OVERLAY': r'input\basins-sample.shp',
    'OVERLAY_FIELDS_PREFIX': '',
    'OUTPUT': r'process\ppla-basin.shp'
})

print('union - done')

## save generalized table to db with encoding utf8
#processing.run("qgis:importintopostgis", 
#{'INPUT':r'process\sett-basin-union.shp',
#'DATABASE':'ASDC-Update',
#'SCHEMA':'public',
#'TABLENAME':None,
#'PRIMARY_KEY':'',
#'GEOMETRY_COLUMN':'geom',
#'ENCODING':'UTF-8',
#'OVERWRITE':True,
#'CREATEINDEX':True,
#'LOWERCASE_NAMES':True,
#'DROP_STRING_LENGTH':False,
#'FORCE_SINGLEPART':False
#})
#
#print('qgis:importintopostgis - done')