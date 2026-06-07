import pandas as pd
import os
import sys
import argparse

from src.data.load import data_load

def main(args):
    print("Loading Data:")
    df= data_load(args.input)
    print("Data Loaded Succesfully")
    print(df.head())


if __name__=="__main__":
    p=argparse.ArgumentParser(description='Customer Churn Project')
    p.add_argument('--input', type=str, required=True, help="path to csv")
    args=p.parse_args()
    main(args)

