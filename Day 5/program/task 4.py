from pathlib import Path
import pandas as pd

csv_path = Path(__file__).resolve().parent / 'student-mat.csv'
df = pd.read_csv(csv_path, sep=';')

print("Nulls before:\n", df.isnull().sum())

for col in df.select_dtypes(include='number').columns:
    df[col] = df[col].fillna(df[col].mean())

for col in df.select_dtypes(include='object').columns:
    df[col] = df[col].fillna('Unknown')

print("\nNulls after:\n", df.isnull().sum())
print("\nAll nulls cleared!" if df.isnull().sum().sum() == 0 else "Some nulls remain.")
