import pandas as pd
import argparse

from src.data.load import data_load

def main(args):
    print("Loading Data:")
    df= data_load(args.input)
    print(df.head())
    print("Data Loaded Succesfully")
    


if __name__=="__main__":
    p=argparse.ArgumentParser(description='Customer Churn Project')
    p.add_argument('--input', type=str, required=True, help="path to csv")
    args=p.parse_args()
    main(args)

