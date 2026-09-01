import rioxarray as rxr
import mapclassify
import pandas as pd

def classify(input_tif, method, number_classes, classes_boundaries, output_tif):
    tif = rxr.open_rasterio(input_tif, masked = True)
    tif = tif.fillna(-9999)
    pixels = tif.values
    pixels_valid = pixels != -9999
    if method == "Natural_Breaks":
        classify = mapclassify. NaturalBreaks(pixels[pixels_valid], number_classes)
        classes = classify.yb +1
    elif method == "Equal_Interval":
        classify = mapclassify.EqualInterval(pixels[pixels_valid], number_classes)
        classes = classify.yb +1
    elif method == "Quantile":
        classify = mapclassify.Quantiles(pixels[pixels_valid], number_classes)
        classes = classify.yb +1
    elif method == "manual":
            classify = pd.cut(pixels[pixels_valid], classes_boundaries, labels = False, include_lowest = True)
            classes = classify + 1
            print(pd.isna(classes).sum())
    tif.values[pixels_valid] = classes
    final_tif = tif.astype("int16")
    final_tif = final_tif.rio.write_nodata(-9999)
    final_tif.rio.to_raster(output_tif)
    return