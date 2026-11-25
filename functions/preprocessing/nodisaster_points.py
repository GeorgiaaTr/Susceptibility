import geopandas as gpd
import pandas as pd
import geopandas as gpd
from sklearn.cluster import DBSCAN

def nodisaster_points(input_disaster_csv, input_factors_csv, crs_code_meters, use_dbscan, buffer_number, number_merge, random_state, distance_min, disaster_name, output_csv):
    factor_points = pd.read_csv(input_factors_csv)
    disaster_points = pd.read_csv(input_disaster_csv)
    disaster_points = gpd.GeoDataFrame(disaster_points, geometry = gpd.points_from_xy(disaster_points["x"], disaster_points["y"]), crs = "EPSG:4326")
    factor_points = gpd.GeoDataFrame(factor_points, geometry = gpd.points_from_xy(factor_points["x"], factor_points["y"]), crs = "EPSG:4326")
    disaster_points_m = disaster_points.to_crs(crs_code_meters)
    factor_points_m = factor_points.to_crs(crs_code_meters)
    if use_dbscan ==  True:
        table = list(zip(disaster_points_m.geometry.x, disaster_points_m.geometry.y))
        points = DBSCAN(eps = number_merge, min_samples = 2).fit(table)
        disaster_points_m["groups"] = points
        single_points = disaster_points_m["groups"] == -1
        merge_points = disaster_points_m["groups"] != -1
        single_points_buffer = disaster_points_m[single_points].buffer(buffer_number).union_all()
        merge_points_buffer = disaster_points_m[merge_points].buffer(number_merge/2).union_all().buffer(buffer_number)
        buffer = single_points_buffer.union(merge_points_buffer)
        points =  factor_points_m.geometry.disjoint(buffer)
        points = factor_points[points]
    else:
        buffer = disaster_points_m.buffer(buffer_number).union_all()
        points =  factor_points_m.geometry.disjoint(buffer)
        points = factor_points[points]

    points = points.reset_index()
    points_m = points.to_crs(crs_code_meters)
    nodisaster_lines = []
    while len(nodisaster_lines) < len(disaster_points) and not points.empty:
        selected = points_m.sample(n = 1, random_state = random_state)
        selected_point = selected.geometry.item()
        selected_row = selected.index.item()
        nodisaster_lines.append(selected_row)
        distances = points_m.geometry.distance(selected_point)
        points_m = points_m[distances > distance_min]
    nodisaster_points = points.take(nodisaster_lines)
    nodisaster_points[disaster_name] = 0
    nodisaster_points= nodisaster_points.drop(columns = ["geometry", "index"])
    nodisaster_points.to_csv(output_csv, index = False)
    return nodisaster_points