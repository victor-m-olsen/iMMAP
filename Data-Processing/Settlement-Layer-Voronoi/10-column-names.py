import geopandas as gpd

os.chdir(r'D:\iMMAP\proj\ASDC\data\sett_workspace_v02')

layer = gpd.read_file(r'output\pop-build-area.shp')

print(layer.head())