#!/usr/bin/env python3
"""
capstone_test.py - the Milestone 5 test harness for the capstone (Shape B).

One command per trial. Run it three separate times, changing nothing between:

    python capstone_test.py --trial 1
    python capstone_test.py --trial 2
    python capstone_test.py --trial 3
    python capstone_test.py --report          # prints the run-log table to paste

Milestone 6, after the one improvement is made, the same three trials again,
into a separate folder so the before numbers are untouched:

    python capstone_test.py --trial 1 --label after
    python capstone_test.py --trial 2 --label after
    python capstone_test.py --trial 3 --label after
    python capstone_test.py --report --label after
    python capstone_test.py --compare         # before and after, side by side

Each trial writes capstone_results/trial_N/ (capstone_results_after/trial_N/ with
--label after) and refuses to overwrite one that already exists, so a finished
trial cannot be replaced by accident. The measurements, the targets and the
files each trial builds are identical before and after. Only the output folder
and --compare were added in Milestone 6.

COMMIT THIS FILE BEFORE YOU RUN IT. The mix of bad and good files below is part
of the test, and it has to exist before the results do.

HOW EACH CRITERION IS MEASURED
This is my reading of the sentences in criteria.md. Where a sentence had no
number or definition I picked one and wrote it here. If your reading differs,
change it BEFORE you commit this file and run anything.

1. "At least 75% of bad inputs in a set of 100 are detected and blocked."
   100 bad files are built (BAD_MIX below) and each goes through run.py's
   run_once(), the same function `python run.py` uses. BLOCKED means the run
   finished with status "refused": the gate stopped it and gave a code. A file
   that gets past the gate (status "ok", or "error" after the gate) is NOT
   blocked. A refusal coded "unexpected" counts as blocked but is reported
   separately, because it means the gate stopped it without a named reason.
   Target: 75 or more of 100.

2. "Regardless of the amount of bad inputs, the run is properly logged."
   After the 100 bad runs above, run_log.jsonl must hold exactly 100 records,
   one per input, each complete. COMPLETE means: a timestamp, an input holding
   the file path, an output with a status (ok, refused or error) and a
   non-empty message, a code on every status that is not ok, and a numeric
   duration_ms. guard_log.jsonl must also hold exactly 100 records.
   Target: 100 of 100 records complete, no extra, none missing.

3. "The original function still works even with the new changes added."
   Two checks on the real labels.csv. (a) The gate returns the DataFrame
   unchanged, equal to pd.read_csv. (b) `python run.py` on labels.csv, seed 42,
   gives the same accuracy and macro F1 as results.json from the notebook,
   rounded to 4 decimals (0.5 and 0.2222), with the same train and test sizes.
   Target: both checks pass.

4. "At least 90% of the good inputs in a set of 100 are able to pass without
   problems."
   100 good files are built (GOOD_VARIANTS below) and each goes through the
   gate. PASS WITHOUT PROBLEMS means no refusal, and the DataFrame returned
   equals what pandas reads from the same file. Target: 90 or more of 100.

5. "After the first run of the program the time it takes for the program to run
   is significantly faster. For example the first run should take up to 5 to 8
   seconds while the rest should take 1 to 2 seconds."
   `python run.py --runs 10` is launched once, as one process, so run 1 is cold
   and runs 2 to 10 are warm. I turned your example into thresholds using the
   upper end of each range. Target: run 1 at 8.0 seconds or less AND every one
   of runs 2 to 10 at 2.0 seconds or less.

The gate is deterministic, so criteria 1 and 4 can score the same across
trials. To keep the trials separate, each trial builds new files from its own
random seed. The kinds and the counts stay fixed.
"""

import argparse
import csv
import json
import os
import platform
import random
import subprocess
import sys
import tempfile
import time
from argparse import Namespace
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO))

from Guard import DEFAULT_LABELS, GuardError, validate_dataset  # noqa: E402
from run import run_once  # noqa: E402  (imports torch only when it trains)

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, OSError, ValueError):
        pass

LABELS = list(DEFAULT_LABELS)
RESULTS_DIR = REPO / "capstone_results"

# Targets, copied from criteria.md.
C1_TARGET = 75      # of 100 bad inputs blocked
C4_TARGET = 90      # of 100 good inputs passed
C5_FIRST_MAX_S = 8.0
C5_REST_MAX_S = 2.0

