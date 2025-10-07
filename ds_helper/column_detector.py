# column_detector.py

import pandas as pd
import numpy as np

def detect_column_types(df: pd.DataFrame, unique_threshold: int = 20):
    """
    Automatically detects categorical, numerical, and text columns.

    Parameters:
        df (pd.DataFrame): Input DataFrame
        unique_threshold (int): Max number of unique values to treat numeric columns as categorical

    Returns:
        dict: Dictionary with keys 'categorical', 'numerical', 'text' and list of column names
    """
    
    categorical_cols = []
    numerical_cols = []
    text_cols = []

    for col in df.columns:
        series = df[col]
        dtype = series.dtype

        # 1. Handle Object/String columns
        if dtype == 'object' or pd.api.types.is_string_dtype(series):
            avg_word_len = series.dropna().astype(str).apply(lambda x: len(x.split())).mean()
            
            # If many words per entry → treat as text
            if avg_word_len > 2:
                text_cols.append(col)
            else:
                categorical_cols.append(col)

        # 2. Handle Numeric columns
        elif pd.api.types.is_numeric_dtype(series):
            unique_vals = series.nunique(dropna=True)

            # If unique values are few → treat as categorical (e.g. ZIP codes)
            if unique_vals < unique_threshold:
                categorical_cols.append(col)
            else:
                numerical_cols.append(col)

        # 3. Handle Other data types (e.g., datetime)
        else:
            categorical_cols.append(col)

    return {
        "categorical": categorical_cols,
        "numerical": numerical_cols,
        "text": text_cols
    }


# Example usage:
if __name__ == "__main__":
    data = {
        "Age": [21, 22, 23, 24, 25],
        "Gender": ["Male", "Female", "Female", "Male", "Male"],
        "ZIP": [560001, 560002, 560001, 560003, 560001],
        "Feedback": ["Very good", "Excellent", "Average", "Very bad", "Good"]
    }
    
    df = pd.DataFrame(data)
    result = detect_column_types(df)
    print("Detected Columns:")
    print(result)
