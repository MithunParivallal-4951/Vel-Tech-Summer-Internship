"""
train_random_search.py
──────────────────────
Randomized hyperparameter search for the movie recommender.

Useful when the full grid is too large to enumerate exhaustively.
Samples N random configurations and reports the best.

Additional parameters vs. the grid-search scripts
--------------------------------------------------
TfidfVectorizer
  - max_df        : ignore terms appearing in > X fraction of docs (0.6 – 1.0)
  - norm          : l1 | l2 | None (vector normalisation)

Similarity
  - similarity_fn : cosine (default) | jaccard (on binary vectors)

Usage
-----
    pip install scikit-learn
    python train_random_search.py --data sample_movies.csv --n-iter 30
    python train_random_search.py --data sample_movies.csv --n-iter 50 --save-best
"""

import argparse
import csv
import math
import pickle
import random
import time
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as sk_cosine

# ── parameter distributions ────────────────────────────────────────────────────
PARAM_DISTRIBUTIONS = {
    "max_features": [200, 300, 500, 800, 1000, 2000, None],
    "ngram_range":  [(1, 1), (1, 2), (2, 2)],
    "sublinear_tf": [True, False],
    "min_df":       [1, 2, 3],
    "max_df":       [0.7, 0.85, 1.0],
    "norm":         ["l1", "l2", None],
    "analyzer":     ["word", "char_wb"],
    "similarity_fn":["cosine", "jaccard"],
}

TEXT_COLUMNS = ["overview", "genres", "director", "cast",
                "Description", "Genres", "Directed by", "Written by"]


# ──────────────────────────────────────────────────────────────────────────────

def load_corpus(csv_path: Path):
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


def jaccard_similarity(va: np.ndarray, vb: np.ndarray) -> float:
    """Binary Jaccard on non-zero positions."""
    a_bin = va > 0
    b_bin = vb > 0
    intersection = np.logical_and(a_bin, b_bin).sum()
    union        = np.logical_or(a_bin, b_bin).sum()
    return float(intersection / union) if union else 0.0


def score_matrix(X, similarity_fn: str, top_k: int, sample: int = 50) -> float:
    """Return mean top-K similarity across a sample of documents."""
    n      = X.shape[0]
    sample = min(n, sample)
    total  = 0.0

    if similarity_fn == "cosine":
        sim_matrix = sk_cosine(X)  # (n x n) — fine for small datasets
    else:
        # Jaccard row-by-row (slower, but correct)
        sim_matrix = None

    for i in range(sample):
        if similarity_fn == "cosine":
            row = sim_matrix[i].copy()
        else:
            row = np.array([jaccard_similarity(X[i].toarray().ravel(),
                                               X[j].toarray().ravel())
                             for j in range(n)])

        row[i] = -1          # exclude self
        top_idx = np.argpartition(row, -top_k)[-top_k:]
        total  += float(np.mean(row[top_idx]))

    return total / sample


def sample_params(distributions: dict) -> dict:
    return {k: random.choice(v) for k, v in distributions.items()}


def random_search(docs: list[str], distributions: dict,
                  n_iter: int, top_k: int, seed: int) -> list[dict]:
    random.seed(seed)
    results = []

    print(f"\nRandomized search: {n_iter} iterations  (seed={seed})\n")
    header = (f"{'#':>3}  {'mf':>5}  {'ng':>5}  {'sub':>5}  {'mdf':>4}  "
              f"{'MDF':>4}  {'norm':>4}  {'anl':>7}  {'sim':>7}  {'score':>7}  {'t':>5}")
    print(header)
    print("-" * len(header))

    for idx in range(1, n_iter + 1):
        params = sample_params(distributions)
        t0     = time.perf_counter()

        try:
            vectorizer = TfidfVectorizer(
                max_features = params["max_features"],
                ngram_range  = params["ngram_range"],
                sublinear_tf = params["sublinear_tf"],
                min_df       = params["min_df"],
                max_df       = params["max_df"],
                norm         = params["norm"],
                analyzer     = params["analyzer"],
            )
            X = vectorizer.fit_transform(docs)

            # skip if vocabulary is empty
            if X.shape[1] == 0:
                continue

            score = score_matrix(X, params["similarity_fn"], top_k)
        except Exception as e:
            score = -1.0

        elapsed = time.perf_counter() - t0
        results.append({**params, "score": round(score, 4), "elapsed": round(elapsed, 3),
                        "vocab_size": X.shape[1] if score >= 0 else 0})

        mf  = str(params["max_features"]) if params["max_features"] else "None"
        ng  = f"{params['ngram_range'][0]},{params['ngram_range'][1]}"
        print(f"{idx:>3}  {mf:>5}  {ng:>5}  {str(params['sublinear_tf'])[0]:>5}  "
              f"{params['min_df']:>4}  {params['max_df']:>4}  "
              f"{str(params['norm']):>4}  {params['analyzer']:>7}  "
              f"{params['similarity_fn']:>7}  {score:>7.4f}  {elapsed:>5.2f}s")

    return results


def print_summary(results: list[dict]) -> dict:
    valid = [r for r in results if r["score"] >= 0]
    if not valid:
        print("No valid configurations found.")
        return {}

    best = max(valid, key=lambda r: r["score"])
    worst = min(valid, key=lambda r: r["score"])

    print("\n" + "=" * 65)
    print(f"BEST  score={best['score']:.4f}")
    for k, v in best.items():
        print(f"  {k:<20}: {v}")
    print(f"\nWORST score={worst['score']:.4f}")
    for k, v in worst.items():
        print(f"  {k:<20}: {v}")

    scores = [r["score"] for r in valid]
    print(f"\nStats over {len(valid)} valid runs:")
    print(f"  mean  : {sum(scores)/len(scores):.4f}")
    print(f"  max   : {max(scores):.4f}")
    print(f"  min   : {min(scores):.4f}")
    return best


def save_best_model(titles, docs, best_params, path):
    vectorizer = TfidfVectorizer(
        max_features = best_params["max_features"],
        ngram_range  = best_params["ngram_range"],
        sublinear_tf = best_params["sublinear_tf"],
        min_df       = best_params["min_df"],
        max_df       = best_params["max_df"],
        norm         = best_params["norm"],
        analyzer     = best_params["analyzer"],
    )
    X = vectorizer.fit_transform(docs)
    payload = {
        "titles":      titles,
        "vectorizer":  vectorizer,
        "matrix":      X,
        "sim_fn":      best_params["similarity_fn"],
        "params":      best_params,
    }
    with open(path, "wb") as f:
        pickle.dump(payload, f)
    print(f"\nBest model saved → {path}")


# ──────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data",      default="sample_movies.csv")
    parser.add_argument("--n-iter",    type=int, default=20,   help="Number of random trials")
    parser.add_argument("--limit",     type=int, default=5,    help="Top-K for scoring")
    parser.add_argument("--seed",      type=int, default=42)
    parser.add_argument("--save-best", action="store_true")
    parser.add_argument("--model",     default="best_random_model.pkl")
    args = parser.parse_args()

    csv_path = Path(args.data)
    if not csv_path.exists():
        raise FileNotFoundError(f"Not found: {csv_path}")

    titles, docs = load_corpus(csv_path)
    print(f"Loaded {len(docs)} movies.")

    results = random_search(docs, PARAM_DISTRIBUTIONS, args.n_iter, args.limit, args.seed)
    best    = print_summary(results)

    if args.save_best and best:
        save_best_model(titles, docs, best, args.model)


if __name__ == "__main__":
    main()
