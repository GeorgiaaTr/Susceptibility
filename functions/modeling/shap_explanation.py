import joblib
import shap
import pandas as pd
import matplotlib.pyplot as plt

def shap_explanation(x_train, x_test, model_joblib, output_png):
    model = joblib.load(model_joblib)
    explainer = shap.Explainer(model.predict_proba, x_train)
    values = explainer(x_test)
    shap_disaster = values[...,1]
    shap.plots.beeswarm(shap_disaster, max_display = 20, show = False)
    plt.gcf().set_size_inches(12,8)
    plt.subplots_adjust(left = 0.30, right = 0.95)
    plt.savefig(output_png)
    plt.show()
    plt.close()
    return
