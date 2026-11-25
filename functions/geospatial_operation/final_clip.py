import geopandas as gpd
import rioxarray as rxr

def final_clip(input_area_shp, input_tif_path, output_tif_path):
     area_shp = gpd.read_file(input_area_shp)
     input_tif = rxr.open_rasterio(input_tif_path)
     final_clip = input_tif.rio.clip(area_shp.geometry.values, area_shp.crs, drop = False, all_touched = False)
     final_clip = final_clip.fillna(-9999)
     final_clip = final_clip.rio.write_nodata(-9999)
     final_clip.rio.to_raster(output_tif_path)
     return final_clip