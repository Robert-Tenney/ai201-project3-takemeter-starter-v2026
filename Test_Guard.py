#!/usr/bin/env python3
"""
Checks that guard.py refuses each kind of bad input with the right code, and
still passes good input. Run:  python test_guard.py
Uses a temporary folder and a temporary log, so it never touches labels.csv
or guard_log.jsonl.
"""

import json
import sys
import tempfile
from pathlib import Path

from guard import GuardError, validate_dataset

LABELS = ["request", "experience", "hot_take", "analysis"]


def good_rows():
    rows = []
    for label, n in (("hot_take", 8), ("request", 4), ("experience", 4), ("analysis", 4)):
        for i in range(n):
            rows.append((f"{label} example number {i}", label))
    return rows


def write_csv(folder, name, rows, header="text,label"):
    path = Path(folder) / name
    lines = [header]
    for text, label in rows:
        lines.append(f'"{text}",{label}')
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def expect(tmp, name, path, code):
    log = Path(tmp) / "log.jsonl"
    try:
        validate_dataset(path, LABELS, log_path=log)
    except GuardError as exc:
        ok = exc.code == code
        print(f"{'ok  ' if ok else 'FAIL'} {name}: refused with {exc.code}" + ("" if ok else f" (wanted {code})"))
        return ok
    print(f"FAIL {name}: was not refused (wanted {code})")
    return False


def main():
    results = []
    with tempfile.TemporaryDirectory() as tmp:
        log = Path(tmp) / "log.jsonl"

        df = validate_dataset(write_csv(tmp, "good.csv", good_rows()), LABELS, log_path=log)
        results.append(len(df) == 20)
        print(f"{'ok  ' if results[-1] else 'FAIL'} good input passes and comes back untouched")

        results.append(expect(tmp, "missing file", Path(tmp) / "nope.csv", "file_missing"))

        empty = Path(tmp) / "empty.csv"
        empty.write_text("", encoding="utf-8")
        results.append(expect(tmp, "zero-byte file", empty, "file_empty"))

        results.append(expect(tmp, "wrong columns", write_csv(tmp, "cols.csv", good_rows(), "body,tag"),
                              "columns_missing"))

        header_only = Path(tmp) / "header.csv"
        header_only.write_text("text,label\n", encoding="utf-8")
        results.append(expect(tmp, "header but no rows", header_only, "no_rows"))

        rows = good_rows()
        rows[0] = ("   ", rows[0][1])
        results.append(expect(tmp, "blank text", write_csv(tmp, "blank.csv", rows), "empty_text"))

        rows = good_rows()
        rows[0] = (rows[0][0], "Hot_take")
        results.append(expect(tmp, "unknown label (capital)", write_csv(tmp, "unk.csv", rows), "label_unknown"))

        rows = good_rows() + [good_rows()[0]]
        results.append(expect(tmp, "duplicate post", write_csv(tmp, "dup.csv", rows), "duplicates"))

        rows = [r for r in good_rows() if r[1] != "analysis"] + [("analysis one", "analysis")]
        results.append(expect(tmp, "label too thin", write_csv(tmp, "thin.csv", rows), "label_too_thin"))

        rows = [(f"hot {i}", "hot_take") for i in range(40)]
        rows += [(f"{l} {i}", l) for l in ("request", "experience", "analysis") for i in range(3)]
        results.append(expect(tmp, "dominant label", write_csv(tmp, "dom.csv", rows), "label_dominant"))

        records = [json.loads(l) for l in log.read_text(encoding="utf-8").splitlines()]
        results.append(records[0]["output"]["status"] == "pass" and {"timestamp", "input", "output", "duration_ms"} <= set(records[0]))
        print(f"{'ok  ' if results[-1] else 'FAIL'} a pass is logged first, with timestamp, input, output and duration_ms")

    print(f"\n{sum(results)} of {len(results)} checks passed")
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())