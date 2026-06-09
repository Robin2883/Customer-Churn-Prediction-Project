import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split

def train_model(X, y, params=None):

    scale_pos_weight = (y == 0).sum() / (y == 1).sum()

    if params is None:
        params = {"n_estimators": 300, "learning_rate": 0.1, "max_depth": 6}

    model = XGBClassifier( **params, random_state=42, n_jobs=-1, eval_metric="logloss", scale_pos_weight=scale_pos_weight)

    model.fit(X, y)

    return model