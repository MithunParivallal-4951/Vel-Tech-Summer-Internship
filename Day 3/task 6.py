from pathlib import Path
import pandas as pd

def eda_report(df, name="Dataset"):
    print(f"\n{'='*40}")
    print(f"EDA Report: {name}")
    print(f"{'='*40}")
    print(f"Shape: {df.shape}")
    print(f"\nNull values:\n{df.isnull().sum()}")
    print(f"\nNumeric summary:\n{df.describe().round(2)}")
    for col in df.select_dtypes(include='object').columns:
        print(f"\nValue counts — {col}:\n{df[col].value_counts()}")

csv_path = Path(__file__).resolve().parent / 'student-mat.csv'
df1 = pd.read_csv(csv_path, sep=';')
eda_report(df1, "Student Math")
