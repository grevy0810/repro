# Reproducibility lab

The repository keeps the Java exercises in `tp1/` and the LLM-generated Python exercises and prompts in `tp2/llm/`. Generated answers are saved beside the corresponding exercise files.

## TP1 (Java)

From the repository root, compile and run the programs with Java 21 or later:

```bash
javac tp1/Associativity.java tp1/BankingProblem.java
./tp1/run.sh
```

The output files are `tp1/answer_associativity.txt` and `tp1/answer_banking.txt`.

To run TP1 in Docker:

```bash
docker build -f tp1/Dockerfile -t rep-lab2 .
docker run --rm --user "$(id -u):$(id -g)" \
  -v "$(pwd):/out" -e OUTPUT_DIR=/out/tp1 rep-lab2
```

## TP2 (LLM / Python)

The prompts, Python programs, and generated answers are in `tp2/llm/`. Run them from the repository root with:

```bash
python3 tp2/llm/associativity.py
python3 tp2/llm/banking.py
```

To run TP2 in Docker:

```bash
docker build -f tp2/llm/Dockerfile.llm -t rep-lab2-llm .
docker run --rm --user "$(id -u):$(id -g)" \
  -v "$(pwd):/out" -e OUTPUT_DIR=/out/tp2/llm rep-lab2-llm
```

## Reproduce TP1 with Nix

Install [Nix](https://nixos.org/download/), enter the project directory, and start the pinned development shell:

```bash
nix-shell
javac tp1/Associativity.java tp1/BankingProblem.java
./tp1/run.sh
```

