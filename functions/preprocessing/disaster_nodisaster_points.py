from functions.preprocessing.disaster_points import disaster_points
from functions.preprocessing.nodisaster_points import nodisaster_points
from functions.preprocessing.final_csv import final_csv

def disaster_nodisaster_points(input_disaster_shp, input_factors_csv, disaster_name, crs_code_meters, output_folder, use_dbscan, buffer_number, number_merge, random_state, distance_min):
    disaster_points_path = output_folder/(disaster_name + "_points.csv")
    disaster_points(input_disaster_shp, input_factors_csv, disaster_name, crs_code_meters, disaster_points_path)
    nodisaster_points_path = output_folder/("no" + disaster_name + "_points.csv")
    nodisaster_points(disaster_points_path, input_factors_csv, crs_code_meters, use_dbscan, buffer_number, number_merge, random_state, distance_min, disaster_name, nodisaster_points_path)
    final_csv_path = output_folder/"final.csv"
    final_csv(disaster_points_path, nodisaster_points_path, final_csv_path)
    return final_csv_path


