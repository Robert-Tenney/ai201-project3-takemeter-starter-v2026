#!/usr/bin/env python3
"""
Command-line front end for guard.py. Capstone, Shape B.

    python validate.py
    python validate.py --data labels.csv
    python validate.py --data labels.csv --labels request,experience,hot_take,analysis

Exit code 0 means the file passed. Exit code 1 means it was refused, with one
named reason printed. Either way a record is appended to guard_log.jsonl.
"""

import argparse
import sys

from guard import DEFAULT_LABELS, LOG_PATH, GuardError, validate_dataset

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, OSError, ValueError):
        pass


def main():
    parser = argparse.ArgumentParser(description="Validate a TakeMeter labels CSV before training.")
    parser.add_argument("--data", default="labels.csv", help="the labelled CSV")
    parser.add_argument("--labels", default=",".join(DEFAULT_LABELS),
                        help="comma-separated labels, exactly as in the notebook's LABELS")
    parser.add_argument("--log", default=LOG_PATH, help="where to append the structured log")
    args = parser.parse_args()

    labels = [l.strip() for l in args.labels.split(",") if l.strip()]

    try:
        df = validate_dataset(args.data, labels, log_path=args.log)
    except GuardError as exc:
        print(f"REFUSED  {exc}")
        print(f"(logged to {args.log})")
        return 1

    print(f"PASSED   {len(df)} rows, {len(labels)} labels")
    print(f"(logged to {args.log})")
    return 0


if __name__ == "__main__":
    sys.exit(main())