import pandas as pd


def load_parquet_dataset(path: str) -> pd.DataFrame:
    return pd.read_parquet(path)