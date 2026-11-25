import pandas as pd
     
     
def encoding(x_train, input_csv, columns_encoding, output_training_encoding_csv, output_encoding_csv):
        if columns_encoding:
                x_train_en = pd.get_dummies(x_train, columns = columns_encoding, prefix_sep= "__",dtype = "int16")   
                csv_en = pd.get_dummies(input_csv, columns = columns_encoding, prefix_sep= "__",dtype = "int16")   
        else:
                x_train_en = x_train
                csv_en = input_csv
        csv_en = csv_en.reindex(columns = x_train_en.columns, fill_value = 0)
        x_train_en.to_csv(output_training_encoding_csv, index = False)
        csv_en.to_csv(output_encoding_csv, index = False)
        return x_train_en, csv_en