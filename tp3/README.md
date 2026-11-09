# TP3 — Part 5: reproducible sampling

`sample.py` draws valid configurations from `fm/experiment.uvl`. The three
`.csvconf` files in `configs/` add the implementations from TP1, TP2, and TP3
as anchor configurations, so they are always present in the sample.

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
The existing GitHub Actions workflow runs this same sampling command and
commits the generated CSV when it changes.

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
language runtime version, platform, and duration. For documented seeds, the
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
