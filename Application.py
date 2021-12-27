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

m = folium.Map([10.763468742370605,
              55.32006177774786], zoom_start=11)
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


dinmor = api.download('e8d0a4e5-c9a2-4c74-aafe-0163284e9aec')

dinmorsmor = dinmor['title'] + ".zip"

import os

print()




with zipfile.ZipFile(dinmorsmor, 'r') as zip_ref:

   zip_ref.extractall("data/")
   print("Zip done")
##
dirName = os.listdir("data\\" + dinmor['title']+ ".SAFE\GRANULE\\")

bands = "data\\" + dinmor['title']+ ".SAFE\GRANULE\\" +dirName[0]+ "\IMG_DATA\R60m"

fileName = os.listdir("data\\" + dinmor['title']+ ".SAFE\GRANULE\\" + dirName[0]+ "\IMG_DATA\R60m")

#blue = rasterio.open(bands + '\T32UNG_20211026T103131_B02_10m.jp2')
#green = rasterio.open(bands +'\T32UNG_20211026T103131_B03_10m.jp2')


band2 = rasterio.open(bands + '\\' + fileName[2]) #blue
band3 = rasterio.open(bands + '\\' + fileName[3]) #green
band4 = rasterio.open(bands + '\\' + fileName[4]) #red
band8 = rasterio.open(bands + '\\' + fileName[8]) #nir

##NDVI
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 4))
plot.show(band2, ax=ax1, cmap='Blues')
plot.show(band3, ax=ax2, cmap='Greens')
plot.show(band4, ax=ax3, cmap='Reds')
fig.tight_layout()


#generate nir and red objects as arrays in float64 format
red = band4.read(1).astype('float')
nir = band8.read(1).astype('float')

nir
#ndvi calculation, empty cells or nodata cells are reported as 0

ndvi = (nir - red) / (nir + red)
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

#Øverst venstre
upperLeft = ndvi.transform * (0,0)
print(upperLeft)

#lavere højre
lowerRight = ndvi.transform * (ndvi.width, ndvi.height)
print(lowerRight)

print(ndvi.crs)
##

from pyproj import Proj, transform

inProj = Proj(init=ndvi.crs)
outProj = Proj(init='epsg:4326')
x1, y1 = upperLeft
x2, y2 = lowerRight

x3, y3 =transform(inProj, outProj, x1, y1)
x4, y4 =transform(inProj, outProj, x2, y2)

#printer upper left
print(y3, x3)

#printer lower right
print(y4, x4)




