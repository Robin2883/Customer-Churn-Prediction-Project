import pandas as pd

pd.set_option("display.max_columns", None)

def map_binary_series(s: pd.Series) -> pd.Series:

    # Get unique values and remove NaN
    vals = s.dropna().unique().astype(str)
    valset=set(vals)  #set is used because order doesn't matter

    # Yes/No mapping
    if valset == {"Yes", "No"}:
        return s.map({"No": 0, "Yes": 1}).astype("Int64")
    
    # Gender mapping
    if valset=={"Female", "Male"}:
        return s.map({"Male": 1, "Female": 0}).astype("Int64")
    
    # Generic Binary Mapping
    if len(vals) == 2:
        sorted_vals=sorted(vals)
        mapping = {sorted_vals[0]: 0, sorted_vals[1]: 1}
        return s.astype(str).map(mapping).astype("Int64")

    # Non-bianry Features
    return s

def build_features(df: pd.DataFrame, target_col: str = "Churn") -> pd.DataFrame:

    print(f"Building features...")

    df = df.copy()

    # Encode target FIRST (if present)
    if target_col in df.columns:
        df[target_col] = df[target_col].str.strip().map({"Yes": 1, "No": 0})

    obj_cols = [c for c in df.select_dtypes(include=["string"]).columns if c != target_col]
    binary_cols = [c for c in obj_cols if df[c].dropna().nunique() == 2]
    multi_cols = [c for c in obj_cols if df[c].dropna().nunique() > 2]
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
    for c in binary_cols:
        df[c] = map_binary_series(df[c].astype(str))

    bool_cols = df.select_dtypes(include=["bool"]).columns.tolist()
    if bool_cols:
        df[bool_cols] = df[bool_cols].astype(int)

    if multi_cols:
        df=pd.get_dummies(df, columns=multi_cols, drop_first=True, dtype=int)

    # Convert nullable integers (Int64) to standard integers for XGBoost
    for c in binary_cols:
        if pd.api.types.is_integer_dtype(df[c]):
            df[c] = df[c].fillna(0).astype(int)

    df.head()
    print(f"Feature engineering completed")

    return df

if __name__ == "__main__":

    df=pd.read_csv(r'Data\processed\processed.csv')
    df_enc=build_features(df)
    print(df_enc.head())