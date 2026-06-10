"""
generate_similarity_matrix.py
───────────────────────────────
Builds and saves the full cosine similarity matrix for all 16,290 movies.

Approach
--------
Pure-Python dict-based cosine similarity across 16k x 16k pairs would take
~26 minutes. Instead we:
  1. Convert all TF-IDF vectors into a sparse scipy matrix (takes ~1.5s)
  2. Use sklearn's vectorised cosine_similarity on the full matrix (~1 min)
  3. For each movie, extract and store only the top-K neighbours (saves memory)
  4. Save as similarity_matrix.pkl in models/

Output format
-------------
similarity_matrix.pkl contains a list of 16,290 dicts:
[
  {
    'movie_index': 0,
    'title':       'The Godfather',
    'top_k': [
      {'index': 123, 'title': 'The Godfather: Part II', 'score': 0.5329},
      {'index': 456, 'title': 'The Rainmaker',           'score': 0.4474},
      ...   (up to TOP_K entries)
    ]
  },
  ...
]

Usage after saving
------------------
  import pickle
  with open('models/similarity_matrix.pkl', 'rb') as f:
      sim = pickle.load(f)

  # Get top recommendations for movie at index 0
  print(sim[0]['title'])
  for rec in sim[0]['top_k']:
      print(rec['title'], rec['score'])

Run
---
    pip install scikit-learn numpy scipy
    python generate_similarity_matrix.py
"""

import math
import os
import pathlib
import pickle
import time

import numpy as np
from scipy.sparse import lil_matrix
from sklearn.metrics.pairwise import cosine_similarity as sk_cosine

# ── patch Windows path ────────────────────────────────────────────────────────
pathlib.WindowsPath = pathlib.PurePosixPath

MODEL_PATH = "movie_recommender.pkl"
OUTPUT_DIR = "models"
OUTPUT_PKL = os.path.join(OUTPUT_DIR, "similarity_matrix.pkl")
TOP_K      = 10     # how many neighbours to store per movie


# ══════════════════════════════════════════════════════════════════════════════
#  Step 1 — Load model
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 65)
print("  Similarity Matrix Generator — Movie Recommender")
print("  Mithun · Day 10 · InnoTrack 2025")
print("=" * 65)

print(f"\n[1/5] Loading model from '{MODEL_PATH}' ...")
t_start = time.perf_counter()

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

n         = len(model.movies)
print(f"      ✔  {n:,} movies loaded")
print(f"      ✔  Feature columns: {model.used_text_columns}")

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ══════════════════════════════════════════════════════════════════════════════
#  Step 2 — Build vocabulary index (term → column index in sparse matrix)
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n[2/5] Building vocabulary index ...")
t0 = time.perf_counter()

term_to_idx = {}
for vector in model.vectors:
    for term in vector:
        if term not in term_to_idx:
            term_to_idx[term] = len(term_to_idx)

vocab_size = len(term_to_idx)
print(f"      ✔  Vocabulary size: {vocab_size:,} unique terms")
print(f"      ✔  Done in {time.perf_counter() - t0:.2f}s")


# ══════════════════════════════════════════════════════════════════════════════
#  Step 3 — Build sparse TF-IDF matrix  (n_movies × vocab_size)
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n[3/5] Building sparse TF-IDF matrix ({n:,} × {vocab_size:,}) ...")
t0 = time.perf_counter()

sparse_mat = lil_matrix((n, vocab_size), dtype=np.float32)

for i, vector in enumerate(model.vectors):
    for term, weight in vector.items():
        sparse_mat[i, term_to_idx[term]] = weight
    if (i + 1) % 2000 == 0:
        print(f"      ... {i+1:,}/{n:,} rows filled")

sparse_csr = sparse_mat.tocsr()   # convert to CSR format for fast math
print(f"      ✔  Matrix shape : {sparse_csr.shape}")
print(f"      ✔  Non-zero entries: {sparse_csr.nnz:,}")
print(f"      ✔  Built in {time.perf_counter() - t0:.2f}s")


# ══════════════════════════════════════════════════════════════════════════════
#  Step 4 — Compute full cosine similarity matrix in chunks
#  We process in chunks of CHUNK_SIZE rows to avoid loading 16k×16k floats
#  all at once (that would be ~2 GB). Each chunk produces a (chunk × n) block.
# ══════════════════════════════════════════════════════════════════════════════

CHUNK_SIZE = 500   # rows per chunk — adjust down if you get MemoryError

print(f"\n[4/5] Computing cosine similarity in chunks of {CHUNK_SIZE} rows ...")
print(f"      Total chunks: {math.ceil(n / CHUNK_SIZE)}")
t0 = time.perf_counter()

similarity_matrix = []   # will hold one dict per movie

