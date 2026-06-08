"""
train_sklearn_grid_search.py
────────────────────────────
Uses scikit-learn's TfidfVectorizer + GridSearchCV-compatible pipeline to find
the best hyperparameters for the movie recommender.

Because this is an unsupervised task (no labels), we use a custom scorer that
measures the average similarity of the top-K results — acting as a proxy for
retrieval quality.

Parameters tuned
----------------
TfidfVectorizer
  - max_features   : vocabulary cap
  - ngram_range    : (1,1) unigrams | (1,2) unigrams+bigrams
  - sublinear_tf   : log-normalised TF
  - min_df         : minimum document frequency
  - analyzer       : 'word' | 'char_wb' (character n-grams)

NearestNeighbors (for fast top-K search)
  - metric         : cosine | euclidean

Usage
-----
    pip install scikit-learn
    python train_sklearn_grid_search.py --data sample_movies.csv
    python train_sklearn_grid_search.py --data sample_movies.csv --save-best
"""

import argparse
import csv
import pickle
import time
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import Pipeline

# ── parameter grid ─────────────────────────────────────────────────────────────
PARAM_GRID = {
    "tfidf__max_features": [500, 1000, None],
    "tfidf__ngram_range":  [(1, 1), (1, 2)],
    "tfidf__sublinear_tf": [False, True],
    "tfidf__min_df":       [1, 2],
    "tfidf__analyzer":     ["word", "char_wb"],
    "nn__metric":          ["cosine", "euclidean"],
}

TEXT_COLUMNS = ["overview", "genres", "director", "cast",
                "Description", "Genres", "Directed by", "Written by"]

# ──────────────────────────────────────────────────────────────────────────────


def load_corpus(csv_path: Path) -> tuple[list[str], list[str]]:
    with csv_path.open("r", encoding="utf-8-sig", errors="replace", newline="") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames or []
        title_col = next((c for c in fields if c.lower().strip() == "title"), None)
        text_cols = [c for c in fields if c in TEXT_COLUMNS or
                     c.lower() in {t.lower() for t in TEXT_COLUMNS}]
        text_cols = [c for c in text_cols if c != title_col]

        titles, docs = [], []
        for row in reader:
            t = row.get(title_col, "").strip()
            if not t:
                continue
            combined = " ".join(row.get(c, "") for c in text_cols)
            titles.append(t)
            docs.append(combined)
    return titles, docs


def build_pipeline(params: dict) -> Pipeline:
    """Build a Pipeline from a flat param dict (sklearn naming convention)."""
    tfidf_params = {k.replace("tfidf__", ""): v
                    for k, v in params.items() if k.startswith("tfidf__")}
    nn_params    = {k.replace("nn__", ""): v
                    for k, v in params.items() if k.startswith("nn__")}

    vectorizer = TfidfVectorizer(**tfidf_params)
    nn = NearestNeighbors(n_neighbors=11, algorithm="brute", **nn_params)
    return Pipeline([("tfidf", vectorizer), ("nn", nn)])


def score_pipeline(pipeline: Pipeline, docs: list[str], top_k: int = 5) -> float:
    """
    Fit the pipeline and compute mean top-K cosine similarity as quality score.
    Higher = the model is more confident in its recommendations.
    """
    X = pipeline.named_steps["tfidf"].fit_transform(docs)
    pipeline.named_steps["nn"].fit(X)

    metric = pipeline.named_steps["nn"].metric
    sample = min(len(docs), 50)
    total  = 0.0

    for i in range(sample):
        distances, indices = pipeline.named_steps["nn"].kneighbors(X[i], n_neighbors=top_k + 1)
        # skip index 0 (self)
        neighbour_dists = distances[0][1:]
        if metric == "cosine":
            sims = 1 - neighbour_dists
        else:
            # convert Euclidean distance to a 0-1 similarity
            sims = 1 / (1 + neighbour_dists)
        total += float(np.mean(sims))

    return total / sample


def grid_search(docs: list[str], param_grid: dict, top_k: int) -> list[dict]:
    import itertools

    keys   = list(param_grid.keys())
    combos = list(itertools.product(*param_grid.values()))
    results = []

    col_w = [12, 8, 7, 8, 7, 8, 9, 8]
    header = (f"{'#':>3}  {'max_feat':>10}  {'ngram':>7}  {'sublin':>6}  "
              f"{'min_df':>6}  {'analyzer':>8}  {'metric':>8}  {'score':>7}  {'time':>5}")
    print(f"\nGrid search: {len(combos)} combinations\n")
    print(header)
    print("-" * len(header))

    for idx, combo in enumerate(combos, 1):
        params = dict(zip(keys, combo))
        t0 = time.perf_counter()

        try:
            pipeline = build_pipeline(params)
            score    = score_pipeline(pipeline, docs, top_k)
        except Exception as e:
            score = -1.0
            print(f"  [skip] {e}")

        elapsed = time.perf_counter() - t0
        results.append({**params, "score": round(score, 4), "elapsed": round(elapsed, 3)})

        mf = str(params["tfidf__max_features"]) if params["tfidf__max_features"] else "None"
        ng = f"{params['tfidf__ngram_range'][0]}-{params['tfidf__ngram_range'][1]}"
        print(f"{idx:>3}  {mf:>10}  {ng:>7}  {str(params['tfidf__sublinear_tf']):>6}  "
              f"{params['tfidf__min_df']:>6}  {params['tfidf__analyzer']:>8}  "
              f"{params['nn__metric']:>8}  {score:>7.4f}  {elapsed:>5.2f}s")

    return results


def print_summary(results: list[dict]) -> dict:
    best = max(results, key=lambda r: r["score"])
    print("\n" + "=" * 70)
    print("BEST CONFIGURATION")
    print("=" * 70)
    for k, v in best.items():
        print(f"  {k:<30}: {v}")
    return best


def save_best_model(titles: list[str], docs: list[str], best_params: dict, path: str):
    pipeline = build_pipeline(best_params)
    X = pipeline.named_steps["tfidf"].fit_transform(docs)
    pipeline.named_steps["nn"].fit(X)

    payload = {
        "titles":   titles,
        "pipeline": pipeline,
        "matrix":   X,
        "params":   best_params,
    }
    with open(path, "wb") as f:
        pickle.dump(payload, f)
    print(f"\nBest model saved → {path}")


# ──────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="sklearn TF-IDF grid search for movie recommender.")
    parser.add_argument("--data",      default="sample_movies.csv")
    parser.add_argument("--limit",     type=int, default=5, help="Top-K for scoring")
    parser.add_argument("--save-best", action="store_true")
    parser.add_argument("--model",     default="best_sklearn_model.pkl")
    args = parser.parse_args()

    csv_path = Path(args.data)
    if not csv_path.exists():
        raise FileNotFoundError(f"Not found: {csv_path}")

    titles, docs = load_corpus(csv_path)
    print(f"Loaded {len(docs)} movies.")

    results = grid_search(docs, PARAM_GRID, args.limit)
    best    = print_summary(results)

    if args.save_best:
        save_best_model(titles, docs, best, args.model)


if __name__ == "__main__":
    main()
