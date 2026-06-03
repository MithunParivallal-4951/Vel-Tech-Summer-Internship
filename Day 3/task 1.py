from pathlib import Path
import pandas as pd

csv_path = Path(__file__).resolve().parent / 'student-mat.csv'
df = pd.read_csv(csv_path, sep=';')

print("Shape:", df.shape)
print("\nColumns:", list(df.columns))
print("\nFirst 3 rows:\n", df.head(3))
print("\nLast 3 rows:\n", df.tail(3))
print("\nInternet access counts:\n", df['internet'].value_counts())
