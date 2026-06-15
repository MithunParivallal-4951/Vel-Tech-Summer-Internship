"""
Content-based movie recommender.

Loads a pre-trained TF-IDF + cosine-similarity model from a pickle file
(model/movie_recommender.pkl). If the pickle doesn't exist yet, it trains
the model on the fly from data/movies.csv and saves it for next time.

Each result also includes:
  - poster_url: a real poster image URL fetched from TMDB (if
    TMDB_API_KEY is configured), or "" if unavailable.
  - poster_emoji / poster_gradient: a genre-themed emoji + color
    gradient used as a fallback "poster" card when poster_url is empty.
"""

import os
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from model.posters import get_poster_url, prefetch_posters

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "movies.csv")
MODEL_PATH = os.path.join(BASE_DIR, "movie_recommender.pkl")


# Simple genre -> (emoji, gradient) theme used to render a "poster" for
# each movie card without needing real poster image files.
GENRE_THEMES = {
    "action":      ("🎬", "#9b2330", "#3a0f12"),
    "adventure":   ("🧭", "#1f6f5c", "#0c2b24"),
    "animation":   ("🎨", "#d8a94e", "#5a3d12"),
    "biography":   ("📜", "#7a6a53", "#2c2419"),
    "comedy":      ("😂", "#e2b53c", "#5a4310"),
    "crime":       ("🕵️", "#4a4a52", "#1a1a1f"),
    "drama":       ("🎭", "#8a3b5a", "#2d1420"),
    "family":      ("👨‍👩‍👧", "#4f8a8b", "#162e2e"),
    "fantasy":     ("🐉", "#6a4fa3", "#241a3a"),
    "history":     ("🏛️", "#9c8255", "#33291a"),
    "horror":      ("👻", "#3b2b3c", "#0e0a10"),
    "music":       ("🎵", "#c9558a", "#3a1726"),
    "mystery":     ("🔎", "#3f4e6b", "#141a26"),
    "romance":     ("❤️", "#b3445c", "#3a151c"),
    "sci-fi":      ("🚀", "#2f6f9e", "#0e2433"),
    "thriller":    ("🔪", "#5a2a2a", "#1e0e0e"),
    "war":         ("⚔️", "#5e5e3a", "#1f1f12"),
}
DEFAULT_THEME = ("🎞️", "#6a6a73", "#1c1c20")


def _poster_theme(genres):
    """Pick a poster emoji/gradient based on the first recognized genre."""
    if not genres:
        return DEFAULT_THEME
    for token in str(genres).replace("|", " ").split():
        theme = GENRE_THEMES.get(token.strip().lower())
        if theme:
            return theme
    return DEFAULT_THEME


class MovieRecommender:
    def __init__(self, data_path=DATA_PATH, model_path=MODEL_PATH):
        self.data_path = data_path
        self.model_path = model_path
        self.df = None
        self.similarity_matrix = None
        self.indices = None
        self.model_source = None
        self._load()
        prefetch_posters(self.df["title"].tolist())

    def _load(self):
        """Load the pickled model if it exists, otherwise train + cache it."""
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, "rb") as f:
                    model_data = pickle.load(f)
                self.df = model_data["df"]
                self.similarity_matrix = model_data["similarity_matrix"]
                self.indices = model_data["indices"]
                self.model_source = "movie_recommender.pkl"
                return
            except Exception:
                # Fall back to training if the pickle is missing/corrupt
                pass

        self._train_and_cache()
        self.model_source = "trained on startup (no .pkl found)"

    def _train_and_cache(self):
        """Train the TF-IDF + cosine-similarity model and save it as .pkl."""
        self.df = pd.read_csv(self.data_path)

        self.df["combined_features"] = (
            self.df["genres"].fillna("") + " " + self.df["overview"].fillna("")
        )

        tfidf = TfidfVectorizer(stop_words="english")
        tfidf_matrix = tfidf.fit_transform(self.df["combined_features"])

        self.similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

        self.indices = pd.Series(
            self.df.index, index=self.df["title"].str.lower()
        ).drop_duplicates()

        try:
            with open(self.model_path, "wb") as f:
                pickle.dump(
                    {
                        "df": self.df,
                        "similarity_matrix": self.similarity_matrix,
                        "indices": self.indices,
                        "vectorizer": tfidf,
                    },
                    f,
                )
        except OSError:
            # If we can't write the pickle (e.g. read-only filesystem),
            # just continue with the in-memory model.
            pass

    def get_all_titles(self):
        """Return a list of all movie titles in the dataset."""
        return self.df["title"].tolist()

    def get_featured(self, n=8):
        """Return a small set of movies (with poster themes) for the
        'Now Showing' grid on the home page."""
        sample = self.df.sample(n=min(n, len(self.df)), random_state=None)
        featured = []
        for _, row in sample.iterrows():
            emoji, color_start, color_end = _poster_theme(row["genres"])
            featured.append(
                {
                    "movieId": int(row["movieId"]),
                    "title": row["title"],
                    "genres": row["genres"],
                    "poster_emoji": emoji,
                    "poster_gradient": [color_start, color_end],
                    "poster_url": get_poster_url(row["title"]),
                }
            )
        return featured

    def recommend(self, title, top_n=5):
        """
        Return a list of recommended movies similar to `title`.

        Each item is a dict with: movieId, title, genres, score (0-1),
        confidence (0-100), poster_emoji, poster_gradient.
        Raises ValueError if the title is not found.
        """
        key = title.strip().lower()
        if key not in self.indices:
            raise ValueError(f"Movie '{title}' not found in dataset.")

        idx = self.indices[key]

        # Get similarity scores for this movie against all others
        scores = list(enumerate(self.similarity_matrix[idx]))

        # Sort by similarity score, descending, skipping the movie itself
        scores = sorted(scores, key=lambda x: x[1], reverse=True)
        scores = [s for s in scores if s[0] != idx][:top_n]

        results = []
        for movie_idx, score in scores:
            row = self.df.iloc[movie_idx]
            emoji, color_start, color_end = _poster_theme(row["genres"])
            results.append(
                {
                    "movieId": int(row["movieId"]),
                    "title": row["title"],
                    "genres": row["genres"],
                    "score": round(float(score), 4),
                    "confidence": round(float(score) * 100, 1),
                    "poster_emoji": emoji,
                    "poster_gradient": [color_start, color_end],
                    "poster_url": get_poster_url(row["title"]),
                }
            )
        return results

    def search_titles(self, query, limit=10):
        """Return titles that contain the query string (case-insensitive)."""
        query = query.strip().lower()
        matches = self.df[self.df["title"].str.lower().str.contains(query)]
        return matches["title"].head(limit).tolist()


# Singleton instance used by the Flask app
recommender = MovieRecommender()
