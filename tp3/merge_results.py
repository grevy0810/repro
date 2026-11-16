#!/usr/bin/env python3
"""Merge per-environment result CSV files into one deterministic CSV."""

import argparse
import csv
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_dir", type=Path)
    parser.add_argument("-o", "--output", type=Path, required=True)
    args = parser.parse_args()

    input_files = sorted(args.input_dir.glob("results-*.csv"))
    if not input_files:
        raise SystemExit(f"No results-*.csv files found in {args.input_dir}")

    columns = None
    rows = []
    for path in input_files:
        with path.open(newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            if reader.fieldnames is None:
                raise SystemExit(f"{path} has no CSV header")
            if columns is None:
                columns = reader.fieldnames
            elif reader.fieldnames != columns:
                raise SystemExit(f"CSV columns differ in {path}")
            rows.extend(reader)

    assert columns is not None
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Merged {len(rows)} result rows from {len(input_files)} environments into {args.output}")


if __name__ == "__main__":
    main()
