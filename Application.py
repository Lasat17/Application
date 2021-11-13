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

#9.7174072265625,55.024873440944816

m = folium.Map([55.024873440944816, 9.7174072265625], zoom_start=11)
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

##
#print(dinfar)


dinmor = api.download("9b93ff2b-9509-4bc1-ba14-a7b9e187c6e0")

dinmorsmor = dinmor['title'] + ".zip"



with zipfile.ZipFile(dinmorsmor, 'r') as zip_ref:
   zip_ref.extractall(".\data")
##

bands = r'D:\Uni\7. Semester\CondaApplication\data\S2B_MSIL2A_20210814T074609_N0301_R135_T39UXV_20210814T095029.SAFE\GRANULE\L2A_T39UXV_A023184_20210814T075212\IMG_DATA\R10m'
blue = rasterio.open(bands + '\T39UXV_20210814T074609_B02_10m.jp2')
green = rasterio.open(bands +'\T39UXV_20210814T074609_B03_10m.jp2')
red = rasterio.open(bands + '\T39UXV_20210814T074609_B04_10m.jp2')
with rasterio.open('image_name.tiff','w',driver='Gtiff', width=blue.width, height=blue.height, count=3, crs=blue.crs,transform=blue.transform, dtype=blue.dtypes[0]) as rgb:
    rgb.write(blue.read(1),3)
    rgb.write(green.read(1),2)
    rgb.write(red.read(1),1)
    rgb.close()

check = rasterio.open("image_name.tiff")
print(check.crs)


bound_crs = boundary.to_crs({'init': 'epsg:32639'})
with rasterio.open("image_name.tiff") as src:
    out_image, out_transform = mask(src,
                                    bound_crs.geometry, crop=True)
    out_meta = src.meta.copy()
    out_meta.update({"driver": "GTiff",
                     "height": out_image.shape[1],
                     "width": out_image.shape[2],
                     "transform": out_transform})

with rasterio.open("masked_image.tif", "w", **out_meta) as final:
    final.write(out_image)

src = rasterio.open(r'...\masked_image.tif')
plt.figure(figsize=(6, 6))
plt.title('Final Image')
plot.show(src, adjust='linear')
