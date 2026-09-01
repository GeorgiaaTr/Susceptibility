import joblib
from sklearn.metrics import roc_auc_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import RocCurveDisplay
from sklearn.metrics import ConfusionMatrixDisplay
import pandas as pd
import matplotlib.pyplot as plt


def evaluation_model(x_train, y_train, x_test, y_test, model_joblib, output_csv, output_roccurves_png, output_cm_test_png, output_cm_train_png):
    model = joblib.load(model_joblib)
    predict_test  = model.predict(x_test)
    prob_test = model.predict_proba(x_test)
    prob_test = prob_test[:,1]
    roc_auc_test = roc_auc_score(y_test, prob_test)
    precision_test = precision_score(y_test, predict_test)
    accuracy_test = accuracy_score(y_test, predict_test)
    sensitivity_test = recall_score(y_test, predict_test)
    specificity_test = recall_score(y_test, predict_test, pos_label = 0)
    f1_test = f1_score(y_test, predict_test)
    confusion_matrix_test = confusion_matrix(y_test, predict_test)

    predict_train  = model.predict(x_train)
    prob_train = model.predict_proba(x_train)
    prob_train = prob_train[:,1]
    roc_auc_train = roc_auc_score(y_train, prob_train)
    precision_train = precision_score(y_train, predict_train)
    accuracy_train = accuracy_score(y_train, predict_train)
    sensitivity_train = recall_score(y_train, predict_train)
    specificity_train = recall_score(y_train, predict_train, pos_label = 0)
    f1_train = f1_score(y_train, predict_train)
    confusion_matrix_train = confusion_matrix(y_train, predict_train)


    metrics = pd.DataFrame([["roc_auc_test:", roc_auc_test], ["precision_test:", precision_test], ["accuracy_test:", accuracy_test], ["sensitivity_test:", sensitivity_test], ["specificity_test", specificity_test], ["f1_test", f1_test], ["confusion_matrix_test", confusion_matrix_test], ["", ], ["roc_auc_train:", roc_auc_train], ["precision_train:", precision_train], ["accuracy_train:", accuracy_train], ["sensitivity_train:", sensitivity_train], ["specificity_train", specificity_train], ["f1_train", f1_train], ["confusion_matrix_train", confusion_matrix_train]])
    metrics.to_csv(output_csv, index = False, header = False)

    fig, ax = plt.subplots()
    RocCurveDisplay.from_predictions(y_test, prob_test, ax = ax, name = "Test")
    RocCurveDisplay.from_predictions(y_train, prob_train ,ax = ax, plot_chance_level = True, name = "Training")
    plt.title("ROC Curves")
    plt.savefig(output_roccurves_png)
    ConfusionMatrixDisplay.from_predictions(y_test, predict_test)
    plt.title("Confusion matrix - Test")
    plt.savefig(output_cm_test_png)
    ConfusionMatrixDisplay.from_predictions(y_train, predict_train)
    plt.title("Confusion matrix - Train")
    plt.savefig(output_cm_train_png)
    plt.show()
    plt.close()
    return

