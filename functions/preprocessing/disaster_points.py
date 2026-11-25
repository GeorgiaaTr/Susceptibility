import geopandas as gpd
import pandas as pd

def disaster_points(input_disaster_shp, input_factors_csv, disaster_name, crs_code_meters, output_csv):
    disaster_points = gpd.read_file(input_disaster_shp, columns = []) 
    disaster_points[disaster_name] = 1
    disaster_points["x"] = disaster_points.geometry.x
    disaster_points["y"] = disaster_points.geometry.y
    factors = pd.read_csv(input_factors_csv)
    factors = gpd.GeoDataFrame(factors, geometry = gpd.points_from_xy(factors["x"], factors["y"]), crs = "EPSG:4326")
    disaster_points_m = disaster_points.to_crs(crs_code_meters)
    factors_m = factors.to_crs(crs_code_meters)
    table = disaster_points_m.sjoin_nearest(factors_m, how = "left")
    disaster_column = table[disaster_name].copy()
    table = table.drop(columns = [disaster_name, "x_left", "y_left", "geometry", "index_right"])
    table = table.rename(columns = {"x_right":"x", "y_right":"y"})
    table[disaster_name] = disaster_column
    table.to_csv(output_csv, index = False)
    return table


    
