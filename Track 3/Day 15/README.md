"""
Train the content-based movie recommender and save it as a .pkl file.

This script builds a TF-IDF representation of each movie's genres +
overview, computes a cosine-similarity matrix, and pickles everything
the Flask app needs into:

    model/movie_recommender.pkl

Run this once before starting the Flask app:

    python train_model.py
"""

import os
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "movies.csv")
MODEL_DIR = os.path.join(BASE_DIR, "model")
MODEL_PATH = os.path.join(MODEL_DIR, "movie_recommender.pkl")


def train_and_save(data_path=DATA_PATH, model_path=MODEL_PATH):
    print(f"Loading dataset from: {data_path}")
    df = pd.read_csv(data_path)

    # Combine genres + overview into a single text field for vectorization
    df["combined_features"] = (
        df["genres"].fillna("") + " " + df["overview"].fillna("")
    )

    print("Fitting TF-IDF vectorizer...")
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(df["combined_features"])

    print("Computing cosine similarity matrix...")
    similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Map title (lowercased) -> dataframe index for quick lookup
    indices = pd.Series(df.index, index=df["title"].str.lower()).drop_duplicates()

    model_data = {
        "df": df,
        "similarity_matrix": similarity_matrix,
        "indices": indices,
        "vectorizer": tfidf,
    }

    os.makedirs(MODEL_DIR, exist_ok=True)
    with open(model_path, "wb") as f:
        pickle.dump(model_data, f)

    print(f"Model trained on {len(df)} movies.")
    print(f"Saved model to: {model_path}")


if __name__ == "__main__":
    train_and_save()
