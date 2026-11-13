#!/usr/bin/env python3
"""
run.py - the single start command for TakeMeter. Capstone, Shape B.

    python run.py                      one gated training run, seed 42
    python run.py --runs 10            ten runs, prints the mean seconds per run
    python run.py --data bad.csv       a refused run (the failure path)

One run does three things, in order:
  1. validate the CSV through guard.py (refuses bad input with a named reason)
  2. split, fine-tune and score exactly as the notebook does (same split, same
     settings, same seed handling), on the held-out test posts
  3. append ONE structured record to run_log.jsonl, pass or fail

Every record has: timestamp, input (what came in), output (what came out) and
duration_ms (how long the whole run took), plus stage timings. A refused or
crashed run leaves a record too, so a failure never shows up only as an absence.

The notebook is still the place to read the full results. This script does not
write results.json, test_split.csv or the three-seed files, so it cannot
overwrite your evidence.
"""

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from guard import DEFAULT_LABELS, GuardError, validate_dataset

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, OSError, ValueError):
        pass

# Same defaults as the notebook's section 2. Not changed in this unit.
BASE_MODEL = "distilbert-base-uncased"
EPOCHS = 3
LEARNING_RATE = 2e-5
BATCH_SIZE = 16
MAX_LENGTH = 128

RUN_LOG = "run_log.jsonl"


def append_record(record, path):
    """One JSON line per run. Logging must never be what crashes a run."""
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except OSError as exc:
        print(f"[warn] could not write {path}: {exc}", file=sys.stderr)


def offline_first(load):
    """
    Load model files from the local cache first, and only go to the Hub if they
    are not there. `load` takes one argument, local_files_only.

    Without this, every run asks the Hub whether the cached files are still
    current, which is network time spent on files that are already on disk.
    Returns (whatever load returned, "cache" or "hub") so the log says which
    way it went. Any error other than a missing file is not swallowed.
    """
    try:
        return load(local_files_only=True), "cache"
    except (OSError, ValueError):
        return load(local_files_only=False), "hub"


def split_dataset(df, seed, test_size=0.15, val_size=0.15):
    """Stratified 70/15/15. Copied from the notebook's section 3, unchanged."""
    from sklearn.model_selection import train_test_split

    def _stratify_on(frame):
        counts = frame["label"].value_counts()
        return frame["label"] if counts.min() >= 2 else None

    rest, test = train_test_split(
        df, test_size=test_size, random_state=seed, stratify=_stratify_on(df)
    )
    val_share = val_size / (1 - test_size)
    train, val = train_test_split(
        rest, test_size=val_share, random_state=seed, stratify=_stratify_on(rest)
    )
    return (
        train.reset_index(drop=True),
        val.reset_index(drop=True),
        test.reset_index(drop=True),
    )


def train_and_score(df, labels, seed):
    """
    Fine-tune on the train split and score the held-out test split.
    Mirrors the notebook's sections 4 and 5. Heavy imports live here so a
    refused run never pays for loading torch.
    """
    import numpy as np
    import torch
    from datasets import Dataset
    from sklearn.metrics import accuracy_score, f1_score
    from transformers import (
        AutoModelForSequenceClassification, AutoTokenizer,
        Trainer, TrainingArguments, set_seed,
    )

    if torch.cuda.is_available():
        device = "cuda"
    elif getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        device = "mps"
    else:
        device = "cpu"

    train_df, val_df, test_df = split_dataset(df, seed)
    set_seed(seed)

    def load(local_files_only):
        set_seed(seed)  # same starting point whichever way the files load
        tok = AutoTokenizer.from_pretrained(BASE_MODEL, local_files_only=local_files_only)
        mdl = AutoModelForSequenceClassification.from_pretrained(
            BASE_MODEL,
            num_labels=len(labels),
            id2label={i: l for i, l in enumerate(labels)},
            label2id={l: i for i, l in enumerate(labels)},
            local_files_only=local_files_only,
        )
        return tok, mdl

    (tokenizer, model), model_source = offline_first(load)

    def to_ids(frame):
        lookup = {label: i for i, label in enumerate(labels)}
        out = frame.copy()
        out["labels"] = out["label"].astype(str).str.strip().map(lookup)
        return out[["text", "labels"]]

    def tokenize(batch):
        return tokenizer(batch["text"], truncation=True,
                         padding="max_length", max_length=MAX_LENGTH)

    train_ds = Dataset.from_pandas(to_ids(train_df)).map(tokenize, batched=True)
    val_ds = Dataset.from_pandas(to_ids(val_df)).map(tokenize, batched=True)
    test_ds = Dataset.from_pandas(to_ids(test_df)).map(tokenize, batched=True)

    def compute_metrics(eval_pred):
        logits, gold = eval_pred
        predicted = np.argmax(logits, axis=-1)
        return {
            "accuracy": accuracy_score(gold, predicted),
            "f1_macro": f1_score(gold, predicted, average="macro", zero_division=0),
        }

    args = TrainingArguments(
        output_dir="./takemeter_out",
        num_train_epochs=EPOCHS,
        learning_rate=LEARNING_RATE,
        per_device_train_batch_size=BATCH_SIZE,
        per_device_eval_batch_size=BATCH_SIZE,
        eval_strategy="epoch",
        save_strategy="no",
        logging_steps=10,
        seed=seed,
        report_to="none",
        disable_tqdm=True,
    )
    trainer = Trainer(model=model, args=args, train_dataset=train_ds,
                      eval_dataset=val_ds, compute_metrics=compute_metrics)
    trainer.train()

    output = trainer.predict(test_ds)
    predicted = np.argmax(output.predictions, axis=-1)
    gold = np.array(output.label_ids)

    return {
        "accuracy": round(float(accuracy_score(gold, predicted)), 4),
        "f1_macro": round(float(f1_score(gold, predicted, average="macro", zero_division=0)), 4),
        "n_train": int(len(train_df)),
        "n_test": int(len(gold)),
        "device": device,
        "model_source": model_source,
    }


