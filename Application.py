
import folium
import geopandas as gpd
from sentinelsat.sentinel import SentinelAPI
import rasterio
import matplotlib.pyplot as plt
from rasterio import plot
from rasterio.plot import show
from rasterio.mask import mask
from osgeo import gdal

m = folium.Map([9.7174072265625, 55.024873440944816], zoom_start=11)
m = folium.Map([10.832519531249998, 55.024873440944816], zoom_start=11)
m = folium.Map([10.832519531249998, 55.665193184436035], zoom_start=11)
m = folium.Map([9.7174072265625,55.665193184436035], zoom_start=11)
m = folium.Map([9.7174072265625, 55.024873440944816], zoom_start=11)
boundary = gpd.read_file(r'map.geojson')
folium.GeoJson(boundary).add_to(m)
m

footprint = None
for i in boundary['geometry']:
    footprint = i

user = "group18r"
password = "eP5NU4H82Y3BktW"
api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')
products = api.query(footprint,
                     date=('20200109', '20200510'), #date=('20211029', '20211029'),
                     platformname='Sentinel-2',
                     processinglevel='Level-2A',
                     cloudcoverpercentage=(0, 20))

gdf = api.to_geodataframe(products)
gdf_sorted = gdf.sort_values(['cloudcoverpercentage'], ascending=[True])
gdf_sorted