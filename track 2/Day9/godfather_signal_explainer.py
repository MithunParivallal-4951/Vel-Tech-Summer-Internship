"""
godfather_signal_explainer.py
──────────────────────────────
Generates a full explainer image showing:
  - The Godfather's top TF-IDF signals (coppola, ford, francis)
  - How those signals link to all 5 recommended films
  - The cosine similarity contribution per term per film
  - A bottom panel explaining the cosine similarity formula

Run:
    python godfather_signal_explainer.py
Output:
    godfather_signal_explainer.png
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# ── Data ──────────────────────────────────────────────────────────────────────

QUERY = "The Godfather"

QUERY_VECTOR = {
    "coppola": 0.3233,
    "ford":    0.2234,
    "francis": 0.2158,
}

RECS = [
    {
        "title":  "The Godfather: Part II",
        "score":  0.5329,
        "stars":  "★★★☆☆",
        "signals": [("coppola", 0.1788), ("ford", 0.0759), ("francis", 0.0708)],
    },
    {
        "title":  "The Godfather: Part III",
        "score":  0.4888,
        "stars":  "★★☆☆☆",
        "signals": [("coppola", 0.1052), ("ford", 0.0670), ("francis", 0.0625)],
    },
    {
        "title":  "The Rainmaker",
        "score":  0.4474,
        "stars":  "★★☆☆☆",
        "signals": [("coppola", 0.1883), ("ford", 0.1199), ("francis", 0.1118)],
    },
    {
        "title":  "The Cotton Club",
        "score":  0.3955,
        "stars":  "★★☆☆☆",
        "signals": [("coppola", 0.1322), ("ford", 0.0842), ("francis", 0.0785)],
    },
    {
        "title":  "Tetro",
        "score":  0.3911,
        "stars":  "★★☆☆☆",
        "signals": [("coppola", 0.1651), ("ford", 0.1051), ("francis", 0.0981)],
    },
]

# ── Colours ───────────────────────────────────────────────────────────────────
BG          = "#f9f8f6"
QUERY_COL   = "#f5a623"      # amber
QUERY_DARK  = "#7a4f00"
REC_COL1    = "#7b6fe0"      # purple  (Godfather films)
REC_COL2    = "#1aab7a"      # teal    (other Coppola films)
REC_DARK1   = "#2d2060"
REC_DARK2   = "#064535"
BAR_COLS    = ["#7b6fe0", "#a08be8", "#c9bcf0"]  # coppola / ford / francis
FORMULA_BG  = "#fff8e7"
FORMULA_BOR = "#f5a623"
INSIGHT_BG  = "#fff3cd"
AXIS_COL    = "#444"
MUTED       = "#666"


def rounded_box(ax, x, y, w, h, color, text_lines,
                text_color="#ffffff", radius=0.008, fontsize=10):
    """Draw a rounded rectangle with centered multi-line text."""
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        facecolor=color, edgecolor="white", linewidth=1.2,
        transform=ax.transData, clip_on=False
    )
    ax.add_patch(box)
    mid_x = x + w / 2
    if len(text_lines) == 1:
        ax.text(mid_x, y + h / 2, text_lines[0],
                ha="center", va="center",
                fontsize=fontsize, color=text_color, fontweight="bold")
    else:
        for i, (txt, fs, bold) in enumerate(text_lines):
            offset = (i - (len(text_lines) - 1) / 2) * (h / (len(text_lines) + 0.5))
            ax.text(mid_x, y + h / 2 - offset, txt,
                    ha="center", va="center",
                    fontsize=fs,
                    color=text_color,
                    fontweight="bold" if bold else "normal")


def draw_arrow(ax, x1, y1, x2, y2, color="#999", lw=1.2):
    ax.annotate("",
        xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(arrowstyle="-|>", color=color,
                        lw=lw, mutation_scale=12))


# ── Figure setup ──────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(16, 14), facecolor=BG)
ax  = fig.add_axes([0, 0, 1, 1], facecolor=BG)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

# ── TITLE ─────────────────────────────────────────────────────────────────────
ax.text(0.5, 0.96,
        "Why 'The Godfather' leads to every recommendation",
        ha="center", va="center",
        fontsize=18, fontweight="bold", color="#222")
ax.text(0.5, 0.925,
        "The model identified Francis Ford Coppola's name as 3 separate high-weight TF-IDF tokens\n"
        "— coppola · ford · francis — and matched every film he directed",
        ha="center", va="center",
        fontsize=11, color=MUTED)

# Divider
ax.plot([0.04, 0.96], [0.905, 0.905], color="#ddd", lw=1)

# ── QUERY BOX (left) ──────────────────────────────────────────────────────────
qx, qy, qw, qh = 0.04, 0.70, 0.18, 0.18
rounded_box(ax, qx, qy, qw, qh, QUERY_COL,
            [("The Godfather", 11, True),
             ("Query movie", 9, False),
             ("(1972)", 9, False)],
            text_color=QUERY_DARK)

# Query vector weights (below query box)
ax.text(qx + qw / 2, qy - 0.025, "TF-IDF signals in this movie's vector:",
        ha="center", va="center", fontsize=8.5, color=MUTED, style="italic")

terms = ["coppola", "ford", "francis"]
weights_q = [0.3233, 0.2234, 0.2158]
bar_y_start = qy - 0.035
bar_h = 0.032
bar_gap = 0.038
max_w_bar = 0.15

for i, (term, wt) in enumerate(zip(terms, weights_q)):
    by = bar_y_start - i * bar_gap - bar_h
    bw = (wt / 0.35) * max_w_bar
    rect = FancyBboxPatch(
        (qx, by), bw, bar_h,
        boxstyle="round,pad=0,rounding_size=0.003",
        facecolor=BAR_COLS[i], edgecolor="none", alpha=0.85
    )
    ax.add_patch(rect)
    ax.text(qx + bw + 0.005, by + bar_h / 2,
            f"{term}  {wt:.4f}",
            va="center", fontsize=8.5, color=AXIS_COL, fontweight="bold")

# ── ARROW from query to recs ──────────────────────────────────────────────────
draw_arrow(ax, qx + qw, qy + qh * 0.5,
           0.26, qy + qh * 0.5,
           color=QUERY_COL, lw=2)

ax.text(0.225, qy + qh * 0.5 + 0.018,
        "cosine\nsimilarity", ha="center", va="bottom",
        fontsize=8, color=MUTED, style="italic")

# ── RECOMMENDED FILMS (right side) ───────────────────────────────────────────
rec_x   = 0.27
rec_w   = 0.26
rec_h   = 0.095
rec_gap = 0.108
rec_y_top = 0.84

for idx, rec in enumerate(RECS):
    ry = rec_y_top - idx * rec_gap
    col  = REC_COL1 if idx < 2 else REC_COL2
    dark = REC_DARK1 if idx < 2 else REC_DARK2

    rounded_box(ax, rec_x, ry, rec_w, rec_h, col,
                [(f"#{idx+1}  {rec['title']}", 9.5, True),
                 (f"Score: {rec['score']}   {rec['stars']}", 8.5, False)],
                text_color="white")

    # Signal bars (to the right of each rec box)
    bar_x_start = rec_x + rec_w + 0.015
    sb_h = 0.016
    sb_gap = 0.026
    max_sb_w = 0.22

    for j, (term, contrib) in enumerate(rec["signals"]):
        sb_y = ry + rec_h - 0.02 - j * sb_gap - sb_h
        sb_w = (contrib / 0.20) * max_sb_w
        sb_w = min(sb_w, max_sb_w)
        rect2 = FancyBboxPatch(
            (bar_x_start, sb_y), sb_w, sb_h,
            boxstyle="round,pad=0,rounding_size=0.002",
            facecolor=BAR_COLS[j], edgecolor="none", alpha=0.75
        )
        ax.add_patch(rect2)
        ax.text(bar_x_start + sb_w + 0.006, sb_y + sb_h / 2,
                f"{term}  {contrib:.4f}",
                va="center", fontsize=8, color=AXIS_COL)

# ── LEGEND for signal bars ────────────────────────────────────────────────────
lx = 0.27
ly = 0.075
for i, (term, col) in enumerate(zip(terms, BAR_COLS)):
    rect3 = FancyBboxPatch(
        (lx + i * 0.12, ly), 0.018, 0.018,
        boxstyle="round,pad=0,rounding_size=0.002",
        facecolor=col, edgecolor="none"
    )
    ax.add_patch(rect3)
    ax.text(lx + i * 0.12 + 0.025, ly + 0.009,
            f"'{term}' contribution",
            va="center", fontsize=8.5, color=AXIS_COL)

# ── BOTTOM: FORMULA PANEL ─────────────────────────────────────────────────────
fx, fy, fw, fh = 0.04, 0.10, 0.92, 0.16

formula_box = FancyBboxPatch(
    (fx, fy), fw, fh,
    boxstyle="round,pad=0,rounding_size=0.008",
    facecolor=FORMULA_BG, edgecolor=FORMULA_BOR, linewidth=1.5
)
ax.add_patch(formula_box)

ax.text(fx + fw / 2, fy + fh - 0.022,
        "How cosine similarity is calculated",
        ha="center", va="center",
        fontsize=12, fontweight="bold", color="#7a4f00")

# Formula text
ax.text(fx + fw / 2, fy + fh * 0.52,
        "similarity(A, B)  =  (coppola_A × coppola_B  +  ford_A × ford_B  +  francis_A × francis_B  +  …)",
        ha="center", va="center",
        fontsize=9.5, color="#333",
        fontfamily="monospace")

ax.text(fx + fw / 2, fy + fh * 0.52 - 0.028,
        "────────────────────────────────────────────────────────────────",
        ha="center", va="center",
        fontsize=9, color="#bbb")

ax.text(fx + fw / 2, fy + fh * 0.52 - 0.050,
        "magnitude(A)  ×  magnitude(B)",
        ha="center", va="center",
        fontsize=9.5, color="#333",
        fontfamily="monospace")

# Key insight strip at very bottom of formula box
insight_rect = FancyBboxPatch(
    (fx + 0.01, fy + 0.005), fw - 0.02, 0.035,
    boxstyle="round,pad=0,rounding_size=0.005",
    facecolor="#ffe8a0", edgecolor=FORMULA_BOR, linewidth=0.8
)
ax.add_patch(insight_rect)

ax.text(fx + fw / 2, fy + 0.005 + 0.0175,
        "Key insight: 'Francis Ford Coppola' splits into 3 tokens — each contributes independently → "
        "director signal is 3× stronger than a single token",
        ha="center", va="center",
        fontsize=9, color="#7a4f00", fontweight="bold")

# ── CONNECTING LINES from query to each rec ───────────────────────────────────
q_cx = qx + qw
q_cy = qy + qh / 2

for idx in range(len(RECS)):
    ry  = rec_y_top - idx * rec_gap
    r_cy = ry + rec_h / 2
    ax.annotate("",
        xy=(rec_x, r_cy),
        xytext=(q_cx, q_cy),
        arrowprops=dict(
            arrowstyle="-",
            color=QUERY_COL,
            lw=0.8,
            alpha=0.4,
            connectionstyle="arc3,rad=0.0"
        ))

# ── WATERMARK / footer ────────────────────────────────────────────────────────
ax.text(0.5, 0.015,
        "Movie Recommender — TF-IDF + Cosine Similarity  |  Day 9 Advanced Techniques  |  InnoTrack 2025",
        ha="center", va="center",
        fontsize=7.5, color="#aaa")

# ── Save ──────────────────────────────────────────────────────────────────────
plt.savefig("godfather_signal_explainer.png",
            dpi=180, bbox_inches="tight",
            facecolor=BG)
plt.close()
print("✔  Saved → godfather_signal_explainer.png")
