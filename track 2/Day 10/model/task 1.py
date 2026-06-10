"""
task1_save_pkl_files.py
────────────────────────
Day 10 · Task 1 — Consolidate and Name All Final .pkl Files
Movie Recommender · Mithun · InnoTrack 2025

Saves three files the Flask developer will need:
  final_model.pkl       — the full trained MovieRecommender object
  similarity_matrix.pkl — pre-computed cosine similarity matrix (top-K per movie)
  movies_list.pkl       — list of all movie dicts (title, normalized_title)

Then verifies every file loads correctly in a fresh variable.

Run:
    python task1_save_pkl_files.py
"""

import math
import os
import pathlib
import pickle

# ── patch Windows path so model loads on Linux / Mac ─────────────────────────
pathlib.WindowsPath = pathlib.PurePosixPath

SOURCE_MODEL = "movie_recommender.pkl"
MODELS_DIR   = "models"
TOP_K        = 10        # how many neighbours to store per movie in the matrix


# ══════════════════════════════════════════════════════════════════════════════
#  Helper
# ══════════════════════════════════════════════════════════════════════════════

def cosine_similarity(va: dict, vb: dict) -> float:
    common = set(va) & set(vb)
    dot    = sum(va[t] * vb[t] for t in common)
    mag_a  = math.sqrt(sum(v * v for v in va.values()))
    mag_b  = math.sqrt(sum(v * v for v in vb.values()))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


# ══════════════════════════════════════════════════════════════════════════════
#  Step 1 — Load source model
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 60)
print("  Task 1 — Save & Verify All .pkl Files")
print("=" * 60)

print(f"\n[1/5] Loading source model from '{SOURCE_MODEL}' ...")
with open(SOURCE_MODEL, "rb") as f:
    model = pickle.load(f)
print(f"      ✔  {len(model.movies):,} movies loaded")
print(f"      ✔  Feature columns: {model.used_text_columns}")

# ══════════════════════════════════════════════════════════════════════════════
#  Step 2 — Create models/ directory
# ══════════════════════════════════════════════════════════════════════════════

os.makedirs(MODELS_DIR, exist_ok=True)
print(f"\n[2/5] Output directory: '{MODELS_DIR}/'")


# ══════════════════════════════════════════════════════════════════════════════
#  Step 3 — Save final_model.pkl
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n[3/5] Saving final_model.pkl ...")
final_model_path = os.path.join(MODELS_DIR, "final_model.pkl")
with open(final_model_path, "wb") as f:
    pickle.dump(model, f)
size_mb = os.path.getsize(final_model_path) / (1024 * 1024)
print(f"      ✔  Saved → {final_model_path}  ({size_mb:.1f} MB)")


# ══════════════════════════════════════════════════════════════════════════════
#  Step 4 — Build and save similarity_matrix.pkl
#  Format: list of dicts, one per movie
#  Each dict: { 'movie_index': int, 'top_k': [(idx, score), ...] }
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n[4/5] Building similarity matrix (top-{TOP_K} per movie) ...")
print(f"      This may take ~30 seconds for 16,290 movies ...")

n = len(model.movies)
similarity_matrix = []

for i in range(n):
    scores = []
    for j in range(n):
        if i == j:
            continue
        score = cosine_similarity(model.vectors[i], model.vectors[j])
        scores.append((j, round(score, 4)))
    scores.sort(key=lambda x: x[1], reverse=True)
    similarity_matrix.append({
        "movie_index": i,
        "top_k":       scores[:TOP_K],
    })

    # progress every 1000 movies
    if (i + 1) % 1000 == 0:
        print(f"      ... processed {i+1:,}/{n:,}")

sim_path = os.path.join(MODELS_DIR, "similarity_matrix.pkl")
with open(sim_path, "wb") as f:
    pickle.dump(similarity_matrix, f)
size_mb2 = os.path.getsize(sim_path) / (1024 * 1024)
print(f"      ✔  Saved → {sim_path}  ({size_mb2:.1f} MB)")


# ══════════════════════════════════════════════════════════════════════════════
#  Step 5 — Save movies_list.pkl
#  Only the fields Flask needs: title and normalized_title
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n[5/5] Saving movies_list.pkl ...")
movies_list = [
    {"title": m["title"], "normalized_title": m["normalized_title"]}
    for m in model.movies
]
movies_path = os.path.join(MODELS_DIR, "movies_list.pkl")
with open(movies_path, "wb") as f:
    pickle.dump(movies_list, f)
size_mb3 = os.path.getsize(movies_path) / (1024 * 1024)
print(f"      ✔  Saved → {movies_path}  ({size_mb3:.1f} MB)")


# ══════════════════════════════════════════════════════════════════════════════
#  Verification — load every file fresh and confirm it works
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'─'*60}")
print(f"  VERIFICATION — Loading all files fresh")
print(f"{'─'*60}")

# Load 1: final_model
with open(final_model_path, "rb") as f:
    loaded_model = pickle.load(f)
test_recs = loaded_model.recommend("The Godfather", limit=2)
print(f"\n  final_model.pkl    ✔  loaded")
print(f"  Quick test: recommend('The Godfather') → {[r['title'] for r in test_recs]}")

# Load 2: similarity_matrix
with open(sim_path, "rb") as f:
    loaded_sim = pickle.load(f)
print(f"\n  similarity_matrix.pkl  ✔  loaded")
print(f"  Entries: {len(loaded_sim):,}  |  "
      f"Top neighbour of movie[0]: index={loaded_sim[0]['top_k'][0][0]}, "
      f"score={loaded_sim[0]['top_k'][0][1]}")

# Load 3: movies_list
with open(movies_path, "rb") as f:
    loaded_movies = pickle.load(f)
print(f"\n  movies_list.pkl    ✔  loaded")
print(f"  Total movies: {len(loaded_movies):,}")
print(f"  Sample: {loaded_movies[0]}")

# ══════════════════════════════════════════════════════════════════════════════
#  Handoff checklist (printed to console — copy into notebook markdown cell)
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'='*60}")
print("  HANDOFF CHECKLIST (copy into your notebook markdown cell)")
print(f"{'='*60}")
print("""
## Files required for prediction

| File                   | Purpose                                      |
|------------------------|----------------------------------------------|
| final_model.pkl        | Trained MovieRecommender (TF-IDF + Cosine)   |
| similarity_matrix.pkl  | Pre-computed top-10 neighbours per movie     |
| movies_list.pkl        | All 16,290 movie titles (for search & lookup)|

## Input
A movie title string, e.g. "The Godfather"

## Output
{
  'query':        'The Godfather',
  'results': [
    {'rank': 1, 'title': 'The Godfather: Part II',
     'score': 0.5329, 'confidence': '53.3%', 'stars': '★★★☆☆'},
    ...
  ]
}
""")

print("  Task 1 Complete ✔")
print("=" * 60)
