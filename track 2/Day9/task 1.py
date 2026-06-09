"""
task1_feature_importance.py
────────────────────────────
Task 1 — Feature Importance for Movie Recommender
Plots the top TF-IDF terms by average weight across all 16,290 movies.
"""

import math
import pathlib
import pickle
from collections import Counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# ── patch so Windows-saved model loads on Linux/Mac ──────────────────────────
pathlib.WindowsPath = pathlib.PurePosixPath

# ── 1. Load model ─────────────────────────────────────────────────────────────
print("Loading model...")
with open("movie_recommender.pkl", "rb") as f:
    model = pickle.load(f)
print(f"✔  Loaded — {len(model.movies):,} movies")

# ── 2. Compute average TF-IDF weight per term ─────────────────────────────────
print("Computing feature importances...")

term_totals = Counter()
term_counts = Counter()

for vector in model.vectors:
    for term, weight in vector.items():
        term_totals[term] += weight
        term_counts[term] += 1

avg_weights = {
    term: term_totals[term] / term_counts[term]
    for term in term_totals
}

TOP_N = 20
top_terms = sorted(avg_weights.items(), key=lambda x: x[1], reverse=True)[:TOP_N]

# ── 3. Print table ────────────────────────────────────────────────────────────
print(f"\n{'Rank':<6} {'Term':<25} {'Avg TF-IDF Weight':>18}")
print("─" * 52)
for rank, (term, weight) in enumerate(top_terms, 1):
    bar = "█" * int(weight * 10)
    print(f"{rank:<6} {term:<25} {weight:>18.5f}  {bar}")

# ── 4. Plot ───────────────────────────────────────────────────────────────────
terms   = [t for t, _ in reversed(top_terms)]
weights = [w for _, w in reversed(top_terms)]

# Colour gradient: low weight = light blue, high weight = dark navy
norm   = mcolors.Normalize(vmin=min(weights), vmax=max(weights))
colors = [plt.cm.Blues(0.4 + 0.6 * norm(w)) for w in weights]

fig, ax = plt.subplots(figsize=(11, 8))
bars = ax.barh(terms, weights, color=colors, edgecolor="white", height=0.7)

# Value labels on each bar
for bar, weight in zip(bars, weights):
    ax.text(
        bar.get_width() + 0.02,
        bar.get_y() + bar.get_height() / 2,
        f"{weight:.4f}",
        va="center", ha="left",
        fontsize=9, color="#333333"
    )

ax.set_xlabel("Average TF-IDF Weight", fontsize=12, labelpad=10)
ax.set_title(
    f"Feature Importance — Top {TOP_N} TF-IDF Terms\n"
    "Words the Movie Recommender Model Cares About Most",
    fontsize=14, fontweight="bold", pad=15
)
ax.set_xlim(0, max(weights) * 1.18)
ax.spines[["top", "right"]].set_visible(False)
ax.tick_params(axis="y", labelsize=10)
ax.tick_params(axis="x", labelsize=9)

# Annotation box explaining what TF-IDF weight means
ax.text(
    0.98, 0.02,
    "Higher weight = this word appears\nfrequently in few movies\n→ very distinctive / important signal",
    transform=ax.transAxes,
    fontsize=8.5, color="#555555",
    ha="right", va="bottom",
    bbox=dict(boxstyle="round,pad=0.4", facecolor="#f0f4ff", edgecolor="#aaaacc")
)

plt.tight_layout()
plt.savefig("feature_importance.png", dpi=150, bbox_inches="tight")
plt.close()

print("\n✔  Chart saved → feature_importance.png")
print("\nWhat these terms mean:")
print("  These are the most DISTINCTIVE words in the dataset.")
print("  They appear with high weight in a small number of movies,")
print("  which means they are strong signals for recommending similar films.")
print("  Most are rare director/writer names — exactly what a content-based")
print("  recommender should rely on to link movies by style and authorship.")
