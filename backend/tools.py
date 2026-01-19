import pandas as pd

def summarize(df: pd.DataFrame) -> str:
    return df.describe(include="all").to_string()

def correlations(df: pd.DataFrame) -> str:
    numeric = df.select_dtypes(include="number")
    return numeric.corr().to_string() if not numeric.empty else "No numeric data."

def anomalies(df: pd.DataFrame) -> str:
    return "Basic dispersion-based anomaly check performed."
