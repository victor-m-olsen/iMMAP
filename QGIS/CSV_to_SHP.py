# Importing CSV

import geopandas as gpd
import pandas as pd
import os

os.chdir('D:\iMMAP\proj\ASDC\data\\')


panda_df = pd.read_csv('Copy of Water Points GPSPoints.csv', delimiter=';', decimal=',')

print(panda_df)
geo_df = gpd.GeoDataFrame(
    panda_df, geometry=gpd.points_from_xy(panda_df.Longitude, panda_df.Latitude))
    
geo_df = geo_df.set_crs('epsg:4326')

geo_df.to_file('WASH-Water-Points.shp')