import pandas as pd
import os

# Try to load a CSV named 'movies.csv' in the current directory
if os.path.exists('movies.csv'):
	df = pd.read_csv('movies.csv')
else:

	df = pd.DataFrame()

print(df.info())

print(df.describe())

print(df.isnull().sum())

if "Genres" in df.columns:
	print(df["Genres"].value_counts().head(10))
else:
	print("Column 'Genres' not found")

if "Directed by" in df.columns:
	print(df["Directed by"].value_counts().head(10))
else:
	print("Column 'Directed by' not found")

