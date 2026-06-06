import pandas as pd

# Replace 'your_file.csv' with the exact name of your uploaded file
df = pd.read_csv('/16k_Movies-mat.csv.csv')
df.head()
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import re

# Load the dataset
try:
    df = pd.read_csv('/content/drive/MyDrive/CineProphet/16k_Movies-mat.csv.csv', encoding='latin-1')
except FileNotFoundError:
    print("Error: 16k_Movies-mat.csv.csv not found. Please upload the file or provide the correct path.")
    # Create a dummy DataFrame for demonstration if the file is not found
    data = {
        'Title':               ['Avatar', 'Titanic', 'Inception', 'The Dark Knight', 'Interstellar'],
        'Release Date':        ['2009', '1997', '2010', '2008', '2014'],
        'Description':         ['A marine on an alien planet.', 'A love story on a ship.',
                                'A thief who enters dreams.', 'Batman fights the Joker.',
                                'Astronauts travel through a wormhole.'],
        'Rating':              [7.8, 7.9, 8.8, 9.0, 8.6],
        'No of Persons Voted': [1200000, 1100000, 2200000, 2500000, 1600000],
        'Directed by':         ['James Cameron', 'James Cameron', 'Christopher Nolan',
                                'Christopher Nolan', 'Christopher Nolan'],
        'Written by':          ['James Cameron', 'James Cameron', 'Christopher Nolan',
                                'Jonathan Nolan', 'Jonathan Nolan'],
        'Duration':            ['2 h 42 m', '3 h 14 m', '2 h 28 m', '2 h 32 m', '2 h 49 m'],
        'Genres':              ['Action,Adventure,Fantasy', 'Drama,Romance',
                                'Action,Thriller,Science Fiction', 'Action,Crime,Drama',
                                'Adventure,Drama,Science Fiction'],
    }
    df = pd.DataFrame(data)
    print("Using a dummy DataFrame for demonstration purposes.")

# Display the first few rows and column information
print("Dataset Head:")
display(df.head())
print("\nDataset Info:")
df.info()
# Drop unnamed index column if present
df.drop(columns=['Unnamed: 0'], inplace=True, errors='ignore')

# Check for missing values
print("Missing values before dropping:")
display(df.isnull().sum())

# Drop rows with missing Description or Genres (needed for tags)
df.dropna(subset=['Description', 'Genres', 'Directed by'], inplace=True)

print("\nMissing values after dropping:")
display(df.isnull().sum())

print(f"\nDataset shape after cleaning: {df.shape}")
display(df.head())
# Parse Duration string (e.g. "2 h 28 m") → total minutes as a string token
def parse_duration_token(d):
    if pd.isna(d):
        return ""
    h = re.search(r'(\d+)\s*h', str(d))
    m = re.search(r'(\d+)\s*m', str(d))
    total = 0
    if h: total += int(h.group(1)) * 60
    if m: total += int(m.group(1))
    # Convert to a duration bucket token
    if total <= 90:   return "shortfilm"
    if total <= 120:  return "mediumfilm"
    if total <= 150:  return "longfilm"
    return "epicfilm"

# Clean names — remove spaces so they become single tokens
# e.g. "Christopher Nolan" → "ChristopherNolan"
def clean_name(name):
    if pd.isna(name):
        return ""
    return str(name).strip().replace(" ", "")

# Parse Genres — split by comma, clean spaces
def parse_genres(g):
    if pd.isna(g):
        return ""
    return " ".join([x.strip().replace(" ", "") for x in str(g).split(",")])

# Apply all transformations
df['tags_genres']    = df['Genres'].apply(parse_genres)
df['tags_director']  = df['Directed by'].apply(clean_name)
df['tags_writer']    = df['Written by'].apply(clean_name)
df['tags_duration']  = df['Duration'].apply(parse_duration_token)
df['tags_overview']  = df['Description'].fillna("")

print("Parsed feature columns sample:")
display(df[['Title', 'tags_genres', 'tags_director', 'tags_duration']].head())
# Recommendation function — returns top 5 similar movies with scores
def recommend(movie_title):
    movie_title = movie_title.strip().lower()
    titles_lower = df_final['Title'].str.lower()

    if movie_title not in titles_lower.values:
        print(f"'{movie_title}' not found in dataset.")
        return

    idx = titles_lower[titles_lower == movie_title].index[0]
    scores = list(enumerate(similarity[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:6]

    print(f"\nTop 5 movies similar to '{df_final['Title'][idx]}':\n")
    print(f"{'Rank':<6} {'Title':<40} {'Similarity'}")
    print("-" * 60)
    for rank, (i, score) in enumerate(scores, 1):
        print(f"{rank:<6} {df_final['Title'][i]:<40} {score:.4f}")

# Test the recommendation function
recommend("Inception")
recommend("The Dark Knight")
"""
predict.py  —  Load trained model and get recommendations
===========================================================
Run  : python predict.py
Requires the 3 .pkl files produced by train.py
"""

import pandas as pd
import numpy as np
import joblib
from sklearn.metrics.pairwise import cosine_similarity

# ─────────────────────────────────────────────
# LOAD TRAINED ARTIFACTS
# ─────────────────────────────────────────────
print("Loading trained model...")

tfidf   = joblib.load("tfidf_vectorizer.pkl")
matrix  = joblib.load("tfidf_matrix.pkl")
df      = pd.read_pickle("movies_df.pkl")

print(f"✓ Model loaded | {len(df):,} movies\n")

# Build title → index lookup
indices = (
    pd.Series(df.index, index=df["Title_clean"].str.lower())
    .drop_duplicates()
)


# ─────────────────────────────────────────────
# RECOMMENDER
# ─────────────────────────────────────────────
def recommend(title: str, n: int = 10) -> pd.DataFrame:
    key = title.lower().strip()

    if key not in indices:
        matches = [t for t in indices.index if key in t]
        if not matches:
            print(f"[✗] '{title}' not found.")
            return pd.DataFrame()
        key = matches[0]
        print(f"[~] Closest match: '{key}'")

    idx         = indices[key]
    sim_scores  = cosine_similarity(matrix[idx], matrix).flatten()
    sim_scores[idx] = 0

    top_idx     = np.argsort(sim_scores)[::-1][:n]
    results     = df.iloc[top_idx][["Title", "Genres", "Rating", "Directed by", "Release Date"]].copy()
    results["Similarity"] = sim_scores[top_idx].round(4)
    results = results.reset_index(drop=True)
    results.index += 1
    return results


# ─────────────────────────────────────────────
# INTERACTIVE LOOP
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("  Movie Recommender  (type 'quit' to exit)")
    print("=" * 55)

    while True:
        title = input("\nEnter movie title: ").strip()
        if title.lower() in ("quit", "exit", "q"):
            break
        n = input("How many recommendations? [default 10]: ").strip()
        n = int(n) if n.isdigit() else 10
        results = recommend(title, n)
        if not results.empty:
            print(f"\n{results.to_string()}")
