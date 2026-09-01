from functions.mapping.map import map
from functions.geospatial_operation.classify import classify

def susceptibility_map(model_joblib, factors, factors_coords, disaster_name, map_tif, method, number_classes, classes_boundaries, classified_map_tif):
    map(model_joblib, factors, factors_coords, disaster_name, map_tif)
    classify(map_tif, method, number_classes, classes_boundaries, classified_map_tif)
    return
