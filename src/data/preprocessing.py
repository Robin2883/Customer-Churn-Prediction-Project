import pandas as pd

def pre_process(df:pd.DataFrame, target_column:str= "Churn" ):
    print("Pre-processing the dataset:")

    #stripping whitespaces in the columns
    df.columns=df.columns.str.strip()
    
    #dropping ID columns
    for col in ["customerID", "CustomerID", "customer_id"]:
        if col in df.columns:
            df = df.drop(columns=[col])

    #total_charges must not be blank
    if 'TotalCharges' in df.columns:
        df['TotalCharges']=pd.to_numeric(df['TotalCharges'], errors='coerce')

    #label enccoding the target column
    df[target_column]=df[target_column].str.strip().map({"Yes": 1, "No": 0})

    #seniorCitizen values should be 0/1 if present
    if 'SeniorCitizen' in df.columns:
        df['SeniorCitizen']=df['SeniorCitizen'].fillna(0).astype(int)

    #numeric columns: fill with 0
    num_columns= df.select_dtypes(include='number').columns
    df[num_columns]=df[num_columns].fillna(0)

    print("Pre-processing completed")

    return df