WORDS = ("spell card danmaku stage boss theme remix remake canon fanon lore game "
         "character route music hitbox bomb extra phantasm moon shrine mansion "
         "forest village hell border dream lunar youkai human barrier opinion "
         "argument pattern boss difficulty release story manga").split()


# --------------------------------------------------------------------------
# Building files
# --------------------------------------------------------------------------

def make_text(rng, tag):
    words = " ".join(rng.choice(WORDS) for _ in range(rng.randint(5, 25)))
    return f"{words} ({tag})"


def make_rows(rng, n, tag):
    """n unique rows. Every label has at least 3, none is over 60% of n."""
    counts = {label: 3 for label in LABELS}
    cap = int(0.6 * n)
    remaining = n - 3 * len(LABELS)
    while remaining > 0:
        label = rng.choice(LABELS)
        if counts[label] < cap:
            counts[label] += 1
            remaining -= 1
    rows = []
    for label, count in counts.items():
        for i in range(count):
            rows.append([make_text(rng, f"{tag}-{label}-{i}"), label])
    rng.shuffle(rows)
    return rows


def write_csv(path, rows, header=("text", "label"), encoding="utf-8",
              lineterminator="\n", delimiter=","):
    with open(path, "w", encoding=encoding, newline="") as f:
        writer = csv.writer(f, delimiter=delimiter, lineterminator=lineterminator)
        writer.writerow(header)
        writer.writerows(rows)


# ---- good inputs ----------------------------------------------------------

def good_plain(rng, path, tag):
    write_csv(path, make_rows(rng, rng.randint(20, 120), tag))

def good_crlf(rng, path, tag):
    write_csv(path, make_rows(rng, rng.randint(20, 120), tag), lineterminator="\r\n")

def good_bom(rng, path, tag):
    write_csv(path, make_rows(rng, rng.randint(20, 120), tag), encoding="utf-8-sig")

def good_punctuation_and_newlines(rng, path, tag):
    rows = make_rows(rng, rng.randint(20, 120), tag)
    for r in rows[:5]:
        r[0] = r[0] + '; she said, "no, really"\nsecond line, with a comma'
    write_csv(path, rows)

def good_unicode(rng, path, tag):
    rows = make_rows(rng, rng.randint(20, 120), tag)
    for r in rows[:5]:
        r[0] = "東方 ☆ ♪ " + r[0]
    write_csv(path, rows)

def good_extra_column(rng, path, tag):
    rows = [r + ["pre-labelled"] for r in make_rows(rng, rng.randint(20, 120), tag)]
    write_csv(path, rows, header=("text", "label", "note"))

def good_swapped_columns(rng, path, tag):
    rows = [[label, text] for text, label in make_rows(rng, rng.randint(20, 120), tag)]
    write_csv(path, rows, header=("label", "text"))

def good_long_text(rng, path, tag):
    rows = make_rows(rng, rng.randint(20, 60), tag)
    for r in rows[:3]:
        r[0] = r[0] + (" word" * 800)
    write_csv(path, rows)

def good_smallest_valid(rng, path, tag):
    write_csv(path, make_rows(rng, 12, tag))

def good_large(rng, path, tag):
    write_csv(path, make_rows(rng, 300, tag))


GOOD_VARIANTS = [
    ("plain", good_plain),
    ("crlf_line_endings", good_crlf),
    ("utf8_bom", good_bom),
    ("commas_quotes_newlines_in_text", good_punctuation_and_newlines),
    ("unicode_text", good_unicode),
    ("extra_column", good_extra_column),
    ("columns_in_other_order", good_swapped_columns),
    ("very_long_text", good_long_text),
    ("smallest_valid_file", good_smallest_valid),
    ("large_file", good_large),
]   # 10 kinds x 10 files = 100 good inputs


# ---- bad inputs -----------------------------------------------------------

def bad_file_missing(rng, path, i, tag):
    pass  # nothing is created

def bad_file_empty(rng, path, i, tag):
    path.write_bytes(b"")

