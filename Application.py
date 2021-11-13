import folium
import geopandas as gpd
from sentinelsat.sentinel import SentinelAPI
import rasterio
import matplotlib.pyplot as plt
from rasterio import plot
from rasterio.plot import show
from rasterio.mask import mask
from osgeo import gdal



m = folium.Map([51.65771484375, 53.76494896075243], zoom_start=11)
boundary = gpd.read_file(r'map.geojson')
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

print(dinfar)

api.download("9b93ff2b-9509-4bc1-ba14-a7b9e187c6e0")


