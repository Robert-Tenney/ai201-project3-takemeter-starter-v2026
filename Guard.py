"""
guard.py - the validation gate in front of TakeMeter's split and training.
Capstone, Shape B (harden against failure).

Before this existed, bad input failed silently or noisily in the wrong place:
the notebook printed [FIX ME] and trained anyway, split_dataset quietly dropped
stratification for rare labels, and a missing file or column ended in a raw
traceback. This module checks the CSV first. It either returns the DataFrame
exactly as pandas read it (so good input trains exactly as before) or raises
GuardError with ONE named reason.

Every call writes one structured record to guard_log.jsonl, pass or refuse:
timestamp, what came in, what came out, how long it took.

Used from the notebook:

    from guard import validate_dataset, GuardError
    df = validate_dataset("labels.csv", LABELS)

and from the command line, through validate.py.
"""

import json
import time
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_LABELS = ["request", "experience", "hot_take", "analysis"]
LOG_PATH = "guard_log.jsonl"

# Hard stops. Below the minimum a label cannot survive a stratified
# 70/15/15 split, and above the cap the model learns to guess one label.
MIN_ROWS_PER_LABEL = 3
MAX_LABEL_SHARE = 0.70

# Warnings only. These are real problems but they do not stop a run, because
# the current dataset trips them and has to keep training.
WARN_TOTAL_ROWS = 150
WARN_LABEL_ROWS = 20


class GuardError(Exception):
    """Input was refused. `code` is a short stable name, `message` is one line."""

    def __init__(self, code, message):
        super().__init__(f"[{code}] {message}")
        self.code = code
        self.message = message


def _log(record, log_path):
    """Append one JSON line. Logging must never be the thing that crashes a run."""
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except OSError:
        pass


def _check(path, labels):
    """
    Run every check in order. Returns (df, warnings) or raises GuardError.
    Order matters: each check assumes the ones before it passed.
    """
    import pandas as pd

    p = Path(path)
    if not p.exists():
        raise GuardError("file_missing", f"No file at {path}.")
    if p.stat().st_size == 0:
        raise GuardError("file_empty", f"{path} is empty (0 bytes).")

    try:
        df = pd.read_csv(p)
    except pd.errors.EmptyDataError:
        raise GuardError("file_empty", f"{path} has no rows or header.")
    except (pd.errors.ParserError, UnicodeDecodeError) as exc:
        raise GuardError("file_unreadable", f"{path} could not be parsed as CSV: {type(exc).__name__}.")

    missing = [c for c in ("text", "label") if c not in df.columns]
    if missing:
        raise GuardError(
            "columns_missing",
            f"No {' or '.join(repr(c) for c in missing)} column. Found: {', '.join(map(str, df.columns))}.",
        )

    if len(df) == 0:
        raise GuardError("no_rows", f"{path} has a header but no rows.")

    # A missing cell and a whitespace-only cell are both "no text".
    blank_text = int((df["text"].fillna("").astype(str).str.strip() == "").sum())
    if blank_text:
        raise GuardError("empty_text", f"{blank_text} row(s) have an empty text column.")

    blank_label = int(df["label"].isna().sum())
    if blank_label:
        raise GuardError("label_blank", f"{blank_label} row(s) have no label.")

    found = set(df["label"].astype(str).str.strip())
    unknown = sorted(found - set(labels))
    if unknown:
        raise GuardError(
            "label_unknown",
            f"Labels not in LABELS: {unknown}. Check capitals and spaces.",
        )

    duplicates = int(df["text"].duplicated().sum())
    if duplicates:
        raise GuardError(
            "duplicates",
            f"{duplicates} duplicate post(s). They would land in different splits and leak.",
        )

    counts = df["label"].astype(str).str.strip().value_counts()
    thin = {l: int(counts.get(l, 0)) for l in labels if counts.get(l, 0) < MIN_ROWS_PER_LABEL}
    if thin:
        raise GuardError(
            "label_too_thin",
            f"Fewer than {MIN_ROWS_PER_LABEL} rows for: {thin}. Cannot stratify a split.",
        )

    top_label, top_count = counts.index[0], int(counts.iloc[0])
    if top_count / len(df) > MAX_LABEL_SHARE:
        raise GuardError(
            "label_dominant",
            f"'{top_label}' is {top_count / len(df):.0%} of the data (cap {MAX_LABEL_SHARE:.0%}).",
        )

    warnings = []
    if len(df) < WARN_TOTAL_ROWS:
        warnings.append(f"{len(df)} rows, under the {WARN_TOTAL_ROWS} floor for a submission.")
    small = {l: int(counts[l]) for l in labels if counts[l] < WARN_LABEL_ROWS}
    if small:
        warnings.append(f"Labels under {WARN_LABEL_ROWS} rows: {small}.")
    return df, warnings


def validate_dataset(path, labels=None, log_path=LOG_PATH):
    """
    Validate `path` against `labels`. Returns the DataFrame untouched on a pass.
    Raises GuardError on a refusal. Always writes one log record either way.
    """
    labels = list(labels) if labels is not None else list(DEFAULT_LABELS)
    start = time.perf_counter()
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "input": {"path": str(path), "labels": labels},
        "output": None,
        "duration_ms": None,
    }
    try:
        df, warnings = _check(path, labels)
        record["input"]["rows"] = int(len(df))
        record["output"] = {"status": "pass", "code": None, "message": "ok", "warnings": warnings}
        return df
    except GuardError as exc:
        record["output"] = {"status": "refused", "code": exc.code, "message": exc.message, "warnings": []}
        raise
    except Exception as exc:  # anything unplanned is still a recorded failure
        record["output"] = {"status": "error", "code": "unexpected",
                            "message": f"{type(exc).__name__}: {exc}", "warnings": []}
        raise GuardError("unexpected", f"{type(exc).__name__}: {exc}") from exc
    finally:
        record["duration_ms"] = round((time.perf_counter() - start) * 1000, 2)
        _log(record, log_path)