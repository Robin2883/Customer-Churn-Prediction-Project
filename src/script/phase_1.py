import pandas as pd
import argparse

from src.data.load import data_load
from src.utils.validate import validate_data
from src.data.preprocessing import pre_process
from src.features.build_features import build_features

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


    


if __name__=="__main__":
    p=argparse.ArgumentParser(description='Customer Churn Project')
    p.add_argument('--input', type=str, required=True, help="path to csv")
    p.add_argument("--target", type=str, default="Churn")
    args=p.parse_args()
    main(args)

