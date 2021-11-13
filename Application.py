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



with zipfile.ZipFile(dinmorsmor, 'r') as zip_ref:
   zip_ref.extractall(".\data")
##

bands = r'D:\Uni\7. Semester\CondaApplication\data\S2A_MSIL2A_20211026T103131_N0301_R108_T32UNG_20211026T133456.SAFE\GRANULE\L2A_T32UNG_A033138_20211026T103127\IMG_DATA\R60m'
blue = rasterio.open(bands + '\T32UNG_20211026T103131_B02_60m.jp2')
green = rasterio.open(bands +'\T32UNG_20211026T103131_B03_60m.jp2')
red = rasterio.open(bands + '\T32UNG_20211026T103131_B04_60m.jp2')
with rasterio.open('image_name.tiff','w',driver='Gtiff', width=blue.width, height=blue.height, count=3, crs=blue.crs,transform=blue.transform, dtype=blue.dtypes[0]) as rgb:
    rgb.write(blue.read(1),3)
    rgb.write(green.read(1),2)
    rgb.write(red.read(1),1)
    rgb.close()

check = rasterio.open("image_name.tiff")
check.crs


bound_crs = boundary.to_crs({'init': 'epsg:32632'})
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

src = rasterio.open(r'masked_image.tif')
plt.figure(figsize=(6, 6))
plt.title('Final Image')
plot.show(src, adjust='linear')
