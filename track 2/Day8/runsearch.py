"""
run_all_searches.py
───────────────────
Convenience runner — executes all three search strategies in sequence and
prints a side-by-side comparison of the best configuration found by each.

Usage
-----
    python run_all_searches.py --data sample_movies.csv
    python run_all_searches.py --data sample_movies.csv --save-best
"""

import argparse
import subprocess
import sys


def run(script: str, extra_args: list[str]) -> int:
    cmd = [sys.executable, script] + extra_args
    print(f"\n{'='*65}")
    print(f"  Running: {' '.join(cmd)}")
    print(f"{'='*65}\n")
    result = subprocess.run(cmd)
    return result.returncode


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data",      default="sample_movies.csv")
    parser.add_argument("--limit",     type=int, default=5)
    parser.add_argument("--n-iter",    type=int, default=20,
                        help="Random-search iterations")
    parser.add_argument("--save-best", action="store_true",
                        help="Save best model from each strategy")
    args = parser.parse_args()

    common = ["--data", args.data, "--limit", str(args.limit)]
    if args.save_best:
        common.append("--save-best")

    scripts = [
        ("train_tfidf_grid_search.py",  common),
        ("train_sklearn_grid_search.py", common),
        ("train_random_search.py",       common + ["--n-iter", str(args.n_iter)]),
    ]

    for script, extra in scripts:
        rc = run(script, extra)
        if rc != 0:
            print(f"[WARNING] {script} exited with code {rc}")

    print("\n\nAll searches complete.")
    print("Saved models:")
    print("  best_tfidf_model.pkl   ← pure-Python TF-IDF grid search")
    print("  best_sklearn_model.pkl ← sklearn TF-IDF + NearestNeighbors grid search")
    print("  best_random_model.pkl  ← randomized search (wider param space)")


if __name__ == "__main__":
    main()
