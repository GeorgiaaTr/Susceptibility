import geopandas as gpd
import xarray as xr
import rioxarray as rxr

def clip(input_area_shp, input_path, output_path):
     area_shp = gpd.read_file(input_area_shp)
     if str(input_path).endswith(".nc"):
         input_nc = xr.open_dataset(input_path)
         clip = input_nc.rio.clip(area_shp.geometry.values, area_shp.crs, drop = True, all_touched = True)
         clip.to_netcdf(output_path)
     elif str(input_path).endswith(".tif"):
        input_tif = rxr.open_rasterio(input_path, masked = True)
        input_tif = input_tif.astype("float32")
        clip = input_tif.rio.clip(area_shp.geometry.values, area_shp.crs, drop = True, all_touched = True)
        clip = clip.fillna(-9999)
        clip = clip.rio.write_nodata(-9999)
        clip.rio.to_raster(output_path)
     elif str(input_path).endswith(".shp"):
        input_shp = gpd.read_file(input_path)
        clip = gpd.clip(input_shp, area_shp)
        clip.to_file(output_path)
     return clip