def bad_columns_missing(rng, path, i, tag):
    rows = make_rows(rng, 30, tag)
    kind = i % 4
    if kind == 0:
        write_csv(path, rows, header=("body", "tag"))
    elif kind == 1:
        write_csv(path, rows, delimiter=";")
    elif kind == 2:
        write_csv(path, rows, header=("Text", "Label"))
    else:
        write_csv(path, [[r[0]] for r in rows], header=("text",))

def bad_no_rows(rng, path, i, tag):
    write_csv(path, [], lineterminator="\r\n" if i % 2 else "\n")

def bad_empty_text(rng, path, i, tag):
    rows = make_rows(rng, 30, tag)
    rows[rng.randrange(len(rows))][0] = ["", "   ", "\t", " \n "][i % 4]
    write_csv(path, rows)

def bad_label_blank(rng, path, i, tag):
    rows = make_rows(rng, 30, tag)
    rows[rng.randrange(len(rows))][1] = ""
    write_csv(path, rows)

def bad_label_unknown(rng, path, i, tag):
    rows = make_rows(rng, 30, tag)
    rows[rng.randrange(len(rows))][1] = ["Hot_take", "analyse", "other", "hot take"][i % 4]
    write_csv(path, rows)

def bad_duplicates(rng, path, i, tag):
    rows = make_rows(rng, 30, tag)
    a, b = rng.sample(range(len(rows)), 2)
    rows[b][0] = rows[a][0]
    write_csv(path, rows)

def bad_label_too_thin(rng, path, i, tag):
    keep = i % 3  # 0, 1 or 2 rows of one label
    thin = rng.choice(LABELS)
    rows = [r for r in make_rows(rng, 40, tag) if r[1] != thin]
    rows += [[make_text(rng, f"{tag}-thin-{k}"), thin] for k in range(keep)]
    rng.shuffle(rows)
    write_csv(path, rows)

def bad_label_dominant(rng, path, i, tag):
    big = rng.choice(LABELS)
    others = [l for l in LABELS if l != big]
    rows = [[make_text(rng, f"{tag}-big-{k}"), big] for k in range(rng.randint(35, 50))]
    for label in others:
        rows += [[make_text(rng, f"{tag}-{label}-{k}"), label] for k in range(3)]
    rng.shuffle(rows)
    write_csv(path, rows)

def bad_unreadable(rng, path, i, tag):
    path.write_bytes(bytes(rng.randrange(128, 256) for _ in range(2000)))

# Not covered by any of the gate's checks. These are in the set on purpose, so
# the 75% target can actually be missed.

def bad_near_duplicates(rng, path, i, tag):
    rows = make_rows(rng, 30, tag)
    source = rng.choice(rows)
    rows.append([source[0].upper(), source[1]])   # same post, different case
    write_csv(path, rows)

def bad_punctuation_only_text(rng, path, i, tag):
    rows = make_rows(rng, 30, tag)
    for k, r in enumerate(rng.sample(rows, 3)):
        r[0] = ["!" * (3 + k), "?" * (3 + k), "." * (3 + k)][k]
    write_csv(path, rows)

def bad_directory_not_file(rng, path, i, tag):
    path.mkdir()


# name, count, generator, covered by a gate check?
BAD_MIX = [
    ("file_missing",           8, bad_file_missing,           True),
    ("file_empty",             8, bad_file_empty,             True),
    ("columns_missing",        8, bad_columns_missing,        True),
    ("no_rows",                8, bad_no_rows,                True),
    ("empty_text",             8, bad_empty_text,             True),
    ("label_blank",            8, bad_label_blank,            True),
    ("label_unknown",          8, bad_label_unknown,          True),
    ("duplicates",             8, bad_duplicates,             True),
    ("label_too_thin",         8, bad_label_too_thin,         True),
    ("label_dominant",         8, bad_label_dominant,         True),
    ("file_unreadable",        4, bad_unreadable,             True),
    ("near_duplicates",        6, bad_near_duplicates,        False),
    ("punctuation_only_text",  6, bad_punctuation_only_text,  False),
    ("directory_not_file",     4, bad_directory_not_file,     False),
]   # totals 100


# --------------------------------------------------------------------------
# Reading logs
# --------------------------------------------------------------------------

def read_jsonl(path):
    records, bad_lines = [], 0
    if not Path(path).exists():
        return records, bad_lines
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            bad_lines += 1
    return records, bad_lines


