import xarray as xr
import rioxarray as rxr
from rasterio.enums import Resampling

def resolution(input_tif_ref, input_path, method, output_tif_path):
     tif_ref = rxr.open_rasterio(input_tif_ref)
     if str(input_path).endswith(".nc"):
         input_nc = xr.open_dataset(input_path)
         if method == "bilinear":
            rm = Resampling.bilinear
         elif method == "mode":
            rm = Resampling.mode
         output = input_nc.rio.reproject_match(tif_ref, resamling=rm)
         output.rio.to_raster(output_tif_path)
     elif str(input_path).endswith(".tif"):
        input_tif = rxr.open_rasterio(input_path)
        if method == "bilinear":
            rm = Resampling.bilinear
        elif method == "mode":
            rm = Resampling.mode
        output = input_tif.rio.reproject_match(tif_ref, resamling=rm)
        output.rio.to_raster(output_tif_path)
     return output