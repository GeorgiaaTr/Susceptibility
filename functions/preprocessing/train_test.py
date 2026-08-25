import pandas as pd
from sklearn.model_selection import train_test_split

def training_test(input_csv, disaster_name, output_training_csv, output_test_csv):
    input_csv = pd.read_csv(input_csv)
    training, test= train_test_split(input_csv, test_size=0.3, random_state=1, stratify=input_csv["floods"])
    x_train = training.drop(columns = ["x", "y", disaster_name])
    y_train = training["floods"]
    x_test = test.drop(columns = ["x", "y", disaster_name])
    y_test = test[disaster_name]
    training.to_csv(output_training_csv, index = False)
    test.to_csv(output_test_csv, index = False)
    return x_train, y_train, x_test, y_test