def record_is_complete(rec):
    """The definition of a complete record from criterion 2."""
    try:
        out = rec["output"]
        return (
            isinstance(rec["timestamp"], str) and rec["timestamp"] != ""
            and isinstance(rec["input"], dict) and bool(rec["input"].get("data"))
            and out["status"] in ("ok", "refused", "error")
            and isinstance(out["message"], str) and out["message"] != ""
            and (out["status"] == "ok" or bool(out.get("code")))
            and isinstance(rec["duration_ms"], (int, float)) and rec["duration_ms"] >= 0
        )
    except (KeyError, TypeError):
        return False


# --------------------------------------------------------------------------
# The five measurements
# --------------------------------------------------------------------------

def measure_bad_and_logging(rng, work, out_dir, trial):
    """Criteria 1 and 2: 100 bad files through run.py's run_once."""
    bad_dir = out_dir / "bad"
    bad_dir.mkdir(parents=True)
    inputs_dir = work / "bad_inputs"
    inputs_dir.mkdir()
    run_log = bad_dir / "run_log.jsonl"

    attempted, by_category = [], {}
    previous_cwd = os.getcwd()
    os.chdir(bad_dir)  # so guard_log.jsonl lands beside run_log.jsonl
    try:
        number = 0
        for name, count, generator, covered in BAD_MIX:
            by_category[name] = {"n": count, "covered_by_gate": covered,
                                 "blocked": 0, "refused_codes": {}, "statuses": {}}
            for i in range(count):
                path = inputs_dir / f"{name}_{i}.csv"
                generator(rng, path, i, f"t{trial}-{name}-{i}")
                number += 1
                record, _ok = run_once(number, Namespace(data=str(path), seed=42,
                                                         log=str(run_log)), LABELS)
                out = record["output"]
                cat = by_category[name]
                cat["statuses"][out["status"]] = cat["statuses"].get(out["status"], 0) + 1
                if out["status"] == "refused":
                    cat["blocked"] += 1
                    code = out.get("code") or "-"
                    cat["refused_codes"][code] = cat["refused_codes"].get(code, 0) + 1
                attempted.append(str(path))
    finally:
        os.chdir(previous_cwd)

    blocked = sum(c["blocked"] for c in by_category.values())
    unexpected = sum(c["refused_codes"].get("unexpected", 0) for c in by_category.values())
    c1 = {"attempted": len(attempted), "blocked": blocked,
          "blocked_with_code_unexpected": unexpected,
          "not_blocked": len(attempted) - blocked,
          "target": C1_TARGET, "by_category": by_category,
          "met": blocked >= C1_TARGET}

    run_records, run_bad_lines = read_jsonl(run_log)
    guard_records, guard_bad_lines = read_jsonl(bad_dir / "guard_log.jsonl")
    logged_paths = [r.get("input", {}).get("data") for r in run_records]
    complete = sum(1 for r in run_records if record_is_complete(r))
    c2 = {"attempted": len(attempted),
          "run_log_records": len(run_records),
          "run_log_unreadable_lines": run_bad_lines,
          "complete_records": complete,
          "guard_log_records": len(guard_records),
          "guard_log_unreadable_lines": guard_bad_lines,
          "every_input_logged_once": sorted(logged_paths) == sorted(attempted),
          "met": (len(run_records) == len(attempted) and complete == len(attempted)
                  and len(guard_records) == len(attempted)
                  and run_bad_lines == 0 and guard_bad_lines == 0
                  and sorted(logged_paths) == sorted(attempted))}
    return c1, c2


def measure_good(rng, work, out_dir, trial):
    """Criterion 4: 100 good files through the gate."""
    import pandas as pd

    good_dir = out_dir / "good"
    good_dir.mkdir(parents=True)
    inputs_dir = work / "good_inputs"
    inputs_dir.mkdir()
    log = good_dir / "guard_log.jsonl"

    passed, refusals, by_variant = 0, [], {}
    for name, generator in GOOD_VARIANTS:
        by_variant[name] = {"n": 10, "passed": 0}
        for i in range(10):
            path = inputs_dir / f"{name}_{i}.csv"
            generator(rng, path, f"t{trial}-{name}-{i}")
            try:
                df = validate_dataset(path, LABELS, log_path=log)
                if df.equals(pd.read_csv(path)):
                    passed += 1
                    by_variant[name]["passed"] += 1
                else:
                    refusals.append({"variant": name, "file": path.name,
                                     "problem": "frame differs from pd.read_csv"})
            except GuardError as exc:
                refusals.append({"variant": name, "file": path.name,
                                 "code": exc.code, "message": exc.message})
    return {"attempted": 100, "passed": passed, "target": C4_TARGET,
            "by_variant": by_variant, "refusals": refusals[:20],
            "met": passed >= C4_TARGET}


