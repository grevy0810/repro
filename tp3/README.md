# TP3 — Reproducible variability experiment

TP3 studies how implementation choices and runtime environments affect
floating-point results. It samples configurations from a feature model, runs
each configuration repeatedly, and analyzes the recorded results.

## Architecture

The files are organized into the following stages and supporting materials:

### Experiment definition and documentation

- `fm/experiment.uvl` defines the factors and valid feature combinations.
- `list_possible_factors.md` records candidate variability factors.
- `steps.md` contains the lab instructions and the workflow from initial
  experiments through analysis.
- `comparison_matrix.md` documents the original programs and their observed
  results.
- `README.md` documents how to reproduce the TP3 sample, experiment, and
  analysis.

### Implementations and experiment tools

- `AssociativityCLI.java` is the configurable Java CLI experiment;
  `run_experiments.sh` runs it over a set of seed and range values.
- `AssociativityRuntime.java` explores how results vary with the number of
  repetitions.
- `experiment.java.jinja` is the Java source template, and `generate.py`
  renders, compiles, and executes the generated implementations.
- `generated/AssociativityFloat.java`, `generated/AssociativityDouble.java`,
  `generated/DistributivityFloat.java`, and
  `generated/DistributivityDouble.java` are the generated template examples.
- `llm/AssociativityLLM.java` is the LLM-generated Java implementation.
  `llm/llm.md` records its prompt/model information, and
  `llm/answer_associativity_llm_java.txt` is its recorded output.
- `answer_associativity_llm_java.txt` is the output from the configurable CLI
  experiment.
- `JavaSampleExperiment.java` and `PythonSampleExperiment.py` are the
  instrumented workers used by the sampled experiment.
- `sample.py` samples valid configurations and writes the sample CSV.
  `run_sample.py` derives their effective settings, compiles/runs the matching
  worker, and records results and execution metadata.
- `merge_results.py` merges per-environment result CSVs from the Actions
  matrix.

### Configurations, data, and analysis

- `configs/tp1_original.csvconf`, `configs/tp2_llm_python.csvconf`, and
  `configs/tp3_llm_java.csvconf` define the three anchor configurations.
- `configs/sample.csv` is the generated seeded sample;
  `configs/results.csv` contains the merged matrix results.
- `configs/causal-range-sample.csv` defines the controlled range comparison,
  and `configs/causal-range-results.csv` contains its recorded results.
- `analyze_results.ipynb` reads the result CSVs and produces descriptive
  comparisons; it does not generate or modify experiment data.

### Dependencies and automation

- `requirements.txt` pins the sampling and experiment dependencies.
- `requirements-analysis.txt` lists the notebook analysis dependencies.
- The [TP3 GitHub Actions workflow](../.github/workflows/tp3-experiments.yml)
  regenerates the seeded sample, runs it across the Python/Java version
  matrix, merges the results, and commits the sample and merged data.

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
