import processing
import geopandas as gpd

os.chdir(r'D:\iMMAP\proj\ASDC\data\sett_workspace_v04')

# Load data
pplp_sample = gpd.read_file(r'input\pplp-sample.shp', encoding='utf-8')
admin = gpd.read_file(r'input\admin.shp', encoding='utf-8')

join = pplp_sample.sjoin(admin, how="inner", predicate='intersects')

join.to_file(r'process\pplp_join.shp', encoding='utf-8')

## Joining admin attributes to points
## Keeping the point vuid and associated village info
## Joining new district, province and regional attributes
#processing.run("native:joinattributesbylocation", {
#'INPUT':r'input\pplp-sample.shp',
#'JOIN':r'input\admin.shp',
#'PREDICATE':[0],
#'JOIN_FIELDS':['ADM2_EN', 'ADM2_DA', 'ADM2_PCODE', 'ADM1_EN', 'ADM1_DA', 'ADM1_PCODE', 'REG_EN', 'REG_DA', 'REG_PCODE'],
#'METHOD':1,'DISCARD_NONMATCHING':True,
#'PREFIX':'',
#'OUTPUT':'postgres://dbname=\'updates\' host=localhost port=5432 sslmode=disable authcfg=w3a657y key=\'id\' srid=32642 type=MultiPolygon checkPrimaryKeyUnicity=\'1\' table="public"."pplp" (geom)'
##'OUTPUT':r'process\pplp-sample-join.shp'
#})

print('native:joinattributesbylocation - done')