def run_script(args, cwd):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    return subprocess.run([sys.executable, str(REPO / "run.py"), *args], cwd=cwd,
                          capture_output=True, text=True, timeout=1800, env=env)


def measure_original(out_dir):
    """Criterion 3: the original system, on the real labels.csv."""
    import pandas as pd

    orig_dir = out_dir / "original"
    orig_dir.mkdir(parents=True)
    labels_csv = REPO / "labels.csv"
    reference = json.loads((REPO / "results.json").read_text(encoding="utf-8"))
    want = {"accuracy": round(reference["accuracy"], 4),
            "f1_macro": round(reference["f1_macro"], 4),
            "n_test": reference["n_test"]}

    try:
        frame_unchanged = validate_dataset(labels_csv, LABELS,
                                           log_path=orig_dir / "guard_log_gate_only.jsonl"
                                           ).equals(pd.read_csv(labels_csv))
    except GuardError:
        frame_unchanged = False

    log = orig_dir / "run_log.jsonl"
    proc = run_script(["--data", str(labels_csv), "--seed", "42", "--log", str(log)], orig_dir)
    records, _ = read_jsonl(log)
    got = {}
    if records:
        out = records[-1]["output"]
        got = {"status": out.get("status"), "accuracy": out.get("accuracy"),
               "f1_macro": out.get("f1_macro"), "n_test": out.get("n_test"),
               "n_train": out.get("n_train"), "message": out.get("message")}
    matches = (got.get("status") == "ok" and got.get("accuracy") == want["accuracy"]
               and got.get("f1_macro") == want["f1_macro"] and got.get("n_test") == want["n_test"])
    return {"reference_results_json": want, "run_py_result": got,
            "gate_returns_frame_unchanged": frame_unchanged,
            "run_py_exit_code": proc.returncode,
            "run_py_matches_results_json": matches,
            "met": bool(frame_unchanged and matches)}


def measure_timing(out_dir):
    """Criterion 5: one process, ten runs. Run 1 is cold, runs 2 to 10 are warm."""
    timing_dir = out_dir / "timing"
    timing_dir.mkdir(parents=True)
    log = timing_dir / "run_log.jsonl"
    proc = run_script(["--data", str(REPO / "labels.csv"), "--runs", "10",
                       "--log", str(log)], timing_dir)
    records, _ = read_jsonl(log)
    seconds = [r["duration_ms"] / 1000 for r in records if r["output"]["status"] == "ok"]
    result = {"run_py_exit_code": proc.returncode, "successful_runs": len(seconds),
              "seconds_per_run": [round(s, 2) for s in seconds],
              "first_max_s": C5_FIRST_MAX_S, "rest_max_s": C5_REST_MAX_S}
    if len(seconds) == 10:
        result.update({"first_run_s": round(seconds[0], 2),
                       "rest_mean_s": round(sum(seconds[1:]) / 9, 2),
                       "rest_max_s_observed": round(max(seconds[1:]), 2),
                       "met": seconds[0] <= C5_FIRST_MAX_S and max(seconds[1:]) <= C5_REST_MAX_S})
    else:
        result.update({"met": False, "note": "fewer than 10 runs succeeded, see run_log.jsonl"})
    return result


# --------------------------------------------------------------------------
# Trial and report
# --------------------------------------------------------------------------

