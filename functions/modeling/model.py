import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold
from optuna_integration.sklearn import OptunaSearchCV
from optuna.distributions import CategoricalDistribution
import joblib
from importlib import import_module

def model(x_train, y_train, model_library, model_name, random_state, scaling, range_parametres, output_csv, output_joblib):
    model_library = import_module(model_library)
    model_type = getattr(model_library, model_name)
    model = model_type()

    if scaling == True:
        model = Pipeline([("scaler", StandardScaler()), ("model", model)])
        start = "model__"
    else:
        start = ""

    model_proba = hasattr(model, "predict_proba")
    if model_proba == False:
        model = CalibratedClassifierCV(estimator = model, ensemble = False)
        start = "estimator__" + start
        
    validation = StratifiedKFold(n_splits = 5, shuffle=True, random_state = random_state)
    hyperparametres = {}
    for name in range_parametres:
        values = range_parametres[name]
        hyperparametres[start + name] = CategoricalDistribution(values)
    optimization = OptunaSearchCV(estimator = model, param_distributions = hyperparametres, n_trials = 100 , cv = validation, random_state = random_state, scoring = "roc_auc")
    optimization.fit(x_train, y_train)
    best_parametrs = optimization.best_params_
    best_score = optimization.best_score_
    model_results = pd.DataFrame([["best_parametrs:", best_parametrs], ["best_score(roc_auc):", best_score]])
    model_results.to_csv(output_csv, index = False, header = False)
    model = optimization.best_estimator_
    joblib.dump(model, output_joblib)
    return model




