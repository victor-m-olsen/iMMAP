import geopandas as gpd

os.chdir(r'D:\iMMAP\proj\ASDC\data\sett_workspace_v02')

polygons = gpd.read_file(r'process\count.shp')

polygons["area"] = polygons['geometry'].area

polygons.to_file(r'output\pop-build-area.shp')