def run_trial(trial):
    out_dir = RESULTS_DIR / f"trial_{trial}"
    if out_dir.exists():
        print(f"{out_dir} already exists. A finished trial is evidence; not overwriting.")
        print("Delete the folder yourself only if you are certain it was a failed attempt.")
        return 1
    out_dir.mkdir(parents=True)
    rng = random.Random(1000 + trial)
    started = datetime.now(timezone.utc).isoformat(timespec="seconds")
    summary = {"trial": trial, "started": started, "python": sys.version.split()[0],
               "platform": platform.platform()}

    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        print(f"Trial {trial}: 100 bad inputs through run.py (criteria 1 and 2)...", flush=True)
        summary["c1"], summary["c2"] = measure_bad_and_logging(rng, work, out_dir, trial)
        print(f"  blocked {summary['c1']['blocked']}/100, "
              f"complete log records {summary['c2']['complete_records']}/100", flush=True)

        print("Trial: 100 good inputs through the gate (criterion 4)...", flush=True)
        summary["c4"] = measure_good(rng, work, out_dir, trial)
        print(f"  passed {summary['c4']['passed']}/100", flush=True)

    print("Trial: original system on labels.csv (criterion 3)...", flush=True)
    summary["c3"] = measure_original(out_dir)
    print(f"  {summary['c3']['run_py_result']}", flush=True)

    print("Trial: ten runs in one process (criterion 5)...", flush=True)
    summary["c5"] = measure_timing(out_dir)
    print(f"  {summary['c5'].get('seconds_per_run')}", flush=True)

    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"\nWrote {out_dir / 'summary.json'}")
    for n, key in enumerate(("c1", "c2", "c3", "c4", "c5"), 1):
        print(f"  criterion {n}: {'target met this trial' if summary[key]['met'] else 'target missed this trial'}")
    print(f"\nCommit {RESULTS_DIR.name}/ when all three trials are done. "
          "Do not run this trial again; run the next one.")
    return 0


def cell(summary, key):
    s = summary[key]
    if key == "c1":
        return f"{s['blocked']}/100"
    if key == "c2":
        return f"{s['complete_records']}/100 complete, {s['run_log_records']} records"
    if key == "c3":
        r = s["run_py_result"]
        return (f"acc {r.get('accuracy')}, F1 {r.get('f1_macro')}"
                if r.get("status") == "ok" else f"{r.get('status', 'no record')}")
    if key == "c4":
        return f"{s['passed']}/100"
    if "first_run_s" in s:
        return f"first {s['first_run_s']}s, rest max {s['rest_max_s_observed']}s"
    return f"{s['successful_runs']}/10 runs ok"


def report():
    summaries = []
    for n in (1, 2, 3):
        path = RESULTS_DIR / f"trial_{n}" / "summary.json"
        if not path.exists():
            print(f"Missing {path}. Run trial {n} first.")
            return 1
        summaries.append(json.loads(path.read_text(encoding="utf-8")))

    rows = [
        ("c1", "1. At least 75% of 100 bad inputs blocked", ">= 75 of 100"),
        ("c2", "2. Every bad-input run logged, completely", "100 of 100 complete, none missing"),
        ("c3", "3. Original still works (seed 42, vs results.json)",
         f"accuracy {summaries[0]['c3']['reference_results_json']['accuracy']}, "
         f"macro F1 {summaries[0]['c3']['reference_results_json']['f1_macro']}"),
        ("c4", "4. At least 90% of 100 good inputs pass", ">= 90 of 100"),
        ("c5", "5. Run 1 <= 8 s and runs 2-10 <= 2 s", "all of runs 2-10 under 2.0 s"),
    ]
    print("| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |")
    print("|---|---|---|---|---|---|")
    for key, name, target in rows:
        cells = " | ".join(cell(s, key) for s in summaries)
        verdict = "MET" if all(s[key]["met"] for s in summaries) else "MISSED"
        print(f"| {name} | {target} | {cells} | {verdict} |")

    t1 = summaries[0]
    print("\n\n--- Real output from trial 1, for the README ---\n")
    print("Criterion 1 (run.py run_once, guard.py validate_dataset): by kind of bad input")
    print("kind, covered by a gate check?, blocked / attempted, refusal codes, all statuses")
    for name, c in t1["c1"]["by_category"].items():
        print(f"  {name:<24} {'yes' if c['covered_by_gate'] else 'NO ':<4} "
              f"{c['blocked']}/{c['n']}   {c['refused_codes']}   {c['statuses']}")
    print(f"  blocked {t1['c1']['blocked']} of {t1['c1']['attempted']}; "
          f"{t1['c1']['blocked_with_code_unexpected']} of those refused as 'unexpected'\n")
    print("Criterion 2 (run.py run_once, run_log.jsonl):")
    print({k: v for k, v in t1["c2"].items() if k != "met"}, "\n")
    print("Criterion 3 (run.py train_and_score vs results.json):")
    print(json.dumps({k: v for k, v in t1["c3"].items() if k != "met"}, indent=2), "\n")
    print("Criterion 4 (guard.py validate_dataset): by kind of good input")
    for name, c in t1["c4"]["by_variant"].items():
        print(f"  {name:<32} {c['passed']}/{c['n']}")
    for r in t1["c4"]["refusals"]:
        print("  refused:", r)
    print("\nCriterion 5 (run.py main, --runs 10): seconds per run")
    print(" ", t1["c5"].get("seconds_per_run"), "\n")
    print("Per-trial values, so the spread is visible:")
    for s in summaries:
        print(f"  trial {s['trial']}: c1 {s['c1']['blocked']}  c2 {s['c2']['complete_records']}  "
              f"c3 {s['c3']['run_py_result'].get('accuracy')}  c4 {s['c4']['passed']}  "
              f"c5 {s['c5'].get('seconds_per_run')}")
    return 0


