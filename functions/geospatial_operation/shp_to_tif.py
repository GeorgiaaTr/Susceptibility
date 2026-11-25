import geopandas as gpd
import rioxarray as rxr
from rasterio.features import rasterize


def shp_to_tif(input_shp_paths, input_tif_ref):
    for input_shp_path, output_tif_path, column_name in input_shp_paths:
        input_shp = gpd.read_file(input_shp_path) 
        tif_ref = rxr.open_rasterio(input_tif_ref)
        tif_values = rasterize(shapes = list(zip(input_shp.geometry, input_shp[column_name])), out_shape = (tif_ref.rio.height, tif_ref.rio.width),transform = tif_ref.rio.transform(), fill = -9999, nodata = -9999, all_touched = False, dtype = "float32")
        tif_output = tif_ref.copy(data = [tif_values])
        tif_output = tif_output.rio.write_nodata(-9999)
        tif_output.rio.to_raster(output_tif_path)
    return tif_output