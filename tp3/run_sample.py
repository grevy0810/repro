#!/usr/bin/env python3
"""Derive, run, and serialize every configuration in configs/sample.csv."""

import argparse
import csv
import hashlib
import json
import os
import platform
import shlex
import subprocess
import sys
import time
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent
SAMPLE = ROOT / "configs" / "sample.csv"
OUTPUT = ROOT / "configs" / "results.csv"
JAVA_SOURCE = ROOT / "JavaSampleExperiment.java"
JAVA_CLASS = ROOT / "JavaSampleExperiment.class"
PYTHON_WORKER = ROOT / "PythonSampleExperiment.py"
REQUIRED_COLUMNS = {
    "config_id",
    "origin_of_config",
    "Language",
    "Implementation",
    "Property",
    "NumberType",
    "Repetitions",
    "RandomSeed",
    "NumberRange",
    "UpperBound",
}


def options():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sample", type=Path, default=SAMPLE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--runs", type=int, default=3, help="repetitions per configuration")
    parser.add_argument("--limit", type=int, help="run only the first N configurations (for a smoke test)")
    return parser.parse_args()


def read_sample(path):
    with path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames or not REQUIRED_COLUMNS.issubset(reader.fieldnames):
            missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
            raise ValueError(f"{path} is missing required columns: {sorted(missing)}")
        rows = list(reader)
    if not rows:
        raise ValueError(f"{path} contains no configurations")
    return reader.fieldnames, rows


def derive(row, run_index):
    repetitions = {
        "Tests_1M": 1_000_000,
        "Tests_100M": 100_000_000,
    }.get(row["Repetitions"])
    if repetitions is None:
        raise ValueError(f"Unknown Repetitions value: {row['Repetitions']}")

    if row["RandomSeed"] == "Seed_42":
        base_seed = 42
    elif row["RandomSeed"] == "Seed_123":
        base_seed = 123
    elif row["RandomSeed"] == "Seed_NotDocumented":
        digest = hashlib.sha256(
            f"{row['config_id']}:{run_index}".encode("utf-8")
        ).digest()
        base_seed = int.from_bytes(digest[:4], "big") & 0x7FFFFFFF
    else:
        raise ValueError(f"Unknown RandomSeed value: {row['RandomSeed']}")

    actual_seed = base_seed + run_index - 1
    if row["NumberRange"] == "Range_Symmetric_1e16":
        minimum, maximum = -1e16, 1e16
    elif row["NumberRange"] == "Range_UnitInterval":
        minimum, maximum = 0.0, 1.0
    elif row["NumberRange"] == "Range_NotDocumented":
        minimum, maximum = (
            (0.0, 1.0)
            if row["Implementation"] == "Original"
            else (-1e16, 1e16)
        )
    else:
        raise ValueError(f"Unknown NumberRange value: {row['NumberRange']}")

    if row["UpperBound"] == "Inclusive":
        inclusive = True
    elif row["UpperBound"] == "Exclusive":
        inclusive = False
    elif row["UpperBound"] == "NotDocumented":
        inclusive = row["Implementation"] != "Original"
    else:
        raise ValueError(f"Unknown UpperBound value: {row['UpperBound']}")

    return {
        "repetitions": repetitions,
        "seed": actual_seed,
        "minimum": minimum,
        "maximum": maximum,
        "inclusive": inclusive,
    }


def compile_java():
    subprocess.run(
        ["javac", "-d", str(ROOT), str(JAVA_SOURCE)],
        check=True,
        cwd=ROOT,
    )


def run_configuration(row, parameters):
    common = [
        "--tests", str(parameters["repetitions"]),
        "--seed", str(parameters["seed"]),
        "--min", repr(parameters["minimum"]),
        "--max", repr(parameters["maximum"]),
        "--type", row["NumberType"],
        "--property", row["Property"],
    ]
    if parameters["inclusive"]:
        common.append("--inclusive")

    if row["Language"] == "Python":
        command = [
            sys.executable,
            str(PYTHON_WORKER),
            *common,
        ]
    elif row["Language"] == "Java":
        command = [
            "java",
            "-cp",
            str(ROOT),
            "JavaSampleExperiment",
            str(parameters["repetitions"]),
            str(parameters["seed"]),
            repr(parameters["minimum"]),
            repr(parameters["maximum"]),
            row["NumberType"],
            row["Property"],
            str(parameters["inclusive"]).lower(),
        ]
    else:
        raise ValueError(f"Unknown Language value: {row['Language']}")

    started = time.perf_counter()
    completed = subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    elapsed = time.perf_counter() - started
    answer = json.loads(completed.stdout.strip())
    return command, answer, elapsed


def runtime_version(language):
    if language == "Python":
        return f"Python {platform.python_version()} / NumPy {np.__version__}"
    command = ["java", "-version"]
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    return (result.stdout or result.stderr).splitlines()[0]


def main():
    args = options()
    if args.runs < 2:
        raise ValueError("--runs must be at least 2")
    if args.limit is not None and args.limit < 1:
        raise ValueError("--limit must be positive")

    sample_columns, configurations = read_sample(args.sample)
    if args.limit is not None:
        configurations = configurations[:args.limit]

    if any(row["Language"] == "Java" for row in configurations):
        compile_java()

    result_columns = [
        "config_id",
        "origin_of_config",
        *[column for column in sample_columns if column not in ("config_id", "origin_of_config")],
        "ExactEquality",
        "run_index",
        "effective_repetitions",
        "actual_seed",
        "effective_min",
        "effective_max",
        "effective_upper_bound",
        "answer_equal_count",
        "answer_percentage",
        "random_generator",
        "runtime_version",
        "platform",
        "command",
        "duration_seconds",
    ]

    args.output.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with args.output.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=result_columns)
        writer.writeheader()
        for row in configurations:
            for run_index in range(1, args.runs + 1):
                parameters = derive(row, run_index)
                command, answer, elapsed = run_configuration(row, parameters)
                writer.writerow({
                    **row,
                    "ExactEquality": "True",
                    "run_index": run_index,
                    "effective_repetitions": parameters["repetitions"],
                    "actual_seed": parameters["seed"],
                    "effective_min": repr(parameters["minimum"]),
                    "effective_max": repr(parameters["maximum"]),
                    "effective_upper_bound": "inclusive" if parameters["inclusive"] else "exclusive",
                    "answer_equal_count": answer["equal"],
                    "answer_percentage": answer["percentage"],
                    "random_generator": "NumPy MT19937" if row["Language"] == "Python" else "java.util.Random",
                    "runtime_version": runtime_version(row["Language"]),
                    "platform": platform.platform(),
                    "command": json.dumps(command),
                    "duration_seconds": f"{elapsed:.6f}",
                })
                file.flush()
                count += 1
                print(
                    f"{row['config_id']} run {run_index}/{args.runs}: "
                    f"{answer['percentage']:.6f}% ({elapsed:.2f}s)",
                    flush=True,
                )

    print(
        f"Wrote {count} runs for {len(configurations)} configurations "
        f"to {args.output}"
    )


if __name__ == "__main__":
    main()
