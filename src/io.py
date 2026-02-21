import pandas as pd

def load_data (path):
    """Load a CSV file into a DataFrame."""
    return pd.read_csv(path)

def save_data (df, path):
    """Save a DataFrame to a CSV file."""
    df.to_csv(path, index=False)