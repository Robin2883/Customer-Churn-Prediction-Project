import pandas as pd
import argparse
import os
import json, joblib
from sklearn.model_selection import train_test_split

from src.data.load import data_load
from src.utils.validate import validate_data
from src.data.preprocessing import pre_process
from src.features.build_features import build_features
from src.model_training.train import train_model
from src.model_training.tune import tune_model
from src.model_training.evaluate import evaluate_model

def main(args):

    df= data_load(args.input)
    print(df.head())
    
    validate_data(df)

    df=pre_process(df)
    print(df.head())

    target = args.target
    if target not in df.columns:
            raise ValueError(f"Target column '{target}' not found in data")
    
    df_enc = build_features(df, target_col=target)
    print(df_enc.head())

    project_root= os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    artifacts_dir=os.path.join(project_root, "artifacts")
    os.makedirs(artifacts_dir, exist_ok=True)
    feature_cols = [c for c in df.columns if c != target]
    with open(os.path.join(artifacts_dir, "feature_columns.json"), "w") as f:
        json.dump(feature_cols, f)

    preprocessing_artifact = { "feature_columns": feature_cols, "target": target}
    joblib.dump(preprocessing_artifact, os.path.join(artifacts_dir, "preprocessing.pkl"))


    X = df_enc.drop(columns=[target])
    y = df_enc[target]

    X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

    best_params = tune_model(X_train, y_train)
    model = train_model(X_train, y_train, params=best_params)

    threshold=args.threshold
    evaluate_model(model, threshold, X_test, y_test)


    


if __name__=="__main__":
    p=argparse.ArgumentParser(description='Customer Churn Project')
    p.add_argument('--input', type=str, required=True, help="path to csv")
    p.add_argument("--target", type=str, default="Churn")
    p.add_argument("--threshold", type=float, default=0.35)
    args=p.parse_args()
    main(args)

