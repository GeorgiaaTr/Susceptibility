import rioxarray as rxr
import xarray as xr
import numpy as np
import geopandas as gpd

def nodata(input_area_shp, input_tif, method, output_tif):
    area_shp = gpd.read_file(input_area_shp)
    tif = rxr.open_rasterio(input_tif) 
    area = xr.ones_like(tif)
    area = area.rio.write_nodata(np.nan)
    area_inside = area.rio.clip(area_shp.geometry, area_shp.crs, drop = False).notnull()
    tif = rxr.open_rasterio(input_tif) 
    tif = tif.where(tif != -9999)
    tif = tif.where(tif)
    tif = tif.rio.write_nodata(np.nan)
    tif = tif.rio.interpolate_na(method = method)
    tif = tif.where(area_inside, -9999)
    tif = tif.fillna(-9999)
    tif = tif.rio.write_nodata(-9999)
    tif.rio.to_raster(output_tif)
    return tif