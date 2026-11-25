import rioxarray as rxr
import numpy as np
import pandas as pd

def table_factors(input_tif, output_factors_csv, output_factors_only_csv):
     tif = rxr.open_rasterio(input_tif, chunks= "auto")
     tif_names = list(tif.attrs["long_name"])
     tif = tif.assign_coords(band = tif_names)
     table_factors = tif.to_dataset(dim = "band").to_dask_dataframe().compute()
     table_factors = table_factors[["x", "y"] + tif_names]
     table_factors = table_factors.replace(-9999, np.nan)
     table_factors = table_factors.dropna()
     table_factors.to_csv(output_factors_csv, index = False)
     factors_coords = table_factors[["x", "y"]]
     table_factors_only = table_factors.drop(columns = ["x", "y"]) 
     table_factors_only.to_csv(output_factors_only_csv, index = False)
     return table_factors, table_factors_only, factors_coords