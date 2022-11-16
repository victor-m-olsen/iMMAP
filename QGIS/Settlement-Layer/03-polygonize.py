import processing
os.chdir(r'D:\iMMAP\proj\ASDC\data\sett_workspace_v04')

processing.run("gdal:polygonize",
{'INPUT':r'process\rcost_map.tif',
'BAND':1,
'FIELD':'DN',
'EIGHT_CONNECTEDNESS':False,
'EXTRA':'',
'OUTPUT':r'process\rcost_map_poly.shp'
})

print('gdal:polygonize - done')


# Joining admin attributes to points
# Keeping the point vuid and associated village info
# Joining new district, province and regional attributes
processing.run("native:joinattributesbylocation", {
'INPUT':r'input\pplp-sample.shp',
'JOIN':r'input\admin.shp',
'PREDICATE':[0],
'JOIN_FIELDS':['ADM2_EN', 'ADM2_DA', 'ADM2_PCODE', 'ADM1_EN', 'ADM1_DA', 'ADM1_PCODE', 'REG_EN', 'REG_DA', 'REG_PCODE'],
'METHOD':1,'DISCARD_NONMATCHING':True,
'PREFIX':'',
'OUTPUT':r'process\pplp-sample-join.shp'
})

print('1/2 native:joinattributesbylocation - done')


#----> take out this step and do it seperately, 
#producing the final pplp (except for vuid pop info) before proceeding

# Joining point attributes to rcost maps polygons
processing.run("native:joinattributesbylocation", {
'INPUT':r'process\rcost_map_poly.shp',
'JOIN':r'process\pplp-sample-join.shp',
'PREDICATE':[0],
'JOIN_FIELDS':['vuid','name_local','name_loc_1','name_alter', 'ADM2_EN', 'ADM2_DA', 'ADM2_PCODE', 'ADM1_EN', 'ADM1_DA', 'ADM1_PCODE', 'REG_EN', 'REG_DA', 'REG_PCODE'],
'METHOD':1,'DISCARD_NONMATCHING':True,
'PREFIX':'',
'OUTPUT':r'process\rcost_map_poly_admAtt.shp'
})

print('2/2 native:joinattributesbylocation - done')


