from functions.geospatial_operation.clip import clip
from functions.geospatial_operation.resolution import resolution
from functions.geospatial_operation.final_clip import final_clip
from functions.geospatial_operation.interpolation import nodata
from functions.geospatial_operation.onetif import onetif


def prepare_factors(input_area_shp, input, output_folder, input_tif_ref, output_onetif_path):
    factors = []
    for input_path, factor_name, match_grid_method, interpolation_method, output_tif_path in input:
        general_clip_path = output_folder/(factor_name + "_general_clipped" + input_path.suffix)
        clip(input_area_shp, input_path, general_clip_path)
        match_grid_path = output_folder/(factor_name + "_match_grid.tif")
        reference_tif = output_folder/(input_tif_ref.stem + "_general_clipped" + input_tif_ref.suffix)
        resolution(reference_tif, general_clip_path, match_grid_method, match_grid_path)
        final_clip_path = output_folder/(factor_name + "_final_clipped.tif")
        final_clip(input_area_shp, match_grid_path, final_clip_path)
        if interpolation_method is not None:
            nodata(input_area_shp, final_clip_path, interpolation_method, output_tif_path)
            tif = output_tif_path
        else:
            tif = final_clip_path
        factors.append((tif, factor_name))
    onetif(factors, output_onetif_path)
    return output_onetif_path