def run_once(number, args, labels):
    """One full run. Returns (record, ok). Always returns a record."""
    start = time.perf_counter()
    record = {
        "run": number,
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "input": {"data": args.data, "seed": args.seed, "labels": labels,
                  "epochs": EPOCHS, "max_length": MAX_LENGTH},
        "output": None,
        "duration_ms": None,
        "stages_ms": {},
    }
    ok = False
    try:
        t0 = time.perf_counter()
        df = validate_dataset(args.data, labels)
        record["stages_ms"]["validate"] = round((time.perf_counter() - t0) * 1000, 1)
        record["input"]["rows"] = int(len(df))

        t1 = time.perf_counter()
        result = train_and_score(df, labels, args.seed)
        record["stages_ms"]["train_and_score"] = round((time.perf_counter() - t1) * 1000, 1)

        record["output"] = {"status": "ok", "code": None, "message": "trained and scored", **result}
        ok = True
    except GuardError as exc:
        record["output"] = {"status": "refused", "code": exc.code, "message": exc.message}
    except Exception as exc:  # anything unplanned is still a recorded failure
        record["output"] = {"status": "error", "code": "unexpected",
                            "message": f"{type(exc).__name__}: {exc}"}
    finally:
        record["duration_ms"] = round((time.perf_counter() - start) * 1000, 1)
        append_record(record, args.log)
    return record, ok


def main():
    parser = argparse.ArgumentParser(description="Gated TakeMeter run with a structured log.")
    parser.add_argument("--data", default="labels.csv", help="the labelled CSV")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--runs", type=int, default=1, help="repeat N times (use 10 to measure cost)")
    parser.add_argument("--log", default=RUN_LOG, help="where to append the structured log")
    parser.add_argument("--labels", default=",".join(DEFAULT_LABELS),
                        help="comma-separated, same order as the notebook's LABELS")
    args = parser.parse_args()
    labels = [l.strip() for l in args.labels.split(",") if l.strip()]

    seconds = []
    exit_code = 0
    for n in range(1, args.runs + 1):
        record, ok = run_once(n, args, labels)
        out = record["output"]
        secs = record["duration_ms"] / 1000
        if ok:
            seconds.append(secs)
            print(f"run {n}/{args.runs}  OK       {secs:6.1f}s  "
                  f"accuracy {out['accuracy']:.3f}  macro F1 {out['f1_macro']:.3f}  "
                  f"({out['device']}, {out['n_test']} test posts)")
        else:
            print(f"run {n}/{args.runs}  {out['status'].upper():<8} {secs:6.1f}s  "
                  f"[{out['code']}] {out['message']}")
            exit_code = 1 if out["status"] == "refused" else 2
            break  # same input would fail the same way

    if seconds:
        mean = sum(seconds) / len(seconds)
        print(f"\n{len(seconds)} successful run(s), mean {mean:.1f}s, "
              f"min {min(seconds):.1f}s, max {max(seconds):.1f}s")
    print(f"(appended to {args.log})")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())