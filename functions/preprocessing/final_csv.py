import pandas as pd

def final_csv(input_csv1, input_csv2, output_csv):
    csv1 = pd.read_csv(input_csv1)
    csv2 = pd.read_csv(input_csv2)
    final_csv = pd.concat([csv1, csv2])
    final_csv.to_csv(output_csv, index = False)
    return final_csv