for chunk_start in range(0, n, CHUNK_SIZE):
    chunk_end  = min(chunk_start + CHUNK_SIZE, n)
    chunk_rows = sparse_csr[chunk_start:chunk_end]

    # Cosine similarity between this chunk and ALL movies: shape = (chunk, n)
    sim_block = sk_cosine(chunk_rows, sparse_csr)   # returns numpy array

    # For each row in the chunk, find top-K neighbours (excluding self)
    for local_i, global_i in enumerate(range(chunk_start, chunk_end)):
        row = sim_block[local_i]       # shape (n,)
        row[global_i] = -1.0           # exclude self

        # argsort descending — take top K
        top_indices = np.argpartition(row, -TOP_K)[-TOP_K:]
        top_indices = top_indices[np.argsort(row[top_indices])[::-1]]

        top_k_list = [
            {
                "index": int(idx),
                "title": model.movies[int(idx)]["title"],
                "score": round(float(row[idx]), 4),
            }
            for idx in top_indices
        ]

        similarity_matrix.append({
            "movie_index": global_i,
            "title":       model.movies[global_i]["title"],
            "top_k":       top_k_list,
        })

    elapsed = time.perf_counter() - t0
    done    = chunk_end / n
    eta     = (elapsed / done) * (1 - done) if done > 0 else 0
    print(f"      chunk {chunk_end//CHUNK_SIZE:>3}/{math.ceil(n/CHUNK_SIZE)}  "
          f"({chunk_end:>5}/{n:,} movies)  "
          f"elapsed={elapsed:.1f}s  ETA={eta:.0f}s")

total_time = time.perf_counter() - t0
print(f"\n      ✔  All {n:,} movies processed in {total_time:.1f}s")


# ══════════════════════════════════════════════════════════════════════════════
#  Step 5 — Save similarity_matrix.pkl
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n[5/5] Saving similarity matrix to '{OUTPUT_PKL}' ...")
t0 = time.perf_counter()

with open(OUTPUT_PKL, "wb") as f:
    pickle.dump(similarity_matrix, f)

size_mb = os.path.getsize(OUTPUT_PKL) / (1024 * 1024)
print(f"      ✔  Saved in {time.perf_counter() - t0:.2f}s")
print(f"      ✔  File size: {size_mb:.1f} MB")


# ══════════════════════════════════════════════════════════════════════════════
#  Verification — load fresh and spot-check
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'─'*65}")
print("  VERIFICATION — Loading matrix fresh and spot-checking")
print(f"{'─'*65}")

with open(OUTPUT_PKL, "rb") as f:
    loaded_sim = pickle.load(f)

print(f"\n  Total entries : {len(loaded_sim):,}")
print(f"  Top-K per movie: {len(loaded_sim[0]['top_k'])}")

# Spot-check 5 well-known movies
spot_check_titles = [
    "The Godfather",
    "Pulp Fiction",
    "Spirited Away",
    "Inception",
    "Goodfellas",
]

print(f"\n  {'Movie':<30} {'Top Recommendation':<35} {'Score':>6}")
print(f"  {'─'*29}  {'─'*34}  {'─'*6}")

for title in spot_check_titles:
    norm  = title.lower().strip()
    entry = next(
        (e for e in loaded_sim if model.movies[e["movie_index"]]["normalized_title"] == norm),
        None
    )
    if entry and entry["top_k"]:
        top = entry["top_k"][0]
        print(f"  {title:<30} {top['title']:<35} {top['score']:>6.4f}")
    else:
        print(f"  {title:<30} {'NOT FOUND':<35}")


# ══════════════════════════════════════════════════════════════════════════════
#  Quick-lookup helper function (for Flask / predict())
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'─'*65}")
print("  HOW TO USE similarity_matrix.pkl IN YOUR FLASK APP")
print(f"{'─'*65}")
print("""
  import pickle

  # Load once at app startup
  with open('models/similarity_matrix.pkl', 'rb') as f:
      sim_matrix = pickle.load(f)

  # Build a title → index lookup dict for fast access
  title_to_idx = {e['title'].lower(): e['movie_index'] for e in sim_matrix}

  def get_recommendations(movie_title: str, top_k: int = 5):
      idx   = title_to_idx.get(movie_title.lower())
      if idx is None:
          return []
      entry = sim_matrix[idx]
      return entry['top_k'][:top_k]

  # Example
  recs = get_recommendations('The Godfather', top_k=5)
  for r in recs:
      print(r['title'], r['score'])
""")

print(f"{'='*65}")
print(f"  Total time: {time.perf_counter() - t_start:.1f}s")
print(f"  similarity_matrix.pkl saved → {OUTPUT_PKL}")
print(f"  ✔  Complete — matrix is ready for Flask / M3 handoff")
print(f"{'='*65}\n")
