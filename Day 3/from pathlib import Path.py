from pathlib import Path
import pandas as pd

csv_path = Path(__file__).resolve().parent / 'student-mat.csv'
df = pd.read_csv(csv_path, sep=';')

print("===== Avg G3 by Study Time =====")
print(df.groupby('studytime')['G3'].mean().round(2))

print("\n===== Avg G3 by Sex =====")
print(df.groupby('sex')['G3'].mean().round(2))

print("\n===== Top 5 Students by G3 =====")
top5 = df.nlargest(5, 'G3')[['G1', 'G2', 'G3', 'studytime', 'absences']]
print(top5)