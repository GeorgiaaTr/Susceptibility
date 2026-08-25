import joblib
from sklearn.inspection import permutation_importance
import pandas as pd
import matplotlib.pyplot as plt

def factors_importance(x_test, y_test, model_joblib, random_state, output_png):
    model = joblib.load(model_joblib)
    factors_importance = permutation_importance(model, x_test, y_test, scoring = "roc_auc", random_state = random_state)
    factors_importance = factors_importance.importances_mean
    factors_importance = pd.Series(factors_importance, x_test.columns)

    factors_names = []
    for factor_name in factors_importance.index:
        if "__" in factor_name:
            factor_name = factor_name.split("__")[0]
        factors_names.append(factor_name)
    factors_importance.index = factors_names
    factors_importance = factors_importance.groupby(factors_importance.index).sum()
    factors_importance = factors_importance.sort_values()
    plt.barh(factors_importance.index, factors_importance.values)
    plt.title("Factors_importance")
    plt.savefig(output_png)
    return