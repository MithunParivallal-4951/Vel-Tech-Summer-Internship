import argparse
import csv
import math
import pickle
import re
from collections import Counter
from pathlib import Path


DEFAULT_DATASET = (
    "C:/Users/Mithun/OneDrive/Desktop/git hub folder/Vel-Tech-Summer-Internship/"
    "Day 3/16k_Movies-mat-csv.csv"
)

DEFAULT_MODEL_PATH = "movie_recommender.pkl"

DEFAULT_TEXT_COLUMNS = [
    "Description",
    "Genres",
    "Directed by",
    "Written by",
]

STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "with",
}


def tokenize(text):
    words = re.findall(r"[a-z0-9]+", text.lower())
    return [word for word in words if word not in STOP_WORDS]


def cosine_similarity(vector_a, vector_b):
    common_terms = set(vector_a) & set(vector_b)
    dot_product = sum(vector_a[term] * vector_b[term] for term in common_terms)

    magnitude_a = math.sqrt(sum(value * value for value in vector_a.values()))
    magnitude_b = math.sqrt(sum(value * value for value in vector_b.values()))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


class MovieRecommender:
    def __init__(self, csv_path, title_column="Title", text_columns=None):
        self.csv_path = Path(csv_path)
        self.title_column = title_column
        self.text_columns = text_columns or DEFAULT_TEXT_COLUMNS
        self.used_text_columns = []
        self.movies = self._load_movies()
        self.vectors = self._build_tfidf_vectors()

    def save(self, model_path=DEFAULT_MODEL_PATH):
        with Path(model_path).open("wb") as file:
            pickle.dump(self, file)

    @staticmethod
    def load(model_path=DEFAULT_MODEL_PATH):
        with Path(model_path).open("rb") as file:
            return pickle.load(file)

    def _resolve_column(self, wanted_column, available_columns):
        if wanted_column in available_columns:
            return wanted_column

        normalized_columns = {column.lower().strip(): column for column in available_columns}
        return normalized_columns.get(wanted_column.lower().strip())

    def _load_movies(self):
        if not self.csv_path.exists():
            raise FileNotFoundError(f"Dataset not found: {self.csv_path}")

        with self.csv_path.open("r", encoding="utf-8-sig", errors="replace", newline="") as file:
            reader = csv.DictReader(file)
            if not reader.fieldnames:
                raise ValueError("Dataset CSV has no header row.")

            title_column = self._resolve_column(self.title_column, reader.fieldnames)
            if not title_column:
                columns = ", ".join(reader.fieldnames)
                raise ValueError(
                    f"Title column '{self.title_column}' was not found. "
                    f"Available columns: {columns}"
                )

            usable_columns = []
            for column in self.text_columns:
                resolved_column = self._resolve_column(column, reader.fieldnames)
                if resolved_column:
                    usable_columns.append(resolved_column)

            if not usable_columns:
                raise ValueError(
                    "No usable text columns were found. "
                    f"Expected one or more of: {', '.join(self.text_columns)}"
                )

            self.title_column = title_column
            self.used_text_columns = usable_columns

            movies = []
            for row in reader:
                title = row.get(title_column, "").strip()
                if not title:
                    continue

                combined_features = " ".join(row.get(column, "") for column in usable_columns)
                movies.append(
                    {
                        "title": title,
                        "normalized_title": title.lower().strip(),
                        "combined_features": combined_features,
                    }
                )

        if not movies:
            raise ValueError("No movies were loaded. Check that your title column has values.")

        return movies

    def _build_tfidf_vectors(self):
        documents = [tokenize(movie["combined_features"]) for movie in self.movies]
        document_count = len(documents)

        document_frequency = Counter()
        for tokens in documents:
            document_frequency.update(set(tokens))

        vectors = []
        for tokens in documents:
            term_frequency = Counter(tokens)
            total_terms = len(tokens) or 1
            vector = {}

            for term, count in term_frequency.items():
                tf = count / total_terms
                idf = math.log((document_count + 1) / (document_frequency[term] + 1)) + 1
                vector[term] = tf * idf

            vectors.append(vector)

        return vectors

    def search_titles(self, query, limit=10):
        query = query.lower().strip()
        matches = [
            movie["title"]
            for movie in self.movies
            if query in movie["normalized_title"]
        ]
        return matches[:limit]

    def recommend(self, movie_title, limit=10):
        normalized_title = movie_title.lower().strip()
        movie_index = None

        for index, movie in enumerate(self.movies):
            if movie["normalized_title"] == normalized_title:
                movie_index = index
                break

        if movie_index is None:
            suggestions = self.search_titles(movie_title, limit=5)
            raise ValueError(
                f"Movie '{movie_title}' was not found."
                + (f" Did you mean: {', '.join(suggestions)}?" if suggestions else "")
            )

        target_vector = self.vectors[movie_index]
        scores = []
        for index, vector in enumerate(self.vectors):
            if index == movie_index:
                continue
            scores.append((index, cosine_similarity(target_vector, vector)))

        scores.sort(key=lambda item: item[1], reverse=True)

        recommendations = []
        for index, score in scores[:limit]:
            recommendations.append(
                {
                    "title": self.movies[index]["title"],
                    "similarity_score": round(score, 4),
                }
            )

        return recommendations


def main():
    parser = argparse.ArgumentParser(description="Recommend similar movies using cosine similarity.")
    parser.add_argument("movie", help="Movie title to search recommendations for")
    parser.add_argument("--data", default=DEFAULT_DATASET, help="Path to your movie dataset CSV")
    parser.add_argument("--title-column", default="Title", help="Column name containing movie titles")
    parser.add_argument("--limit", type=int, default=10, help="Number of recommendations to show")
    parser.add_argument(
        "--text-columns",
        nargs="+",
        default=DEFAULT_TEXT_COLUMNS,
        help="Text columns used to calculate similarity",
    )
    args = parser.parse_args()

    recommender = MovieRecommender(
        csv_path=args.data,
        title_column=args.title_column,
        text_columns=args.text_columns,
    )

    recommendations = recommender.recommend(args.movie, limit=args.limit)

    print(f"\nRecommendations for: {args.movie}\n")
    for number, movie in enumerate(recommendations, start=1):
        print(f"{number}. {movie['title']}  | score: {movie['similarity_score']}")


if __name__ == "__main__":
    main()
