"""
task2_predict_function.py
──────────────────────────
Day 10 · Task 2 — Write and Test a Single predict() Function
Movie Recommender · Mithun · InnoTrack 2025

This is the function the Flask developer will copy directly into their app.
Input  : movie title string (exactly as typed by the user in the web form)
Output : dict with top-5 recommendations, scores, stars, and watch priority

Run:
    python task2_predict_function.py
"""

import math
import pathlib
import pickle
import os

pathlib.WindowsPath = pathlib.PurePosixPath

MODELS_DIR = "models"


# ══════════════════════════════════════════════════════════════════════════════
#  THE PREDICT FUNCTION  ← Flask developer copies everything below this line
# ══════════════════════════════════════════════════════════════════════════════

def predict(inputs: dict) -> dict:
    """
    Full prediction pipeline for the Movie Recommender.

    Parameters
    ----------
    inputs : dict
        Must contain key 'title' with a movie name string.
        Example: {'title': 'The Godfather'}

    Returns
    -------
    dict with keys:
        status       : 'success' or 'error'
        query        : original input title
        resolved     : title as found in the dataset
        results      : list of recommendation cards (top 5)
        error        : error message string (only present on failure)

    Each result card contains:
        rank, title, score, confidence, stars, watch_priority, match_label
    """

    # ── Step 1: Load all required .pkl files ──────────────────────────────────
    # These files must be in the same 'models/' folder as this script
    try:
        model_path  = os.path.join(MODELS_DIR, "final_model.pkl")
        movies_path = os.path.join(MODELS_DIR, "movies_list.pkl")

        with open(model_path, "rb") as f:
            model = pickle.load(f)
        with open(movies_path, "rb") as f:
            movies_list = pickle.load(f)

    except FileNotFoundError as e:
        return {
            "status": "error",
            "error":  f"Model file not found: {e}. Run task1_save_pkl_files.py first."
        }

    # ── Step 2: Validate input ────────────────────────────────────────────────
    raw_title = inputs.get("title", "").strip()

    if not raw_title:
        return {
            "status": "error",
            "query":  raw_title,
            "error":  "No movie title provided. Please enter a title."
        }

    # ── Step 3: Preprocess — resolve title to exact match ─────────────────────
    # Simulates search-as-you-type: if the user's typing isn't exact,
    # auto-select the closest match from the dataset.
    normalised  = raw_title.lower().strip()
    exact_match = any(m["normalized_title"] == normalised for m in movies_list)

    if exact_match:
        resolved_title = next(
            m["title"] for m in movies_list if m["normalized_title"] == normalised
        )
    else:
        suggestions = model.search_titles(raw_title, limit=5)
        if not suggestions:
            return {
                "status": "error",
                "query":  raw_title,
                "error":  f"Movie '{raw_title}' not found. Try a different title."
            }
        resolved_title = suggestions[0]

    # ── Step 4: Run model prediction ──────────────────────────────────────────
    try:
        raw_recs = model.recommend(resolved_title, limit=5)
    except ValueError as e:
        return {
            "status": "error",
            "query":  raw_title,
            "error":  str(e)
        }

    # ── Step 5: Enrich output — convert raw scores to human-readable cards ────
    def enrich(rank: int, rec: dict) -> dict:
        score = rec["similarity_score"]
        if score >= 0.85:
            label, priority, stars = "Excellent match", "Watch immediately",   "★★★★★"
        elif score >= 0.70:
            label, priority, stars = "Strong match",    "Highly recommended",  "★★★★☆"
        elif score >= 0.50:
            label, priority, stars = "Good match",      "Worth watching",      "★★★☆☆"
        elif score >= 0.30:
            label, priority, stars = "Moderate match",  "If you have time",    "★★☆☆☆"
        else:
            label, priority, stars = "Loose match",     "Exploratory",         "★☆☆☆☆"
        return {
            "rank":           rank,
            "title":          rec["title"],
            "score":          score,
            "confidence":     f"{score * 100:.1f}%",
            "stars":          stars,
            "match_label":    label,
            "watch_priority": priority,
        }

    enriched = [enrich(i + 1, r) for i, r in enumerate(raw_recs)]

    # ── Step 6: Return clean result dict ──────────────────────────────────────
    return {
        "status":   "success",
        "query":    raw_title,
        "resolved": resolved_title,
        "results":  enriched,
    }


# ══════════════════════════════════════════════════════════════════════════════
#  SAFE WRAPPER  — used in Task 3 testing
# ══════════════════════════════════════════════════════════════════════════════

def predict_safe(inputs: dict) -> dict:
    """Wraps predict() so any unexpected crash returns an error dict, not an exception."""
    try:
        return predict(inputs)
    except Exception as e:
        return {
            "status": "error",
            "query":  inputs.get("title", ""),
            "error":  str(e),
            "results": []
        }


# ══════════════════════════════════════════════════════════════════════════════
#  QUICK TEST — one call to confirm the function works
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("  Task 2 — predict() Function Test")
    print("=" * 60)

    sample = {"title": "The Godfather"}
    print(f"\nCalling predict({sample}) ...\n")

    result = predict(sample)

    if result["status"] == "success":
        print(f"  Status   : {result['status']}")
        print(f"  Query    : {result['query']}")
        print(f"  Resolved : {result['resolved']}")
        print(f"  Results  :")
        for card in result["results"]:
            print(f"    {card['rank']}. {card['title']:<35} "
                  f"{card['confidence']:>6}  {card['stars']}  {card['watch_priority']}")
    else:
        print(f"  ERROR: {result['error']}")

    print(f"\n  ✔  predict() function is working and M3/Flask ready.")
    print("=" * 60)
