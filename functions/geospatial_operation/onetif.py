import xarray as xr
import rioxarray as rxr

def onetif(input_tifs, output_tif):
    tifs = []
    tif_names = []
    for input_tif, tif_name in input_tifs:
        tif = rxr.open_rasterio(input_tif) 
        tif = tif.squeeze("band", drop = True)
        tifs.append(tif)
        tif_names.append(tif_name)
    onetif = xr.concat(tifs, dim = "band")
    onetif.attrs["long_name"] = tif_names
    onetif = onetif.fillna(-9999)
    onetif = onetif.rio.write_nodata(-9999)
    onetif.rio.to_raster(output_tif)
    return onetif