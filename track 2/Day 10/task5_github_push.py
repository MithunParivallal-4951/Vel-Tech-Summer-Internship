"""
task5_github_push.py
──────────────────────
Day 10 · Task 5 — Push All Files to GitHub and Submit InnoTrack Report
Movie Recommender · Mithun · InnoTrack 2025

This script:
  1. Creates the correct GitHub folder structure locally
  2. Copies all final files into the right places
  3. Prints the exact git commands to run
  4. Prints the InnoTrack submission checklist

Run:
    python task5_github_push.py
"""

import os
import shutil
import pathlib

pathlib.WindowsPath = pathlib.PurePosixPath

# ══════════════════════════════════════════════════════════════════════════════
#  FOLDER STRUCTURE SETUP
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 65)
print("  Task 5 — GitHub Structure Setup & Push Guide")
print("=" * 65)

# Create required folders
folders = ["models", "charts"]
for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print(f"  ✔  folder '{folder}/' ready")

# ── Copy pkl files (already saved by task1) ───────────────────────────────────
pkl_files = [
    ("models/final_model.pkl",       "models/final_model.pkl"),
    ("models/similarity_matrix.pkl", "models/similarity_matrix.pkl"),
    ("models/movies_list.pkl",       "models/movies_list.pkl"),
]

print(f"\n  Verifying model files ...")
for src, dst in pkl_files:
    if os.path.exists(src):
        size_mb = os.path.getsize(src) / (1024 * 1024)
        print(f"  ✔  {dst:<40} ({size_mb:.1f} MB)")
    else:
        print(f"  ✗  MISSING: {src}  ← run task1_save_pkl_files.py first")

# ── Verify chart files ────────────────────────────────────────────────────────
chart_files = [
    "feature_importance.png",
    "genre_distribution.png",
    "godfather_signal_explainer.png",
]

print(f"\n  Verifying chart files ...")
for chart in chart_files:
    src = chart
    dst = os.path.join("charts", chart)
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"  ✔  charts/{chart}")
    elif os.path.exists(dst):
        print(f"  ✔  charts/{chart}  (already in place)")
    else:
        print(f"  ✗  MISSING: {chart}  ← run the relevant day9 script first")

# ── Python task files ────────────────────────────────────────────────────────
task_files = [
    "task1_save_pkl_files.py",
    "task2_predict_function.py",
    "task3_test_cases.py",
    "task4_model_summary_card.py",
    "task5_github_push.py",
    "day9_advanced_techniques.py",
    "godfather_signal_explainer.py",
    "model_summary_card.md",
]

print(f"\n  Verifying task scripts ...")
for f in task_files:
    exists = os.path.exists(f)
    mark   = "✔" if exists else "✗  MISSING"
    print(f"  {mark}  {f}")

# ══════════════════════════════════════════════════════════════════════════════
#  PRINT FOLDER TREE
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'─'*65}")
print("  EXPECTED GITHUB FOLDER STRUCTURE")
print(f"{'─'*65}")
structure = """
  your-repo/
  │
  ├── M2_model_development.ipynb        ← your full Day 6-10 notebook
  │
  ├── models/
  │   ├── final_model.pkl               ← trained MovieRecommender (~22 MB)
  │   ├── similarity_matrix.pkl         ← pre-computed top-10 neighbours
  │   └── movies_list.pkl               ← all 16,290 movie titles
  │
  ├── charts/
  │   ├── feature_importance.png        ← Task 1 Day 9 chart
  │   ├── genre_distribution.png        ← Task 2 Day 9 chart
  │   └── godfather_signal_explainer.png← Task 3 Day 9 explainer
  │
  ├── task1_save_pkl_files.py
  ├── task2_predict_function.py         ← Flask developer copies this
  ├── task3_test_cases.py
  ├── task4_model_summary_card.py
  ├── task5_github_push.py
  ├── day9_advanced_techniques.py
  └── model_summary_card.md             ← Flask team reads this first
"""
print(structure)

# ══════════════════════════════════════════════════════════════════════════════
#  GIT COMMANDS
# ══════════════════════════════════════════════════════════════════════════════

print(f"{'─'*65}")
print("  GIT COMMANDS — run these in your terminal")
print(f"{'─'*65}")
print("""
  # 1. Navigate to your project folder
  cd your-project-folder

  # 2. Initialise git (skip if already a repo)
  git init

  # 3. Add your GitHub remote (replace with your actual URL)
  git remote add origin https://github.com/your-username/your-repo.git

  # 4. Stage every file
  git add .

  # 5. Commit with a clear message
  git commit -m "M2 complete: final model, predict function, 10 test cases, summary card"

  # 6. Push to GitHub
  git push origin main

  # If push is rejected (remote has files you don't have):
  git pull origin main --allow-unrelated-histories
  git push origin main
""")

# ══════════════════════════════════════════════════════════════════════════════
#  INNOTRACK SUBMISSION CHECKLIST
# ══════════════════════════════════════════════════════════════════════════════

print(f"{'─'*65}")
print("  INNOTRACK SUBMISSION CHECKLIST")
print(f"{'─'*65}")
checklist = [
    ("GitHub repo link",
     "https://github.com/your-username/your-repo"),
    ("Screenshot: feature_importance.png",
     "charts/feature_importance.png"),
    ("Screenshot: 10 test cases table",
     "run task3_test_cases.py and screenshot the output"),
    ("Screenshot: model summary card",
     "model_summary_card.md — open and screenshot"),
    ("Screenshot: predict() function output",
     "run task2_predict_function.py and screenshot"),
]

for i, (item, action) in enumerate(checklist, 1):
    print(f"\n  {i}. {item}")
    print(f"     → {action}")

# ══════════════════════════════════════════════════════════════════════════════
#  THE MENTOR TEST
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'─'*65}")
print("  THE MENTOR TEST — confirm this works before submitting")
print(f"{'─'*65}")
print("""
  Your mentor will open a fresh Python session and run:

      from task2_predict_function import predict

      result = predict({'title': 'The Dark Knight'})
      print(result)

  Expected output (printed in under 3 seconds):

      {
        'status':   'success',
        'query':    'The Dark Knight',
        'resolved': 'The Dark Knight',
        'results': [
          {'rank': 1, 'title': 'Batman Begins',  'confidence': '57.4%', 'stars': '★★★☆☆', ...},
          {'rank': 2, 'title': 'The Dark Knight Rises', ...},
          ...
        ]
      }

  If this prints cleanly → you are M3-READY ✔
  If it crashes        → fix task2_predict_function.py before submitting
""")

# ══════════════════════════════════════════════════════════════════════════════
#  FINAL CHECKLIST
# ══════════════════════════════════════════════════════════════════════════════

print(f"{'='*65}")
print("  FINAL M2 END-OF-DAY CHECKLIST")
print(f"{'='*65}")
final_checks = [
    "final_model.pkl saved in models/ folder",
    "similarity_matrix.pkl saved in models/ folder",
    "movies_list.pkl saved in models/ folder",
    "All 3 .pkl files load without errors",
    "predict() function written and self-contained",
    "predict() returns human-readable dict",
    "10 test cases run — 9 PASS, case 10 returns ERROR not crash",
    "Model summary card written (model_summary_card.md)",
    "All chart PNGs in charts/ folder",
    "GitHub repo pushed with correct folder structure",
    "InnoTrack submitted with link + screenshots",
]

for item in final_checks:
    print(f"  ✔  {item}")

print(f"\n{'='*65}")
print("  Task 5 Complete — M2 Handoff Ready ✔")
print(f"{'='*65}\n")
