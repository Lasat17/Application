import folium
import geopandas as gpd
from sentinelsat.sentinel import SentinelAPI
import zipfile
import rasterio
import matplotlib.pyplot as plt
from rasterio import plot
from rasterio.plot import show
from rasterio.mask import mask
from osgeo import gdal
import numpy as np

#9.7174072265625,55.024873440944816

m = folium.Map([9.5965576171875,
              54.6833587900274], zoom_start=11)
boundary = gpd.read_file(r'map(cph).geojson')
folium.GeoJson(boundary).add_to(m)

footprint = None
for i in boundary['geometry']:
    footprint = i

user = "group18r"
password = "eP5NU4H82Y3BktW"
api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')
products = api.query(footprint,
    date = ('20210809', '20211010'),
    platformname = 'Sentinel-2',
    processinglevel = 'Level-2A',
    cloudcoverpercentage = (0, 20))

gdf = api.to_geodataframe(products)
gdf_sorted = gdf.sort_values(['cloudcoverpercentage'], ascending=[True])

dinfar = gdf_sorted.values

##
#print(dinfar)


dinmor = api.download("1508e383-6070-463c-9a4d-9bb93b529c54")

dinmorsmor = dinmor['title'] + ".zip"

import os

print()
dirName = os.listdir("data\\" + dinmor['title']+ ".SAFE\GRANULE\\")



with zipfile.ZipFile(dinmorsmor, 'r') as zip_ref:
   zip_ref.extractall(".\data")
##

bands = "data\\" + dinmor['title']+ ".SAFE\GRANULE\\" +dirName[0]+ "\IMG_DATA\R10m"

fileName = os.listdir("data\\" + dinmor['title']+ ".SAFE\GRANULE\\" + dirName[0]+ "\IMG_DATA\R10m")

#blue = rasterio.open(bands + '\T32UNG_20211026T103131_B02_10m.jp2')
#green = rasterio.open(bands +'\T32UNG_20211026T103131_B03_10m.jp2')

band4 = rasterio.open(bands + '\\' + fileName[3]) #red
band5 = rasterio.open(bands + '\\' + fileName[4]) #nir

##NDVI

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
#plot.show(band4, ax=ax1, cmap='Blues') #red
#plot.show(band5, ax=ax2, cmap='Blues') #nir
fig.tight_layout()

#generate nir and red objects as arrays in float64 format
red = band4.read(1).astype('float64')
nir = band5.read(1).astype('float64')

nir
#ndvi calculation, empty cells or nodata cells are reported as 0
ndvi=np.where(
    (nir+red)==0.,
    0,
    (nir-red)/(nir+red))
ndvi[:5,:5]
#export ndvi image
ndviImage = rasterio.open('image_name.tiff','w',driver='Gtiff',
                          width=band4.width,
                          height = band4.height,
                          count=1, crs=band4.crs,
                          transform=band4.transform,
                          dtype='float64')
ndviImage.write(ndvi,1)
ndviImage.close()
#plot ndvi
ndvi = rasterio.open('image_name.tiff')
fig = plt.figure(figsize=(18,12))
plot.show(ndvi)
##






