import pandas as pd
import os

def data_load(file_path:str) ->pd.DataFrame:
    '''
    Loads csv data into dataframe
    
    Args: file_path which should be string

    Output: pd.DataFrame    Loaded Dataset

    '''
    if not os.path.exists(file_path):
        raise FileNotFoundError (f"File Not Found: {file_path}")
    
    df=pd.read_csv(file_path)
    return df