def load_trials(folder):
    summaries = []
    for n in (1, 2, 3):
        path = folder / f"trial_{n}" / "summary.json"
        if not path.exists():
            print(f"Missing {path}. Run that trial first.")
            return None
        summaries.append(json.loads(path.read_text(encoding="utf-8")))
    return summaries


def compare():
    """Before and after, side by side. Reads both folders, changes nothing."""
    before = load_trials(REPO / "capstone_results")
    after = load_trials(REPO / "capstone_results_after")
    if before is None or after is None:
        return 1

    rows = [
        ("c1", "1. Bad inputs blocked", ">= 75 of 100"),
        ("c2", "2. Bad-input runs logged completely", "100 of 100"),
        ("c3", "3. Original still works", "acc 0.5, F1 0.2222"),
        ("c4", "4. Good inputs pass", ">= 90 of 100"),
        ("c5", "5. Run 1 <= 8 s, runs 2-10 <= 2 s", "see criteria.md"),
    ]

    def verdict(summaries, key):
        return "MET" if all(s[key]["met"] for s in summaries) else "MISSED"

    print("| Criterion | Target | Before: run 1 / 2 / 3 | After: run 1 / 2 / 3 | Before | After |")
    print("|---|---|---|---|---|---|")
    for key, name, target in rows:
        b = " / ".join(cell(s, key) for s in before)
        a = " / ".join(cell(s, key) for s in after)
        print(f"| {name} | {target} | {b} | {a} | {verdict(before, key)} | {verdict(after, key)} |")

    print("\nSeconds per run, criterion 5 (run 1 is cold, runs 2 to 10 are warm):\n")
    print("| Trial | Before: run 1 | Before: runs 2-10 mean / max | After: run 1 | After: runs 2-10 mean / max |")
    print("|---|---|---|---|---|")
    for b, a in zip(before, after):
        def parts(s):
            t = s["c5"]
            if "first_run_s" not in t:
                return "n/a", "n/a"
            return f"{t['first_run_s']} s", f"{t['rest_mean_s']} / {t['rest_max_s_observed']} s"
        bf, br = parts(b)
        af, ar = parts(a)
        print(f"| {b['trial']} | {bf} | {br} | {af} | {ar} |")

    print("\nAll seconds, trial 1:")
    print("  before:", before[0]["c5"].get("seconds_per_run"))
    print("  after: ", after[0]["c5"].get("seconds_per_run"))
    return 0


def main():
    global RESULTS_DIR
    parser = argparse.ArgumentParser(description="Milestone 5 and 6 test harness.")
    parser.add_argument("--trial", type=int, choices=(1, 2, 3), help="run one trial")
    parser.add_argument("--report", action="store_true", help="print the run-log table")
    parser.add_argument("--compare", action="store_true",
                        help="before and after side by side (Milestone 6)")
    parser.add_argument("--label", choices=("before", "after"), default="before",
                        help="'after' writes to capstone_results_after/ (Milestone 6)")
    args = parser.parse_args()
    if args.label == "after":
        RESULTS_DIR = REPO / "capstone_results_after"
    if args.compare:
        return compare()
    if args.report:
        return report()
    if args.trial:
        return run_trial(args.trial)
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())