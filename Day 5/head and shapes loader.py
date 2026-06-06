import pandas as pd

df = pd.read_csv("1780635721858_16k_Movies-mat_csv.csv")

print("=" * 50)
print("SHAPE")
print("=" * 50)
print(f"Rows    : {df.shape[0]:,}")
print(f"Columns : {df.shape[1]}")

print("\n" + "=" * 50)
print("HEAD (first 5 rows)")
print("=" * 50)
print(df.head())

print("\n" + "=" * 50)
print("DATA TYPES")
print("=" * 50)
print(df.dtypes)

print("\n" + "=" * 50)
print("NULL VALUES PER COLUMN")
print("=" * 50)
print(df.isnull().sum())
