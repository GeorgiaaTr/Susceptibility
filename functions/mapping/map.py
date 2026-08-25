import joblib
import rioxarray as rxr

def map(model_joblib, factors, factors_coords, disaster_name, output_tif):
    model = joblib.load(model_joblib)
    disaster_prob = model.predict_proba(factors)[:, 1]
    map_coords = factors_coords
    disaster_probability = disaster_name + "_probability"
    map_coords[disaster_probability] = disaster_prob
    map_data = map_coords.set_index(["y", "x"])
    map = map_data[disaster_probability].to_xarray()
    map = map.sortby("y", ascending = False)
    map = map.fillna(-9999)
    map = map.rio.write_crs("EPSG:4326")
    map = map.rio.write_nodata(-9999)
    map.rio.to_raster(output_tif)
    return