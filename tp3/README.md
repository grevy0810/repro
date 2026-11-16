# TP3 — Reproducible variability experiment

TP3 studies how implementation choices and runtime environments affect
floating-point results. It samples configurations from a feature model, runs
each configuration repeatedly, and analyzes the recorded results.

## Architecture

- `fm/experiment.uvl` defines the factors and valid combinations.
- `configs/*.csvconf` define the TP1, TP2, and TP3 anchor configurations;
  `configs/sample.csv` and the results CSVs contain generated data.
- `sample.py` samples valid configurations and writes the sample CSV.
- `run_sample.py` derives the effective settings, compiles the Java worker as
  needed, runs the Java or Python worker, and records the results and execution
  metadata.
- `JavaSampleExperiment.java` and `PythonSampleExperiment.py` implement the
  instrumented floating-point experiments.
- `merge_results.py` merges the per-environment CSV files produced by the
  GitHub Actions matrix.
- `analyze_results.ipynb` reads the result CSVs and produces descriptive
  comparisons; it does not generate or modify experiment data.
- `.github/workflows/tp3-experiments.yml` runs the seeded sample across a
  Python/Java version matrix and commits the merged sample and results.

## Reproduce the sample

From this directory, with Python 3.11 or later, create an isolated environment
and install the pinned dependencies:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Then run:

```bash
.venv/bin/python sample.py fm/experiment.uvl \
  --size 30 \
  --seed 1 \
  --include configs/tp1_original.csvconf \
            configs/tp2_llm_python.csvconf \
            configs/tp3_llm_java.csvconf \
  -o configs/sample.csv
```

The script prints the total number of valid model configurations and writes
the selected configurations to `configs/sample.csv`. The output contains the
three anchors plus 30 randomly selected configurations.

The sample size of 30 is a manageable first exploration: it is small enough to
inspect and execute easily, but large enough to expose combinations across the
model's factors. It is not intended to provide statistical guarantees or to
replace an exhaustive run.

To check reproducibility, run the exact command twice and compare the output:

```bash
cp configs/sample.csv /tmp/sample-first.csv
.venv/bin/python sample.py fm/experiment.uvl \
  --size 30 \
  --seed 1 \
  --include configs/tp1_original.csvconf \
            configs/tp2_llm_python.csvconf \
            configs/tp3_llm_java.csvconf \
  -o configs/sample.csv
cmp /tmp/sample-first.csv configs/sample.csv
```

`sample.py` fixes `PYTHONHASHSEED` for Flamapy's sampling process so the
combination of the same model, command, and seed yields the same CSV.
The [TP3 GitHub Actions workflow](../.github/workflows/tp3-experiments.yml)
runs this same sampling command as part of the end-to-end experiment.

## Part 6: serialize experiment results

From this directory, compile and run every sampled configuration three times:

```bash
.venv/bin/python run_sample.py
```

This writes `configs/results.csv`. To smoke-test the runner without executing
the whole sample, use `--limit 1 --runs 2`; `--sample` and `--output` can select
different CSV paths.

The runner derives property, numeric type, repetitions, seed, range, and
endpoint behavior from each sample row. It invokes the Java or Python worker
accordingly. Since the sample describes historical implementations while the
experiment also varies their factors, `Implementation` is retained as a
provenance factor; both workers use the same instrumented expressions so
configurations remain comparable.

Each result row includes the original factors, the effective values used by
the worker, the run number, answer count and percentage, exact command,
language runtime version, and runner/matrix versions. For documented seeds, the
three runs use the configured seed followed by the next two integers.
`Seed_NotDocumented` gets a deterministic seed derived from the configuration
ID and run number. Missing ranges and endpoint choices use the historical
implementation's defaults: `Original` uses `[0, 1)`; `LLMGenerated` uses
`[-1e16, 1e16]`. The effective choices are recorded in every result row.

Python's `Float` mode rounds inputs and every arithmetic operation to IEEE
binary32; `Double` uses Python's binary64 float. NumPy's MT19937 generator
provides vectorized random samples so the 100-million-test configurations are
practical to execute. The Java worker uses `java.util.Random`. The random
generator, seed, and exact command are recorded in each result row;
cross-language runs are not expected to use identical random sequences.
The Java worker uses Java `float` and `double` respectively.

## Part 8: analyze results

Install the notebook dependencies and open `analyze_results.ipynb` in Jupyter
or VS Code:

```bash
python -m pip install -r requirements-analysis.txt
jupyter lab analyze_results.ipynb
```

Run all cells from a clean kernel. The notebook reads `configs/results.csv` and
`configs/causal-range-results.csv`; it does not generate or modify experiment
data. The controlled range comparison is run separately:

```bash
.venv/bin/python run_sample.py \
  --sample configs/causal-range-sample.csv \
  --output configs/causal-range-results.csv \
  --runs 3
```

The notebook summarizes effects across sampled configurations, shows a shallow
decision tree as a descriptive aid, compares the TP1/TP2/TP3 anchor results,
and analyzes the paired range experiment. Observational comparisons are not
interpreted as causal effects.

## Part 7: run the experiment matrix in GitHub Actions

The workflow runs on pushes that change `tp3/` and can also be started
manually with **Actions → TP3 variability experiments → Run workflow**. Its
matrix combines Python 3.11/3.12 with Java 21/25 on `ubuntu-24.04`. Each job
regenerates the same seeded sample, runs all configurations, and uploads its
CSV. A final job merges the four files into `configs/results.csv` and commits
the sample and results. The legacy workflow continues to produce TP1/TP2
answers; it no longer samples TP3.

To check a rerun of the same commit, compare the answer columns
(`config_id`, `run_index`, the two matrix version columns, `answer_equal_count`,
and `answer_percentage`) in the generated CSV. With the same tool versions and
seed, the numerical results should be identical. The CSV also records exact
runtime versions and the runner, so a hosted runner image update may change
metadata even when the answers remain the same.

## AI usage statement

The TP2 anchor represents the LLM-generated implementation from `tp2/llm/`.
TP3 models this implementation as one of the historical implementations under
study; its sampling, execution, result merging, and analysis scripts do not
make LLM calls.
