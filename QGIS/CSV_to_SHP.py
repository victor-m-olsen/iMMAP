# Importing CSV

import geopandas as gpd
import pandas as pd
import os

os.chdir('D:\iMMAP\proj\ASDC\data\OCHA-Received\\')

panda_df = pd.read_csv('MISIT_VIllages_With_VilID_AfgID.csv', delimiter=';', decimal=',')

geo_df = gpd.GeoDataFrame(
    panda_df, geometry=gpd.points_from_xy(panda_df.POINT_X, panda_df.POINT_Y))
    
geo_df = geo_df.set_crs('epsg:4326')

geo_df.to_file('MISIT_OCHA.shp')