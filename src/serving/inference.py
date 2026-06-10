import pandas as pd
import joblib, json
import os

# MODEL LOADING CONFIGURATION
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
artifacts_dir = os.path.join(project_root, "artifacts")
model_path = os.path.join(artifacts_dir, "xgb_model.pkl")

try:
    model = joblib.load(model_path)
    print(f"Model loaded successfully from {model_path}")
except Exception as e:
    raise Exception(f"Failed to load model from {model_path}: {e}")

# FEATURE COLUMNS LOADING
try:
    with open(os.path.join(artifacts_dir, "feature_columns.json"), "r") as f:
        FEATURE_COLS = json.load(f)
        print(f"Loaded {len(FEATURE_COLS)} feature columns")
except Exception as e:
    raise Exception(f"Failed to load feature columns: {e}")


BINARY_MAP = {
    "gender": {"Female": 0, "Male": 1},
    "Partner": {"No": 0, "Yes": 1},
    "Dependents": {"No": 0, "Yes": 1},
    "PhoneService": {"No": 0, "Yes": 1},
    "PaperlessBilling": {"No": 0, "Yes": 1},
}

NUMERIC_COLS = ["tenure", "MonthlyCharges", "TotalCharges"]


def serve_transform(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()
    df.columns = df.columns.str.strip()

    # numeric cleaning
    for c in NUMERIC_COLS:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
            df[c] = df[c].fillna(0)

    # binary mapping
    for c, mapping in BINARY_MAP.items():
        if c in df.columns:
            df[c] = (
                df[c]
                .astype(str)
                .str.strip()
                .map(mapping)
                .fillna(0)
                .astype(int)
            )

    obj_cols = [c for c in df.select_dtypes(include=["string"]).columns]

    if obj_cols:
        df = pd.get_dummies(df, columns=obj_cols, drop_first=True)

    bool_cols = df.select_dtypes(include=["bool"]).columns
    if len(bool_cols) > 0:
        df[bool_cols] = df[bool_cols].astype(int)

    # align with training features
    df = df.reindex(columns=FEATURE_COLS, fill_value=0)

    return df


def predict(input_dict: dict) -> str:

    df = pd.DataFrame([input_dict])

    required_cols = [
        "gender",
        "Partner",
        "Dependents",
        "PhoneService",
        "PaperlessBilling",
        "tenure",
        "MonthlyCharges",
        "TotalCharges"
    ]

    missing = [c for c in required_cols if c not in df.columns]

    if missing:
        raise ValueError(f"Missing input columns: {missing}")

    df_enc = serve_transform(df)

    preds = model.predict(df_enc)
    print(preds)

    result = preds[0]

    if result == 1:
        return "Likely to churn"      
    else:
        return "Not likely to churn"


if __name__ == "__main__":

    payload = {
        "gender": "Male",
        "Partner": "Yes",
        "Dependents": "No",
        "PhoneService": "Yes",
        "MultipleLines": "No",
        "InternetService": "Fiber optic",
        "OnlineSecurity": "No",
        "OnlineBackup": "No",
        "DeviceProtection": "No",
        "TechSupport": "No",
        "StreamingTV": "Yes",
        "StreamingMovies": "Yes",
        "Contract": "Month-to-month",
        "PaperlessBilling": "Yes",
        "PaymentMethod": "Electronic check",
        "tenure": 12,
        "MonthlyCharges": 120,
        "TotalCharges": 6789,
    }

    print(predict(payload))