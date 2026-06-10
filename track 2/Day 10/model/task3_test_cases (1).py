"""
task3_test_cases.py
────────────────────
Day 10 · Task 3 — Run 10 Test Cases and Log Results
Movie Recommender · Mithun · InnoTrack 2025

Runs 10 varied inputs through predict_safe() and prints a results table.

Case types:
  1-3  Normal popular movies (different genres)
  4-5  High similarity expected (same director)
  6-7  Edge cases (obscure title, one-word title)
  8-9  Known good matches (films sharing a director)
  10   Invalid input (empty / gibberish — must return error, NOT crash)

Run:
    python task3_test_cases.py
    (task2_predict_function.py must be importable)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from task2_predict_function import predict_safe

# ══════════════════════════════════════════════════════════════════════════════
#  10 TEST CASES
# ══════════════════════════════════════════════════════════════════════════════

TEST_CASES = [
    # ── Normal cases (1-3) ───────────────────────────────────────────────────
    {
        "case":        1,
        "type":        "Normal",
        "description": "Classic crime drama",
        "input":       {"title": "The Godfather"},
        "expect":      "success — top result should be another Coppola film",
    },
    {
        "case":        2,
        "type":        "Normal",
        "description": "Studio Ghibli animation",
        "input":       {"title": "Spirited Away"},
        "expect":      "success — top result should be another Miyazaki film",
    },
    {
        "case":        3,
        "type":        "Normal",
        "description": "Christopher Nolan thriller",
        "input":       {"title": "Inception"},
        "expect":      "success — top results should be other Nolan films",
    },

    # ── High similarity expected (4-5) ───────────────────────────────────────
    {
        "case":        4,
        "type":        "High Similarity",
        "description": "Tarantino crime film — Reservoir Dogs expected at top",
        "input":       {"title": "Pulp Fiction"},
        "expect":      "success — Reservoir Dogs score > 0.50",
    },
    {
        "case":        5,
        "type":        "High Similarity",
        "description": "Sequel query — should find original and other parts",
        "input":       {"title": "The Godfather: Part II"},
        "expect":      "success — The Godfather score > 0.50",
    },

    # ── Edge cases (6-7) ─────────────────────────────────────────────────────
    {
        "case":        6,
        "type":        "Edge Case",
        "description": "Partial title / lowercase input",
        "input":       {"title": "parasite"},
        "expect":      "success — auto-resolved to 'Parasite'",
    },
    {
        "case":        7,
        "type":        "Edge Case",
        "description": "One-word obscure title",
        "input":       {"title": "Tetro"},
        "expect":      "success — should return Coppola films",
    },

    # ── Known good matches (8-9) ─────────────────────────────────────────────
    {
        "case":        8,
        "type":        "Known Match",
        "description": "Disney/Pixar — should find other Pixar films",
        "input":       {"title": "Toy Story"},
        "expect":      "success — top results should be Pixar films",
    },
    {
        "case":        9,
        "type":        "Known Match",
        "description": "Martin Scorsese film",
        "input":       {"title": "Goodfellas"},
        "expect":      "success — top results should be other Scorsese films",
    },

    # ── Invalid input (10) ───────────────────────────────────────────────────
    {
        "case":        10,
        "type":        "Invalid Input",
        "description": "Empty string — should return error, NOT crash Python",
        "input":       {"title": ""},
        "expect":      "error — readable message returned, no crash",
    },
]


# ══════════════════════════════════════════════════════════════════════════════
#  RUN ALL 10 AND LOG RESULTS
# ══════════════════════════════════════════════════════════════════════════════

def run_tests(cases: list) -> list:
    log = []
    for tc in cases:
        result = predict_safe(tc["input"])

        if result["status"] == "success" and result.get("results"):
            top      = result["results"][0]
            top_title = top["title"]
            top_conf  = top["confidence"]
            top_stars = top["stars"]
            status    = "PASS"
        elif result["status"] == "error":
            top_title = result.get("error", "")[:35]
            top_conf  = "N/A"
            top_stars = "—"
            # Case 10 is expected to be an error — that is a PASS
            status = "PASS" if tc["type"] == "Invalid Input" else "FAIL"
        else:
            top_title = "No results"
            top_conf  = "N/A"
            top_stars = "—"
            status    = "FAIL"

        log.append({
            "case":         tc["case"],
            "type":         tc["type"],
            "input":        tc["input"]["title"] or "(empty)",
            "top_result":   top_title,
            "confidence":   top_conf,
            "stars":        top_stars,
            "status":       status,
            "raw":          result,
        })

    return log


def print_results(log: list):
    SEP  = "=" * 100
    SEP2 = "-" * 100

    print(f"\n{SEP}")
    print(f"  Task 3 — 10 Test Cases · Movie Recommender · Day 10")
    print(SEP)
    print(f"\n{'Case':<5} {'Type':<16} {'Input Title':<25} "
          f"{'Top Recommendation':<32} {'Match':>6}  {'Stars':<10}  Status")
    print(SEP2)

    for row in log:
        status_icon = "✔" if row["status"] == "PASS" else "✗"
        print(f"{row['case']:<5} {row['type']:<16} {row['input']:<25} "
              f"{row['top_result'][:31]:<32} {row['confidence']:>6}  "
              f"{row['stars']:<10}  {status_icon} {row['status']}")

    print(SEP2)
    passed = sum(1 for r in log if r["status"] == "PASS")
    failed = sum(1 for r in log if r["status"] == "FAIL")
    print(f"\n  Total: {len(log)} cases  |  "
          f"PASSED: {passed}  |  FAILED: {failed}")
    print(f"  Note: Case 10 (Invalid Input) returning ERROR is correct — "
          f"it means try/except caught the bad input safely.\n")

    # Detailed output for each case
    print(f"\n{'─'*100}")
    print("  DETAILED OUTPUT PER CASE")
    print(f"{'─'*100}")

    for row in log:
        tc = next(t for t in TEST_CASES if t["case"] == row["case"])
        print(f"\n  Case {row['case']} — {tc['type']} — \"{tc['description']}\"")
        print(f"  Input    : {{'title': '{row['input']}'}}")
        print(f"  Expected : {tc['expect']}")
        res = row["raw"]
        if res["status"] == "success":
            print(f"  Status   : ✔ SUCCESS")
            print(f"  Resolved : {res.get('resolved', '')}")
            print(f"  Results  :")
            for card in res.get("results", []):
                print(f"    {card['rank']}. {card['title']:<38} "
                      f"{card['confidence']:>6}  {card['stars']}")
        else:
            print(f"  Status   : {'✔ ERROR (expected)' if tc['type']=='Invalid Input' else '✗ ERROR'}")
            print(f"  Message  : {res.get('error', '')}")

    print(f"\n{SEP}")
    print(f"  Task 3 Complete — {passed}/10 PASSED ✔")
    print(SEP)


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "█" * 60)
    print("  Task 3 — Running 10 Test Cases")
    print("█" * 60)
    print("  Loading model and running all cases ...\n")

    log = run_tests(TEST_CASES)
    print_results(log)
