from functions.modeling.factors_importance import factors_importance
from functions.modeling.shap_explanation import shap_explanation

def explain_model(x_test, y_test, model_joblib, random_state, output_importance_png, x_train, output_shapexplanation_png):
    factors_importance(x_test, y_test, model_joblib, random_state, output_importance_png)
    shap_explanation(x_train, x_test, model_joblib, output_shapexplanation_png)
    return

