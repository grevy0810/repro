# Reproducibility lab

This repository compares floating-point programs from three lab exercises and
studies how implementation and runtime choices affect their results. Generated
answers and experiment data are kept alongside the code that produces them.

## Repository architecture

| Path | Purpose |
| --- | --- |
| `tp1/` | Original Java implementations, Docker setup, and generated answer files. |
| `tp2/llm/` | LLM-generated Python implementations, their prompts, Docker setup, and answer files. |
| `tp3/` | Feature model, configuration sampler, Java/Python experiment workers, results, and analysis notebook. |
| `.github/workflows/` | Actions to generate TP1/TP2 answers and run the TP3 experiment matrix. |
| `shell.nix`, `nixpkgs-pin.nix` | Pinned Nix development shell for reproducing TP1. |

TP3's `sample.py` reads `fm/experiment.uvl` and writes configurations to
`configs/`. `run_sample.py` derives experiment parameters from those
configurations, runs the Java or Python worker, and records the runtime and
command with each result. `merge_results.py` combines the per-environment CSVs
created by GitHub Actions. `analyze_results.ipynb` analyzes the recorded data;
it does not generate experiment results.

## Reproduce the results

### TP1 — Java

With Java 21 or later, from the repository root:

```bash
javac tp1/Associativity.java tp1/BankingProblem.java
./tp1/run.sh
```

The answer files are `tp1/answer_associativity.txt` and
`tp1/answer_banking.txt`. Alternatively, run TP1 in Docker:

```bash
docker build -f tp1/Dockerfile -t rep-lab2 .
docker run --rm --user "$(id -u):$(id -g)" \
  -v "$(pwd):/out" -e OUTPUT_DIR=/out/tp1 rep-lab2
```

To use the pinned Nix environment, install [Nix](https://nixos.org/download/)
and run `nix-shell` from the repository root before compiling and running TP1.

### TP2 — LLM-generated Python

From the repository root, run the programs with Python 3:

```bash
python3 tp2/llm/associativity.py
python3 tp2/llm/banking.py
```

Their prompts and generated answer files are in `tp2/llm/`. To run them in
Docker:

```bash
docker build -f tp2/llm/Dockerfile.llm -t rep-lab2-llm .
docker run --rm --user "$(id -u):$(id -g)" \
  -v "$(pwd):/out" -e OUTPUT_DIR=/out/tp2/llm rep-lab2-llm
```

### TP3 — sampled variability experiment

Use Python 3.11 or later and Java 21 or later. From the repository root:

```bash
python3 -m venv tp3/.venv
tp3/.venv/bin/python -m pip install -r tp3/requirements.txt
cd tp3
.venv/bin/python sample.py fm/experiment.uvl \
  --size 30 \
  --seed 1 \
  --include configs/tp1_original.csvconf \
            configs/tp2_llm_python.csvconf \
            configs/tp3_llm_java.csvconf \
  -o configs/sample.csv
.venv/bin/python run_sample.py
```

This creates `tp3/configs/sample.csv` (the three anchor configurations plus
30 seeded random configurations) and `tp3/configs/results.csv`. To reproduce
the controlled range comparison used in the analysis, run:

```bash
.venv/bin/python run_sample.py \
  --sample configs/causal-range-sample.csv \
  --output configs/causal-range-results.csv \
  --runs 3
```

Install the notebook dependencies and run all cells in a clean Jupyter or VS
Code kernel to analyze the results:

```bash
.venv/bin/python -m pip install -r requirements-analysis.txt
jupyter lab analyze_results.ipynb
```

The TP3 GitHub Actions workflow runs the seeded sampling and experiment for
Python 3.11/3.12 and Java 21/25 on `ubuntu-24.04`, then merges the results. It
can run automatically after changes under `tp3/` or be started from the Actions
tab. The separate “Generate Answers” workflow produces the TP1/TP2 answer
files.

## AI usage statement

An LLM was used to generate the TP2 Python implementations. The prompts and
resulting programs are included in `tp2/llm/` for inspection. The TP3 sampling,
experiment execution, and analysis use the repository's scripts and recorded
data; they do not make LLM calls.
